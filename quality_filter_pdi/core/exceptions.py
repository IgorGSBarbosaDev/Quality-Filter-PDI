"""
🛡️ Sistema de Exceções Padronizadas
Hierarquia consistente de exceções para todo o projeto
"""

from typing import Optional, Dict, Any


class QualityFilterPDIError(Exception):
    """Exceção base para todos os erros do Quality Filter PDI"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}


class ConfigurationError(QualityFilterPDIError):
    """Erro de configuração do sistema"""
    pass


class FileProcessingError(QualityFilterPDIError):
    """Erro no processamento de arquivos"""
    pass


class AIAnalysisError(QualityFilterPDIError):
    """Erro na análise com IA"""
    pass


class DataValidationError(QualityFilterPDIError):
    """Erro na validação de dados"""
    pass


class PerformanceError(QualityFilterPDIError):
    """Erro relacionado à performance/cache"""
    pass


class AnalysisError(QualityFilterPDIError):
    """Erro durante análise de qualidade"""
    pass


def handle_exception(func):
    """Decorator para tratamento padronizado de exceções"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except QualityFilterPDIError:
            raise  # Re-raise custom exceptions
        except Exception as e:
            # Convert to custom exception
            raise QualityFilterPDIError(
                f"Erro inesperado em {func.__name__}: {str(e)}",
                error_code="UNEXPECTED_ERROR",
                details={"function": func.__name__, "args": str(args), "kwargs": str(kwargs)}
            ) from e
    return wrapper
