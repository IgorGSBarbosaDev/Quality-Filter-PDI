import re
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class PDIExample:
    nome: str
    acoes: str
    objetivo: str


class SimplePDIAnalyzer:
    QUALITY_WORDS = ['implementar', 'desenvolver', 'concluir', 'atingir', 'realizar']
    NEGATIVE_WORDS = ['talvez', 'acho que', 'tentar', 'espero']
    MIN_WORDS = 10
    
    def analyze_pdi(self, acoes: str, objetivo: str) -> Dict[str, Any]:
        score = 0.0
        suggestions = []
        
        score += self._evaluate_length(acoes, objetivo, suggestions)
        score += self._evaluate_specificity(acoes, objetivo, suggestions)
        score += self._evaluate_quality_words(acoes, objetivo, suggestions)
        score += self._evaluate_language_quality(acoes, objetivo, suggestions)
        
        level = self._determine_level(score)
        
        if not suggestions:
            suggestions.append("• PDI de boa qualidade!")
        
        return {
            'level': level,
            'score': round(score, 2),
            'suggestions': " ".join(suggestions)
        }
    
    def _evaluate_length(self, acoes: str, objetivo: str, suggestions: List[str]) -> float:
        score = 0.0
        acoes_words = len(acoes.split()) if acoes else 0
        objetivo_words = len(objetivo.split()) if objetivo else 0
        
        if acoes_words >= self.MIN_WORDS:
            score += 0.2
        else:
            suggestions.append(f"• Expanda as ações planejadas (mínimo {self.MIN_WORDS} palavras)")
        
        if objetivo_words >= self.MIN_WORDS:
            score += 0.2
        else:
            suggestions.append(f"• Expanda o objetivo de desenvolvimento (mínimo {self.MIN_WORDS} palavras)")
        
        return score
    
    def _evaluate_specificity(self, acoes: str, objetivo: str, suggestions: List[str]) -> float:
        combined_text = f"{acoes} {objetivo}"
        
        if re.search(r'\d+', combined_text):
            return 0.2
        else:
            suggestions.append("• Inclua números específicos (prazos, quantidades, metas)")
            return 0.0
    
    def _evaluate_quality_words(self, acoes: str, objetivo: str, suggestions: List[str]) -> float:
        combined_text = f"{acoes} {objetivo}".lower()
        
        if any(word in combined_text for word in self.QUALITY_WORDS):
            return 0.2
        else:
            suggestions.append("• Use verbos de ação mais específicos")
            return 0.0
    
    def _evaluate_language_quality(self, acoes: str, objetivo: str, suggestions: List[str]) -> float:
        combined_text = f"{acoes} {objetivo}".lower()
        
        if any(word in combined_text for word in self.NEGATIVE_WORDS):
            suggestions.append("• Evite linguagem incerta - seja mais assertivo")
            return 0.1
        else:
            return 0.2
    
    def _determine_level(self, score: float) -> str:
        if score >= 0.8:
            return "Alto"
        elif score >= 0.6:
            return "Médio"
        return "Baixo"


class PDIDemoRunner:
    def __init__(self) -> None:
        self.analyzer = SimplePDIAnalyzer()
        self.examples = self._create_examples()
    
    def _create_examples(self) -> List[PDIExample]:
        return [
            PDIExample(
                nome='João Silva',
                acoes='Realizar curso de Excel avançado com duração de 40 horas até dezembro de 2024. Praticar relatórios gerenciais semanalmente.',
                objetivo='Tornar-me especialista em análise financeira avançada até dezembro de 2024.'
            ),
            PDIExample(
                nome='Maria Santos',
                acoes='Fazer alguns cursos de liderança.',
                objetivo='Desenvolver habilidades de liderança.'
            ),
            PDIExample(
                nome='Carlos Oliveira',
                acoes='Melhorar habilidades.',
                objetivo='Crescer profissionalmente.'
            )
        ]
    
    def run_demo(self) -> None:
        print("Sistema Simplificado de Análise de PDI")
        print("=" * 40)
        
        for exemplo in self.examples:
            self._analyze_and_display(exemplo)
    
    def _analyze_and_display(self, exemplo: PDIExample) -> None:
        print(f"\nFuncionário: {exemplo.nome}")
        print(f"Ações: {exemplo.acoes}")
        print(f"Objetivo: {exemplo.objetivo}")
        
        resultado = self.analyzer.analyze_pdi(exemplo.acoes, exemplo.objetivo)
        
        print(f"Nível de Qualidade: {resultado['level']}")
        print(f"Pontuação: {resultado['score']}")
        print(f"Sugestões: {resultado['suggestions']}")
        print("-" * 40)


def main() -> None:
    runner = PDIDemoRunner()
    runner.run_demo()


if __name__ == "__main__":
    main()
