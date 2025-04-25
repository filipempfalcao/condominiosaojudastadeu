"""
Script para iniciar a aplicação Flask do site de controle de demandas do condomínio.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
