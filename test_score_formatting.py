#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

import pandas as pd

def test_score_formatting():
    """
    Testa se todos os scores estão limitados a 4 dígitos
    """
    print("=== TESTE DE FORMATACAO DE SCORES ===")
    
    try:
        from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
        
        print("OK - Servico importado com sucesso")
        
        # Criar dados de teste com diferentes tamanhos para gerar scores variados
        test_data = {
            'objetivo': [
                "Este é um objetivo extremamente detalhado e muito específico com muitas palavras e informações técnicas para gerar um score alto e potencialmente números grandes",
                "Objetivo médio com algumas especificações",
                "Meta",
                "Desenvolver competências avançadas em tecnologia de última geração"
            ],
            'acoes': [
                "Realizar múltiplas ações detalhadas incluindo estudos avançados, certificações profissionais, projetos práticos, mentorias especializadas e avaliações periódicas",
                "Fazer curso e praticar regularmente",
                "Estudar",
                "Implementar estratégias inovadoras"
            ],
            'nome': ['Teste 1', 'Teste 2', 'Teste 3', 'Teste 4']
        }
        
        df_test = pd.DataFrame(test_data)
        print(f"OK - DataFrame de teste criado com {len(df_test)} registros")
        
        # Analisar dados
        analysis_service = PDIAnalysisService()
        results = analysis_service.analyze_dataframe(df_test)
        
        if results['success']:
            print(f"OK - Analise completada: {results['total_analyzed']} PDIs processados")
            
            # Verificar formatação dos scores
            df_resultado = results['detailed_results']
            
            # Colunas de score para verificar
            score_columns = [
                'overall_score', 'clarity_score', 'specificity_score', 
                'completeness_score', 'structure_score', 'smart_criteria_score'
            ]
            
            print(f"\nVERIFICACAO DE FORMATACAO DOS SCORES:")
            print("-" * 50)
            
            all_within_limit = True
            
            for col in score_columns:
                if col in df_resultado.columns:
                    max_val = df_resultado[col].max()
                    min_val = df_resultado[col].min()
                    
                    # Verificar número de dígitos
                    max_digits = len(str(max_val).replace('.', '').replace('-', ''))
                    
                    print(f"{col:20s}: Min={min_val:8.4f}, Max={max_val:8.4f}, Digitos={max_digits}")
                    
                    if max_digits > 4:
                        print(f"  ERRO: {col} excede 4 dígitos!")
                        all_within_limit = False
                    else:
                        print(f"  OK: {col} dentro do limite")
            
            # Mostrar amostra dos valores
            print(f"\nAMOSTRA DOS SCORES:")
            print("-" * 60)
            for idx, row in df_resultado.iterrows():
                print(f"PDI {idx+1}:")
                for col in score_columns:
                    if col in row:
                        valor = row[col]
                        digitos = len(str(valor).replace('.', '').replace('-', ''))
                        print(f"  {col:20s}: {valor:8.4f} ({digitos} dígitos)")
                print()
            
            # Testar método de formatação diretamente
            print(f"\nTESTE DIRETO DO METODO _format_score:")
            print("-" * 40)
            
            test_values = [0.0, 0.5, 0.99999, 1.0, 50.0, 100.0, 999.99, 1000.0, 99999.99]
            
            for val in test_values:
                formatted = analysis_service._format_score(val)
                original_digits = len(str(val).replace('.', '').replace('-', ''))
                formatted_digits = len(str(formatted).replace('.', '').replace('-', ''))
                
                print(f"  {val:10.4f} -> {formatted:8.4f} ({original_digits} -> {formatted_digits} dígitos)")
            
            # Status final
            if all_within_limit:
                print(f"\nSUCCESS - Todos os scores estao dentro do limite de 4 dígitos!")
                return True
            else:
                print(f"\nFAIL - Alguns scores excedem o limite de 4 dígitos!")
                return False
                
        else:
            print(f"ERRO - Falha na analise: {results.get('error', 'Erro desconhecido')}")
            return False
            
    except Exception as e:
        print(f"ERRO - Excecao: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_score_formatting()
    print(f"\n=== RESULTADO FINAL: {'PASSOU' if success else 'FALHOU'} ===")
