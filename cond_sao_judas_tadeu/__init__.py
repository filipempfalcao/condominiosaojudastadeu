"""
Inicialização da aplicação Flask para o site de controle de demandas do condomínio.
"""

from flask import Flask, redirect, url_for
from flask_login import LoginManager
import os

def create_app(test_config=None):
    # Criar e configurar a aplicação
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # Substituir por chave secreta em produção
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )

    if test_config is None:
        # Carregar a configuração da instância, se existir
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carregar a configuração de teste
        app.config.from_mapping(test_config)

    # Garantir que o diretório de instância existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializar o sistema de login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Registrar blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.demandas import bp as demandas_bp
    app.register_blueprint(demandas_bp)
    
    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Definir a rota principal
    @app.route('/')
    def index():
        return redirect(url_for('demandas.list'))

    return app
