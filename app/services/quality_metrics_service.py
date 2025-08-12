"""
Serviço de métricas de qualidade.
Implementa algoritmos para calcular diferentes aspectos da qualidade de texto.
"""
from typing import Dict, List
from ..core.config import SMART_KEYWORDS, POSITIVE_INDICATORS, NEGATIVE_INDICATORS
from ..utils.text_utils import TextUtils


class QualityMetricsService:
    """Serviço para cálculo de métricas de qualidade de texto."""
    
    def __init__(self):
        self.smart_keywords = SMART_KEYWORDS
        self.positive_indicators = POSITIVE_INDICATORS
        self.negative_indicators = NEGATIVE_INDICATORS
    
    def calculate_clarity(self, text: str) -> float:
        """
        Calcula a clareza do texto baseado em comprimento e estrutura.
        
        Args:
            text: Texto para análise
            
        Returns:
            Score de clareza (0.0 a 1.0)
        """
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            words = TextUtils.tokenize(text)
            sentences = TextUtils.count_sentences(text)
            
            if not words or sentences == 0:
                return 0.0
            
            avg_word_length = TextUtils.calculate_avg_word_length(text)
            words_per_sentence = len(words) / sentences
            
            # Lógica de pontuação baseada em tamanho
            if len(words) < 3:
                return 0.2
            elif len(words) > 50:
                clarity_score = max(0.3, 1.0 - (words_per_sentence - 10) * 0.02)
            else:
                clarity_score = min(1.0, 0.5 + (len(words) * 0.05))
            
            # Penaliza palavras muito longas
            if avg_word_length > 8:
                clarity_score *= 0.9
            
            return max(0.0, min(1.0, clarity_score))
            
        except Exception:
            return 0.3
    
    def calculate_specificity(self, text: str) -> float:
        """
        Calcula a especificidade do texto baseado em termos técnicos e números.
        
        Args:
            text: Texto para análise
            
        Returns:
            Score de especificidade (0.0 a 1.0)
        """
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            words = TextUtils.tokenize(text)
            
            if len(words) < 3:
                return 0.1
            
            # Palavras específicas (mais de 4 caracteres)
            specific_words = sum(1 for word in words if len(word) > 4)
            
            # Números e termos técnicos
            numbers_count = TextUtils.count_numbers(text)
            technical_terms = TextUtils.extract_technical_terms(text)
            
            # Cálculo do score
            specificity_score = (specific_words / len(words)) * 0.6
            specificity_score += (numbers_count * 0.1)
            specificity_score += (len(technical_terms) * 0.15)
            
            return max(0.0, min(1.0, specificity_score))
            
        except Exception:
            return 0.3
    
    def calculate_completeness(self, text: str) -> float:
        """
        Calcula a completude do texto baseado em ações e contexto.
        
        Args:
            text: Texto para análise
            
        Returns:
            Score de completude (0.0 a 1.0)
        """
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            words = TextUtils.tokenize(text)
            word_count_score = min(1.0, len(words) / 20)  # Ideal ~20 palavras
            
            # Verifica elementos de completude
            has_action = any(
                word in text.lower() for word in self.positive_indicators
            )
            has_context = len(words) > 5
            has_specifics = TextUtils.has_numbers(text) or len(words) > 10
            
            # Cálculo do score
            completeness_score = word_count_score * 0.5
            
            if has_action:
                completeness_score += 0.2
            if has_context:
                completeness_score += 0.2
            if has_specifics:
                completeness_score += 0.1
            
            return max(0.0, min(1.0, completeness_score))
            
        except Exception:
            return 0.3
    
    def calculate_structure(self, text: str) -> float:
        """
        Calcula a qualidade da estrutura do texto.
        
        Args:
            text: Texto para análise
            
        Returns:
            Score de estrutura (0.0 a 1.0)
        """
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            words = TextUtils.tokenize(text)
            sentences = TextUtils.count_sentences(text)
            
            # Verifica elementos estruturais
            has_punctuation = TextUtils.has_punctuation(text)
            has_proper_case = TextUtils.has_proper_case(text)
            
            # Score base
            structure_score = 0.3
            
            if has_punctuation:
                structure_score += 0.2
            if has_proper_case:
                structure_score += 0.1
            if sentences > 1:
                structure_score += 0.2
            if 5 <= len(words) <= 30:
                structure_score += 0.2
            
            return max(0.0, min(1.0, structure_score))
            
        except Exception:
            return 0.3
    
    def calculate_smart_criteria(self, text: str) -> float:
        """
        Calcula a presença de critérios SMART no texto.
        
        Args:
            text: Texto para análise
            
        Returns:
            Score de critérios SMART (0.0 a 1.0)
        """
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            text_lower = text.lower()
            smart_score = 0.0
            
            # Verifica cada categoria SMART
            for category, keywords in self.smart_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    smart_score += 0.2
            
            return max(0.0, min(1.0, smart_score))
            
        except Exception:
            return 0.2
    
    def calculate_negative_impact(self, text: str) -> float:
        """
        Calcula o impacto negativo de indicadores de incerteza.
        
        Args:
            text: Texto para análise
            
        Returns:
            Score de impacto negativo (0.0 a 1.0, onde 1.0 é totalmente negativo)
        """
        if not text:
            return 0.0
        
        text_lower = text.lower()
        negative_count = sum(
            1 for indicator in self.negative_indicators
            if indicator in text_lower
        )
        
        # Normaliza o impacto
        max_negative = len(self.negative_indicators)
        return min(1.0, negative_count / max_negative)
    
    def calculate_overall_quality(
        self, 
        text: str, 
        weights: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calcula a qualidade geral do texto usando todas as métricas.
        
        Args:
            text: Texto para análise
            weights: Pesos para cada métrica
            
        Returns:
            Dicionário com scores individuais e geral
        """
        # Calcula métricas individuais
        clarity = self.calculate_clarity(text)
        specificity = self.calculate_specificity(text)
        completeness = self.calculate_completeness(text)
        structure = self.calculate_structure(text)
        smart_criteria = self.calculate_smart_criteria(text)
        
        # Aplica impacto negativo
        negative_impact = self.calculate_negative_impact(text)
        
        # Ajusta scores com impacto negativo
        if negative_impact > 0:
            reduction_factor = 1 - (negative_impact * 0.3)  # Redução máxima de 30%
            clarity *= reduction_factor
            specificity *= reduction_factor
            completeness *= reduction_factor
        
        # Calcula score geral ponderado
        overall_score = (
            clarity * weights.get('clarity', 0.25) +
            specificity * weights.get('specificity', 0.25) +
            completeness * weights.get('completeness', 0.25) +
            structure * weights.get('structure', 0.15) +
            smart_criteria * weights.get('smart_criteria', 0.10)
        )
        
        return {
            'clarity_score': clarity,
            'specificity_score': specificity,
            'completeness_score': completeness,
            'structure_score': structure,
            'smart_criteria_score': smart_criteria,
            'overall_score': overall_score,
            'negative_impact': negative_impact
        }
