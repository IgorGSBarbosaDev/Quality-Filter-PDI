"""
Utilitários para processamento de texto.
Contém funções auxiliares para limpeza, tokenização e análise de texto.
"""
import re
import pandas as pd
from typing import List, Optional


class TextUtils:
    """Utilitários para processamento de texto sem dependências externas."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Limpa e normaliza texto de forma segura.
        
        Args:
            text: Texto a ser limpo
            
        Returns:
            Texto limpo e normalizado
        """
        if pd.isna(text) or text is None:
            return ""
        
        text = str(text).strip()
        text = re.sub(r'[^\w\s\-\.,;:!?()]', ' ', text, flags=re.UNICODE)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """
        Tokenização simples sem dependências externas.
        
        Args:
            text: Texto a ser tokenizado
            
        Returns:
            Lista de tokens (palavras)
        """
        if not text:
            return []
        
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    @staticmethod
    def count_sentences(text: str) -> int:
        """
        Conta sentenças de forma simples.
        
        Args:
            text: Texto para contagem
            
        Returns:
            Número de sentenças (mínimo 1)
        """
        if not text:
            return 0
        
        sentence_endings = re.findall(r'[.!?]+', text)
        return max(1, len(sentence_endings))
    
    @staticmethod
    def count_words(text: str) -> int:
        """
        Conta palavras no texto.
        
        Args:
            text: Texto para contagem
            
        Returns:
            Número de palavras
        """
        if not text:
            return 0
        
        words = TextUtils.tokenize(text)
        return len(words)
    
    @staticmethod
    def calculate_avg_word_length(text: str) -> float:
        """
        Calcula comprimento médio das palavras.
        
        Args:
            text: Texto para análise
            
        Returns:
            Comprimento médio das palavras
        """
        words = TextUtils.tokenize(text)
        if not words:
            return 0.0
        
        total_length = sum(len(word) for word in words)
        return total_length / len(words)
    
    @staticmethod
    def has_numbers(text: str) -> bool:
        """
        Verifica se o texto contém números.
        
        Args:
            text: Texto para verificação
            
        Returns:
            True se contém números, False caso contrário
        """
        return bool(re.search(r'\d+', text))
    
    @staticmethod
    def count_numbers(text: str) -> int:
        """
        Conta ocorrências de números no texto.
        
        Args:
            text: Texto para contagem
            
        Returns:
            Número de ocorrências numéricas
        """
        return len(re.findall(r'\d+', text))
    
    @staticmethod
    def has_proper_case(text: str) -> bool:
        """
        Verifica se o texto inicia com letra maiúscula.
        
        Args:
            text: Texto para verificação
            
        Returns:
            True se inicia com maiúscula, False caso contrário
        """
        return bool(re.search(r'^[A-Z]', text.strip()))
    
    @staticmethod
    def has_punctuation(text: str) -> bool:
        """
        Verifica se o texto contém pontuação.
        
        Args:
            text: Texto para verificação
            
        Returns:
            True se contém pontuação, False caso contrário
        """
        return bool(re.search(r'[.!?]', text))
    
    @staticmethod
    def extract_technical_terms(text: str) -> List[str]:
        """
        Extrai termos técnicos do texto.
        
        Args:
            text: Texto para análise
            
        Returns:
            Lista de termos técnicos encontrados
        """
        technical_patterns = [
            r'\bSAP\b', r'\bsistema\b', r'\bprocesso\b', r'\bmódulo\b',
            r'\bcurso\b', r'\btreinamento\b', r'\bhabilidade\b', r'\bcompetência\b'
        ]
        
        found_terms = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_terms.extend(matches)
        
        return found_terms
    
    @staticmethod
    def validate_text_quality(text: str, min_words: int = 3) -> bool:
        """
        Valida se o texto tem qualidade mínima para análise.
        
        Args:
            text: Texto para validação
            min_words: Número mínimo de palavras
            
        Returns:
            True se o texto é válido, False caso contrário
        """
        if not text or pd.isna(text):
            return False
        
        clean_text = TextUtils.clean_text(text)
        word_count = TextUtils.count_words(clean_text)
        
        return len(clean_text) >= 3 and word_count >= min_words
