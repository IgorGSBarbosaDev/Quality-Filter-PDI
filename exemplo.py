"""
Exemplo de uso do sistema de análise de PDI
"""
import pandas as pd
import os
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdi_analyzer import PDIAnalyzer

def create_sample_data():
    """
    Cria dados de exemplo para demonstrar o sistema
    """
    data = {
        'Nome': [
            'João Silva',
            'Maria Santos',
            'Carlos Oliveira',
            'Ana Costa',
            'Pedro Rodrigues'
        ],
        'Matrícula': [
            'EMP001',
            'EMP002',
            'EMP003',
            'EMP004',
            'EMP005'
        ],
        'Finalidade do objetivo': [
            'Posição atual',
            'Desenvolvimento futuro',
            'Posição atual',
            'Desenvolvimento futuro',
            'Posição atual'
        ],
        'Ações planejadas': [
            # Exemplo de alta qualidade
            'Realizar curso de Excel avançado com duração de 40 horas até dezembro de 2024. '
            'Praticar relatórios gerenciais semanalmente. Aplicar conhecimentos em projetos '
            'reais do departamento financeiro durante os próximos 6 meses.',
            
            # Exemplo de qualidade média
            'Fazer cursos de liderança e participar de reuniões da equipe. '
            'Tentar aplicar técnicas de gestão no dia a dia.',
            
            # Exemplo de baixa qualidade
            'Melhorar habilidades.',
            
            # Exemplo de alta qualidade
            'Participar do programa de mentoria executiva por 12 meses. '
            'Conduzir pelo menos 3 projetos estratégicos como líder. '
            'Concluir MBA em gestão até junho de 2025. Desenvolver plano '
            'sucessório para 2 colaboradores diretos.',
            
            # Exemplo de qualidade média
            'Estudar sobre gestão de projetos e maybe fazer certificação PMP. '
            'Acho que seria bom liderar algum projeto pequeno.'
        ],
        'Objetivo de desenvolvimento': [
            # Exemplo de alta qualidade
            'Tornar-me especialista em análise financeira avançada, '
            'dominando ferramentas de modelagem e sendo capaz de '
            'apresentar insights estratégicos para a diretoria até o final de 2024.',
            
            # Exemplo de qualidade média
            'Desenvolver habilidades de liderança para gerenciar equipes.',
            
            # Exemplo de baixa qualidade
            'Crescer profissionalmente.',
            
            # Exemplo de alta qualidade
            'Alcançar posição de Diretor Regional em 24 meses, '
            'responsável por pelo menos 50 funcionários e receita de '
            'R$ 10 milhões anuais, demonstrando competências em '
            'gestão estratégica e desenvolvimento de pessoas.',
            
            # Exemplo de qualidade média
            'Conseguir promoção para gerente de projetos e liderar '
            'projetos importantes na empresa.'
        ]
    }
    
    return pd.DataFrame(data)

def main():
    """
    Executa exemplo de análise
    """
    print("Exemplo de Análise de Qualidade de PDI")
    print("======================================\n")
    
    # Cria dados de exemplo
    df = create_sample_data()
    print("Dados de exemplo criados:")
    print(df[['Nome', 'Ações planejadas', 'Objetivo de desenvolvimento']].to_string())
    print("\n")
    
    # Inicializa analisador
    analyzer = PDIAnalyzer()
    
    # Analisa dados
    print("Realizando análise...")
    result_df = analyzer.analyze_dataframe(df)
    
    # Exibe resultados
    print("\nResultados da análise:")
    print("="*80)
    
    for idx, row in result_df.iterrows():
        print(f"\nFuncionário: {row['Nome']}")
        print(f"Nível de Qualidade: {row['quality_level']}")
        print(f"Pontuação: {row['quality_score']}")
        print(f"Sugestões: {row['suggestions']}")
        print("-" * 40)
    
    # Gera relatório resumido
    summary = analyzer.generate_summary_report(result_df)
    
    print("\nRelatório Resumido:")
    print("="*50)
    print(f"Total de PDIs: {summary['total_pdis']}")
    print(f"Pontuação média: {summary['average_score']}")
    print(f"Distribuição: {summary['quality_distribution']}")
    
    # Salva resultados
    output_dir = os.path.join(os.path.dirname(__file__), 'data', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'exemplo_analise_pdi.xlsx')
    result_df.to_excel(output_path, index=False)
    print(f"\nResultados salvos em: {output_path}")

if __name__ == "__main__":
    main()
