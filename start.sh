#!/bin/bash
# Instala as dependências
pip install --no-cache-dir -r requirements.txt

# Instala o gevent
pip install --no-cache-dir gevent

# Define a porta (a porta 80 geralmente requer privilégios de root)
PORT=${PORT:-5000}

echo "Iniciando o servidor na porta $PORT"

# Inicia o servidor
python -c "from app import app, socketio; socketio.run(app, host='0.0.0.0', port=$PORT, debug=False, log_output=True, allow_unsafe_werkzeug=True)"