"""
Serviço de manipulação de arquivos.
Gerencia carregamento, salvamento e processamento de arquivos CSV e Excel.
"""
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional, List
import json
from datetime import datetime

from ..core.config import SUPPORTED_ENCODINGS, OUTPUT_ENCODING


class FileService:
    """Serviço para manipulação de arquivos de dados."""
    
    @staticmethod
    def load_csv(file_path: str) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Carrega arquivo CSV com detecção automática de encoding.
        
        Args:
            file_path: Caminho para o arquivo CSV
            
        Returns:
            Tupla com DataFrame (ou None se erro) e encoding usado
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        # Tenta diferentes encodings
        for encoding in SUPPORTED_ENCODINGS:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"✅ Arquivo carregado com encoding: {encoding}")
                return df, encoding
                
            except Exception as e:
                print(f"❌ Falha com encoding {encoding}: {str(e)}")
                continue
        
        raise ValueError("Não foi possível carregar o arquivo com nenhum encoding suportado")
    
    @staticmethod
    def load_excel(file_path: str) -> pd.DataFrame:
        """
        Carrega arquivo Excel.
        
        Args:
            file_path: Caminho para o arquivo Excel
            
        Returns:
            DataFrame com os dados
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        try:
            df = pd.read_excel(file_path)
            print(f"✅ Arquivo Excel carregado: {file_path.name}")
            return df
            
        except Exception as e:
            raise ValueError(f"Erro ao carregar arquivo Excel: {str(e)}")
    
    @staticmethod
    def save_results(
        df: pd.DataFrame, 
        summary: dict, 
        output_dir: str = "output",
        base_name: str = "analise_pdi"
    ) -> Tuple[str, str]:
        """
        Salva resultados da análise em CSV e JSON.
        
        Args:
            df: DataFrame com resultados
            summary: Resumo da análise
            output_dir: Diretório de saída
            base_name: Nome base dos arquivos
            
        Returns:
            Tupla com caminhos dos arquivos salvos (CSV, JSON)
        """
        # Cria diretório se não existir
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Gera timestamp para nomes únicos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salva CSV
        csv_path = output_path / f"{base_name}_{timestamp}.csv"
        df.to_csv(csv_path, index=False, encoding=OUTPUT_ENCODING)
        
        # Salva resumo JSON
        json_path = output_path / f"{base_name}_resumo_{timestamp}.json"
        with open(json_path, 'w', encoding=OUTPUT_ENCODING) as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Resultados salvos: {csv_path}")
        print(f"📋 Resumo salvo: {json_path}")
        
        return str(csv_path), str(json_path)
    
    @staticmethod
    def detect_file_type(file_path: str) -> str:
        """
        Detecta o tipo de arquivo baseado na extensão.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Tipo do arquivo ('csv', 'excel' ou 'unknown')
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.csv':
            return 'csv'
        elif extension in ['.xlsx', '.xls']:
            return 'excel'
        else:
            return 'unknown'
    
    @staticmethod
    def find_data_files(directory: str) -> List[str]:
        """
        Encontra arquivos de dados em um diretório.
        
        Args:
            directory: Diretório para busca
            
        Returns:
            Lista de caminhos de arquivos encontrados
        """
        directory = Path(directory)
        
        if not directory.exists():
            return []
        
        data_files = []
        
        # Busca arquivos CSV
        for csv_file in directory.glob("*.csv"):
            data_files.append(str(csv_file))
        
        # Busca arquivos Excel
        for excel_file in directory.glob("*.xlsx"):
            data_files.append(str(excel_file))
        
        for excel_file in directory.glob("*.xls"):
            data_files.append(str(excel_file))
        
        return sorted(data_files)
    
    @staticmethod
    def validate_data_structure(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, List[str]]:
        """
        Valida se o DataFrame possui as colunas necessárias.
        
        Args:
            df: DataFrame para validação
            required_columns: Lista de colunas obrigatórias
            
        Returns:
            Tupla com (válido, colunas_faltantes)
        """
        missing_columns = []
        
        for col in required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        is_valid = len(missing_columns) == 0
        return is_valid, missing_columns
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        Obtém informações sobre um arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Dicionário com informações do arquivo
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'exists': False}
        
        stat = file_path.stat()
        
        return {
            'exists': True,
            'name': file_path.name,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'type': FileService.detect_file_type(str(file_path))
        }
