# Preparação para Implantação Online

Este documento contém os passos necessários para preparar o site para implantação online usando GitHub Pages (frontend) e PythonAnywhere (backend).

## 1. Separação de Frontend e Backend

Para a implantação híbrida, precisamos separar o frontend do backend:

### 1.1 Estrutura do Frontend (GitHub Pages)

```
frontend/
├── css/              # Estilos CSS
│   └── style.css
├── js/               # Scripts JavaScript
│   ├── main.js
│   └── dashboard.js
├── index.html        # Página principal (redirecionamento para demandas)
├── demandas.html     # Página de listagem de demandas
├── nova-demanda.html # Formulário de nova demanda
├── detalhes.html     # Página de detalhes da demanda
├── dashboard.html    # Dashboard
├── login.html        # Página de login
└── register.html     # Página de registro
```

### 1.2 Estrutura do Backend (PythonAnywhere)

```
backend/
├── app/              # Aplicação Flask
│   ├── __init__.py
│   ├── config.py
│   ├── auth/
│   ├── demandas/
│   ├── dashboard/
│   └── database/
├── requirements.txt
└── app.py            # Ponto de entrada da aplicação
```

## 2. Adaptações Necessárias

### 2.1 Frontend

- Converter templates Flask para HTML estático
- Adicionar chamadas AJAX para API do backend
- Configurar URLs da API para apontar para o backend no PythonAnywhere
- Implementar gerenciamento de autenticação via localStorage/sessionStorage

### 2.2 Backend

- Configurar CORS para permitir requisições do GitHub Pages
- Implementar endpoints de API RESTful
- Configurar autenticação baseada em token (JWT)
- Otimizar para o ambiente PythonAnywhere

## 3. Passos para Implantação

### 3.1 GitHub Pages

1. Criar repositório no GitHub
2. Preparar arquivos estáticos do frontend
3. Configurar GitHub Pages no repositório
4. Testar acesso ao frontend

### 3.2 PythonAnywhere

1. Criar conta no PythonAnywhere
2. Configurar aplicação web Flask
3. Fazer upload dos arquivos do backend
4. Configurar variáveis de ambiente
5. Configurar arquivo WSGI
6. Testar API do backend

## 4. Integração e Testes

1. Testar comunicação entre frontend e backend
2. Verificar funcionalidades de autenticação
3. Testar CRUD de demandas
4. Verificar funcionamento do dashboard
5. Testar em diferentes dispositivos

## 5. Documentação Final

1. Atualizar README com instruções de acesso
2. Documentar URLs de acesso
3. Criar guia de manutenção
4. Documentar procedimentos de backup
