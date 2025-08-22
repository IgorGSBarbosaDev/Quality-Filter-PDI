"""
Quality Filter PDI v3.1.0

Sistema avançado de análise de qualidade para Planos de Desenvolvimento Individual (PDI).
Implementa análise inteligente com IA, métricas robustas e arquitetura modular.

Principais funcionalidades:
- Análise de qualidade com métricas (Clareza, Especificidade, Completude)
- Análise de coesão da meta usando IA avançada
- Sistema de configuração flexível
- Logging estruturado e tratamento de erros robusto
- Cache inteligente e processamento paralelo opcional
"""

__version__ = "3.1.0"
__author__ = "Quality Filter PDI Team"
__email__ = "contato@qualityfilter.dev"

# Imports essenciais do core
from .core.config import DefaultConfiguration, QualityThresholds, MetricWeights
from .core.exceptions import QualityFilterPDIError, ConfigurationError, AIAnalysisError
from .core.logging_config import get_logger
from .core.factory import ServiceManager
from .core.validators import PDIDataValidator, ConfigValidator

# Import seguro do analisador principal
def _safe_import():
    """Importa componentes de forma segura"""
    try:
        from .pdi_analyzer import PDIAnalyzer
        return PDIAnalyzer
    except ImportError as e:
        get_logger(__name__).warning(f"Importação do PDIAnalyzer falhou: {e}")
        return None

# Classe principal exportada
QualityFilterPDI = _safe_import()
PDIAnalyzer = QualityFilterPDI  # Alias para compatibilidade

# Função de conveniência para análise rápida
def quick_analyze(meta_desenvolvimento, acoes="", atividades="", enable_ai=True, enable_cache=True):
    """
    Análise rápida de qualidade de PDI
    
    Args:
        meta_desenvolvimento (str): Objetivo de desenvolvimento
        acoes (str): Ações planejadas (opcional)
        atividades (str): Atividades planejadas (opcional)
        enable_ai (bool): Habilitar análise de IA
        enable_cache (bool): Habilitar cache
    
    Returns:
        dict: Resultado da análise com métricas e pontuação
    """
    if QualityFilterPDI is None:
        raise QualityFilterPDIError("PDIAnalyzer não está disponível")
    
    analyzer = QualityFilterPDI(enable_ai=enable_ai, enable_cache=enable_cache)
    return analyzer.analyze_single(meta_desenvolvimento, acoes, atividades)

# Função para obter status do sistema
def get_system_status():
    """
    Obtém status dos componentes do sistema
    
    Returns:
        dict: Status de cada componente
    """
    status = {
        "version": __version__,
        "core_components": True,
        "pdi_analyzer": QualityFilterPDI is not None,
        "ai_available": False,
        "cache_available": False
    }
    
    # Verifica disponibilidade de IA
    try:
        from .ai.analyzers import CohesionAnalyzer
        status["ai_available"] = True
    except ImportError:
        pass
    
    # Verifica disponibilidade de cache
    try:
        from .utils.cache import CacheManager
        status["cache_available"] = True
    except ImportError:
        pass
    
    return status

# Exports principais
__all__ = [
    # Classe principal
    "QualityFilterPDI",
    "PDIAnalyzer",
    
    # Funções utilitárias
    "quick_analyze",
    "get_system_status",
    
    # Configuração
    "DefaultConfiguration",
    "QualityThresholds", 
    "MetricWeights",
    
    # Exceções
    "QualityFilterPDIError",
    "ConfigurationError",
    "AIAnalysisError",
    
    # Utilitários
    "get_logger",
    "ServiceManager",
    "PDIDataValidator",
    "ConfigValidator",
    
    # Metadados
    "__version__",
    "__author__",
    "__email__"
]

# Configuração inicial do logging
_logger = get_logger(__name__)
_logger.info(f"Quality Filter PDI v{__version__} inicializado")

# Verificação de dependências opcionais
_status = get_system_status()
if not _status["pdi_analyzer"]:
    _logger.warning("PDIAnalyzer não disponível - verifique dependências")
if not _status["ai_available"]:
    _logger.info("Componentes de IA não disponíveis - funcionalidade básica ativa")
if not _status["cache_available"]:
    _logger.info("Sistema de cache não disponível - processamento sem cache")
