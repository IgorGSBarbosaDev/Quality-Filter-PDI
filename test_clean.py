#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

print("=== TESTE SIMPLES DE MOTIVOS CONCISOS ===")

try:
    from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService
    print("OK - QualityMetricsService importado com sucesso")
    
    # Teste básico
    service = QualityMetricsService()
    print("OK - Servico instanciado")
    
    # Testar método de motivos concisos
    motivos = service.generate_concise_reasons(
        clarity=0.8,
        specificity=0.6, 
        completeness=0.4,
        structure=0.7,
        smart=0.5,
        actionability=0.0,
        overall_score=60.0
    )
    
    print("OK - Motivos concisos gerados:")
    print(f"  Motivo 1: {motivos['motivo_1']}")
    print(f"  Motivo 2: {motivos['motivo_2']}")
    print(f"  Motivo 3: {motivos['motivo_3']}")
    
except ImportError as e:
    print(f"ERRO - Erro de importacao: {e}")
except Exception as e:
    print(f"ERRO - Erro geral: {e}")
    import traceback
    traceback.print_exc()

print("\n=== FIM DO TESTE ===")
