# Requisitos para Migração do Site de Controle de Demandas do Condomínio

## Análise do Site Atual
O site atual (https://filipempfalcao.github.io/condominiosaojudastadeu/) é uma aplicação web simples com as seguintes páginas e funcionalidades:

1. **Página de Demandas**:
   - Lista de demandas com informações como título, ID, categoria, data, criticidade e status
   - Filtros por status, categoria e criticidade
   - Campo de busca
   - Paginação
   - Botões para acessar detalhes de cada demanda

2. **Dashboard**:
   - Indicadores: Total de demandas, demandas abertas, tempo médio de resolução, taxa de resolução
   - Gráfico de demandas por status e categoria
   - Gráfico de evolução de demandas (novas vs. resolvidas) ao longo do tempo
   - Filtro por período

3. **Formulário de Nova Demanda**:
   - Campos para título, categoria, criticidade, descrição, localização
   - Opção para anexar arquivos
   - Botões para cancelar ou enviar demanda

## Requisitos para a Nova Versão em Python

### Funcionalidades Principais
1. **Controle de Demandas**:
   - Manter todas as funcionalidades de cadastro e listagem de demandas
   - Implementar filtros e busca
   - Manter visualização de status, criticidade e detalhes das demandas

2. **Dashboard**:
   - Integrar com dados das demandas em tempo real
   - Unificar gráficos de demandas por status, categoria e evolução em um único gráfico
   - Reduzir tamanho dos indicadores em 75% para melhor visualização
   - Manter métricas de criticidade, tempo de resolução e custo final

3. **Nova Demanda**:
   - Manter formulário para cadastro de novas demandas
   - Permitir anexos de arquivos

### Requisitos Técnicos
1. **Base de Dados**:
   - Implementar integração com base de dados gratuita (avaliar Google Sheets como opção)
   - Garantir atualização em tempo real dos dados
   - Permitir acesso aos dados por todos os usuários do site

2. **Autenticação**:
   - Adicionar sistema de autenticação básico
   - Restringir acesso apenas a condôminos, administradora e síndico
   - Implementar níveis de permissão diferentes (se necessário)

3. **Interface**:
   - Design responsivo para celular
   - Interface leve e minimalista
   - Navegação simplificada com foco na funcionalidade principal

4. **Hospedagem**:
   - Solução gratuita para desenvolvimento e validação
   - Compatível com GitHub Pages ou alternativas gratuitas

### Requisitos Não-Funcionais
1. **Simplicidade**:
   - Código fácil de manter e atualizar
   - Documentação clara

2. **Performance**:
   - Aplicação leve para consumo
   - Carregamento rápido em dispositivos móveis

3. **Usabilidade**:
   - Interface intuitiva
   - Flexibilidade para boa experiência do usuário

4. **Transparência**:
   - Proporcionar transparência na gestão do síndico
   - Evitar omissões e falta de transparência na gestão do condomínio

## Tecnologias Sugeridas
- **Backend**: Framework Python (a ser definido entre Flask, Django, FastAPI)
- **Frontend**: HTML, CSS, JavaScript com bibliotecas responsivas
- **Visualização de Dados**: Plotly (já familiar ao usuário)
- **Banco de Dados**: Integração com Google Sheets ou alternativa gratuita
- **Autenticação**: Sistema básico de login/senha
- **Hospedagem**: GitHub Pages (frontend) + serviço gratuito para backend
