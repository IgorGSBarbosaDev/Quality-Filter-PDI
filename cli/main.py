#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent))

from quality_filter_pdi import PDIAnalyzer


class PDIAnalysisRunner:
    
    def __init__(self):
        self.analyzer = PDIAnalyzer()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def run_interactive(self):
        print("🚀 SISTEMA DE ANÁLISE DE QUALIDADE PDI")
        print("=" * 50)
        
        while True:
            print("\n📋 Escolha uma opção:")
            print("1. Analisar arquivo CSV/Excel")
            print("2. Análise de texto individual")
            print("3. Sair")
            
            choice = input("\nOpção (1-3): ").strip()
            
            if choice == "1":
                self._analyze_file()
            elif choice == "2":
                self._analyze_text()
            elif choice == "3":
                print("👋 Encerrando sistema...")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
                
            input("\nPressione Enter para continuar...")
    
    def _analyze_file(self):
        file_path = input("📁 Digite o caminho do arquivo: ").strip()
        
        if not file_path:
            print("❌ Caminho do arquivo é obrigatório")
            return 
        
        try:
            sample_input = input("📊 Tamanho da amostra (Enter para arquivo completo): ").strip()
            sample_size = int(sample_input) if sample_input else None
            
            print(f"\n🔄 Analisando arquivo: {Path(file_path).name}")
            
            result = self.analyzer.analyze_file(file_path, str(self.output_dir), sample_size)
            
            if result.get('success', False):
                self._display_file_results(result)
            else:
                print(f"❌ Erro na análise: {result.get('error', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _analyze_text(self):
        print("\n📝 ANÁLISE DE TEXTO INDIVIDUAL")
        
        objetivo = input("🎯 Digite o objetivo: ").strip()
        acoes = input("📋 Digite as ações: ").strip()
        
        if not objetivo or not acoes:
            print("❌ Objetivo e ações são obrigatórios")
            return
        
        try:
            result = self.analyzer.analyze_text(objetivo, acoes)
            self._display_text_results(result)
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
    
    def _display_file_results(self, result):
        print("\n📊 RESULTADOS DA ANÁLISE")
        print("=" * 40)
        
        print(f"📈 Total analisado: {result['total_analyzed']} PDIs")
        
        summary = result.get('summary', {})
        alta = summary.get('Alta', 0)
        media = summary.get('Média', 0)
        baixa = summary.get('Baixa', 0)
        total = alta + media + baixa
        
        if total > 0:
            print(f"🟢 Qualidade ALTA: {alta} PDIs ({alta/total*100:.1f}%)")
            print(f"🟡 Qualidade MÉDIA: {media} PDIs ({media/total*100:.1f}%)")
            print(f"🔴 Qualidade BAIXA: {baixa} PDIs ({baixa/total*100:.1f}%)")
        
        if 'output_file' in result:
            print(f"\n💾 Resultados salvos em: {result['output_file']}")
    
    def _display_text_results(self, result):
        print("\n📊 RESULTADO DA ANÁLISE")
        print("=" * 30)
        
        print(f"📈 Score Geral: {result['overall_score']:.2f}")
        print(f"🏆 Nível de Qualidade: {result['quality_level']}")
        
        if 'skill_classification' in result:
            skill_info = result['skill_classification']
            print(f"\n🎯 CLASSIFICAÇÃO DE HABILIDADE:")
            print(f"   📚 Tipo: {skill_info['skill_type']}")
            print(f"   📊 Confiança: {skill_info['confidence']:.2f}")
            print(f"   💡 Recomendação: {skill_info['recommendation']}")
        
        print(f"\n📋 Detalhamento:")
        print(f"   📝 Clareza: {result['clarity_score']:.2f}")
        print(f"   🎯 Especificidade: {result['specificity_score']:.2f}")
        print(f"   📖 Completude: {result['completeness_score']:.2f}")
        print(f"   🏗️ Estrutura: {result['structure_score']:.2f}")
        print(f"   🎯 SMART: {result['smart_criteria_score']:.2f}")
        
        recommendations = self.analyzer.get_quality_recommendations(result)
        if recommendations:
            print(f"\n💡 Recomendações:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")


def main():
    try:
        runner = PDIAnalysisRunner()
        runner.run_interactive()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
