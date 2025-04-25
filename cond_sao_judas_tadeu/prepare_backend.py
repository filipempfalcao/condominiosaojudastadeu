"""
Script para preparar o backend para implantação no PythonAnywhere.
Este script adapta a aplicação Flask para funcionar como uma API RESTful.
"""

import os
import shutil
import json
import re
from pathlib import Path

# Configurações
BACKEND_DIR = "backend"
APP_DIR = "app"
FRONTEND_URL = "https://filipempfalcao.github.io/condominiosaojudastadeu"  # Será substituído pelo URL real do GitHub Pages

def create_directory_structure():
    """Cria a estrutura de diretórios para o backend."""
    # Criar diretório principal
    if os.path.exists(BACKEND_DIR):
        shutil.rmtree(BACKEND_DIR)
    os.makedirs(BACKEND_DIR)
    
    # Copiar diretório da aplicação
    shutil.copytree(APP_DIR, os.path.join(BACKEND_DIR, APP_DIR))
    
    print(f"Estrutura de diretórios criada em: {BACKEND_DIR}")

def create_wsgi_file():
    """Cria o arquivo WSGI para o PythonAnywhere."""
    wsgi_content = """import sys
import os

# Adicionar diretório do projeto ao path
path = '/home/seu_usuario/mysite'
if path not in sys.path:
    sys.path.append(path)

# Configurar variáveis de ambiente
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'sua-chave-secreta-aqui'
os.environ['GOOGLE_CREDENTIALS_FILE'] = 'credentials.json'
os.environ['SPREADSHEET_NAME'] = 'Condominio_Sao_Judas_Tadeu'
os.environ['FRONTEND_URL'] = '""" + FRONTEND_URL + """'

# Importar a aplicação
from app import create_app
application = create_app()
"""
    
    with open(os.path.join(BACKEND_DIR, "wsgi.py"), "w", encoding="utf-8") as f:
        f.write(wsgi_content)
    
    print("Criado: wsgi.py")

def create_app_py():
    """Cria o arquivo app.py para iniciar a aplicação."""
    app_py_content = """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
    
    with open(os.path.join(BACKEND_DIR, "app.py"), "w", encoding="utf-8") as f:
        f.write(app_py_content)
    
    print("Criado: app.py")

def update_init_py():
    """Atualiza o arquivo __init__.py para configurar CORS e JWT."""
    init_py_path = os.path.join(BACKEND_DIR, APP_DIR, "__init__.py")
    
    with open(init_py_path, "r", encoding="utf-8") as f:
        init_content = f.read()
    
    # Adicionar importações
    imports = """import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
"""
    
    # Substituir importações existentes
    init_content = init_content.replace("from flask import Flask", imports)
    
    # Adicionar configuração de CORS e JWT
    create_app_function = """def create_app(test_config=None):
    # Criar e configurar a aplicação
    app = Flask(__name__, instance_relative_config=True)
    
    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": os.environ.get('FRONTEND_URL', '*')}})
    
    # Configurar JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-jwt')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 horas
    jwt = JWTManager(app)
    
    # Configurações da aplicação
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        GOOGLE_CREDENTIALS_FILE=os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        SPREADSHEET_NAME=os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu'),
    )
    
    if test_config is None:
        # Carregar configuração da instância, se existir
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carregar configuração de teste
        app.config.from_mapping(test_config)
    
    # Registrar blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.demandas import bp as demandas_bp
    app.register_blueprint(demandas_bp)
    
    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    # Rota raiz
    @app.route('/')
    def index():
        return {'message': 'API do Condomínio São Judas Tadeu'}
    
    return app
"""
    
    # Substituir função create_app existente
    init_content = re.sub(r'def create_app\(.*?\):.*?return app', 
                         create_app_function, 
                         init_content, 
                         flags=re.DOTALL)
    
    # Salvar arquivo atualizado
    with open(init_py_path, "w", encoding="utf-8") as f:
        f.write(init_content)
    
    print("Atualizado: app/__init__.py")

def update_auth_module():
    """Atualiza o módulo de autenticação para usar JWT."""
    auth_init_path = os.path.join(BACKEND_DIR, APP_DIR, "auth", "__init__.py")
    
    with open(auth_init_path, "r", encoding="utf-8") as f:
        auth_content = f.read()
    
    # Adicionar importações
    imports = """from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
import sys
from werkzeug.security import generate_password_hash, check_password_hash

# Importar módulo de banco de dados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database.sheets_api import SheetsDatabase
"""
    
    # Substituir importações existentes
    auth_content = auth_content.replace("from flask import Blueprint", imports)
    
    # Atualizar blueprint
    auth_content = auth_content.replace("bp = Blueprint('auth', __name__)", 
                                      "bp = Blueprint('auth', __name__, url_prefix='/api/auth')")
    
    # Adicionar rotas de API
    api_routes = """
@bp.route('/login', methods=['POST'])
def login():
    # Login de usuário via API.
    if not request.is_json:
        return jsonify({"message": "Requisição inválida, JSON esperado"}), 400
    
    data = request.get_json()
    email = data.get('email', None)
    senha = data.get('senha', None)
    
    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios"}), 400
    
    # Conectar ao banco de dados
    db = SheetsDatabase(
        os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
    )
    
    # Verificar usuário
    usuario = db.get_usuario_by_email(email)
    
    if not usuario or not check_password_hash(usuario['senha'], senha):
        return jsonify({"message": "Email ou senha inválidos"}), 401
    
    # Criar token JWT
    access_token = create_access_token(identity={
        'id': usuario['id'],
        'email': usuario['email'],
        'nome': usuario['nome'],
        'tipo': usuario['tipo']
    })
    
    return jsonify({
        "message": "Login realizado com sucesso",
        "token": access_token,
        "usuario": {
            "id": usuario['id'],
            "email": usuario['email'],
            "nome": usuario['nome'],
            "tipo": usuario['tipo']
        }
    })

@bp.route('/register', methods=['POST'])
def register():
    # Registro de novo usuário via API.
    if not request.is_json:
        return jsonify({"message": "Requisição inválida, JSON esperado"}), 400
    
    data = request.get_json()
    nome = data.get('nome', None)
    email = data.get('email', None)
    senha = data.get('senha', None)
    
    if not nome or not email or not senha:
        return jsonify({"message": "Nome, email e senha são obrigatórios"}), 400
    
    # Conectar ao banco de dados
    db = SheetsDatabase(
        os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
    )
    
    # Verificar se usuário já existe
    usuario_existente = db.get_usuario_by_email(email)
    if usuario_existente:
        return jsonify({"message": "Email já cadastrado"}), 400
    
    # Criar novo usuário
    senha_hash = generate_password_hash(senha)
    novo_usuario = {
        'nome': nome,
        'email': email,
        'senha': senha_hash,
        'tipo': 'condomino'  # Por padrão, novos usuários são condôminos
    }
    
    usuario_id = db.add_usuario(novo_usuario)
    
    return jsonify({
        "message": "Usuário registrado com sucesso",
        "usuario": {
            "id": usuario_id,
            "email": email,
            "nome": nome,
            "tipo": 'condomino'
        }
    })

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    # Retorna informações do usuário autenticado.
    current_user = get_jwt_identity()
    return jsonify(current_user)
"""
    
    # Adicionar rotas de API ao final do arquivo
    auth_content += api_routes
    
    # Salvar arquivo atualizado
    with open(auth_init_path, "w", encoding="utf-8") as f:
        f.write(auth_content)
    
    print("Atualizado: app/auth/__init__.py")

def update_demandas_module():
    """Atualiza o módulo de demandas para usar API RESTful."""
    demandas_init_path = os.path.join(BACKEND_DIR, APP_DIR, "demandas", "__init__.py")
    
    with open(demandas_init_path, "r", encoding="utf-8") as f:
        demandas_content = f.read()
    
    # Adicionar importações
    imports = """from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import sys
from datetime import datetime

# Importar módulo de banco de dados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database.sheets_api import SheetsDatabase
"""
    
    # Substituir importações existentes
    demandas_content = demandas_content.replace("from flask import Blueprint", imports)
    
    # Atualizar blueprint
    demandas_content = demandas_content.replace("bp = Blueprint('demandas', __name__)", 
                                             "bp = Blueprint('demandas', __name__, url_prefix='/api/demandas')")
    
    # Adicionar rotas de API
    api_routes = """
@bp.route('/', methods=['GET'])
@jwt_required()
def list_demandas():
    # Lista de demandas via API.
    # Obter parâmetros de filtro
    status = request.args.get('status', 'Todos os Status')
    categoria = request.args.get('categoria', 'Todas as Categorias')
    criticidade = request.args.get('criticidade', 'Todas as Criticidades')
    busca = request.args.get('busca', '')
    page = int(request.args.get('page', 1))
    
    # Conectar ao banco de dados
    db = SheetsDatabase(
        os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
    )
    
    # Obter demandas filtradas
    demandas, total_pages = db.get_demandas_filtradas(
        status=status,
        categoria=categoria,
        criticidade=criticidade,
        busca=busca,
        page=page
    )
    
    return jsonify({
        "demandas": demandas,
        "total_pages": total_pages,
        "page": page,
        "filtros": {
            "status": status,
            "categoria": categoria,
            "criticidade": criticidade,
            "busca": busca
        }
    })

@bp.route('/<demanda_id>', methods=['GET'])
@jwt_required()
def get_demanda(demanda_id):
    # Obter detalhes de uma demanda via API.
    # Conectar ao banco de dados
    db = SheetsDatabase(
        os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
    )
    
    # Obter demanda
    demanda = db.get_demanda_by_id(demanda_id)
    
    if not demanda:
        return jsonify({"message": "Demanda não encontrada"}), 404
    
    return jsonify({"demanda": demanda})

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_demanda():
    # Criar nova demanda via API.
    if not request.is_json:
        return jsonify({"message": "Requisição inválida, JSON esperado"}), 400
    
    data = request.get_json()
    titulo = data.get('titulo', None)
    categoria = data.get('categoria', None)
    criticidade = data.get('criticidade', None)
    descricao = data.get('descricao', None)
    localizacao = data.get('localizacao', None)
    
    if not titulo or not categoria or not criticidade or not descricao or not localizacao:
        return jsonify({"message": "Todos os campos são obrigatórios"}), 400
    
    # Obter usuário atual
    current_user = get_jwt_identity()
    
    # Conectar ao banco de dados
    db = SheetsDatabase(
        os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
    )
    
    # Criar nova demanda
    nova_demanda = {
        'titulo': titulo,
        'categoria': categoria,
        'criticidade': criticidade,
        'descricao': descricao,
        'localizacao': localizacao,
        'status': 'Aberta',
        'data_criacao': datetime.now().strftime('%d/%m/%Y'),
        'data_atualizacao': datetime.now().strftime('%d/%m/%Y'),
        'usuario_id': current_user.get('id')
    }
    
    demanda_id = db.add_demanda(nova_demanda)
    nova_demanda['id'] = demanda_id
    
    return jsonify({
        "message": "Demanda criada com sucesso",
        "demanda": nova_demanda
    })

@bp.route('/<demanda_id>', methods=['PUT'])
@jwt_required()
def atualizar_demanda(demanda_id):
    # Atualizar demanda via API.
    if not request.is_json:
        return jsonify({"message": "Requisição inválida, JSON esperado"}), 400
    
    # Obter usuário atual
    current_user = get_jwt_identity()
    
    # Verificar permissão (apenas síndico e administradora podem editar)
    if current_user.get('tipo') not in ['sindico', 'administradora']:
        return jsonify({"message": "Permissão negada"}), 403
    
    # Conectar ao banco de dados
    db = SheetsDatabase(
        os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
    )
    
    # Obter demanda existente
    demanda = db.get_demanda_by_id(demanda_id)
    
    if not demanda:
        return jsonify({"message": "Demanda não encontrada"}), 404
    
    # Atualizar campos
    data = request.get_json()
    demanda['titulo'] = data.get('titulo', demanda['titulo'])
    demanda['categoria'] = data.get('categoria', demanda['categoria'])
    demanda['criticidade'] = data.get('criticidade', demanda['criticidade'])
    demanda['descricao'] = data.get('descricao', demanda['descricao'])
    demanda['localizacao'] = data.get('localizacao', demanda['localizacao'])
    demanda['status'] = data.get('status', demanda['status'])
    demanda['data_atualizacao'] = datetime.now().strftime('%d/%m/%Y')
    
    # Salvar demanda atualizada
    db.update_demanda(demanda_id, demanda)
    
    return jsonify({
        "message": "Demanda atualizada com sucesso",
        "demanda": demanda
    })

@bp.route('/<demanda_id>', methods=['DELETE'])
@jwt_required()
def excluir_demanda(demanda_id):
    # Excluir demanda via API.
    # Obter usuário atual
    current_user = get_jwt_identity()
    
    # Verificar permissão (apenas administradora pode excluir)
    if current_user.get('tipo') != 'administradora':
        return jsonify({"message": "Permissão negada"}), 403
    
    # Conectar ao banco de dados
    db = SheetsDatabase(
        os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
        os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
    )
    
    # Verificar se demanda existe
    demanda = db.get_demanda_by_id(demanda_id)
    
    if not demanda:
        return jsonify({"message": "Demanda não encontrada"}), 404
    
    # Excluir demanda
    db.delete_demanda(demanda_id)
    
    return jsonify({"message": "Demanda excluída com sucesso"})
"""
    
    # Adicionar rotas de API ao final do arquivo
    demandas_content += api_routes
    
    # Salvar arquivo atualizado
    with open(demandas_init_path, "w", encoding="utf-8") as f:
        f.write(demandas_content)
    
    print("Atualizado: app/demandas/__init__.py")

def update_dashboard_module():
    """Atualiza o módulo de dashboard para usar API RESTful."""
    dashboard_init_path = os.path.join(BACKEND_D
(Content truncated due to size limit. Use line ranges to read in chunks)