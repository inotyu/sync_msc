# Sync Music Player 🎵

### Select Your Language / Selecione seu Idioma
[![English](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg/50px-Flag_of_the_United_Kingdom_%283-5%29.svg.png)](#-english-instructions)  
[![Português](https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/45px-Flag_of_Brazil.svg.png)](#-instruções-em-português)

## 🇬🇧 English Instructions

### 🚀 Overview
Sync Music Player is a web application that allows multiple users to create and share synchronized YouTube playlists in real-time. Built with Python (Flask) and JavaScript, it provides a seamless experience for collaborative music listening.

### ✨ Features
- Real-time playlist synchronization
- Multiple user rooms for collaborative listening
- Intuitive playback controls
- Responsive design for all devices
- YouTube video integration

### 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/inotyu/sync_msc.git
   cd sync_msc
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

### 🎮 Usage
1. Open the application in your web browser
2. Create a new room or join an existing one
3. Add YouTube video URLs to the playlist
4. Control playback for all users in the room

## 🇧🇷 Instruções em Português

### 🚀 Visão Geral
O Sync Music Player é uma aplicação web que permite que múltiplos usuários criem e compartilhem playlists do YouTube sincronizadas em tempo real. Desenvolvido com Python (Flask) e JavaScript, oferece uma experiência fluida para escuta colaborativa de músicas.

### ✨ Recursos
- Sincronização de playlist em tempo real
- Salas para múltiplos usuários
- Controles intuitivos de reprodução
- Design responsivo
- Integração com vídeos do YouTube

### 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/inotyu/sync_msc.git
   cd sync_msc
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   python app.py
   ```
   A aplicação estará disponível em `http://localhost:5000`

### 🎮 Como Usar
1. Abra a aplicação no navegador
2. Crie uma nova sala ou entre em uma existente
3. Adicione vídeos do YouTube à playlist
4. Controle a reprodução para todos os usuários da sala

### 📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### 👥 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. **Instale as dependências necessárias:**

   Este projeto não requer dependências adicionais em Python, mas você precisará de:
   - Google Chrome ou Mozilla Firefox
   - Um editor de texto ou IDE (como o VSCode)

4. **Configure o projeto:**

   Simplesmente abra o arquivo `index.html` no seu navegador preferido. O projeto depende da API do YouTube, então uma conexão com a internet é necessária para carregar e reproduzir os vídeos.

5. **Uso:**

   - Adicione links de vídeos do YouTube no campo de entrada e clique em "Carregar Vídeo" para adicioná-los à sua playlist.
   - Use os controles de reprodução para tocar, pausar e parar o vídeo.
   - Use os botões "Próximo" e "Anterior" para navegar pela playlist.
   - Use os controles de paginação para navegar por várias páginas da playlist.
