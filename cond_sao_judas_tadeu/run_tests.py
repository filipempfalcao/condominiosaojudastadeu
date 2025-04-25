"""
Script para executar os testes e gerar relatório de cobertura.
"""

import unittest
import coverage
import os
import sys

# Configurar cobertura de código
cov = coverage.Coverage(
    branch=True,
    include=["app/*"],
    omit=["tests/*", "*/venv/*"]
)
cov.start()

# Descobrir e executar todos os testes
test_loader = unittest.TestLoader()
test_suite = test_loader.discover('tests', pattern='test_*.py')
test_runner = unittest.TextTestRunner(verbosity=2)
test_result = test_runner.run(test_suite)

# Gerar relatório de cobertura
cov.stop()
cov.save()

print("\nCobertura de código:")
cov.report()

# Gerar relatório HTML
cov_dir = os.path.join(os.path.dirname(__file__), 'coverage_html')
cov.html_report(directory=cov_dir)
print(f"\nRelatório HTML de cobertura gerado em: {cov_dir}")

# Retornar código de saída apropriado
sys.exit(not test_result.wasSuccessful())
