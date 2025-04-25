"""
Script para preparar os arquivos do frontend para implantação no GitHub Pages.
Este script converte os templates Flask em HTML estático e configura as chamadas de API.
"""

import os
import re
import shutil
import json
from pathlib import Path

# Configurações
BACKEND_URL = "https://seu-usuario.pythonanywhere.com/api"  # Será substituído pelo URL real
FRONTEND_DIR = "frontend"
TEMPLATES_DIR = "app/templates"
STATIC_DIR = "app/static"

def create_directory_structure():
    """Cria a estrutura de diretórios para o frontend."""
    # Criar diretório principal
    if os.path.exists(FRONTEND_DIR):
        shutil.rmtree(FRONTEND_DIR)
    os.makedirs(FRONTEND_DIR)
    
    # Criar subdiretórios
    os.makedirs(os.path.join(FRONTEND_DIR, "css"))
    os.makedirs(os.path.join(FRONTEND_DIR, "js"))
    os.makedirs(os.path.join(FRONTEND_DIR, "images"))
    
    print(f"Estrutura de diretórios criada em: {FRONTEND_DIR}")

def copy_static_files():
    """Copia arquivos estáticos (CSS, JS, imagens) para o diretório do frontend."""
    # Copiar CSS
    css_files = os.listdir(os.path.join(STATIC_DIR, "css"))
    for file in css_files:
        shutil.copy(
            os.path.join(STATIC_DIR, "css", file),
            os.path.join(FRONTEND_DIR, "css", file)
        )
    
    # Copiar JS
    js_files = os.listdir(os.path.join(STATIC_DIR, "js"))
    for file in js_files:
        shutil.copy(
            os.path.join(STATIC_DIR, "js", file),
            os.path.join(FRONTEND_DIR, "js", file)
        )
    
    # Copiar imagens (se existirem)
    if os.path.exists(os.path.join(STATIC_DIR, "images")):
        for file in os.listdir(os.path.join(STATIC_DIR, "images")):
            shutil.copy(
                os.path.join(STATIC_DIR, "images", file),
                os.path.join(FRONTEND_DIR, "images", file)
            )
    
    print("Arquivos estáticos copiados")

def convert_templates():
    """Converte templates Flask em HTML estático."""
    # Mapear templates para arquivos HTML
    template_mapping = {
        "base.html": None,  # Base não será convertido diretamente
        "auth/login.html": "login.html",
        "auth/register.html": "register.html",
        "demandas/list.html": "demandas.html",
        "demandas/nova.html": "nova-demanda.html",
        "demandas/detalhes.html": "detalhes.html",
        "dashboard/index.html": "dashboard.html"
    }
    
    # Ler o template base
    with open(os.path.join(TEMPLATES_DIR, "base.html"), "r", encoding="utf-8") as f:
        base_content = f.read()
    
    # Converter cada template
    for template_path, output_file in template_mapping.items():
        if output_file is None:
            continue
        
        # Ler o conteúdo do template
        full_template_path = os.path.join(TEMPLATES_DIR, template_path)
        with open(full_template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
        
        # Extrair o conteúdo do bloco
        content_match = re.search(r'{%\s*block\s+content\s*%}(.*?){%\s*endblock\s*%}', 
                                 template_content, re.DOTALL)
        if content_match:
            content = content_match.group(1)
        else:
            content = ""
        
        # Extrair o título
        title_match = re.search(r'{%\s*block\s+title\s*%}(.*?){%\s*endblock\s*%}', 
                               template_content, re.DOTALL)
        if title_match:
            title = title_match.group(1)
        else:
            title = "Condomínio São Judas Tadeu"
        
        # Substituir o bloco de conteúdo no template base
        html_content = base_content.replace('{% block title %}{% endblock %}', title)
        html_content = html_content.replace('{% block content %}{% endblock %}', content)
        
        # Substituir URLs Flask por URLs estáticos
        html_content = html_content.replace("{{ url_for('static', filename='", "")
        html_content = html_content.replace("') }}", "")
        html_content = html_content.replace("{{ url_for('index') }}", "index.html")
        html_content = html_content.replace("{{ url_for('auth.login') }}", "login.html")
        html_content = html_content.replace("{{ url_for('auth.register') }}", "register.html")
        html_content = html_content.replace("{{ url_for('auth.logout') }}", "login.html")
        html_content = html_content.replace("{{ url_for('demandas.list') }}", "demandas.html")
        html_content = html_content.replace("{{ url_for('demandas.nova') }}", "nova-demanda.html")
        html_content = html_content.replace("{{ url_for('demandas.detalhes', demanda_id=demanda.id) }}", "detalhes.html?id={{ demanda.id }}")
        html_content = html_content.replace("{{ url_for('dashboard.index') }}", "dashboard.html")
        
        # Remover lógica Jinja
        html_content = re.sub(r'{%\s*if.*?%}.*?{%\s*endif\s*%}', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'{%\s*for.*?%}.*?{%\s*endfor\s*%}', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'{{\s*.*?\s*}}', '', html_content)
        
        # Adicionar script para API
        api_script = f"""
        <script>
            // Configuração da API
            const API_URL = "{BACKEND_URL}";
            
            // Função para verificar autenticação
            function checkAuth() {{
                const token = localStorage.getItem('auth_token');
                if (!token && window.location.pathname !== '/login.html' && window.location.pathname !== '/register.html') {{
                    window.location.href = 'login.html';
                }}
            }}
            
            // Verificar autenticação ao carregar a página
            document.addEventListener('DOMContentLoaded', checkAuth);
        </script>
        """
        
        html_content = html_content.replace('</body>', f'{api_script}\n</body>')
        
        # Salvar o arquivo HTML
        output_path = os.path.join(FRONTEND_DIR, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Convertido: {template_path} -> {output_file}")
    
    # Criar index.html (redirecionamento para demandas.html)
    index_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Condomínio São Judas Tadeu</title>
    <meta http-equiv="refresh" content="0;url=demandas.html">
    <script>
        window.location.href = "demandas.html";
    </script>
</head>
<body>
    <p>Redirecionando para <a href="demandas.html">demandas</a>...</p>
</body>
</html>
"""
    
    with open(os.path.join(FRONTEND_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    
    print("Criado: index.html")

def create_api_js():
    """Cria arquivo JavaScript para comunicação com a API."""
    api_js = f"""/**
 * API para comunicação com o backend
 */

const API_URL = "{BACKEND_URL}";

// Função para obter token de autenticação
function getAuthToken() {{
    return localStorage.getItem('auth_token');
}}

// Função para definir token de autenticação
function setAuthToken(token) {{
    localStorage.setItem('auth_token', token);
}}

// Função para remover token de autenticação
function removeAuthToken() {{
    localStorage.removeItem('auth_token');
}}

// Função para verificar se o usuário está autenticado
function isAuthenticated() {{
    return !!getAuthToken();
}}

// Função para fazer login
async function login(email, senha) {{
    try {{
        const response = await fetch(`${{API_URL}}/auth/login`, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ email, senha }})
        }});
        
        const data = await response.json();
        
        if (response.ok) {{
            setAuthToken(data.token);
            return {{ success: true }};
        }} else {{
            return {{ success: false, message: data.message || 'Erro ao fazer login' }};
        }}
    }} catch (error) {{
        console.error('Erro ao fazer login:', error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}

// Função para fazer logout
function logout() {{
    removeAuthToken();
    window.location.href = 'login.html';
}}

// Função para registrar novo usuário
async function register(nome, email, senha) {{
    try {{
        const response = await fetch(`${{API_URL}}/auth/register`, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ nome, email, senha }})
        }});
        
        const data = await response.json();
        
        if (response.ok) {{
            return {{ success: true }};
        }} else {{
            return {{ success: false, message: data.message || 'Erro ao registrar' }};
        }}
    }} catch (error) {{
        console.error('Erro ao registrar:', error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}

// Função para obter lista de demandas
async function getDemandas(filtros = {{}}) {{
    try {{
        const token = getAuthToken();
        if (!token) return {{ success: false, message: 'Não autenticado' }};
        
        // Construir query string com filtros
        const queryParams = new URLSearchParams();
        Object.keys(filtros).forEach(key => {{
            if (filtros[key]) queryParams.append(key, filtros[key]);
        }});
        
        const response = await fetch(`${{API_URL}}/demandas?${{queryParams}}`, {{
            headers: {{
                'Authorization': `Bearer ${{token}}`
            }}
        }});
        
        const data = await response.json();
        
        if (response.ok) {{
            return {{ success: true, demandas: data.demandas, total_pages: data.total_pages }};
        }} else {{
            return {{ success: false, message: data.message || 'Erro ao obter demandas' }};
        }}
    }} catch (error) {{
        console.error('Erro ao obter demandas:', error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}

// Função para obter detalhes de uma demanda
async function getDemanda(id) {{
    try {{
        const token = getAuthToken();
        if (!token) return {{ success: false, message: 'Não autenticado' }};
        
        const response = await fetch(`${{API_URL}}/demandas/${{id}}`, {{
            headers: {{
                'Authorization': `Bearer ${{token}}`
            }}
        }});
        
        const data = await response.json();
        
        if (response.ok) {{
            return {{ success: true, demanda: data.demanda }};
        }} else {{
            return {{ success: false, message: data.message || 'Erro ao obter demanda' }};
        }}
    }} catch (error) {{
        console.error(`Erro ao obter demanda ${{id}}:`, error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}

// Função para criar nova demanda
async function criarDemanda(demanda) {{
    try {{
        const token = getAuthToken();
        if (!token) return {{ success: false, message: 'Não autenticado' }};
        
        const response = await fetch(`${{API_URL}}/demandas`, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${{token}}`
            }},
            body: JSON.stringify(demanda)
        }});
        
        const data = await response.json();
        
        if (response.ok) {{
            return {{ success: true, demanda: data.demanda }};
        }} else {{
            return {{ success: false, message: data.message || 'Erro ao criar demanda' }};
        }}
    }} catch (error) {{
        console.error('Erro ao criar demanda:', error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}

// Função para atualizar demanda
async function atualizarDemanda(id, demanda) {{
    try {{
        const token = getAuthToken();
        if (!token) return {{ success: false, message: 'Não autenticado' }};
        
        const response = await fetch(`${{API_URL}}/demandas/${{id}}`, {{
            method: 'PUT',
            headers: {{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${{token}}`
            }},
            body: JSON.stringify(demanda)
        }});
        
        const data = await response.json();
        
        if (response.ok) {{
            return {{ success: true, demanda: data.demanda }};
        }} else {{
            return {{ success: false, message: data.message || 'Erro ao atualizar demanda' }};
        }}
    }} catch (error) {{
        console.error(`Erro ao atualizar demanda ${{id}}:`, error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}

// Função para excluir demanda
async function excluirDemanda(id) {{
    try {{
        const token = getAuthToken();
        if (!token) return {{ success: false, message: 'Não autenticado' }};
        
        const response = await fetch(`${{API_URL}}/demandas/${{id}}`, {{
            method: 'DELETE',
            headers: {{
                'Authorization': `Bearer ${{token}}`
            }}
        }});
        
        const data = await response.json();
        
        if (response.ok) {{
            return {{ success: true }};
        }} else {{
            return {{ success: false, message: data.message || 'Erro ao excluir demanda' }};
        }}
    }} catch (error) {{
        console.error(`Erro ao excluir demanda ${{id}}:`, error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}

// Função para obter dados do dashboard
async function getDashboardData(periodo = 'ultimos_30_dias') {{
    try {{
        const token = getAuthToken();
        if (!token) return {{ success: false, message: 'Não autenticado' }};
        
        // Obter indicadores
        const indicadoresResponse = await fetch(`${{API_URL}}/dashboard/indicadores?periodo=${{periodo}}`, {{
            headers: {{
                'Authorization': `Bearer ${{token}}`
            }}
        }});
        
        const indicadoresData = await indicadoresResponse.json();
        
        // Obter dados do gráfico
        const graficoResponse = await fetch(`${{API_URL}}/dashboard/grafico_unificado?periodo=${{periodo}}`, {{
            headers: {{
                'Authorization': `Bearer ${{token}}`
            }}
        }});
        
        const graficoData = await graficoResponse.json();
        
        if (indicadoresResponse.ok && graficoResponse.ok) {{
            return {{
                success: true,
                indicadores: indicadoresData,
                grafico: graficoData
            }};
        }} else {{
            return {{ 
                success: false, 
                message: indicadoresData.message || graficoData.message || 'Erro ao obter dados do dashboard' 
            }};
        }}
    }} catch (error) {{
        console.error('Erro ao obter dados do dashboard:', error);
        return {{ success: false, message: 'Erro de conexão' }};
    }}
}}
"""
    
    with open(os.path.join(FRONTEND_DIR, "js", "api.js"), "w", encoding="utf-8") as f:
        f.write(api_js)
    
    print("Criado: js/api.js")

def update_js_files():
    """Atualiza arquivos JavaScript para usar a API."""
    # Atualizar main.js para usar a API
    main_js_path = os.path.join(FRONTEND_DIR, "js", "main.js")
    with open(main_js_path, "r", encoding="utf-8") as f:
        main_js = f.read()
    
    # Adicionar importação da API
    main_js = f'// Importar API\ndocument.write(\'<script src="js/api.js"></script>\');\n\n{main_js}'
    
    # Salvar arquivo atualizado
    with open(main_js_path, "w", encoding="utf-8") as f:
        f.write(main_js)
    
    print("Atualizado: js/mai
(Content truncated due to size limit. Use line ranges to read in chunks)