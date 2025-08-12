"""
Script para limpeza e organização dos arquivos antigos.
"""
import os
import shutil
from pathlib import Path

# Arquivos a manter (além da nova estrutura)
KEEP_FILES = {
    'README.md',
    'requirements.txt', 
    'main_v2.py',
    'Relatório_de_PDI__Completo__2025_08_11_12_49_15.csv'  # Arquivo de dados do usuário
}

# Arquivos/pastas a remover
REMOVE_ITEMS = {
    'main.py',
    'setup.py', 
    'sistema_integrado.py',
    'pdi_analyzer_robust.py',
    'demo_csv_direto.py',
    'demo_simples.py',
    'diagnostico_completo.py',
    'execucao_automatica.py',
    'exemplo.py',
    'relatorio_final.py',
    'teste_basico.py',
    'test_csv.py',
    'test_quick.py',
    'test_system.py',
    'validate_system.py',
    'verificar_resultados.py',
    'src/',
    'config/',
    'data/',
    'output/',
    '__pycache__/',
    'DOCUMENTACAO.md',
    'INSTRUCOES.md', 
    'MELHORIAS.md'
}

# Arquivos CSV de saída antigos
OLD_CSV_PATTERN = [
    'analise_automatica_*.csv',
    'analise_qualidade_pdi_*.csv', 
    'analise_robusta_*.csv',
    'resumo_*.json'
]

def cleanup_project():
    """Remove arquivos antigos e organiza o projeto."""
    base_path = Path('.')
    
    print("🧹 Iniciando limpeza do projeto...")
    
    # Remove arquivos específicos
    for item in REMOVE_ITEMS:
        item_path = base_path / item
        if item_path.exists():
            if item_path.is_dir():
                shutil.rmtree(item_path)
                print(f"📁 Removido diretório: {item}")
            else:
                item_path.unlink()
                print(f"📄 Removido arquivo: {item}")
    
    # Remove arquivos CSV antigos
    import glob
    for pattern in OLD_CSV_PATTERN:
        for file in glob.glob(pattern):
            Path(file).unlink()
            print(f"📄 Removido arquivo CSV antigo: {file}")
    
    # Move arquivo de dados para examples se ainda não estiver lá
    data_file = Path('Relatório_de_PDI__Completo__2025_08_11_12_49_15.csv')
    if data_file.exists():
        target = Path('examples') / 'dados_exemplo.csv'
        shutil.move(str(data_file), str(target))
        print(f"📄 Arquivo de dados movido para: {target}")
    
    print("\n✅ Limpeza concluída!")
    print("\n📂 Estrutura final do projeto:")
    show_final_structure()

def show_final_structure():
    """Mostra a estrutura final do projeto."""
    def print_tree(path, prefix="", is_last=True):
        if path.name.startswith('.'):
            return
            
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{path.name}{'/' if path.is_dir() else ''}")
        
        if path.is_dir():
            children = [p for p in path.iterdir() if not p.name.startswith('.')]
            children.sort(key=lambda x: (not x.is_dir(), x.name))
            
            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                next_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(child, next_prefix, is_last_child)
    
    print_tree(Path('.'))

if __name__ == "__main__":
    cleanup_project()
