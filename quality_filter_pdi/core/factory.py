"""
🏭 Factory Pattern para Componentes
Criação consistente e configurável de componentes do sistema
"""

from typing import Dict, Any, Optional, Type, TypeVar, Generic
from ..core.interfaces import AIAnalyzer, CacheProvider, ConfigurationProvider
from ..core.exceptions import ConfigurationError
from ..core.logging_config import get_logger

logger = get_logger('factory')

T = TypeVar('T')


class ComponentFactory(Generic[T]):
    """Factory base para criação de componentes"""
    
    def __init__(self):
        self._registry: Dict[str, Type[T]] = {}
        self._instances: Dict[str, T] = {}
    
    def register(self, name: str, component_class: Type[T]) -> None:
        """Registra uma classe de componente"""
        self._registry[name] = component_class
        logger.debug(f"Registrado componente '{name}': {component_class.__name__}")
    
    def create(self, name: str, **kwargs) -> T:
        """Cria instância do componente"""
        if name not in self._registry:
            available = list(self._registry.keys())
            raise ConfigurationError(
                f"Componente '{name}' não registrado. Disponíveis: {available}"
            )
        
        component_class = self._registry[name]
        try:
            instance = component_class(**kwargs)
            logger.debug(f"Criado componente '{name}' com sucesso")
            return instance
        except Exception as e:
            raise ConfigurationError(
                f"Erro ao criar componente '{name}': {str(e)}"
            ) from e
    
    def get_or_create_singleton(self, name: str, **kwargs) -> T:
        """Retorna instância singleton do componente"""
        if name not in self._instances:
            self._instances[name] = self.create(name, **kwargs)
        return self._instances[name]
    
    def list_available(self) -> list[str]:
        """Lista componentes disponíveis"""
        return list(self._registry.keys())


class AIAnalyzerFactory(ComponentFactory[AIAnalyzer]):
    """Factory específica para analisadores de IA"""
    
    def __init__(self):
        super().__init__()
        self._setup_default_analyzers()
    
    def _setup_default_analyzers(self):
        """Registra analisadores padrão disponíveis"""
        
        # Tentar registrar IA simples
        try:
            from ..ai.simple_ai_analyzer import SimpleAIAnalyzer
            self.register('simple', SimpleAIAnalyzer)
        except ImportError:
            logger.warning("SimpleAIAnalyzer não disponível")
        
        # Tentar registrar IA avançada
        try:
            from ..ai.advanced_ai_analyzer import AdvancedAIAnalyzer
            self.register('advanced', AdvancedAIAnalyzer)
        except ImportError:
            logger.warning("AdvancedAIAnalyzer não disponível")
        
        # Tentar registrar IA cloud
        try:
            from ..ai.cloud_ai_analyzer import CloudAIAnalyzer
            self.register('cloud', CloudAIAnalyzer)
        except ImportError:
            logger.warning("CloudAIAnalyzer não disponível")
    
    def create_best_available(self, **kwargs) -> Optional[AIAnalyzer]:
        """Cria o melhor analisador disponível"""
        
        # Prioridade: advanced > cloud > simple
        preferences = ['advanced', 'cloud', 'simple']
        
        for analyzer_name in preferences:
            if analyzer_name in self._registry:
                try:
                    analyzer = self.create(analyzer_name, **kwargs)
                    if hasattr(analyzer, 'is_available') and analyzer.is_available():
                        logger.info(f"Usando analisador de IA: {analyzer_name}")
                        return analyzer
                except Exception as e:
                    logger.warning(f"Falha ao inicializar {analyzer_name}: {e}")
                    continue
        
        logger.warning("Nenhum analisador de IA disponível")
        return None


class CacheProviderFactory(ComponentFactory[CacheProvider]):
    """Factory para provedores de cache"""
    
    def __init__(self):
        super().__init__()
        self._setup_default_providers()
    
    def _setup_default_providers(self):
        """Registra provedores padrão"""
        
        # Cache em memória simples
        try:
            from ..core.performance_cache import MemoryCacheProvider
            self.register('memory', MemoryCacheProvider)
        except ImportError:
            # Criar um cache simples se não existir
            self._create_simple_cache()
    
    def _create_simple_cache(self):
        """Cria cache simples em memória"""
        
        class SimpleCacheProvider:
            def __init__(self):
                self._cache = {}
            
            def get(self, key: str) -> Optional[Any]:
                return self._cache.get(key)
            
            def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
                self._cache[key] = value
            
            def clear(self) -> None:
                self._cache.clear()
        
        self.register('simple', SimpleCacheProvider)


class ServiceManager:
    """Gerenciador central de serviços e dependências"""
    
    def __init__(self):
        self.ai_factory = AIAnalyzerFactory()
        self.cache_factory = CacheProviderFactory()
        self._config: Optional[ConfigurationProvider] = None
        self._services: Dict[str, Any] = {}
    
    def set_configuration(self, config: ConfigurationProvider) -> None:
        """Define provedor de configuração"""
        self._config = config
    
    def get_ai_analyzer(self, analyzer_type: Optional[str] = None, **kwargs) -> Optional[AIAnalyzer]:
        """Obtém analisador de IA"""
        if analyzer_type:
            return self.ai_factory.create(analyzer_type, **kwargs)
        return self.ai_factory.create_best_available(**kwargs)
    
    def get_cache_provider(self, provider_type: str = 'memory', **kwargs) -> CacheProvider:
        """Obtém provedor de cache"""
        return self.cache_factory.get_or_create_singleton(provider_type, **kwargs)
    
    def register_service(self, name: str, service: Any) -> None:
        """Registra serviço customizado"""
        self._services[name] = service
        logger.debug(f"Serviço '{name}' registrado")
    
    def get_service(self, name: str) -> Any:
        """Recupera serviço registrado"""
        if name not in self._services:
            raise ConfigurationError(f"Serviço '{name}' não registrado")
        return self._services[name]
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Recupera configuração"""
        if self._config:
            return self._config.get(key, default)
        return default


# Instância global do gerenciador
service_manager = ServiceManager()
