"""
Módulo de demandas para o site de controle de demandas do condomínio.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
import os
import sys
from datetime import datetime

# Criar blueprint
bp = Blueprint('demandas', __name__, url_prefix='/demandas')

# Importar módulo de banco de dados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database.sheets_api import SheetsDatabase

# Rotas para demandas
@bp.route('/')
@login_required
def list():
    """Página de listagem de demandas."""
    try:
        # Conectar ao banco de dados
        db = SheetsDatabase(
            os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
            os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
        )
        
        # Obter filtros da query string
        status = request.args.get('status')
        categoria = request.args.get('categoria')
        criticidade = request.args.get('criticidade')
        busca = request.args.get('busca')
        
        # Construir filtros
        filters = {}
        if status and status != "Todos os Status":
            filters['status'] = status
        if categoria and categoria != "Todas as Categorias":
            filters['categoria'] = categoria
        if criticidade and criticidade != "Todas as Criticidades":
            filters['criticidade'] = criticidade
            
        # Obter demandas
        demandas = db.filter_demandas(filters)
        
        # Aplicar busca se existir
        if busca:
            demandas = [d for d in demandas if busca.lower() in d['titulo'].lower() or 
                        busca.lower() in d['descricao'].lower() or 
                        busca.lower() in d['localizacao'].lower() or
                        busca.lower() in d['id'].lower()]
        
        # Ordenar demandas (mais recentes primeiro)
        demandas.sort(key=lambda x: datetime.strptime(x['data_criacao'], '%d/%m/%Y'), reverse=True)
        
        # Paginação
        page = int(request.args.get('page', 1))
        per_page = 10
        total_pages = (len(demandas) + per_page - 1) // per_page
        demandas_paginadas = demandas[(page-1)*per_page:page*per_page]
        
        return render_template('demandas/list.html', 
                              demandas=demandas_paginadas,
                              page=page,
                              total_pages=total_pages,
                              status=status or "Todos os Status",
                              categoria=categoria or "Todas as Categorias",
                              criticidade=criticidade or "Todas as Criticidades",
                              busca=busca or "")
        
    except Exception as e:
        flash(f'Erro ao carregar demandas: {e}', 'error')
        return render_template('demandas/list.html', demandas=[], page=1, total_pages=1)

@bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    """Página de criação de nova demanda."""
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        categoria = request.form.get('categoria')
        criticidade = request.form.get('criticidade')
        descricao = request.form.get('descricao')
        localizacao = request.form.get('localizacao')
        
        # Validar inputs
        if not titulo or not categoria or not criticidade or not descricao or not localizacao:
            flash('Todos os campos são obrigatórios', 'error')
            return render_template('demandas/nova.html')
        
        try:
            # Conectar ao banco de dados
            db = SheetsDatabase(
                os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
                os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
            )
            
            # Criar nova demanda
            demanda_data = {
                'titulo': titulo,
                'categoria': categoria,
                'criticidade': criticidade,
                'descricao': descricao,
                'localizacao': localizacao,
                'status': 'Aberta',
                'data_criacao': datetime.now().strftime('%d/%m/%Y'),
                'data_atualizacao': datetime.now().strftime('%d/%m/%Y')
            }
            
            result = db.add_demanda(demanda_data)
            if result:
                flash('Demanda criada com sucesso!', 'success')
                return redirect(url_for('demandas.list'))
            else:
                flash('Erro ao criar demanda', 'error')
                
        except Exception as e:
            flash(f'Erro ao criar demanda: {e}', 'error')
        
    return render_template('demandas/nova.html')

@bp.route('/<demanda_id>')
@login_required
def detalhes(demanda_id):
    """Página de detalhes de uma demanda."""
    try:
        # Conectar ao banco de dados
        db = SheetsDatabase(
            os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
            os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
        )
        
        # Obter demanda
        demanda = db.get_demanda_by_id(demanda_id)
        if not demanda:
            flash('Demanda não encontrada', 'error')
            return redirect(url_for('demandas.list'))
            
        return render_template('demandas/detalhes.html', demanda=demanda)
        
    except Exception as e:
        flash(f'Erro ao carregar detalhes da demanda: {e}', 'error')
        return redirect(url_for('demandas.list'))

@bp.route('/<demanda_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(demanda_id):
    """Página de edição de demanda."""
    # Verificar permissões (apenas síndico e administradora podem editar)
    if current_user.tipo not in ['sindico', 'administradora']:
        flash('Você não tem permissão para editar demandas', 'error')
        return redirect(url_for('demandas.detalhes', demanda_id=demanda_id))
    
    try:
        # Conectar ao banco de dados
        db = SheetsDatabase(
            os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
            os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
        )
        
        # Obter demanda
        demanda = db.get_demanda_by_id(demanda_id)
        if not demanda:
            flash('Demanda não encontrada', 'error')
            return redirect(url_for('demandas.list'))
        
        if request.method == 'POST':
            # Atualizar demanda
            demanda_data = {
                'titulo': request.form.get('titulo'),
                'categoria': request.form.get('categoria'),
                'criticidade': request.form.get('criticidade'),
                'descricao': request.form.get('descricao'),
                'localizacao': request.form.get('localizacao'),
                'status': request.form.get('status'),
                'data_atualizacao': datetime.now().strftime('%d/%m/%Y')
            }
            
            result = db.update_demanda(demanda_id, demanda_data)
            if result:
                flash('Demanda atualizada com sucesso!', 'success')
                return redirect(url_for('demandas.detalhes', demanda_id=demanda_id))
            else:
                flash('Erro ao atualizar demanda', 'error')
                
        return render_template('demandas/editar.html', demanda=demanda)
        
    except Exception as e:
        flash(f'Erro ao carregar formulário de edição: {e}', 'error')
        return redirect(url_for('demandas.list'))

@bp.route('/<demanda_id>/excluir', methods=['POST'])
@login_required
def excluir(demanda_id):
    """Rota para excluir uma demanda."""
    # Verificar permissões (apenas administradora pode excluir)
    if current_user.tipo != 'administradora':
        flash('Você não tem permissão para excluir demandas', 'error')
        return redirect(url_for('demandas.detalhes', demanda_id=demanda_id))
    
    try:
        # Conectar ao banco de dados
        db = SheetsDatabase(
            os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
            os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu')
        )
        
        # Excluir demanda
        result = db.delete_demanda(demanda_id)
        if result:
            flash('Demanda excluída com sucesso!', 'success')
        else:
            flash('Erro ao excluir demanda', 'error')
            
        return redirect(url_for('demandas.list'))
        
    except Exception as e:
        flash(f'Erro ao excluir demanda: {e}', 'error')
        return redirect(url_for('demandas.list'))

# API para obter dados de demandas em formato JSON (para o dashboard)
@bp.route('/api/dados')
@login_required
def api_dados():
    """API para obter dados de demandas em formato JSON."""
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
        
        # Filtrar por período se necessário
        if periodo != 'todos':
            hoje = datetime.now()
            demandas_filtradas = []
            
            for demanda in demandas:
                data_criacao = datetime.strptime(demanda['data_criacao'], '%d/%m/%Y')
                
                if periodo == 'ultimos_7_dias' and (hoje - data_criacao).days <= 7:
                    demandas_filtradas.append(demanda)
                elif periodo == 'ultimos_30_dias' and (hoje - data_criacao).days <= 30:
                    demandas_filtradas.append(demanda)
                elif periodo == 'ultimos_90_dias' and (hoje - data_criacao).days <= 90:
                    demandas_filtradas.append(demanda)
                elif periodo == 'ultimos_6_meses' and (hoje - data_criacao).days <= 180:
                    demandas_filtradas.append(demanda)
                elif periodo == 'ultimo_ano' and (hoje - data_criacao).days <= 365:
                    demandas_filtradas.append(demanda)
            
            demandas = demandas_filtradas
        
        return jsonify(demandas)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
