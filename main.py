import os
import sys
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdi_analyzer import PDIAnalyzer
from config.settings import EXCEL_COLUMNS


class PDIAnalysisRunner:
    def __init__(self) -> None:
        self.input_dir = Path(__file__).parent / 'data' / 'input'
        self.output_dir = Path(__file__).parent / 'data' / 'output'
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_analysis(self) -> None:
        print("Sistema de Análise de Qualidade de PDI")
        print("=====================================\n")
        
        excel_file = self._select_input_file()
        if not excel_file:
            return
        
        try:
            df = self._load_excel_file(excel_file)
            analyzer = PDIAnalyzer()
            
            print("Realizando análise de qualidade...")
            result_df = analyzer.analyze_dataframe(df)
            
            print("Gerando relatório resumido...")
            summary = analyzer.generate_summary_report(result_df)
            
            print("Salvando resultados...")
            self._save_results(result_df, excel_file, summary)
            
            self._print_summary_report(summary)
            
            print("Análise concluída com sucesso!")
            print(f"Resultados disponíveis em: {self.output_dir}")
            
        except Exception as e:
            print(f"Erro durante a análise: {str(e)}")
    
    def _select_input_file(self) -> Optional[Path]:
        excel_files = list(self.input_dir.glob('*.xlsx')) + list(self.input_dir.glob('*.xls'))
        
        if not excel_files:
            print(f"Nenhum arquivo Excel encontrado em: {self.input_dir}")
            print("Por favor, coloque sua planilha na pasta 'data/input/'")
            return None
        
        if len(excel_files) == 1:
            selected_file = excel_files[0]
            print(f"Arquivo encontrado: {selected_file.name}")
            return selected_file
        
        return self._choose_from_multiple_files(excel_files)
    
    def _choose_from_multiple_files(self, excel_files: List[Path]) -> Path:
        print("Múltiplos arquivos encontrados:")
        for i, file in enumerate(excel_files, 1):
            print(f"{i}. {file.name}")
        
        try:
            choice = int(input("Selecione o arquivo (número): ")) - 1
            return excel_files[choice]
        except (ValueError, IndexError):
            print("Seleção inválida. Usando o primeiro arquivo.")
            return excel_files[0]
    
    def _load_excel_file(self, file_path: Path) -> pd.DataFrame:
        print(f"\nCarregando arquivo: {file_path.name}")
        
        df = pd.read_excel(file_path)
        print(f"Arquivo carregado com sucesso: {len(df)} registros encontrados")
        
        self._validate_columns(df)
        return df
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        required_columns = [
            EXCEL_COLUMNS['acoes_planejadas'],
            EXCEL_COLUMNS['objetivo_desenvolvimento']
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"AVISO: Colunas não encontradas: {missing_columns}")
            print(f"Colunas disponíveis: {list(df.columns)}")
            self._suggest_similar_columns(df.columns, missing_columns)
    
    def _suggest_similar_columns(self, available_columns: List[str], missing_columns: List[str]) -> None:
        print("\nTentando encontrar colunas similares...")
        for missing_col in missing_columns:
            similar_cols = [
                col for col in available_columns 
                if missing_col.lower() in col.lower()
            ]
            if similar_cols:
                print(f"Possíveis correspondências para '{missing_col}': {similar_cols}")
    
    def _save_results(self, df: pd.DataFrame, input_file: Path, summary: dict) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = input_file.stem
        
        output_path = self.output_dir / f"{base_filename}_analise_qualidade_{timestamp}.xlsx"
        df.to_excel(output_path, index=False)
        print(f"Resultados salvos em: {output_path}")
        
        summary_path = self.output_dir / f"{base_filename}_relatorio_resumo_{timestamp}.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"Relatório resumido salvo em: {summary_path}")
    
    def _print_summary_report(self, summary: dict) -> None:
        print("\n" + "="*60)
        print("RELATÓRIO DE ANÁLISE DE QUALIDADE PDI")
        print("="*60)
        
        print(f"Total de PDIs analisados: {summary['total_pdis']}")
        print(f"Pontuação média de qualidade: {summary['average_score']}")
        
        print("\nDistribuição por nível de qualidade:")
        for level, count in summary['quality_distribution'].items():
            percentage = summary['quality_percentage'].get(level.lower(), 0)
            print(f"  {level}: {count} PDIs ({percentage:.1f}%)")
        
        print("\nMétricas médias:")
        for metric, value in summary['average_metrics'].items():
            print(f"  {metric.title()}: {value}")
        
        if summary['main_improvement_areas']:
            areas = ', '.join(summary['main_improvement_areas'])
            print(f"\nPrincipais áreas para melhoria: {areas}")
        
        print("="*60 + "\n")


def main() -> None:
    runner = PDIAnalysisRunner()
    runner.run_analysis()


if __name__ == "__main__":
    main()
