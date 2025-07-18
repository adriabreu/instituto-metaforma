#!/bin/bash

# Script de deploy para Sistema Instituto Metaforma
# Execute este script na sua hospedagem

echo "=== Deploy Sistema Instituto Metaforma ==="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instalando Docker..."
    
    # Instalar Docker no Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Adicionar usuário ao grupo docker
    sudo usermod -aG docker $USER
    echo "✅ Docker instalado. Reinicie o terminal e execute novamente."
    exit 1
fi

# Verificar se docker-compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Instalando..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose instalado."
fi

# Parar containers existentes
echo "🔄 Parando containers existentes..."
docker-compose down

# Construir nova imagem
echo "🏗️  Construindo nova imagem..."
docker-compose build

# Iniciar aplicação
echo "🚀 Iniciando aplicação..."
docker-compose up -d

# Aguardar aplicação ficar pronta
echo "⏳ Aguardando aplicação ficar pronta..."
sleep 30

# Verificar se está funcionando
if curl -f http://localhost:8501/healthz &> /dev/null; then
    echo "✅ Sistema Instituto Metaforma está funcionando!"
    echo "🌐 Acesse: http://seu-dominio.com:8501"
    echo "📋 Cadastro Online: http://seu-dominio.com:8501/Cadastro_Online"
else
    echo "❌ Erro ao iniciar a aplicação. Verificando logs..."
    docker-compose logs
fi

echo "=== Deploy concluído ==="