from .pdi_analyzer import PDIAnalyzer
from .core.config import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, COLUMN_MAPPING,
    SMART_KEYWORDS, POSITIVE_INDICATORS, NEGATIVE_INDICATORS
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

__version__ = "2.0.0"
__author__ = "Quality Filter PDI Team"
__description__ = "Sistema de Análise de Qualidade de PDI com IA"

__all__ = [
    "PDIAnalyzer",
    "PDIAnalysisService", 
    "QualityMetricsService",
    "FileService",
    "SkillClassifier",
    "TextUtils",
    "QUALITY_THRESHOLDS",
    "METRIC_WEIGHTS",
    "COLUMN_MAPPING",
    "AI_AVAILABLE"
]
