from typing import Dict, List
from ..core.config import POSITIVE_INDICATORS, NEGATIVE_INDICATORS
from ..utils.text_utils import TextUtils

# Importação condicional do cache para performance
try:
    from ..core.performance_cache import cached_metric, cached_tokenize, cached_sentence_count, cached_avg_word_length
    CACHE_AVAILABLE = True
except ImportError:
    # Fallback se cache não estiver disponível
    CACHE_AVAILABLE = False
    def cached_metric(method_name):
        def decorator(func):
            return func
        return decorator


class QualityMetricsService:
    
    def __init__(self, enable_cache: bool = True):
        self.positive_indicators = POSITIVE_INDICATORS
        self.negative_indicators = NEGATIVE_INDICATORS
        self.cache_enabled = enable_cache and CACHE_AVAILABLE
    
    @cached_metric('clarity')
    def calculate_clarity(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            if self.cache_enabled:
                words = list(cached_tokenize(text))
                sentences = cached_sentence_count(text)
                avg_word_length = cached_avg_word_length(text)
            else:
                words = TextUtils.tokenize(text)
                sentences = TextUtils.count_sentences(text)
                avg_word_length = TextUtils.calculate_avg_word_length(text)
            
            if not words or sentences == 0:
                return 0.0
            
            words_per_sentence = len(words) / sentences
            
            if len(words) < 3:
                return 0.2
            elif len(words) > 50:
                clarity_score = max(0.3, 1.0 - (words_per_sentence - 10) * 0.02)
            else:
                clarity_score = min(1.0, 0.5 + (len(words) * 0.05))
            
            if avg_word_length > 8:
                clarity_score *= 0.8
            
            if TextUtils.has_proper_case(text):
                clarity_score *= 1.1
            
            if TextUtils.has_punctuation(text):
                clarity_score *= 1.05
            
            return min(1.0, clarity_score)
            
        except Exception:
            return 0.0
    
    @cached_metric('specificity')
    def calculate_specificity(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            specificity_score = 0.1
            
            if TextUtils.has_numbers(text):
                specificity_score += 0.3
                number_count = TextUtils.count_numbers(text)
                specificity_score += min(0.2, number_count * 0.05)
            
            technical_terms = TextUtils.extract_technical_terms(text)
            if technical_terms:
                specificity_score += min(0.3, len(technical_terms) * 0.1)
            
            keywords = ['específico', 'detalhado', 'preciso', 'exato', 'claro']
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    specificity_score += 0.1
            
            return min(1.0, specificity_score)
            
        except Exception:
            return 0.0
    
    @cached_metric('completeness')
    def calculate_completeness(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            if self.cache_enabled:
                words = list(cached_tokenize(text))
                sentences = cached_sentence_count(text)
                word_count = len(words)
                sentence_count = sentences
            else:
                word_count = TextUtils.count_words(text)
                sentence_count = TextUtils.count_sentences(text)
            
            if word_count < 5:
                return 0.1
            
            completeness_score = min(0.6, word_count * 0.02)
            
            completeness_score += min(0.2, sentence_count * 0.05)
            
            important_elements = ['quando', 'como', 'onde', 'o que', 'por que', 'quem']
            for element in important_elements:
                if element.lower() in text.lower():
                    completeness_score += 0.05
            
            if len(text) > 100:
                completeness_score += 0.1
            
            return min(1.0, completeness_score)
            
        except Exception:
            return 0.0
    
    def calculate_negative_impact(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            negative_score = 0.0
            text_lower = text.lower()
            
            for indicator in self.negative_indicators:
                if indicator.lower() in text_lower:
                    negative_score += 0.1
            
            return min(0.5, negative_score)
            
        except Exception:
            return 0.0
    
    def calculate_overall_quality(self, clarity: float, specificity: float, 
                                completeness: float) -> Dict[str, float]:
        """
        Calcula a qualidade geral do PDI com base nos critérios principais.
        
        Critérios rebalanceados (3 critérios):
        - Clareza: 35%
        - Especificidade: 35% 
        - Completude: 30%
        """
        weights = {
            'clarity': 0.35,        # 35%
            'specificity': 0.35,    # 35%
            'completeness': 0.30    # 30%
        }
        
        overall_score = (
            clarity * weights['clarity'] +
            specificity * weights['specificity'] +
            completeness * weights['completeness']
        )
        
        if overall_score >= 0.6:
            quality_level = 'Alta'
        elif overall_score >= 0.3:
            quality_level = 'Média'
        else:
            quality_level = 'Baixa'
        
        return {
            'overall_score': overall_score,
            'quality_level': quality_level,
            'clarity_score': clarity,
            'specificity_score': specificity,
            'completeness_score': completeness
        }
    
    def generate_score_explanation(self, clarity: float, specificity: float, 
                                 completeness: float, 
                                 negative_impact: float = 0.0) -> str:
        """
        Gera uma explicação detalhada de como a nota foi calculada
        
        Pesos rebalanceados (3 critérios):
        - Clareza: 35%
        - Especificidade: 35%
        - Completude: 30%
        """
        weights = {
            'clarity': 0.35,        # 35%
            'specificity': 0.35,    # 35%
            'completeness': 0.30    # 30%
        }
        
        # Calcular contribuições de cada critério
        contributions = {
            'Clareza': clarity * weights['clarity'] * 100,
            'Especificidade': specificity * weights['specificity'] * 100,
            'Completude': completeness * weights['completeness'] * 100
        }
        
        total_score = sum(contributions.values())
        
        # Ajustar por impacto negativo
        if negative_impact > 0:
            penalty = negative_impact * 10
            total_score = max(0, total_score - penalty)
        
        explanation = f"\n{'='*60}\n"
        explanation += "📊 DETALHAMENTO DA AVALIAÇÃO\n"
        explanation += f"{'='*60}\n\n"
        
        explanation += f"🎯 NOTA FINAL: {total_score:.1f}/100\n\n"
        
        explanation += "📋 BREAKDOWN POR CRITÉRIO:\n"
        explanation += "-" * 40 + "\n"
        
        for criterion, score in contributions.items():
            weight_pct = {
                'Clareza': 35.0,
                'Especificidade': 35.0, 
                'Completude': 30.0
            }[criterion]
            
            raw_score = score / weight_pct * 100
            
            explanation += f"• {criterion:15} ({weight_pct:4.1f}%): {score:5.1f} pontos "
            explanation += f"(base: {raw_score:.1f}/100)\n"
        
        if negative_impact > 0:
            explanation += f"\n⚠️  PENALIDADES:\n"
            explanation += f"• Indicadores negativos: -{negative_impact * 10:.1f} pontos\n"
        
        explanation += f"\n🔍 ANÁLISE DETALHADA:\n"
        explanation += "-" * 40 + "\n"
        
        # Análise por critério
        if clarity >= 0.8:
            explanation += "✅ CLAREZA (EXCELENTE): Texto muito claro e compreensível\n"
        elif clarity >= 0.6:
            explanation += "✅ CLAREZA (BOA): Texto claro com pequenos ajustes possíveis\n"
        elif clarity >= 0.4:
            explanation += "⚠️  CLAREZA (REGULAR): Texto necessita melhorar clareza\n"
        else:
            explanation += "❌ CLAREZA (BAIXA): Texto confuso, necessita reescrita\n"
        
        if specificity >= 0.8:
            explanation += "✅ ESPECIFICIDADE (EXCELENTE): Muito específico e detalhado\n"
        elif specificity >= 0.6:
            explanation += "✅ ESPECIFICIDADE (BOA): Razoavelmente específico\n"
        elif specificity >= 0.4:
            explanation += "⚠️  ESPECIFICIDADE (REGULAR): Falta mais detalhes específicos\n"
        else:
            explanation += "❌ ESPECIFICIDADE (BAIXA): Muito vago, adicionar detalhes\n"
        
        if completeness >= 0.8:
            explanation += "✅ COMPLETUDE (EXCELENTE): Informações muito completas\n"
        elif completeness >= 0.6:
            explanation += "✅ COMPLETUDE (BOA): Informações adequadas\n"
        elif completeness >= 0.4:
            explanation += "⚠️  COMPLETUDE (REGULAR): Faltam algumas informações\n"
        else:
            explanation += "❌ COMPLETUDE (BAIXA): Informações insuficientes\n"
        
        # SMART removido das explicações - não é mais usado no cálculo
        
        explanation += f"\n🎯 CLASSIFICAÇÃO GERAL:\n"
        if total_score >= 80:
            explanation += "🌟 EXCELENTE - PDI de alta qualidade\n"
        elif total_score >= 60:
            explanation += "✅ BOM - PDI de boa qualidade\n"
        elif total_score >= 40:
            explanation += "⚠️  REGULAR - PDI necessita melhorias\n"
        else:
            explanation += "❌ INADEQUADO - PDI necessita reescrita\n"
        
        explanation += f"\n{'='*60}\n"
        
        return explanation
    
    def generate_concise_reasons(self, clarity: float, specificity: float, 
                                completeness: float, 
                                negative_impact: float = 0.0,
                                overall_score: float = 0.0) -> dict:
        """
        Gera 3 motivos concisos e diretos para a nota recebida
        Sem emojis, sem textos longos - apenas os pontos principais
        
        Critérios rebalanceados (3 critérios):
        - Clareza: 35%
        - Especificidade: 35%
        - Completude: 30%
        """
        # Calcular nota final se não fornecida
        if overall_score == 0.0:
            weights = {
                'clarity': 0.35,        # 35%
                'specificity': 0.35,    # 35%
                'completeness': 0.30    # 30%
            }
            
            overall_score = (
                clarity * weights['clarity'] +
                specificity * weights['specificity'] +
                completeness * weights['completeness']
            ) * 100
            
            if negative_impact > 0:
                overall_score = max(0, overall_score - (negative_impact * 10))
        
        # Identificar os 3 principais problemas/pontos fortes
        criteria_scores = {
            'clareza': clarity,
            'especificidade': specificity,
            'completude': completeness
        }
        
        # Ordenar critérios por pontuação (do menor para o maior)
        sorted_criteria = sorted(criteria_scores.items(), key=lambda x: x[1])
        
        motivos = []
        
        # Analisar os 3 critérios com menor pontuação para identificar problemas
        for criterio, score in sorted_criteria[:3]:
            if criterio == 'clareza':
                if score < 0.4:
                    motivos.append("Objetivo muito vago e confuso")
                elif score < 0.7:
                    motivos.append("Objetivo precisa ser mais claro")
                else:
                    motivos.append("Clareza adequada")
            
            elif criterio == 'especificidade':
                if score < 0.4:
                    motivos.append("Faltam detalhes específicos e números")
                elif score < 0.7:
                    motivos.append("Precisa mais detalhes específicos")
                else:
                    motivos.append("Especificidade adequada")
            
            elif criterio == 'completude':
                if score < 0.4:
                    motivos.append("Informações muito incompletas")
                elif score < 0.7:
                    motivos.append("Faltam informações importantes")
                else:
                    motivos.append("Informações suficientes")
            
            elif criterio == 'estrutura':
                if score < 0.4:
                    motivos.append("Texto mal organizado")
                elif score < 0.7:
                    motivos.append("Estrutura pode melhorar")
                else:
                    motivos.append("Bem estruturado")
        
        # Se a nota é muito baixa, focar nos problemas mais críticos
        if overall_score < 40:
            motivos = [
                "Objetivo extremamente vago",
                "Faltam detalhes essenciais",
                "Não especifica como executar"
            ]
        
        # Se a nota é boa, focar nos pontos de melhoria
        elif overall_score >= 70:
            # Para notas altas, identificar pequenos ajustes
            lowest_criteria = sorted_criteria[0]
            if lowest_criteria[1] < 0.8:  # Se o critério mais baixo ainda pode melhorar
                if lowest_criteria[0] == 'especificidade':
                    motivos[0] = "Pode adicionar mais números e datas"
                elif lowest_criteria[0] == 'completude':
                    motivos[0] = "Pode detalhar mais as ações"
                elif lowest_criteria[0] == 'clareza':
                    motivos[0] = "Pode ser mais direto e claro"
            else:
                motivos[0] = "PDI de boa qualidade geral"
        
        # Considerar impacto negativo
        if negative_impact > 0.1:
            motivos[-1] = "Contém termos negativos ou vagos"
        
        # Garantir que temos exatamente 3 motivos
        while len(motivos) < 3:
            motivos.append("Análise complementar necessária")
        
        # Limitar a 3 motivos
        motivos = motivos[:3]
        
        return {
            'motivo_1': motivos[0],
            'motivo_2': motivos[1],
            'motivo_3': motivos[2]
        }
