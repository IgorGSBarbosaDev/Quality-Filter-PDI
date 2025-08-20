#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
    
    print("✓ Importações bem-sucedidas")
    
    # Criar resultado mock como dictionary (como o sistema usa)
    test_result = {
        'id': 1,
        'objetivo_desenvolvimento': 'Desenvolver habilidades de liderança',
        'acoes_planejadas': 'Participar de cursos e mentorias',
        'overall_score': 0.755,
        'clarity_score': 0.80,
        'specificity_score': 0.70,
        'completeness_score': 0.75,
        'structure_score': 0.80,
        'analysis_metadata': {
            'word_count': 10,
            'sentence_count': 2
        }
    }
    
    print("✓ Dados de teste criados")
    
    # Verificar DataFrame resultante usando o método interno
    service = PDIAnalysisService()
    df = service._create_results_dataframe([test_result])
    
    print("✓ DataFrame criado")
    print(f"Colunas ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Verificar se score_explanation foi removida
    if 'score_explanation' in df.columns:
        print("\n❌ ERRO: score_explanation ainda presente!")
    else:
        print("\n✅ SUCESSO: score_explanation removida!")
        
    # Verificar outras colunas removidas anteriormente
    removed_cols = ['has_numbers', 'negative_impact']
    for col in removed_cols:
        if col in df.columns:
            print(f"❌ ERRO: {col} ainda presente!")
        else:
            print(f"✅ OK: {col} removida!")
            
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
