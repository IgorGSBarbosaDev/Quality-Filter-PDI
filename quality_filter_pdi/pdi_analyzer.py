import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path

from .core.config import COLUMN_MAPPING
from .services.pdi_analysis_service import PDIAnalysisService
from .services.file_service import FileService

# Importação condicional de performance
try:
    from .core.performance_cache import get_cache_stats, clear_all_caches
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False


class PDIAnalyzer:
    
    def __init__(self, enable_cache: bool = True, enable_parallel: bool = True):
        """
        Args:
            enable_cache: Habilitar cache de performance
            enable_parallel: Habilitar processamento paralelo
        """
        self.analysis_service = PDIAnalysisService(
            enable_cache=enable_cache,
            enable_parallel=enable_parallel
        )
        self.file_service = FileService()
        self.column_mapping = COLUMN_MAPPING
        self.performance_enabled = PERFORMANCE_AVAILABLE
    
    def analyze_file(
        self, 
        file_path: str, 
        output_dir: str = "output",
        sample_size: Optional[int] = None
    ) -> Dict[str, Any]:
        print(f"🚀 Iniciando análise do arquivo: {Path(file_path).name}")
        
        try:
            df = self._load_file(file_path)
            
            if df.empty:
                return {
                    'success': False,
                    'error': 'Arquivo vazio ou sem dados válidos',
                    'total_analyzed': 0
                }
            
            if sample_size and sample_size < len(df):
                df = df.sample(n=sample_size, random_state=42)
                print(f"📊 Usando amostra de {sample_size} registros")
            
            results = self.analysis_service.analyze_dataframe(df)
            
            if results.get('success', False):
                output_path = Path(output_dir) / self.file_service.generate_filename()
                saved, save_path = self.file_service.save_results(
                    results['detailed_results'], 
                    str(output_path),
                    {
                        'total_analyzed': results['total_analyzed'],
                        'summary': results['summary'],
                        'analysis_timestamp': results['analysis_timestamp']
                    }
                )
                
                if saved:
                    results['output_file'] = save_path
                    print(f"✅ Resultados salvos em: {save_path}")
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro durante análise: {str(e)}',
                'total_analyzed': 0
            }
    
    def analyze_text(self, objetivo: str, acoes: str, **kwargs) -> Dict[str, Any]:
        pdi_data = {
            self.column_mapping['objetivo_desenvolvimento']: objetivo,
            self.column_mapping['acoes_planejadas']: acoes
        }
        
        for key, value in kwargs.items():
            pdi_data[key] = value
        
        return self.analysis_service.analyze_single_pdi(pdi_data)
    
    def get_quality_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        return self.analysis_service.get_quality_recommendations(analysis_result)
    
    def _load_file(self, file_path: str) -> pd.DataFrame:
        is_valid, message = self.file_service.validate_file(file_path)
        if not is_valid:
            raise ValueError(f"Arquivo inválido: {message}")
        
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.csv':
            df, encoding = self.file_service.load_csv(str(file_path))
            print(f"📄 CSV carregado com encoding: {encoding}")
        else:
            df = self.file_service.load_excel(str(file_path))
            print(f"📄 Excel carregado")
        
        print(f"📊 Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
        
        try:
            df_normalized = self.file_service.normalize_dataframe(df)
            print(f"📊 Dados normalizados: {len(df_normalized)} linhas válidas")
            return df_normalized
        except ValueError as e:
            print(f"⚠️ Erro na normalização: {e}")
            print("📋 Tentando mapeamento manual de colunas...")
            return self._try_manual_column_mapping(df)
    
    def _try_manual_column_mapping(self, df: pd.DataFrame) -> pd.DataFrame:
        print(f"📋 Colunas disponíveis: {list(df.columns)}")
        
        if len(df.columns) >= 2:
            df_mapped = df.copy()
            df_mapped['objetivo'] = df.iloc[:, 0]
            df_mapped['acoes'] = df.iloc[:, 1]
            
            df_mapped['objetivo'] = df_mapped['objetivo'].fillna('')
            df_mapped['acoes'] = df_mapped['acoes'].fillna('')
            
            df_mapped = df_mapped[df_mapped['objetivo'].str.strip() != '']
            df_mapped = df_mapped[df_mapped['acoes'].str.strip() != '']
            
            print(f"✅ Mapeamento manual aplicado: {len(df_mapped)} linhas válidas")
            return df_mapped
        
        raise ValueError("Não foi possível mapear colunas automaticamente")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        return self.file_service.get_file_info(file_path)
    
    def preview_file(self, file_path: str, max_rows: int = 5) -> Dict[str, Any]:
        try:
            df = self._load_file(file_path)
            
            return {
                'success': True,
                'total_rows': len(df),
                'columns': list(df.columns),
                'sample_data': df.head(max_rows).to_dict('records'),
                'data_types': df.dtypes.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_batch(
        self, 
        file_paths: List[str], 
        output_dir: str = "output"
    ) -> Dict[str, Any]:
        batch_results = []
        
        for file_path in file_paths:
            print(f"\n📁 Processando: {Path(file_path).name}")
            
            try:
                result = self.analyze_file(file_path, output_dir)
                result['file_path'] = file_path
                batch_results.append(result)
                
            except Exception as e:
                batch_results.append({
                    'file_path': file_path,
                    'success': False,
                    'error': str(e),
                    'total_analyzed': 0
                })
        
        total_analyzed = sum(r.get('total_analyzed', 0) for r in batch_results)
        successful_files = sum(1 for r in batch_results if r.get('success', False))
        
        return {
            'batch_summary': {
                'total_files': len(file_paths),
                'successful_files': successful_files,
                'total_pdis_analyzed': total_analyzed
            },
            'individual_results': batch_results
        }
    
    def analyze_pdis_from_dataframe(self, df: pd.DataFrame, use_parallel: bool = None) -> pd.DataFrame:
        """
        Análise otimizada de DataFrame com cache e processamento paralelo
        
        Args:
            df: DataFrame com colunas 'objetivo' e 'acoes'
            use_parallel: Forçar uso (True) ou não uso (False) de paralelo. None = automático
        """
        return self.analysis_service.analyze_dataframe_optimized(df, use_parallel)
    
    def analyze_single_pdi(self, objetivo: str, acoes: str, atividade: str = "") -> Dict[str, Any]:
        """Análise de PDI individual otimizada"""
        return self.analysis_service.analyze_single_pdi(objetivo, acoes, atividade)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance"""
        stats = {
            'performance_enabled': self.performance_enabled
        }
        
        if self.performance_enabled:
            stats.update(self.analysis_service.get_performance_stats())
        
        return stats
    
    def clear_cache(self):
        """Limpa cache de performance"""
        if self.performance_enabled:
            self.analysis_service.clear_performance_cache()
        else:
            print("⚠️ Cache de performance não está habilitado")
    
    def benchmark_performance(self, sample_size: int = 100) -> Dict[str, Any]:
        """
        Executa benchmark de performance
        
        Args:
            sample_size: Número de PDIs para teste
        """
        import time
        
        # Gerar dados de teste
        test_data = []
        for i in range(sample_size):
            test_data.append({
                'objetivo': f"Objetivo de teste {i+1} para análise de performance com detalhamento específico",
                'acoes': f"Ações específicas {i+1} com cronograma detalhado e metodologia definida"
            })
        
        df = pd.DataFrame(test_data)
        
        # Teste sequencial
        start = time.time()
        result_seq = self.analyze_pdis_from_dataframe(df, use_parallel=False)
        time_seq = time.time() - start
        
        # Teste paralelo (se disponível)
        time_par = None
        if self.performance_enabled:
            start = time.time()
            result_par = self.analyze_pdis_from_dataframe(df, use_parallel=True)
            time_par = time.time() - start
        
        # Estatísticas
        stats = {
            'sample_size': sample_size,
            'sequential_time': time_seq,
            'sequential_rate': sample_size / time_seq,
            'parallel_time': time_par,
            'parallel_rate': sample_size / time_par if time_par else None,
            'speedup': time_seq / time_par if time_par else None,
            'cache_stats': self.get_performance_stats() if self.performance_enabled else None
        }
        
        return stats
