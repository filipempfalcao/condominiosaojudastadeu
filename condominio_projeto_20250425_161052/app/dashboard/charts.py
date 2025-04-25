"""
Módulo para integração do dashboard com os dados das demandas.
Este arquivo contém funções para processar dados e gerar visualizações para o dashboard.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

def processar_dados_demandas(demandas):
    """
    Processa os dados das demandas para uso no dashboard.
    
    Args:
        demandas: Lista de dicionários contendo os dados das demandas
        
    Returns:
        DataFrame pandas com os dados processados
    """
    if not demandas:
        return pd.DataFrame()
    
    # Converter para DataFrame
    df = pd.DataFrame(demandas)
    
    # Converter datas para datetime
    df['data_criacao'] = pd.to_datetime(df['data_criacao'], format='%d/%m/%Y')
    df['data_atualizacao'] = pd.to_datetime(df['data_atualizacao'], format='%d/%m/%Y')
    
    # Calcular tempo de resolução para demandas resolvidas
    df['tempo_resolucao'] = None
    mask_resolvidas = df['status'] == 'Resolvida'
    if mask_resolvidas.any():
        df.loc[mask_resolvidas, 'tempo_resolucao'] = (
            df.loc[mask_resolvidas, 'data_atualizacao'] - 
            df.loc[mask_resolvidas, 'data_criacao']
        ).dt.days
    
    return df

def filtrar_por_periodo(df, periodo):
    """
    Filtra o DataFrame por período.
    
    Args:
        df: DataFrame pandas com os dados das demandas
        periodo: String indicando o período de filtro
        
    Returns:
        DataFrame pandas filtrado
    """
    if df.empty or periodo == 'todos':
        return df
    
    hoje = datetime.now()
    
    if periodo == 'ultimos_7_dias':
        data_inicio = hoje - timedelta(days=7)
    elif periodo == 'ultimos_30_dias':
        data_inicio = hoje - timedelta(days=30)
    elif periodo == 'ultimos_90_dias':
        data_inicio = hoje - timedelta(days=90)
    elif periodo == 'ultimos_6_meses':
        data_inicio = hoje - timedelta(days=180)
    elif periodo == 'ultimo_ano':
        data_inicio = hoje - timedelta(days=365)
    else:
        return df
    
    return df[df['data_criacao'] >= data_inicio]

def calcular_indicadores(df, df_periodo_anterior=None):
    """
    Calcula os indicadores para o dashboard.
    
    Args:
        df: DataFrame pandas com os dados das demandas
        df_periodo_anterior: DataFrame pandas com os dados do período anterior (para comparação)
        
    Returns:
        Dicionário com os indicadores calculados
    """
    if df.empty:
        return {
            'total_demandas': 0,
            'demandas_abertas': 0,
            'tempo_medio_resolucao': 0,
            'taxa_resolucao': 0,
            'total_demandas_variacao': 0,
            'demandas_abertas_variacao': 0,
            'tempo_medio_resolucao_variacao': 0,
            'taxa_resolucao_variacao': 0
        }
    
    # Total de demandas
    total_demandas = len(df)
    
    # Demandas abertas
    demandas_abertas = len(df[df['status'] != 'Resolvida'])
    
    # Tempo médio de resolução
    df_resolvidas = df[df['status'] == 'Resolvida']
    tempo_medio_resolucao = df_resolvidas['tempo_resolucao'].mean() if not df_resolvidas.empty else 0
    
    # Taxa de resolução
    taxa_resolucao = (len(df_resolvidas) / total_demandas * 100) if total_demandas > 0 else 0
    
    # Calcular variações em relação ao período anterior
    variacoes = {
        'total_demandas_variacao': 0,
        'demandas_abertas_variacao': 0,
        'tempo_medio_resolucao_variacao': 0,
        'taxa_resolucao_variacao': 0
    }
    
    if df_periodo_anterior is not None and not df_periodo_anterior.empty:
        # Indicadores do período anterior
        total_anterior = len(df_periodo_anterior)
        abertas_anterior = len(df_periodo_anterior[df_periodo_anterior['status'] != 'Resolvida'])
        
        df_resolvidas_anterior = df_periodo_anterior[df_periodo_anterior['status'] == 'Resolvida']
        tempo_medio_anterior = df_resolvidas_anterior['tempo_resolucao'].mean() if not df_resolvidas_anterior.empty else 0
        
        taxa_anterior = (len(df_resolvidas_anterior) / total_anterior * 100) if total_anterior > 0 else 0
        
        # Calcular variações percentuais
        if total_anterior > 0:
            variacoes['total_demandas_variacao'] = ((total_demandas - total_anterior) / total_anterior) * 100
        
        if abertas_anterior > 0:
            variacoes['demandas_abertas_variacao'] = ((demandas_abertas - abertas_anterior) / abertas_anterior) * 100
        
        if tempo_medio_anterior > 0:
            variacoes['tempo_medio_resolucao_variacao'] = ((tempo_medio_resolucao - tempo_medio_anterior) / tempo_medio_anterior) * 100
        
        if taxa_anterior > 0:
            variacoes['taxa_resolucao_variacao'] = ((taxa_resolucao - taxa_anterior) / taxa_anterior) * 100
    
    return {
        'total_demandas': total_demandas,
        'demandas_abertas': demandas_abertas,
        'tempo_medio_resolucao': round(tempo_medio_resolucao, 1) if not pd.isna(tempo_medio_resolucao) else 0,
        'taxa_resolucao': round(taxa_resolucao, 1),
        'total_demandas_variacao': round(variacoes['total_demandas_variacao'], 1),
        'demandas_abertas_variacao': round(variacoes['demandas_abertas_variacao'], 1),
        'tempo_medio_resolucao_variacao': round(variacoes['tempo_medio_resolucao_variacao'], 1),
        'taxa_resolucao_variacao': round(variacoes['taxa_resolucao_variacao'], 1)
    }

def criar_grafico_unificado(df):
    """
    Cria o gráfico unificado para o dashboard.
    
    Args:
        df: DataFrame pandas com os dados das demandas
        
    Returns:
        Objeto JSON com os dados do gráfico
    """
    if df.empty:
        return {}
    
    # Preparar dados para gráfico de barras por status e categoria
    df_status_categoria = df.groupby(['status', 'categoria']).size().reset_index(name='quantidade')
    
    # Preparar dados para gráfico de evolução
    df['mes'] = df['data_criacao'].dt.strftime('%m/%Y')
    df_evolucao = df.groupby(['mes', 'status']).size().reset_index(name='quantidade')
    
    # Ordenar meses cronologicamente
    meses_ordenados = sorted(df['mes'].unique(), key=lambda x: datetime.strptime(x, '%m/%Y'))
    
    # Criar dados para o gráfico unificado
    grafico_data = {
        'status_categoria': df_status_categoria.to_dict('records'),
        'evolucao': df_evolucao.to_dict('records'),
        'meses_ordenados': meses_ordenados,
        'categorias': df['categoria'].unique().tolist(),
        'status': df['status'].unique().tolist()
    }
    
    return grafico_data

def gerar_figura_plotly(dados_grafico):
    """
    Gera uma figura Plotly a partir dos dados do gráfico unificado.
    
    Args:
        dados_grafico: Dicionário com os dados do gráfico
        
    Returns:
        Figura Plotly
    """
    if not dados_grafico or 'status_categoria' not in dados_grafico:
        # Retornar figura vazia
        fig = go.Figure()
        fig.update_layout(
            title="Não há dados suficientes para exibir o gráfico",
            xaxis_title="",
            yaxis_title=""
        )
        return fig
    
    # Preparar dados para o gráfico de barras por status e categoria
    traces = []
    
    # Agrupar por status
    status_grupos = {}
    for item in dados_grafico['status_categoria']:
        if item['status'] not in status_grupos:
            status_grupos[item['status']] = []
        status_grupos[item['status']].append(item)
    
    # Criar uma trace para cada status
    cores_status = {
        'Aberta': '#ff9800',  # Laranja
        'Em Análise': '#2196f3',  # Azul
        'Em Andamento': '#03a9f4',  # Azul claro
        'Aguardando Terceiros': '#9c27b0',  # Roxo
        'Resolvida': '#4caf50',  # Verde
        'Cancelada': '#f44336'   # Vermelho
    }
    
    for status, items in status_grupos.items():
        categorias = [item['categoria'] for item in items]
        quantidades = [item['quantidade'] for item in items]
        
        cor = cores_status.get(status, '#757575')  # Cinza como cor padrão
        
        traces.append(go.Bar(
            x=categorias,
            y=quantidades,
            name=status,
            marker_color=cor
        ))
    
    # Adicionar trace de linha para evolução de demandas
    if 'meses_ordenados' in dados_grafico and dados_grafico['meses_ordenados']:
        # Agrupar por status para evolução
        evolucao_grupos = {}
        for item in dados_grafico['evolucao']:
            if item['status'] not in evolucao_grupos:
                evolucao_grupos[item['status']] = {}
            evolucao_grupos[item['status']][item['mes']] = item['quantidade']
        
        # Criar uma trace de linha para cada status
        for status, valores_por_mes in evolucao_grupos.items():
            valores = [valores_por_mes.get(mes, 0) for mes in dados_grafico['meses_ordenados']]
            
            cor = cores_status.get(status, '#757575')
            
            traces.append(go.Scatter(
                x=dados_grafico['meses_ordenados'],
                y=valores,
                name=f"Evolução: {status}",
                mode='lines+markers',
                yaxis='y2',
                line=dict(color=cor, width=3),
                marker=dict(size=8)
            ))
    
    # Layout do gráfico
    layout = go.Layout(
        title="Demandas por Status, Categoria e Evolução",
        barmode='group',
        xaxis=dict(
            title="Categoria",
            tickangle=-45
        ),
        yaxis=dict(
            title="Quantidade",
            side='left'
        ),
        yaxis2=dict(
            title="Evolução",
            side='right',
            overlaying='y',
            showgrid=False
        ),
        legend=dict(
            orientation='h',
            y=-0.2
        ),
        margin=dict(
            l=50,
            r=50,
            t=50,
            b=100
        ),
        height=500,
        template='plotly_white'
    )
    
    # Criar a figura
    fig = go.Figure(data=traces, layout=layout)
    
    return fig

def exportar_figura_json(fig):
    """
    Exporta uma figura Plotly para JSON.
    
    Args:
        fig: Figura Plotly
        
    Returns:
        String JSON da figura
    """
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
