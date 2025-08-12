"""
Configurações do sistema de análise de PDI
"""

# Configurações de análise
ANALYSIS_CONFIG = {
    'min_word_count': 10,
    'min_sentence_count': 2,
    'quality_thresholds': {
        'low': 0.3,
        'medium': 0.6,
        'high': 0.8
    }
}

# Pesos para diferentes métricas
METRIC_WEIGHTS = {
    'clarity': 0.25,
    'specificity': 0.25,
    'completeness': 0.25,
    'structure': 0.15,
    'smart_criteria': 0.10
}

# Configurações de colunas da planilha
EXCEL_COLUMNS = {
    'nome': 'Nome',
    'matricula': 'Matrícula',
    'finalidade': 'Finalidade do objetivo',
    'acoes_planejadas': 'Ações planejadas',
    'objetivo_desenvolvimento': 'Objetivo de desenvolvimento'
}

# Palavras-chave para análise SMART
SMART_KEYWORDS = {
    'specific': ['específico', 'especifica', 'claro', 'preciso', 'definido', 'detalhado'],
    'measurable': ['medir', 'mensurar', 'métrica', 'indicador', 'quantidade', 'percentual', '%', 'prazo'],
    'achievable': ['possível', 'viável', 'realista', 'alcançável', 'factível'],
    'relevant': ['importante', 'relevante', 'necessário', 'estratégico', 'essencial'],
    'time_bound': ['prazo', 'até', 'em', 'durante', 'mês', 'ano', 'trimestre', 'semestre', 'data']
}

# Palavras que indicam baixa qualidade
NEGATIVE_INDICATORS = [
    'não sei', 'talvez', 'pode ser', 'acho que', 'vou tentar',
    'espero', 'gostaria', 'pretendo', 'deveria', 'poderia'
]

# Palavras que indicam alta qualidade
POSITIVE_INDICATORS = [
    'implementar', 'desenvolver', 'executar', 'realizar', 'concluir',
    'atingir', 'alcançar', 'obter', 'conseguir', 'finalizar'
]
