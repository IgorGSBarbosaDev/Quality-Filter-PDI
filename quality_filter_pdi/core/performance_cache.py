"""
Cache otimizado para Quality Filter PDI
Implementa LRU cache para cálculos de métricas repetidas
"""

import hashlib
from functools import lru_cache
from typing import Dict, Any, Tuple


class PerformanceCache:
    """
    Sistema de cache otimizado para métricas de PDI
    """
    
    def __init__(self, maxsize: int = 1000):
        self.maxsize = maxsize
        self._cache: Dict[str, Any] = {}
        self._access_count: Dict[str, int] = {}
    
    def _generate_key(self, text: str, method: str) -> str:
        """Gera chave única para o cache baseada no texto e método"""
        content = f"{method}:{text.strip().lower()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, method: str) -> Any:
        """Recupera valor do cache se existir"""
        key = self._generate_key(text, method)
        if key in self._cache:
            self._access_count[key] = self._access_count.get(key, 0) + 1
            return self._cache[key]
        return None
    
    def set(self, text: str, method: str, value: Any) -> None:
        """Armazena valor no cache com LRU"""
        if len(self._cache) >= self.maxsize:
            self._evict_least_used()
        
        key = self._generate_key(text, method)
        self._cache[key] = value
        self._access_count[key] = 1
    
    def _evict_least_used(self) -> None:
        """Remove o item menos usado do cache"""
        if not self._access_count:
            return
        
        least_used_key = min(self._access_count, key=self._access_count.get)
        del self._cache[least_used_key]
        del self._access_count[least_used_key]
    
    def clear(self) -> None:
        """Limpa todo o cache"""
        self._cache.clear()
        self._access_count.clear()
    
    def stats(self) -> Dict[str, int]:
        """Retorna estatísticas do cache"""
        return {
            'size': len(self._cache),
            'maxsize': self.maxsize,
            'total_accesses': sum(self._access_count.values())
        }


# Instância global do cache
_performance_cache = PerformanceCache(maxsize=2000)


def cached_metric(method_name: str):
    """
    Decorator para cache automático de métricas
    """
    def decorator(func):
        def wrapper(self, text: str, *args, **kwargs):
            # Verificar cache primeiro
            cached_result = _performance_cache.get(text, method_name)
            if cached_result is not None:
                return cached_result
            
            # Calcular se não estiver em cache
            result = func(self, text, *args, **kwargs)
            
            # Armazenar no cache
            _performance_cache.set(text, method_name, result)
            
            return result
        return wrapper
    return decorator


@lru_cache(maxsize=500)
def cached_tokenize(text: str) -> Tuple[str, ...]:
    """Cache para tokenização de texto"""
    from ..utils.text_utils import TextUtils
    tokens = TextUtils.tokenize(text)
    return tuple(tokens) if tokens else ()


@lru_cache(maxsize=500) 
def cached_sentence_count(text: str) -> int:
    """Cache para contagem de sentenças"""
    from ..utils.text_utils import TextUtils
    return TextUtils.count_sentences(text)


@lru_cache(maxsize=500)
def cached_avg_word_length(text: str) -> float:
    """Cache para cálculo de comprimento médio de palavras"""
    from ..utils.text_utils import TextUtils
    return TextUtils.calculate_avg_word_length(text)


def get_cache_stats() -> Dict[str, Any]:
    """Retorna estatísticas de performance do cache"""
    return {
        'performance_cache': _performance_cache.stats(),
        'tokenize_cache': cached_tokenize.cache_info()._asdict(),
        'sentence_cache': cached_sentence_count.cache_info()._asdict(),
        'word_length_cache': cached_avg_word_length.cache_info()._asdict()
    }


def clear_all_caches():
    """Limpa todos os caches de performance"""
    _performance_cache.clear()
    cached_tokenize.cache_clear()
    cached_sentence_count.cache_clear()
    cached_avg_word_length.cache_clear()
