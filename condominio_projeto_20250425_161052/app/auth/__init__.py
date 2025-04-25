"""
Módulo de autenticação para o site de controle de demandas do condomínio.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
from datetime import datetime

# Criar blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Importar módulo de banco de dados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database.sheets_api import SheetsDatabase

# Classe de usuário para Flask-Login
class User:
    def __init__(self, id, email, nome, tipo):
        self.id = id
        self.email = email
        self.nome = nome
        self.tipo = tipo  # 'condomino', 'sindico', 'administradora'
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        
    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id, db):
        """Obter usuário pelo ID."""
        user_data = db.get_user_by_id(user_id)
        if user_data:
            return User(
                user_data['id'],
                user_data['email'],
                user_data['nome'],
                user_data['tipo']
            )
        return None

# Rotas de autenticação
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login."""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validar inputs
        if not email or not senha:
            flash('Email e senha são obrigatórios', 'error')
            return render_template('auth/login.html')
        
        # Conectar ao banco de dados
        try:
            db = SheetsDatabase(
                os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
                os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
            )
            
            # Verificar usuário
            user_data = db.get_user_by_email(email)
            if user_data and check_password_hash(user_data['senha_hash'], senha):
                user = User(
                    user_data['id'],
                    user_data['email'],
                    user_data['nome'],
                    user_data['tipo']
                )
                login_user(user)
                
                # Redirecionar para a página solicitada ou para a página principal
                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('demandas.list')
                return redirect(next_page)
            
            flash('Email ou senha incorretos', 'error')
            
        except Exception as e:
            flash(f'Erro ao conectar ao banco de dados: {e}', 'error')
        
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """Rota de logout."""
    logout_user()
    flash('Você foi desconectado com sucesso', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de usuário."""
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Validar inputs
        if not email or not nome or not senha:
            flash('Todos os campos são obrigatórios', 'error')
            return render_template('auth/register.html')
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem', 'error')
            return render_template('auth/register.html')
        
        # Conectar ao banco de dados
        try:
            db = SheetsDatabase(
                os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
                os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
            )
            
            # Verificar se o email já existe
            existing_user = db.get_user_by_email(email)
            if existing_user:
                flash('Este email já está em uso', 'error')
                return render_template('auth/register.html')
            
            # Criar novo usuário
            user_data = {
                'email': email,
                'nome': nome,
                'senha_hash': generate_password_hash(senha),
                'tipo': 'condomino',  # Tipo padrão
                'data_criacao': datetime.now().strftime('%d/%m/%Y')
            }
            
            db.add_user(user_data)
            flash('Registro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'Erro ao registrar usuário: {e}', 'error')
        
    return render_template('auth/register.html')

# Função para inicializar o login_manager
def init_login_manager(login_manager, app):
    """Inicializar o gerenciador de login."""
    @login_manager.user_loader
    def load_user(user_id):
        try:
            db = SheetsDatabase(
                os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
                os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
            )
            return User.get(user_id, db)
        except Exception as e:
            app.logger.error(f"Erro ao carregar usuário: {e}")
            return None
