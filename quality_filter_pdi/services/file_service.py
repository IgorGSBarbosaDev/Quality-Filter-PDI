import pandas as pd
from pathlib import Path
from typing import Tuple, Optional, List
import json
from datetime import datetime

from ..core.config import SUPPORTED_ENCODINGS, OUTPUT_ENCODING


class FileService:
    
    @staticmethod
    def load_csv(file_path: str) -> Tuple[Optional[pd.DataFrame], str]:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
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
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        if file_path.suffix.lower() == '.xlsx':
            return pd.read_excel(file_path, engine='openpyxl')
        elif file_path.suffix.lower() == '.xls':
            return pd.read_excel(file_path, engine='xlrd')
        else:
            raise ValueError("Formato de arquivo Excel não suportado")
    
    @staticmethod
    def detect_columns(df: pd.DataFrame) -> Tuple[str, str]:
        df.columns = df.columns.str.strip()
        
        objective_patterns = [
            'objetivo', 'objetivos', 'meta', 'metas', 
            'objetivo de desenvolvimento', 'objetivo desenvolvimento',
            'gap', 'finalidade'
        ]
        
        action_patterns = [
            'acoes', 'ações', 'acao', 'ação', 'acoes planejadas', 
            'ações planejadas', 'plano', 'atividades', 'atividade',
            'ações a serem realizadas', 'acoes a serem realizadas'
        ]
        
        objective_col = None
        action_col = None
        
        for col in df.columns:
            col_lower = col.lower().strip()
            
            if not objective_col:
                for pattern in objective_patterns:
                    if pattern in col_lower:
                        objective_col = col
                        break
            
            if not action_col:
                for pattern in action_patterns:
                    if pattern in col_lower:
                        action_col = col
                        break
        
        if not objective_col or not action_col:
            available_cols = list(df.columns)
            raise ValueError(
                f"Não foi possível identificar colunas de objetivo e ações. "
                f"Colunas disponíveis: {available_cols}"
            )
        
        return objective_col, action_col
    
    @staticmethod
    def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        objective_col, action_col = FileService.detect_columns(df)
        
        df_normalized = df.copy()
        
        if objective_col != 'objetivo':
            df_normalized['objetivo'] = df_normalized[objective_col]
        
        if action_col != 'acoes':
            df_normalized['acoes'] = df_normalized[action_col]
        
        df_normalized['objetivo'] = df_normalized['objetivo'].fillna('')
        df_normalized['acoes'] = df_normalized['acoes'].fillna('')
        
        df_normalized = df_normalized[df_normalized['objetivo'].str.strip() != '']
        df_normalized = df_normalized[df_normalized['acoes'].str.strip() != '']
        
        return df_normalized
    
    @staticmethod
    def save_results(results_df: pd.DataFrame, output_path: str, 
                    summary_data: dict = None) -> Tuple[bool, str]:
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            results_df.to_csv(output_path, index=False, encoding=OUTPUT_ENCODING)
            
            if summary_data:
                summary_path = output_path.with_suffix('.json')
                with open(summary_path, 'w', encoding=OUTPUT_ENCODING) as f:
                    json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            return True, str(output_path)
            
        except Exception as e:
            return False, f"Erro ao salvar: {str(e)}"
    
    @staticmethod
    def generate_filename(prefix: str = "analise", extension: str = "csv") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    
    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        file_path = Path(file_path)
        
        if not file_path.exists():
            return False, "Arquivo não encontrado"
        
        if file_path.suffix.lower() not in ['.csv', '.xlsx', '.xls']:
            return False, "Formato de arquivo não suportado"
        
        if file_path.stat().st_size == 0:
            return False, "Arquivo está vazio"
        
        return True, "Arquivo válido"
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        file_path = Path(file_path)
        
        info = {
            'nome': file_path.name,
            'tamanho': file_path.stat().st_size,
            'extensao': file_path.suffix.lower(),
            'caminho_completo': str(file_path.absolute()),
            'existe': file_path.exists()
        }
        
        return info
