import sys
import os
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent))

try:
    from config.settings import QUALITY_THRESHOLDS, METRIC_WEIGHTS
    from src.text_processor import TextProcessor
    from src.quality_metrics import QualityMetrics
    from src.pdi_analyzer import PDIAnalyzer
except ImportError as e:
    print(f"Erro de importação: {e}")
    sys.exit(1)


class SystemTester:
    def __init__(self) -> None:
        self.passed_tests = 0
        self.total_tests = 0
    
    def run_all_tests(self) -> None:
        print("Executando testes do sistema...")
        print("=" * 40)
        
        self.test_imports()
        self.test_text_processor()
        self.test_quality_metrics()
        self.test_pdi_analyzer()
        
        self.display_results()
    
    def test_imports(self) -> None:
        print("\n1. Testando importações...")
        
        modules = [
            ("pandas", "pd"),
            ("nltk", None),
            ("textstat", None),
            ("config.settings", "settings"),
            ("src.text_processor", "TextProcessor"),
            ("src.quality_metrics", "QualityMetrics"),
            ("src.pdi_analyzer", "PDIAnalyzer")
        ]
        
        for module_name, alias in modules:
            self._test_import(module_name, alias)
    
    def test_text_processor(self) -> None:
        print("\n2. Testando TextProcessor...")
        
        try:
            processor = TextProcessor()
            
            test_text = "Este é um teste com 10 palavras para verificar funcionamento."
            
            word_count = processor.get_word_count(test_text)
            self._assert_test(word_count >= 8, "Contagem de palavras")
            
            sentence_count = processor.get_sentence_count(test_text)
            self._assert_test(sentence_count >= 1, "Contagem de sentenças")
            
            readability = processor.get_readability_score(test_text)
            self._assert_test(0 <= readability <= 1, "Score de legibilidade")
            
        except Exception as e:
            self._fail_test(f"TextProcessor: {e}")
    
    def test_quality_metrics(self) -> None:
        print("\n3. Testando QualityMetrics...")
        
        try:
            metrics = QualityMetrics()
            
            test_text = "Implementar sistema até dezembro com 100% de qualidade."
            
            clarity = metrics.calculate_clarity_score(test_text)
            self._assert_test(0 <= clarity <= 1, "Score de clareza")
            
            specificity = metrics.calculate_specificity_score(test_text)
            self._assert_test(0 <= specificity <= 1, "Score de especificidade")
            
            completeness = metrics.calculate_completeness_score(test_text)
            self._assert_test(0 <= completeness <= 1, "Score de completude")
            
        except Exception as e:
            self._fail_test(f"QualityMetrics: {e}")
    
    def test_pdi_analyzer(self) -> None:
        print("\n4. Testando PDIAnalyzer...")
        
        try:
            analyzer = PDIAnalyzer()
            
            acoes = "Realizar curso de Python em 3 meses e aplicar em projeto real."
            objetivo = "Tornar-me desenvolvedor full-stack em 12 meses."
            
            result = analyzer.analyze_single_pdi(acoes, objetivo)
            
            required_keys = ['quality_level', 'quality_score', 'suggestions']
            for key in required_keys:
                self._assert_test(key in result, f"Chave '{key}' no resultado")
            
            self._assert_test(result['quality_level'] in ['Alto', 'Médio', 'Baixo'], "Nível de qualidade válido")
            self._assert_test(0 <= result['quality_score'] <= 1, "Score de qualidade válido")
            
        except Exception as e:
            self._fail_test(f"PDIAnalyzer: {e}")
    
    def _test_import(self, module_name: str, alias: str = None) -> None:
        try:
            if alias:
                exec(f"from {module_name} import {alias}")
            else:
                exec(f"import {module_name}")
            self._pass_test(f"Importação {module_name}")
        except Exception as e:
            self._fail_test(f"Importação {module_name}: {e}")
    
    def _assert_test(self, condition: bool, test_name: str) -> None:
        if condition:
            self._pass_test(test_name)
        else:
            self._fail_test(test_name)
    
    def _pass_test(self, test_name: str) -> None:
        print(f"  ✓ {test_name}")
        self.passed_tests += 1
        self.total_tests += 1
    
    def _fail_test(self, test_name: str) -> None:
        print(f"  ✗ {test_name}")
        self.total_tests += 1
    
    def display_results(self) -> None:
        print("\n" + "=" * 40)
        print("RESULTADO DOS TESTES")
        print("=" * 40)
        print(f"Testes executados: {self.total_tests}")
        print(f"Testes aprovados: {self.passed_tests}")
        print(f"Testes falharam: {self.total_tests - self.passed_tests}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"Taxa de sucesso: {success_rate:.1f}%")
        
        if self.passed_tests == self.total_tests:
            print("\n🎉 Todos os testes passaram! Sistema pronto para uso.")
        else:
            print(f"\n⚠️  {self.total_tests - self.passed_tests} teste(s) falharam. Verifique as dependências.")


def main() -> None:
    tester = SystemTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
