#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path

def reorganize_project():
    base_path = Path("c:/Users/u014441/Documents/Projects/Quality Filter PDI")
    
    # Mapeamento de arquivos para nova estrutura
    file_mapping = {
        # Core files
        "app/core/config.py": "quality_filter_pdi/core/config.py",
        
        # Services
        "app/services/pdi_analysis_service.py": "quality_filter_pdi/services/pdi_analysis_service.py",
        "app/services/quality_metrics_service.py": "quality_filter_pdi/services/quality_metrics_service.py",
        "app/services/file_service.py": "quality_filter_pdi/services/file_service.py",
        "app/services/skill_classifier.py": "quality_filter_pdi/services/skill_classifier.py",
        
        # AI Services
        "app/services/ai_text_analyzer.py": "quality_filter_pdi/ai/ai_text_analyzer.py",
        "app/services/advanced_ai_analyzer.py": "quality_filter_pdi/ai/advanced_ai_analyzer.py",
        "app/services/cloud_ai_analyzer.py": "quality_filter_pdi/ai/cloud_ai_analyzer.py",
        
        # Utils
        "app/utils/text_utils.py": "quality_filter_pdi/utils/text_utils.py",
        
        # Main analyzer
        "app/pdi_analyzer.py": "quality_filter_pdi/pdi_analyzer.py",
        
        # CLI
        "main_v2.py": "cli/main.py",
        
        # Setup
        "setup_environment.ps1": "setup/setup_environment.ps1",
        "setup_environment.bat": "setup/setup_environment.bat",
        
        # Documentation
        "COMO_USAR.md": "documentation/COMO_USAR.md",
        "GUIA_COMPLETO.md": "documentation/GUIA_COMPLETO.md",
        "IMPLEMENTACAO_IA.md": "documentation/IMPLEMENTACAO_IA.md",
        "CONFIGURACAO_AMBIENTE.md": "documentation/CONFIGURACAO_AMBIENTE.md",
        "STATUS_CONFIGURACAO.md": "documentation/STATUS_CONFIGURACAO.md",
        
        # Examples
        "demo_final.py": "examples/demo_final.py",
        "demo_csv_direto.py": "examples/demo_csv_direto.py",
        "PROJETO_CONCLUIDO.py": "examples/projeto_concluido.py",
        "relatorio_final.py": "examples/relatorio_final.py",
        
        # Tests
        "test_system.py": "tests/integration/test_system.py",
        "test_complete.py": "tests/integration/test_complete.py",
        "test_simple.py": "tests/unit/test_simple.py",
        "test_skill_classification.py": "tests/unit/test_skill_classification.py",
        "final_validation.py": "tests/integration/final_validation.py",
        
        # Requirements
        "requirements.txt": "requirements.txt",
        "requirements_ai.txt": "requirements_ai.txt",
    }
    
    print("🔄 Reorganizando estrutura do projeto...")
    
    # Copiar arquivos para nova estrutura
    for old_path, new_path in file_mapping.items():
        old_file = base_path / old_path
        new_file = base_path / new_path
        
        if old_file.exists():
            # Criar diretório se não existir
            new_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copiar arquivo
            shutil.copy2(old_file, new_file)
            print(f"✅ {old_path} → {new_path}")
        else:
            print(f"⚠️ Arquivo não encontrado: {old_path}")
    
    # Criar __init__.py files
    init_dirs = [
        "quality_filter_pdi",
        "quality_filter_pdi/core", 
        "quality_filter_pdi/services",
        "quality_filter_pdi/utils",
        "quality_filter_pdi/ai",
        "tests",
        "tests/unit",
        "tests/integration"
    ]
    
    for dir_path in init_dirs:
        init_file = base_path / dir_path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print(f"✅ Criado: {dir_path}/__init__.py")

if __name__ == "__main__":
    reorganize_project()
    print("\n🎉 Reorganização concluída!")
    print("📁 Nova estrutura criada em quality_filter_pdi/")
    print("🔧 Execute: python cli/main.py")
