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
