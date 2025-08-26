"""
🎯 Serviço de Métricas de Qualidade Refatorado - Quality Filter PDI
Classe principal que coordena todas as calculadoras especializadas
"""

from typing import Dict, Any
from .metrics import (
    ClarityCalculator,
    SpecificityCalculator,
    CompletenessCalculator,
    CohesionCalculator,
    QualityAggregator,
    ScoreExplainer
)


class QualityMetricsService:
    """
    Serviço principal de métricas de qualidade.
    
    Esta classe coordena todas as calculadoras especializadas:
    - ClarityCalculator: Calcula clareza do texto
    - SpecificityCalculator: Calcula especificidade e detalhamento
    - CompletenessCalculator: Calcula completude das informações
    - CohesionCalculator: Analisa coesão entre objetivo e ações
    - QualityAggregator: Agrega métricas em score final
    - ScoreExplainer: Gera explicações detalhadas
    """
    
    def __init__(self, enable_cache: bool = True, enable_ai: bool = True):
        """
        Inicializa o serviço com todas as calculadoras especializadas
        
        Args:
            enable_cache: Habilita cache para performance
            enable_ai: Habilita análise de IA para coesão
        """
        # Inicializar calculadoras especializadas
        self.clarity_calculator = ClarityCalculator(enable_cache=enable_cache)
        self.specificity_calculator = SpecificityCalculator(enable_cache=enable_cache)
        self.completeness_calculator = CompletenessCalculator(enable_cache=enable_cache)
        self.cohesion_calculator = CohesionCalculator(enable_ai=enable_ai)
        
        # Inicializar agregador e explicador
        self.quality_aggregator = QualityAggregator()
        self.score_explainer = ScoreExplainer()
        
        # Status do serviço
        self.cache_enabled = enable_cache
        self.ai_enabled = enable_ai
    
    # === INTERFACE PÚBLICA - MÉTRICAS INDIVIDUAIS ===
    
    def calculate_clarity(self, text: str) -> float:
        """Calcula clareza do texto"""
        return self.clarity_calculator.calculate(text)
    
    def calculate_specificity(self, text: str) -> float:
        """Calcula especificidade do texto"""
        return self.specificity_calculator.calculate(text)
    
    def calculate_completeness(self, text: str) -> float:
        """Calcula completude do texto"""
        return self.completeness_calculator.calculate(text)
    
    def calculate_negative_impact(self, text: str) -> float:
        """Calcula impacto negativo de indicadores problemáticos"""
        return self.quality_aggregator.calculate_negative_impact(text)
    
    def calculate_goal_cohesion(self, objetivo: str, acoes: str, atividades: str = "") -> Dict[str, float]:
        """Calcula coesão entre objetivo e ações/atividades"""
        return self.cohesion_calculator.calculate_goal_cohesion(objetivo, acoes, atividades)
    
    # === INTERFACE PÚBLICA - AGREGAÇÃO DE QUALIDADE ===
    
    def calculate_overall_quality(self, clarity: float, specificity: float, 
                                completeness: float) -> Dict[str, float]:
        """Calcula qualidade geral baseada nos critérios principais"""
        return self.quality_aggregator.calculate_overall_quality(clarity, specificity, completeness)
    
    def calculate_comprehensive_quality(self, clarity: float, specificity: float, 
                                      completeness: float, cohesion_score: float = None,
                                      negative_impact: float = 0.0) -> Dict[str, Any]:
        """Calcula qualidade abrangente incluindo coesão e impacto negativo"""
        return self.quality_aggregator.calculate_comprehensive_quality(
            clarity, specificity, completeness, cohesion_score, negative_impact
        )
    
    # === INTERFACE PÚBLICA - EXPLICAÇÕES ===
    
    def generate_score_explanation(self, clarity: float, specificity: float, 
                                 completeness: float, 
                                 negative_impact: float = 0.0) -> str:
        """Gera explicação detalhada da pontuação"""
        return self.score_explainer.generate_score_explanation(
            clarity, specificity, completeness, negative_impact
        )
    
    def generate_concise_reasons(self, clarity: float, specificity: float, 
                                completeness: float, 
                                negative_impact: float = 0.0,
                                overall_score: float = 0.0) -> dict:
        """Gera razões concisas para a pontuação"""
        return self.score_explainer.generate_concise_reasons(
            clarity, specificity, completeness, negative_impact, overall_score
        )
    
    def generate_cohesion_explanation(self, cohesion_score: float, cohesion_level: str) -> str:
        """Gera explicação específica para coesão"""
        return self.score_explainer.generate_cohesion_explanation(cohesion_score, cohesion_level)
    
    # === MÉTODOS DE CONVENIÊNCIA ===
    
    def analyze_text_quality(self, text: str) -> Dict[str, Any]:
        """
        Analisa qualidade completa de um texto individual
        
        Returns:
            Dict com todas as métricas calculadas
        """
        if not text or not text.strip():
            return {
                'clarity': 0.0,
                'specificity': 0.0,
                'completeness': 0.0,
                'negative_impact': 0.0,
                'overall_score': 0.0,
                'quality_level': 'muito ruim'
            }
        
        # Calcular métricas individuais
        clarity = self.calculate_clarity(text)
        specificity = self.calculate_specificity(text)
        completeness = self.calculate_completeness(text)
        negative_impact = self.calculate_negative_impact(text)
        
        # Calcular qualidade abrangente
        quality_result = self.calculate_comprehensive_quality(
            clarity, specificity, completeness, None, negative_impact
        )
        
        return {
            'clarity': clarity,
            'specificity': specificity,
            'completeness': completeness,
            'negative_impact': negative_impact,
            'overall_score': quality_result['overall_score'],
            'quality_level': quality_result['nivel_qualidade'],
            'pontuacao_total': quality_result['pontuacao_total']
        }
    
    def analyze_pdi_complete(self, objetivo: str, acoes: str, atividades: str = "") -> Dict[str, Any]:
        """
        Análise completa de um PDI incluindo coesão
        
        Args:
            objetivo: Objetivo de desenvolvimento
            acoes: Ações planejadas
            atividades: Atividades complementares
        
        Returns:
            Dict com análise completa incluindo coesão
        """
        # Combinar textos para análise de qualidade
        combined_text = f"{objetivo} {acoes} {atividades}".strip()
        
        # Análise de qualidade do texto
        text_quality = self.analyze_text_quality(combined_text)
        
        # Análise de coesão
        cohesion_result = self.calculate_goal_cohesion(objetivo, acoes, atividades)
        
        # Qualidade final incluindo coesão
        final_quality = self.calculate_comprehensive_quality(
            text_quality['clarity'],
            text_quality['specificity'],
            text_quality['completeness'],
            cohesion_result['cohesion_score'],
            text_quality['negative_impact']
        )
        
        return {
            # Métricas individuais
            'clarity': text_quality['clarity'],
            'specificity': text_quality['specificity'],
            'completeness': text_quality['completeness'],
            'negative_impact': text_quality['negative_impact'],
            
            # Coesão
            'cohesion_score': cohesion_result['cohesion_score'],
            'coesao_da_meta': cohesion_result['cohesion_level'],
            
            # Scores finais
            'overall_score': final_quality['overall_score'],
            'pontuacao_total': final_quality['pontuacao_total'],
            'nivel_qualidade': final_quality['nivel_qualidade'],
            
            # Detalhes para debugging
            'scores': final_quality.get('scores', {}),
            'analysis_details': {
                'objetivo': objetivo,
                'acoes': acoes,
                'atividades': atividades,
                'combined_text_length': len(combined_text)
            }
        }
    
    # === MÉTODOS DE STATUS ===
    
    def get_service_status(self) -> Dict[str, Any]:
        """Retorna status do serviço e suas dependências"""
        return {
            'service_active': True,
            'cache_enabled': self.cache_enabled,
            'ai_enabled': self.ai_enabled and self.cohesion_calculator.ai_enabled,
            'calculators': {
                'clarity': True,
                'specificity': True,
                'completeness': True,
                'cohesion': True,
                'aggregator': True,
                'explainer': True
            },
            'ai_analyzer_loaded': hasattr(self.cohesion_calculator, 'ai_analyzer') and 
                                self.cohesion_calculator.ai_analyzer is not None
        }
