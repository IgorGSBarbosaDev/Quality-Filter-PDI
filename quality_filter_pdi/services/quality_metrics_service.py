from typing import Dict, List
from ..core.config import SMART_KEYWORDS, POSITIVE_INDICATORS, NEGATIVE_INDICATORS
from ..utils.text_utils import TextUtils


class QualityMetricsService:
    
    def __init__(self):
        self.smart_keywords = SMART_KEYWORDS
        self.positive_indicators = POSITIVE_INDICATORS
        self.negative_indicators = NEGATIVE_INDICATORS
    
    def calculate_clarity(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            words = TextUtils.tokenize(text)
            sentences = TextUtils.count_sentences(text)
            
            if not words or sentences == 0:
                return 0.0
            
            avg_word_length = TextUtils.calculate_avg_word_length(text)
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
    
    def calculate_completeness(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
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
    
    def calculate_structure(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            structure_score = 0.2
            
            connectors = ['e', 'mas', 'porém', 'então', 'assim', 'portanto', 'além disso']
            for connector in connectors:
                if connector.lower() in text.lower():
                    structure_score += 0.1
            
            if TextUtils.has_proper_case(text):
                structure_score += 0.2
            
            if TextUtils.has_punctuation(text):
                structure_score += 0.2
            
            sentences = TextUtils.count_sentences(text)
            if sentences > 1:
                structure_score += min(0.3, sentences * 0.1)
            
            return min(1.0, structure_score)
            
        except Exception:
            return 0.0
    
    def calculate_smart_criteria(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            smart_score = 0.0
            text_lower = text.lower()
            
            for category, keywords in self.smart_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        smart_score += 0.15
                        break
            
            return min(1.0, smart_score)
            
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
                                completeness: float, structure: float, 
                                smart_criteria: float) -> Dict[str, float]:
        weights = {
            'clarity': 0.25,
            'specificity': 0.25,
            'completeness': 0.25,
            'structure': 0.15,
            'smart_criteria': 0.10
        }
        
        overall_score = (
            clarity * weights['clarity'] +
            specificity * weights['specificity'] +
            completeness * weights['completeness'] +
            structure * weights['structure'] +
            smart_criteria * weights['smart_criteria']
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
            'completeness_score': completeness,
            'structure_score': structure,
            'smart_criteria_score': smart_criteria
        }
