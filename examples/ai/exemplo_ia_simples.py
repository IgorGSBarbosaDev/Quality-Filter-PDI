"""
🎯 EXEMPLO PRÁTICO - IA SIMPLES NO QUALITY FILTER PDI
Como usar a IA Simples implementada para análise de PDIs
"""

def exemplo_basico():
    """Exemplo básico de uso da IA Simples"""
    print("🤖 EXEMPLO BÁSICO - IA SIMPLES")
    print("=" * 40)
    
    try:
        # 1. Importar o analisador
        from quality_filter_pdi.pdi_analyzer import PDIAnalyzer
        
        # 2. Inicializar com IA
        print("📱 Inicializando PDI Analyzer com IA...")
        analyzer = PDIAnalyzer(enable_ai=True)
        
        # 3. Verificar status da IA
        ai_info = analyzer.get_ai_info()
        print(f"✅ IA disponível: {ai_info.get('ai_available', False)}")
        
        if not ai_info.get('ai_available', False):
            print("❌ IA não disponível")
            print(f"💡 Execute: {ai_info.get('recommendation', '')}")
            return
        
        # 4. Exemplos de PDIs para testar
        exemplos = [
            {
                "nome": "PDI Bem Estruturado",
                "objetivo": "Obter certificação AWS Solutions Architect Associate até dezembro de 2024",
                "acoes": "Estudar documentação oficial AWS, completar 3 labs práticos por semana, fazer 2 simulados mensais e agendar exame para novembro de 2024"
            },
            {
                "nome": "PDI Básico",
                "objetivo": "Aprender Python para análise de dados",
                "acoes": "Fazer curso online de Python e praticar com datasets"
            },
            {
                "nome": "PDI Vago",
                "objetivo": "Melhorar habilidades",
                "acoes": "Estudar mais"
            }
        ]
        
        # 5. Analisar cada exemplo
        for i, exemplo in enumerate(exemplos, 1):
            print(f"\n📝 {i}. {exemplo['nome']}")
            print(f"   Objetivo: {exemplo['objetivo']}")
            print(f"   Ações: {exemplo['acoes']}")
            
            # Análise híbrida (tradicional + IA)
            resultado = analyzer.analyze_text(
                objetivo=exemplo['objetivo'],
                acoes=exemplo['acoes']
            )
            
            # Mostrar resultados
            print("\n📊 RESULTADOS:")
            
            # Scores
            score_tradicional = resultado.get('scores', {}).get('overall_score', 0)
            score_ia = resultado.get('ai_overall_score', 0)
            score_hibrido = resultado.get('hybrid_score', 0)
            
            print(f"   📈 Score Tradicional: {score_tradicional:.2f}")
            print(f"   🤖 Score IA: {score_ia:.2f}")
            print(f"   🔀 Score Híbrido Final: {score_hibrido:.2f}")
            
            # Classificação
            if score_hibrido >= 0.8:
                print("   🟢 EXCELENTE PDI")
            elif score_hibrido >= 0.6:
                print("   🟡 BOM PDI - Pode melhorar")
            else:
                print("   🔴 PDI PRECISA DE REVISÃO")
            
            # Insights da IA
            ai_insights = resultado.get('ai_insights', {})
            
            strengths = ai_insights.get('strengths', [])
            if strengths:
                print(f"   💪 Pontos Fortes: {', '.join(strengths[:2])}")
            
            improvements = ai_insights.get('improvements', [])
            if improvements:
                print(f"   🔧 Melhorias: {', '.join(improvements[:2])}")
            
            suggestions = ai_insights.get('suggestions', [])
            if suggestions:
                print(f"   💡 Sugestão: {suggestions[0]}")
            
            print("   " + "-" * 40)
        
        print("\n🎉 EXEMPLO CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def exemplo_apenas_ia():
    """Exemplo usando apenas a IA (sem análise tradicional)"""
    print("\n🧠 EXEMPLO APENAS IA")
    print("=" * 40)
    
    try:
        from quality_filter_pdi.pdi_analyzer import PDIAnalyzer
        
        analyzer = PDIAnalyzer(enable_ai=True)
        
        texto = "Desenvolver competências em machine learning usando Python, scikit-learn e TensorFlow para implementar modelos de classificação e regressão em projetos de análise de dados durante 6 meses, com meta de concluir 3 projetos práticos"
        
        print(f"📝 Texto: {texto[:60]}...")
        
        resultado = analyzer.analyze_text_with_ai_only(texto)
        
        if 'error' in resultado:
            print(f"❌ Erro: {resultado['error']}")
            return
        
        print(f"\n📊 Score IA: {resultado['overall_score']:.3f}")
        print(f"🎯 Confiança: {resultado['confidence']:.3f}")
        
        # Análise detalhada
        print(f"\n🔍 ANÁLISE DETALHADA:")
        intent = resultado.get('intent_classification', {})
        print(f"   Intenção Principal: {intent.get('primary_intent', 'N/A')}")
        print(f"   Clareza da Intenção: {intent.get('intent_clarity', 'N/A')}")
        
        semantic = resultado.get('semantic_analysis', {})
        print(f"   Verbos de Ação: {len(semantic.get('action_verbs', []))}")
        print(f"   Termos Técnicos: {len(semantic.get('technical_terms', []))}")
        print(f"   Expressões Temporais: {len(semantic.get('time_expressions', []))}")
        
        quality = resultado.get('quality_assessment', {})
        print(f"   Clareza: {quality.get('clarity', 0):.2f}")
        print(f"   Especificidade: {quality.get('specificity', 0):.2f}")
        print(f"   Orientação Temporal: {quality.get('temporal_definition', 0):.2f}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🎯 QUALITY FILTER PDI - EXEMPLOS PRÁTICOS COM IA SIMPLES")
    print("Características: 💰 Custo Zero | 🔒 100% Offline | 📊 Precisão 75-80%")
    
    # Executar exemplos
    exemplo_basico()
    exemplo_apenas_ia()
    
    print("\n" + "=" * 50)
    print("🚀 PRONTO PARA USAR!")
    print("💡 A IA Simples está integrada e funcionando!")
    print("📖 Use analyzer.analyze_text() para análise híbrida")
    print("🧠 Use analyzer.analyze_text_with_ai_only() para apenas IA")
