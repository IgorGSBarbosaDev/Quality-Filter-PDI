import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app import PDIAnalyzer, TextUtils, QualityMetricsService


class TestTextUtils(unittest.TestCase):
    
    def test_clean_text(self):
        result = TextUtils.clean_text("Desenvolver habilidades em SAP.")
        self.assertEqual(result, "Desenvolver habilidades em SAP.")
        
        result = TextUtils.clean_text("Teste @#$% com símbolos!")
        self.assertEqual(result, "Teste com símbolos!")
        
        self.assertEqual(TextUtils.clean_text(""), "")
        self.assertEqual(TextUtils.clean_text(None), "")
    
    def test_tokenize(self):
        tokens = TextUtils.tokenize("Desenvolver habilidades específicas")
        self.assertEqual(tokens, ["desenvolver", "habilidades", "específicas"])
        
        self.assertEqual(TextUtils.tokenize(""), [])
    
    def test_count_sentences(self):
        self.assertEqual(TextUtils.count_sentences("Desenvolver habilidades."), 1)
        
        self.assertEqual(TextUtils.count_sentences("Primeira. Segunda! Terceira?"), 3)
        
        self.assertEqual(TextUtils.count_sentences("Texto sem pontuação"), 1)
    
    def test_validate_text_quality(self):
        self.assertTrue(TextUtils.validate_text_quality("Desenvolver habilidades específicas em programação"))
        
        self.assertFalse(TextUtils.validate_text_quality("Ok"))
        
        self.assertFalse(TextUtils.validate_text_quality(""))


class TestQualityMetricsService(unittest.TestCase):
    
    def setUp(self):
        self.service = QualityMetricsService()
    
    def test_calculate_clarity(self):
        score = self.service.calculate_clarity("Desenvolver habilidades específicas em programação Python")
        self.assertGreater(score, 0.5)
        
        score = self.service.calculate_clarity("Ok")
        self.assertLess(score, 0.3)
    
    def test_calculate_specificity(self):
        score = self.service.calculate_specificity("Completar 40 horas de treinamento SAP módulo SD")
        self.assertGreater(score, 0.3)
        
        score = self.service.calculate_specificity("Melhorar habilidades")
        self.assertLess(score, 0.5)
    
    def test_calculate_smart_criteria(self):
        score = self.service.calculate_smart_criteria("Completar curso específico até dezembro")
        self.assertGreater(score, 0.0)
        
        score = self.service.calculate_smart_criteria("Melhorar algo")
        self.assertEqual(score, 0.0)
    
    def test_negative_impact(self):
        score = self.service.calculate_negative_impact("Talvez eu possa tentar melhorar")
        self.assertGreater(score, 0.0)
        
        score = self.service.calculate_negative_impact("Vou implementar e executar")
        self.assertEqual(score, 0.0)


class TestPDIAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = PDIAnalyzer()
    
    def test_analyze_text_good_quality(self):
        objetivo = "Desenvolver competências específicas em gestão de projetos ágeis"
        acoes = "Realizar curso de 40 horas sobre Scrum e Kanban até dezembro"
        
        result = self.analyzer.analyze_text(objetivo, acoes)
        
        self.assertIn('overall_score', result)
        self.assertIn('quality_level', result)
        self.assertGreater(result['overall_score'], 0.4)
    
    def test_analyze_text_poor_quality(self):
        objetivo = "Melhorar"
        acoes = "Fazer algo"
        
        result = self.analyzer.analyze_text(objetivo, acoes)
        
        self.assertEqual(result['quality_level'], 'Baixa')
        self.assertLess(result['overall_score'], 0.3)
    
    def test_analyze_empty_text(self):
        result = self.analyzer.analyze_text("", "")
        
        self.assertEqual(result['quality_level'], 'Baixa')
        self.assertEqual(result['overall_score'], 0.0)


if __name__ == '__main__':
    unittest.main()
