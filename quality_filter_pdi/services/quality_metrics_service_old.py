"""
Serviço de métricas de qualidade para análise de PDI.

Este módulo contém a lógica principal para calcular métricas de qualidade
de textos PDI, incluindo clareza, especificidade, completude e coesão.
Suporta análise tradicional e com IA avançada.
"""

from typing import Dict, List, Optional, Tuple, Union
import logging
from dataclasses import dataclass

from ..core.config import (
    POSITIVE_INDICATORS, NEGATIVE_INDICATORS, METRIC_WEIGHTS, 
    QualityLevel, AnalysisMethod
)
from ..utils.text_utils import TextUtils

# Configurar logging
logger = logging.getLogger(__name__)

# Importação condicional do cache para performance
try:
    from ..core.performance_cache import (
        cached_metric, cached_tokenize, cached_sentence_count, cached_avg_word_length
    )
    CACHE_AVAILABLE = True
    logger.info("Cache de performance carregado")
except ImportError:
    CACHE_AVAILABLE = False
    logger.warning("Cache de performance não disponível")
    
    # Fallback para decorador vazio
    def cached_metric(method_name):
        def decorator(func):
            return func
        return decorator

# Importação condicional da IA
try:
    from ..ai.advanced_ai_analyzer import AdvancedAIAnalyzer
    AI_AVAILABLE = True
    logger.info("Módulo de IA avançada disponível")
except ImportError:
    AI_AVAILABLE = False
    logger.warning("Módulo de IA avançada não disponível")


@dataclass
class QualityMetrics:
    """Classe para representar métricas de qualidade."""
    clarity: float
    specificity: float
    completeness: float
    overall_score: float
    quality_level: str
    suggestions: List[str]


@dataclass
class CohesionResult:
    """Classe para representar resultado de análise de coesão."""
    score: float
    level: str
    method: str
    ai_enabled: bool
    used_fields: List[str]
    details: Optional[Dict] = None


class QualityMetricsService:
    """
    Serviço responsável por calcular métricas de qualidade de PDI.
    
    Fornece análise de clareza, especificidade, completude e coesão,
    com suporte opcional a IA avançada.
    """
    
    def __init__(self, enable_cache: bool = True, enable_ai: bool = True):
        """
        Inicializa o serviço de métricas de qualidade.
        
        Args:
            enable_cache: Ativar cache de performance
            enable_ai: Ativar análise com IA avançada
        """
        self.positive_indicators = POSITIVE_INDICATORS
        self.negative_indicators = NEGATIVE_INDICATORS
        self.cache_enabled = enable_cache and CACHE_AVAILABLE
        
        # Inicializar IA se disponível e solicitado
        self.ai_enabled = enable_ai and AI_AVAILABLE
        self.ai_analyzer = None
        
        if self.ai_enabled:
            try:
                self.ai_analyzer = AdvancedAIAnalyzer()
                logger.info("IA carregada para análise de coesão avançada")
            except Exception as e:
                logger.warning(f"Erro ao carregar IA: {e}")
                self.ai_enabled = False
        
        logger.info(f"QualityMetricsService inicializado (Cache: {self.cache_enabled}, IA: {self.ai_enabled})")
    
    def _get_tokenization_data(self, text: str) -> Tuple[List[str], int, float]:
        """
        Obtém dados de tokenização (com cache se disponível).
        
        Returns:
            Tuple com (palavras, número_sentenças, comprimento_médio_palavra)
        """
        if self.cache_enabled:
            words = list(cached_tokenize(text))
            sentences = cached_sentence_count(text)
            avg_word_length = cached_avg_word_length(text)
        else:
            words = TextUtils.tokenize(text)
            sentences = TextUtils.count_sentences(text)
            avg_word_length = TextUtils.calculate_avg_word_length(text)
        
        return words, sentences, avg_word_length
    
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
    
    @cached_metric('goal_cohesion')
    def calculate_goal_cohesion(self, objetivo: str, acoes: str, atividades: str = "") -> Dict[str, float]:
        """
        Avalia a coesão entre o objetivo de desenvolvimento e as ações/atividades planejadas.
        
        Utiliza IA avançada quando disponível, ou análise tradicional como fallback.
        
        Args:
            objetivo: Texto do objetivo de desenvolvimento
            acoes: Texto das ações a serem realizadas  
            atividades: Texto das atividades de aprendizagem (opcional)
            
        Returns:
            Dict com score numérico, classificação textual e metadados de análise
        """
        # Usar IA se disponível
        if self.ai_enabled and self.ai_analyzer:
            try:
                ai_result = self.ai_analyzer.analyze_goal_cohesion_ai(objetivo, acoes, atividades)
                
                # Adicionar metadados sobre o tipo de análise
                ai_result['analysis_method'] = 'AI_ADVANCED'
                ai_result['ai_enabled'] = True
                
                return ai_result
                
            except Exception as e:
                print(f"⚠️ Erro na análise AI, usando fallback: {e}")
                # Continuar com análise tradicional em caso de erro
        
        # Análise tradicional (fallback ou quando IA não está disponível)
        return self._traditional_cohesion_analysis(objetivo, acoes, atividades)
    
    def _traditional_cohesion_analysis(self, objetivo: str, acoes: str, atividades: str = "") -> Dict[str, float]:
        """
        Análise tradicional de coesão (fallback quando IA não está disponível).
        
        Args:
            objetivo: Texto do objetivo de desenvolvimento
            acoes: Texto das ações a serem realizadas  
            atividades: Texto das atividades de aprendizagem (opcional)
            
        Returns:
            Dict com score numérico e classificação textual
        """
        if not objetivo:
            return {
                'cohesion_score': 0.0,
                'cohesion_level': 'muito ruim',
                'analysis_method': 'TRADITIONAL',
                'ai_enabled': False
            }
        
        # Normalizar textos
        objetivo_clean = TextUtils.clean_text(objetivo.lower())
        acoes_clean = TextUtils.clean_text(acoes.lower()) if acoes and acoes.strip() else ""
        atividades_clean = TextUtils.clean_text(atividades.lower()) if atividades and atividades.strip() else ""
        
        # Lógica inteligente: considerar apenas campos com conteúdo
        campos_com_conteudo = []
        
        if acoes_clean:
            campos_com_conteudo.append(acoes_clean)
        
        if atividades_clean:
            campos_com_conteudo.append(atividades_clean)
        
        # Se nenhum campo tem conteúdo, retorna score muito baixo
        if not campos_com_conteudo:
            return {
                'cohesion_score': 0.0,
                'cohesion_level': 'muito ruim',
                'analysis_method': 'TRADITIONAL',
                'ai_enabled': False
            }
        
        # Combinar apenas os campos que têm conteúdo
        acoes_atividades_combined = " ".join(campos_com_conteudo).strip()
        
        # Extrair palavras-chave do objetivo
        objetivo_keywords = set(TextUtils.tokenize(objetivo_clean))
        objetivo_keywords = {word for word in objetivo_keywords if len(word) > 3}
        
        # Extrair palavras-chave das ações e atividades (apenas campos com conteúdo)
        action_keywords = set(TextUtils.tokenize(acoes_atividades_combined))
        action_keywords = {word for word in action_keywords if len(word) > 3}
        
        if not objetivo_keywords or not action_keywords:
            return {
                'cohesion_score': 0.1,
                'cohesion_level': 'muito ruim',
                'analysis_method': 'TRADITIONAL',
                'ai_enabled': False
            }
        
        # Calcular overlap de palavras-chave
        intersection = objetivo_keywords.intersection(action_keywords)
        union = objetivo_keywords.union(action_keywords)
        
        keyword_overlap = len(intersection) / len(union) if union else 0
        
        # Verificar alinhamento semântico básico
        # Palavras relacionadas a desenvolvimento e aprendizagem
        development_terms = {
            'desenvolver', 'melhorar', 'aprender', 'estudar', 'capacitar',
            'treinar', 'praticar', 'dominar', 'adquirir', 'habilidade',
            'competencia', 'conhecimento', 'skill', 'curso', 'treinamento'
        }
        
        objetivo_has_dev = any(term in objetivo_clean for term in development_terms)
        acoes_has_dev = any(term in acoes_atividades_combined for term in development_terms)
        
        semantic_alignment = 0.3 if (objetivo_has_dev and acoes_has_dev) else 0.0
        
        # Verificar consistência de domínio/área
        # Termos técnicos que podem indicar área específica
        tech_terms = {
            'python', 'programacao', 'software', 'gestao', 'lideranca',
            'vendas', 'marketing', 'financeiro', 'operacional', 'tecnico',
            'comunicacao', 'apresentacao', 'analise', 'dados', 'excel'
        }
        
        objetivo_tech = {term for term in tech_terms if term in objetivo_clean}
        acoes_tech = {term for term in tech_terms if term in acoes_atividades_combined}
        
        domain_consistency = 0.0
        if objetivo_tech and acoes_tech:
            domain_overlap = len(objetivo_tech.intersection(acoes_tech))
            domain_consistency = domain_overlap / max(len(objetivo_tech), len(acoes_tech))
        
        # Verificar especificidade das ações em relação ao objetivo
        specificity_bonus = 0.0
        if len(acoes_atividades_combined) > len(objetivo_clean) * 0.8:  # Ações detalhadas
            specificity_bonus = 0.1
        
        # Calcular score final
        final_score = (
            keyword_overlap * 0.4 +           # 40% - overlap de palavras-chave
            semantic_alignment * 0.3 +        # 30% - alinhamento semântico
            domain_consistency * 0.2 +        # 20% - consistência de domínio
            specificity_bonus * 0.1           # 10% - especificidade
        )
        
        # Garantir que o score esteja entre 0 e 1
        final_score = max(0.0, min(1.0, final_score))
        
        # Classificar em níveis
        if final_score >= 0.8:
            level = 'otimo'
        elif final_score >= 0.6:
            level = 'bom'
        elif final_score >= 0.4:
            level = 'medio'
        elif final_score >= 0.2:
            level = 'ruim'
        else:
            level = 'muito ruim'
        
        return {
            'cohesion_score': final_score,
            'cohesion_level': level,
            'analysis_method': 'TRADITIONAL',
            'ai_enabled': False
        }
    
    @cached_metric('overall_quality')
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
            'clarity': 0.35,      # 35%
            'specificity': 0.35,  # 35%
            'completeness': 0.30  # 30%
        }
        
        overall_score = (
            clarity * weights['clarity'] +
            specificity * weights['specificity'] +
            completeness * weights['completeness']
        )
        
        return {
            'overall_score': overall_score,
            'clarity_score': clarity,
            'specificity_score': specificity,
            'completeness_score': completeness,
            'scores': {
                'overall_score': overall_score
            }
        }
    
    def generate_score_explanation (self, clarity: float, specificity: float,
        
        # Verificar especificidade das ações em relação ao objetivo
        specificity_bonus = 0.0
        if len(acoes_atividades_combined) > len(objetivo_clean) * 0.8:  # Ações detalhadas
            specificity_bonus = 0.1
        
        # Calcular score final
        final_score = (
            keyword_overlap * 0.4 +           # 40% - overlap de palavras-chave
            semantic_alignment * 0.3 +        # 30% - alinhamento semântico
            domain_consistency * 0.2 +        # 20% - consistência de domínio
            specificity_bonus * 0.1           # 10% - especificidade
        )
        
        # Garantir que o score esteja entre 0 e 1
        final_score = max(0.0, min(1.0, final_score))
        
        # Classificar em níveis
        if final_score >= 0.8:
            level = 'otimo'
        elif final_score >= 0.6:
            level = 'bom'
        elif final_score >= 0.4:
            level = 'medio'
        elif final_score >= 0.2:
            level = 'ruim'
        else:
            level = 'muito ruim'
        
        return {
            'cohesion_score': final_score,
            'cohesion_level': level
        }
    
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
