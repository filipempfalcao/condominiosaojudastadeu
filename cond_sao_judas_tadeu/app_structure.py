"""
Estrutura básica da aplicação Flask para o site de controle de demandas do condomínio.
Este arquivo serve como um esqueleto para a implementação do backend.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Definição da estrutura básica da aplicação Flask
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
    from . import auth, demandas, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(demandas.bp)
    app.register_blueprint(dashboard.bp)

    # Definir a rota principal
    @app.route('/')
    def index():
        return redirect(url_for('demandas.list'))

    return app

# Modelo básico para integração com Google Sheets
class SheetsDatabase:
    def __init__(self, credentials_file, spreadsheet_name):
        # Definir escopo e credenciais
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        
        # Autorizar cliente
        self.client = gspread.authorize(credentials)
        
        # Abrir planilha
        self.spreadsheet = self.client.open(spreadsheet_name)
        
    def get_worksheet(self, name):
        """Obter uma planilha específica pelo nome."""
        try:
            return self.spreadsheet.worksheet(name)
        except gspread.exceptions.WorksheetNotFound:
            return self.spreadsheet.add_worksheet(title=name, rows=100, cols=20)
    
    def get_all_demandas(self):
        """Obter todas as demandas da planilha."""
        worksheet = self.get_worksheet('demandas')
        records = worksheet.get_all_records()
        return records
    
    def add_demanda(self, demanda_data):
        """Adicionar uma nova demanda à planilha."""
        worksheet = self.get_worksheet('demandas')
        worksheet.append_row([
            demanda_data.get('id'),
            demanda_data.get('titulo'),
            demanda_data.get('categoria'),
            demanda_data.get('criticidade'),
            demanda_data.get('descricao'),
            demanda_data.get('localizacao'),
            demanda_data.get('status'),
            demanda_data.get('data_criacao'),
            demanda_data.get('data_atualizacao')
        ])
        
    def update_demanda(self, demanda_id, demanda_data):
        """Atualizar uma demanda existente."""
        worksheet = self.get_worksheet('demandas')
        cell = worksheet.find(demanda_id)
        row = cell.row
        
        # Atualizar os dados na linha correspondente
        worksheet.update_cell(row, 2, demanda_data.get('titulo'))
        worksheet.update_cell(row, 3, demanda_data.get('categoria'))
        worksheet.update_cell(row, 4, demanda_data.get('criticidade'))
        worksheet.update_cell(row, 5, demanda_data.get('descricao'))
        worksheet.update_cell(row, 6, demanda_data.get('localizacao'))
        worksheet.update_cell(row, 7, demanda_data.get('status'))
        worksheet.update_cell(row, 9, demanda_data.get('data_atualizacao'))

# Modelo básico para usuário
class User(UserMixin):
    def __init__(self, id, email, nome, tipo):
        self.id = id
        self.email = email
        self.nome = nome
        self.tipo = tipo  # 'condomino', 'sindico', 'administradora'

# Modelo básico para demanda
class Demanda:
    def __init__(self, id, titulo, categoria, criticidade, descricao, localizacao, 
                 status='Aberta', data_criacao=None, data_atualizacao=None):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.criticidade = criticidade
        self.descricao = descricao
        self.localizacao = localizacao
        self.status = status
        self.data_criacao = data_criacao or datetime.now().strftime('%d/%m/%Y')
        self.data_atualizacao = data_atualizacao or self.data_criacao
        
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'categoria': self.categoria,
            'criticidade': self.criticidade,
            'descricao': self.descricao,
            'localizacao': self.localizacao,
            'status': self.status,
            'data_criacao': self.data_criacao,
            'data_atualizacao': self.data_atualizacao
        }

# Funções básicas para geração de gráficos com Plotly
def criar_grafico_demandas_por_status_categoria(demandas):
    """Criar gráfico unificado de demandas por status e categoria."""
    df = pd.DataFrame(demandas)
    
    # Contar demandas por status e categoria
    df_status = df.groupby(['status', 'categoria']).size().reset_index(name='quantidade')
    
    # Criar gráfico de barras
    fig = px.bar(
        df_status, 
        x='categoria', 
        y='quantidade', 
        color='status',
        title='Demandas por Status e Categoria',
        labels={'categoria': 'Categoria', 'quantidade': 'Quantidade', 'status': 'Status'},
        barmode='group'
    )
    
    return fig

def criar_grafico_evolucao_demandas(demandas):
    """Criar gráfico de evolução de demandas ao longo do tempo."""
    df = pd.DataFrame(demandas)
    
    # Converter datas para datetime
    df['data_criacao'] = pd.to_datetime(df['data_criacao'], format='%d/%m/%Y')
    
    # Agrupar por mês e contar
    df['mes'] = df['data_criacao'].dt.strftime('%m/%Y')
    df_evolucao = df.groupby(['mes', 'status']).size().reset_index(name='quantidade')
    
    # Criar gráfico de linha
    fig = px.line(
        df_evolucao,
        x='mes',
        y='quantidade',
        color='status',
        title='Evolução de Demandas',
        labels={'mes': 'Mês', 'quantidade': 'Quantidade', 'status': 'Status'},
        markers=True
    )
    
    return fig

def calcular_indicadores(demandas):
    """Calcular indicadores para o dashboard."""
    df = pd.DataFrame(demandas)
    
    # Total de demandas
    total_demandas = len(df)
    
    # Demandas abertas
    demandas_abertas = len(df[df['status'] != 'Resolvida'])
    
    # Tempo médio de resolução (para demandas resolvidas)
    df_resolvidas = df[df['status'] == 'Resolvida'].copy()
    if not df_resolvidas.empty:
        df_resolvidas['data_criacao'] = pd.to_datetime(df_resolvidas['data_criacao'], format='%d/%m/%Y')
        df_resolvidas['data_atualizacao'] = pd.to_datetime(df_resolvidas['data_atualizacao'], format='%d/%m/%Y')
        df_resolvidas['tempo_resolucao'] = (df_resolvidas['data_atualizacao'] - df_resolvidas['data_criacao']).dt.days
        tempo_medio_resolucao = df_resolvidas['tempo_resolucao'].mean()
    else:
        tempo_medio_resolucao = 0
    
    # Taxa de resolução
    if total_demandas > 0:
        taxa_resolucao = (len(df[df['status'] == 'Resolvida']) / total_demandas) * 100
    else:
        taxa_resolucao = 0
    
    return {
        'total_demandas': total_demandas,
        'demandas_abertas': demandas_abertas,
        'tempo_medio_resolucao': round(tempo_medio_resolucao, 1),
        'taxa_resolucao': round(taxa_resolucao, 1)
    }
