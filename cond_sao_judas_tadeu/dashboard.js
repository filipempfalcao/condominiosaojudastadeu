/**
 * Script específico para o dashboard
 * Responsável por carregar e renderizar os gráficos com Plotly
 */

// Função para inicializar o dashboard
function initDashboard() {
  // Carregar indicadores
  loadIndicadores();
  
  // Carregar gráfico unificado
  loadGraficoUnificado();
  
  // Inicializar seletor de período
  const periodoSelect = document.getElementById('periodo-select');
  if (periodoSelect) {
    periodoSelect.addEventListener('change', () => {
      loadIndicadores();
      loadGraficoUnificado();
    });
  }
}

// Função para carregar indicadores do dashboard
async function loadIndicadores() {
  const indicadoresContainer = document.getElementById('indicadores-container');
  const periodoSelect = document.getElementById('periodo-select');
  
  if (!indicadoresContainer) return;
  
  try {
    // Mostrar indicador de carregamento
    indicadoresContainer.querySelectorAll('.indicator-card').forEach(card => {
      card.classList.add('loading');
    });
    
    const periodo = periodoSelect ? periodoSelect.value : 'ultimos_30_dias';
    const response = await fetch(`/dashboard/api/indicadores?periodo=${periodo}`);
    const data = await response.json();
    
    if (data.error) {
      console.error('Erro ao carregar indicadores:', data.error);
      return;
    }
    
    // Atualizar indicadores
    updateIndicador('total-demandas', data.total_demandas, data.total_demandas_variacao);
    updateIndicador('demandas-abertas', data.demandas_abertas, data.demandas_abertas_variacao);
    updateIndicador('tempo-medio-resolucao', data.tempo_medio_resolucao, data.tempo_medio_resolucao_variacao, ' dias');
    updateIndicador('taxa-resolucao', data.taxa_resolucao, data.taxa_resolucao_variacao, '%');
    
    // Remover indicador de carregamento
    indicadoresContainer.querySelectorAll('.indicator-card').forEach(card => {
      card.classList.remove('loading');
    });
    
  } catch (error) {
    console.error('Erro ao carregar indicadores:', error);
    
    // Remover indicador de carregamento em caso de erro
    indicadoresContainer.querySelectorAll('.indicator-card').forEach(card => {
      card.classList.remove('loading');
    });
  }
}

// Função para atualizar um indicador específico
function updateIndicador(id, valor, variacao, sufixo = '') {
  const indicador = document.getElementById(id);
  if (!indicador) return;
  
  const valorElement = indicador.querySelector('.indicator-value');
  const variacaoElement = indicador.querySelector('.indicator-variation');
  
  if (valorElement) {
    valorElement.textContent = valor + sufixo;
  }
  
  if (variacaoElement && variacao !== undefined) {
    const isPositive = variacao > 0;
    const isNegative = variacao < 0;
    
    variacaoElement.textContent = `${isPositive ? '+' : ''}${variacao}%`;
    variacaoElement.className = 'indicator-variation';
    
    if (isPositive) {
      variacaoElement.classList.add('variation-positive');
    } else if (isNegative) {
      variacaoElement.classList.add('variation-negative');
    }
  }
}

// Função para carregar o gráfico unificado
async function loadGraficoUnificado() {
  const graficoContainer = document.getElementById('grafico-unificado');
  const periodoSelect = document.getElementById('periodo-select');
  
  if (!graficoContainer) return;
  
  try {
    // Mostrar indicador de carregamento
    graficoContainer.innerHTML = '<div class="loading-spinner">Carregando gráfico...</div>';
    
    const periodo = periodoSelect ? periodoSelect.value : 'ultimos_30_dias';
    const response = await fetch(`/dashboard/api/grafico_unificado?periodo=${periodo}`);
    const data = await response.json();
    
    if (data.error) {
      console.error('Erro ao carregar gráfico unificado:', data.error);
      graficoContainer.innerHTML = '<p class="error-message">Erro ao carregar o gráfico.</p>';
      return;
    }
    
    // Renderizar gráfico com Plotly
    if (data.figura_json) {
      const figuraObj = JSON.parse(data.figura_json);
      Plotly.newPlot(graficoContainer, figuraObj.data, figuraObj.layout);
    } else if (data.dados_brutos) {
      // Fallback para renderização no cliente
      renderizarGraficoCliente(graficoContainer, data.dados_brutos);
    } else {
      graficoContainer.innerHTML = '<p>Não há dados suficientes para exibir o gráfico.</p>';
    }
    
  } catch (error) {
    console.error('Erro ao carregar gráfico unificado:', error);
    graficoContainer.innerHTML = '<p class="error-message">Erro ao carregar o gráfico.</p>';
  }
}

// Função para renderizar o gráfico no cliente (fallback)
function renderizarGraficoCliente(container, dados) {
  if (!dados || !dados.status_categoria || !dados.evolucao) {
    container.innerHTML = '<p>Não há dados suficientes para exibir o gráfico.</p>';
    return;
  }
  
  // Preparar dados para o gráfico de barras por status e categoria
  const traces = [];
  
  // Agrupar por status
  const statusGroups = {};
  dados.status_categoria.forEach(item => {
    if (!statusGroups[item.status]) {
      statusGroups[item.status] = [];
    }
    statusGroups[item.status].push(item);
  });
  
  // Cores para status
  const coresStatus = {
    'Aberta': '#ff9800',
    'Em Análise': '#2196f3',
    'Em Andamento': '#03a9f4',
    'Aguardando Terceiros': '#9c27b0',
    'Resolvida': '#4caf50',
    'Cancelada': '#f44336'
  };
  
  // Criar uma trace para cada status
  Object.keys(statusGroups).forEach(status => {
    const items = statusGroups[status];
    
    traces.push({
      x: items.map(item => item.categoria),
      y: items.map(item => item.quantidade),
      name: status,
      type: 'bar',
      marker: {
        color: coresStatus[status] || '#757575'
      }
    });
  });
  
  // Adicionar trace de linha para evolução de demandas
  if (dados.meses_ordenados && dados.meses_ordenados.length > 0) {
    // Agrupar por status para evolução
    const evolucaoGroups = {};
    dados.evolucao.forEach(item => {
      if (!evolucaoGroups[item.status]) {
        evolucaoGroups[item.status] = {};
      }
      evolucaoGroups[item.status][item.mes] = item.quantidade;
    });
    
    // Criar uma trace de linha para cada status
    Object.keys(evolucaoGroups).forEach(status => {
      const values = dados.meses_ordenados.map(mes => evolucaoGroups[status][mes] || 0);
      
      traces.push({
        x: dados.meses_ordenados,
        y: values,
        name: `Evolução: ${status}`,
        type: 'scatter',
        mode: 'lines+markers',
        yaxis: 'y2',
        line: {
          color: coresStatus[status] || '#757575',
          width: 3
        },
        marker: {
          size: 8
        }
      });
    });
  }
  
  // Layout do gráfico
  const layout = {
    title: 'Demandas por Status, Categoria e Evolução',
    barmode: 'group',
    xaxis: {
      title: 'Categoria',
      tickangle: -45
    },
    yaxis: {
      title: 'Quantidade',
      side: 'left'
    },
    yaxis2: {
      title: 'Evolução',
      side: 'right',
      overlaying: 'y',
      showgrid: false
    },
    legend: {
      orientation: 'h',
      y: -0.2
    },
    margin: {
      l: 50,
      r: 50,
      t: 50,
      b: 100
    },
    height: 500,
    template: 'plotly_white'
  };
  
  // Criar o gráfico
  Plotly.newPlot(container, traces, layout);
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', initDashboard);
