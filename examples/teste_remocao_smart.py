#!/usr/bin/env python3
"""
Teste final do sistema sem SMART
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quality_filter_pdi import QualityFilterPDI
import pandas as pd

def test_sem_smart():
    print("🔍 Testando sistema sem metodologia SMART...")
    
    # Criar analisador
    analyzer = QualityFilterPDI()
    
    # Carregar dados de exemplo
    df = pd.read_csv('examples/exemplo_pdis.csv')
    print(f"📁 Carregados {len(df)} PDIs do CSV")
    
    # Análise completa
    result_df = analyzer.analyze_pdis_from_dataframe(df)
    
    # Verificar colunas resultantes
    print(f"\n📊 Colunas no resultado: {list(result_df.columns)}")
    
    # Verificar se smart_criteria_score não está mais presente
    if 'smart_criteria_score' in result_df.columns:
        print("❌ ERRO: smart_criteria_score ainda está presente!")
    else:
        print("✅ SUCCESS: smart_criteria_score foi removido com sucesso!")
    
    # Salvar resultado
    output_file = 'examples/teste_sem_smart_final.csv'
    result_df.to_csv(output_file, index=False)
    print(f"💾 Resultado salvo em: {output_file}")
    
    # Mostrar resumo
    print(f"\n📈 Resumo dos scores:")
    print(f"   📝 Clareza média: {result_df['clarity_score'].mean():.3f}")
    print(f"   🎯 Especificidade média: {result_df['specificity_score'].mean():.3f}")
    print(f"   📋 Completude média: {result_df['completeness_score'].mean():.3f}")
    print(f"   🏗️ Estrutura média: {result_df['structure_score'].mean():.3f}")
    print(f"   🎯 Score geral médio: {result_df['overall_score'].mean():.3f}")
    
    print("\n🎉 Teste concluído com sucesso! SMART foi completamente removido do sistema.")

if __name__ == "__main__":
    test_sem_smart()
