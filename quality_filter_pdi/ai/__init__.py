"""
🤖 Módulo de Inteligência Artificial - Quality Filter PDI
Analisadores de IA para análise semântica e processamento de linguagem natural
"""

# Importações condicionais de componentes de IA
def _safe_import(module_name: str, class_name: str = None):
    """Importação segura com fallback"""
    try:
        if class_name:
            from importlib import import_module
            full_module_name = f"{__name__}.{module_name}"
            module = import_module(full_module_name)
            return getattr(module, class_name)
        else:
            from importlib import import_module
            return import_module(f"{__name__}.{module_name}")
    except (ImportError, ModuleNotFoundError, AttributeError):
        return None

# Tentar importar cada componente de IA
SimpleAIAnalyzer = _safe_import('simple_ai_analyzer', 'SimpleAIAnalyzer')
AdvancedAIAnalyzer = _safe_import('advanced_ai_analyzer', 'AdvancedAIAnalyzer')
CloudAIAnalyzer = _safe_import('cloud_ai_analyzer', 'CloudAIAnalyzer')
AITextAnalyzer = _safe_import('ai_text_analyzer', 'AITextAnalyzer')

# Detectar quais componentes estão disponíveis
AVAILABLE_ANALYZERS = {}
if SimpleAIAnalyzer:
    AVAILABLE_ANALYZERS['simple'] = SimpleAIAnalyzer

if AdvancedAIAnalyzer:
    AVAILABLE_ANALYZERS['advanced'] = AdvancedAIAnalyzer

if CloudAIAnalyzer:
    AVAILABLE_ANALYZERS['cloud'] = CloudAIAnalyzer

if AITextAnalyzer:
    AVAILABLE_ANALYZERS['text'] = AITextAnalyzer

# Exports dinâmicos baseados em disponibilidade
__all__ = ["AVAILABLE_ANALYZERS"]

if SimpleAIAnalyzer:
    __all__.append("SimpleAIAnalyzer")

if AdvancedAIAnalyzer:
    __all__.append("AdvancedAIAnalyzer")

if CloudAIAnalyzer:
    __all__.append("CloudAIAnalyzer")

if AITextAnalyzer:
    __all__.append("AITextAnalyzer")

def get_best_analyzer():
    """Retorna o melhor analisador disponível"""
    # Ordem de preferência: advanced > cloud > simple > text
    preferences = ['advanced', 'cloud', 'simple', 'text']
    
    for pref in preferences:
        if pref in AVAILABLE_ANALYZERS:
            return AVAILABLE_ANALYZERS[pref]
    
    return None

def list_available_analyzers() -> list:
    """Lista analisadores disponíveis"""
    return list(AVAILABLE_ANALYZERS.keys())

__all__.extend(["get_best_analyzer", "list_available_analyzers"])