"""
Script principal para análise de qualidade de PDI
"""
import os
import sys
import pandas as pd
from datetime import datetime
import json

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdi_analyzer import PDIAnalyzer
from config.settings import EXCEL_COLUMNS

def load_excel_file(file_path: str) -> pd.DataFrame:
    """
    Carrega arquivo Excel e verifica se as colunas necessárias existem
    """
    try:
        df = pd.read_excel(file_path)
        print(f"Arquivo carregado com sucesso: {len(df)} registros encontrados")
        
        # Verifica se as colunas necessárias existem
        required_columns = [
            EXCEL_COLUMNS['acoes_planejadas'],
            EXCEL_COLUMNS['objetivo_desenvolvimento']
        ]
        
        missing_columns = []
        for col in required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"AVISO: Colunas não encontradas: {missing_columns}")
            print(f"Colunas disponíveis: {list(df.columns)}")
            
            # Tenta encontrar colunas similares
            print("\nTentando encontrar colunas similares...")
            for missing_col in missing_columns:
                similar_cols = [col for col in df.columns if missing_col.lower() in col.lower()]
                if similar_cols:
                    print(f"Possíveis correspondências para '{missing_col}': {similar_cols}")
        
        return df
        
    except Exception as e:
        raise Exception(f"Erro ao carregar arquivo: {str(e)}")

def save_results(df: pd.DataFrame, input_file_path: str, output_dir: str):
    """
    Salva os resultados em arquivo Excel
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_filename = os.path.splitext(os.path.basename(input_file_path))[0]
    output_filename = f"{input_filename}_analise_qualidade_{timestamp}.xlsx"
    output_path = os.path.join(output_dir, output_filename)
    
    # Salva o DataFrame com resultados
    df.to_excel(output_path, index=False)
    print(f"Resultados salvos em: {output_path}")
    
    return output_path

def save_summary_report(summary: dict, output_dir: str, input_filename: str):
    """
    Salva relatório resumido em JSON
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filename = f"{input_filename}_relatorio_resumo_{timestamp}.json"
    summary_path = os.path.join(output_dir, summary_filename)
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Relatório resumido salvo em: {summary_path}")
    return summary_path

def print_summary_report(summary: dict):
    """
    Exibe relatório resumido no console
    """
    print("\n" + "="*60)
    print("RELATÓRIO DE ANÁLISE DE QUALIDADE PDI")
    print("="*60)
    
    print(f"Total de PDIs analisados: {summary['total_pdis']}")
    print(f"Pontuação média de qualidade: {summary['average_score']}")
    
    print("\nDistribuição por nível de qualidade:")
    for level, count in summary['quality_distribution'].items():
        percentage = summary['quality_percentage'][level.lower()] if level.lower() in summary['quality_percentage'] else 0
        print(f"  {level}: {count} PDIs ({percentage:.1f}%)")
    
    print("\nMétricas médias:")
    for metric, value in summary['average_metrics'].items():
        print(f"  {metric.title()}: {value}")
    
    if summary['main_improvement_areas']:
        print(f"\nPrincipais áreas para melhoria: {', '.join(summary['main_improvement_areas'])}")
    
    print("="*60 + "\n")

def main():
    """
    Função principal
    """
    print("Sistema de Análise de Qualidade de PDI")
    print("=====================================\n")
    
    # Diretórios
    input_dir = os.path.join(os.path.dirname(__file__), 'data', 'input')
    output_dir = os.path.join(os.path.dirname(__file__), 'data', 'output')
    
    # Cria diretórios se não existirem
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Verifica se há arquivos na pasta input
    excel_files = [f for f in os.listdir(input_dir) if f.endswith(('.xlsx', '.xls'))]
    
    if not excel_files:
        print(f"Nenhum arquivo Excel encontrado em: {input_dir}")
        print("Por favor, coloque sua planilha na pasta 'data/input/'")
        return
    
    if len(excel_files) == 1:
        selected_file = excel_files[0]
        print(f"Arquivo encontrado: {selected_file}")
    else:
        print("Múltiplos arquivos encontrados:")
        for i, file in enumerate(excel_files, 1):
            print(f"{i}. {file}")
        
        try:
            choice = int(input("Selecione o arquivo (número): ")) - 1
            selected_file = excel_files[choice]
        except (ValueError, IndexError):
            print("Seleção inválida. Usando o primeiro arquivo.")
            selected_file = excel_files[0]
    
    input_path = os.path.join(input_dir, selected_file)
    
    try:
        # Carrega dados
        print(f"\nCarregando arquivo: {selected_file}")
        df = load_excel_file(input_path)
        
        # Inicializa analisador
        print("Inicializando analisador...")
        analyzer = PDIAnalyzer()
        
        # Realiza análise
        print("Realizando análise de qualidade...")
        result_df = analyzer.analyze_dataframe(df)
        
        # Gera relatório resumido
        print("Gerando relatório resumido...")
        summary = analyzer.generate_summary_report(result_df)
        
        # Salva resultados
        print("Salvando resultados...")
        output_path = save_results(result_df, input_path, output_dir)
        
        # Salva relatório resumido
        input_filename = os.path.splitext(selected_file)[0]
        summary_path = save_summary_report(summary, output_dir, input_filename)
        
        # Exibe relatório resumido
        print_summary_report(summary)
        
        print("Análise concluída com sucesso!")
        print(f"Resultados disponíveis em: {output_dir}")
        
    except Exception as e:
        print(f"Erro durante a análise: {str(e)}")
        return

if __name__ == "__main__":
    main()
