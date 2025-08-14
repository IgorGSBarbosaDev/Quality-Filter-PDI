import pandas as pd
from typing import Dict, List, Tuple, Any
from datetime import datetime
import json

from ..core.config import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, COLUMN_MAPPING,
    PROGRESS_INTERVAL
)
from ..services.quality_metrics_service import QualityMetricsService
from ..services.skill_classifier import SkillClassifier
from ..utils.text_utils import TextUtils

try:
    from ..ai.ai_text_analyzer import AITextAnalyzer
    from ..ai.advanced_ai_analyzer import AdvancedAIAnalyzer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class PDIAnalysisService:
    
    def __init__(self):
        self.quality_service = QualityMetricsService()
        self.skill_classifier = SkillClassifier()
        self.thresholds = QUALITY_THRESHOLDS
        self.weights = METRIC_WEIGHTS
        self.column_mapping = COLUMN_MAPPING
        
        if AI_AVAILABLE:
            try:
                self.ai_analyzer = AITextAnalyzer()
                self.advanced_ai = AdvancedAIAnalyzer()
                self.ai_enabled = True
                print("✅ Módulos de IA carregados com sucesso")
            except Exception as e:
                print(f"⚠️ Erro ao carregar IA: {e}")
                self.ai_enabled = False
        else:
            self.ai_enabled = False
    
    def analyze_single_pdi(self, pdi_data: Dict[str, Any]) -> Dict[str, Any]:
        objetivo = pdi_data.get(self.column_mapping['objetivo_desenvolvimento'], '')
        acoes = pdi_data.get(self.column_mapping['acoes_planejadas'], '')
        atividade = pdi_data.get(self.column_mapping.get('atividade_aprendizagem', ''), '')
        
        texto_completo = f"{objetivo} {acoes} {atividade}".strip()
        
        if not TextUtils.validate_text_quality(texto_completo):
            return self._create_empty_result(texto_completo)
        
        metrics = self.quality_service.calculate_overall_quality(
            self.quality_service.calculate_clarity(texto_completo),
            self.quality_service.calculate_specificity(texto_completo),
            self.quality_service.calculate_completeness(texto_completo),
            self.quality_service.calculate_structure(texto_completo),
            self.quality_service.calculate_smart_criteria(texto_completo)
        )
        
        negative_impact = self.quality_service.calculate_negative_impact(texto_completo)
        metrics['overall_score'] = max(0, metrics['overall_score'] - negative_impact)
        
        if metrics['overall_score'] >= self.thresholds['medium']:
            if metrics['overall_score'] >= self.thresholds['high']:
                metrics['quality_level'] = 'Alta'
            else:
                metrics['quality_level'] = 'Média'
        else:
            metrics['quality_level'] = 'Baixa'
        
        skill_analysis = self.skill_classifier.classify_skill(objetivo)
        
        ai_insights = {}
        if self.ai_enabled:
            try:
                ai_enhancement = self.ai_analyzer.enhance_quality_analysis(texto_completo, metrics)
                ai_intent = self.advanced_ai.analyze_pdi_intent(objetivo, acoes)
                ai_suggestions = self.advanced_ai.generate_smart_suggestions(objetivo, metrics['overall_score'])
                
                ai_insights = {
                    'enhancement': ai_enhancement.get('ai_enhancement', {}),
                    'intent_analysis': ai_intent,
                    'smart_suggestions': ai_suggestions,
                    'ai_boosted_score': ai_enhancement.get('enhanced_overall_score', metrics['overall_score'])
                }
                
                if ai_enhancement.get('enhanced_overall_score', 0) > metrics['overall_score']:
                    metrics['overall_score'] = ai_enhancement['enhanced_overall_score']
                    metrics['ai_enhanced'] = True
                    
            except Exception as e:
                print(f"⚠️ Erro na análise AI: {e}")
                ai_insights = {'error': 'AI analysis failed', 'ai_enhanced': False}
        
        result = {
            **metrics,
            'original_text': {
                'objetivo': objetivo,
                'acoes': acoes,
                'atividade': atividade
            },
            'skill_classification': skill_analysis,
            'ai_insights': ai_insights,
            'analysis_metadata': {
                'word_count': TextUtils.count_words(texto_completo),
                'sentence_count': TextUtils.count_sentences(texto_completo),
                'has_numbers': TextUtils.has_numbers(texto_completo),
                'technical_terms': TextUtils.extract_technical_terms(texto_completo),
                'negative_impact': negative_impact,
                'ai_enabled': self.ai_enabled
            }
        }
        
        for key, value in pdi_data.items():
            if key not in result:
                result[key] = value
        
        return result
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            return {
                'success': False,
                'error': 'DataFrame vazio',
                'total_analyzed': 0,
                'results': []
            }
        
        try:
            results = []
            total_rows = len(df)
            
            print(f"Iniciando análise de {total_rows} PDIs...")
            
            for index, row in df.iterrows():
                try:
                    pdi_data = row.to_dict()
                    analysis_result = self.analyze_single_pdi(pdi_data)
                    
                    analysis_result['row_index'] = index
                    results.append(analysis_result)
                    
                    if (index + 1) % PROGRESS_INTERVAL == 0:
                        print(f"Processados: {index + 1}/{total_rows}")
                        
                except Exception as e:
                    print(f"Erro ao analisar linha {index}: {e}")
                    continue
            
            print(f"Análise concluída: {len(results)} PDIs processados")
            
            return {
                'success': True,
                'total_analyzed': len(results),
                'results': results,
                'summary': self._generate_summary(results),
                'detailed_results': self._create_results_dataframe(results),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro durante análise: {str(e)}',
                'total_analyzed': 0,
                'results': []
            }
    
    def _create_empty_result(self, text: str) -> Dict[str, Any]:
        return {
            'overall_score': 0.0,
            'quality_level': 'Baixa',
            'clarity_score': 0.0,
            'specificity_score': 0.0,
            'completeness_score': 0.0,
            'structure_score': 0.0,
            'smart_criteria_score': 0.0,
            'original_text': text,
            'analysis_metadata': {
                'word_count': 0,
                'sentence_count': 0,
                'has_numbers': False,
                'technical_terms': [],
                'negative_impact': 0.0,
                'validation_failed': True
            }
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict[str, int]:
        summary = {'Alta': 0, 'Média': 0, 'Baixa': 0}
        
        for result in results:
            quality_level = result.get('quality_level', 'Baixa')
            summary[quality_level] += 1
        
        return summary
    
    def _create_results_dataframe(self, results: List[Dict]) -> pd.DataFrame:
        simplified_results = []
        
        for result in results:
            simplified = {
                'row_index': result.get('row_index', 0),
                'overall_score': result.get('overall_score', 0.0),
                'quality_level': result.get('quality_level', 'Baixa'),
                'clarity_score': result.get('clarity_score', 0.0),
                'specificity_score': result.get('specificity_score', 0.0),
                'completeness_score': result.get('completeness_score', 0.0),
                'structure_score': result.get('structure_score', 0.0),
                'smart_criteria_score': result.get('smart_criteria_score', 0.0)
            }
            
            # Gerar explicação detalhada da nota
            metadata = result.get('analysis_metadata', {})
            score_explanation = self.quality_service.generate_score_explanation(
                result.get('clarity_score', 0.0),
                result.get('specificity_score', 0.0),
                result.get('completeness_score', 0.0),
                result.get('structure_score', 0.0),
                result.get('smart_criteria_score', 0.0),
                metadata.get('negative_impact', 0.0)
            )
            
            simplified.update({
                'word_count': metadata.get('word_count', 0),
                'sentence_count': metadata.get('sentence_count', 0),
                'has_numbers': metadata.get('has_numbers', False),
                'negative_impact': metadata.get('negative_impact', 0.0),
                'score_explanation': score_explanation  # Nova coluna com explicação detalhada
            })
            
            for key, value in result.items():
                if key not in simplified and key not in ['analysis_metadata', 'original_text']:
                    simplified[key] = value
            
            simplified_results.append(simplified)
        
        return pd.DataFrame(simplified_results)
    
    def save_results(self, results: Dict[str, Any], output_path: str) -> bool:
        try:
            if 'detailed_results' in results and isinstance(results['detailed_results'], pd.DataFrame):
                results['detailed_results'].to_csv(output_path, index=False, encoding='utf-8')
                
                summary_path = output_path.replace('.csv', '_resumo.json')
                summary_data = {
                    'total_analyzed': results.get('total_analyzed', 0),
                    'summary': results.get('summary', {}),
                    'analysis_timestamp': results.get('analysis_timestamp', ''),
                    'success': results.get('success', False)
                }
                
                with open(summary_path, 'w', encoding='utf-8') as f:
                    json.dump(summary_data, f, indent=2, ensure_ascii=False)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Erro ao salvar resultados: {e}")
            return False
    
    def get_quality_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        recommendations = []
        
        if analysis_result.get('clarity_score', 0) < 0.5:
            recommendations.append("Melhore a clareza: use frases mais simples e diretas")
        
        if analysis_result.get('specificity_score', 0) < 0.5:
            recommendations.append("Adicione mais detalhes: números, datas e termos específicos")
        
        if analysis_result.get('completeness_score', 0) < 0.5:
            recommendations.append("Expanda o conteúdo: inclua mais informações sobre o 'como', 'quando' e 'onde'")
        
        if analysis_result.get('structure_score', 0) < 0.5:
            recommendations.append("Melhore a estrutura: use conectores e organize melhor as ideias")
        
        if analysis_result.get('smart_criteria_score', 0) < 0.5:
            recommendations.append("Aplique critérios SMART: torne os objetivos mais específicos, mensuráveis e com prazo")
        
        if not recommendations:
            recommendations.append("PDI de boa qualidade! Continue mantendo este padrão.")
        
        return recommendations
