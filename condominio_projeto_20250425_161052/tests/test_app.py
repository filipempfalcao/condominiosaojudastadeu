"""
Script para testar as funcionalidades do site de controle de demandas do condomínio.
Este script realiza testes automatizados para verificar o funcionamento correto do sistema.
"""

import os
import sys
import unittest
import json
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.database.sheets_api import SheetsDatabase
from app.dashboard.charts import processar_dados_demandas, calcular_indicadores

class TestSiteCondominio(unittest.TestCase):
    """Classe de testes para o site de controle de demandas do condomínio."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Configurar banco de dados de teste
        # Nota: Em um ambiente real, usaríamos um banco de dados de teste separado
        self.db = SheetsDatabase(
            os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json'),
            os.environ.get('SPREADSHEET_NAME', 'Condominio_Sao_Judas_Tadeu_Test')
        )
        
        # Dados de teste
        self.test_user = {
            'email': 'teste@exemplo.com',
            'nome': 'Usuário Teste',
            'senha': 'senha123',
            'tipo': 'condomino'
        }
        
        self.test_demanda = {
            'titulo': 'Demanda de Teste',
            'categoria': 'Elétrica',
            'criticidade': 'Média',
            'descricao': 'Esta é uma demanda de teste para verificar o funcionamento do sistema.',
            'localizacao': 'Área de teste, próximo à entrada',
            'status': 'Aberta',
            'data_criacao': datetime.now().strftime('%d/%m/%Y'),
            'data_atualizacao': datetime.now().strftime('%d/%m/%Y')
        }
    
    def tearDown(self):
        """Limpeza após os testes."""
        self.app_context.pop()
    
    def test_pagina_inicial(self):
        """Teste para verificar se a página inicial redireciona para a página de demandas."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        self.assertTrue('/demandas' in response.location)
    
    def test_pagina_login(self):
        """Teste para verificar se a página de login é carregada corretamente."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_pagina_registro(self):
        """Teste para verificar se a página de registro é carregada corretamente."""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro', response.data)
    
    def test_acesso_protegido(self):
        """Teste para verificar se as páginas protegidas redirecionam para o login."""
        # Testar acesso à página de demandas sem autenticação
        response = self.client.get('/demandas/')
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        self.assertTrue('/auth/login' in response.location)
        
        # Testar acesso à página de dashboard sem autenticação
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        self.assertTrue('/auth/login' in response.location)
    
    def test_processar_dados_demandas(self):
        """Teste para verificar o processamento de dados das demandas."""
        # Criar algumas demandas de teste
        demandas = [
            {
                'id': '001',
                'titulo': 'Demanda 1',
                'categoria': 'Elétrica',
                'criticidade': 'Alta',
                'descricao': 'Descrição 1',
                'localizacao': 'Local 1',
                'status': 'Aberta',
                'data_criacao': '01/04/2025',
                'data_atualizacao': '01/04/2025'
            },
            {
                'id': '002',
                'titulo': 'Demanda 2',
                'categoria': 'Hidráulica',
                'criticidade': 'Média',
                'descricao': 'Descrição 2',
                'localizacao': 'Local 2',
                'status': 'Resolvida',
                'data_criacao': '02/04/2025',
                'data_atualizacao': '05/04/2025'
            }
        ]
        
        # Processar dados
        df = processar_dados_demandas(demandas)
        
        # Verificar se o DataFrame foi criado corretamente
        self.assertEqual(len(df), 2)
        self.assertIn('tempo_resolucao', df.columns)
        
        # Verificar se o tempo de resolução foi calculado corretamente
        self.assertEqual(df.loc[df['id'] == '002', 'tempo_resolucao'].values[0], 3)
    
    def test_calcular_indicadores(self):
        """Teste para verificar o cálculo de indicadores."""
        # Criar algumas demandas de teste
        demandas = [
            {
                'id': '001',
                'titulo': 'Demanda 1',
                'categoria': 'Elétrica',
                'criticidade': 'Alta',
                'descricao': 'Descrição 1',
                'localizacao': 'Local 1',
                'status': 'Aberta',
                'data_criacao': '01/04/2025',
                'data_atualizacao': '01/04/2025'
            },
            {
                'id': '002',
                'titulo': 'Demanda 2',
                'categoria': 'Hidráulica',
                'criticidade': 'Média',
                'descricao': 'Descrição 2',
                'localizacao': 'Local 2',
                'status': 'Resolvida',
                'data_criacao': '02/04/2025',
                'data_atualizacao': '05/04/2025'
            }
        ]
        
        # Processar dados
        df = processar_dados_demandas(demandas)
        
        # Calcular indicadores
        indicadores = calcular_indicadores(df)
        
        # Verificar se os indicadores foram calculados corretamente
        self.assertEqual(indicadores['total_demandas'], 2)
        self.assertEqual(indicadores['demandas_abertas'], 1)
        self.assertEqual(indicadores['tempo_medio_resolucao'], 3)
        self.assertEqual(indicadores['taxa_resolucao'], 50)

if __name__ == '__main__':
    unittest.main()
