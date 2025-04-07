// Arquivo JavaScript para a página de nova demanda

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do formulário
    const novaDemandaForm = document.getElementById('novaDemandaForm');
    const cancelarBtn = document.getElementById('cancelarBtn');
    
    // Adicionar evento ao botão cancelar
    cancelarBtn.addEventListener('click', function() {
        // Redirecionar para a página de demandas
        window.location.href = 'demandas.html';
    });
    
    // Adicionar evento ao formulário
    novaDemandaForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obter valores do formulário
        const titulo = document.getElementById('titulo').value;
        const categoria = document.getElementById('categoria').value;
        const criticidade = document.getElementById('criticidade').value;
        const descricao = document.getElementById('descricao').value;
        const localizacao = document.getElementById('localizacao').value;
        
        // Validar campos obrigatórios
        if (!titulo || !categoria || !criticidade || !descricao || !localizacao) {
            mostrarNotificacao('Preencha todos os campos obrigatórios', 'erro');
            return;
        }
        
        // Obter demandas existentes
        const demandas = obterDados('demandas', []);
        
        // Gerar ID para a nova demanda
        const ultimoId = demandas.length > 0 ? parseInt(demandas[demandas.length - 1].id) : 0;
        const novoId = (ultimoId + 1).toString().padStart(3, '0');
        
        // Obter label da categoria
        const categoriaSelect = document.getElementById('categoria');
        const categoriaLabel = categoriaSelect.options[categoriaSelect.selectedIndex].text;
        
        // Criar nova demanda
        const novaDemanda = {
            id: novoId,
            titulo: titulo,
            categoria: categoria,
            categoriaLabel: categoriaLabel,
            data: new Date().toISOString().split('T')[0], // Formato YYYY-MM-DD
            criticidade: criticidade,
            status: 'aberta',
            descricao: descricao,
            localizacao: localizacao,
            custo: 0 // Custo inicial zero
        };
        
        // Adicionar nova demanda à lista
        demandas.push(novaDemanda);
        
        // Salvar no localStorage
        salvarDados('demandas', demandas);
        
        // Mostrar notificação de sucesso
        mostrarNotificacao('Demanda registrada com sucesso!', 'sucesso');
        
        // Redirecionar para a página de demandas após 1 segundo
        setTimeout(() => {
            window.location.href = 'demandas.html';
        }, 1000);
    });
});
