"""
Testes para o sistema de análise de qualidade PDI.
"""
import unittest
import sys
from pathlib import Path

# Adiciona o diretório da aplicação ao path
sys.path.append(str(Path(__file__).parent.parent))

from app import PDIAnalyzer, TextUtils, QualityMetricsService


class TestTextUtils(unittest.TestCase):
    """Testes para utilitários de texto."""
    
    def test_clean_text(self):
        """Testa limpeza de texto."""
        # Texto normal
        result = TextUtils.clean_text("Desenvolver habilidades em SAP.")
        self.assertEqual(result, "Desenvolver habilidades em SAP.")
        
        # Texto com caracteres especiais
        result = TextUtils.clean_text("Teste @#$% com símbolos!")
        self.assertEqual(result, "Teste com símbolos!")
        
        # Texto vazio/nulo
        self.assertEqual(TextUtils.clean_text(""), "")
        self.assertEqual(TextUtils.clean_text(None), "")
    
    def test_tokenize(self):
        """Testa tokenização."""
        tokens = TextUtils.tokenize("Desenvolver habilidades específicas")
        self.assertEqual(tokens, ["desenvolver", "habilidades", "específicas"])
        
        # Texto vazio
        self.assertEqual(TextUtils.tokenize(""), [])
    
    def test_count_sentences(self):
        """Testa contagem de sentenças."""
        # Uma sentença
        self.assertEqual(TextUtils.count_sentences("Desenvolver habilidades."), 1)
        
        # Múltiplas sentenças
        self.assertEqual(TextUtils.count_sentences("Primeira. Segunda! Terceira?"), 3)
        
        # Sem pontuação
        self.assertEqual(TextUtils.count_sentences("Texto sem pontuação"), 1)
    
    def test_validate_text_quality(self):
        """Testa validação de qualidade de texto."""
        # Texto válido
        self.assertTrue(TextUtils.validate_text_quality("Desenvolver habilidades específicas em programação"))
        
        # Texto muito curto
        self.assertFalse(TextUtils.validate_text_quality("Ok"))
        
        # Texto vazio
        self.assertFalse(TextUtils.validate_text_quality(""))


class TestQualityMetricsService(unittest.TestCase):
    """Testes para serviço de métricas de qualidade."""
    
    def setUp(self):
        """Configura testes."""
        self.service = QualityMetricsService()
    
    def test_calculate_clarity(self):
        """Testa cálculo de clareza."""
        # Texto claro e bem estruturado
        score = self.service.calculate_clarity("Desenvolver habilidades específicas em programação Python")
        self.assertGreater(score, 0.5)
        
        # Texto muito curto
        score = self.service.calculate_clarity("Ok")
        self.assertLess(score, 0.3)
    
    def test_calculate_specificity(self):
        """Testa cálculo de especificidade."""
        # Texto com números e termos técnicos
        score = self.service.calculate_specificity("Completar 40 horas de treinamento SAP módulo SD")
        self.assertGreater(score, 0.3)
        
        # Texto genérico
        score = self.service.calculate_specificity("Melhorar habilidades")
        self.assertLess(score, 0.5)
    
    def test_calculate_smart_criteria(self):
        """Testa cálculo de critérios SMART."""
        # Texto com critérios SMART
        score = self.service.calculate_smart_criteria("Completar curso específico até dezembro")
        self.assertGreater(score, 0.0)
        
        # Texto sem critérios SMART
        score = self.service.calculate_smart_criteria("Melhorar algo")
        self.assertEqual(score, 0.0)
    
    def test_negative_impact(self):
        """Testa cálculo de impacto negativo."""
        # Texto com indicadores negativos
        score = self.service.calculate_negative_impact("Talvez eu possa tentar melhorar")
        self.assertGreater(score, 0.0)
        
        # Texto positivo
        score = self.service.calculate_negative_impact("Vou implementar e executar")
        self.assertEqual(score, 0.0)


class TestPDIAnalyzer(unittest.TestCase):
    """Testes para analisador principal."""
    
    def setUp(self):
        """Configura testes."""
        self.analyzer = PDIAnalyzer()
    
    def test_analyze_text_good_quality(self):
        """Testa análise de texto de boa qualidade."""
        objetivo = "Desenvolver competências específicas em gestão de projetos ágeis"
        acoes = "Realizar curso de 40 horas sobre Scrum e Kanban até dezembro"
        
        result = self.analyzer.analyze_text(objetivo, acoes)
        
        self.assertIn('overall_score', result)
        self.assertIn('quality_level', result)
        self.assertGreater(result['overall_score'], 0.4)
    
    def test_analyze_text_poor_quality(self):
        """Testa análise de texto de baixa qualidade."""
        objetivo = "Melhorar"
        acoes = "Fazer algo"
        
        result = self.analyzer.analyze_text(objetivo, acoes)
        
        self.assertEqual(result['quality_level'], 'Baixa')
        self.assertLess(result['overall_score'], 0.3)
    
    def test_analyze_empty_text(self):
        """Testa análise de texto vazio."""
        result = self.analyzer.analyze_text("", "")
        
        self.assertEqual(result['quality_level'], 'Baixa')
        self.assertEqual(result['overall_score'], 0.0)


if __name__ == '__main__':
    unittest.main()
