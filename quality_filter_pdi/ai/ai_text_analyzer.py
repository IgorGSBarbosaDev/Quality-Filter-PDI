import spacy
from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AITextAnalyzer:
    
    def __init__(self):
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except OSError:
            print("⚠️ Modelo português não encontrado. Usando modelo base.")
            self.nlp = None
        
        self.skill_vectors = None
        self.quality_patterns = {
            'clarity_indicators': ['claro', 'específico', 'objetivo', 'meta', 'foco'],
            'specificity_indicators': ['até', 'em', 'durante', 'através', 'usando'],
            'completeness_indicators': ['para', 'com objetivo', 'visando', 'a fim de']
        }
    
    def extract_semantic_features(self, text: str) -> Dict:
        features = {
            'entities': [],
            'intent_keywords': [],
            'action_verbs': [],
            'time_expressions': [],
            'technical_terms': [],
            'semantic_score': 0.0
        }
        
        if not self.nlp:
            return self._fallback_analysis(text)
        
        doc = self.nlp(text)
        
        for ent in doc.ents:
            features['entities'].append({
                'text': ent.text,
                'label': ent.label_,
                'confidence': 1.0
            })
        
        for token in doc:
            if token.pos_ == 'VERB' and not token.is_stop:
                features['action_verbs'].append(token.lemma_)
            elif token.like_num or token.ent_type_ == 'DATE':
                features['time_expressions'].append(token.text)
        
        features['semantic_score'] = self._calculate_semantic_coherence(doc)
        
        return features
    
    def _fallback_analysis(self, text: str) -> Dict:
        import re
        
        features = {
            'entities': [],
            'intent_keywords': [],
            'action_verbs': [],
            'time_expressions': [],
            'technical_terms': [],
            'semantic_score': 0.5
        }
        
        action_verbs = re.findall(r'\b(?:aprender|desenvolver|obter|melhorar|estudar|praticar|aplicar|dominar)\b', text.lower())
        features['action_verbs'] = list(set(action_verbs))
        
        time_expressions = re.findall(r'\b(?:\d+\s*(?:dias?|semanas?|meses?|anos?)|até\s+\w+|durante\s+\w+)\b', text.lower())
        features['time_expressions'] = time_expressions
        
        tech_terms = re.findall(r'\b(?:python|java|excel|sap|sql|aws|azure|machine learning|ia)\b', text.lower())
        features['technical_terms'] = list(set(tech_terms))
        
        return features
    
    def _calculate_semantic_coherence(self, doc) -> float:
        try:
            if len(doc) < 3:
                return 0.3
            
            coherence_score = 0.0
            
            verbs = [token for token in doc if token.pos_ == 'VERB']
            nouns = [token for token in doc if token.pos_ == 'NOUN']
            
            if len(verbs) > 0 and len(nouns) > 0:
                coherence_score += 0.4
            
            if any(ent.label_ in ['PERSON', 'ORG', 'DATE', 'TIME'] for ent in doc.ents):
                coherence_score += 0.3
            
            avg_similarity = self._calculate_token_similarity(doc)
            coherence_score += avg_similarity * 0.3
            
            return min(coherence_score, 1.0)
            
        except Exception:
            return 0.5
    
    def _calculate_token_similarity(self, doc) -> float:
        try:
            vectors = [token.vector for token in doc if token.has_vector and not token.is_stop]
            if len(vectors) < 2:
                return 0.5
            
            similarities = []
            for i in range(len(vectors)):
                for j in range(i+1, len(vectors)):
                    sim = np.dot(vectors[i], vectors[j]) / (np.linalg.norm(vectors[i]) * np.linalg.norm(vectors[j]))
                    similarities.append(sim)
            
            return np.mean(similarities) if similarities else 0.5
            
        except Exception:
            return 0.5
    
    def classify_intent(self, text: str) -> Dict:
        intent_patterns = {
            'learning': ['aprender', 'estudar', 'curso', 'treinamento', 'capacitação'],
            'improving': ['melhorar', 'aprimorar', 'desenvolver', 'fortalecer'],
            'obtaining': ['obter', 'conseguir', 'alcançar', 'certificação'],
            'applying': ['aplicar', 'praticar', 'implementar', 'utilizar']
        }
        
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, keywords in intent_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            intent_scores[intent] = score / len(keywords)
        
        primary_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[primary_intent]
        
        return {
            'primary_intent': primary_intent,
            'confidence': confidence,
            'all_scores': intent_scores
        }
    
    def enhance_quality_analysis(self, text: str, base_scores: Dict) -> Dict:
        semantic_features = self.extract_semantic_features(text)
        intent_analysis = self.classify_intent(text)
        
        ai_enhancement = {
            'semantic_coherence': semantic_features['semantic_score'],
            'intent_clarity': intent_analysis['confidence'],
            'entity_richness': len(semantic_features['entities']) / 10,
            'action_orientation': len(semantic_features['action_verbs']) / 5,
            'temporal_specificity': len(semantic_features['time_expressions']) / 3
        }
        
        ai_boost = sum(ai_enhancement.values()) / len(ai_enhancement) * 0.15
        
        enhanced_scores = base_scores.copy()
        enhanced_scores['ai_enhancement'] = ai_enhancement
        enhanced_scores['ai_boost'] = ai_boost
        enhanced_scores['enhanced_overall_score'] = min(base_scores.get('overall_score', 0) + ai_boost, 1.0)
        
        return enhanced_scores
