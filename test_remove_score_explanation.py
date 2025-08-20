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

def test_score_explanation_removal():
    """
    Testa se a coluna score_explanation foi removida do CSV
    """
    print("=== TESTE DE REMOCAO DA COLUNA SCORE_EXPLANATION ===")
    print()
    
    try:
        from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
        
        print("OK - Servico importado com sucesso")
        
        # Criar dados de teste
        test_data = {
            'objetivo': [
                "Obter certificacao AWS Solutions Architect Associate ate junho de 2025 com nota minima de 720 pontos",
                "Aprender Python para desenvolvimento web ate dezembro",
                "Melhorar comunicacao"
            ],
            'acoes': [
                "Estudar documentacao oficial AWS 10 horas por semana, realizar 5 simulados praticos",
                "Fazer curso online de Python, praticar com projetos",
                "Estudar mais"
            ],
            'nome': ['Teste 1', 'Teste 2', 'Teste 3']
        }
        
        df_test = pd.DataFrame(test_data)
        print(f"OK - DataFrame de teste criado com {len(df_test)} registros")
        
        # Analisar dados
        analysis_service = PDIAnalysisService()
        results = analysis_service.analyze_dataframe(df_test)
        
        if results['success']:
            print(f"OK - Analise completada: {results['total_analyzed']} PDIs processados")
            
            # Verificar colunas do DataFrame resultante
            df_resultado = results['detailed_results']
            colunas = list(df_resultado.columns)
            
            print(f"\nCOLUNAS NO CSV FINAL ({len(colunas)} total):")
            for i, col in enumerate(colunas, 1):
                print(f"  {i:2d}. {col}")
            
            # Verificar se score_explanation foi removida
            if 'score_explanation' in colunas:
                print(f"\nERRO: Coluna 'score_explanation' ainda esta presente no CSV!")
                return False
            else:
                print(f"\nOK: Coluna 'score_explanation' foi removida com sucesso!")
            
            # Verificar se as outras colunas importantes estao presentes
            colunas_esperadas = ['feedback_responsavel', 'motivo_1', 'motivo_2', 'motivo_3']
            colunas_presentes = [col for col in colunas_esperadas if col in colunas]
            
            print(f"\nVERIFICACAO DE OUTRAS COLUNAS:")
            if len(colunas_presentes) == len(colunas_esperadas):
                print(f"  OK - Todas as colunas essenciais presentes: {colunas_presentes}")
            else:
                faltando = set(colunas_esperadas) - set(colunas_presentes)
                print(f"  AVISO - Colunas faltando: {faltando}")
            
            # Salvar arquivo de teste
            output_dir = project_root / "output"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / "teste_sem_score_explanation.csv"
            df_resultado.to_csv(output_file, index=False, encoding='utf-8')
            print(f"\nOK - Arquivo de teste salvo: {output_file}")
            
            # Mostrar estrutura final
            print(f"\nESTRUTURA FINAL DO CSV:")
            print("-" * 50)
            for idx, row in df_resultado.head(1).iterrows():
                print(f"Exemplo de registro:")
                for col in colunas:
                    valor = str(row[col])[:50] + "..." if len(str(row[col])) > 50 else str(row[col])
                    print(f"  {col:20s}: {valor}")
                break
            
            # Verificar tamanho do arquivo gerado
            file_size = output_file.stat().st_size
            print(f"\nTamanho do arquivo gerado: {file_size} bytes")
            
            # Status final
            if 'score_explanation' not in colunas and len(colunas_presentes) >= 3:
                print(f"\nSUCCESS - Teste passou! Coluna removida e estrutura adequada.")
                return True
            else:
                print(f"\nFAIL - Teste falhou! Verificar configuracao.")
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
    success = test_score_explanation_removal()
    print(f"\n=== RESULTADO FINAL: {'PASSOU' if success else 'FALHOU'} ===")
