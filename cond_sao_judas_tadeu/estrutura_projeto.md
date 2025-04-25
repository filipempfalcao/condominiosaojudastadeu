# Estrutura do Projeto - Site de Controle de Demandas do Condomínio

## Arquitetura Geral

O projeto será desenvolvido utilizando uma arquitetura de aplicação web moderna, com separação clara entre frontend e backend, seguindo o padrão MVC (Model-View-Controller). A aplicação será construída com Flask como framework principal, aproveitando sua flexibilidade e simplicidade.

### Visão Geral da Arquitetura

```
Condomínio São Judas Tadeu
├── Frontend (HTML/CSS/JavaScript + Plotly)
│   ├── Páginas (Templates)
│   ├── Estilos (CSS)
│   └── Scripts (JavaScript)
│
├── Backend (Flask + Python)
│   ├── Rotas e Controladores
│   ├── Modelos de Dados
│   ├── Serviços
│   └── Autenticação
│
└── Banco de Dados (Google Sheets API)
    └── Integração via API
```

## Estrutura de Diretórios

```
condominio_app/
│
├── app/                      # Diretório principal da aplicação
│   ├── __init__.py           # Inicialização da aplicação Flask
│   ├── config.py             # Configurações da aplicação
│   │
│   ├── auth/                 # Módulo de autenticação
│   │   ├── __init__.py
│   │   ├── routes.py         # Rotas de autenticação
│   │   └── forms.py          # Formulários de login/registro
│   │
│   ├── demandas/             # Módulo de demandas
│   │   ├── __init__.py
│   │   ├── routes.py         # Rotas para gerenciamento de demandas
│   │   ├── forms.py          # Formulários para demandas
│   │   └── models.py         # Modelos de dados para demandas
│   │
│   ├── dashboard/            # Módulo de dashboard
│   │   ├── __init__.py
│   │   ├── routes.py         # Rotas para dashboard
│   │   └── charts.py         # Funções para geração de gráficos
│   │
│   ├── database/             # Módulo de banco de dados
│   │   ├── __init__.py
│   │   └── sheets_api.py     # Integração com Google Sheets
│   │
│   ├── static/               # Arquivos estáticos
│   │   ├── css/              # Estilos CSS
│   │   ├── js/               # Scripts JavaScript
│   │   └── images/           # Imagens
│   │
│   └── templates/            # Templates HTML
│       ├── base.html         # Template base
│       ├── auth/             # Templates de autenticação
│       ├── demandas/         # Templates de demandas
│       └── dashboard/        # Templates de dashboard
│
├── instance/                 # Configurações de instância (não versionadas)
│   └── config.py             # Configurações sensíveis (chaves API, etc.)
│
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_demandas.py
│   └── test_dashboard.py
│
├── venv/                     # Ambiente virtual Python (não versionado)
│
├── requirements.txt          # Dependências do projeto
├── run.py                    # Script para iniciar a aplicação
└── README.md                 # Documentação do projeto
```

## Componentes Principais

### 1. Backend (Flask)

#### Módulos Principais:

1. **Autenticação (auth)**
   - Sistema de login/logout para condôminos, administradora e síndico
   - Gerenciamento de sessões
   - Controle de acesso baseado em papéis

2. **Demandas (demandas)**
   - CRUD completo para demandas
   - Filtros e busca
   - Gerenciamento de status e categorias

3. **Dashboard (dashboard)**
   - Geração de gráficos com Plotly
   - Cálculo de métricas e indicadores
   - Filtros por período

4. **Banco de Dados (database)**
   - Integração com Google Sheets via API
   - Funções para leitura/escrita de dados
   - Cache para otimização de performance

### 2. Frontend

#### Tecnologias:

1. **HTML/CSS**
   - Bootstrap para responsividade
   - Design minimalista e leve

2. **JavaScript**
   - Interatividade na interface
   - Validação de formulários
   - Requisições assíncronas (AJAX)

3. **Plotly.js**
   - Visualização de dados no dashboard
   - Gráficos interativos

### 3. Integração com Google Sheets

A integração com o Google Sheets será implementada utilizando a biblioteca `gspread` do Python, que oferece uma interface simples para a API do Google Sheets. Esta abordagem permitirá:

1. Armazenar dados das demandas em planilhas
2. Atualizar informações em tempo real
3. Compartilhar dados facilmente entre usuários
4. Manter um histórico de alterações
5. Backup automático dos dados

## Fluxo de Dados

```
[Usuário] → [Interface Web] → [Flask Routes] → [Serviços Python] → [Google Sheets API]
                                                      ↑
                                                      ↓
                                              [Plotly (Gráficos)]
```

## Sistema de Autenticação

O sistema de autenticação será implementado utilizando Flask-Login, com os seguintes recursos:

1. Login com email/senha
2. Níveis de acesso:
   - Condômino: visualização e criação de demandas
   - Síndico: gerenciamento completo de demandas
   - Administradora: acesso total ao sistema

3. Proteção de rotas baseada em permissões
4. Sessões seguras com timeout

## Considerações de Segurança

1. Proteção contra CSRF (Cross-Site Request Forgery)
2. Sanitização de inputs
3. Armazenamento seguro de credenciais
4. Validação de dados em frontend e backend

## Estratégia de Implantação

Para a fase de desenvolvimento e validação, a aplicação será implantada utilizando:

1. **Frontend**: GitHub Pages
2. **Backend**: PythonAnywhere (plano gratuito) ou Heroku (plano gratuito)
3. **Banco de Dados**: Google Sheets (gratuito)

Esta estrutura permite uma implantação de baixo custo enquanto mantém a flexibilidade para escalar no futuro, se necessário.
