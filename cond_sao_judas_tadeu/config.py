"""
Configurações da aplicação Flask para o site de controle de demandas do condomínio.
"""

import os

class Config:
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-desenvolvimento'
    
    # Configurações do Google Sheets
    GOOGLE_CREDENTIALS_FILE = os.environ.get('GOOGLE_CREDENTIALS_FILE') or 'credentials.json'
    SPREADSHEET_NAME = os.environ.get('SPREADSHEET_NAME') or 'Condominio_Sao_Judas_Tadeu'
    
    # Configurações de upload de arquivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limite para uploads
    
    # Configurações de autenticação
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos
    
    # Configurações de desenvolvimento
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Em produção, use uma chave secreta forte
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-producao'

# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
