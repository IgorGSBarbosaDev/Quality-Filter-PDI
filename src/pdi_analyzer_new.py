import pandas as pd
from typing import Dict, List, Any
from .quality_metrics import QualityMetrics
from .text_processor import TextProcessor
from config.settings import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, EXCEL_COLUMNS, 
    MIN_WORD_COUNT
)


class PDIAnalyzer:
    def __init__(self) -> None:
        self.quality_metrics = QualityMetrics()
        self.text_processor = TextProcessor()
        self.thresholds = QUALITY_THRESHOLDS
    
    def analyze_single_pdi(self, acoes_planejadas: str, objetivo_desenvolvimento: str) -> Dict[str, Any]:
        quality_result = self.quality_metrics.calculate_overall_quality(
            acoes_planejadas, objetivo_desenvolvimento, METRIC_WEIGHTS
        )
        
        score = quality_result['score']
        level = self._determine_quality_level(score)
        
        suggestions = self._generate_suggestions(
            acoes_planejadas, objetivo_desenvolvimento, quality_result
        )
        
        return {
            'quality_level': level,
            'quality_score': round(score, 3),
            'detailed_metrics': quality_result['metrics'],
            'suggestions': suggestions,
            'analysis_breakdown': {
                'acoes_metrics': quality_result['acoes_metrics'],
                'objetivo_metrics': quality_result['objetivo_metrics']
            }
        }
    
    def analyze_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        results = []
        
        for idx, row in df.iterrows():
            try:
                acoes = str(row.get(EXCEL_COLUMNS['acoes_planejadas'], ''))
                objetivo = str(row.get(EXCEL_COLUMNS['objetivo_desenvolvimento'], ''))
                
                analysis = self.analyze_single_pdi(acoes, objetivo)
                
                results.append(self._format_analysis_result(analysis))
                
            except Exception as e:
                results.append(self._create_error_result(str(e)))
        
        result_df = df.copy()
        for i, result in enumerate(results):
            for key, value in result.items():
                result_df.loc[i, key] = value
        
        return result_df
    
    def _determine_quality_level(self, score: float) -> str:
        if score >= self.thresholds['high']:
            return 'Alto'
        elif score >= self.thresholds['medium']:
            return 'Médio'
        return 'Baixo'
    
    def _format_analysis_result(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'quality_level': analysis['quality_level'],
            'quality_score': analysis['quality_score'],
            'suggestions': analysis['suggestions'],
            'clarity_score': round(analysis['detailed_metrics']['clarity'], 3),
            'specificity_score': round(analysis['detailed_metrics']['specificity'], 3),
            'completeness_score': round(analysis['detailed_metrics']['completeness'], 3),
            'structure_score': round(analysis['detailed_metrics']['structure'], 3),
            'smart_score': round(analysis['detailed_metrics']['smart'], 3)
        }
    
    def _create_error_result(self, error_msg: str) -> Dict[str, Any]:
        return {
            'quality_level': 'Baixo',
            'quality_score': 0.0,
            'suggestions': f'Erro na análise: {error_msg}',
            'clarity_score': 0.0,
            'specificity_score': 0.0,
            'completeness_score': 0.0,
            'structure_score': 0.0,
            'smart_score': 0.0
        }
    
    def _generate_suggestions(
        self, 
        acoes: str, 
        objetivo: str, 
        quality_result: Dict[str, Any]
    ) -> str:
        suggestions = []
        metrics = quality_result['metrics']
        acoes_metrics = quality_result['analysis_breakdown']['acoes_metrics']
        objetivo_metrics = quality_result['analysis_breakdown']['objetivo_metrics']
        
        suggestions.extend(self._get_metric_suggestions(metrics))
        suggestions.extend(self._get_smart_suggestions(metrics, acoes_metrics, objetivo_metrics))
        suggestions.extend(self._get_specific_suggestions(acoes_metrics, objetivo_metrics))
        suggestions.extend(self._get_length_suggestions(acoes, objetivo))
        
        if not suggestions:
            if quality_result['score'] >= self.thresholds['high']:
                suggestions.append("• PDI de excelente qualidade! Continue mantendo esse padrão.")
            else:
                suggestions.append("• Revise o PDI para maior clareza e especificidade.")
        
        return " ".join(suggestions)
    
    def _get_metric_suggestions(self, metrics: Dict[str, float]) -> List[str]:
        suggestions = []
        metric_suggestions = {
            'clarity': "• Melhore a clareza: Use linguagem mais objetiva e direta",
            'specificity': "• Seja mais específico: Inclua números, prazos e medidas concretas",
            'completeness': "• Adicione mais detalhes: Explique como, quando e onde as ações serão realizadas",
            'structure': "• Melhore a estrutura: Organize as informações em sentenças bem construídas"
        }
        
        for metric, suggestion in metric_suggestions.items():
            if metrics.get(metric, 0) < 0.6:
                suggestions.append(suggestion)
        
        return suggestions
    
    def _get_smart_suggestions(
        self, 
        metrics: Dict[str, float], 
        acoes_metrics: Dict[str, float], 
        objetivo_metrics: Dict[str, float]
    ) -> List[str]:
        suggestions = []
        
        if metrics.get('smart', 0) < 0.5:
            smart_suggestions = []
            if acoes_metrics.get('smart', 0) < 0.4:
                smart_suggestions.append("torne as ações mais específicas e mensuráveis")
            if objetivo_metrics.get('smart', 0) < 0.4:
                smart_suggestions.append("defina objetivos com prazos e métricas claras")
            
            if smart_suggestions:
                suggestions.append(f"• Critérios SMART: {', '.join(smart_suggestions)}")
        
        return suggestions
    
    def _get_specific_suggestions(
        self, 
        acoes_metrics: Dict[str, float], 
        objetivo_metrics: Dict[str, float]
    ) -> List[str]:
        suggestions = []
        
        if acoes_metrics.get('completeness', 0) < 0.5:
            suggestions.append("• Ações planejadas: Detalhe melhor as etapas e cronograma")
        
        if objetivo_metrics.get('specificity', 0) < 0.5:
            suggestions.append("• Objetivo: Seja mais específico sobre o resultado esperado")
        
        return suggestions
    
    def _get_length_suggestions(self, acoes: str, objetivo: str) -> List[str]:
        suggestions = []
        
        acoes_words = self.text_processor.get_word_count(acoes)
        objetivo_words = self.text_processor.get_word_count(objetivo)
        
        if acoes_words < MIN_WORD_COUNT:
            suggestions.append(f"• Ações muito breves: Expanda para pelo menos {MIN_WORD_COUNT} palavras")
        
        if objetivo_words < MIN_WORD_COUNT:
            suggestions.append(f"• Objetivo muito breve: Expanda para pelo menos {MIN_WORD_COUNT} palavras")
        
        return suggestions
    
    def generate_summary_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        total_pdis = len(df)
        
        quality_distribution = df['quality_level'].value_counts().to_dict()
        avg_score = df['quality_score'].mean()
        
        avg_metrics = {
            'clarity': df['clarity_score'].mean(),
            'specificity': df['specificity_score'].mean(),
            'completeness': df['completeness_score'].mean(),
            'structure': df['structure_score'].mean(),
            'smart': df['smart_score'].mean()
        }
        
        improvement_areas = self._identify_improvement_areas(df)
        
        return {
            'total_pdis': total_pdis,
            'quality_distribution': quality_distribution,
            'average_score': round(avg_score, 3),
            'average_metrics': {k: round(v, 3) for k, v in avg_metrics.items()},
            'main_improvement_areas': improvement_areas,
            'quality_percentage': self._calculate_quality_percentages(quality_distribution, total_pdis)
        }
    
    def _identify_improvement_areas(self, df: pd.DataFrame) -> List[str]:
        low_quality_df = df[df['quality_level'] == 'Baixo']
        improvement_areas = []
        
        if len(low_quality_df) > 0:
            metrics_to_check = {
                'clarity_score': 'Clareza',
                'specificity_score': 'Especificidade',
                'completeness_score': 'Completude'
            }
            
            for score_column, area_name in metrics_to_check.items():
                if low_quality_df[score_column].mean() < 0.5:
                    improvement_areas.append(area_name)
        
        return improvement_areas
    
    def _calculate_quality_percentages(
        self, 
        quality_distribution: Dict[str, int], 
        total_pdis: int
    ) -> Dict[str, float]:
        return {
            'high': quality_distribution.get('Alto', 0) / total_pdis * 100,
            'medium': quality_distribution.get('Médio', 0) / total_pdis * 100,
            'low': quality_distribution.get('Baixo', 0) / total_pdis * 100
        }
