"""
⚙️ Configurações Centralizadas do Quality Filter PDI
Sistema de configuração robusto e extensível
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json
import os
from .interfaces import ConfigurationProvider
from .exceptions import ConfigurationError


@dataclass
class QualityThresholds:
    """Limites de qualidade para classificação"""
    baixo: float = 0.3
    medio: float = 0.6
    alto: float = 0.8
    excelente: float = 0.9


@dataclass
class MetricWeights:
    """Pesos das métricas de qualidade (deve somar 1.0)"""
    clarity: float = 0.35      # 35% - Clareza
    specificity: float = 0.35  # 35% - Especificidade  
    completeness: float = 0.30 # 30% - Completude
    
    def __post_init__(self):
        total = self.clarity + self.specificity + self.completeness
        if abs(total - 1.0) > 0.001:
            raise ConfigurationError(f"Pesos das métricas devem somar 1.0, atual: {total}")


@dataclass
class CohesionThresholds:
    """Limites para análise de coesão"""
    muito_ruim: float = 0.2
    ruim: float = 0.4
    medio: float = 0.6
    bom: float = 0.8


@dataclass
class TextAnalysisConfig:
    """Configurações para análise de texto"""
    min_word_count: int = 10
    min_sentence_count: int = 2
    max_text_length: int = 1000
    encoding_options: List[str] = field(default_factory=lambda: [
        'utf-8', 'latin-1', 'iso-8859-1', 'cp1252'
    ])
    output_encoding: str = 'utf-8'


@dataclass
class ProcessingConfig:
    """Configurações de processamento"""
    batch_size: int = 100
    progress_interval: int = 50
    enable_parallel: bool = True
    max_workers: Optional[int] = None
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hora


@dataclass
class AIConfig:
    """Configurações de IA"""
    enable_ai: bool = True
    preferred_analyzer: str = 'advanced'
    fallback_to_traditional: bool = True
    model_cache_dir: Optional[str] = None
    max_retries: int = 3


class DefaultConfiguration(ConfigurationProvider):
    """Provedor de configuração padrão"""
    
    def __init__(self):
        self._config = self._load_default_config()
        self._custom_config = {}
        
        # Carregar configurações personalizadas se existirem
        self._load_custom_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Carrega configurações padrão"""
        return {
            'quality_thresholds': QualityThresholds(),
            'metric_weights': MetricWeights(),
            'cohesion_thresholds': CohesionThresholds(),
            'text_analysis': TextAnalysisConfig(),
            'processing': ProcessingConfig(),
            'ai': AIConfig(),
            
            # Mapeamento de colunas
            'column_mapping': {
                'nome': 'Nome Completo',
                'matricula': 'Proprietário do Meta Matrícula',
                'finalidade': 'Finalidade',
                'acoes_planejadas': 'Ações a serem realizadas',
                'objetivo_desenvolvimento': 'Objetivo de Desenvolvimento (GAP)',
                'atividade_aprendizagem': 'Atividade de Aprendizagem',
                'descricao': 'Descrição'
            },
            
            # Indicadores de texto
            'positive_indicators': [
                'implementar', 'desenvolver', 'executar', 'realizar', 'concluir',
                'atingir', 'alcançar', 'obter', 'conseguir', 'finalizar',
                'criar', 'construir', 'estabelecer', 'melhorar', 'aprimorar',
                'definir', 'planejar', 'organizar', 'analisar', 'avaliar'
            ],
            
            'negative_indicators': [
                'não sei', 'talvez', 'pode ser', 'acho que', 'vou tentar',
                'espero', 'gostaria', 'pretendo', 'deveria', 'poderia',
                'quem sabe', 'se possível', 'tentarei'
            ],
            
            # Categorias para classificação de skills
            'skill_categories': {
                'hard_skills': [
                    'programação', 'python', 'java', 'javascript', 'sql',
                    'excel', 'powerbi', 'tableau', 'photoshop', 'autocad',
                    'análise de dados', 'machine learning', 'contabilidade',
                    'marketing digital', 'seo', 'análise financeira'
                ],
                'soft_skills': [
                    'liderança', 'comunicação', 'trabalho em equipe',
                    'resolução de problemas', 'criatividade', 'adaptabilidade',
                    'gestão do tempo', 'pensamento crítico', 'empatia',
                    'negociação', 'apresentação', 'feedback'
                ]
            }
        }
    
    def _load_custom_config(self):
        """Carrega configurações personalizadas de arquivo"""
        config_file = Path.cwd() / 'quality_filter_config.json'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self._custom_config = json.load(f)
            except Exception as e:
                from .logging_config import get_logger
                logger = get_logger('config')
                logger.warning(f"Erro ao carregar configuração personalizada: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Recupera configuração"""
        # Primeiro verifica configurações personalizadas
        if key in self._custom_config:
            return self._custom_config[key]
        
        # Depois configurações padrão
        keys = key.split('.')
        current = self._config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            elif hasattr(current, k):
                current = getattr(current, k)
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any) -> None:
        """Define configuração personalizada"""
        self._custom_config[key] = value
    
    def load_from_file(self, file_path: str) -> None:
        """Carrega configurações de arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self._custom_config.update(config)
        except Exception as e:
            raise ConfigurationError(f"Erro ao carregar configuração de {file_path}: {e}")
    
    def save_custom_config(self, file_path: Optional[str] = None) -> None:
        """Salva configurações personalizadas"""
        if not file_path:
            file_path = Path.cwd() / 'quality_filter_config.json'
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._custom_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ConfigurationError(f"Erro ao salvar configuração: {e}")


# Instância global da configuração
config = DefaultConfiguration()

# Funções de conveniência para compatibilidade
def get_quality_thresholds() -> QualityThresholds:
    return config.get('quality_thresholds')

def get_metric_weights() -> MetricWeights:
    return config.get('metric_weights')

def get_cohesion_thresholds() -> CohesionThresholds:
    return config.get('cohesion_thresholds')

# Exportações para compatibilidade com código existente
QUALITY_THRESHOLDS = {
    'low': config.get('quality_thresholds').baixo,
    'medium': config.get('quality_thresholds').medio,
    'high': config.get('quality_thresholds').alto
}

METRIC_WEIGHTS = {
    'clarity': config.get('metric_weights').clarity,
    'specificity': config.get('metric_weights').specificity,
    'completeness': config.get('metric_weights').completeness
}

MIN_WORD_COUNT = config.get('text_analysis').min_word_count
MIN_SENTENCE_COUNT = config.get('text_analysis').min_sentence_count
MAX_TEXT_LENGTH = config.get('text_analysis').max_text_length

COLUMN_MAPPING = config.get('column_mapping')
POSITIVE_INDICATORS = config.get('positive_indicators')
NEGATIVE_INDICATORS = config.get('negative_indicators')

SUPPORTED_ENCODINGS = config.get('text_analysis').encoding_options
OUTPUT_ENCODING = config.get('text_analysis').output_encoding

BATCH_SIZE = config.get('processing').batch_size
PROGRESS_INTERVAL = config.get('processing').progress_interval
