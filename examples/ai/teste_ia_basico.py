"""
🧪 TESTE SIMPLES DA IA
Teste básico para verificar se a IA Simples está funcionando
"""

# Teste de importações
try:
    print("🔄 Testando importações...")
    
    # Importar bibliotecas básicas
    import spacy
    print("✅ spaCy importado")
    
    import nltk
    print("✅ NLTK importado")
    
    import sklearn
    print("✅ scikit-learn importado")
    
    # Tentar carregar modelo spaCy
    try:
        nlp = spacy.load("pt_core_news_sm")
        print("✅ Modelo spaCy português carregado")
    except:
        print("⚠️ Modelo spaCy não encontrado - baixando...")
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "pt_core_news_sm"])
        nlp = spacy.load("pt_core_news_sm")
        print("✅ Modelo spaCy baixado e carregado")
    
    # Teste básico do modelo
    doc = nlp("Aprender Python para análise de dados durante 3 meses")
    print(f"✅ Teste básico: {len(doc)} tokens processados")
    
    # Importar nosso analisador
    from quality_filter_pdi.ai.simple_ai_analyzer import SimpleAIAnalyzer
    print("✅ SimpleAIAnalyzer importado")
    
    # Inicializar analisador
    analyzer = SimpleAIAnalyzer()
    print("✅ SimpleAIAnalyzer inicializado")
    
    # Teste básico
    texto = "Desenvolver habilidades em Python para análise de dados usando pandas durante 3 meses"
    resultado = analyzer.analyze_pdi_text(texto)
    
    print(f"\n🎯 RESULTADO DO TESTE:")
    print(f"Score geral: {resultado['overall_score']:.3f}")
    print(f"Confiança: {resultado['confidence']:.3f}")
    print(f"Pontos fortes: {len(resultado['ai_insights']['strengths'])}")
    print(f"Melhorias: {len(resultado['ai_insights']['improvements'])}")
    
    print("\n🎉 IA SIMPLES FUNCIONANDO PERFEITAMENTE!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
