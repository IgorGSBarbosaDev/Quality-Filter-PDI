"""
Analisador de IA avançado para PDI usando modelos de transformers.

Este módulo fornece análise semântica avançada para avaliação de qualidade
e coesão de PDI usando modelos BERT e técnicas de NLP modernas.
"""

from typing import Dict, List, Optional, Tuple, Union
import re
import logging
import numpy as np
from dataclasses import dataclass

# Configurar logging
logger = logging.getLogger(__name__)

# Importações condicionais para diferentes níveis de IA
try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
    logger.info("Transformers disponível para IA avançada")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers não disponível - usando análise básica")

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("Scikit-learn não disponível - funcionalidade limitada")


@dataclass
class AIAnalysisResult:
    """Resultado da análise de IA."""
    score: float
    confidence: float
    method: str
    details: Dict
    suggestions: List[str]


class AdvancedAIAnalyzer:
    """
    Analisador de IA avançado usando transformers e técnicas de NLP.
    
    Fornece análise semântica sofisticada para avaliação de qualidade
    e coesão de PDI.
    """
    
    def __init__(self):
        """Inicializa o analisador com os modelos apropriados."""
        self.sentiment_analyzer = None
        self.embeddings_model = None
        self.tokenizer = None
        self.use_fallback = False
        
        self._initialize_models()
    
    def _initialize_models(self) -> None:
        """Inicializa os modelos de IA disponíveis."""
        if TRANSFORMERS_AVAILABLE:
            try:
                # Tentar carregar modelo português específico
                model_name = "neuralmind/bert-base-portuguese-cased"
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis", 
                    model=model_name,
                    return_all_scores=True
                )
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                logger.info(f"Modelo BERT português carregado: {model_name}")
                
            except Exception as e:
                logger.warning(f"Erro ao carregar modelo português: {e}")
                try:
                    # Fallback para modelo multilíngue
                    model_name = "bert-base-multilingual-cased"
                    self.sentiment_analyzer = pipeline(
                        "sentiment-analysis", 
                        model=model_name,
                        return_all_scores=True
                    )
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    logger.info(f"Modelo BERT multilíngue carregado: {model_name}")
                    
                except Exception as e2:
                    logger.error(f"Erro ao carregar modelo multilíngue: {e2}")
                    self._setup_fallback()
        else:
            self._setup_fallback()
    
    def _setup_fallback(self) -> None:
        """Configura análise de fallback sem transformers."""
        logger.info("Usando análise baseada em regras como fallback")
        self.use_fallback = True
    
    
    def analyze_goal_cohesion_ai(self, objetivo: str, acoes: str, atividades: str = "") -> Dict:
        """
        Análise avançada de coesão usando IA semântica.
        
        Analisa a coerência entre objetivo e ações/atividades usando:
        - Similaridade semântica (35%)
        - Sobreposição de categorias (25%) 
        - Completude (20%)
        - Praticidade (15%)
        - Alinhamento de intenção (5%)
        
        Args:
            objetivo: Texto do objetivo de desenvolvimento
            acoes: Texto das ações planejadas
            atividades: Texto das atividades de aprendizagem
            
        Returns:
            Dict com score, nível e detalhes da análise
        """
        if not objetivo:
            return self._create_cohesion_result(0.0, "muito ruim", "AI_ADVANCED", [])
        
        # Aplicar lógica inteligente de campos vazios (igual ao método tradicional)
        fields_to_analyze = []
        used_fields = []
        
        if acoes and acoes.strip():
            fields_to_analyze.append(acoes.strip())
            used_fields.append("acoes")
        
        if atividades and atividades.strip():
            fields_to_analyze.append(atividades.strip())
            used_fields.append("atividades")
        
        # Se nenhum campo tem conteúdo, retorna score baixo
        if not fields_to_analyze:
            return self._create_cohesion_result(0.0, "muito ruim", "AI_ADVANCED", [])
        
        # Combinar apenas campos com conteúdo
        actions_combined = " ".join(fields_to_analyze).strip()
        
        # Usar IA se disponível, senão fallback
        if self.use_fallback:
            return self._fallback_cohesion_analysis(objetivo, actions_combined, used_fields)
        
        try:
            # Análise semântica avançada com IA
            semantic_score = self._calculate_semantic_similarity(objetivo, actions_combined)
            category_score = self._analyze_category_overlap(objetivo, actions_combined) 
            completeness_score = self._assess_completeness(objetivo, actions_combined)
            practicality_score = self._evaluate_practicality(actions_combined)
            intent_score = self._analyze_intent_alignment(objetivo, actions_combined)
            
            # Calcular score final com pesos definidos
            final_score = (
                semantic_score * 0.35 +      # 35% - Similaridade semântica
                category_score * 0.25 +      # 25% - Sobreposição de categorias
                completeness_score * 0.20 +  # 20% - Completude
                practicality_score * 0.15 +  # 15% - Praticidade
                intent_score * 0.05          # 5% - Alinhamento de intenção
            )
            
            # Garantir que está entre 0 e 1
            final_score = max(0.0, min(1.0, final_score))
            
            # Categorizar o resultado
            level = self._categorize_cohesion_score(final_score)
            
            return self._create_cohesion_result(
                final_score, level, "AI_ADVANCED", used_fields,
                details={
                    'semantic_similarity': semantic_score,
                    'category_overlap': category_score,
                    'completeness': completeness_score,
                    'practicality': practicality_score,
                    'intent_alignment': intent_score,
                    'used_fields': len(used_fields)
                }
            )
            
        except Exception as e:
            logger.error(f"Erro na análise AI: {e}")
            return self._fallback_cohesion_analysis(objetivo, actions_combined, used_fields)
    
    def _calculate_semantic_similarity(self, objetivo: str, actions: str) -> float:
        """Calcula similaridade semântica entre objetivo e ações."""
        try:
            if not SKLEARN_AVAILABLE:
                return self._simple_word_overlap(objetivo, actions)
            
            # Usar TF-IDF para vectorização
            vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 2))
            corpus = [objetivo.lower(), actions.lower()]
            
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            # Calcular similaridade coseno
            similarity_matrix = cosine_similarity(tfidf_matrix)
            similarity_score = similarity_matrix[0, 1]
            
            return max(0.0, min(1.0, similarity_score))
            
        except Exception as e:
            logger.warning(f"Erro no cálculo de similaridade: {e}")
            return self._simple_word_overlap(objetivo, actions)
    
    def _simple_word_overlap(self, text1: str, text2: str) -> float:
        """Fallback simples para similaridade baseada em overlap de palavras."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _analyze_category_overlap(self, objetivo: str, actions: str) -> float:
        """Analisa sobreposição de categorias/domínios."""
        # Categorias de desenvolvimento profissional
        categories = {
            'technical': ['python', 'sql', 'excel', 'sap', 'programacao', 'sistema', 'software', 'dados'],
            'leadership': ['lideranca', 'gestao', 'equipe', 'coordenacao', 'supervisao'],
            'communication': ['comunicacao', 'apresentacao', 'relatorio', 'reuniao', 'feedback'],
            'process': ['processo', 'melhoria', 'otimizacao', 'eficiencia', 'qualidade'],
            'learning': ['curso', 'treinamento', 'capacitacao', 'estudo', 'certificacao']
        }
        
        objetivo_lower = objetivo.lower()
        actions_lower = actions.lower()
        
        objetivo_categories = set()
        actions_categories = set()
        
        for category, keywords in categories.items():
            if any(keyword in objetivo_lower for keyword in keywords):
                objetivo_categories.add(category)
            if any(keyword in actions_lower for keyword in keywords):
                actions_categories.add(category)
        
        if not objetivo_categories or not actions_categories:
            return 0.3  # Score neutro se não encontrar categorias
        
        intersection = objetivo_categories.intersection(actions_categories)
        union = objetivo_categories.union(actions_categories)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _assess_completeness(self, objetivo: str, actions: str) -> float:
        """Avalia se as ações são completas em relação ao objetivo."""
        # Fatores de completude
        factors = {
            'length_ratio': min(1.0, len(actions) / max(len(objetivo), 1)),
            'has_timeline': 1.0 if self._has_timeline_indicators(actions) else 0.0,
            'has_specific_actions': 1.0 if self._has_specific_actions(actions) else 0.5,
            'covers_objective': self._calculate_objective_coverage(objetivo, actions)
        }
        
        # Média ponderada dos fatores
        completeness_score = (
            factors['length_ratio'] * 0.3 +
            factors['has_timeline'] * 0.2 +
            factors['has_specific_actions'] * 0.3 +
            factors['covers_objective'] * 0.2
        )
        
        return max(0.0, min(1.0, completeness_score))
    
    def _has_timeline_indicators(self, text: str) -> bool:
        """Verifica se o texto contém indicadores de prazo."""
        timeline_patterns = [
            r'\b\d+\s*(dia|semana|mes|mês|ano|hora)s?\b',
            r'\b(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\b',
            r'\b\d{1,2}/\d{1,2}(/\d{2,4})?\b',
            r'\b(até|prazo|deadline|cronograma)\b'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in timeline_patterns)
    
    def _has_specific_actions(self, text: str) -> bool:
        """Verifica se o texto contém ações específicas."""
        action_verbs = [
            'fazer', 'realizar', 'executar', 'implementar', 'desenvolver',
            'criar', 'estudar', 'aprender', 'praticar', 'aplicar',
            'participar', 'concluir', 'obter', 'alcançar'
        ]
        
        text_lower = text.lower()
        action_count = sum(1 for verb in action_verbs if verb in text_lower)
        
        return action_count >= 2  # Pelo menos 2 verbos de ação
    
    def _calculate_objective_coverage(self, objetivo: str, actions: str) -> float:
        """Calcula o quanto as ações cobrem o objetivo."""
        objetivo_words = set(objetivo.lower().split())
        actions_words = set(actions.lower().split())
        
        # Remover palavras muito comuns
        stop_words = {'de', 'da', 'do', 'para', 'em', 'com', 'por', 'a', 'o', 'e', 'que', 'se'}
        objetivo_words -= stop_words
        actions_words -= stop_words
        
        if not objetivo_words:
            return 0.0
        
        covered_words = objetivo_words.intersection(actions_words)
        coverage_ratio = len(covered_words) / len(objetivo_words)
        
        return min(1.0, coverage_ratio * 1.5)  # Multiplicador para dar mais peso
    
    def _evaluate_practicality(self, actions: str) -> float:
        """Avalia a praticidade das ações propostas."""
        practicality_factors = {
            'has_concrete_steps': 1.0 if self._has_concrete_steps(actions) else 0.0,
            'realistic_scope': self._assess_realistic_scope(actions),
            'measurable_outcomes': 1.0 if self._has_measurable_outcomes(actions) else 0.5
        }
        
        return sum(practicality_factors.values()) / len(practicality_factors)
    
    def _has_concrete_steps(self, text: str) -> bool:
        """Verifica se há passos concretos nas ações."""
        concrete_indicators = [
            'primeiro', 'segundo', 'terceiro', 'inicialmente', 'depois',
            'em seguida', 'finalmente', 'etapa', 'fase', 'passo'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in concrete_indicators)
    
    def _assess_realistic_scope(self, text: str) -> float:
        """Avalia se o escopo é realista."""
        # Indicadores de escopo muito amplo (penalizam)
        overly_broad = ['tudo', 'todos', 'toda', 'completo', 'total', 'máximo']
        
        # Indicadores de escopo específico (favorecem)
        specific_scope = ['específico', 'focado', 'direcionado', 'particular']
        
        text_lower = text.lower()
        
        broad_count = sum(1 for term in overly_broad if term in text_lower)
        specific_count = sum(1 for term in specific_scope if term in text_lower)
        
        # Score baseado na especificidade vs generalização
        if broad_count > specific_count:
            return 0.3  # Escopo muito amplo
        elif specific_count > 0:
            return 1.0  # Escopo específico
        else:
            return 0.7  # Neutro
    
    def _has_measurable_outcomes(self, text: str) -> bool:
        """Verifica se há resultados mensuráveis."""
        measurable_patterns = [
            r'\b\d+%?\b',  # Números e percentuais
            r'\b(certificação|diploma|nota|score|resultado)\b',
            r'\b(melhorar|aumentar|reduzir)\s+em\s+\d+\b'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in measurable_patterns)
    
    def _analyze_intent_alignment(self, objetivo: str, actions: str) -> float:
        """Analisa se a intenção das ações está alinhada com o objetivo."""
        # Tipos de intenção
        intent_types = {
            'learning': ['aprender', 'estudar', 'conhecer', 'entender'],
            'improving': ['melhorar', 'aprimorar', 'desenvolver', 'crescer'],
            'achieving': ['atingir', 'alcançar', 'obter', 'conseguir'],
            'implementing': ['implementar', 'aplicar', 'executar', 'realizar']
        }
        
        objetivo_lower = objetivo.lower()
        actions_lower = actions.lower()
        
        objetivo_intents = set()
        actions_intents = set()
        
        for intent_type, keywords in intent_types.items():
            if any(keyword in objetivo_lower for keyword in keywords):
                objetivo_intents.add(intent_type)
            if any(keyword in actions_lower for keyword in keywords):
                actions_intents.add(intent_type)
        
        if not objetivo_intents or not actions_intents:
            return 0.5  # Neutro se não conseguir identificar intenções
        
        # Calcular alinhamento de intenções
        aligned_intents = objetivo_intents.intersection(actions_intents)
        total_intents = objetivo_intents.union(actions_intents)
        
        return len(aligned_intents) / len(total_intents) if total_intents else 0.0
    
    def _categorize_cohesion_score(self, score: float) -> str:
        """Categoriza o score de coesão em níveis textuais."""
        if score >= 0.8:
            return "otimo"
        elif score >= 0.6:
            return "bom"
        elif score >= 0.4:
            return "medio"
        elif score >= 0.2:
            return "ruim"
        else:
            return "muito ruim"
    
    def _create_cohesion_result(self, score: float, level: str, method: str, 
                                used_fields: List[str], details: Optional[Dict] = None) -> Dict:
        """Cria resultado padronizado da análise de coesão."""
        return {
            'cohesion_score': score,
            'cohesion_level': level,
            'analysis_method': method,
            'ai_enabled': not self.use_fallback,
            'used_fields': used_fields,
            'analysis_details': details or {}
        }
    
    def _fallback_cohesion_analysis(self, objetivo: str, actions: str, used_fields: List[str]) -> Dict:
        """Análise de fallback quando IA não está disponível."""
        # Implementação similar ao método tradicional mas simplificada
        similarity = self._simple_word_overlap(objetivo, actions)
        
        # Ajustes baseados em heurísticas simples
        if len(actions) > len(objetivo) * 0.8:
            similarity += 0.1  # Bônus por ações detalhadas
        
        if any(word in actions.lower() for word in ['curso', 'treinamento', 'certificacao']):
            similarity += 0.1  # Bônus por ações educacionais
        
        final_score = max(0.0, min(1.0, similarity))
        level = self._categorize_cohesion_score(final_score)
        
        return self._create_cohesion_result(
            final_score, level, "AI_FALLBACK", used_fields,
            details={'similarity_score': similarity}
        )
            
            category_scores = {}
            text_lower = full_text.lower()
            
            for category, keywords in intent_categories.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                category_scores[category] = score / len(keywords)
            
            primary_category = max(category_scores, key=category_scores.get)
            
            return {
                'primary_intent': primary_category,
                'confidence': category_scores[primary_category],
                'sentiment': sentiment[0] if sentiment else {'label': 'NEUTRAL', 'score': 0.5},
                'all_categories': category_scores,
                'ai_processed': True
            }
            
        except Exception as e:
            print(f"⚠️ Erro na análise AI: {e}")
            return self._fallback_intent_analysis(full_text)
    
    def _fallback_intent_analysis(self, text: str) -> Dict:
        text_lower = text.lower()
        
        technical_indicators = len(re.findall(r'\b(?:python|java|excel|sap|sql|aws|azure)\b', text_lower))
        soft_indicators = len(re.findall(r'\b(?:liderança|comunicação|equipe|empatia)\b', text_lower))
        learning_indicators = len(re.findall(r'\b(?:aprender|estudar|curso|treinamento)\b', text_lower))
        
        scores = {
            'technical_skill': technical_indicators / 5,
            'soft_skill': soft_indicators / 4,
            'learning_development': learning_indicators / 4,
            'process_improvement': 0.3
        }
        
        primary = max(scores, key=scores.get)
        
        return {
            'primary_intent': primary,
            'confidence': scores[primary],
            'sentiment': {'label': 'POSITIVE', 'score': 0.7},
            'all_categories': scores,
            'ai_processed': False
        }
    
    def extract_learning_objectives(self, text: str) -> List[Dict]:
        objectives = []
        
        # Padrões para identificar objetivos de aprendizagem
        patterns = [
            r'aprender\s+(.+?)(?:\.|$|,)',
            r'desenvolver\s+(.+?)(?:\.|$|,)',
            r'obter\s+(.+?)(?:\.|$|,)',
            r'melhorar\s+(.+?)(?:\.|$|,)',
            r'dominar\s+(.+?)(?:\.|$|,)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                objectives.append({
                    'objective': match.strip(),
                    'type': self._classify_objective_type(match),
                    'complexity': self._estimate_complexity(match)
                })
        
        return objectives[:5]  # Limitar a 5 objetivos principais
    
    def _classify_objective_type(self, objective: str) -> str:
        tech_keywords = ['python', 'excel', 'sap', 'sql', 'programação', 'sistema']
        soft_keywords = ['liderança', 'comunicação', 'equipe', 'relacionamento']
        
        if any(keyword in objective for keyword in tech_keywords):
            return 'technical'
        elif any(keyword in objective for keyword in soft_keywords):
            return 'behavioral'
        else:
            return 'general'
    
    def _estimate_complexity(self, objective: str) -> str:
        complex_indicators = ['avançado', 'certificação', 'especialização', 'mestrado']
        basic_indicators = ['básico', 'introdução', 'fundamentos', 'inicial']
        
        if any(indicator in objective for indicator in complex_indicators):
            return 'high'
        elif any(indicator in objective for indicator in basic_indicators):
            return 'low'
        else:
            return 'medium'
    
    def analyze_action_alignment(self, objetivo: str, acoes: str) -> Dict:
        if not acoes:
            return {
                'alignment_score': 0.2,
                'missing_actions': True,
                'suggestions': ["📝 Adicione ações específicas para alcançar o objetivo"]
            }
        
        objetivo_words = set(objetivo.lower().split())
        acoes_words = set(acoes.lower().split())
        
        # Calcular sobreposição semântica básica
        overlap = len(objetivo_words.intersection(acoes_words))
        total_unique = len(objetivo_words.union(acoes_words))
        
        alignment_score = overlap / total_unique if total_unique > 0 else 0
        
        # Boost para ações específicas
        specific_action_words = ['curso', 'treinamento', 'prática', 'projeto', 'estudo']
        if any(word in acoes.lower() for word in specific_action_words):
            alignment_score += 0.2
        
        # Boost para prazos
        if re.search(r'\b(?:até|em|durante)\s+\w+', acoes.lower()):
            alignment_score += 0.15
        
        alignment_score = min(alignment_score, 1.0)
        
        suggestions = []
        if alignment_score < 0.6:
            suggestions.extend([
                "🔗 Alinhe melhor as ações com o objetivo principal",
                "📋 Adicione mais detalhes sobre como executar"
            ])
        
        return {
            'alignment_score': alignment_score,
            'missing_actions': False,
            'suggestions': suggestions
        }
    
    def analyze_goal_cohesion_ai(self, objetivo: str, acoes: str, atividades: str = "") -> Dict:
        """
        Análise de coesão da meta usando IA avançada.
        
        Utiliza análise semântica profunda para avaliar alinhamento entre objetivo e ações.
        """
        if hasattr(self, 'use_fallback'):
            return self._fallback_cohesion_analysis(objetivo, acoes, atividades)
        
        try:
            # Combinar campos com conteúdo (lógica inteligente)
            campos_com_conteudo = []
            if acoes and acoes.strip():
                campos_com_conteudo.append(acoes.strip())
            if atividades and atividades.strip():
                campos_com_conteudo.append(atividades.strip())
            
            if not campos_com_conteudo:
                return {
                    'cohesion_score': 0.0,
                    'cohesion_level': 'muito ruim',
                    'ai_confidence': 1.0,
                    'analysis_details': 'Nenhuma ação ou atividade encontrada'
                }
            
            acoes_combined = " ".join(campos_com_conteudo)
            
            # 1. Análise de Sentimento e Intenção
            objetivo_analysis = self._analyze_text_intent(objetivo)
            acoes_analysis = self._analyze_text_intent(acoes_combined)
            
            # 2. Análise de Similaridade Semântica
            semantic_similarity = self._calculate_semantic_similarity(objetivo, acoes_combined)
            
            # 3. Análise de Categorias e Domínios
            objetivo_categories = self._extract_categories(objetivo)
            acoes_categories = self._extract_categories(acoes_combined)
            category_overlap = self._calculate_category_overlap(objetivo_categories, acoes_categories)
            
            # 4. Análise de Completude das Ações
            completeness_score = self._analyze_action_completeness(objetivo, acoes_combined)
            
            # 5. Análise de Especificidade e Praticidade
            practicality_score = self._analyze_action_practicality(acoes_combined)
            
            # Calcular score final com pesos baseados em IA
            final_score = (
                semantic_similarity * 0.35 +      # 35% - Similaridade semântica
                category_overlap * 0.25 +         # 25% - Overlap de categorias
                completeness_score * 0.20 +       # 20% - Completude das ações
                practicality_score * 0.15 +       # 15% - Praticidade das ações
                self._calculate_intent_alignment(objetivo_analysis, acoes_analysis) * 0.05  # 5% - Alinhamento de intenção
            )
            
            # Garantir que o score esteja entre 0 e 1
            final_score = max(0.0, min(1.0, final_score))
            
            # Classificar em níveis
            if final_score >= 0.85:
                level = 'otimo'
            elif final_score >= 0.70:
                level = 'bom'
            elif final_score >= 0.50:
                level = 'medio'
            elif final_score >= 0.25:
                level = 'ruim'
            else:
                level = 'muito ruim'
            
            # Calcular confiança da IA
            confidence = min(1.0, (semantic_similarity + category_overlap) / 2)
            
            return {
                'cohesion_score': final_score,
                'cohesion_level': level,
                'ai_confidence': confidence,
                'analysis_details': {
                    'semantic_similarity': semantic_similarity,
                    'category_overlap': category_overlap,
                    'completeness_score': completeness_score,
                    'practicality_score': practicality_score,
                    'objective_categories': objetivo_categories,
                    'actions_categories': acoes_categories,
                    'used_fields': len(campos_com_conteudo)
                }
            }
            
        except Exception as e:
            print(f"⚠️ Erro na análise AI de coesão: {e}")
            return self._fallback_cohesion_analysis(objetivo, acoes, atividades)
    
    def _analyze_text_intent(self, text: str) -> Dict:
        """Analisa a intenção do texto usando IA"""
        try:
            if self.sentiment_analyzer:
                sentiment = self.sentiment_analyzer(text)
                return {
                    'sentiment': sentiment[0]['label'],
                    'confidence': sentiment[0]['score']
                }
        except:
            pass
        
        return {'sentiment': 'NEUTRAL', 'confidence': 0.5}
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade semântica entre dois textos"""
        try:
            # Análise baseada em palavras-chave semânticas aprimorada
            keywords_tech = {
                'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'azure',
                'excel', 'powerbi', 'tableau', 'sap', 'salesforce', 'git', 'docker'
            }
            
            keywords_soft = {
                'lideranca', 'gestao', 'comunicacao', 'apresentacao', 'negociacao',
                'vendas', 'marketing', 'atendimento', 'relacionamento', 'equipe'
            }
            
            keywords_process = {
                'processo', 'melhoria', 'otimizacao', 'eficiencia', 'produtividade',
                'qualidade', 'metodologia', 'agil', 'scrum', 'lean'
            }
            
            text1_lower = text1.lower()
            text2_lower = text2.lower()
            
            # Verificar sobreposição em cada categoria
            tech_overlap = self._check_keyword_overlap(text1_lower, text2_lower, keywords_tech)
            soft_overlap = self._check_keyword_overlap(text1_lower, text2_lower, keywords_soft)
            process_overlap = self._check_keyword_overlap(text1_lower, text2_lower, keywords_process)
            
            # Score baseado na melhor categoria
            max_overlap = max(tech_overlap, soft_overlap, process_overlap)
            
            # Bonus por palavras de ação alinhadas
            action_words = {
                'desenvolver', 'aprender', 'melhorar', 'implementar', 'criar',
                'estudar', 'praticar', 'dominar', 'aplicar', 'executar'
            }
            action_overlap = self._check_keyword_overlap(text1_lower, text2_lower, action_words)
            
            return min(1.0, max_overlap + (action_overlap * 0.3))
            
        except Exception:
            return 0.3  # Fallback básico
    
    def _check_keyword_overlap(self, text1: str, text2: str, keywords: set) -> float:
        """Verifica sobreposição de palavras-chave entre dois textos"""
        text1_keywords = {word for word in keywords if word in text1}
        text2_keywords = {word for word in keywords if word in text2}
        
        if not text1_keywords or not text2_keywords:
            return 0.0
        
        intersection = text1_keywords.intersection(text2_keywords)
        union = text1_keywords.union(text2_keywords)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _extract_categories(self, text: str) -> List[str]:
        """Extrai categorias do texto"""
        categories = []
        text_lower = text.lower()
        
        category_keywords = {
            'tecnologia': ['python', 'java', 'sql', 'excel', 'powerbi', 'aws', 'programacao'],
            'gestao': ['lideranca', 'gestao', 'equipe', 'gerenciamento', 'coordenacao'],
            'vendas': ['vendas', 'comercial', 'negociacao', 'cliente', 'prospeccao'],
            'comunicacao': ['apresentacao', 'comunicacao', 'oratoria', 'redacao'],
            'analise': ['analise', 'dados', 'relatorio', 'dashboard', 'metricas'],
            'processo': ['processo', 'melhoria', 'otimizacao', 'metodologia'],
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        return categories
    
    def _calculate_category_overlap(self, categories1: List[str], categories2: List[str]) -> float:
        """Calcula sobreposição entre categorias"""
        if not categories1 or not categories2:
            return 0.0
        
        set1 = set(categories1)
        set2 = set(categories2)
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _analyze_action_completeness(self, objetivo: str, acoes: str) -> float:
        """Analisa se as ações são completas em relação ao objetivo"""
        # Verifica se as ações incluem elementos de execução
        execution_indicators = {
            'fazer', 'executar', 'realizar', 'implementar', 'praticar',
            'estudar', 'curso', 'treinamento', 'projeto', 'exercicio'
        }
        
        acoes_lower = acoes.lower()
        execution_count = sum(1 for indicator in execution_indicators if indicator in acoes_lower)
        
        # Bonus por detalhes específicos
        detail_indicators = {
            'horas', 'dias', 'semanas', 'meses', 'ate', 'durante',
            'online', 'presencial', 'certificacao', 'diploma'
        }
        
        detail_count = sum(1 for detail in detail_indicators if detail in acoes_lower)
        
        # Score baseado na presença de indicadores
        completeness = (execution_count * 0.3) + (detail_count * 0.2)
        
        return min(1.0, completeness)
    
    def _analyze_action_practicality(self, acoes: str) -> float:
        """Analisa a praticidade das ações propostas"""
        practical_indicators = {
            'curso', 'treinamento', 'workshop', 'certificacao', 'livro',
            'documentacao', 'tutorial', 'video', 'online', 'presencial',
            'projeto', 'pratica', 'exercicio', 'estudo'
        }
        
        acoes_lower = acoes.lower()
        practical_count = sum(1 for indicator in practical_indicators if indicator in acoes_lower)
        
        # Penalizar ações muito vagas
        vague_indicators = {'melhorar', 'desenvolver', 'aprender'} 
        vague_count = sum(1 for vague in vague_indicators if vague in acoes_lower)
        
        practicality = (practical_count * 0.2) - (vague_count * 0.1)
        
        return max(0.0, min(1.0, practicality))
    
    def _calculate_intent_alignment(self, objetivo_analysis: Dict, acoes_analysis: Dict) -> float:
        """Calcula alinhamento de intenção entre objetivo e ações"""
        # Se ambos têm sentimento positivo, há melhor alinhamento
        if (objetivo_analysis.get('sentiment') == 'POSITIVE' and 
            acoes_analysis.get('sentiment') == 'POSITIVE'):
            return 0.8
        elif (objetivo_analysis.get('sentiment') == acoes_analysis.get('sentiment')):
            return 0.6
        else:
            return 0.3
    
    def _fallback_cohesion_analysis(self, objetivo: str, acoes: str, atividades: str) -> Dict:
        """Análise de fallback quando IA não está disponível"""
        # Usar análise básica por palavras-chave
        objetivo_words = set(objetivo.lower().split())
        
        campos_com_conteudo = []
        if acoes and acoes.strip():
            campos_com_conteudo.append(acoes.strip())
        if atividades and atividades.strip():
            campos_com_conteudo.append(atividades.strip())
        
        if not campos_com_conteudo:
            return {
                'cohesion_score': 0.0,
                'cohesion_level': 'muito ruim',
                'ai_confidence': 1.0,
                'analysis_details': 'Análise básica - campos vazios'
            }
        
        acoes_words = set(" ".join(campos_com_conteudo).lower().split())
        
        # Cálculo simples de sobreposição
        intersection = objetivo_words.intersection(acoes_words)
        union = objetivo_words.union(acoes_words)
        
        basic_score = len(intersection) / len(union) if union else 0.0
        
        # Classificação
        if basic_score >= 0.4:
            level = 'bom'
        elif basic_score >= 0.2:
            level = 'medio'
        else:
            level = 'ruim'
        
        return {
            'cohesion_score': basic_score,
            'cohesion_level': level,
            'ai_confidence': 0.5,
            'analysis_details': 'Análise básica por palavras-chave'
        }
