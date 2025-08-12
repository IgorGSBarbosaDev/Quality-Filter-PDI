"""
Processador de texto para análise de PDI
"""
import re
import string
from typing import List, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import textstat

class TextProcessor:
    def __init__(self):
        self._download_nltk_data()
        self.stop_words = set(stopwords.words('portuguese'))
    
    def _download_nltk_data(self):
        """Download dados necessários do NLTK"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    def clean_text(self, text: str) -> str:
        """Limpa e normaliza o texto"""
        if not isinstance(text, str):
            return ""
        
        # Remove caracteres especiais, mantém apenas letras, números e espaços
        text = re.sub(r'[^\w\s]', ' ', text)
        # Remove espaços múltiplos
        text = re.sub(r'\s+', ' ', text)
        # Remove espaços no início e fim
        text = text.strip()
        
        return text.lower()
    
    def tokenize_words(self, text: str) -> List[str]:
        """Tokeniza o texto em palavras"""
        clean = self.clean_text(text)
        tokens = word_tokenize(clean, language='portuguese')
        # Remove stopwords e palavras muito curtas
        return [word for word in tokens if word not in self.stop_words and len(word) > 2]
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """Tokeniza o texto em sentenças"""
        if not isinstance(text, str):
            return []
        return sent_tokenize(text, language='portuguese')
    
    def get_word_count(self, text: str) -> int:
        """Conta o número de palavras"""
        return len(self.tokenize_words(text))
    
    def get_sentence_count(self, text: str) -> int:
        """Conta o número de sentenças"""
        return len(self.tokenize_sentences(text))
    
    def get_readability_score(self, text: str) -> float:
        """Calcula pontuação de legibilidade"""
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        try:
            # Usa Flesch Reading Ease adaptado para português
            score = textstat.flesch_reading_ease(text)
            # Normaliza para 0-1
            return max(0, min(1, score / 100))
        except:
            return 0.5  # Score neutro em caso de erro
    
    def has_keywords(self, text: str, keywords: List[str]) -> bool:
        """Verifica se o texto contém alguma das palavras-chave"""
        clean = self.clean_text(text)
        return any(keyword.lower() in clean for keyword in keywords)
    
    def count_keywords(self, text: str, keywords: List[str]) -> int:
        """Conta quantas palavras-chave estão presentes"""
        clean = self.clean_text(text)
        return sum(1 for keyword in keywords if keyword.lower() in clean)
    
    def extract_metrics(self, text: str) -> Dict[str, any]:
        """Extrai métricas básicas do texto"""
        return {
            'word_count': self.get_word_count(text),
            'sentence_count': self.get_sentence_count(text),
            'char_count': len(text) if isinstance(text, str) else 0,
            'readability': self.get_readability_score(text),
            'avg_word_length': self._get_avg_word_length(text),
            'avg_sentence_length': self._get_avg_sentence_length(text)
        }
    
    def _get_avg_word_length(self, text: str) -> float:
        """Calcula o comprimento médio das palavras"""
        words = self.tokenize_words(text)
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)
    
    def _get_avg_sentence_length(self, text: str) -> float:
        """Calcula o comprimento médio das sentenças"""
        sentences = self.tokenize_sentences(text)
        if not sentences:
            return 0.0
        
        total_words = sum(len(self.tokenize_words(sentence)) for sentence in sentences)
        return total_words / len(sentences)
