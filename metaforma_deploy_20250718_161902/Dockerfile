# Dockerfile para deploy do Sistema Instituto Metaforma
FROM python:3.11-slim

# Configurar diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY deploy_requirements.txt .

# Instalar dependências Python
RUN pip3 install -r deploy_requirements.txt

# Copiar código da aplicação
COPY . .

# Configurar Streamlit
RUN mkdir -p ~/.streamlit/
RUN echo "\
[server]\n\
headless = true\n\
address = '0.0.0.0'\n\
port = 8501\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor = '#1f4e79'\n\
backgroundColor = '#ffffff'\n\
secondaryBackgroundColor = '#f0f2f6'\n\
textColor = '#262730'\n\
" > ~/.streamlit/config.toml

# Expor porta
EXPOSE 8501

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]