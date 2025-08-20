#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService
from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
import pandas as pd

def demonstrar_feedback_responsavel():
    """
    Demonstra a nova funcionalidade de feedback direto para o responsável pelo PDI
    """
    print("🎯 DEMONSTRAÇÃO: FEEDBACK PARA O RESPONSÁVEL DO PDI")
    print("=" * 60)
    
    # Exemplos de PDIs com diferentes qualidades
    exemplos = [
        {
            "titulo": "PDI EXCELENTE (80+ pontos)",
            "objetivo": "Obter certificação AWS Solutions Architect Associate até junho de 2025 com nota mínima de 720 pontos para atuar como arquiteto de soluções cloud sênior",
            "acoes": "Estudar documentação oficial AWS 10 horas por semana, realizar 5 simulados práticos na plataforma WhizLabs, completar curso preparatório de 80 horas na AWS Training, agendar exame para maio de 2025, criar 3 projetos práticos com EC2, S3 e RDS"
        },
        {
            "titulo": "PDI BOM (60-79 pontos)", 
            "objetivo": "Aprender Python para desenvolvimento web até dezembro",
            "acoes": "Fazer curso online de Python, praticar com projetos reais, estudar frameworks Django"
        },
        {
            "titulo": "PDI REGULAR (40-59 pontos)",
            "objetivo": "Melhorar habilidades de comunicação",
            "acoes": "Participar de treinamentos e praticar apresentações"
        },
        {
            "titulo": "PDI INADEQUADO (0-39 pontos)",
            "objetivo": "Melhorar",
            "acoes": "Estudar"
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
        
        # Gerar feedback para o responsável
        feedback = quality_service.generate_feedback_for_responsible(
            result['clarity_score'],
            result['specificity_score'],
            result['completeness_score'], 
            result['structure_score'],
            result['smart_criteria_score'],
            result.get('analysis_metadata', {}).get('negative_impact', 0.0),
            result['overall_score'] * 100
        )
        
        print(f"\n📋 FEEDBACK PARA O RESPONSÁVEL:")
        print("=" * 50)
        print(feedback)
        print("\n" + "="*60)
    
    # Demonstrar funcionamento em lote com arquivo CSV
    print("\n📊 DEMONSTRAÇÃO: ARQUIVO CSV COM FEEDBACK PARA RESPONSÁVEIS")
    print("=" * 60)
    
    # Criar DataFrame de teste
    df_test = pd.DataFrame([
        {
            'objetivo': exemplo['objetivo'],
            'acoes': exemplo['acoes'],
            'nome_responsavel': f'Colaborador {i}'
        } 
        for i, exemplo in enumerate(exemplos, 1)
    ])
    
    # Analisar lote
    results = analysis_service.analyze_dataframe(df_test)
    
    if results['success']:
        print(f"✅ {results['total_analyzed']} PDIs analisados com sucesso!")
        
        # Salvar arquivo com feedback para responsáveis
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "pdis_com_feedback_responsavel.csv"
        
        try:
            results['detailed_results'].to_csv(output_file, index=False, encoding='utf-8')
            print(f"📄 Arquivo salvo em: {output_file}")
            print("🔍 NOVAS COLUNAS ADICIONADAS:")
            print("  • score_explanation: Explicação técnica detalhada")
            print("  • feedback_responsavel: Feedback direto para o responsável")
            
            # Mostrar amostra do feedback
            sample_feedback = results['detailed_results']['feedback_responsavel'].iloc[0]
            print(f"\n📋 AMOSTRA DO FEEDBACK PARA RESPONSÁVEL:")
            print("-" * 50)
            print(sample_feedback[:300] + "..." if len(sample_feedback) > 300 else sample_feedback)
                
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
    else:
        print(f"❌ Erro na análise: {results.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    try:
        demonstrar_feedback_responsavel()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
