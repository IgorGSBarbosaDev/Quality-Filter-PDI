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

def demonstrar_motivos_concisos():
    """
    Demonstra a nova funcionalidade de motivos concisos sem emojis
    """
    print("🧪 DEMONSTRAÇÃO: MOTIVOS CONCISOS PARA CSV")
    print("=" * 60)
    
    # Exemplos de PDIs com diferentes qualidades
    exemplos = [
        {
            "titulo": "PDI Excelente",
            "objetivo": "Obter certificação AWS Solutions Architect Associate até junho de 2025 com nota mínima de 720 pontos para atuar como arquiteto de soluções cloud",
            "acoes": "Estudar documentação oficial AWS 10 horas por semana, realizar 5 simulados práticos na plataforma WhizLabs, completar curso preparatório de 80 horas, agendar exame para maio de 2025"
        },
        {
            "titulo": "PDI Médio", 
            "objetivo": "Aprender Python para desenvolvimento web até dezembro",
            "acoes": "Fazer curso online de Python, praticar com projetos"
        },
        {
            "titulo": "PDI Ruim",
            "objetivo": "Melhorar comunicação",
            "acoes": "Estudar"
        }
    ]
    
    # Instanciar serviços
    quality_service = QualityMetricsService()
    
    print("EXEMPLOS DE MOTIVOS CONCISOS (sem emojis, texto direto):")
    print("-" * 60)
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n{i}. {exemplo['titulo']}:")
        print(f"   Objetivo: {exemplo['objetivo']}")
        print(f"   Ações: {exemplo['acoes']}")
        
        # Calcular métricas básicas
        clarity = quality_service.calculate_clarity(f"{exemplo['objetivo']} {exemplo['acoes']}")
        specificity = quality_service.calculate_specificity(f"{exemplo['objetivo']} {exemplo['acoes']}")
        completeness = quality_service.calculate_completeness(f"{exemplo['objetivo']} {exemplo['acoes']}")
        structure = quality_service.calculate_structure(f"{exemplo['objetivo']} {exemplo['acoes']}")
        smart = quality_service.calculate_smart_criteria(f"{exemplo['objetivo']} {exemplo['acoes']}")
        
        # Calcular nota final
        overall_score = (clarity * 0.25 + specificity * 0.25 + completeness * 0.25 + 
                        structure * 0.15 + smart * 0.10) * 100
        
        # Gerar motivos concisos
        motivos = quality_service.generate_concise_reasons(
            clarity, specificity, completeness, structure, smart, 0.0, overall_score
        )
        
        print(f"   Nota: {overall_score:.1f}/100")
        print(f"   Motivo 1: {motivos['motivo_1']}")
        print(f"   Motivo 2: {motivos['motivo_2']}")
        print(f"   Motivo 3: {motivos['motivo_3']}")
    
    # Demonstrar arquivo CSV completo
    print(f"\n{'='*60}")
    print("ARQUIVO CSV COMPLETO COM NOVAS COLUNAS:")
    print("-" * 60)
    
    # Criar DataFrame de teste
    df_test = pd.DataFrame([
        {
            'objetivo': exemplo['objetivo'],
            'acoes': exemplo['acoes'],
            'nome': f'Colaborador {i}'
        } 
        for i, exemplo in enumerate(exemplos, 1)
    ])
    
    # Analisar com o serviço completo
    analysis_service = PDIAnalysisService()
    results = analysis_service.analyze_dataframe(df_test)
    
    if results['success']:
        print(f"✅ {results['total_analyzed']} PDIs analisados com sucesso!")
        
        # Salvar arquivo CSV limpo
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "pdis_motivos_concisos.csv"
        
        try:
            results['detailed_results'].to_csv(output_file, index=False, encoding='utf-8')
            print(f"📄 Arquivo salvo em: {output_file}")
            
            print(f"\n📋 COLUNAS DO ARQUIVO CSV:")
            for col in results['detailed_results'].columns:
                if col.startswith('motivo_'):
                    print(f"  🆕 {col}")  # Destacar novas colunas
                else:
                    print(f"     {col}")
            
            # Mostrar amostra das novas colunas
            print(f"\n📊 AMOSTRA DAS NOVAS COLUNAS:")
            print("-" * 40)
            for idx, row in results['detailed_results'].iterrows():
                print(f"PDI {idx+1}:")
                print(f"  Nota: {row['overall_score']:.1f}")
                print(f"  Motivo 1: {row['motivo_1']}")
                print(f"  Motivo 2: {row['motivo_2']}")
                print(f"  Motivo 3: {row['motivo_3']}")
                print()
                
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
    else:
        print(f"❌ Erro na análise: {results.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    try:
        demonstrar_motivos_concisos()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
