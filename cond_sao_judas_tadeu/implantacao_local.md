# Guia de Implantação Local - Site de Controle de Demandas do Condomínio

Este guia contém instruções detalhadas para configurar e executar o site de controle de demandas do condomínio em seu ambiente local para testes.

## Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Conta no Google para usar o Google Sheets
- Credenciais de API do Google para o Google Sheets

## 1. Configuração do Ambiente

### 1.1 Baixar o Código

Baixe o código do projeto e extraia-o para uma pasta em seu computador.

### 1.2 Criar e Ativar Ambiente Virtual

Abra um terminal ou prompt de comando na pasta do projeto e execute:

```bash
# No Linux/Mac
python3 -m venv venv
source venv/bin/activate

# No Windows
python -m venv venv
venv\Scripts\activate
```

### 1.3 Instalar Dependências

Com o ambiente virtual ativado, instale as dependências:

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
FLASK_ENV=development
SECRET_KEY=chave-secreta-para-desenvolvimento
GOOGLE_CREDENTIALS_FILE=credentials.json
SPREADSHEET_NAME=Nome_Da_Sua_Planilha
```

Substitua `Nome_Da_Sua_Planilha` pelo nome da planilha que você criou no Google Sheets.

## 4. Executar a Aplicação

Com o ambiente virtual ativado, execute:

```bash
flask run --host=0.0.0.0
```

A aplicação estará disponível em `http://localhost:5000`

## 5. Acessar o Site

Abra um navegador e acesse `http://localhost:5000`

### 5.1 Criar um Usuário

1. Acesse a página de registro (`http://localhost:5000/auth/register`)
2. Preencha o formulário com seus dados
3. Faça login com as credenciais criadas

## 6. Testar Funcionalidades

### 6.1 Gerenciamento de Demandas

- Crie novas demandas
- Visualize a lista de demandas
- Teste os filtros por status, categoria e criticidade
- Acesse os detalhes das demandas

### 6.2 Dashboard

- Acesse o dashboard
- Verifique se os indicadores são exibidos corretamente
- Teste o filtro por período
- Verifique se o gráfico unificado é exibido corretamente

## 7. Solução de Problemas

### 7.1 Problemas de Conexão com Google Sheets

- Verifique se o arquivo de credenciais está correto
- Verifique se a planilha foi compartilhada com a conta de serviço
- Verifique se as APIs do Google Sheets e Google Drive estão ativadas

### 7.2 Erros de Aplicação

- Verifique os logs da aplicação no terminal
- Verifique se todas as dependências estão instaladas
- Verifique se as variáveis de ambiente estão configuradas corretamente

## 8. Próximos Passos

Após validar o funcionamento local, podemos prosseguir com a implantação online usando GitHub Pages + PythonAnywhere conforme planejado.
