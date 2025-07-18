#!/bin/bash

# Script de deploy manual (sem Docker)
# Para hospedagens que não suportam Docker

echo "=== Deploy Manual - Sistema Instituto Metaforma ==="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# Criar ambiente virtual
echo "🔧 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r deploy_requirements.txt

# Criar diretório de configuração do Streamlit
mkdir -p ~/.streamlit/

# Configurar Streamlit
echo "⚙️  Configurando Streamlit..."
cat > ~/.streamlit/config.toml << EOL
[server]
headless = true
address = "0.0.0.0"
port = 8501
enableCORS = false

[theme]
primaryColor = "#1f4e79"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOL

# Criar arquivo de serviço systemd
echo "🔧 Criando serviço systemd..."
sudo tee /etc/systemd/system/metaforma.service > /dev/null << EOL
[Unit]
Description=Sistema Instituto Metaforma
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Habilitar e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable metaforma
sudo systemctl start metaforma

# Verificar status
echo "📊 Verificando status..."
sudo systemctl status metaforma

echo "✅ Sistema Instituto Metaforma instalado!"
echo "🌐 Acesse: http://seu-dominio.com:8501"
echo "📋 Cadastro Online: http://seu-dominio.com:8501/Cadastro_Online"
echo ""
echo "Comandos úteis:"
echo "  sudo systemctl start metaforma    # Iniciar"
echo "  sudo systemctl stop metaforma     # Parar"
echo "  sudo systemctl restart metaforma  # Reiniciar"
echo "  sudo systemctl status metaforma   # Ver status"
echo "  sudo journalctl -u metaforma -f   # Ver logs"