#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Importar módulos
from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService
from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
import pandas as pd

def demonstrar_explicacao_notas():
    """
    Demonstra a nova funcionalidade de explicação detalhada das notas
    """
    print("🎯 DEMONSTRAÇÃO: EXPLICAÇÃO DETALHADA DAS NOTAS")
    print("=" * 60)
    
    # Exemplos de PDIs com diferentes qualidades
    exemplos = [
        {
            "titulo": "PDI ALTA QUALIDADE",
            "objetivo": "Obter certificação AWS Solutions Architect Associate até junho de 2025 com nota mínima de 720 pontos para atuar como arquiteto de soluções cloud",
            "acoes": "Estudar documentação oficial AWS 10 horas por semana, realizar 5 simulados práticos, completar curso preparatório de 80 horas na AWS Training, agendar exame para maio de 2025"
        },
        {
            "titulo": "PDI MÉDIA QUALIDADE", 
            "objetivo": "Aprender Python para desenvolvimento web",
            "acoes": "Fazer curso online, praticar com projetos"
        },
        {
            "titulo": "PDI BAIXA QUALIDADE",
            "objetivo": "Melhorar comunicação",
            "acoes": "Falar melhor"
        }
    ]
    
    # Instanciar serviços
    quality_service = QualityMetricsService()
    analysis_service = PDIAnalysisService()
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n🔍 EXEMPLO {i}: {exemplo['titulo']}")
        print("-" * 50)
        print(f"📝 Objetivo: {exemplo['objetivo']}")
        print(f"🎯 Ações: {exemplo['acoes']}")
        
        # Analisar PDI
        pdi_data = {
            'objetivo': exemplo['objetivo'],
            'acoes': exemplo['acoes']
        }
        
        result = analysis_service.analyze_single_pdi(pdi_data)
        
        # Gerar explicação detalhada
        explanation = quality_service.generate_score_explanation(
            result['clarity_score'],
            result['specificity_score'],
            result['completeness_score'], 
            result['structure_score'],
            result['smart_criteria_score'],
            result.get('analysis_metadata', {}).get('negative_impact', 0.0)
        )
        
        print(explanation)
        print("\n" + "="*60)
    
    # Demonstrar funcionamento em lote
    print("\n📊 DEMONSTRAÇÃO: ANÁLISE EM LOTE COM EXPLICAÇÕES")
    print("=" * 60)
    
    # Criar DataFrame de teste
    df_test = pd.DataFrame([
        {
            'objetivo': exemplo['objetivo'],
            'acoes': exemplo['acoes']
        } 
        for exemplo in exemplos
    ])
    
    # Analisar lote
    results = analysis_service.analyze_dataframe(df_test)
    
    if results['success']:
        print(f"✅ {results['total_analyzed']} PDIs analisados com sucesso!")
        
        # Salvar arquivo com explicações
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "demonstracao_explicacoes.csv"
        
        try:
            results['detailed_results'].to_csv(output_file, index=False, encoding='utf-8')
            print(f"📄 Arquivo salvo em: {output_file}")
            print("🔍 Verifique a coluna 'score_explanation' no arquivo CSV!")
            
            # Mostrar informações do arquivo
            print(f"\n📋 COLUNAS DO ARQUIVO GERADO:")
            for col in results['detailed_results'].columns:
                print(f"  • {col}")
                
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
    else:
        print(f"❌ Erro na análise: {results.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    try:
        demonstrar_explicacao_notas()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
