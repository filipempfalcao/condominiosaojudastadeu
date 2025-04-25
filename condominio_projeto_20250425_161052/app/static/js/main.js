/**
 * Scripts principais para o site de controle de demandas do condomínio
 */

// Função para inicializar o menu mobile
function initMobileMenu() {
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('nav ul');
  
  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', () => {
      navMenu.classList.toggle('show');
    });
  }
}

// Função para inicializar os alertas
function initAlerts() {
  const alerts = document.querySelectorAll('.alert');
  
  alerts.forEach(alert => {
    // Adicionar botão de fechar
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.className = 'alert-close';
    closeBtn.addEventListener('click', () => {
      alert.style.display = 'none';
    });
    alert.appendChild(closeBtn);
    
    // Auto-fechar após 5 segundos
    setTimeout(() => {
      alert.style.display = 'none';
    }, 5000);
  });
}

// Função para inicializar os filtros de demandas
function initFilters() {
  const filterForm = document.getElementById('filter-form');
  const filterInputs = document.querySelectorAll('.filter-item select, .filter-item input');
  
  if (filterForm && filterInputs.length > 0) {
    filterInputs.forEach(input => {
      input.addEventListener('change', () => {
        filterForm.submit();
      });
    });
  }
}

// Função para inicializar o dashboard
function initDashboard() {
  const dashboardContainer = document.getElementById('dashboard-container');
  
  if (!dashboardContainer) return;
  
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
    
  } catch (error) {
    console.error('Erro ao carregar indicadores:', error);
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
    const periodo = periodoSelect ? periodoSelect.value : 'ultimos_30_dias';
    const response = await fetch(`/dashboard/api/grafico_unificado?periodo=${periodo}`);
    const data = await response.json();
    
    if (data.error) {
      console.error('Erro ao carregar gráfico unificado:', data.error);
      return;
    }
    
    // Criar gráfico unificado com Plotly
    criarGraficoUnificado(graficoContainer, data);
    
  } catch (error) {
    console.error('Erro ao carregar gráfico unificado:', error);
  }
}

// Função para criar o gráfico unificado com Plotly
function criarGraficoUnificado(container, data) {
  if (!data || !data.status_categoria || !data.evolucao) {
    container.innerHTML = '<p>Não há dados suficientes para exibir o gráfico.</p>';
    return;
  }
  
  // Preparar dados para o gráfico de barras por status e categoria
  const traces = [];
  
  // Agrupar por status
  const statusGroups = {};
  data.status_categoria.forEach(item => {
    if (!statusGroups[item.status]) {
      statusGroups[item.status] = [];
    }
    statusGroups[item.status].push(item);
  });
  
  // Criar uma trace para cada status
  Object.keys(statusGroups).forEach(status => {
    const items = statusGroups[status];
    
    traces.push({
      x: items.map(item => item.categoria),
      y: items.map(item => item.quantidade),
      name: status,
      type: 'bar'
    });
  });
  
  // Adicionar trace de linha para evolução de demandas
  if (data.meses_ordenados && data.meses_ordenados.length > 0) {
    // Agrupar por status para evolução
    const evolucaoGroups = {};
    data.evolucao.forEach(item => {
      if (!evolucaoGroups[item.status]) {
        evolucaoGroups[item.status] = {};
      }
      evolucaoGroups[item.status][item.mes] = item.quantidade;
    });
    
    // Criar uma trace de linha para cada status
    Object.keys(evolucaoGroups).forEach(status => {
      const values = data.meses_ordenados.map(mes => evolucaoGroups[status][mes] || 0);
      
      traces.push({
        x: data.meses_ordenados,
        y: values,
        name: `Evolução: ${status}`,
        type: 'scatter',
        mode: 'lines+markers',
        yaxis: 'y2'
      });
    });
  }
  
  // Layout do gráfico
  const layout = {
    title: 'Demandas por Status, Categoria e Evolução',
    barmode: 'group',
    xaxis: {
      title: 'Categoria'
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
    height: 500
  };
  
  // Criar o gráfico
  Plotly.newPlot(container, traces, layout);
}

// Função para validar formulário de nova demanda
function validateDemandaForm() {
  const form = document.getElementById('nova-demanda-form');
  
  if (!form) return true;
  
  const titulo = form.querySelector('[name="titulo"]');
  const categoria = form.querySelector('[name="categoria"]');
  const criticidade = form.querySelector('[name="criticidade"]');
  const descricao = form.querySelector('[name="descricao"]');
  const localizacao = form.querySelector('[name="localizacao"]');
  
  let isValid = true;
  
  // Validar título
  if (!titulo.value.trim()) {
    markInvalid(titulo, 'O título é obrigatório');
    isValid = false;
  } else {
    markValid(titulo);
  }
  
  // Validar categoria
  if (categoria.value === 'Selecione uma categoria') {
    markInvalid(categoria, 'Selecione uma categoria');
    isValid = false;
  } else {
    markValid(categoria);
  }
  
  // Validar criticidade
  if (criticidade.value === 'Selecione a criticidade') {
    markInvalid(criticidade, 'Selecione a criticidade');
    isValid = false;
  } else {
    markValid(criticidade);
  }
  
  // Validar descrição
  if (!descricao.value.trim()) {
    markInvalid(descricao, 'A descrição é obrigatória');
    isValid = false;
  } else {
    markValid(descricao);
  }
  
  // Validar localização
  if (!localizacao.value.trim()) {
    markInvalid(localizacao, 'A localização é obrigatória');
    isValid = false;
  } else {
    markValid(localizacao);
  }
  
  return isValid;
}

// Função para marcar campo como inválido
function markInvalid(field, message) {
  field.classList.add('is-invalid');
  
  // Adicionar mensagem de erro
  let errorElement = field.nextElementSibling;
  if (!errorElement || !errorElement.classList.contains('error-message')) {
    errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    field.parentNode.insertBefore(errorElement, field.nextSibling);
  }
  
  errorElement.textContent = message;
}

// Função para marcar campo como válido
function markValid(field) {
  field.classList.remove('is-invalid');
  
  // Remover mensagem de erro
  const errorElement = field.nextElementSibling;
  if (errorElement && errorElement.classList.contains('error-message')) {
    errorElement.remove();
  }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initAlerts();
  initFilters();
  initDashboard();
  
  // Inicializar validação de formulário
  const novaDemandaForm = document.getElementById('nova-demanda-form');
  if (novaDemandaForm) {
    novaDemandaForm.addEventListener('submit', (e) => {
      if (!validateDemandaForm()) {
        e.preventDefault();
      }
    });
  }
});
