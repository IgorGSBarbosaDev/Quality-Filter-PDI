"""
Módulo principal da aplicação de análise de qualidade PDI.
"""

from .pdi_analyzer import PDIAnalyzer
from .core.config import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, COLUMN_MAPPING,
    SMART_KEYWORDS, POSITIVE_INDICATORS, NEGATIVE_INDICATORS
)
from .services.pdi_analysis_service import PDIAnalysisService
from .services.quality_metrics_service import QualityMetricsService
from .services.file_service import FileService
from .utils.text_utils import TextUtils

__version__ = "2.0.0"
__author__ = "Sistema de Análise de Qualidade PDI"

__all__ = [
    "PDIAnalyzer",
    "PDIAnalysisService",
    "QualityMetricsService", 
    "FileService",
    "TextUtils",
    "QUALITY_THRESHOLDS",
    "METRIC_WEIGHTS",
    "COLUMN_MAPPING",
    "SMART_KEYWORDS",
    "POSITIVE_INDICATORS",
    "NEGATIVE_INDICATORS"
]
