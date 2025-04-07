// Arquivo JavaScript para a página de demandas

document.addEventListener('DOMContentLoaded', function() {
    // Carregar demandas do localStorage
    const demandas = obterDados('demandas', []);
    
    // Elementos do DOM
    const demandasList = document.getElementById('demandasList');
    const statusFilter = document.getElementById('statusFilter');
    const categoryFilter = document.getElementById('categoryFilter');
    const searchInput = document.getElementById('searchInput');
    const pagination = document.getElementById('pagination');
    
    // Configurações de paginação
    const itensPorPagina = 5;
    let paginaAtual = 1;
    
    // Função para renderizar as demandas com filtros e paginação
    function renderizarDemandas() {
        // Aplicar filtros
        const statusSelecionado = statusFilter.value;
        const categoriaSelecionada = categoryFilter.value;
        const termoBusca = searchInput.value.toLowerCase();
        
        const demandasFiltradas = demandas.filter(demanda => {
            // Filtro de status
            if (statusSelecionado && demanda.status !== statusSelecionado) {
                return false;
            }
            
            // Filtro de categoria
            if (categoriaSelecionada && demanda.categoria !== categoriaSelecionada) {
                return false;
            }
            
            // Filtro de busca
            if (termoBusca && !demanda.titulo.toLowerCase().includes(termoBusca) && 
                !demanda.id.toLowerCase().includes(termoBusca)) {
                return false;
            }
            
            return true;
        });
        
        // Calcular paginação
        const totalPaginas = Math.ceil(demandasFiltradas.length / itensPorPagina);
        const inicio = (paginaAtual - 1) * itensPorPagina;
        const fim = inicio + itensPorPagina;
        const demandasPaginadas = demandasFiltradas.slice(inicio, fim);
        
        // Limpar lista atual
        demandasList.innerHTML = '';
        
        // Verificar se há demandas para exibir
        if (demandasPaginadas.length === 0) {
            demandasList.innerHTML = `
                <div class="demand-item text-center">
                    <p>Nenhuma demanda encontrada com os filtros selecionados.</p>
                </div>
            `;
            return;
        }
        
        // Renderizar demandas
        demandasPaginadas.forEach(demanda => {
            const demandaElement = document.createElement('div');
            demandaElement.className = 'demand-item';
            demandaElement.innerHTML = `
                <div class="demand-header">
                    <div class="demand-title">${demanda.titulo}</div>
                    <div class="demand-id">ID: ${demanda.id}</div>
                </div>
                <div class="demand-meta">
                    <div>${demanda.categoriaLabel} | ${formatarData(demanda.data)}</div>
                    <div class="demand-badges">
                        <span class="badge ${criticidadeClasses[demanda.criticidade]}">${criticidadeLabels[demanda.criticidade]}</span>
                        <span class="badge ${statusClasses[demanda.status]}">${statusLabels[demanda.status]}</span>
                        <a href="#" class="btn btn-outline btn-sm visualizar-demanda" data-id="${demanda.id}">Detalhes</a>
                    </div>
                </div>
            `;
            demandasList.appendChild(demandaElement);
        });
        
        // Renderizar paginação
        renderizarPaginacao(totalPaginas);
        
        // Adicionar eventos aos botões de visualização
        document.querySelectorAll('.visualizar-demanda').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const id = this.getAttribute('data-id');
                visualizarDemanda(id);
            });
        });
    }
    
    // Função para renderizar a paginação
    function renderizarPaginacao(totalPaginas) {
        pagination.innerHTML = '';
        
        if (totalPaginas <= 1) {
            return;
        }
        
        // Botão Anterior
        const btnAnterior = document.createElement('button');
        btnAnterior.textContent = 'Anterior';
        btnAnterior.disabled = paginaAtual === 1;
        btnAnterior.addEventListener('click', () => {
            if (paginaAtual > 1) {
                paginaAtual--;
                renderizarDemandas();
            }
        });
        pagination.appendChild(btnAnterior);
        
        // Botões de páginas
        for (let i = 1; i <= totalPaginas; i++) {
            const btnPagina = document.createElement('button');
            btnPagina.textContent = i;
            btnPagina.className = i === paginaAtual ? 'active' : '';
            btnPagina.addEventListener('click', () => {
                paginaAtual = i;
                renderizarDemandas();
            });
            pagination.appendChild(btnPagina);
        }
        
        // Botão Próxima
        const btnProxima = document.createElement('button');
        btnProxima.textContent = 'Próxima';
        btnProxima.disabled = paginaAtual === totalPaginas;
        btnProxima.addEventListener('click', () => {
            if (paginaAtual < totalPaginas) {
                paginaAtual++;
                renderizarDemandas();
            }
        });
        pagination.appendChild(btnProxima);
    }
    
    // Função para visualizar detalhes de uma demanda
    function visualizarDemanda(id) {
        const demanda = demandas.find(d => d.id === id);
        
        if (!demanda) {
            mostrarNotificacao('Demanda não encontrada', 'erro');
            return;
        }
        
        // Aqui você pode implementar um modal ou redirecionar para uma página de detalhes
        // Por enquanto, vamos apenas mostrar um alerta com os detalhes
        alert(`
            Demanda: ${demanda.titulo}
            ID: ${demanda.id}
            Categoria: ${demanda.categoriaLabel}
            Data: ${formatarData(demanda.data)}
            Criticidade: ${criticidadeLabels[demanda.criticidade]}
            Status: ${statusLabels[demanda.status]}
            Localização: ${demanda.localizacao}
            Descrição: ${demanda.descricao}
            ${demanda.custo > 0 ? `Custo: R$ ${demanda.custo.toFixed(2)}` : 'Custo: Não definido'}
        `);
    }
    
    // Adicionar eventos aos filtros
    statusFilter.addEventListener('change', () => {
        paginaAtual = 1;
        renderizarDemandas();
    });
    
    categoryFilter.addEventListener('change', () => {
        paginaAtual = 1;
        renderizarDemandas();
    });
    
    searchInput.addEventListener('input', () => {
        paginaAtual = 1;
        renderizarDemandas();
    });
    
    // Renderizar demandas iniciais
    renderizarDemandas();
});
