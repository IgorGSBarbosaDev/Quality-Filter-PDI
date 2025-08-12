import re
from typing import Dict, List, Tuple, Any
from .text_processor import TextProcessor
from config.settings import (
    SMART_KEYWORDS, NEGATIVE_INDICATORS, POSITIVE_INDICATORS,
    MIN_WORD_COUNT, MIN_SENTENCE_COUNT
)


class QualityMetrics:
    def __init__(self) -> None:
        self.text_processor = TextProcessor()
    
    def calculate_clarity_score(self, text: str) -> float:
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        metrics = self.text_processor.extract_metrics(text)
        
        readability_score = metrics['readability']
        
        negative_count = self.text_processor.count_keywords(text, NEGATIVE_INDICATORS)
        positive_count = self.text_processor.count_keywords(text, POSITIVE_INDICATORS)
        
        word_count = max(1, metrics['word_count'])
        indicator_score = max(0, min(1, (positive_count - negative_count * 2) / word_count + 0.5))
        
        structure_score = self._calculate_structure_score(metrics)
        
        return 0.4 * readability_score + 0.4 * indicator_score + 0.2 * structure_score
    
    def calculate_specificity_score(self, text: str) -> float:
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        metrics = self.text_processor.extract_metrics(text)
        
        words = self.text_processor.tokenize_words(text)
        unique_words = len(set(words))
        total_words = len(words)
        
        density_score = unique_words / max(1, total_words) if total_words > 0 else 0
        
        specificity_patterns = [
            r'\d+%', r'\d+\s*(dias?|semanas?|meses?|anos?)',
            r'\d+\s*(horas?|minutos?)', r'\d+'
        ]
        
        specificity_count = sum(
            len(re.findall(pattern, text, re.IGNORECASE)) 
            for pattern in specificity_patterns
        )
        
        specificity_score = min(1.0, specificity_count / max(1, metrics['sentence_count']))
        length_score = min(1.0, metrics['avg_word_length'] / 6.0)
        
        return 0.4 * density_score + 0.4 * specificity_score + 0.2 * length_score
    
    def calculate_completeness_score(self, text: str) -> float:
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        metrics = self.text_processor.extract_metrics(text)
        
        word_score = min(1.0, metrics['word_count'] / MIN_WORD_COUNT)
        sentence_score = min(1.0, metrics['sentence_count'] / MIN_SENTENCE_COUNT)
        
        essential_aspects = ['como', 'quando', 'onde', 'por que', 'o que']
        coverage_score = sum(
            1 for aspect in essential_aspects 
            if self.text_processor.has_keywords(text, [aspect])
        ) / len(essential_aspects)
        
        return 0.4 * word_score + 0.3 * sentence_score + 0.3 * coverage_score
    
    def calculate_smart_score(self, text: str) -> float:
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        smart_scores = {}
        
        for criterion, keywords in SMART_KEYWORDS.items():
            keyword_count = self.text_processor.count_keywords(text, keywords)
            sentences = max(1, self.text_processor.get_sentence_count(text))
            smart_scores[criterion] = min(1.0, keyword_count / sentences)
        
        return sum(smart_scores.values()) / len(smart_scores)
    
    def _calculate_structure_score(self, metrics: Dict[str, Any]) -> float:
        if metrics['sentence_count'] == 0:
            return 0.0
        
        avg_sentence_length = metrics['avg_sentence_length']
        
        if avg_sentence_length < 5 or avg_sentence_length > 25:
            length_score = 0.5
        else:
            length_score = 1.0
        
        sentence_score = min(1.0, metrics['sentence_count'] / 3)
        
        return 0.6 * length_score + 0.4 * sentence_score
    
    def calculate_overall_quality(
        self, 
        acoes_text: str, 
        objetivo_text: str, 
        weights: Dict[str, float]
    ) -> Dict[str, Any]:
        acoes_metrics = {
            'clarity': self.calculate_clarity_score(acoes_text),
            'specificity': self.calculate_specificity_score(acoes_text),
            'completeness': self.calculate_completeness_score(acoes_text),
            'smart': self.calculate_smart_score(acoes_text)
        }
        
        objetivo_metrics = {
            'clarity': self.calculate_clarity_score(objetivo_text),
            'specificity': self.calculate_specificity_score(objetivo_text),
            'completeness': self.calculate_completeness_score(objetivo_text),
            'smart': self.calculate_smart_score(objetivo_text)
        }
        
        combined_metrics = {}
        for metric in acoes_metrics:
            combined_metrics[metric] = (
                0.6 * acoes_metrics[metric] + 0.4 * objetivo_metrics[metric]
            )
        
        combined_text = f"{acoes_text} {objetivo_text}"
        combined_metrics['structure'] = self._calculate_structure_score(
            self.text_processor.extract_metrics(combined_text)
        )
        
        final_score = sum(
            combined_metrics[metric] * weights.get(metric, 0) 
            for metric in combined_metrics
        )
        
        return {
            'score': final_score,
            'metrics': combined_metrics,
            'acoes_metrics': acoes_metrics,
            'objetivo_metrics': objetivo_metrics
        }
