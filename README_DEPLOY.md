# 🚀 Deploy do Sistema Instituto Metaforma

## Instruções para Hospedar na Sua Hospedagem

### 📋 Pré-requisitos

- Servidor Linux (Ubuntu/Debian recomendado)
- Acesso SSH ao servidor
- Domínio configurado (opcional)

### 🔧 Opção 1: Deploy com Docker (Recomendado)

1. **Fazer upload dos arquivos** para o servidor:
   ```bash
   # Copiar todos os arquivos do projeto para o servidor
   scp -r * usuario@seu-servidor.com:/home/usuario/metaforma/
   ```

2. **Conectar ao servidor** via SSH:
   ```bash
   ssh usuario@seu-servidor.com
   cd /home/usuario/metaforma/
   ```

3. **Executar o script de deploy**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Configurar proxy reverso** (Nginx):
   ```nginx
   server {
       listen 80;
       server_name metaforma.com.br;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

### 🔧 Opção 2: Deploy Manual (Sem Docker)

1. **Fazer upload dos arquivos** para o servidor

2. **Executar o script manual**:
   ```bash
   chmod +x deploy_manual.sh
   ./deploy_manual.sh
   ```

### 🌐 Configuração do Domínio

1. **Apontar domínio** para o IP do servidor
2. **Configurar Nginx** como proxy reverso
3. **Instalar SSL** (Let's Encrypt):
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d metaforma.com.br
   ```

### 📊 URLs Importantes

- **Sistema Principal**: `http://metaforma.com.br`
- **Cadastro Online**: `http://metaforma.com.br/Cadastro_Online`
- **Dashboard**: `http://metaforma.com.br/Dashboard_Financeiro`
- **Conciliação**: `http://metaforma.com.br/Conciliacao_Bancaria`

### 🔍 Monitoramento

**Verificar status:**
```bash
# Com Docker
docker-compose ps
docker-compose logs

# Manual
sudo systemctl status metaforma
sudo journalctl -u metaforma -f
```

### 🔒 Segurança

1. **Alterar senha admin** no arquivo `pages/9_Cadastro_Online.py`
2. **Configurar firewall**:
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

### 🆘 Solução de Problemas

**Erro de porta ocupada:**
```bash
sudo netstat -tulpn | grep :8501
sudo kill -9 <PID>
```

**Erro de permissão:**
```bash
sudo chown -R $USER:$USER /home/usuario/metaforma/
chmod +x *.sh
```

**Logs detalhados:**
```bash
# Docker
docker-compose logs -f

# Manual
tail -f ~/.streamlit/logs/streamlit.log
```

### 📞 Suporte

Para suporte técnico:
- Verifique os logs de erro
- Confirme se todas as dependências estão instaladas
- Teste o acesso local primeiro (localhost:8501)

### 🔄 Atualizações

Para atualizar o sistema:
1. Fazer backup do banco de dados
2. Fazer upload dos novos arquivos
3. Reexecutar o script de deploy
4. Verificar se tudo está funcionando

---

**✅ Seu sistema estará disponível 24/7 na sua hospedagem!**