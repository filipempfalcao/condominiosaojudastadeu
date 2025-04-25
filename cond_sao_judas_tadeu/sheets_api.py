"""
Módulo de integração com Google Sheets para o site de controle de demandas do condomínio.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

class SheetsDatabase:
    def __init__(self, credentials_file, spreadsheet_name):
        # Definir escopo e credenciais
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
            
            # Autorizar cliente
            self.client = gspread.authorize(credentials)
            
            # Abrir planilha ou criar se não existir
            try:
                self.spreadsheet = self.client.open(spreadsheet_name)
            except gspread.exceptions.SpreadsheetNotFound:
                self.spreadsheet = self.client.create(spreadsheet_name)
                
            # Inicializar worksheets necessárias
            self._init_worksheets()
            
        except Exception as e:
            print(f"Erro ao inicializar conexão com Google Sheets: {e}")
            raise
    
    def _init_worksheets(self):
        """Inicializar as planilhas necessárias com cabeçalhos."""
        # Planilha de demandas
        try:
            demandas_ws = self.get_worksheet('demandas')
            # Verificar se já tem cabeçalhos
            headers = demandas_ws.row_values(1)
            if not headers:
                demandas_ws.append_row([
                    'id', 'titulo', 'categoria', 'criticidade', 'descricao', 
                    'localizacao', 'status', 'data_criacao', 'data_atualizacao'
                ])
        except Exception as e:
            print(f"Erro ao inicializar planilha de demandas: {e}")
            
        # Planilha de usuários
        try:
            usuarios_ws = self.get_worksheet('usuarios')
            # Verificar se já tem cabeçalhos
            headers = usuarios_ws.row_values(1)
            if not headers:
                usuarios_ws.append_row([
                    'id', 'email', 'nome', 'senha_hash', 'tipo', 'data_criacao'
                ])
        except Exception as e:
            print(f"Erro ao inicializar planilha de usuários: {e}")
    
    def get_worksheet(self, name):
        """Obter uma planilha específica pelo nome."""
        try:
            return self.spreadsheet.worksheet(name)
        except gspread.exceptions.WorksheetNotFound:
            return self.spreadsheet.add_worksheet(title=name, rows=100, cols=20)
    
    # Métodos para demandas
    def get_all_demandas(self):
        """Obter todas as demandas da planilha."""
        try:
            worksheet = self.get_worksheet('demandas')
            records = worksheet.get_all_records()
            return records
        except Exception as e:
            print(f"Erro ao obter demandas: {e}")
            return []
    
    def get_demanda_by_id(self, demanda_id):
        """Obter uma demanda específica pelo ID."""
        try:
            worksheet = self.get_worksheet('demandas')
            records = worksheet.get_all_records()
            for record in records:
                if str(record['id']) == str(demanda_id):
                    return record
            return None
        except Exception as e:
            print(f"Erro ao obter demanda por ID: {e}")
            return None
    
    def add_demanda(self, demanda_data):
        """Adicionar uma nova demanda à planilha."""
        try:
            worksheet = self.get_worksheet('demandas')
            
            # Gerar ID se não existir
            if not demanda_data.get('id'):
                records = worksheet.get_all_records()
                if records:
                    max_id = max([int(record['id']) for record in records if record['id'].isdigit()])
                    demanda_data['id'] = str(max_id + 1).zfill(3)
                else:
                    demanda_data['id'] = '001'
            
            # Adicionar datas se não existirem
            now = datetime.now().strftime('%d/%m/%Y')
            if not demanda_data.get('data_criacao'):
                demanda_data['data_criacao'] = now
            if not demanda_data.get('data_atualizacao'):
                demanda_data['data_atualizacao'] = now
                
            worksheet.append_row([
                demanda_data.get('id'),
                demanda_data.get('titulo'),
                demanda_data.get('categoria'),
                demanda_data.get('criticidade'),
                demanda_data.get('descricao'),
                demanda_data.get('localizacao'),
                demanda_data.get('status', 'Aberta'),
                demanda_data.get('data_criacao'),
                demanda_data.get('data_atualizacao')
            ])
            return demanda_data
        except Exception as e:
            print(f"Erro ao adicionar demanda: {e}")
            return None
        
    def update_demanda(self, demanda_id, demanda_data):
        """Atualizar uma demanda existente."""
        try:
            worksheet = self.get_worksheet('demandas')
            
            # Encontrar a linha da demanda
            cell = None
            try:
                cell = worksheet.find(str(demanda_id))
            except gspread.exceptions.CellNotFound:
                print(f"Demanda com ID {demanda_id} não encontrada")
                return None
                
            if cell:
                row = cell.row
                
                # Atualizar a data de atualização
                demanda_data['data_atualizacao'] = datetime.now().strftime('%d/%m/%Y')
                
                # Obter dados atuais para manter valores não atualizados
                current_data = self.get_demanda_by_id(demanda_id)
                
                # Atualizar os dados na linha correspondente
                worksheet.update_cell(row, 2, demanda_data.get('titulo', current_data['titulo']))
                worksheet.update_cell(row, 3, demanda_data.get('categoria', current_data['categoria']))
                worksheet.update_cell(row, 4, demanda_data.get('criticidade', current_data['criticidade']))
                worksheet.update_cell(row, 5, demanda_data.get('descricao', current_data['descricao']))
                worksheet.update_cell(row, 6, demanda_data.get('localizacao', current_data['localizacao']))
                worksheet.update_cell(row, 7, demanda_data.get('status', current_data['status']))
                worksheet.update_cell(row, 9, demanda_data['data_atualizacao'])
                
                return self.get_demanda_by_id(demanda_id)
            return None
        except Exception as e:
            print(f"Erro ao atualizar demanda: {e}")
            return None
    
    def delete_demanda(self, demanda_id):
        """Excluir uma demanda pelo ID."""
        try:
            worksheet = self.get_worksheet('demandas')
            
            # Encontrar a linha da demanda
            cell = None
            try:
                cell = worksheet.find(str(demanda_id))
            except gspread.exceptions.CellNotFound:
                print(f"Demanda com ID {demanda_id} não encontrada")
                return False
                
            if cell:
                worksheet.delete_row(cell.row)
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir demanda: {e}")
            return False
    
    def filter_demandas(self, filters=None):
        """Filtrar demandas com base em critérios."""
        if filters is None:
            filters = {}
            
        try:
            all_demandas = self.get_all_demandas()
            if not all_demandas:
                return []
                
            df = pd.DataFrame(all_demandas)
            
            # Aplicar filtros
            for key, value in filters.items():
                if value and value != f"Todos os {key.capitalize()}s" and value != f"Todas as {key.capitalize()}s":
                    df = df[df[key] == value]
            
            # Converter de volta para lista de dicionários
            return df.to_dict('records')
        except Exception as e:
            print(f"Erro ao filtrar demandas: {e}")
            return []
    
    # Métodos para usuários
    def get_all_users(self):
        """Obter todos os usuários da planilha."""
        try:
            worksheet = self.get_worksheet('usuarios')
            records = worksheet.get_all_records()
            return records
        except Exception as e:
            print(f"Erro ao obter usuários: {e}")
            return []
    
    def get_user_by_email(self, email):
        """Obter um usuário pelo email."""
        try:
            worksheet = self.get_worksheet('usuarios')
            records = worksheet.get_all_records()
            for record in records:
                if record['email'] == email:
                    return record
            return None
        except Exception as e:
            print(f"Erro ao obter usuário por email: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Obter um usuário pelo ID."""
        try:
            worksheet = self.get_worksheet('usuarios')
            records = worksheet.get_all_records()
            for record in records:
                if str(record['id']) == str(user_id):
                    return record
            return None
        except Exception as e:
            print(f"Erro ao obter usuário por ID: {e}")
            return None
    
    def add_user(self, user_data):
        """Adicionar um novo usuário à planilha."""
        try:
            worksheet = self.get_worksheet('usuarios')
            
            # Verificar se o email já existe
            existing_user = self.get_user_by_email(user_data.get('email'))
            if existing_user:
                print(f"Usuário com email {user_data.get('email')} já existe")
                return None
            
            # Gerar ID se não existir
            if not user_data.get('id'):
                records = worksheet.get_all_records()
                if records:
                    max_id = max([int(record['id']) for record in records if record['id'].isdigit()])
                    user_data['id'] = str(max_id + 1)
                else:
                    user_data['id'] = '1'
            
            # Adicionar data de criação se não existir
            if not user_data.get('data_criacao'):
                user_data['data_criacao'] = datetime.now().strftime('%d/%m/%Y')
                
            worksheet.append_row([
                user_data.get('id'),
                user_data.get('email'),
                user_data.get('nome'),
                user_data.get('senha_hash'),
                user_data.get('tipo', 'condomino'),
                user_data.get('data_criacao')
            ])
            return user_data
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            return None
