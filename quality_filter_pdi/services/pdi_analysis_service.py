import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import json

from ..core.config import (
    QUALITY_THRESHOLDS, METRIC_WEIGHTS, COLUMN_MAPPING,
    PROGRESS_INTERVAL
)
from ..services.quality_metrics_service import QualityMetricsService
from ..services.skill_classifier import SkillClassifier
from ..utils.text_utils import TextUtils

# Importação condicional de performance
try:
    from ..core.parallel_processor import ParallelProcessor, create_parallel_analyzer, process_single_pdi_worker
    from ..core.performance_cache import get_cache_stats, clear_all_caches
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False

try:
    from ..ai.ai_text_analyzer import AITextAnalyzer
    from ..ai.advanced_ai_analyzer import AdvancedAIAnalyzer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class PDIAnalysisService:
    
    def __init__(self, 
                 quality_service: Optional[QualityMetricsService] = None,
                 skill_classifier: Optional[SkillClassifier] = None,
                 thresholds: Optional[Dict] = None,
                 ai_enabled: bool = True,
                 enable_parallel: bool = True,
                 enable_cache: bool = True):
        """
        Args:
            enable_parallel: Habilitar processamento paralelo para lotes
            enable_cache: Habilitar cache de performance
        """
        self.quality_service = quality_service or QualityMetricsService(enable_cache=enable_cache)
        self.skill_classifier = skill_classifier or SkillClassifier()
        self.thresholds = thresholds or QUALITY_THRESHOLDS
        self.weights = METRIC_WEIGHTS
        self.column_mapping = COLUMN_MAPPING
        self.enable_parallel = enable_parallel and PERFORMANCE_AVAILABLE
        self.enable_cache = enable_cache
        
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
            self.quality_service.calculate_structure(texto_completo)
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
                
                ai_insights = {
                    'enhancement': ai_enhancement.get('ai_enhancement', {}),
                    'intent_analysis': ai_intent,
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
    
    def _format_score(self, score: float, max_digits: int = 4) -> float:
        """
        Formata um score para garantir que não passe do número máximo de dígitos
        
        Args:
            score: Score original (float)
            max_digits: Número máximo de dígitos (default: 4)
            
        Returns:
            Score formatado limitado aos dígitos especificados
        """
        if score is None or score == 0:
            return 0.0
        
        # Garantir que é um número positivo
        score = abs(float(score))
        
        # Para scores na escala 0-1 (scores individuais), máximo 0.99
        if score <= 1.0:
            return min(round(score, 2), 0.99)  # Máximo 4 dígitos: 0.99
        
        # Para scores na escala 0-100, máximo 99.9
        if score <= 100.0:
            return min(round(score, 1), 99.9)  # Máximo 4 dígitos: 99.9
        
        # Para valores maiores que 100, máximo 999
        if score <= 1000.0:
            return min(float(int(score)), 999.0)  # Máximo 3 dígitos: 999
        
        # Para valores muito grandes, limitar a 999
        return 999.0
    
    def analyze_dataframe_optimized(self, df: pd.DataFrame, use_parallel: bool = None) -> pd.DataFrame:
        """
        Análise otimizada de DataFrame com cache e processamento paralelo
        
        Args:
            df: DataFrame com colunas 'objetivo' e 'acoes'
            use_parallel: Forçar uso (True) ou não uso (False) de paralelo. None = automático
        """
        if use_parallel is None:
            use_parallel = self.enable_parallel and len(df) >= 20
        
        print(f"🔍 Analisando {len(df)} PDIs...")
        if use_parallel and self.enable_parallel:
            print("⚡ Usando processamento paralelo")
            return self._analyze_parallel(df)
        else:
            print("🔄 Usando processamento sequencial")
            return self._analyze_sequential(df)
    
    def _analyze_parallel(self, df: pd.DataFrame) -> pd.DataFrame:
        """Análise paralela otimizada"""
        try:
            # Preparar dados para processamento paralelo
            pdi_data = []
            for idx, row in df.iterrows():
                pdi_data.append({
                    'objetivo': row.get('objetivo', ''),
                    'acoes': row.get('acoes', ''),
                    'atividade': row.get('atividade', ''),
                    'row_index': idx
                })
            
            # Criar processador paralelo otimizado
            processor = create_parallel_analyzer(use_threads=False)
            
            # Processar em paralelo
            results = processor.process_batch(
                pdi_data,
                process_single_pdi_worker,
                chunk_size=max(1, len(pdi_data) // (processor.max_workers * 2))
            )
            
            # Converter para DataFrame
            results_df = pd.DataFrame(results)
            
            # Aplicar formatação de scores
            return self._apply_score_formatting(results_df)
            
        except Exception as e:
            print(f"⚠️ Erro no processamento paralelo: {e}")
            print("🔄 Fallback para processamento sequencial")
            return self._analyze_sequential(df)
    
    def _analyze_sequential(self, df: pd.DataFrame) -> pd.DataFrame:
        """Análise sequencial com cache"""
        results = []
        
        for idx, row in df.iterrows():
            if idx % 50 == 0 and idx > 0:
                print(f"📊 Processados {idx}/{len(df)} PDIs...")
            
            try:
                result = self.analyze_single_pdi(
                    row.get('objetivo', ''),
                    row.get('acoes', ''),
                    row.get('atividade', '')
                )
                result['row_index'] = idx
                results.append(result)
                
            except Exception as e:
                print(f"⚠️ Erro no PDI {idx}: {e}")
                results.append({
                    'row_index': idx,
                    'overall_score': 0.0,
                    'quality_level': 'Baixa',
                    'clarity_score': 0.0,
                    'specificity_score': 0.0,
                    'completeness_score': 0.0,
                    'structure_score': 0.0,
                    'error': str(e)
                })
        
        results_df = pd.DataFrame(results)
        return self._apply_score_formatting(results_df)
    
    def _apply_score_formatting(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica formatação de scores ao DataFrame"""
        score_columns = ['overall_score', 'clarity_score', 'specificity_score', 
                        'completeness_score', 'structure_score']
        
        for col in score_columns:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: self._format_score(x))
        
        return df
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance"""
        if not self.enable_cache:
            return {'cache_enabled': False}
        
        try:
            from ..core.performance_cache import get_cache_stats
            stats = get_cache_stats()
            stats['cache_enabled'] = True
            stats['parallel_enabled'] = self.enable_parallel
            return stats
        except ImportError:
            return {'cache_enabled': False, 'error': 'Performance cache not available'}
    
    def clear_performance_cache(self):
        """Limpa cache de performance"""
        if self.enable_cache:
            try:
                from ..core.performance_cache import clear_all_caches
                clear_all_caches()
                print("✅ Cache de performance limpo")
            except ImportError:
                print("⚠️ Cache de performance não disponível")

    def _create_results_dataframe(self, results: List[Dict]) -> pd.DataFrame:
        simplified_results = []
        
        for result in results:
            simplified = {
                'row_index': result.get('row_index', 0),
                'overall_score': self._format_score(result.get('overall_score', 0.0)),
                'quality_level': result.get('quality_level', 'Baixa'),
                'clarity_score': self._format_score(result.get('clarity_score', 0.0)),
                'specificity_score': self._format_score(result.get('specificity_score', 0.0)),
                'completeness_score': self._format_score(result.get('completeness_score', 0.0)),
                'structure_score': self._format_score(result.get('structure_score', 0.0))
            }
            
            # Gerar explicação detalhada da nota - REMOVIDA do CSV final
            metadata = result.get('analysis_metadata', {})
            # score_explanation = self.quality_service.generate_score_explanation(
            #     result.get('clarity_score', 0.0),
            #     result.get('specificity_score', 0.0),
            #     result.get('completeness_score', 0.0),
            #     result.get('structure_score', 0.0),
            #     result.get('smart_criteria_score', 0.0),
            #     metadata.get('negative_impact', 0.0)
            # )
            
            # Gerar motivos concisos para o CSV (sem emojis, texto direto)
            motivos_concisos = self.quality_service.generate_concise_reasons(
                result.get('clarity_score', 0.0),
                result.get('specificity_score', 0.0),
                result.get('completeness_score', 0.0),
                result.get('structure_score', 0.0),
                metadata.get('negative_impact', 0.0),
                self._format_score(result.get('overall_score', 0.0) * 100)  # Converter para escala 0-100 e formatar
            )
            
            simplified.update({
                'word_count': metadata.get('word_count', 0),
                'sentence_count': metadata.get('sentence_count', 0),
                'motivo_1': motivos_concisos['motivo_1'],  # Novo: Motivo 1 conciso
                'motivo_2': motivos_concisos['motivo_2'],  # Novo: Motivo 2 conciso
                'motivo_3': motivos_concisos['motivo_3']   # Novo: Motivo 3 conciso
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
        
        if not recommendations:
            recommendations.append("PDI de boa qualidade! Continue mantendo este padrão.")
        
        return recommendations
