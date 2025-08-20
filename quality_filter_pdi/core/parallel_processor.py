import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import List, Dict, Any, Callable, Optional
import pandas as pd
import os
from functools import partial


class ParallelProcessor:
    """
    Sistema de processamento paralelo para análise de PDIs
    """
    
    def __init__(self, max_workers: Optional[int] = None, use_threads: bool = False):
        """
        Args:
            max_workers: Número máximo de workers (None = automático)
            use_threads: Usar threads ao invés de processes (para I/O intensivo)
        """
        self.max_workers = max_workers or min(mp.cpu_count(), 8)
        self.use_threads = use_threads
        
    def process_batch(self, 
                     items: List[Dict[str, Any]], 
                     process_func: Callable,
                     chunk_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Processa lista de itens em paralelo
        
        Args:
            items: Lista de dicionários com dados para processar
            process_func: Função que processa um item individual
            chunk_size: Tamanho do chunk (None = automático)
        """
        if len(items) < 10:  # Para poucos itens, processo sequencial é mais eficiente
            return [process_func(item) for item in items]
        
        chunk_size = chunk_size or max(1, len(items) // (self.max_workers * 2))
        
        if self.use_threads:
            executor_class = ThreadPoolExecutor
        else:
            executor_class = ProcessPoolExecutor
            
        try:
            with executor_class(max_workers=self.max_workers) as executor:
                # Dividir em chunks para melhor distribuição
                chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
                
                # Processar chunks em paralelo
                chunk_results = list(executor.map(
                    partial(self._process_chunk, process_func=process_func), 
                    chunks
                ))
                
                # Flatten results
                results = []
                for chunk_result in chunk_results:
                    results.extend(chunk_result)
                    
                return results
                
        except Exception as e:
            print(f"⚠️ Erro no processamento paralelo, fallback para sequencial: {e}")
            return [process_func(item) for item in items]
    
    @staticmethod
    def _process_chunk(chunk: List[Dict[str, Any]], process_func: Callable) -> List[Dict[str, Any]]:
        """Processa um chunk de itens"""
        return [process_func(item) for item in chunk]
    
    def process_dataframe(self, 
                         df: pd.DataFrame,
                         process_func: Callable,
                         batch_size: int = 100) -> pd.DataFrame:
        """
        Processa DataFrame em paralelo por batches
        
        Args:
            df: DataFrame com dados
            process_func: Função que processa uma linha
            batch_size: Tamanho do batch para processamento
        """
        if len(df) < batch_size:
            # Para DataFrames pequenos, processo sequencial
            results = []
            for idx, row in df.iterrows():
                result = process_func(row.to_dict())
                result['row_index'] = idx
                results.append(result)
            return pd.DataFrame(results)
        
        # Dividir DataFrame em batches
        batches = [df.iloc[i:i + batch_size] for i in range(0, len(df), batch_size)]
        
        # Processar batches em paralelo
        batch_results = []
        
        if self.use_threads:
            executor_class = ThreadPoolExecutor
        else:
            executor_class = ProcessPoolExecutor
        
        try:
            with executor_class(max_workers=self.max_workers) as executor:
                futures = []
                
                for batch_idx, batch in enumerate(batches):
                    future = executor.submit(
                        self._process_dataframe_batch,
                        batch, 
                        process_func,
                        batch_idx * batch_size
                    )
                    futures.append(future)
                
                # Coletar resultados
                for future in futures:
                    batch_result = future.result()
                    batch_results.extend(batch_result)
                    
        except Exception as e:
            print(f"⚠️ Erro no processamento paralelo de DataFrame: {e}")
            # Fallback sequencial
            results = []
            for idx, row in df.iterrows():
                result = process_func(row.to_dict())
                result['row_index'] = idx
                results.append(result)
            return pd.DataFrame(results)
        
        return pd.DataFrame(batch_results)
    
    @staticmethod
    def _process_dataframe_batch(batch: pd.DataFrame, 
                                process_func: Callable,
                                start_index: int) -> List[Dict[str, Any]]:
        """Processa um batch do DataFrame"""
        results = []
        for idx, row in batch.iterrows():
            result = process_func(row.to_dict())
            result['row_index'] = start_index + (idx - batch.index[0])
            results.append(result)
        return results


def get_optimal_workers() -> int:
    """Retorna número ótimo de workers baseado no sistema"""
    cpu_count = mp.cpu_count()
    
    # Para análise de texto, uso mais conservativo de CPU
    if cpu_count <= 2:
        return 2
    elif cpu_count <= 4:
        return 3
    elif cpu_count <= 8:
        return min(6, cpu_count)
    else:
        return min(8, cpu_count - 2)  # Deixar algumas CPUs livres


def create_parallel_analyzer(use_threads: bool = False) -> ParallelProcessor:
    """
    Factory para criar processador paralelo otimizado
    
    Args:
        use_threads: True para I/O intensivo, False para CPU intensivo
    """
    optimal_workers = get_optimal_workers()
    return ParallelProcessor(max_workers=optimal_workers, use_threads=use_threads)


# Worker function para processamento de PDI individual
def process_single_pdi_worker(pdi_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Worker function para processamento paralelo de PDI individual
    Deve ser importada no processo worker
    """
    try:
        # Import local para evitar problemas de serialização
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
        from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService
        from quality_filter_pdi.services.skill_classifier import SkillClassifier
        from quality_filter_pdi.core.config import QUALITY_THRESHOLDS
        
        # Criar serviços
        quality_service = QualityMetricsService()
        skill_classifier = SkillClassifier()
        
        # Processar PDI
        objetivo = pdi_data.get('objetivo', '')
        acoes = pdi_data.get('acoes', '')
        atividade = pdi_data.get('atividade', '')
        
        # Análise simplificada sem AI para performance
        analysis_service = PDIAnalysisService(
            quality_service=quality_service,
            skill_classifier=skill_classifier,
            thresholds=QUALITY_THRESHOLDS,
            ai_enabled=False  # Desabilitar AI para processamento paralelo
        )
        
        result = analysis_service.analyze_single_pdi(objetivo, acoes, atividade)
        result['row_index'] = pdi_data.get('row_index', 0)
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'row_index': pdi_data.get('row_index', 0),
            'overall_score': 0.0,
            'quality_level': 'Baixa'
        }
