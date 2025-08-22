"""
🔌 Interfaces e Protocolos
Definições de contratos para componentes do sistema
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class TextAnalyzer(Protocol):
    """Protocolo para analisadores de texto"""
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analisa texto e retorna métricas"""
        ...


@runtime_checkable
class AIAnalyzer(Protocol):
    """Protocolo para analisadores de IA"""
    
    def analyze_goal_cohesion(self, objetivo: str, acoes: str, atividades: str = "") -> Dict[str, Any]:
        """Analisa coesão entre objetivo e ações"""
        ...
    
    def is_available(self) -> bool:
        """Verifica se o analisador está disponível"""
        ...


@runtime_checkable
class CacheProvider(Protocol):
    """Protocolo para provedores de cache"""
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache"""
        ...
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Armazena valor no cache"""
        ...
    
    def clear(self) -> None:
        """Limpa o cache"""
        ...


class BaseQualityMetric(ABC):
    """Classe base abstrata para métricas de qualidade"""
    
    @abstractmethod
    def calculate(self, text: str) -> float:
        """Calcula a métrica para o texto fornecido"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome da métrica"""
        pass
    
    def validate_text(self, text: str) -> bool:
        """Valida se o texto é adequado para análise"""
        return text and text.strip() and len(text.strip()) > 0


class BaseAnalysisService(ABC):
    """Classe base para serviços de análise"""
    
    def __init__(self, cache_provider: Optional[CacheProvider] = None):
        self.cache_provider = cache_provider
    
    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa análise dos dados"""
        pass
    
    def _get_cache_key(self, data: Dict[str, Any]) -> str:
        """Gera chave única para cache baseada nos dados"""
        import hashlib
        import json
        
        # Serializa dados de forma consistente
        serialized = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(serialized.encode()).hexdigest()
    
    def _cache_get(self, key: str) -> Optional[Any]:
        """Recupera do cache se disponível"""
        if self.cache_provider:
            return self.cache_provider.get(key)
        return None
    
    def _cache_set(self, key: str, value: Any) -> None:
        """Armazena no cache se disponível"""
        if self.cache_provider:
            self.cache_provider.set(key, value)


class ConfigurationProvider(ABC):
    """Provedor abstrato de configurações"""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Recupera configuração"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Define configuração"""
        pass
    
    @abstractmethod
    def load_from_file(self, file_path: str) -> None:
        """Carrega configurações de arquivo"""
        pass


class AnalysisResult:
    """Resultado padronizado de análise"""
    
    def __init__(self, 
                 success: bool = True,
                 data: Optional[Dict[str, Any]] = None,
                 errors: Optional[List[str]] = None,
                 warnings: Optional[List[str]] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        self.success = success
        self.data = data or {}
        self.errors = errors or []
        self.warnings = warnings or []
        self.metadata = metadata or {}
    
    def add_error(self, error: str) -> None:
        """Adiciona erro ao resultado"""
        self.errors.append(error)
        self.success = False
    
    def add_warning(self, warning: str) -> None:
        """Adiciona aviso ao resultado"""
        self.warnings.append(warning)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'success': self.success,
            'data': self.data,
            'errors': self.errors,
            'warnings': self.warnings,
            'metadata': self.metadata
        }
