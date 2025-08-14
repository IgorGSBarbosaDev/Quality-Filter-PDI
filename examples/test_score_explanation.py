import pandas as pd
import sys
import os

# Adicionar o caminho do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quality_filter_pdi import PDIAnalysisService, FileService

def test_score_explanation():
    """
    Testa a nova funcionalidade de explicação detalhada das notas
    """
    print("🧪 TESTANDO EXPLICAÇÃO DETALHADA DAS NOTAS")
    print("=" * 60)
    
    # Dados de exemplo com diferentes qualidades
    test_data = [
        {
            'objetivo': 'Aprender Python avançado até dezembro de 2025 para desenvolvimento de sistemas automatizados',
            'acoes': 'Fazer curso online de 40 horas, praticar 2 horas por semana, desenvolver 3 projetos práticos'
        },
        {
            'objetivo': 'Melhorar comunicação',
            'acoes': 'Falar melhor'
        },
        {
            'objetivo': 'Obter certificação AWS Solutions Architect Associate até junho de 2025 com nota mínima de 720 pontos',
            'acoes': 'Estudar documentação oficial 10 horas/semana, fazer 3 simulados, curso preparatório de 60 horas'
        }
    ]
    
    # Criar DataFrame
    df = pd.DataFrame(test_data)
    
    # Instanciar serviço
    analyzer = PDIAnalysisService()
    
    print("\n📊 ANÁLISES INDIVIDUAIS COM EXPLICAÇÃO DETALHADA:")
    print("-" * 60)
    
    for i, row in df.iterrows():
        print(f"\n🎯 PDI {i+1}:")
        print(f"Objetivo: {row['objetivo']}")
        print(f"Ações: {row['acoes']}")
        
        # Analisar PDI individual
        result = analyzer.analyze_single_pdi(row.to_dict())
        
        # Gerar explicação detalhada
        explanation = analyzer.quality_service.generate_score_explanation(
            result['clarity_score'],
            result['specificity_score'], 
            result['completeness_score'],
            result['structure_score'],
            result['smart_criteria_score'],
            result.get('analysis_metadata', {}).get('negative_impact', 0.0)
        )
        
        print(explanation)
        print("\n" + "="*60)
    
    # Analisar DataFrame completo
    print("\n📈 ANÁLISE COMPLETA DO LOTE:")
    results = analyzer.analyze_dataframe(df)
    
    if results['success']:
        print(f"\n✅ {results['total_analyzed']} PDIs analisados com sucesso!")
        
        # Salvar resultados
        output_file = "output/test_score_explanation.csv"
        os.makedirs("output", exist_ok=True)
        
        file_service = FileService()
        success, message = file_service.save_results(
            results['detailed_results'], 
            output_file,
            results.get('summary', {})
        )
        
        if success:
            print(f"📄 Resultados salvos em: {message}")
            print(f"🔍 Verifique a coluna 'score_explanation' no arquivo CSV")
        else:
            print(f"❌ Erro ao salvar: {message}")
    else:
        print(f"❌ Erro na análise: {results.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    test_score_explanation()
