"""
Atualização do módulo de dashboard para integrar com as funções de visualização.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import os
import sys
import json
from datetime import datetime, timedelta

# Criar blueprint
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Importar módulo de banco de dados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database.sheets_api import SheetsDatabase
from app.dashboard.charts import (
    processar_dados_demandas, 
    filtrar_por_periodo, 
    calcular_indicadores, 
    criar_grafico_unificado,
    gerar_figura_plotly,
    exportar_figura_json
)

# Rotas para dashboard
@bp.route('/')
@login_required
def index():
    """Página principal do dashboard."""
    return render_template('dashboard/index.html')

@bp.route('/api/indicadores')
@login_required
def api_indicadores():
    """API para obter indicadores do dashboard."""
    try:
        # Conectar ao banco de dados
        db = SheetsDatabase(
            os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
            os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
        )
        
        # Obter período do filtro
        periodo = request.args.get('periodo', 'ultimos_30_dias')
        
        # Obter todas as demandas
        demandas = db.get_all_demandas()
        
        # Processar dados
        df = processar_dados_demandas(demandas)
        
        # Definir período atual e anterior
        hoje = datetime.now()
        
        if periodo == 'ultimos_7_dias':
            data_inicio_atual = hoje - timedelta(days=7)
            data_inicio_anterior = hoje - timedelta(days=14)
            data_fim_anterior = data_inicio_atual
        elif periodo == 'ultimos_30_dias':
            data_inicio_atual = hoje - timedelta(days=30)
            data_inicio_anterior = hoje - timedelta(days=60)
            data_fim_anterior = data_inicio_atual
        elif periodo == 'ultimos_90_dias':
            data_inicio_atual = hoje - timedelta(days=90)
            data_inicio_anterior = hoje - timedelta(days=180)
            data_fim_anterior = data_inicio_atual
        elif periodo == 'ultimos_6_meses':
            data_inicio_atual = hoje - timedelta(days=180)
            data_inicio_anterior = hoje - timedelta(days=360)
            data_fim_anterior = data_inicio_atual
        elif periodo == 'ultimo_ano':
            data_inicio_atual = hoje - timedelta(days=365)
            data_inicio_anterior = hoje - timedelta(days=730)
            data_fim_anterior = data_inicio_atual
        else:  # todos
            data_inicio_atual = datetime.min
            data_inicio_anterior = None
            data_fim_anterior = None
        
        # Filtrar dados para período atual
        df_atual = df[df['data_criacao'] >= data_inicio_atual] if not df.empty else df
        
        # Filtrar dados para período anterior
        df_anterior = None
        if data_inicio_anterior is not None and data_fim_anterior is not None:
            df_anterior = df[(df['data_criacao'] >= data_inicio_anterior) & 
                             (df['data_criacao'] < data_fim_anterior)] if not df.empty else None
        
        # Calcular indicadores
        indicadores = calcular_indicadores(df_atual, df_anterior)
        
        return jsonify(indicadores)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/grafico_unificado')
@login_required
def api_grafico_unificado():
    """API para obter dados do gráfico unificado."""
    try:
        # Conectar ao banco de dados
        db = SheetsDatabase(
            os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
            os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
        )
        
        # Obter período do filtro
        periodo = request.args.get('periodo', 'ultimos_30_dias')
        
        # Obter todas as demandas
        demandas = db.get_all_demandas()
        
        # Processar dados
        df = processar_dados_demandas(demandas)
        
        # Filtrar por período
        df_filtrado = filtrar_por_periodo(df, periodo)
        
        # Criar dados para o gráfico unificado
        grafico_data = criar_grafico_unificado(df_filtrado)
        
        # Gerar figura Plotly
        fig = gerar_figura_plotly(grafico_data)
        
        # Exportar figura para JSON
        fig_json = exportar_figura_json(fig)
        
        # Adicionar dados brutos para uso no frontend
        response_data = {
            'figura_json': fig_json,
            'dados_brutos': grafico_data
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
