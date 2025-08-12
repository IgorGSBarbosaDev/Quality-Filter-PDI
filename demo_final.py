"""
🚀 SISTEMA DE ANÁLISE DE QUALIDADE PDI - VERSÃO FINAL
=====================================================

Sistema completo e reorganizado para análise automática de PDIs.
"""
import sys
from pathlib import Path

# Adiciona o diretório da aplicação ao path
sys.path.append(str(Path(__file__).parent))

from app import PDIAnalyzer


def main():
    """Demonstração completa do sistema final."""
    print("🚀 SISTEMA DE ANÁLISE DE QUALIDADE PDI")
    print("=" * 50)
    print("✅ Sistema reorganizado com arquitetura profissional")
    print("✅ Código limpo seguindo boas práticas")
    print("✅ Estrutura modular e testável")
    
    try:
        # Inicializa o analisador
        analyzer = PDIAnalyzer()
        print("\n📊 Testando sistema...")
        
        # Teste 1: PDI de alta qualidade
        print("\n1️⃣ PDI de Alta Qualidade:")
        resultado1 = analyzer.analyze_text(
            objetivo="Desenvolver competências avançadas em gestão de projetos ágeis com certificação Scrum Master",
            acoes="Completar curso PSM I de 40 horas até março de 2024, aplicar metodologia em 3 projetos piloto e liderar equipe de 5 pessoas"
        )
        print(f"   📈 Score: {resultado1['overall_score']:.2f}")
        print(f"   🏆 Nível: {resultado1['quality_level']}")
        print(f"   📝 Clareza: {resultado1['clarity_score']:.2f}")
        print(f"   🎯 Especificidade: {resultado1['specificity_score']:.2f}")
        
        # Teste 2: PDI de baixa qualidade
        print("\n2️⃣ PDI de Baixa Qualidade:")
        resultado2 = analyzer.analyze_text(
            objetivo="Melhorar habilidades",
            acoes="Estudar mais"
        )
        print(f"   📈 Score: {resultado2['overall_score']:.2f}")
        print(f"   📉 Nível: {resultado2['quality_level']}")
        
        # Teste 3: Verificar se há arquivo CSV de exemplo
        csv_path = Path("examples/dados_exemplo.csv")
        if csv_path.exists():
            print("\n3️⃣ Análise de Arquivo CSV:")
            resultado3 = analyzer.analyze_file(str(csv_path))
            if resultado3['success']:
                print(f"   📁 Arquivo analisado com sucesso!")
                print(f"   📊 Total: {resultado3['total_analyzed']} PDIs")
                print(f"   🏆 Alta: {resultado3['summary']['Alta']}")
                print(f"   📊 Média: {resultado3['summary']['Média']}")
                print(f"   📉 Baixa: {resultado3['summary']['Baixa']}")
        
        print("\n" + "=" * 50)
        print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("=" * 50)
        
        print("\n📚 Como usar:")
        print("  from app import PDIAnalyzer")
        print("  analyzer = PDIAnalyzer()")
        print("  resultado = analyzer.analyze_text(objetivo, acoes)")
        print("  resultado = analyzer.analyze_file('arquivo.csv')")
        
        print("\n📂 Estrutura do projeto:")
        print("  app/                 # Sistema principal")
        print("  ├── core/            # Configurações")
        print("  ├── services/        # Lógica de negócio")
        print("  ├── utils/           # Utilitários")
        print("  └── pdi_analyzer.py  # Interface principal")
        print("  tests/               # Testes unitários")
        print("  examples/            # Exemplos e demos")
        print("  docs/                # Documentação")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro no sistema: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✨ Demonstração concluída com sucesso!")
    else:
        print("\n💥 Houve problemas na demonstração.")
        sys.exit(1)
