#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from app import PDIAnalyzer

def test_complete_system():
    analyzer = PDIAnalyzer()
    
    test_cases = [
        {
            'objetivo': 'Aprender Python para desenvolvimento web',
            'acoes': 'Fazer curso online, praticar projetos'
        },
        {
            'objetivo': 'Desenvolver habilidades de liderança',
            'acoes': 'Participar de workshops, liderar projetos'
        },
        {
            'objetivo': 'Obter certificação AWS Solutions Architect',
            'acoes': 'Estudar documentação, fazer labs práticos'
        }
    ]
    
    print("🚀 TESTE COMPLETO DO SISTEMA PDI")
    print("=" * 50)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 TESTE {i}")
        print(f"Objetivo: {case['objetivo']}")
        print(f"Ações: {case['acoes']}")
        
        try:
            result = analyzer.analyze_text(case['objetivo'], case['acoes'])
            
            print(f"\n📊 Resultados:")
            print(f"Score: {result['overall_score']:.2f}")
            print(f"Qualidade: {result['quality_level']}")
            
            if 'skill_classification' in result:
                skill = result['skill_classification']
                print(f"Tipo Habilidade: {skill['skill_type']}")
                print(f"Confiança: {skill['confidence']:.2f}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
        
        print("-" * 40)

if __name__ == "__main__":
    test_complete_system()
