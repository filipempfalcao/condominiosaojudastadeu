# Plano de Testes - Site de Controle de Demandas do Condomínio

## 1. Testes de Autenticação

### 1.1 Registro de Usuário
- Verificar se é possível registrar um novo usuário com dados válidos
- Verificar se o sistema impede registro com email já existente
- Verificar se o sistema valida campos obrigatórios
- Verificar se o sistema valida a confirmação de senha

### 1.2 Login
- Verificar se um usuário registrado consegue fazer login
- Verificar se o sistema impede login com credenciais inválidas
- Verificar se o sistema redireciona corretamente após o login

### 1.3 Logout
- Verificar se o usuário consegue fazer logout
- Verificar se após o logout o usuário é redirecionado para a página de login

### 1.4 Controle de Acesso
- Verificar se usuários não autenticados são redirecionados para a página de login
- Verificar se condôminos podem visualizar demandas mas não podem editar
- Verificar se síndicos podem editar demandas mas não podem excluir
- Verificar se administradores têm acesso completo (editar e excluir)

## 2. Testes de Gerenciamento de Demandas

### 2.1 Listagem de Demandas
- Verificar se a lista de demandas é exibida corretamente
- Verificar se a paginação funciona corretamente
- Verificar se os filtros (status, categoria, criticidade) funcionam corretamente
- Verificar se a busca por texto funciona corretamente

### 2.2 Criação de Demandas
- Verificar se é possível criar uma nova demanda com dados válidos
- Verificar se o sistema valida campos obrigatórios
- Verificar se a demanda criada aparece na lista de demandas

### 2.3 Visualização de Detalhes
- Verificar se os detalhes da demanda são exibidos corretamente
- Verificar se as informações de data, status e criticidade estão corretas

### 2.4 Edição de Demandas
- Verificar se síndicos e administradores podem editar demandas
- Verificar se as alterações são salvas corretamente
- Verificar se condôminos não têm acesso à edição

### 2.5 Exclusão de Demandas
- Verificar se apenas administradores podem excluir demandas
- Verificar se a exclusão remove a demanda da lista

## 3. Testes do Dashboard

### 3.1 Carregamento de Indicadores
- Verificar se os indicadores são carregados corretamente
- Verificar se os valores dos indicadores estão corretos
- Verificar se as variações percentuais são calculadas corretamente

### 3.2 Filtro por Período
- Verificar se o filtro por período atualiza os indicadores corretamente
- Verificar se o filtro por período atualiza o gráfico corretamente

### 3.3 Gráfico Unificado
- Verificar se o gráfico é renderizado corretamente
- Verificar se o gráfico exibe dados de status e categoria
- Verificar se o gráfico exibe a evolução das demandas
- Verificar se as cores do gráfico correspondem aos status

## 4. Testes de Responsividade

### 4.1 Desktop
- Verificar se o layout está correto em telas grandes
- Verificar se todos os elementos são exibidos corretamente

### 4.2 Tablet
- Verificar se o layout se adapta a telas médias
- Verificar se todos os elementos são exibidos corretamente

### 4.3 Mobile
- Verificar se o layout se adapta a telas pequenas
- Verificar se o menu mobile funciona corretamente
- Verificar se todos os elementos são exibidos corretamente

## 5. Testes de Integração com Google Sheets

### 5.1 Leitura de Dados
- Verificar se o sistema lê corretamente os dados do Google Sheets
- Verificar se as alterações no Google Sheets são refletidas no site

### 5.2 Escrita de Dados
- Verificar se o sistema escreve corretamente os dados no Google Sheets
- Verificar se as alterações no site são refletidas no Google Sheets

## 6. Testes de Performance

### 6.1 Tempo de Carregamento
- Verificar se as páginas carregam em tempo aceitável
- Verificar se o dashboard carrega em tempo aceitável

### 6.2 Uso de Recursos
- Verificar se o uso de memória é aceitável
- Verificar se o uso de CPU é aceitável

## 7. Testes de Segurança

### 7.1 Validação de Inputs
- Verificar se o sistema valida e sanitiza inputs do usuário
- Verificar se o sistema é resistente a injeção de código

### 7.2 Proteção de Rotas
- Verificar se rotas protegidas não são acessíveis sem autenticação
- Verificar se rotas restritas não são acessíveis por usuários sem permissão
