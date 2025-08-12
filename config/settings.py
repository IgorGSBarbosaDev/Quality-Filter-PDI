from typing import Dict, List

MIN_WORD_COUNT = 10
MIN_SENTENCE_COUNT = 2

QUALITY_THRESHOLDS = {
    'low': 0.3,
    'medium': 0.6,
    'high': 0.8
}

METRIC_WEIGHTS = {
    'clarity': 0.25,
    'specificity': 0.25,
    'completeness': 0.25,
    'structure': 0.15,
    'smart_criteria': 0.10
}

EXCEL_COLUMNS = {
    'nome': 'Nome',
    'matricula': 'Matrícula',
    'finalidade': 'Finalidade do objetivo',
    'acoes_planejadas': 'Ações planejadas',
    'objetivo_desenvolvimento': 'Objetivo de desenvolvimento'
}

SMART_KEYWORDS: Dict[str, List[str]] = {
    'specific': ['específico', 'especifica', 'claro', 'preciso', 'definido', 'detalhado'],
    'measurable': ['medir', 'mensurar', 'métrica', 'indicador', 'quantidade', 'percentual', '%', 'prazo'],
    'achievable': ['possível', 'viável', 'realista', 'alcançável', 'factível'],
    'relevant': ['importante', 'relevante', 'necessário', 'estratégico', 'essencial'],
    'time_bound': ['prazo', 'até', 'em', 'durante', 'mês', 'ano', 'trimestre', 'semestre', 'data']
}

NEGATIVE_INDICATORS: List[str] = [
    'não sei', 'talvez', 'pode ser', 'acho que', 'vou tentar',
    'espero', 'gostaria', 'pretendo', 'deveria', 'poderia'
]

POSITIVE_INDICATORS: List[str] = [
    'implementar', 'desenvolver', 'executar', 'realizar', 'concluir',
    'atingir', 'alcançar', 'obter', 'conseguir', 'finalizar'
]
