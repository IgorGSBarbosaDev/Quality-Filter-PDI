"""
Configurações do sistema de análise de qualidade PDI.
Define constantes, thresholds e configurações gerais.
"""
from typing import Dict, List

# Configurações de qualidade
QUALITY_THRESHOLDS: Dict[str, float] = {
    'low': 0.3,
    'medium': 0.6,
    'high': 0.8
}

# Pesos das métricas de qualidade
METRIC_WEIGHTS: Dict[str, float] = {
    'clarity': 0.25,
    'specificity': 0.25,
    'completeness': 0.25,
    'structure': 0.15,
    'smart_criteria': 0.10
}

# Limites de validação
MIN_WORD_COUNT: int = 10
MIN_SENTENCE_COUNT: int = 2
MAX_TEXT_LENGTH: int = 1000

# Mapeamento de colunas para CSV
COLUMN_MAPPING: Dict[str, str] = {
    'nome': 'Nome Completo',
    'matricula': 'Proprietário do Meta Matrícula',
    'finalidade': 'Finalidade',
    'acoes_planejadas': 'Ações a serem realizadas',
    'objetivo_desenvolvimento': 'Objetivo de Desenvolvimento (GAP)',
    'atividade_aprendizagem': 'Atividade de Aprendizagem',
    'descricao': 'Descrição'
}

# Palavras-chave SMART em português
SMART_KEYWORDS: Dict[str, List[str]] = {
    'specific': ['específico', 'especifica', 'claro', 'preciso', 'definido', 'detalhado'],
    'measurable': ['medir', 'mensurar', 'métrica', 'indicador', 'quantidade', 'percentual', '%', 'prazo'],
    'achievable': ['possível', 'viável', 'realista', 'alcançável', 'factível'],
    'relevant': ['importante', 'relevante', 'necessário', 'estratégico', 'essencial'],
    'time_bound': ['prazo', 'até', 'em', 'durante', 'mês', 'ano', 'trimestre', 'semestre', 'data']
}

# Indicadores de qualidade
POSITIVE_INDICATORS: List[str] = [
    'implementar', 'desenvolver', 'executar', 'realizar', 'concluir',
    'atingir', 'alcançar', 'obter', 'conseguir', 'finalizar',
    'criar', 'construir', 'estabelecer', 'melhorar', 'aprimorar'
]

NEGATIVE_INDICATORS: List[str] = [
    'não sei', 'talvez', 'pode ser', 'acho que', 'vou tentar',
    'espero', 'gostaria', 'pretendo', 'deveria', 'poderia'
]

# Configurações de arquivo
SUPPORTED_ENCODINGS: List[str] = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
OUTPUT_ENCODING: str = 'utf-8'

# Configurações de processamento
BATCH_SIZE: int = 100
PROGRESS_INTERVAL: int = 50
