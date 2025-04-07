// Arquivo JavaScript principal para funcionalidades comuns

// Função para alternar a visibilidade do menu em dispositivos móveis
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const mainNav = document.getElementById('mainNav');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
    }
    
    // Fechar o menu ao clicar fora dele
    document.addEventListener('click', function(event) {
        if (mainNav && mainNav.classList.contains('active') && 
            !mainNav.contains(event.target) && 
            event.target !== navToggle) {
            mainNav.classList.remove('active');
        }
    });
});

// Função para formatar data
function formatarData(data) {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
    return new Date(data).toLocaleDateString('pt-BR', options);
}

// Função para obter dados do localStorage ou usar dados padrão
function obterDados(chave, dadosPadrao) {
    const dadosArmazenados = localStorage.getItem(chave);
    return dadosArmazenados ? JSON.parse(dadosArmazenados) : dadosPadrao;
}

// Função para salvar dados no localStorage
function salvarDados(chave, dados) {
    localStorage.setItem(chave, JSON.stringify(dados));
}

// Função para gerar ID único
function gerarId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

// Função para mostrar notificação
function mostrarNotificacao(mensagem, tipo = 'sucesso') {
    const notificacao = document.createElement('div');
    notificacao.className = `notificacao ${tipo}`;
    notificacao.textContent = mensagem;
    
    document.body.appendChild(notificacao);
    
    setTimeout(() => {
        notificacao.classList.add('mostrar');
    }, 10);
    
    setTimeout(() => {
        notificacao.classList.remove('mostrar');
        setTimeout(() => {
            document.body.removeChild(notificacao);
        }, 300);
    }, 3000);
}

// Dados iniciais para o sistema
const dadosIniciais = {
    demandas: [
        {
            id: '001',
            titulo: 'Lâmpadas queimadas no corredor',
            categoria: 'eletrica',
            categoriaLabel: 'Elétrica',
            data: '2025-04-01',
            criticidade: 'media',
            status: 'em-andamento',
            descricao: 'Três lâmpadas queimadas no corredor do 2º andar, próximo aos apartamentos 201-204.',
            localizacao: 'Corredor do 2º andar',
            custo: 150
        },
        {
            id: '002',
            titulo: 'Vazamento no banheiro social',
            categoria: 'hidraulica',
            categoriaLabel: 'Hidráulica',
            data: '2025-03-28',
            criticidade: 'alta',
            status: 'resolvida',
            descricao: 'Vazamento na tubulação do banheiro social da área comum, próximo à piscina.',
            localizacao: 'Banheiro social da área comum',
            custo: 350
        },
        {
            id: '003',
            titulo: 'Limpeza da área da piscina',
            categoria: 'limpeza',
            categoriaLabel: 'Limpeza',
            data: '2025-03-25',
            criticidade: 'baixa',
            status: 'resolvida',
            descricao: 'Limpeza geral da área da piscina, incluindo deck e mobiliário.',
            localizacao: 'Área da piscina',
            custo: 200
        },
        {
            id: '004',
            titulo: 'Trinca na parede do hall',
            categoria: 'estrutural',
            categoriaLabel: 'Estrutural',
            data: '2025-03-20',
            criticidade: 'alta',
            status: 'aguardando-terceiros',
            descricao: 'Trinca na parede do hall de entrada, próximo ao elevador. Necessita avaliação estrutural.',
            localizacao: 'Hall de entrada',
            custo: 0
        },
        {
            id: '005',
            titulo: 'Câmera de segurança com defeito',
            categoria: 'seguranca',
            categoriaLabel: 'Segurança',
            data: '2025-03-15',
            criticidade: 'alta',
            status: 'resolvida',
            descricao: 'Câmera de segurança da entrada principal não está funcionando.',
            localizacao: 'Entrada principal',
            custo: 420
        },
        {
            id: '006',
            titulo: 'Interfone do apartamento 302 não funciona',
            categoria: 'eletrica',
            categoriaLabel: 'Elétrica',
            data: '2025-03-12',
            criticidade: 'media',
            status: 'aberta',
            descricao: 'Interfone do apartamento 302 não está recebendo chamadas da portaria.',
            localizacao: 'Apartamento 302',
            custo: 0
        },
        {
            id: '007',
            titulo: 'Pintura da fachada descascando',
            categoria: 'estrutural',
            categoriaLabel: 'Estrutural',
            data: '2025-03-10',
            criticidade: 'media',
            status: 'em-analise',
            descricao: 'Pintura da fachada principal está descascando em vários pontos.',
            localizacao: 'Fachada principal',
            custo: 0
        },
        {
            id: '008',
            titulo: 'Infiltração no teto do 5º andar',
            categoria: 'hidraulica',
            categoriaLabel: 'Hidráulica',
            data: '2025-03-10',
            criticidade: 'alta',
            status: 'em-andamento',
            descricao: 'Infiltração no teto do corredor do 5º andar, próximo ao apartamento 502.',
            localizacao: 'Corredor do 5º andar',
            custo: 0
        }
    ]
};

// Inicializar dados no localStorage se não existirem
if (!localStorage.getItem('demandas')) {
    salvarDados('demandas', dadosIniciais.demandas);
}

// Mapeamento de status para labels em português
const statusLabels = {
    'aberta': 'Aberta',
    'em-analise': 'Em Análise',
    'em-andamento': 'Em Andamento',
    'aguardando-terceiros': 'Aguardando Terceiros',
    'resolvida': 'Resolvida',
    'cancelada': 'Cancelada'
};

// Mapeamento de criticidade para labels em português
const criticidadeLabels = {
    'baixa': 'Baixa',
    'media': 'Média',
    'alta': 'Alta'
};

// Mapeamento de criticidade para classes CSS
const criticidadeClasses = {
    'baixa': 'badge-low',
    'media': 'badge-medium',
    'alta': 'badge-high'
};

// Mapeamento de status para classes CSS
const statusClasses = {
    'aberta': 'badge-open',
    'em-analise': 'badge-open',
    'em-andamento': 'badge-in-progress',
    'aguardando-terceiros': 'badge-waiting',
    'resolvida': 'badge-resolved',
    'cancelada': 'badge-waiting'
};
