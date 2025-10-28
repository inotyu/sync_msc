import os
import sys

# Adicione o diretório do projeto ao path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Importa o app e o socketio depois de configurar o path
from app import app, socketio

# Define a aplicação para produção
application = app

# Se estiver executando diretamente, inicia o servidor
if __name__ == '__main__':
    print("Iniciando servidor com gevent e suporte a WebSockets...")
    # Força o uso de gevent-websocket
    from gevent import monkey
    monkey.patch_all()
    
    # Inicia o servidor
    socketio.run(
        app,
        host='0.0.0.0',
        port=80,
        debug=False,
        use_reloader=False,
        log_output=True,
        keyfile=None,
        certfile=None
    )
