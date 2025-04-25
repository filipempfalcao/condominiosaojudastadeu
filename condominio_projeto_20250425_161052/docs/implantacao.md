"""
Documentação de implantação para o site de controle de demandas do condomínio.
Este arquivo contém instruções para configurar e implantar a aplicação.
"""

# Guia de Implantação - Site de Controle de Demandas do Condomínio

## Requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Conta no Google para usar o Google Sheets
- Credenciais de API do Google para o Google Sheets

## 1. Configuração do Ambiente

### 1.1 Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd condominio_projeto
```

### 1.2 Criar e Ativar Ambiente Virtual

```bash
# No Linux/Mac
python3 -m venv venv
source venv/bin/activate

# No Windows
python -m venv venv
venv\Scripts\activate
```

### 1.3 Instalar Dependências

```bash
pip install -r requirements.txt
```

## 2. Configuração do Google Sheets

### 2.1 Criar Credenciais da API

1. Acesse o [Console de Desenvolvedores do Google](https://console.developers.google.com/)
2. Crie um novo projeto
3. Ative a API do Google Sheets e Google Drive
4. Crie credenciais de conta de serviço
5. Baixe o arquivo JSON de credenciais
6. Renomeie o arquivo para `credentials.json` e coloque-o na raiz do projeto

### 2.2 Configurar Planilha

1. Crie uma nova planilha no Google Sheets
2. Compartilhe a planilha com o email da conta de serviço (encontrado no arquivo de credenciais)
3. Anote o nome da planilha para usar nas configurações

## 3. Configuração da Aplicação

### 3.1 Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-aqui
GOOGLE_CREDENTIALS_FILE=credentials.json
SPREADSHEET_NAME=Nome_Da_Sua_Planilha
```

## 4. Opções de Implantação

### 4.1 Implantação Local

Para executar a aplicação localmente:

```bash
flask run --host=0.0.0.0
```

A aplicação estará disponível em `http://localhost:5000`

### 4.2 Implantação no PythonAnywhere (Gratuito)

1. Crie uma conta no [PythonAnywhere](https://www.pythonanywhere.com/)
2. Faça upload do código para o PythonAnywhere
3. Configure um novo aplicativo web:
   - Escolha Flask como framework
   - Configure o caminho para o arquivo WSGI
   - Configure o ambiente virtual
4. Faça upload do arquivo de credenciais
5. Configure as variáveis de ambiente

### 4.3 Implantação no Heroku

1. Crie uma conta no [Heroku](https://www.heroku.com/)
2. Instale o Heroku CLI
3. Crie um arquivo `Procfile` na raiz do projeto com o conteúdo:
   ```
   web: gunicorn run:app
   ```
4. Adicione `gunicorn` ao arquivo `requirements.txt`
5. Implante a aplicação:
   ```bash
   heroku login
   heroku create
   git push heroku main
   ```
6. Configure as variáveis de ambiente no Heroku

### 4.4 Implantação com GitHub Pages (Frontend) + Backend Separado

Para uma solução híbrida:

1. Extraia os arquivos estáticos (HTML, CSS, JS) para uma pasta separada
2. Implante esses arquivos no GitHub Pages
3. Implante o backend em um serviço como PythonAnywhere ou Heroku
4. Configure o frontend para acessar o backend via API

## 5. Manutenção

### 5.1 Backup

Recomenda-se fazer backup regular da planilha do Google Sheets.

### 5.2 Atualizações

Para atualizar a aplicação:

1. Faça pull das alterações mais recentes
2. Atualize as dependências:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
3. Reinicie a aplicação

## 6. Solução de Problemas

### 6.1 Problemas de Conexão com Google Sheets

- Verifique se o arquivo de credenciais está correto
- Verifique se a planilha foi compartilhada com a conta de serviço
- Verifique se as APIs do Google Sheets e Google Drive estão ativadas

### 6.2 Erros de Aplicação

- Verifique os logs da aplicação
- Verifique se todas as dependências estão instaladas
- Verifique se as variáveis de ambiente estão configuradas corretamente
