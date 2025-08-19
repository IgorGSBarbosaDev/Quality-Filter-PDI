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

from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService

def analyze_smart_impact():
    """
    Analisa o impacto de remover o critério SMART na nota geral
    """
    print("=== ANALISE DO IMPACTO DO CRITERIO SMART ===")
    print()
    
    # Configuração atual (COM SMART)
    weights_with_smart = {
        'clarity': 0.25,
        'specificity': 0.25,
        'completeness': 0.25,
        'structure': 0.15,
        'smart_criteria': 0.10
    }
    
    # Configuração proposta (SEM SMART - redistribuindo proporcionalmente)
    # Removendo smart (0.10) e redistribuindo entre os outros
    total_without_smart = 0.90  # 1.0 - 0.10
    weights_without_smart = {
        'clarity': 0.25 / total_without_smart,      # 0.278 (27.8%)
        'specificity': 0.25 / total_without_smart,  # 0.278 (27.8%)
        'completeness': 0.25 / total_without_smart, # 0.278 (27.8%)
        'structure': 0.15 / total_without_smart,    # 0.167 (16.7%)
        'smart_criteria': 0.0                       # 0.0 (0%)
    }
    
    print("CONFIGURACAO ATUAL (COM SMART):")
    for criterion, weight in weights_with_smart.items():
        print(f"  {criterion:15s}: {weight:.3f} ({weight*100:5.1f}%)")
    print(f"  {'TOTAL':15s}: {sum(weights_with_smart.values()):.3f}")
    
    print("\nCONFIGURACAO PROPOSTA (SEM SMART):")
    for criterion, weight in weights_without_smart.items():
        if weight > 0:
            print(f"  {criterion:15s}: {weight:.3f} ({weight*100:5.1f}%)")
    print(f"  {'TOTAL':15s}: {sum(weights_without_smart.values()):.3f}")
    
    # Criar service para testar
    service = QualityMetricsService()
    
    # Criar cenários de teste variados
    test_scenarios = [
        {
            'name': 'PDI Excelente',
            'text': 'Obter certificação AWS Solutions Architect Associate até junho de 2025 com nota mínima de 720 pontos para atuar como arquiteto de soluções cloud. Estudar documentação oficial AWS 10 horas por semana, realizar 5 simulados práticos na plataforma WhizLabs, completar curso preparatório de 80 horas.',
            'description': 'PDI bem estruturado com objetivos claros e ações específicas'
        },
        {
            'name': 'PDI Médio',
            'text': 'Aprender Python para desenvolvimento web até dezembro. Fazer curso online de Python, praticar com projetos pequenos.',
            'description': 'PDI com direção clara mas falta detalhamento'
        },
        {
            'name': 'PDI Fraco',
            'text': 'Melhorar comunicação. Estudar mais.',
            'description': 'PDI vago sem especificações adequadas'
        },
        {
            'name': 'PDI Técnico',
            'text': 'Desenvolver expertise em machine learning aplicado a análise de dados financeiros até Q4 2025. Completar especialização Stanford CS229, implementar 3 projetos práticos.',
            'description': 'PDI técnico com terminologia específica'
        },
        {
            'name': 'PDI Simples',
            'text': 'Aprender Excel avançado em 6 meses. Fazer curso online.',
            'description': 'PDI simples mas com prazo definido'
        }
    ]
    
    print("\n" + "="*80)
    print("ANALISE COMPARATIVA POR CENARIO")
    print("="*80)
    
    results_comparison = []
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name'].upper()}:")
        print(f"Texto: {scenario['text']}")
        print(f"Descricao: {scenario['description']}")
        print("-" * 60)
        
        # Calcular scores individuais
        clarity = service.calculate_clarity(scenario['text'])
        specificity = service.calculate_specificity(scenario['text'])
        completeness = service.calculate_completeness(scenario['text'])
        structure = service.calculate_structure(scenario['text'])
        smart = service.calculate_smart_criteria(scenario['text'])
        
        print(f"Scores individuais:")
        print(f"  Clareza:       {clarity:.3f}")
        print(f"  Especificidade: {specificity:.3f}")
        print(f"  Completude:     {completeness:.3f}")
        print(f"  Estrutura:      {structure:.3f}")
        print(f"  SMART:          {smart:.3f}")
        
        # Calcular nota COM SMART
        score_with_smart = (
            clarity * weights_with_smart['clarity'] +
            specificity * weights_with_smart['specificity'] +
            completeness * weights_with_smart['completeness'] +
            structure * weights_with_smart['structure'] +
            smart * weights_with_smart['smart_criteria']
        )
        
        # Calcular nota SEM SMART
        score_without_smart = (
            clarity * weights_without_smart['clarity'] +
            specificity * weights_without_smart['specificity'] +
            completeness * weights_without_smart['completeness'] +
            structure * weights_without_smart['structure']
        )
        
        # Diferença
        difference = score_without_smart - score_with_smart
        percent_change = (difference / score_with_smart) * 100 if score_with_smart > 0 else 0
        
        print(f"\nResultados:")
        print(f"  COM SMART:    {score_with_smart:.3f} ({score_with_smart*100:5.1f}%)")
        print(f"  SEM SMART:    {score_without_smart:.3f} ({score_without_smart*100:5.1f}%)")
        print(f"  DIFERENCA:    {difference:+.3f} ({percent_change:+5.1f}%)")
        
        # Determinar impacto
        if difference > 0:
            impact = "MELHORA"
        elif difference < 0:
            impact = "PIORA"
        else:
            impact = "NEUTRO"
        
        print(f"  IMPACTO:      {impact}")
        
        results_comparison.append({
            'scenario': scenario['name'],
            'with_smart': score_with_smart,
            'without_smart': score_without_smart,
            'difference': difference,
            'percent_change': percent_change,
            'impact': impact,
            'smart_score': smart
        })
    
    # Análise estatística
    print("\n" + "="*80)
    print("ANALISE ESTATISTICA GERAL")
    print("="*80)
    
    df_results = pd.DataFrame(results_comparison)
    
    print(f"Total de cenários analisados: {len(df_results)}")
    print(f"\nEstatísticas da diferença:")
    print(f"  Média:      {df_results['difference'].mean():+.3f}")
    print(f"  Mediana:    {df_results['difference'].median():+.3f}")
    print(f"  Mínimo:     {df_results['difference'].min():+.3f}")
    print(f"  Máximo:     {df_results['difference'].max():+.3f}")
    print(f"  Desvio:     {df_results['difference'].std():.3f}")
    
    print(f"\nEstatísticas da variação percentual:")
    print(f"  Média:      {df_results['percent_change'].mean():+5.1f}%")
    print(f"  Mediana:    {df_results['percent_change'].median():+5.1f}%")
    print(f"  Mínimo:     {df_results['percent_change'].min():+5.1f}%")
    print(f"  Máximo:     {df_results['percent_change'].max():+5.1f}%")
    
    # Contar impactos
    impact_counts = df_results['impact'].value_counts()
    print(f"\nDistribuição de impactos:")
    for impact, count in impact_counts.items():
        print(f"  {impact:10s}: {count} cenários ({count/len(df_results)*100:.1f}%)")
    
    # Análise por performance do critério SMART
    print(f"\nAnalise por performance do criterio SMART:")
    print(f"  Score SMART médio: {df_results['smart_score'].mean():.3f}")
    print(f"  Score SMART mínimo: {df_results['smart_score'].min():.3f}")
    print(f"  Score SMART máximo: {df_results['smart_score'].max():.3f}")
    
    # Recomendação
    print("\n" + "="*80)
    print("RECOMENDACAO")
    print("="*80)
    
    avg_improvement = df_results['difference'].mean()
    improvement_scenarios = len(df_results[df_results['difference'] > 0])
    total_scenarios = len(df_results)
    
    if avg_improvement > 0 and improvement_scenarios >= total_scenarios * 0.7:
        recommendation = "REMOVER"
        reason = f"A remoção do critério SMART melhora a nota em {improvement_scenarios}/{total_scenarios} cenários ({improvement_scenarios/total_scenarios*100:.1f}%) com melhoria média de {avg_improvement*100:+.1f}%"
    elif avg_improvement < -0.05:
        recommendation = "MANTER"
        reason = f"A remoção do critério SMART prejudica significativamente as notas (redução média de {abs(avg_improvement)*100:.1f}%)"
    else:
        recommendation = "NEUTRO"
        reason = f"O impacto da remoção é mínimo (variação média de {avg_improvement*100:+.1f}%)"
    
    print(f"RECOMENDACAO: {recommendation} o critério SMART")
    print(f"JUSTIFICATIVA: {reason}")
    
    if recommendation == "REMOVER":
        print(f"\nNOVOS PESOS SUGERIDOS (sem SMART):")
        for criterion, weight in weights_without_smart.items():
            if weight > 0:
                print(f"  {criterion:15s}: {weight:.3f} ({weight*100:5.1f}%)")
    
    return df_results, recommendation, weights_without_smart

if __name__ == "__main__":
    try:
        results, recommendation, new_weights = analyze_smart_impact()
        
        # Salvar resultados
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "analise_criterio_smart.csv"
        results.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\nResultados salvos em: {output_file}")
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
