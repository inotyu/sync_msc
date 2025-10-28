# 🎵 SyncMusic - Player Sincronizado

Sistema de reprodução de música do YouTube sincronizada em tempo real para ouvir com amigos!

## 🚀 Funcionalidades

- **Salas Privadas**: Códigos únicos de 5 caracteres
- **Host Control**: Apenas o host pode controlar a reprodução
- **Sincronização Real**: Todos ouvem no mesmo momento
- **Auto-Sync**: Novos participantes sincronizam automaticamente
- **Playlist Compartilhada**: Adicione músicas do YouTube
- **Interface Responsiva**: Funciona em desktop e mobile

## 📋 Como Usar

### 1. Instalação
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python app.py
```

### 2. Acessar o Sistema
- Abra `http://localhost:5000` no navegador
- Escolha "Criar Sala" ou "Entrar em Sala"

### 3. Como Host
1. Clique em "Criar Nova Sala"
2. Compartilhe o código da sala com seus amigos
3. Adicione músicas do YouTube colando o link
4. Use os controles para tocar, pausar, pular músicas
5. Todos os ouvintes serão sincronizados automaticamente

### 4. Como Ouvinte
1. Clique em "Entrar em Sala"
2. Digite o código de 5 caracteres da sala
3. Você será sincronizado automaticamente com o host
4. Relaxe e ouça! 🎧

## 🎛️ Controles

### Host (🎛️)
- ▶️ **Tocar/Pausar**: Controla reprodução para todos
- ⏭️ **Pular**: Avança para próxima música
- ⏮️ **Anterior**: Volta para música anterior
- ➕ **Adicionar**: Adiciona músicas à playlist
- 🔄 **Auto-Skip**: Próxima música toca automaticamente

### Ouvinte (🎧)
- 👂 **Escuta Sincronizada**: Áudio sincronizado automaticamente
- 📱 **Visualização**: Vê playlist e música atual
- 🔄 **Auto-Sync**: Sincroniza mesmo entrando no meio da música

## 🔧 Tecnologias

- **Backend**: Flask + Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript
- **Player**: YouTube IFrame API
- **Comunicação**: Socket.IO (tempo real)
- **Sincronização**: Timestamps precisos

## 🎨 Interface

- **Tema**: Roxo e preto (mantido do original)
- **Responsiva**: Funciona em qualquer dispositivo
- **Intuitiva**: Interface clara para host vs ouvinte
- **Visual**: Miniaturas dos vídeos e playlist

## 🔒 Recursos de Sala

- **Códigos Únicos**: Cada sala tem código de 5 caracteres
- **Transferência de Host**: Se host sair, outro vira host
- **Participantes Online**: Contador em tempo real
- **Persistência**: Salas ficam ativas enquanto há participantes

## 🎵 Easter Egg

O easter egg original foi mantido! Experimente adicionar links com certas palavras especiais... 😉

## 🚨 Notas Importantes

1. **Conexão**: Todos precisam estar conectados à internet
2. **Navegador**: Use Chrome, Firefox ou Edge (suporte ao YouTube API)
3. **Firewall**: Porta 5000 deve estar liberada
4. **Performance**: Recomendado máximo 10 pessoas por sala

## 🔧 Configuração Avançada

Para usar em rede local ou servidor:
```python
# No app.py, altere a linha final:
socketio.run(app, debug=False, host='0.0.0.0', port=5000)
```

## 📱 Compatibilidade

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Edge
- ✅ Safari (iOS/macOS)
- ✅ Mobile browsers

---

**Divirta-se ouvindo música sincronizada com seus amigos! 🎉**
