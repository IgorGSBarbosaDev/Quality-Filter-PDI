from typing import Dict, List, Optional
import re
import numpy as np

try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class AdvancedAIAnalyzer:
    
    def __init__(self):
        self.sentiment_analyzer = None
        self.text_classifier = None
        self.embeddings_model = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                                 model="neuralmind/bert-base-portuguese-cased")
                self.text_classifier = pipeline("text-classification",
                                               model="neuralmind/bert-base-portuguese-cased")
                print("✅ Modelos AI carregados com sucesso")
            except Exception as e:
                print(f"⚠️ Erro ao carregar modelos: {e}")
                self._setup_fallback()
        else:
            self._setup_fallback()
    
    def _setup_fallback(self):
        print("🔄 Usando análise baseada em regras como fallback")
        self.use_fallback = True
    
    def analyze_pdi_intent(self, objetivo: str, acoes: str = "") -> Dict:
        full_text = f"{objetivo} {acoes}".strip()
        
        if hasattr(self, 'use_fallback'):
            return self._fallback_intent_analysis(full_text)
        
        try:
            sentiment = self.sentiment_analyzer(full_text)
            
            intent_categories = {
                'technical_skill': ['python', 'excel', 'sap', 'sql', 'aws', 'certificação'],
                'soft_skill': ['liderança', 'comunicação', 'trabalho em equipe', 'empatia'],
                'process_improvement': ['melhorar', 'otimizar', 'eficiência', 'produtividade'],
                'learning_development': ['aprender', 'estudar', 'desenvolver', 'curso']
            }
            
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
