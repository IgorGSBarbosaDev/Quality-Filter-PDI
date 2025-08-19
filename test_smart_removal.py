#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path
import pandas as pd

# Configurar path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService

def test_smart_removal():
    """
    Testa se a remoção do critério SMART está funcionando corretamente
    """
    print("=== TESTE DE REMOCAO DO CRITERIO SMART ===")
    print()
    
    # Criar dados de teste
    test_data = {
        'objetivo': [
            "Obter certificação AWS Solutions Architect Associate até junho de 2025 com nota mínima de 720 pontos",
            "Aprender Python para desenvolvimento web até dezembro",
            "Melhorar comunicação"
        ],
        'acoes': [
            "Estudar documentação oficial AWS 10 horas por semana, realizar 5 simulados práticos",
            "Fazer curso online de Python, praticar com projetos",
            "Estudar mais"
        ],
        'nome': ['Teste 1', 'Teste 2', 'Teste 3']
    }
    
    df_test = pd.DataFrame(test_data)
    print(f"Dados de teste criados: {len(df_test)} PDIs")
    
    # Analisar com o novo sistema (sem SMART)
    analysis_service = PDIAnalysisService()
    results = analysis_service.analyze_dataframe(df_test)
    
    if results['success']:
        print(f"Análise completada: {results['total_analyzed']} PDIs processados")
        
        df_resultado = results['detailed_results']
        
        print(f"\nRESULTADOS COM NOVA CONFIGURACAO (SEM SMART):")
        print("="*60)
        
        for idx, row in df_resultado.iterrows():
            print(f"\nPDI {idx+1}: {test_data['nome'][idx]}")
            print(f"  Objetivo: {test_data['objetivo'][idx][:50]}...")
            print(f"  Nota Final: {row['overall_score']:.2f}")
            print(f"  Scores individuais:")
            print(f"    Clareza:       {row['clarity_score']:.3f}")
            print(f"    Especificidade: {row['specificity_score']:.3f}")
            print(f"    Completude:     {row['completeness_score']:.3f}")
            print(f"    Estrutura:      {row['structure_score']:.3f}")
            print(f"    SMART:          {row['smart_criteria_score']:.3f} (peso 0%)")
            print(f"  Motivos:")
            print(f"    1. {row['motivo_1']}")
            print(f"    2. {row['motivo_2']}")
            print(f"    3. {row['motivo_3']}")
        
        # Validar que o critério SMART não está mais impactando
        print(f"\nVALIDACAO:")
        print("-"*40)
        
        # Teste: verificar se scores SMART altos/baixos não afetam mais a nota
        all_tests_passed = True
        
        for idx, row in df_resultado.iterrows():
            # Recalcular nota manualmente com os novos pesos
            expected_score = (
                row['clarity_score'] * 0.278 +
                row['specificity_score'] * 0.278 + 
                row['completeness_score'] * 0.278 +
                row['structure_score'] * 0.167
                # SMART score não incluído
            )
            
            actual_score = row['overall_score']
            
            # Tolerância de 0.01 para diferenças de arredondamento
            if abs(expected_score - actual_score) > 0.01:
                print(f"ERRO: PDI {idx+1} - Esperado: {expected_score:.3f}, Atual: {actual_score:.3f}")
                all_tests_passed = False
            else:
                print(f"OK: PDI {idx+1} - Nota calculada corretamente ({actual_score:.3f})")
        
        # Verificar se explicações não mencionam SMART
        smart_mentions = 0
        for idx, row in df_resultado.iterrows():
            explanation = row['score_explanation'].lower()
            if 'smart' in explanation and 'critérios smart' in explanation:
                smart_mentions += 1
                print(f"AVISO: PDI {idx+1} ainda menciona critérios SMART na explicação")
        
        if smart_mentions == 0:
            print("OK: Nenhuma explicação menciona critérios SMART")
        
        # Calcular melhoria média
        print(f"\nRESUMO DA REMOCAO:")
        print("-"*40)
        print(f"Total de PDIs analisados: {len(df_resultado)}")
        print(f"Nota média: {df_resultado['overall_score'].mean():.2f}")
        print(f"Nota mínima: {df_resultado['overall_score'].min():.2f}")
        print(f"Nota máxima: {df_resultado['overall_score'].max():.2f}")
        
        print(f"\nNOVOS PESOS ATIVOS:")
        print(f"  Clareza:       27.8%")
        print(f"  Especificidade: 27.8%")
        print(f"  Completude:     27.8%")
        print(f"  Estrutura:      16.7%")
        print(f"  SMART:           0.0% (REMOVIDO)")
        
        if all_tests_passed:
            print(f"\nSUCCESS: Critério SMART removido com sucesso!")
            return True
        else:
            print(f"\nFAIL: Problemas detectados na remoção do SMART")
            return False
            
    else:
        print(f"ERRO: Falha na análise - {results.get('error', 'Erro desconhecido')}")
        return False

if __name__ == "__main__":
    success = test_smart_removal()
    print(f"\n=== RESULTADO: {'PASSOU' if success else 'FALHOU'} ===")
