from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import string
import random
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

# Configura o SocketIO para usar gevent com suporte a WebSockets
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    logger=True,
    engineio_logger=True,
    allow_upgrades=True,
    transports=['websocket', 'polling'],
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=100 * 1024 * 1024  # 100MB
)

# Armazenamento temporário das salas
salas = {}

def gerar_codigo_sala():
    """Gera um código único de 5 caracteres para a sala"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar-sala')
def criar_sala():
    codigo_sala = gerar_codigo_sala()
    while codigo_sala in salas:
        codigo_sala = gerar_codigo_sala()
    
    # Inicializa a sala
    salas[codigo_sala] = {
        'host': None,
        'participantes': {},
        'playlist': [],
        'video_atual': None,
        'indice_atual': -1,
        'tempo_atual': 0,
        'tocando': False,
        'timestamp_ultima_acao': datetime.now(),
        'criada_em': datetime.now()
    }
    
    session['codigo_sala'] = codigo_sala
    session['is_host'] = True
    return redirect(url_for('sala', codigo=codigo_sala))

@app.route('/entrar-sala', methods=['GET', 'POST'])
def entrar_sala():
    if request.method == 'POST':
        codigo_sala = request.form['codigo'].upper()
        if codigo_sala in salas:
            session['codigo_sala'] = codigo_sala
            session['is_host'] = False
            return redirect(url_for('sala', codigo=codigo_sala))
        else:
            return render_template('entrar_sala.html', erro='Sala não encontrada!')
    return render_template('entrar_sala.html')

@app.route('/sala/<codigo>')
def sala(codigo):
    if codigo not in salas:
        return redirect(url_for('index'))
    
    session['codigo_sala'] = codigo
    is_host = session.get('is_host', False)
    
    return render_template('sala.html', 
                         codigo_sala=codigo, 
                         is_host=is_host,
                         sala_data=salas[codigo])

# Eventos Socket.IO
@socketio.on('conectar_sala')
def conectar_sala(data):
    codigo_sala = data['codigo_sala']
    is_host = data['is_host']
    
    if codigo_sala not in salas:
        emit('erro', {'mensagem': 'Sala não encontrada'})
        return
    
    join_room(codigo_sala)
    
    # Adiciona participante à sala
    salas[codigo_sala]['participantes'][request.sid] = {
        'is_host': is_host,
        'conectado_em': datetime.now()
    }
    
    # Define o host se for o primeiro ou se é realmente o host
    if is_host:
        if salas[codigo_sala]['host'] is None:
            salas[codigo_sala]['host'] = request.sid
        else:
            # Atualiza o SID do host se ele reconectou
            salas[codigo_sala]['host'] = request.sid
    
    # Envia estado atual da sala para o novo participante
    emit('estado_sala', {
        'playlist': salas[codigo_sala]['playlist'],
        'video_atual': salas[codigo_sala]['video_atual'],
        'indice_atual': salas[codigo_sala]['indice_atual'],
        'tempo_atual': salas[codigo_sala]['tempo_atual'],
        'tocando': salas[codigo_sala]['tocando']
    })
    
    # Notifica outros participantes
    emit('participante_conectou', {
        'total_participantes': len(salas[codigo_sala]['participantes'])
    }, room=codigo_sala)

@socketio.on('adicionar_video')
def adicionar_video(data):
    codigo_sala = data['codigo_sala']
    video_id = data['video_id']
    
    print(f"[DEBUG] Tentativa de adicionar vídeo:")
    print(f"  - Sala: {codigo_sala}")
    print(f"  - Vídeo ID: {video_id}")
    print(f"  - Request SID: {request.sid}")
    print(f"  - Host atual: {salas.get(codigo_sala, {}).get('host', 'N/A')}")
    
    if codigo_sala not in salas:
        print(f"[ERROR] Sala {codigo_sala} não encontrada")
        return
    
    # Verifica se é o host
    current_host = salas[codigo_sala]['host']
    is_user_host = salas[codigo_sala]['participantes'].get(request.sid, {}).get('is_host', False)
    
    print(f"  - É host na sessão: {is_user_host}")
    
    if current_host != request.sid and not is_user_host:
        print(f"[ERROR] Usuário {request.sid} não é host. Host atual: {current_host}")
        emit('erro', {'mensagem': 'Apenas o host pode adicionar vídeos'})
        return
    
    # Se chegou aqui, atualiza o host SID se necessário
    if is_user_host and current_host != request.sid:
        salas[codigo_sala]['host'] = request.sid
        print(f"[INFO] Host SID atualizado para: {request.sid}")
    
    # Adiciona à playlist se não existir
    if video_id not in salas[codigo_sala]['playlist']:
        salas[codigo_sala]['playlist'].append(video_id)
        
        # Se é o primeiro vídeo, define como atual
        if len(salas[codigo_sala]['playlist']) == 1:
            salas[codigo_sala]['indice_atual'] = 0
            salas[codigo_sala]['video_atual'] = video_id
        
        # Atualiza todos os participantes
        emit('playlist_atualizada', {
            'playlist': salas[codigo_sala]['playlist'],
            'video_atual': salas[codigo_sala]['video_atual'],
            'indice_atual': salas[codigo_sala]['indice_atual']
        }, room=codigo_sala)

@socketio.on('remover_video')
def remover_video(data):
    codigo_sala = data['codigo_sala']
    video_id = data['video_id']
    
    print(f"[DEBUG] Tentativa de remover vídeo:")
    print(f"  - Sala: {codigo_sala}")
    print(f"  - Vídeo ID: {video_id}")
    
    if codigo_sala not in salas:
        return
    
    # Verifica se é o host
    current_host = salas[codigo_sala]['host']
    is_user_host = salas[codigo_sala]['participantes'].get(request.sid, {}).get('is_host', False)
    
    if current_host != request.sid and not is_user_host:
        return
    
    # Atualiza host SID se necessário
    if is_user_host and current_host != request.sid:
        salas[codigo_sala]['host'] = request.sid
    
    # Remove da playlist
    if video_id in salas[codigo_sala]['playlist']:
        indice_removido = salas[codigo_sala]['playlist'].index(video_id)
        salas[codigo_sala]['playlist'].remove(video_id)
        
        print(f"[INFO] Vídeo {video_id} removido da playlist")
        
        # Ajusta índice atual se necessário
        if indice_removido <= salas[codigo_sala]['indice_atual']:
            salas[codigo_sala]['indice_atual'] = max(0, salas[codigo_sala]['indice_atual'] - 1)
        
        # Se removeu o vídeo atual e ainda há vídeos, carrega o próximo
        if salas[codigo_sala]['playlist']:
            if salas[codigo_sala]['indice_atual'] >= len(salas[codigo_sala]['playlist']):
                salas[codigo_sala]['indice_atual'] = 0
            salas[codigo_sala]['video_atual'] = salas[codigo_sala]['playlist'][salas[codigo_sala]['indice_atual']]
        else:
            # Se não há mais vídeos
            salas[codigo_sala]['video_atual'] = None
            salas[codigo_sala]['indice_atual'] = -1
        
        # Atualiza todos os participantes
        emit('playlist_atualizada', {
            'playlist': salas[codigo_sala]['playlist'],
            'video_atual': salas[codigo_sala]['video_atual'],
            'indice_atual': salas[codigo_sala]['indice_atual']
        }, room=codigo_sala)

@socketio.on('importar_playlist')
def importar_playlist(data):
    codigo_sala = data['codigo_sala']
    playlist_id = data['playlist_id']
    
    print(f"[DEBUG] Tentativa de importar playlist:")
    print(f"  - Sala: {codigo_sala}")
    print(f"  - Playlist ID: {playlist_id}")
    
    if codigo_sala not in salas:
        emit('playlist_erro', {'mensagem': 'Sala não encontrada'})
        return
    
    # Verifica se é o host
    current_host = salas[codigo_sala]['host']
    is_user_host = salas[codigo_sala]['participantes'].get(request.sid, {}).get('is_host', False)
    
    if current_host != request.sid and not is_user_host:
        emit('playlist_erro', {'mensagem': 'Apenas o host pode importar playlists'})
        return
    
    # Atualiza host SID se necessário
    if is_user_host and current_host != request.sid:
        salas[codigo_sala]['host'] = request.sid
    
    try:
        # Método simples: usar regex na URL da playlist
        import requests
        import re
        
        playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
        
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"[INFO] Fazendo request para: {playlist_url}")
        response = requests.get(playlist_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise Exception(f"Erro HTTP {response.status_code}")
        
        # Extrai IDs de vídeo usando regex
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', response.text)
        
        # Remove duplicatas mantendo ordem
        unique_video_ids = []
        for video_id in video_ids:
            if video_id not in unique_video_ids:
                unique_video_ids.append(video_id)
        
        if not unique_video_ids:
            raise Exception("Nenhum vídeo encontrado na playlist")
        
        print(f"[INFO] Encontrados {len(unique_video_ids)} vídeos únicos")
        
        # Adiciona vídeos à playlist da sala
        videos_adicionados = 0
        for video_id in unique_video_ids[:50]:  # Limita a 50 vídeos
            if video_id not in salas[codigo_sala]['playlist']:
                salas[codigo_sala]['playlist'].append(video_id)
                videos_adicionados += 1
                
                # Se é o primeiro vídeo, define como atual
                if len(salas[codigo_sala]['playlist']) == 1:
                    salas[codigo_sala]['indice_atual'] = 0
                    salas[codigo_sala]['video_atual'] = video_id
        
        print(f"[INFO] {videos_adicionados} vídeos adicionados à playlist")
        
        # Atualiza todos os participantes
        emit('playlist_atualizada', {
            'playlist': salas[codigo_sala]['playlist'],
            'video_atual': salas[codigo_sala]['video_atual'],
            'indice_atual': salas[codigo_sala]['indice_atual']
        }, room=codigo_sala)
        
        # Confirma sucesso
        emit('playlist_importada', {
            'sucesso': True,
            'total_videos': videos_adicionados
        })
        
    except Exception as e:
        print(f"[ERROR] Erro ao importar playlist: {str(e)}")
        emit('playlist_erro', {
            'mensagem': f'Erro ao processar playlist: {str(e)}'
        })

@socketio.on('tocar_video')
def tocar_video(data):
    codigo_sala = data['codigo_sala']
    
    if codigo_sala not in salas:
        return
    
    # Verifica se é o host
    current_host = salas[codigo_sala]['host']
    is_user_host = salas[codigo_sala]['participantes'].get(request.sid, {}).get('is_host', False)
    
    if current_host != request.sid and not is_user_host:
        return
    
    # Atualiza host SID se necessário
    if is_user_host and current_host != request.sid:
        salas[codigo_sala]['host'] = request.sid
    
    salas[codigo_sala]['tocando'] = True
    salas[codigo_sala]['timestamp_ultima_acao'] = datetime.now()
    
    emit('video_tocando', {
        'tempo_atual': salas[codigo_sala]['tempo_atual']
    }, room=codigo_sala)

@socketio.on('pausar_video')
def pausar_video(data):
    codigo_sala = data['codigo_sala']
    tempo_atual = data.get('tempo_atual', 0)
    
    if codigo_sala not in salas:
        return
    
    # Verifica se é o host
    current_host = salas[codigo_sala]['host']
    is_user_host = salas[codigo_sala]['participantes'].get(request.sid, {}).get('is_host', False)
    
    if current_host != request.sid and not is_user_host:
        return
    
    # Atualiza host SID se necessário
    if is_user_host and current_host != request.sid:
        salas[codigo_sala]['host'] = request.sid
    
    salas[codigo_sala]['tocando'] = False
    salas[codigo_sala]['tempo_atual'] = tempo_atual
    salas[codigo_sala]['timestamp_ultima_acao'] = datetime.now()
    
    emit('video_pausado', {
        'tempo_atual': tempo_atual
    }, room=codigo_sala)

@socketio.on('pular_video')
def pular_video(data):
    codigo_sala = data['codigo_sala']
    
    if codigo_sala not in salas:
        return
    
    # Verifica se é o host
    if salas[codigo_sala]['host'] != request.sid:
        return
    
    sala = salas[codigo_sala]
    if sala['indice_atual'] < len(sala['playlist']) - 1:
        sala['indice_atual'] += 1
        sala['video_atual'] = sala['playlist'][sala['indice_atual']]
        sala['tempo_atual'] = 0
        sala['tocando'] = True  # Define como tocando
        sala['timestamp_ultima_acao'] = datetime.now()
        
        emit('video_alterado', {
            'video_atual': sala['video_atual'],
            'indice_atual': sala['indice_atual'],
            'tempo_atual': 0
        }, room=codigo_sala)
        
        # Emite comando para tocar
        emit('video_tocando', {
            'tempo_atual': 0
        }, room=codigo_sala)

@socketio.on('video_anterior')
def video_anterior(data):
    codigo_sala = data['codigo_sala']
    
    if codigo_sala not in salas:
        return
    
    # Verifica se é o host
    if salas[codigo_sala]['host'] != request.sid:
        return
    
    sala = salas[codigo_sala]
    if sala['indice_atual'] > 0:
        sala['indice_atual'] -= 1
        sala['video_atual'] = sala['playlist'][sala['indice_atual']]
        sala['tempo_atual'] = 0
        sala['tocando'] = True  # Define como tocando
        sala['timestamp_ultima_acao'] = datetime.now()
        
        emit('video_alterado', {
            'video_atual': sala['video_atual'],
            'indice_atual': sala['indice_atual'],
            'tempo_atual': 0
        }, room=codigo_sala)
        
        # Emite comando para tocar
        emit('video_tocando', {
            'tempo_atual': 0
        }, room=codigo_sala)

@socketio.on('ir_para_video')
def ir_para_video(data):
    codigo_sala = data['codigo_sala']
    indice = data['indice']
    
    print(f"[DEBUG] Tentativa de ir para vídeo:")
    print(f"  - Sala: {codigo_sala}")
    print(f"  - Índice: {indice}")
    
    if codigo_sala not in salas:
        return
    
    # Verifica se é o host
    current_host = salas[codigo_sala]['host']
    is_user_host = salas[codigo_sala]['participantes'].get(request.sid, {}).get('is_host', False)
    
    if current_host != request.sid and not is_user_host:
        return
    
    # Atualiza host SID se necessário
    if is_user_host and current_host != request.sid:
        salas[codigo_sala]['host'] = request.sid
    
    sala = salas[codigo_sala]
    
    # Verifica se o índice é válido
    if 0 <= indice < len(sala['playlist']):
        sala['indice_atual'] = indice
        sala['video_atual'] = sala['playlist'][indice]
        sala['tempo_atual'] = 0
        sala['tocando'] = True  # Define como tocando
        sala['timestamp_ultima_acao'] = datetime.now()
        
        print(f"[INFO] Mudando para vídeo no índice {indice}: {sala['video_atual']}")
        
        # Emite evento de mudança de vídeo
        emit('video_alterado', {
            'video_atual': sala['video_atual'],
            'indice_atual': sala['indice_atual'],
            'tempo_atual': 0
        }, room=codigo_sala)
        
        # Emite comando para tocar
        emit('video_tocando', {
            'tempo_atual': 0
        }, room=codigo_sala)

@socketio.on('sincronizar_tempo')
def sincronizar_tempo(data):
    codigo_sala = data['codigo_sala']
    tempo_atual = data['tempo_atual']
    
    if codigo_sala not in salas:
        return
    
    # Apenas o host pode sincronizar
    if salas[codigo_sala]['host'] == request.sid:
        salas[codigo_sala]['tempo_atual'] = tempo_atual
        salas[codigo_sala]['timestamp_ultima_acao'] = datetime.now()

@socketio.on('disconnect')
def desconectar():
    # Remove participante de todas as salas
    for codigo_sala, sala in salas.items():
        if request.sid in sala['participantes']:
            del sala['participantes'][request.sid]
            
            # Se era o host, transfere para outro participante
            if sala['host'] == request.sid and sala['participantes']:
                novo_host = next(iter(sala['participantes']))
                sala['host'] = novo_host
                sala['participantes'][novo_host]['is_host'] = True
                
                emit('novo_host', {'novo_host': True}, room=novo_host)
            
            # Notifica outros participantes
            emit('participante_desconectou', {
                'total_participantes': len(sala['participantes'])
            }, room=codigo_sala)
            
            break

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)
