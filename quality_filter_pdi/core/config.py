from typing import Dict, List

QUALITY_THRESHOLDS: Dict[str, float] = {
    'low': 0.3,
    'medium': 0.6,
    'high': 0.8
}

METRIC_WEIGHTS: Dict[str, float] = {
    'clarity': 0.278,        # 27.8% (rebalanceado)
    'specificity': 0.278,    # 27.8% (rebalanceado)
    'completeness': 0.278,   # 27.8% (rebalanceado)
    'structure': 0.167       # 16.7% (rebalanceado)
}

MIN_WORD_COUNT: int = 10
MIN_SENTENCE_COUNT: int = 2
MAX_TEXT_LENGTH: int = 1000

COLUMN_MAPPING: Dict[str, str] = {
    'nome': 'Nome Completo',
    'matricula': 'Proprietário do Meta Matrícula',
    'finalidade': 'Finalidade',
    'acoes_planejadas': 'Ações a serem realizadas',
    'objetivo_desenvolvimento': 'Objetivo de Desenvolvimento (GAP)',
    'atividade_aprendizagem': 'Atividade de Aprendizagem',
    'descricao': 'Descrição'
}

POSITIVE_INDICATORS: List[str] = [
    'implementar', 'desenvolver', 'executar', 'realizar', 'concluir',
    'atingir', 'alcançar', 'obter', 'conseguir', 'finalizar',
    'criar', 'construir', 'estabelecer', 'melhorar', 'aprimorar'
]

NEGATIVE_INDICATORS: List[str] = [
    'não sei', 'talvez', 'pode ser', 'acho que', 'vou tentar',
    'espero', 'gostaria', 'pretendo', 'deveria', 'poderia'
]

SUPPORTED_ENCODINGS: List[str] = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
OUTPUT_ENCODING: str = 'utf-8'

BATCH_SIZE: int = 100
PROGRESS_INTERVAL: int = 50
