#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService

def test_format_simple():
    print("=== TESTE SIMPLES DE FORMATACAO ===")
    
    service = PDIAnalysisService()
    
    test_values = [0.0, 0.5, 0.99, 1.0, 50.0, 100.0, 999.99, 1000.0, 99999.99]
    
    print("Valores de teste:")
    for val in test_values:
        formatted = service._format_score(val)
        digits = len(str(formatted).replace('.', '').replace('0', '').replace('-', ''))
        if str(formatted).endswith('.0'):
            digits = len(str(formatted).replace('.0', ''))
        print(f"  {val:10.2f} -> {formatted:8.2f} ({digits} digitos)")
    
    print("\nTeste concluido!")

if __name__ == "__main__":
    test_format_simple()
