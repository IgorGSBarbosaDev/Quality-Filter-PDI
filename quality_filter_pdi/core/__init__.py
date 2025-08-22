"""
🧠 Módulo Core - Quality Filter PDI
Componentes fundamentais do sistema: configuração, cache, logging, etc.
"""

from .config import config, get_quality_thresholds, get_metric_weights
from .exceptions import (
    QualityFilterPDIError,
    ConfigurationError,
    FileProcessingError,
    AIAnalysisError,
    DataValidationError,
    AnalysisError
)
from .logging_config import get_logger
from .factory import service_manager
from .validators import validate_text, validate_pdi_data, validate_dataframe
from .interfaces import AnalysisResult, BaseQualityMetric, BaseAnalysisService

# Importações condicionais
try:
    from .performance_cache import get_cache_stats, clear_all_caches
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False

try:
    from .parallel_processor import ParallelProcessor
    PARALLEL_AVAILABLE = True
except ImportError:
    PARALLEL_AVAILABLE = False

__all__ = [
    # Configuração
    "config",
    "get_quality_thresholds",
    "get_metric_weights",
    
    # Exceções
    "QualityFilterPDIError",
    "ConfigurationError",
    "FileProcessingError",
    "AIAnalysisError",
    "DataValidationError",
    "AnalysisError",
    
    # Logging
    "get_logger",
    
    # Factory
    "service_manager",
    
    # Validação
    "validate_text",
    "validate_pdi_data",
    "validate_dataframe",
    
    # Interfaces
    "AnalysisResult",
    "BaseQualityMetric",
    "BaseAnalysisService",
    
    # Performance (opcional)
    "CACHE_AVAILABLE",
    "PARALLEL_AVAILABLE"
]

if CACHE_AVAILABLE:
    __all__.extend(["get_cache_stats", "clear_all_caches"])

if PARALLEL_AVAILABLE:
    __all__.extend(["ParallelProcessor"])