import pandas as pd
import os
import sys
from pathlib import Path
from typing import Dict, Any

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdi_analyzer import PDIAnalyzer


class PDIExampleGenerator:
    def __init__(self) -> None:
        self.output_dir = Path(__file__).parent / 'data' / 'output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_sample_data(self) -> pd.DataFrame:
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
                'Realizar curso de Excel avançado com duração de 40 horas até dezembro de 2024. '
                'Praticar relatórios gerenciais semanalmente. Aplicar conhecimentos em projetos '
                'reais do departamento financeiro durante os próximos 6 meses.',
                
                'Fazer cursos de liderança e participar de reuniões da equipe. '
                'Tentar aplicar técnicas de gestão no dia a dia.',
                
                'Melhorar habilidades.',
                
                'Participar do programa de mentoria executiva por 12 meses. '
                'Conduzir pelo menos 3 projetos estratégicos como líder. '
                'Concluir MBA em gestão até junho de 2025. Desenvolver plano '
                'sucessório para 2 colaboradores diretos.',
                
                'Estudar sobre gestão de projetos e maybe fazer certificação PMP. '
                'Acho que seria bom liderar algum projeto pequeno.'
            ],
            'Objetivo de desenvolvimento': [
                'Tornar-me especialista em análise financeira avançada, '
                'dominando ferramentas de modelagem e sendo capaz de '
                'apresentar insights estratégicos para a diretoria até o final de 2024.',
                
                'Desenvolver habilidades de liderança para gerenciar equipes.',
                
                'Crescer profissionalmente.',
                
                'Alcançar posição de Diretor Regional em 24 meses, '
                'responsável por pelo menos 50 funcionários e receita de '
                'R$ 10 milhões anuais, demonstrando competências em '
                'gestão estratégica e desenvolvimento de pessoas.',
                
                'Conseguir promoção para gerente de projetos e liderar '
                'projetos importantes na empresa.'
            ]
        }
        
        return pd.DataFrame(data)
    
    def run_example_analysis(self) -> None:
        print("Exemplo de Análise de Qualidade de PDI")
        print("======================================\n")
        
        df = self.create_sample_data()
        self._display_sample_data(df)
        
        analyzer = PDIAnalyzer()
        
        print("Realizando análise...")
        result_df = analyzer.analyze_dataframe(df)
        
        self._display_results(result_df)
        self._display_summary(analyzer.generate_summary_report(result_df))
        self._save_results(result_df)
    
    def _display_sample_data(self, df: pd.DataFrame) -> None:
        print("Dados de exemplo criados:")
        columns_to_show = ['Nome', 'Ações planejadas', 'Objetivo de desenvolvimento']
        print(df[columns_to_show].to_string())
        print("\n")
    
    def _display_results(self, result_df: pd.DataFrame) -> None:
        print("\nResultados da análise:")
        print("="*80)
        
        for idx, row in result_df.iterrows():
            print(f"\nFuncionário: {row['Nome']}")
            print(f"Nível de Qualidade: {row['quality_level']}")
            print(f"Pontuação: {row['quality_score']}")
            print(f"Sugestões: {row['suggestions']}")
            print("-" * 40)
    
    def _display_summary(self, summary: Dict[str, Any]) -> None:
        print("\nRelatório Resumido:")
        print("="*50)
        print(f"Total de PDIs: {summary['total_pdis']}")
        print(f"Pontuação média: {summary['average_score']}")
        print(f"Distribuição: {summary['quality_distribution']}")
    
    def _save_results(self, result_df: pd.DataFrame) -> None:
        output_path = self.output_dir / 'exemplo_analise_pdi.xlsx'
        result_df.to_excel(output_path, index=False)
        print(f"\nResultados salvos em: {output_path}")


def main() -> None:
    generator = PDIExampleGenerator()
    generator.run_example_analysis()


if __name__ == "__main__":
    main()
