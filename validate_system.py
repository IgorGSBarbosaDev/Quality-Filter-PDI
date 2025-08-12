"""
Teste rápido do sistema reorganizado.
"""
from app import PDIAnalyzer

# Teste básico
print("🚀 Testando sistema reorganizado...")

try:
    analyzer = PDIAnalyzer()
    print("✅ PDIAnalyzer importado com sucesso!")
    
    # Teste de análise
    result = analyzer.analyze_text(
        objetivo="Desenvolver competências em Python",
        acoes="Completar curso de 40 horas até dezembro"
    )
    
    print(f"✅ Análise concluída!")
    print(f"   Score: {result['overall_score']:.2f}")
    print(f"   Nível: {result['quality_level']}")
    print(f"   Clareza: {result['clarity_score']:.2f}")
    print(f"   Especificidade: {result['specificity_score']:.2f}")
    
    print("\n🎉 Sistema funcionando perfeitamente!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
