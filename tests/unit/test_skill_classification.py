from app.pdi_analyzer import PDIAnalyzer

def test_skill_classification():
    analyzer = PDIAnalyzer()
    
    test_cases = [
        "Aprender Python para desenvolvimento web",
        "Desenvolver habilidades de liderança",
        "Estudar Excel avançado e Power BI", 
        "Melhorar comunicação interpessoal",
        "Obter certificação AWS Solutions Architect",
        "Aprimorar inteligência emocional"
    ]
    
    print("=== TESTE DE CLASSIFICAÇÃO DE HABILIDADES ===\n")
    
    for i, objetivo in enumerate(test_cases, 1):
        print(f"Teste {i}: {objetivo}")
        
        result = analyzer.analyze_text(objetivo)
        
        if 'skill_classification' in result:
            skill_info = result['skill_classification']
            print(f"Tipo: {skill_info['skill_type']}")
            print(f"Confiança: {skill_info['confidence']:.2f}")
            print(f"Recomendação: {skill_info['recommendation']}")
        else:
            print("Classificação não encontrada")
        
        print("-" * 50)

if __name__ == "__main__":
    test_skill_classification()
