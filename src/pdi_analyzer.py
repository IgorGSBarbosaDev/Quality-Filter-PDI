"""
Analisador principal de PDI
"""
import pandas as pd
from typing import Dict, List, Tuple
from .quality_metrics import QualityMetrics
from .text_processor import TextProcessor
from config.settings import ANALYSIS_CONFIG, METRIC_WEIGHTS, EXCEL_COLUMNS

class PDIAnalyzer:
    def __init__(self):
        self.quality_metrics = QualityMetrics()
        self.text_processor = TextProcessor()
        self.thresholds = ANALYSIS_CONFIG['quality_thresholds']
    
    def analyze_single_pdi(self, acoes_planejadas: str, objetivo_desenvolvimento: str) -> Dict:
        """
        Analisa um único PDI e retorna avaliação completa
        """
        # Calcula qualidade geral
        quality_result = self.quality_metrics.calculate_overall_quality(
            acoes_planejadas, objetivo_desenvolvimento, METRIC_WEIGHTS
        )
        
        # Determina nível de qualidade
        score = quality_result['score']
        if score >= self.thresholds['high']:
            level = 'Alto'
        elif score >= self.thresholds['medium']:
            level = 'Médio'
        else:
            level = 'Baixo'
        
        # Gera sugestões de melhoria
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
        """
        Analisa um DataFrame completo de PDIs
        """
        results = []
        
        for idx, row in df.iterrows():
            try:
                acoes = str(row.get(EXCEL_COLUMNS['acoes_planejadas'], ''))
                objetivo = str(row.get(EXCEL_COLUMNS['objetivo_desenvolvimento'], ''))
                
                analysis = self.analyze_single_pdi(acoes, objetivo)
                
                results.append({
                    'quality_level': analysis['quality_level'],
                    'quality_score': analysis['quality_score'],
                    'suggestions': analysis['suggestions'],
                    'clarity_score': round(analysis['detailed_metrics']['clarity'], 3),
                    'specificity_score': round(analysis['detailed_metrics']['specificity'], 3),
                    'completeness_score': round(analysis['detailed_metrics']['completeness'], 3),
                    'structure_score': round(analysis['detailed_metrics']['structure'], 3),
                    'smart_score': round(analysis['detailed_metrics']['smart'], 3)
                })
                
            except Exception as e:
                # Em caso de erro, atribui qualidade baixa
                results.append({
                    'quality_level': 'Baixo',
                    'quality_score': 0.0,
                    'suggestions': f'Erro na análise: {str(e)}',
                    'clarity_score': 0.0,
                    'specificity_score': 0.0,
                    'completeness_score': 0.0,
                    'structure_score': 0.0,
                    'smart_score': 0.0
                })
        
        # Adiciona resultados ao DataFrame original\n        result_df = df.copy()\n        for i, result in enumerate(results):\n            for key, value in result.items():\n                result_df.loc[i, key] = value\n        \n        return result_df\n    \n    def _generate_suggestions(self, acoes: str, objetivo: str, quality_result: Dict) -> str:\n        \"\"\"\n        Gera sugestões específicas de melhoria baseadas na análise\n        \"\"\"\n        suggestions = []\n        metrics = quality_result['metrics']\n        acoes_metrics = quality_result['analysis_breakdown']['acoes_metrics']\n        objetivo_metrics = quality_result['analysis_breakdown']['objetivo_metrics']\n        \n        # Sugestões para clareza\n        if metrics['clarity'] < 0.6:\n            suggestions.append(\"• Melhore a clareza: Use linguagem mais objetiva e direta\")\n            \n        # Sugestões para especificidade\n        if metrics['specificity'] < 0.6:\n            suggestions.append(\"• Seja mais específico: Inclua números, prazos e medidas concretas\")\n        \n        # Sugestões para completude\n        if metrics['completeness'] < 0.6:\n            suggestions.append(\"• Adicione mais detalhes: Explique como, quando e onde as ações serão realizadas\")\n        \n        # Sugestões para estrutura\n        if metrics['structure'] < 0.6:\n            suggestions.append(\"• Melhore a estrutura: Organize as informações em sentenças bem construídas\")\n        \n        # Sugestões para critérios SMART\n        if metrics['smart'] < 0.5:\n            smart_suggestions = []\n            if acoes_metrics['smart'] < 0.4:\n                smart_suggestions.append(\"torne as ações mais específicas e mensuráveis\")\n            if objetivo_metrics['smart'] < 0.4:\n                smart_suggestions.append(\"defina objetivos com prazos e métricas claras\")\n            \n            if smart_suggestions:\n                suggestions.append(f\"• Critérios SMART: {', '.join(smart_suggestions)}\")\n        \n        # Sugestões específicas para ações planejadas\n        if acoes_metrics['completeness'] < 0.5:\n            suggestions.append(\"• Ações planejadas: Detalhe melhor as etapas e cronograma\")\n        \n        # Sugestões específicas para objetivos\n        if objetivo_metrics['specificity'] < 0.5:\n            suggestions.append(\"• Objetivo: Seja mais específico sobre o resultado esperado\")\n        \n        # Verifica conteúdo mínimo\n        acoes_words = self.text_processor.get_word_count(acoes)\n        objetivo_words = self.text_processor.get_word_count(objetivo)\n        \n        if acoes_words < ANALYSIS_CONFIG['min_word_count']:\n            suggestions.append(f\"• Ações muito breves: Expanda para pelo menos {ANALYSIS_CONFIG['min_word_count']} palavras\")\n        \n        if objetivo_words < ANALYSIS_CONFIG['min_word_count']:\n            suggestions.append(f\"• Objetivo muito breve: Expanda para pelo menos {ANALYSIS_CONFIG['min_word_count']} palavras\")\n        \n        # Se não há sugestões específicas, adiciona uma geral\n        if not suggestions:\n            if quality_result['score'] >= self.thresholds['high']:\n                suggestions.append(\"• PDI de excelente qualidade! Continue mantendo esse padrão.\")\n            else:\n                suggestions.append(\"• Revise o PDI para maior clareza e especificidade.\")\n        \n        return \" \".join(suggestions)\n    \n    def generate_summary_report(self, df: pd.DataFrame) -> Dict:\n        \"\"\"\n        Gera relatório resumido da análise\n        \"\"\"\n        total_pdis = len(df)\n        \n        quality_distribution = df['quality_level'].value_counts().to_dict()\n        avg_score = df['quality_score'].mean()\n        \n        # Métricas por categoria\n        avg_metrics = {\n            'clarity': df['clarity_score'].mean(),\n            'specificity': df['specificity_score'].mean(),\n            'completeness': df['completeness_score'].mean(),\n            'structure': df['structure_score'].mean(),\n            'smart': df['smart_score'].mean()\n        }\n        \n        # Identifica áreas de melhoria mais comuns\n        low_quality_df = df[df['quality_level'] == 'Baixo']\n        improvement_areas = []\n        \n        if len(low_quality_df) > 0:\n            if low_quality_df['clarity_score'].mean() < 0.5:\n                improvement_areas.append('Clareza')\n            if low_quality_df['specificity_score'].mean() < 0.5:\n                improvement_areas.append('Especificidade')\n            if low_quality_df['completeness_score'].mean() < 0.5:\n                improvement_areas.append('Completude')\n        \n        return {\n            'total_pdis': total_pdis,\n            'quality_distribution': quality_distribution,\n            'average_score': round(avg_score, 3),\n            'average_metrics': {k: round(v, 3) for k, v in avg_metrics.items()},\n            'main_improvement_areas': improvement_areas,\n            'quality_percentage': {\n                'high': quality_distribution.get('Alto', 0) / total_pdis * 100,\n                'medium': quality_distribution.get('Médio', 0) / total_pdis * 100,\n                'low': quality_distribution.get('Baixo', 0) / total_pdis * 100\n            }\n        }
