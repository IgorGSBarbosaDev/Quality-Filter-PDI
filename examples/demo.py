"""
Script para demonstração do sistema de análise PDI.
"""
import sys
from pathlib import Path

# Adiciona o diretório da aplicação ao path
sys.path.append(str(Path(__file__).parent.parent))

from app import PDIAnalyzer
import pandas as pd


def demo_text_analysis():
    """Demonstra análise de texto."""
    print("=== DEMONSTRAÇÃO: ANÁLISE DE TEXTO ===\n")
    
    analyzer = PDIAnalyzer()
    
    # Exemplos de PDIs com diferentes níveis de qualidade
    examples = [
        {
            "nome": "PDI Alta Qualidade",
            "objetivo": "Desenvolver competências avançadas em gestão de projetos ágeis com foco em Scrum e Kanban",
            "acoes": "Completar certificação PSM I até março de 2024, aplicar metodologia em 3 projetos piloto e liderar equipe de 5 pessoas"
        },
        {
            "nome": "PDI Média Qualidade", 
            "objetivo": "Melhorar habilidades de liderança e comunicação",
            "acoes": "Fazer curso de liderança e praticar apresentações"
        },
        {
            "nome": "PDI Baixa Qualidade",
            "objetivo": "Crescer profissionalmente",
            "acoes": "Estudar mais"
        }
    ]
    
    for example in examples:
        print(f"📋 {example['nome']}")
        print(f"Objetivo: {example['objetivo']}")
        print(f"Ações: {example['acoes']}")
        
        result = analyzer.analyze_text(example['objetivo'], example['acoes'])
        
        print(f"📊 Resultado:")
        print(f"   Score Geral: {result['overall_score']:.2f}")
        print(f"   Nível: {result['quality_level']}")
        print(f"   Clareza: {result['clarity_score']:.2f}")
        print(f"   Especificidade: {result['specificity_score']:.2f}")
        print(f"   Completude: {result['completeness_score']:.2f}")
        print("-" * 60)


def demo_csv_analysis():
    """Demonstra análise de arquivo CSV."""
    print("\n=== DEMONSTRAÇÃO: ANÁLISE DE ARQUIVO CSV ===\n")
    
    # Procura por arquivos CSV no diretório examples
    csv_files = list(Path("examples").glob("*.csv"))
    
    if csv_files:
        csv_file = csv_files[0]
        print(f"📁 Analisando arquivo: {csv_file.name}")
        
        analyzer = PDIAnalyzer()
        try:
            result = analyzer.analyze_file(str(csv_file))
            
            if result['success']:
                print(f"✅ Análise concluída com sucesso!")
                print(f"📊 Total de PDIs analisados: {result['total_analyzed']}")
                print(f"   Alta qualidade: {result['summary']['Alta']}")
                print(f"   Média qualidade: {result['summary']['Média']}")
                print(f"   Baixa qualidade: {result['summary']['Baixa']}")
                
                # Mostra alguns exemplos
                df = result['detailed_results']
                print(f"\n📋 Primeiros 3 resultados:")
                for idx, row in df.head(3).iterrows():
                    print(f"   PDI {idx+1}: {row['quality_level']} ({row['overall_score']:.2f})")
            else:
                print(f"❌ Erro na análise: {result['error']}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    else:
        print("📁 Nenhum arquivo CSV encontrado no diretório examples/")
        print("   Criando exemplo para demonstração...")
        
        # Cria exemplo de CSV
        sample_data = {
            'objetivo': [
                'Desenvolver competências em análise de dados com Python e SQL',
                'Melhorar comunicação',
                'Liderar projetos de transformação digital até 2024'
            ],
            'acoes': [
                'Completar curso de 60h em Data Science, aplicar em 2 projetos reais',
                'Fazer apresentações',
                'Gerenciar 3 projetos piloto e capacitar equipe de 10 pessoas'
            ]
        }
        
        example_path = Path("examples/exemplo_pdi.csv")
        example_path.parent.mkdir(exist_ok=True)
        
        df = pd.DataFrame(sample_data)
        df.to_csv(example_path, index=False, encoding='utf-8')
        
        print(f"✅ Arquivo exemplo criado: {example_path}")
        
        # Analisa o exemplo criado
        analyzer = PDIAnalyzer()
        result = analyzer.analyze_file(str(example_path))
        
        if result['success']:
            print(f"\n📊 Resultados da análise:")
            print(f"   Total: {result['total_analyzed']}")
            print(f"   Alta: {result['summary']['Alta']}")
            print(f"   Média: {result['summary']['Média']}")
            print(f"   Baixa: {result['summary']['Baixa']}")


def main():
    """Função principal da demonstração."""
    print("🚀 SISTEMA DE ANÁLISE DE QUALIDADE PDI")
    print("=====================================")
    
    try:
        # Demonstra análise de texto
        demo_text_analysis()
        
        # Demonstra análise de CSV
        demo_csv_analysis()
        
        print("\n✅ Demonstração concluída com sucesso!")
        print("\n📚 Para usar o sistema:")
        print("   1. Para análise de texto: analyzer.analyze_text(objetivo, acoes)")
        print("   2. Para análise de arquivo: analyzer.analyze_file(caminho_arquivo)")
        
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
