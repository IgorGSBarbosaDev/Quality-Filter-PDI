"""
🤖 Quality Filter PDI - Sistema de Análise Inteligente de PDI
Análise automatizada de qualidade com IA integrada e performance otimizada
"""

from .pdi_analyzer import PDIAnalyzer
from .core.config import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, COLUMN_MAPPING,
    POSITIVE_INDICATORS, NEGATIVE_INDICATORS
)

# Importação condicional de IA
try:
    from .ai.simple_ai_analyzer import SimpleAIAnalyzer
    AI_SIMPLE_AVAILABLE = True
except ImportError:
    AI_SIMPLE_AVAILABLE = False

try:
    from .ai.advanced_ai_analyzer import AdvancedAIAnalyzer
    from .ai.cloud_ai_analyzer import CloudAIAnalyzer
    AI_ADVANCED_AVAILABLE = True
except ImportError:
    AI_ADVANCED_AVAILABLE = False

# Importação condicional de performance
try:
    from .core.performance_cache import get_cache_stats, clear_all_caches
    from .core.parallel_processor import ParallelProcessor
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False

__version__ = "3.0.0"
__author__ = "Quality Filter PDI Team"
__description__ = "Sistema de Análise de Qualidade de PDI com IA Simples Integrada"

# Status das funcionalidades
FEATURES = {
    'ai_simple': AI_SIMPLE_AVAILABLE,
    'ai_advanced': AI_ADVANCED_AVAILABLE,
    'performance': PERFORMANCE_AVAILABLE,
    'version': __version__
}

# Wrapper de compatibilidade para manter API existente
class QualityFilterPDI(PDIAnalyzer):
    """
    Wrapper de compatibilidade que mantém a API original
    com IA e performance otimizada por padrão
    """
    
    def __init__(self, enable_performance: bool = True, enable_ai: bool = True):
        """
        Args:
            enable_performance: Habilitar otimizações de performance
            enable_ai: Habilitar IA Simples (recomendado)
        """
        super().__init__(
            enable_cache=enable_performance,
            enable_parallel=enable_performance,
            enable_ai=enable_ai
        )

__all__ = [
    "PDIAnalyzer",
    "QualityFilterPDI",
    "QUALITY_THRESHOLDS",
    "METRIC_WEIGHTS", 
    "COLUMN_MAPPING",
    "FEATURES"
]

# Funções de conveniência
def get_system_status():
    """Retorna status completo do sistema"""
    return {
        "version": __version__,
        "features": FEATURES,
        "description": __description__,
        "ai_simple_ready": AI_SIMPLE_AVAILABLE,
        "performance_ready": PERFORMANCE_AVAILABLE
    }

def quick_analyze(objetivo: str, acoes: str, enable_ai: bool = True):
    """
    Análise rápida de PDI sem instanciar classe
    
    Args:
        objetivo: Objetivo do PDI
        acoes: Ações planejadas
        enable_ai: Usar IA (recomendado)
    
    Returns:
        Dict com resultado da análise
    """
    analyzer = PDIAnalyzer(enable_ai=enable_ai)
    return analyzer.analyze_text(objetivo, acoes)

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
