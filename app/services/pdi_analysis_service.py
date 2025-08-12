"""
Serviço principal de análise de PDI.
Coordena a análise de qualidade e geração de relatórios.
"""
import pandas as pd
from typing import Dict, List, Tuple, Any
from datetime import datetime
import json

from ..core.config import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, COLUMN_MAPPING,
    PROGRESS_INTERVAL
)
from ..services.quality_metrics_service import QualityMetricsService
from ..utils.text_utils import TextUtils


class PDIAnalysisService:
    """Serviço principal para análise de qualidade de PDI."""
    
    def __init__(self):
        self.quality_service = QualityMetricsService()
        self.thresholds = QUALITY_THRESHOLDS
        self.weights = METRIC_WEIGHTS
        self.column_mapping = COLUMN_MAPPING
    
    def analyze_single_pdi(self, pdi_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa um único PDI.
        
        Args:
            pdi_data: Dados do PDI para análise
            
        Returns:
            Resultado da análise com scores e classificação
        """
        # Extrai textos principais
        objetivo = pdi_data.get(self.column_mapping['objetivo_desenvolvimento'], '')
        acoes = pdi_data.get(self.column_mapping['acoes_planejadas'], '')
        atividade = pdi_data.get(self.column_mapping.get('atividade_aprendizagem', ''), '')
        
        # Combina textos para análise
        texto_completo = f"{objetivo} {acoes} {atividade}".strip()
        
        # Valida qualidade mínima do texto
        if not TextUtils.validate_text_quality(texto_completo):
            return self._create_empty_result(texto_completo)
        
        # Calcula métricas de qualidade
        metrics = self.quality_service.calculate_overall_quality(
            texto_completo, self.weights
        )
        
        # Determina nível de qualidade
        overall_score = metrics['overall_score']
        quality_level = self._determine_quality_level(overall_score)
        
        # Gera sugestões de melhoria
        suggestions = self._generate_suggestions(metrics, texto_completo)
        
        return {
            'clarity_score': round(metrics['clarity_score'], 3),
            'specificity_score': round(metrics['specificity_score'], 3),
            'completeness_score': round(metrics['completeness_score'], 3),
            'structure_score': round(metrics['structure_score'], 3),
            'smart_criteria_score': round(metrics['smart_criteria_score'], 3),
            'overall_score': round(overall_score, 3),
            'quality_level': quality_level,
            'negative_impact': round(metrics['negative_impact'], 3),
            'suggestions': suggestions,
            'text_analyzed': self._truncate_text(texto_completo, 100)
        }
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Analisa um DataFrame completo de PDIs.
        
        Args:
            df: DataFrame com dados dos PDIs
            
        Returns:
            Tupla com DataFrame de resultados e resumo da análise
        """
        print(f"🔍 Iniciando análise de {len(df)} PDIs...")
        
        # Cria cópia do DataFrame
        result_df = df.copy()
        results = []
        
        # Processa cada linha
        for idx, row in df.iterrows():
            try:
                # Converte linha para dicionário
                pdi_data = row.to_dict()
                
                # Analisa o PDI
                analysis_result = self.analyze_single_pdi(pdi_data)
                
                # Adiciona resultado ao DataFrame
                for key, value in analysis_result.items():
                    if key != 'text_analyzed':  # Evita duplicar texto
                        result_df.loc[idx, key] = value
                
                results.append(analysis_result)
                
                # Mostra progresso
                if (idx + 1) % PROGRESS_INTERVAL == 0:
                    print(f"✅ Processados {idx + 1}/{len(df)} PDIs")
                
            except Exception as e:
                print(f"⚠️ Erro na linha {idx}: {str(e)}")
                
                # Preenche com resultado de erro
                error_result = self._create_error_result(str(e))
                
                for key, value in error_result.items():
                    if key != 'text_analyzed':
                        result_df.loc[idx, key] = value
                
                results.append(error_result)
        
        # Gera resumo da análise
        summary = self._generate_summary(results)
        
        print("✅ Análise concluída!")
        return result_df, summary
    
    def _determine_quality_level(self, score: float) -> str:
        """Determina o nível de qualidade baseado no score."""
        if score >= self.thresholds['high']:
            return 'Alta'
        elif score >= self.thresholds['medium']:
            return 'Média'
        else:
            return 'Baixa'
    
    def _create_empty_result(self, text: str) -> Dict[str, Any]:
        """Cria resultado para texto vazio ou inválido."""
        return {
            'clarity_score': 0.0,
            'specificity_score': 0.0,
            'completeness_score': 0.0,
            'structure_score': 0.0,
            'smart_criteria_score': 0.0,
            'overall_score': 0.0,
            'quality_level': 'Baixa',
            'negative_impact': 0.0,
            'suggestions': 'Texto insuficiente para análise. Adicione mais conteúdo.',
            'text_analyzed': text[:50] + '...' if len(text) > 50 else text
        }
    
    def _create_error_result(self, error_msg: str) -> Dict[str, Any]:
        """Cria resultado para casos de erro."""
        return {
            'clarity_score': 0.0,
            'specificity_score': 0.0,
            'completeness_score': 0.0,
            'structure_score': 0.0,
            'smart_criteria_score': 0.0,
            'overall_score': 0.0,
            'quality_level': 'Baixa',
            'negative_impact': 0.0,
            'suggestions': f'Erro na análise: {error_msg}',
            'text_analyzed': 'Erro no processamento'
        }
    
    def _generate_suggestions(self, metrics: Dict[str, float], text: str) -> str:
        """
        Gera sugestões de melhoria baseadas nas métricas.
        
        Args:
            metrics: Métricas calculadas
            text: Texto analisado
            
        Returns:
            Sugestões de melhoria
        """
        suggestions = []
        
        # Sugestões baseadas em scores baixos
        if metrics['clarity_score'] < 0.5:
            suggestions.append("Melhore a clareza usando frases mais simples e diretas")
        
        if metrics['specificity_score'] < 0.5:
            suggestions.append("Adicione detalhes específicos, números e termos técnicos")
        
        if metrics['completeness_score'] < 0.5:
            suggestions.append("Desenvolva melhor o contexto e as ações planejadas")
        
        if metrics['structure_score'] < 0.5:
            suggestions.append("Melhore a estrutura com pontuação adequada")
        
        if metrics['smart_criteria_score'] < 0.5:
            suggestions.append("Inclua critérios SMART (específico, mensurável, prazo)")
        
        # Sugestões baseadas em impacto negativo
        if metrics['negative_impact'] > 0.3:
            suggestions.append("Evite linguagem incerta - seja mais assertivo")
        
        # Sugestões específicas do texto
        word_count = TextUtils.count_words(text)
        if word_count < 10:
            suggestions.append("Texto muito curto - adicione mais detalhes")
        elif word_count > 50:
            suggestions.append("Texto muito longo - seja mais conciso")
        
        if not TextUtils.has_numbers(text):
            suggestions.append("Inclua números específicos (prazos, metas, indicadores)")
        
        # Caso não haja sugestões específicas
        if not suggestions:
            if metrics['overall_score'] >= 0.8:
                suggestions.append("Excelente qualidade! Continue mantendo esse padrão")
            else:
                suggestions.append("Revise o texto para maior clareza e especificidade")
        
        return " | ".join(suggestions)
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Gera resumo estatístico da análise.
        
        Args:
            results: Lista de resultados de análise
            
        Returns:
            Resumo com estatísticas da análise
        """
        if not results:
            return self._empty_summary()
        
        # Conta níveis de qualidade
        quality_counts = {'Alta': 0, 'Média': 0, 'Baixa': 0}
        total_scores = {
            'clarity': 0.0,
            'specificity': 0.0,
            'completeness': 0.0,
            'structure': 0.0,
            'smart_criteria': 0.0,
            'overall': 0.0,
            'negative_impact': 0.0
        }
        
        for result in results:
            # Conta qualidade
            quality_level = result.get('quality_level', 'Baixa')
            quality_counts[quality_level] += 1
            
            # Soma scores
            total_scores['clarity'] += result.get('clarity_score', 0.0)
            total_scores['specificity'] += result.get('specificity_score', 0.0)
            total_scores['completeness'] += result.get('completeness_score', 0.0)
            total_scores['structure'] += result.get('structure_score', 0.0)
            total_scores['smart_criteria'] += result.get('smart_criteria_score', 0.0)
            total_scores['overall'] += result.get('overall_score', 0.0)
            total_scores['negative_impact'] += result.get('negative_impact', 0.0)
        
        # Calcula médias
        total_analyzed = len(results)
        avg_scores = {
            key: round(value / total_analyzed, 3)
            for key, value in total_scores.items()
        }
        
        return {
            'total_analyzed': total_analyzed,
            'high_quality': quality_counts['Alta'],
            'medium_quality': quality_counts['Média'],
            'low_quality': quality_counts['Baixa'],
            'quality_percentages': {
                'high': round(quality_counts['Alta'] / total_analyzed * 100, 1),
                'medium': round(quality_counts['Média'] / total_analyzed * 100, 1),
                'low': round(quality_counts['Baixa'] / total_analyzed * 100, 1)
            },
            'average_scores': avg_scores,
            'timestamp': datetime.now().isoformat(),
            'analysis_version': '2.0'
        }
    
    def _empty_summary(self) -> Dict[str, Any]:
        """Retorna resumo vazio para casos sem dados."""
        return {
            'total_analyzed': 0,
            'high_quality': 0,
            'medium_quality': 0,
            'low_quality': 0,
            'quality_percentages': {'high': 0.0, 'medium': 0.0, 'low': 0.0},
            'average_scores': {
                'clarity': 0.0, 'specificity': 0.0, 'completeness': 0.0,
                'structure': 0.0, 'smart_criteria': 0.0, 'overall': 0.0,
                'negative_impact': 0.0
            },
            'timestamp': datetime.now().isoformat(),
            'analysis_version': '2.0'
        }
    
    @staticmethod
    def _truncate_text(text: str, max_length: int) -> str:
        """Trunca texto para tamanho máximo."""
        if len(text) <= max_length:
            return text
        return text[:max_length] + '...'
