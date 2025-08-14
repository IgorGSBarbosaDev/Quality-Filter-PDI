#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService

def test_simple_explanation():
    """Teste simples da explicação de notas"""
    
    print("🧪 TESTE SIMPLES - EXPLICAÇÃO DE NOTAS")
    print("=" * 50)
    
    service = QualityMetricsService()
    
    # Texto de exemplo
    texto = "Aprender Python avançado até dezembro de 2025 para desenvolvimento de sistemas automatizados"
    
    # Calcular métricas
    clarity = service.calculate_clarity(texto)
    specificity = service.calculate_specificity(texto)  
    completeness = service.calculate_completeness(texto)
    structure = service.calculate_structure(texto)
    smart = service.calculate_smart_criteria(texto)
    negative = service.calculate_negative_impact(texto)
    
    print(f"📊 MÉTRICAS CALCULADAS:")
    print(f"• Clareza: {clarity:.2f}")
    print(f"• Especificidade: {specificity:.2f}")
    print(f"• Completude: {completeness:.2f}")
    print(f"• Estrutura: {structure:.2f}")
    print(f"• SMART: {smart:.2f}")
    print(f"• Impacto Negativo: {negative:.2f}")
    
    # Gerar explicação
    explanation = service.generate_score_explanation(clarity, specificity, completeness, structure, smart, negative)
    
    print("\n📋 EXPLICAÇÃO DETALHADA:")
    print(explanation)

if __name__ == "__main__":
    test_simple_explanation()
