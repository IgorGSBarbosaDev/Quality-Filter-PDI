import re
from typing import List, Dict, Any
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import textstat


class TextProcessor:
    def __init__(self) -> None:
        self._download_nltk_data()
        self.stop_words = set(stopwords.words('portuguese'))
    
    def _download_nltk_data(self) -> None:
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    def clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def tokenize_words(self, text: str) -> List[str]:
        clean = self.clean_text(text)
        tokens = word_tokenize(clean, language='portuguese')
        return [word for word in tokens if word not in self.stop_words and len(word) > 2]
    
    def tokenize_sentences(self, text: str) -> List[str]:
        if not isinstance(text, str):
            return []
        return sent_tokenize(text, language='portuguese')
    
    def get_word_count(self, text: str) -> int:
        return len(self.tokenize_words(text))
    
    def get_sentence_count(self, text: str) -> int:
        return len(self.tokenize_sentences(text))
    
    def get_readability_score(self, text: str) -> float:
        if not isinstance(text, str) or len(text.strip()) == 0:
            return 0.0
        
        try:
            score = textstat.flesch_reading_ease(text)
            return max(0, min(1, score / 100))
        except Exception:
            return 0.5
    
    def has_keywords(self, text: str, keywords: List[str]) -> bool:
        clean = self.clean_text(text)
        return any(keyword.lower() in clean for keyword in keywords)
    
    def count_keywords(self, text: str, keywords: List[str]) -> int:
        clean = self.clean_text(text)
        return sum(1 for keyword in keywords if keyword.lower() in clean)
    
    def extract_metrics(self, text: str) -> Dict[str, Any]:
        return {
            'word_count': self.get_word_count(text),
            'sentence_count': self.get_sentence_count(text),
            'char_count': len(text) if isinstance(text, str) else 0,
            'readability': self.get_readability_score(text),
            'avg_word_length': self._get_avg_word_length(text),
            'avg_sentence_length': self._get_avg_sentence_length(text)
        }
    
    def _get_avg_word_length(self, text: str) -> float:
        words = self.tokenize_words(text)
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)
    
    def _get_avg_sentence_length(self, text: str) -> float:
        sentences = self.tokenize_sentences(text)
        if not sentences:
            return 0.0
        
        total_words = sum(len(self.tokenize_words(sentence)) for sentence in sentences)
        return total_words / len(sentences)
