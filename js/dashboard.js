// Versão atualizada do dashboard.js com gráficos de barras empilhadas
// Definir variáveis globais necessárias
window.statusLabels = {
  'aberta': 'Aberta',
  'em-analise': 'Em Análise',
  'em-andamento': 'Em Andamento',
  'aguardando-terceiros': 'Aguardando Terceiros',
  'resolvida': 'Resolvida',
  'cancelada': 'Cancelada'
};

window.criticidadeLabels = {
  'baixa': 'Baixa',
  'media': 'Média',
  'alta': 'Alta'
};

window.criticidadeClasses = {
  'baixa': 'badge-success',
  'media': 'badge-warning',
  'alta': 'badge-danger'
};

window.statusClasses = {
  'aberta': 'badge-secondary',
  'em-analise': 'badge-info',
  'em-andamento': 'badge-primary',
  'aguardando-terceiros': 'badge-warning',
  'resolvida': 'badge-success',
  'cancelada': 'badge-danger'
};

window.formatarData = function(dataString) {
  const data = new Date(dataString);
  return data.toLocaleDateString('pt-BR');
};

// Função para obter dados do localStorage
window.obterDados = function(chave, valorPadrao) {
  const dados = localStorage.getItem(chave);
  return dados ? JSON.parse(dados) : valorPadrao;
};

// Função para mostrar notificação
window.mostrarNotificacao = function(mensagem, tipo) {
  alert(mensagem);
};

document.addEventListener('DOMContentLoaded', function() {
  // Obter dados das demandas
  const demandas = window.obterDados('demandas', []);
  
  // Elementos de estatísticas
  const totalDemandasEl = document.getElementById('totalDemandas');
  const totalDemandasChangeEl = document.getElementById('totalDemandasChange');
  const demandasAbertasEl = document.getElementById('demandasAbertas');
  const demandasAbertasChangeEl = document.getElementById('demandasAbertasChange');
  const tempoMedioEl = document.getElementById('tempoMedio');
  const tempoMedioChangeEl = document.getElementById('tempoMedioChange');
  const taxaResolucaoEl = document.getElementById('taxaResolucao');
  const taxaResolucaoChangeEl = document.getElementById('taxaResolucaoChange');
  
  // Elementos de filtro e lista
  const periodoFilter = document.getElementById('periodoFilter');
  const demandasCriticasList = document.getElementById('demandasCriticas');
  
  // Contextos dos gráficos
  const demandasChartCtx = document.getElementById('demandasChart').getContext('2d');
  const evolucaoChartCtx = document.getElementById('evolucaoChart').getContext('2d');
  
  // Variáveis para armazenar instâncias dos gráficos
  let demandasChart = null;
  let evolucaoChart = null;
  
  // Função para atualizar o dashboard
  function atualizarDashboard() {
    // Obter período selecionado
    const periodo = parseInt(periodoFilter.value);
    
    // Calcular datas para filtro
    const hoje = new Date();
    const dataInicio = new Date(hoje);
    dataInicio.setDate(hoje.getDate() - periodo);
    
    // Filtrar demandas do período atual
    const demandasPeriodoAtual = demandas.filter(demanda => {
      const dataDemanda = new Date(demanda.data);
      return dataDemanda >= dataInicio;
    });
    
    // Calcular datas para período anterior (para comparação)
    const dataInicioAnterior = new Date(dataInicio);
    dataInicioAnterior.setDate(dataInicioAnterior.getDate() - periodo);
    
    // Filtrar demandas do período anterior
    const demandasPeriodoAnterior = demandas.filter(demanda => {
      const dataDemanda = new Date(demanda.data);
      return dataDemanda >= dataInicioAnterior && dataDemanda < dataInicio;
    });
    
    // Calcular estatísticas do período atual
    const totalDemandas = demandasPeriodoAtual.length;
    const demandasAbertas = demandasPeriodoAtual.filter(demanda => 
      demanda.status === 'aberta' || 
      demanda.status === 'em-analise' || 
      demanda.status === 'em-andamento' || 
      demanda.status === 'aguardando-terceiros'
    ).length;
    const demandasResolvidas = demandasPeriodoAtual.filter(demanda => demanda.status === 'resolvida').length;
    const taxaResolucao = totalDemandas > 0 ? (demandasResolvidas / totalDemandas) * 100 : 0;
    
    // Calcular tempo médio de resolução
    let tempoTotalResolucao = 0;
    let demandasResolvidasComData = 0;
    
    demandasPeriodoAtual.forEach(demanda => {
      if (demanda.status === 'resolvida' && demanda.dataResolucao) {
        const dataAbertura = new Date(demanda.data);
        const dataResolucao = new Date(demanda.dataResolucao);
        const diasResolucao = Math.floor((dataResolucao - dataAbertura) / (1000 * 60 * 60 * 24));
        tempoTotalResolucao += diasResolucao;
        demandasResolvidasComData++;
      }
    });
    
    const tempoMedioResolucao = demandasResolvidasComData > 0 ? tempoTotalResolucao / demandasResolvidasComData : 8.5;
    
    // Calcular estatísticas do período anterior
    const totalDemandasAnterior = demandasPeriodoAnterior.length;
    const demandasAbertasAnterior = demandasPeriodoAnterior.filter(demanda => 
      demanda.status === 'aberta' || 
      demanda.status === 'em-analise' || 
      demanda.status === 'em-andamento' || 
      demanda.status === 'aguardando-terceiros'
    ).length;
    const demandasResolvidasAnterior = demandasPeriodoAnterior.filter(demanda => demanda.status === 'resolvida').length;
    const taxaResolucaoAnterior = totalDemandasAnterior > 0 ? (demandasResolvidasAnterior / totalDemandasAnterior) * 100 : 0;
    
    // Calcular tempo médio de resolução do período anterior
    let tempoTotalResolucaoAnterior = 0;
    let demandasResolvidasComDataAnterior = 0;
    
    demandasPeriodoAnterior.forEach(demanda => {
      if (demanda.status === 'resolvida' && demanda.dataResolucao) {
        const dataAbertura = new Date(demanda.data);
        const dataResolucao = new Date(demanda.dataResolucao);
        const diasResolucao = Math.floor((dataResolucao - dataAbertura) / (1000 * 60 * 60 * 24));
        tempoTotalResolucaoAnterior += diasResolucao;
        demandasResolvidasComDataAnterior++;
      }
    });
    
    const tempoMedioResolucaoAnterior = demandasResolvidasComDataAnterior > 0 ? tempoTotalResolucaoAnterior / demandasResolvidasComDataAnterior : 10.8;
    
    // Calcular variações percentuais
    const variacaoTotalDemandas = totalDemandasAnterior > 0 ? ((totalDemandas - totalDemandasAnterior) / totalDemandasAnterior) * 100 : 0;
    const variacaoDemandasAbertas = demandasAbertasAnterior > 0 ? ((demandasAbertas - demandasAbertasAnterior) / demandasAbertasAnterior) * 100 : 0;
    const variacaoTempoMedio = tempoMedioResolucaoAnterior > 0 ? tempoMedioResolucao - tempoMedioResolucaoAnterior : 0;
    const variacaoTaxaResolucao = taxaResolucaoAnterior > 0 ? taxaResolucao - taxaResolucaoAnterior : 0;
    
    // Atualizar elementos de estatísticas
    totalDemandasEl.textContent = totalDemandas;
    totalDemandasChangeEl.textContent = `${variacaoTotalDemandas >= 0 ? '+' : ''}${variacaoTotalDemandas.toFixed(1)}% em relação ao período anterior`;
    totalDemandasChangeEl.className = `stat-change ${variacaoTotalDemandas >= 0 ? 'positive' : 'negative'}`;
    
    demandasAbertasEl.textContent = demandasAbertas;
    demandasAbertasChangeEl.textContent = `${variacaoDemandasAbertas >= 0 ? '+' : ''}${variacaoDemandasAbertas.toFixed(1)}% em relação ao período anterior`;
    demandasAbertasChangeEl.className = `stat-change ${variacaoDemandasAbertas >= 0 ? 'positive' : 'negative'}`;
    
    tempoMedioEl.textContent = `${tempoMedioResolucao.toFixed(1)} dias`;
    tempoMedioChangeEl.textContent = `${variacaoTempoMedio >= 0 ? '+' : ''}${variacaoTempoMedio.toFixed(1)} dias em relação ao período anterior`;
    tempoMedioChangeEl.className = `stat-change ${variacaoTempoMedio <= 0 ? 'positive' : 'negative'}`;
    
    taxaResolucaoEl.textContent = `${taxaResolucao.toFixed(1)}%`;
    taxaResolucaoChangeEl.textContent = `${variacaoTaxaResolucao >= 0 ? '+' : ''}${variacaoTaxaResolucao.toFixed(1)}% em relação ao período anterior`;
    taxaResolucaoChangeEl.className = `stat-change ${variacaoTaxaResolucao >= 0 ? 'positive' : 'negative'}`;
    
    // Atualizar gráficos
    atualizarGraficoDemandas(demandasPeriodoAtual);
    atualizarGraficoEvolucao(demandas);
    
    // Atualizar lista de demandas críticas
    atualizarDemandasCriticas();
  }
  
  // Função para atualizar o gráfico de demandas por status e categoria
  function atualizarGraficoDemandas(demandasFiltradas) {
    // Agrupar demandas por status
    const statusGroups = {
      'abertas': ['aberta', 'em-analise', 'em-andamento', 'aguardando-terceiros'],
      'encerradas': ['resolvida', 'cancelada']
    };
    
    // Processar dados para categorias
    const categorias = {};
    demandasFiltradas.forEach(demanda => {
      if (!categorias[demanda.categoriaLabel]) {
        categorias[demanda.categoriaLabel] = {
          'abertas': 0,
          'encerradas': 0
        };
      }
      
      // Determinar se a demanda está aberta ou encerrada
      let statusGroup = 'abertas';
      if (statusGroups.encerradas.includes(demanda.status)) {
        statusGroup = 'encerradas';
      }
      
      categorias[demanda.categoriaLabel][statusGroup]++;
    });
    
    const categoriasLabels = Object.keys(categorias);
    const abertasPorCategoria = categoriasLabels.map(cat => categorias[cat].abertas);
    const encerradasPorCategoria = categoriasLabels.map(cat => categorias[cat].encerradas);
    
    // Cores para os datasets
    const coresAbertas = 'rgba(54, 162, 235, 0.8)';
    const coresEncerradas = 'rgba(75, 192, 192, 0.8)';
    
    // Atualizar ou criar gráfico de demandas
    if (demandasChart) {
      demandasChart.destroy();
    }
    
    demandasChart = new Chart(demandasChartCtx, {
      type: 'bar',
      data: {
        labels: categoriasLabels,
        datasets: [
          {
            label: 'Demandas Abertas',
            data: abertasPorCategoria,
            backgroundColor: coresAbertas,
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Demandas Encerradas',
            data: encerradasPorCategoria,
            backgroundColor: coresEncerradas,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            stacked: true,
            title: {
              display: true,
              text: 'Categoria'
            }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              precision: 0
            },
            title: {
              display: true,
              text: 'Quantidade'
            }
          }
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 15
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        }
      }
    });
  }
  
  // Função para atualizar o gráfico de evolução
  function atualizarGraficoEvolucao(todasDemandas) {
    // Processar dados para evolução
    const evolucaoDemandas = {};
    const evolucaoResolucoes = {};
    
    // Inicializar dados dos últimos 6 meses
    const hoje = new Date();
    for (let i = 5; i >= 0; i--) {
      const data = new Date(hoje);
      data.setMonth(hoje.getMonth() - i);
      const mesAno = `${data.getMonth() + 1}/${data.getFullYear()}`;
      evolucaoDemandas[mesAno] = 0;
      evolucaoResolucoes[mesAno] = 0;
    }
    
    // Preencher dados de demandas por mês
    todasDemandas.forEach(demanda => {
      const dataDemanda = new Date(demanda.data);
      const mesAno = `${dataDemanda.getMonth() + 1}/${dataDemanda.getFullYear()}`;
      
      if (evolucaoDemandas[mesAno] !== undefined) {
        evolucaoDemandas[mesAno]++;
      }
      
      // Preencher dados de resoluções por mês
      if (demanda.status === 'resolvida' && demanda.dataResolucao) {
        const dataResolucao = new Date(demanda.dataResolucao);
        const mesAnoResolucao = `${dataResolucao.getMonth() + 1}/${dataResolucao.getFullYear()}`;
        
        if (evolucaoResolucoes[mesAnoResolucao] !== undefined) {
          evolucaoResolucoes[mesAnoResolucao]++;
        }
      }
    });
    
    const evolucaoLabels = Object.keys(evolucaoDemandas);
    const evolucaoDadosDemandas = Object.values(evolucaoDemandas);
    const evolucaoDadosResolucoes = Object.values(evolucaoResolucoes);
    
    // Atualizar ou criar gráfico de evolução
    if (evolucaoChart) {
      evolucaoChart.destroy();
    }
    
    evolucaoChart = new Chart(evolucaoChartCtx, {
      type: 'line',
      data: {
        labels: evolucaoLabels,
        datasets: [
          {
            label: 'Novas Demandas',
            data: evolucaoDadosDemandas,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            tension: 0.4,
            fill: true
          },
          {
            label: 'Demandas Resolvidas',
            data: evolucaoDadosResolucoes,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.4,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0
            }
          }
        },
        plugins: {
          legend: {
            position: 'top'
          }
        }
      }
    });
  }
  
  // Função para atualizar a lista de demandas críticas
  function atualizarDemandasCriticas() {
    // Filtrar demandas críticas (alta criticidade e não resolvidas)
    const demandasCriticas = demandas.filter(demanda => 
      demanda.criticidade === 'alta' && 
      demanda.status !== 'resolvida' && 
      demanda.status !== 'cancelada'
    );
    
    // Ordenar por data (mais recentes primeiro)
    demandasCriticas.sort((a, b) => new Date(b.data) - new Date(a.data));
    
    // Limitar a 3 demandas
    const demandasCriticasLimitadas = demandasCriticas.slice(0, 3);
    
    // Limpar lista atual
    demandasCriticasList.innerHTML = '';
    
    // Verificar se há demandas críticas
    if (demandasCriticasLimitadas.length === 0) {
      demandasCriticasList.innerHTML = `
        <div class="demand-item text-center">
          <p>Não há demandas críticas no momento.</p>
        </div>
      `;
      return;
    }
    
    // Adicionar demandas críticas à lista
    demandasCriticasLimitadas.forEach(demanda => {
      const demandaEl = document.createElement('div');
      demandaEl.className = 'demand-item';
      demandaEl.innerHTML = `
        <div class="demand-header">
          <div class="demand-title">${demanda.titulo}</div>
          <div class="demand-id">ID: ${demanda.id}</div>
        </div>
        <div class="demand-meta">
          <div>${demanda.categoriaLabel} | ${window.formatarData(demanda.data)}</div>
          <div class="demand-badges">
            <span class="badge ${window.criticidadeClasses[demanda.criticidade]}">${window.criticidadeLabels[demanda.criticidade]}</span>
            <span class="badge ${window.statusClasses[demanda.status]}">${window.statusLabels[demanda.status]}</span>
          </div>
        </div>
        <div class="text-right">
          <a href="#" class="btn btn-outline btn-sm visualizar-demanda" data-id="${demanda.id}">Detalhes</a>
        </div>
      `;
      demandasCriticasList.appendChild(demandaEl);
    });
    
    // Adicionar eventos aos botões de detalhes
    document.querySelectorAll('.visualizar-demanda').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const id = this.getAttribute('data-id');
        visualizarDemanda(id);
      });
    });
  }
  
  // Função para visualizar detalhes de uma demanda
  function visualizarDemanda(id) {
    const demanda = demandas.find(d => d.id === id);
    
    if (demanda) {
      alert(`
        Demanda: ${demanda.titulo}
        ID: ${demanda.id}
        Categoria: ${demanda.categoriaLabel}
        Data: ${window.formatarData(demanda.data)}
        Criticidade: ${window.criticidadeLabels[demanda.criticidade]}
        Status: ${window.statusLabels[demanda.status]}
        Localização: ${demanda.localizacao}
        Descrição: ${demanda.descricao}
        ${demanda.custo > 0 ? `Custo: R$ ${demanda.custo.toFixed(2)}` : 'Custo: Não definido'}
      `);
    } else {
      window.mostrarNotificacao('Demanda não encontrada', 'erro');
    }
  }
  
  // Adicionar evento ao filtro de período
  periodoFilter.addEventListener('change', atualizarDashboard);
  
  // Inicializar dashboard
  setTimeout(function() {
    try {
      atualizarDashboard();
      console.log("Dashboard inicializado com sucesso");
    } catch (error) {
      console.error("Erro ao inicializar dashboard:", error);
    }
  }, 500);
});
