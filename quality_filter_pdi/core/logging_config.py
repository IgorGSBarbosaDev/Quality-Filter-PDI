"""
📊 Sistema de Logging Padronizado
Configuração consistente de logs para todo o projeto
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class QualityFilterLogger:
    """Logger padronizado para o Quality Filter PDI"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logging()
            QualityFilterLogger._initialized = True
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        
        # Formato padrão
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Logger principal
        self.logger = logging.getLogger('quality_filter_pdi')
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Evitar duplicação de handlers
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Retorna logger específico para módulo"""
        if name:
            return logging.getLogger(f'quality_filter_pdi.{name}')
        return self.logger
    
    def set_level(self, level: str):
        """Define nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)"""
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(numeric_level)
        for handler in self.logger.handlers:
            handler.setLevel(numeric_level)
    
    def add_file_handler(self, log_file: Path, level: str = 'INFO'):
        """Adiciona handler para arquivo"""
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)


# Instância global
logger_instance = QualityFilterLogger()

# Função de conveniência
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Função de conveniência para obter logger"""
    return logger_instance.get_logger(name)
