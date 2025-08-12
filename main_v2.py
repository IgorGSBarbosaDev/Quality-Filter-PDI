#!/usr/bin/env python3
"""
Sistema de Análise de Qualidade PDI - Versão 2.0
Interface principal para análise de Planos de Desenvolvimento Individual.
"""

import sys
from pathlib import Path
from typing import Optional

# Adiciona o diretório da aplicação ao path
sys.path.append(str(Path(__file__).parent))

from app import PDIAnalyzer


class PDIAnalysisRunner:
    """Runner principal para análise de PDI."""
    
    def __init__(self):
        self.analyzer = PDIAnalyzer()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def run_interactive(self):
        """Executa análise interativa."""
        print("🚀 SISTEMA DE ANÁLISE DE QUALIDADE PDI v2.0\n")
        
        while True:
            print("📋 OPÇÕES DISPONÍVEIS:")
            print("1. Analisar arquivo completo")
            print("2. Analisar amostra de arquivo") 
            print("3. Analisar texto individual")
            print("4. Gerar relatório de arquivo existente")
            print("5. Sair")
            
            choice = input("\nEscolha uma opção (1-5): ").strip()
            
            if choice == "1":
                self._analyze_full_file()
            elif choice == "2":
                self._analyze_sample()
            elif choice == "3":
                self._analyze_individual_text()
            elif choice == "4":
                self._generate_report()
            elif choice == "5":
                print("👋 Obrigado por usar o sistema!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
            
            input("\nPressione Enter para continuar...")
            print("\n" + "="*50 + "\n")
    
    def run_automated(
        self, 
        file_path: str, 
        sample_size: Optional[int] = None,
        output_dir: str = "output"
    ):
        """
        Executa análise automatizada.
        
        Args:
            file_path: Caminho para o arquivo
            sample_size: Tamanho da amostra (None para completo)
            output_dir: Diretório de saída
        """
        try:
            csv_path, json_path, summary = self.analyzer.analyze_file(
                file_path, output_dir, sample_size
            )
            
            self._print_summary(summary)
            print(f"\n📄 Resultados salvos em: {csv_path}")
            print(f"📋 Resumo salvo em: {json_path}")
            
        except Exception as e:
            print(f"❌ Erro durante análise: {str(e)}")
    
    def _analyze_full_file(self):
        """Analisa arquivo completo."""
        file_path = input("📁 Digite o caminho do arquivo: ").strip()
        
        if not file_path:
            print("❌ Caminho do arquivo é obrigatório")
            return
        
        try:
            csv_path, json_path, summary = self.analyzer.analyze_file(file_path)
            self._print_summary(summary)
            print(f"\n📄 Resultados: {csv_path}")
            print(f"📋 Resumo: {json_path}")
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    def _analyze_sample(self):
        """Analisa amostra de arquivo."""
        file_path = input("📁 Digite o caminho do arquivo: ").strip()
        
        if not file_path:
            print("❌ Caminho do arquivo é obrigatório")
            return
        
        try:
            sample_size = int(input("📊 Digite o tamanho da amostra: ").strip())
        except ValueError:
            print("❌ Tamanho da amostra deve ser um número")
            return
        
        try:
            csv_path, json_path, summary = self.analyzer.analyze_file(
                file_path, sample_size=sample_size
            )
            self._print_summary(summary)
            print(f"\n📄 Resultados: {csv_path}")
            print(f"📋 Resumo: {json_path}")
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    def _analyze_individual_text(self):
        """Analisa texto individual."""
        print("📝 ANÁLISE DE TEXTO INDIVIDUAL")
        
        objetivo = input("Objetivo de desenvolvimento: ").strip()
        
        if not objetivo:
            print("❌ Objetivo é obrigatório")
            return
        
        acoes = input("Ações planejadas (opcional): ").strip()
        atividade = input("Atividade de aprendizagem (opcional): ").strip()
        
        try:
            result = self.analyzer.analyze_text(objetivo, acoes, atividade)
            self._print_individual_result(result)
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    def _generate_report(self):
        """Gera relatório de arquivo existente."""
        file_path = input("📁 Digite o caminho do arquivo de resultados: ").strip()
        
        if not file_path:
            print("❌ Caminho do arquivo é obrigatório")
            return
        
        try:
            report = self.analyzer.generate_report(file_path)
            self._print_detailed_report(report)
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    def _print_summary(self, summary: dict):
        """Imprime resumo da análise."""
        print(f"\n📊 RESUMO DA ANÁLISE:")
        print(f"   📈 Total analisado: {summary['total_analyzed']} PDIs")
        
        percentages = summary.get('quality_percentages', {})
        print(f"   🟢 Qualidade ALTA: {summary['high_quality']} PDIs ({percentages.get('high', 0):.1f}%)")
        print(f"   🟡 Qualidade MÉDIA: {summary['medium_quality']} PDIs ({percentages.get('medium', 0):.1f}%)")
        print(f"   🔴 Qualidade BAIXA: {summary['low_quality']} PDIs ({percentages.get('low', 0):.1f}%)")
        
        avg_scores = summary.get('average_scores', {})
        print(f"   📊 Score médio geral: {avg_scores.get('overall', 0):.3f}")
    
    def _print_individual_result(self, result: dict):
        """Imprime resultado de análise individual."""
        print(f"\n📊 RESULTADO DA ANÁLISE:")
        print(f"   🎯 Qualidade geral: {result['quality_level']} ({result['overall_score']:.3f})")
        print(f"   📝 Clareza: {result['clarity_score']:.3f}")
        print(f"   🎯 Especificidade: {result['specificity_score']:.3f}")
        print(f"   📋 Completude: {result['completeness_score']:.3f}")
        print(f"   🏗️ Estrutura: {result['structure_score']:.3f}")
        print(f"   ⭐ Critérios SMART: {result['smart_criteria_score']:.3f}")
        
        if result.get('suggestions'):
            print(f"\n💡 SUGESTÕES DE MELHORIA:")
            suggestions = result['suggestions'].split(' | ')
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
    
    def _print_detailed_report(self, report: dict):
        """Imprime relatório detalhado."""
        if 'error' in report:
            print(f"❌ {report['error']}")
            return
        
        print(f"\n📊 RELATÓRIO DETALHADO:")
        print(f"   📈 Total analisado: {report['total_analyzed']} PDIs")
        
        # Distribuição de qualidade
        quality_dist = report['quality_distribution']
        percentages = report['quality_percentages']
        
        for level, count in quality_dist.items():
            percentage = percentages[level]
            print(f"   📊 {level}: {count} PDIs ({percentage:.1f}%)")
        
        # Estatísticas de scores
        print(f"\n📈 ESTATÍSTICAS DE SCORES:")
        score_stats = report['score_statistics']
        
        for metric, stats in score_stats.items():
            print(f"   {metric.title()}: média={stats['mean']:.3f}, "
                  f"min={stats['min']:.3f}, max={stats['max']:.3f}")
        
        # Melhores PDIs
        if report['best_pdis']:
            print(f"\n🏆 TOP 5 MELHORES PDIs:")
            for i, pdi in enumerate(report['best_pdis'], 1):
                print(f"   {i}. {pdi['Nome Completo']} - Score: {pdi['overall_score']:.3f}")


def main():
    """Função principal."""
    runner = PDIAnalysisRunner()
    
    # Verifica se há argumentos de linha de comando
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        sample_size = int(sys.argv[2]) if len(sys.argv) > 2 else None
        
        print(f"🚀 Executando análise automatizada...")
        runner.run_automated(file_path, sample_size)
    else:
        # Executa modo interativo
        runner.run_interactive()


if __name__ == "__main__":
    main()
