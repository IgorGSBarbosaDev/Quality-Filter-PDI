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

def test_csv_columns():
    """
    Testa se as colunas has_numbers e negative_impact foram removidas do CSV
    """
    print("=== TESTE DE REMOCAO DE COLUNAS ===")
    
    try:
        from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
        from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService
        
        print("OK - Servicos importados com sucesso")
        
        # Criar dados de teste
        test_data = {
            'objetivo': [
                "Obter certificacao AWS Solutions Architect Associate ate junho de 2025 com nota minima de 720 pontos",
                "Aprender Python para desenvolvimento web ate dezembro",
                "Melhorar comunicacao"
            ],
            'acoes': [
                "Estudar documentacao oficial AWS 10 horas por semana, realizar 5 simulados praticos na plataforma WhizLabs",
                "Fazer curso online de Python, praticar com projetos",
                "Estudar"
            ],
            'nome': ['Colaborador 1', 'Colaborador 2', 'Colaborador 3']
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
            
            # Verificar se as colunas removidas estao ausentes
            colunas_removidas = ['has_numbers', 'negative_impact']
            colunas_presentes = []
            colunas_ausentes = []
            
            for col in colunas_removidas:
                if col in colunas:
                    colunas_presentes.append(col)
                else:
                    colunas_ausentes.append(col)
            
            print(f"\nVERIFICACAO DE REMOCAO:")
            if colunas_ausentes:
                print(f"  OK - Colunas removidas com sucesso: {colunas_ausentes}")
            if colunas_presentes:
                print(f"  ERRO - Colunas ainda presentes: {colunas_presentes}")
            
            # Verificar se as novas colunas de motivos estao presentes
            colunas_esperadas = ['motivo_1', 'motivo_2', 'motivo_3']
            colunas_motivos = [col for col in colunas_esperadas if col in colunas]
            
            print(f"\nVERIFICACAO DE MOTIVOS CONCISOS:")
            if len(colunas_motivos) == 3:
                print(f"  OK - Todas as colunas de motivos presentes: {colunas_motivos}")
            else:
                print(f"  ERRO - Colunas de motivos faltando: {set(colunas_esperadas) - set(colunas_motivos)}")
            
            # Salvar arquivo de teste
            output_dir = project_root / "output"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / "teste_colunas_removidas.csv"
            df_resultado.to_csv(output_file, index=False, encoding='utf-8')
            print(f"\nOK - Arquivo de teste salvo: {output_file}")
            
            # Mostrar amostra dos dados
            print(f"\nAMOSTRA DO RESULTADO:")
            print("-" * 50)
            for idx, row in df_resultado.head(2).iterrows():
                print(f"PDI {idx+1}:")
                print(f"  Nota: {row['overall_score']:.1f}")
                print(f"  Motivo 1: {row['motivo_1']}")
                print(f"  Motivo 2: {row['motivo_2']}")
                print(f"  Motivo 3: {row['motivo_3']}")
                print()
            
            # Status final
            if not colunas_presentes and len(colunas_motivos) == 3:
                print("SUCCESS - Teste passou! Colunas removidas e motivos presentes.")
                return True
            else:
                print("FAIL - Teste falhou! Verificar configuracao.")
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
    success = test_csv_columns()
    print(f"\n=== RESULTADO FINAL: {'PASSOU' if success else 'FALHOU'} ===")
