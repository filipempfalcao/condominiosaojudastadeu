"""
Script para criar um arquivo ZIP com todos os arquivos do projeto para distribuição.
"""

import os
import zipfile
import datetime

def create_zip():
    """Cria um arquivo ZIP com todos os arquivos do projeto."""
    # Nome do arquivo ZIP com data e hora atual
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"condominio_projeto_{timestamp}.zip"
    
    # Diretórios e arquivos a serem incluídos
    include_dirs = ['app', 'docs', 'tests']
    include_files = ['run.py', 'requirements.txt', 'README.md', 'run_tests.py']
    
    # Diretórios e arquivos a serem excluídos
    exclude_patterns = ['__pycache__', '.pyc', '.env', 'venv', 'credentials.json']
    
    # Criar o arquivo ZIP
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Adicionar arquivos individuais
        for file in include_files:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Adicionado: {file}")
        
        # Adicionar diretórios
        for dir_name in include_dirs:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    # Excluir diretórios indesejados
                    dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
                    
                    for file in files:
                        # Excluir arquivos indesejados
                        if not any(pattern in file for pattern in exclude_patterns):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"Adicionado: {file_path}")
    
    print(f"\nArquivo ZIP criado: {zip_filename}")
    return zip_filename

if __name__ == "__main__":
    create_zip()
