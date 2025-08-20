from .pdi_analyzer import PDIAnalyzer
from .core.config import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, COLUMN_MAPPING,
    POSITIVE_INDICATORS, NEGATIVE_INDICATORS
)
from .services.pdi_analysis_service import PDIAnalysisService
from .services.quality_metrics_service import QualityMetricsService
from .services.file_service import FileService
from .services.skill_classifier import SkillClassifier
from .utils.text_utils import TextUtils

try:
    from .ai.ai_text_analyzer import AITextAnalyzer
    from .ai.advanced_ai_analyzer import AdvancedAIAnalyzer
    from .ai.cloud_ai_analyzer import CloudAIAnalyzer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Importação condicional de performance
try:
    from .core.performance_cache import get_cache_stats, clear_all_caches
    from .core.parallel_processor import ParallelProcessor
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False

__version__ = "2.1.0"
__author__ = "Quality Filter PDI Team"
__description__ = "Sistema de Análise de Qualidade de PDI com IA e Otimizações de Performance"

# Wrapper de compatibilidade para manter API existente
class QualityFilterPDI(PDIAnalyzer):
    """
    Wrapper de compatibilidade que mantém a API original
    com melhorias de performance opcionais
    """
    
    def __init__(self, enable_performance: bool = True):
        """
        Args:
            enable_performance: Habilitar otimizações de performance (cache + paralelo)
        """
        super().__init__(
            enable_cache=enable_performance,
            enable_parallel=enable_performance
        )

__all__ = [
    "PDIAnalyzer",
    "QualityFilterPDI",  # Wrapper de compatibilidade
    "PDIAnalysisService", 
    "QualityMetricsService",
    "FileService",
    "SkillClassifier",
    "TextUtils",
    "QUALITY_THRESHOLDS",
    "METRIC_WEIGHTS",
    "COLUMN_MAPPING",
    "AI_AVAILABLE",
    "PERFORMANCE_AVAILABLE"
]
