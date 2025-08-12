"""
Teste simples do sistema
"""
import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("Testando importações...")
    
    print("1. Importando pandas...")
    import pandas as pd
    
    print("2. Importando nltk...")
    import nltk
    
    print("3. Importando textstat...")
    import textstat
    
    print("4. Importando config...")
    from config.settings import ANALYSIS_CONFIG
    
    print("5. Importando text_processor...")
    from src.text_processor import TextProcessor
    
    print("6. Importando quality_metrics...")
    from src.quality_metrics import QualityMetrics
    
    print("7. Importando pdi_analyzer...")
    from src.pdi_analyzer import PDIAnalyzer
    
    print("\nTodas as importações foram bem-sucedidas!")
    
    # Teste básico
    print("\nTestando análise básica...")
    analyzer = PDIAnalyzer()
    
    result = analyzer.analyze_single_pdi(
        "Realizar curso de Python em 3 meses e aplicar em projeto real.",
        "Tornar-me desenvolvedor full-stack em 12 meses."
    )
    
    print(f"Resultado: {result['quality_level']} - Score: {result['quality_score']}")
    print("Teste concluído com sucesso!")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
