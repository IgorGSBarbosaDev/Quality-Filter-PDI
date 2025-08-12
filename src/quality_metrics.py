"""
Métricas de qualidade para análise de PDI
"""
from typing import Dict, List, Tuple
from .text_processor import TextProcessor
from config.settings import SMART_KEYWORDS, NEGATIVE_INDICATORS, POSITIVE_INDICATORS, ANALYSIS_CONFIG

class QualityMetrics:
    def __init__(self):
        self.text_processor = TextProcessor()
    
    def calculate_clarity_score(self, text: str) -> float:
        """
        Calcula pontuação de clareza baseada em:
        - Legibilidade
        - Presença de palavras negativas/positivas
        - Estrutura das sentenças
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        metrics = self.text_processor.extract_metrics(text)
        
        # Componente de legibilidade (40%)
        readability_score = metrics['readability']
        
        # Componente de indicadores negativos/positivos (40%)
        negative_count = self.text_processor.count_keywords(text, NEGATIVE_INDICATORS)
        positive_count = self.text_processor.count_keywords(text, POSITIVE_INDICATORS)
        
        # Penaliza indicadores negativos e recompensa positivos
        word_count = max(1, metrics['word_count'])
        indicator_score = max(0, min(1, (positive_count - negative_count * 2) / word_count + 0.5))
        
        # Componente de estrutura (20%)
        structure_score = self._calculate_structure_score(metrics)
        
        return 0.4 * readability_score + 0.4 * indicator_score + 0.2 * structure_score
    
    def calculate_specificity_score(self, text: str) -> float:
        """
        Calcula pontuação de especificidade baseada em:
        - Densidade de informação
        - Presença de detalhes específicos
        - Uso de termos precisos
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        metrics = self.text_processor.extract_metrics(text)
        
        # Densidade de informação (palavras únicas / total)
        words = self.text_processor.tokenize_words(text)
        unique_words = len(set(words))
        total_words = len(words)
        
        density_score = unique_words / max(1, total_words) if total_words > 0 else 0
        
        # Presença de números e medidas específicas
        specificity_patterns = [
            r'\d+%',  # percentuais
            r'\d+\s*(dias?|semanas?|meses?|anos?)',  # prazos
            r'\d+\s*(horas?|minutos?)',  # tempo
            r'\d+',  # números em geral
        ]
        
        import re
        specificity_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                              for pattern in specificity_patterns)
        
        specificity_score = min(1.0, specificity_count / max(1, metrics['sentence_count']))
        
        # Comprimento médio das palavras (indica uso de termos mais específicos)
        length_score = min(1.0, metrics['avg_word_length'] / 6.0)
        
        return 0.4 * density_score + 0.4 * specificity_score + 0.2 * length_score
    
    def calculate_completeness_score(self, text: str) -> float:
        """
        Calcula pontuação de completude baseada em:
        - Quantidade de conteúdo
        - Cobertura de aspectos essenciais
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        metrics = self.text_processor.extract_metrics(text)
        
        # Score baseado na quantidade de conteúdo
        min_words = ANALYSIS_CONFIG['min_word_count']
        min_sentences = ANALYSIS_CONFIG['min_sentence_count']
        
        word_score = min(1.0, metrics['word_count'] / min_words)
        sentence_score = min(1.0, metrics['sentence_count'] / min_sentences)
        
        # Verifica cobertura de aspectos essenciais
        essential_aspects = ['como', 'quando', 'onde', 'por que', 'o que']
        coverage_score = sum(1 for aspect in essential_aspects 
                           if self.text_processor.has_keywords(text, [aspect])) / len(essential_aspects)
        
        return 0.4 * word_score + 0.3 * sentence_score + 0.3 * coverage_score
    
    def calculate_smart_score(self, text: str) -> float:
        """
        Calcula pontuação baseada nos critérios SMART
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        smart_scores = {}
        
        for criterion, keywords in SMART_KEYWORDS.items():
            keyword_count = self.text_processor.count_keywords(text, keywords)
            # Normaliza baseado no número de sentenças
            sentences = max(1, self.text_processor.get_sentence_count(text))
            smart_scores[criterion] = min(1.0, keyword_count / sentences)
        
        # Retorna a média dos critérios SMART
        return sum(smart_scores.values()) / len(smart_scores)
    
    def _calculate_structure_score(self, metrics: Dict) -> float:
        """Calcula pontuação de estrutura do texto"""
        # Verifica se o texto tem estrutura adequada
        if metrics['sentence_count'] == 0:
            return 0.0
        
        # Pontuação baseada na variação do comprimento das sentenças
        avg_sentence_length = metrics['avg_sentence_length']
        
        # Sentences muito curtas ou muito longas reduzem a pontuação
        if avg_sentence_length < 5 or avg_sentence_length > 25:
            length_score = 0.5
        else:
            length_score = 1.0
        
        # Presença de múltiplas sentenças indica melhor estrutura
        sentence_score = min(1.0, metrics['sentence_count'] / 3)
        
        return 0.6 * length_score + 0.4 * sentence_score
    
    def calculate_overall_quality(self, acoes_text: str, objetivo_text: str, weights: Dict[str, float]) -> Dict:
        """
        Calcula a qualidade geral combinando ações planejadas e objetivo de desenvolvimento
        """
        # Calcula métricas para ações planejadas
        acoes_metrics = {
            'clarity': self.calculate_clarity_score(acoes_text),
            'specificity': self.calculate_specificity_score(acoes_text),
            'completeness': self.calculate_completeness_score(acoes_text),
            'smart': self.calculate_smart_score(acoes_text)
        }
        
        # Calcula métricas para objetivo de desenvolvimento
        objetivo_metrics = {
            'clarity': self.calculate_clarity_score(objetivo_text),
            'specificity': self.calculate_specificity_score(objetivo_text),
            'completeness': self.calculate_completeness_score(objetivo_text),
            'smart': self.calculate_smart_score(objetivo_text)
        }
        
        # Combina métricas (60% ações, 40% objetivo)
        combined_metrics = {}
        for metric in acoes_metrics:
            combined_metrics[metric] = (0.6 * acoes_metrics[metric] + 
                                      0.4 * objetivo_metrics[metric])
        
        # Adiciona estrutura geral
        combined_text = f"{acoes_text} {objetivo_text}"
        combined_metrics['structure'] = self._calculate_structure_score(
            self.text_processor.extract_metrics(combined_text)
        )
        
        # Calcula pontuação final ponderada
        final_score = sum(combined_metrics[metric] * weights.get(metric, 0) 
                         for metric in combined_metrics)
        
        return {
            'score': final_score,
            'metrics': combined_metrics,
            'acoes_metrics': acoes_metrics,
            'objetivo_metrics': objetivo_metrics
        }
