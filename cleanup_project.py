#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Remove arquivos duplicados e desnecessários"""
    
    base_path = Path("c:/Users/u014441/Documents/Projects/Quality Filter PDI")
    
    # Arquivos e pastas para REMOVER (duplicados/obsoletos)
    files_to_remove = [
        # Pasta app antiga (já movida para quality_filter_pdi)
        "app/",
        
        # Arquivos de documentação duplicados na raiz
        "COMO_USAR.md",
        "GUIA_COMPLETO.md", 
        "IMPLEMENTACAO_IA.md",
        "CONFIGURACAO_AMBIENTE.md",
        "STATUS_CONFIGURACAO.md",
        
        # Scripts de teste duplicados na raiz
        "test_complete.py",
        "test_simple.py", 
        "test_skill_classification.py",
        "test_system.py",
        "final_validation.py",
        
        # Scripts de exemplo duplicados na raiz
        "demo_csv_direto.py",
        "demo_final.py",
        "PROJETO_CONCLUIDO.py", 
        "relatorio_final.py",
        
        # Scripts de setup duplicados na raiz
        "setup_environment.ps1",
        "setup_environment.bat",
        "main_v2.py",
        
        # Arquivos temporários/de desenvolvimento
        "reorganize_project.py",
        "validate_structure.py",
        
        # Pastas vazias/desnecessárias
        "config/",
        "docs/", 
        "scripts/",
        "src/",
        
        # Arquivos de versão desnecessários
        "2.0.0",
        "3.1.0", 
        "5.0.0",
        
        # JSONs de resumo temporários
        "resumo_analise_20250812_095455.json",
        "resumo_analise_20250812_095528.json",
        "resumo_automatico_20250812_095918.json",
        
        # Cache Python
        "__pycache__/",
        
        # README duplicado
        "README.md"  # Manter apenas README_NEW.md
    ]
    
    print("🧹 Limpando arquivos desnecessários e duplicados...")
    print("=" * 60)
    
    removed_count = 0
    
    for item in files_to_remove:
        item_path = base_path / item
        
        if item_path.exists():
            try:
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"🗂️ Pasta removida: {item}")
                else:
                    item_path.unlink()
                    print(f"📄 Arquivo removido: {item}")
                
                removed_count += 1
                
            except Exception as e:
                print(f"⚠️ Erro ao remover {item}: {e}")
        else:
            print(f"ℹ️ Já removido: {item}")
    
    # Renomear README_NEW.md para README.md
    readme_new = base_path / "README_NEW.md"
    readme_main = base_path / "README.md"
    
    if readme_new.exists():
        readme_new.rename(readme_main)
        print(f"✅ README_NEW.md → README.md")
    
    print("\n" + "=" * 60)
    print(f"🎯 Limpeza concluída! {removed_count} itens removidos")
    
    return removed_count

def validate_final_structure():
    """Valida a estrutura final limpa"""
    
    base_path = Path("c:/Users/u014441/Documents/Projects/Quality Filter PDI")
    
    # Estrutura final esperada (apenas arquivos essenciais)
    essential_structure = {
        "📦 Pacote Principal": [
            "quality_filter_pdi/__init__.py",
            "quality_filter_pdi/pdi_analyzer.py",
            "quality_filter_pdi/core/config.py",
            "quality_filter_pdi/services/pdi_analysis_service.py",
            "quality_filter_pdi/services/quality_metrics_service.py",
            "quality_filter_pdi/services/file_service.py",
            "quality_filter_pdi/services/skill_classifier.py",
            "quality_filter_pdi/utils/text_utils.py",
            "quality_filter_pdi/ai/ai_text_analyzer.py",
            "quality_filter_pdi/ai/advanced_ai_analyzer.py",
            "quality_filter_pdi/ai/cloud_ai_analyzer.py"
        ],
        "💻 Interface": [
            "cli/main.py"
        ],
        "📚 Documentação": [
            "documentation/COMO_USAR.md",
            "documentation/GUIA_COMPLETO.md",
            "documentation/IMPLEMENTACAO_IA.md",
            "documentation/CONFIGURACAO_AMBIENTE.md"
        ],
        "🧪 Testes": [
            "tests/unit/test_simple.py",
            "tests/integration/test_system.py"
        ],
        "🎨 Exemplos": [
            "examples/demo_final.py",
            "examples/projeto_concluido.py"
        ],
        "🔧 Setup": [
            "setup/setup_environment.ps1",
            "setup/setup_environment.bat"
        ],
        "📂 Dados": [
            "data/samples/exemplo_pdis.csv"
        ],
        "📄 Configuração": [
            "README.md",
            "pyproject.toml",
            "requirements.txt",
            "requirements_ai.txt",
            "REORGANIZACAO_COMPLETA.md"
        ]
    }
    
    print("\n🔍 Validando estrutura final...")
    print("=" * 60)
    
    all_present = True
    total_files = 0
    
    for section, files in essential_structure.items():
        print(f"\n{section}")
        print("-" * 40)
        
        for file_path in files:
            full_path = base_path / file_path
            total_files += 1
            
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - AUSENTE")
                all_present = False
    
    print(f"\n📊 Total de arquivos essenciais: {total_files}")
    
    return all_present

if __name__ == "__main__":
    print("🧹 LIMPEZA DE ARQUIVOS DUPLICADOS E DESNECESSÁRIOS")
    print("=" * 60)
    
    removed = cleanup_project()
    
    if validate_final_structure():
        print("\n🎉 PROJETO LIMPO E ORGANIZADO!")
        print("✅ Apenas arquivos essenciais mantidos")
        print("🗂️ Estrutura profissional final")
        print("🚀 Pronto para produção!")
    else:
        print("\n⚠️ Alguns arquivos essenciais estão ausentes")
    
    print(f"\n📈 Arquivos removidos: {removed}")
    print("🎯 Execute: python cli/main.py")
    
    input("\nPressione Enter para continuar...")
