# Guia de Implantação Online - Site de Controle de Demandas do Condomínio

Este guia contém instruções detalhadas para implantar o site de controle de demandas do condomínio online usando GitHub Pages (frontend) e PythonAnywhere (backend).

## 1. Implantação do Frontend no GitHub Pages

### 1.1 Preparação do Repositório

1. Acesse sua conta no GitHub (https://github.com/)
2. Crie um novo repositório chamado `condominiosaojudastadeu` (ou use o repositório existente)
3. Clone o repositório para sua máquina local ou use a interface web do GitHub para upload

### 1.2 Upload dos Arquivos do Frontend

1. Navegue até a pasta `frontend` gerada pelo script de preparação
2. Faça upload de todos os arquivos desta pasta para o repositório GitHub:
   - Se estiver usando Git localmente:
     ```bash
     cd frontend
     git init
     git add .
     git commit -m "Adicionar arquivos do frontend"
     git remote add origin https://github.com/seu-usuario/condominiosaojudastadeu.git
     git push -u origin main
     ```
   - Se estiver usando a interface web do GitHub:
     - Acesse seu repositório no GitHub
     - Clique em "Add file" > "Upload files"
     - Arraste todos os arquivos da pasta `frontend` ou selecione-os manualmente
     - Clique em "Commit changes"

### 1.3 Ativar GitHub Pages

1. Acesse seu repositório no GitHub
2. Clique em "Settings" (aba de configurações)
3. Role para baixo até a seção "GitHub Pages"
4. Em "Source", selecione a branch principal (main ou master)
5. Clique em "Save"
6. Aguarde alguns minutos para que o site seja publicado
7. O GitHub fornecerá uma URL (geralmente no formato `https://seu-usuario.github.io/condominiosaojudastadeu/`)

## 2. Implantação do Backend no PythonAnywhere

### 2.1 Criar Conta no PythonAnywhere

1. Acesse https://www.pythonanywhere.com/
2. Crie uma conta gratuita (ou faça login se já tiver uma)

### 2.2 Configurar Aplicação Web

1. Após fazer login, acesse o Dashboard do PythonAnywhere
2. Clique em "Web" na barra de navegação superior
3. Clique em "Add a new web app"
4. Escolha o domínio gratuito (geralmente `seu-usuario.pythonanywhere.com`)
5. Selecione "Flask" como framework
6. Escolha a versão mais recente do Python (3.8 ou superior)
7. Configure o caminho para o arquivo WSGI como `/home/seu-usuario/mysite/wsgi.py`

### 2.3 Upload dos Arquivos do Backend

1. No Dashboard do PythonAnywhere, clique em "Files" na barra de navegação superior
2. Navegue até a pasta `/home/seu-usuario/mysite/`
3. Faça upload de todos os arquivos da pasta `backend` gerada pelo script de preparação:
   - Você pode fazer upload dos arquivos individualmente ou criar um arquivo ZIP
   - Se criar um ZIP, faça upload e depois descompacte usando o console do PythonAnywhere

### 2.4 Configurar Ambiente Virtual

1. No Dashboard do PythonAnywhere, clique em "Consoles" na barra de navegação superior
2. Inicie um novo console Bash
3. Execute os seguintes comandos:
   ```bash
   cd /home/seu-usuario/mysite
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 2.5 Configurar Credenciais do Google Sheets

1. Crie um projeto no Google Cloud Console e obtenha um arquivo de credenciais JSON
2. Faça upload do arquivo de credenciais para `/home/seu-usuario/mysite/credentials.json`
3. Crie uma planilha no Google Sheets para armazenar os dados
4. Compartilhe a planilha com o email da conta de serviço (encontrado no arquivo de credenciais)

### 2.6 Configurar Variáveis de Ambiente

1. No Dashboard do PythonAnywhere, clique em "Web" na barra de navegação superior
2. Role até a seção "WSGI configuration file" e clique no link para editar o arquivo
3. Atualize as variáveis de ambiente no arquivo WSGI:
   ```python
   # Configurar variáveis de ambiente
   os.environ['FLASK_ENV'] = 'production'
   os.environ['SECRET_KEY'] = 'sua-chave-secreta-aqui'  # Substitua por uma chave segura
   os.environ['GOOGLE_CREDENTIALS_FILE'] = 'credentials.json'
   os.environ['SPREADSHEET_NAME'] = 'Nome_Da_Sua_Planilha'  # Substitua pelo nome da sua planilha
   os.environ['FRONTEND_URL'] = 'https://seu-usuario.github.io/condominiosaojudastadeu'  # Substitua pela URL do seu GitHub Pages
   ```
4. Salve o arquivo

### 2.7 Reiniciar a Aplicação Web

1. No Dashboard do PythonAnywhere, clique em "Web" na barra de navegação superior
2. Clique no botão "Reload" para reiniciar a aplicação web

## 3. Integração do Frontend com o Backend

### 3.1 Atualizar URL da API no Frontend

1. Acesse seu repositório no GitHub
2. Edite o arquivo `js/api.js`
3. Atualize a constante `API_URL` com a URL do seu backend no PythonAnywhere:
   ```javascript
   const API_URL = "https://seu-usuario.pythonanywhere.com/api";
   ```
4. Salve as alterações

## 4. Teste da Implantação

### 4.1 Testar o Frontend

1. Acesse a URL do GitHub Pages (https://seu-usuario.github.io/condominiosaojudastadeu/)
2. Verifique se a página inicial carrega corretamente
3. Tente registrar um novo usuário
4. Faça login com o usuário registrado

### 4.2 Testar o Backend

1. Acesse a URL do backend (https://seu-usuario.pythonanywhere.com/)
2. Verifique se a mensagem "API do Condomínio São Judas Tadeu" é exibida
3. Teste os endpoints da API usando ferramentas como Postman ou o próprio navegador

### 4.3 Testar a Integração

1. Após fazer login no frontend, verifique se é possível:
   - Visualizar a lista de demandas
   - Criar novas demandas
   - Visualizar o dashboard

## 5. Manutenção e Atualizações

### 5.1 Atualizar o Frontend

1. Faça as alterações necessárias nos arquivos do frontend
2. Faça upload das alterações para o repositório GitHub
3. O GitHub Pages atualizará automaticamente o site

### 5.2 Atualizar o Backend

1. Faça as alterações necessárias nos arquivos do backend
2. Faça upload das alterações para o PythonAnywhere
3. Reinicie a aplicação web no PythonAnywhere

## 6. Solução de Problemas

### 6.1 Problemas no Frontend

- Verifique o console do navegador para erros JavaScript
- Verifique se a URL da API está configurada corretamente
- Verifique se o GitHub Pages está ativado e funcionando

### 6.2 Problemas no Backend

- Verifique os logs de erro no PythonAnywhere
- Verifique se as variáveis de ambiente estão configuradas corretamente
- Verifique se o arquivo de credenciais do Google Sheets está correto
- Verifique se a planilha foi compartilhada com a conta de serviço
