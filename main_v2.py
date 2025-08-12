
import sys
from pathlib import Path
from typing import Optional

sys.path.append(str(Path(__file__).parent))

from app import PDIAnalyzer


class PDIAnalysisRunner:
    
    def __init__(self):
        self.analyzer = PDIAnalyzer()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def run_interactive(self):
        Executa análise automatizada.
        
        Args:
            file_path: Caminho para o arquivo
            sample_size: Tamanho da amostra (None para completo)
            output_dir: Diretório de saída
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
        print(f"\n📊 RESUMO DA ANÁLISE:")
        print(f"   📈 Total analisado: {summary['total_analyzed']} PDIs")
        
        percentages = summary.get('quality_percentages', {})
        print(f"   🟢 Qualidade ALTA: {summary['high_quality']} PDIs ({percentages.get('high', 0):.1f}%)")
        print(f"   🟡 Qualidade MÉDIA: {summary['medium_quality']} PDIs ({percentages.get('medium', 0):.1f}%)")
        print(f"   🔴 Qualidade BAIXA: {summary['low_quality']} PDIs ({percentages.get('low', 0):.1f}%)")
        
        avg_scores = summary.get('average_scores', {})
        print(f"   📊 Score médio geral: {avg_scores.get('overall', 0):.3f}")
    
    def _print_individual_result(self, result: dict):
        if 'error' in report:
            print(f"❌ {report['error']}")
            return
        
        print(f"\n📊 RELATÓRIO DETALHADO:")
        print(f"   📈 Total analisado: {report['total_analyzed']} PDIs")
        
        quality_dist = report['quality_distribution']
        percentages = report['quality_percentages']
        
        for level, count in quality_dist.items():
            percentage = percentages[level]
            print(f"   📊 {level}: {count} PDIs ({percentage:.1f}%)")
        
        print(f"\n📈 ESTATÍSTICAS DE SCORES:")
        score_stats = report['score_statistics']
        
        for metric, stats in score_stats.items():
            print(f"   {metric.title()}: média={stats['mean']:.3f}, "
                  f"min={stats['min']:.3f}, max={stats['max']:.3f}")
        
        if report['best_pdis']:
            print(f"\n🏆 TOP 5 MELHORES PDIs:")
            for i, pdi in enumerate(report['best_pdis'], 1):
                print(f"   {i}. {pdi['Nome Completo']} - Score: {pdi['overall_score']:.3f}")


def main():
