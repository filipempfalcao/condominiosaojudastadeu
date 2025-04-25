# Site de Controle de Demandas do Condomínio São Judas Tadeu

Este projeto é uma aplicação web desenvolvida em Python/Flask para gerenciamento de demandas de condomínio, com dashboard integrado e visualização de dados.

## Visão Geral

O site permite o controle transparente de demandas do condomínio, com recursos para:

- Cadastro e gerenciamento de demandas
- Classificação por criticidade, categoria e status
- Dashboard com indicadores e gráficos dinâmicos
- Sistema de autenticação para condôminos, síndico e administradora

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS, JavaScript
- **Banco de Dados**: Google Sheets (via API)
- **Visualização de Dados**: Plotly
- **Autenticação**: Flask-Login

## Estrutura do Projeto

```
condominio_projeto/
├── app/                      # Diretório principal da aplicação
│   ├── __init__.py           # Inicialização da aplicação Flask
│   ├── config.py             # Configurações da aplicação
│   ├── auth/                 # Módulo de autenticação
│   ├── demandas/             # Módulo de demandas
│   ├── dashboard/            # Módulo de dashboard
│   ├── database/             # Módulo de banco de dados
│   ├── static/               # Arquivos estáticos (CSS, JS, imagens)
│   └── templates/            # Templates HTML
├── docs/                     # Documentação
│   ├── implantacao.md        # Guia de implantação
│   └── implantacao_local.md  # Guia de implantação local
├── tests/                    # Testes automatizados
├── requirements.txt          # Dependências do projeto
├── run.py                    # Script para iniciar a aplicação
└── run_tests.py              # Script para executar testes
```

## Funcionalidades Principais

### Controle de Demandas
- Cadastro de novas demandas
- Listagem com filtros por status, categoria e criticidade
- Detalhes completos de cada demanda
- Atualização de status e informações

### Dashboard
- Indicadores de desempenho (total de demandas, abertas, tempo médio de resolução)
- Gráfico unificado de demandas por status, categoria e evolução
- Filtros por período para análise temporal

### Autenticação
- Registro de novos usuários
- Login seguro
- Níveis de acesso diferenciados (condômino, síndico, administradora)

## Instalação e Execução

Consulte os guias de implantação na pasta `docs/`:
- [Implantação Local](docs/implantacao_local.md) - Para testes em ambiente local
- [Implantação](docs/implantacao.md) - Para implantação em ambiente de produção

## Requisitos

Veja o arquivo [requirements.txt](requirements.txt) para a lista completa de dependências.

## Testes

Execute os testes automatizados com:

```bash
python run_tests.py
```

## Licença

Este projeto é para uso exclusivo do Condomínio São Judas Tadeu.

## Contato

Para suporte ou dúvidas, entre em contato com o desenvolvedor.
