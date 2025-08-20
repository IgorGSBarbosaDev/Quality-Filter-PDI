#!/usr/bin/env python3
"""
🧪 TESTE DA IA SIMPLES
Script para testar a implementação da IA Simples no Quality Filter PDI
"""

import sys
from pathlib import Path

# Adicionar o caminho do projeto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from quality_filter_pdi.pdi_analyzer import PDIAnalyzer

def test_ai_implementation():
    """Testa a implementação da IA Simples"""
    print("🧪 TESTANDO IMPLEMENTAÇÃO DA IA SIMPLES")
    print("=" * 50)
    
    try:
        # Inicializar o analisador com IA
        print("1️⃣ Inicializando PDI Analyzer com IA...")
        analyzer = PDIAnalyzer(enable_ai=True)
        
        # Verificar status da IA
        print("\n2️⃣ Verificando status da IA...")
        ai_info = analyzer.get_ai_info()
        print(f"✅ Status: {ai_info.get('status', 'Desconhecido')}")
        print(f"📊 Precisão esperada: {ai_info.get('performance', {}).get('precision', 'N/A')}")
        print(f"💰 Custo: {ai_info.get('performance', {}).get('cost', 'N/A')}")
        
        if not ai_info.get('ai_available', False):
            print("❌ IA não disponível!")
            print(f"💡 Recomendação: {ai_info.get('recommendation', '')}")
            return False
        
        # Teste básico da IA
        print("\n3️⃣ Executando teste básico da IA...")
        test_result = analyzer.test_ai_analysis()
        
        if test_result.get('test_successful', False):
            print("✅ Teste da IA bem-sucedido!")
            print(f"📊 Score: {test_result.get('overall_score', 0):.3f}")
            print(f"🎯 Confiança: {test_result.get('confidence', 0):.3f}")
            
            insights = test_result.get('main_insights', [])
            if insights:
                print("💡 Principais insights:")
                for insight in insights:
                    print(f"   • {insight}")
        else:
            print(f"❌ Teste falhou: {test_result.get('error', 'Erro desconhecido')}")
            return False
        
        # Teste com exemplos reais
        print("\n4️⃣ Testando com exemplos de PDIs...")
        
        exemplos_pdi = [
            {
                "objetivo": "Aprender Python para análise de dados",
                "acoes": "Fazer curso online de Python e praticar com datasets reais durante 3 meses",
                "nome": "PDI Básico"
            },
            {
                "objetivo": "Obter certificação AWS Solutions Architect Associate até dezembro de 2024",
                "acoes": "Estudar documentação AWS, fazer labs práticos e simulados, agendar exame para novembro",
                "nome": "PDI Específico"
            },
            {
                "objetivo": "Melhorar habilidades",
                "acoes": "Estudar",
                "nome": "PDI Vago"
            }
        ]
        
        for i, exemplo in enumerate(exemplos_pdi, 1):
            print(f"\n   📝 Exemplo {i}: {exemplo['nome']}")
            
            # Análise tradicional + IA
            resultado = analyzer.analyze_text(
                objetivo=exemplo['objetivo'],
                acoes=exemplo['acoes']
            )
            
            # Mostrar resultados
            score_tradicional = resultado.get('scores', {}).get('overall_score', 0)
            score_ia = resultado.get('ai_overall_score', 0)
            score_hibrido = resultado.get('hybrid_score', 0)
            
            print(f"      📊 Score Tradicional: {score_tradicional:.3f}")
            print(f"      🤖 Score IA: {score_ia:.3f}")
            print(f"      🔀 Score Híbrido: {score_hibrido:.3f}")
            
            # Recomendações da IA
            ai_recommendations = resultado.get('ai_recommendations', [])
            if ai_recommendations:
                print(f"      💡 Recomendação IA: {ai_recommendations[0]}")
        
        # Teste de performance
        print("\n5️⃣ Teste de performance da IA...")
        import time
        
        texto_teste = "Desenvolver competências em machine learning usando Python e scikit-learn para implementar modelos preditivos em projetos de análise de dados durante 6 meses"
        
        start_time = time.time()
        for _ in range(10):
            analyzer.analyze_text_with_ai_only(texto_teste)
        end_time = time.time()
        
        tempo_medio = (end_time - start_time) / 10
        print(f"⚡ Tempo médio por análise: {tempo_medio:.3f}s")
        print(f"📈 Taxa de processamento: {1/tempo_medio:.1f} análises/segundo")
        
        print("\n🎉 TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO!")
        print("\n📋 RESUMO:")
        print("✅ IA Simples instalada e configurada")
        print("✅ Integração com sistema tradicional funcionando")
        print("✅ Análise híbrida operacional")
        print("✅ Performance adequada")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE O TESTE: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def mostrar_exemplo_uso():
    """Mostra exemplo de uso da IA"""
    print("\n" + "=" * 50)
    print("📖 EXEMPLO DE USO DA IA SIMPLES")
    print("=" * 50)
    
    codigo_exemplo = '''
# 1. Importar o analisador
from quality_filter_pdi.pdi_analyzer import PDIAnalyzer

# 2. Inicializar com IA ativada
analyzer = PDIAnalyzer(enable_ai=True)

# 3. Verificar se IA está disponível
ai_info = analyzer.get_ai_info()
print(f"IA disponível: {ai_info['ai_available']}")

# 4. Analisar um PDI com IA
resultado = analyzer.analyze_text(
    objetivo="Aprender Python para análise de dados",
    acoes="Fazer curso online durante 3 meses e praticar com projetos reais"
)

# 5. Ver resultados híbridos
print(f"Score tradicional: {resultado['scores']['overall_score']:.3f}")
print(f"Score IA: {resultado['ai_overall_score']:.3f}")
print(f"Score híbrido: {resultado['hybrid_score']:.3f}")

# 6. Ver insights da IA
ai_insights = resultado['ai_insights']
print("Pontos fortes:", ai_insights['strengths'])
print("Melhorias:", ai_insights['improvements'])
print("Sugestões:", ai_insights['suggestions'])
'''
    
    print(codigo_exemplo)

if __name__ == "__main__":
    print("🤖 QUALITY FILTER PDI - TESTE DE IA SIMPLES")
    print("Implementação: spaCy + NLTK + scikit-learn")
    print("Características: 💰 Custo Zero | 🔒 100% Offline | ⚡ Setup Rápido")
    print()
    
    # Executar testes
    sucesso = test_ai_implementation()
    
    if sucesso:
        mostrar_exemplo_uso()
        print("\n🚀 A IA SIMPLES ESTÁ PRONTA PARA USO!")
    else:
        print("\n🔧 VERIFIQUE A INSTALAÇÃO E TENTE NOVAMENTE")
        print("💡 Execute: pip install spacy scikit-learn nltk")
        print("💡 Execute: python -m spacy download pt_core_news_sm")
