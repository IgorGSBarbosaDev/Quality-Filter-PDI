#!/usr/bin/env python3

import sys
import os
from pathlib import Path

def validate_project_structure():
    """Valida se a nova estrutura do projeto está correta"""
    
    base_path = Path("c:/Users/u014441/Documents/Projects/Quality Filter PDI")
    
    # Estrutura esperada
    expected_structure = {
        "📦 Pacote Principal": [
            "quality_filter_pdi/__init__.py",
            "quality_filter_pdi/pdi_analyzer.py"
        ],
        "🧠 Módulos IA": [
            "quality_filter_pdi/ai/__init__.py",
            "quality_filter_pdi/ai/ai_text_analyzer.py",
            "quality_filter_pdi/ai/advanced_ai_analyzer.py",
            "quality_filter_pdi/ai/cloud_ai_analyzer.py"
        ],
        "🔧 Core": [
            "quality_filter_pdi/core/__init__.py",
            "quality_filter_pdi/core/config.py"
        ],
        "🎯 Services": [
            "quality_filter_pdi/services/__init__.py",
            "quality_filter_pdi/services/pdi_analysis_service.py",
            "quality_filter_pdi/services/quality_metrics_service.py",
            "quality_filter_pdi/services/file_service.py",
            "quality_filter_pdi/services/skill_classifier.py"
        ],
        "🛠️ Utils": [
            "quality_filter_pdi/utils/__init__.py",
            "quality_filter_pdi/utils/text_utils.py"
        ],
        "💻 CLI": [
            "cli/main.py"
        ],
        "📚 Documentation": [
            "documentation/COMO_USAR.md",
            "documentation/GUIA_COMPLETO.md",
            "documentation/IMPLEMENTACAO_IA.md",
            "documentation/CONFIGURACAO_AMBIENTE.md"
        ],
        "🧪 Tests": [
            "tests/unit/test_simple.py",
            "tests/integration/test_system.py"
        ],
        "🎨 Examples": [
            "examples/demo_final.py",
            "examples/projeto_concluido.py"
        ],
        "🔧 Setup": [
            "setup/setup_environment.ps1",
            "setup/setup_environment.bat"
        ],
        "📂 Data": [
            "data/samples/exemplo_pdis.csv"
        ],
        "📄 Config": [
            "pyproject.toml",
            "requirements.txt",
            "requirements_ai.txt"
        ]
    }
    
    print("🔍 Validando estrutura do projeto reorganizado...")
    print("=" * 60)
    
    all_valid = True
    
    for section, files in expected_structure.items():
        print(f"\n{section}")
        print("-" * 40)
        
        for file_path in files:
            full_path = base_path / file_path
            
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - AUSENTE")
                all_valid = False
    
    print("\n" + "=" * 60)
    
    if all_valid:
        print("🎉 ESTRUTURA VÁLIDA - Projeto reorganizado com sucesso!")
        print("🚀 Execute: python cli/main.py")
    else:
        print("⚠️ ESTRUTURA INCOMPLETA - Alguns arquivos estão ausentes")
    
    # Teste de importação
    print("\n🔬 Testando importações...")
    
    try:
        sys.path.append(str(base_path))
        from quality_filter_pdi import PDIAnalyzer
        print("✅ Importação do PDIAnalyzer bem-sucedida")
        
        analyzer = PDIAnalyzer()
        print("✅ Instanciação do PDIAnalyzer bem-sucedida")
        
        # Teste básico
        result = analyzer.analyze_text("Teste de estrutura")
        print(f"✅ Teste básico: Score {result['overall_score']:.2f}")
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        all_valid = False
    
    return all_valid

if __name__ == "__main__":
    if validate_project_structure():
        print("\n🎯 PROJETO REORGANIZADO E FUNCIONAL!")
        print("📁 Nova estrutura profissional implementada")
        print("🤖 IA integrada e disponível")
        print("📚 Documentação organizada")
        print("🧪 Testes estruturados")
    else:
        print("\n⚠️ Reorganização precisa de ajustes")
    
    input("\nPressione Enter para continuar...")
