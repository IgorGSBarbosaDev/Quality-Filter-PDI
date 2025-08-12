import ssl
from typing import List
import nltk


class NLTKSetup:
    REQUIRED_DATASETS = ['punkt', 'stopwords']
    
    def __init__(self) -> None:
        self._configure_ssl()
    
    def _configure_ssl(self) -> None:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
    
    def setup_nltk(self) -> bool:
        print("Configurando NLTK...")
        
        success_count = 0
        for dataset in self.REQUIRED_DATASETS:
            if self._download_dataset(dataset):
                success_count += 1
        
        if success_count == len(self.REQUIRED_DATASETS):
            print("Configuração do NLTK concluída com sucesso!")
            return True
        else:
            print(f"Configuração parcialmente concluída: {success_count}/{len(self.REQUIRED_DATASETS)} datasets baixados")
            return False
    
    def _download_dataset(self, dataset: str) -> bool:
        try:
            nltk.data.find(f'tokenizers/{dataset}' if dataset == 'punkt' else f'corpora/{dataset}')
            print(f"Dataset '{dataset}' já disponível")
            return True
        except LookupError:
            try:
                print(f"Baixando dataset '{dataset}'...")
                nltk.download(dataset, quiet=True)
                print(f"Dataset '{dataset}' baixado com sucesso")
                return True
            except Exception as e:
                print(f"Erro ao baixar dataset '{dataset}': {e}")
                return False


def main() -> None:
    setup = NLTKSetup()
    setup.setup_nltk()


if __name__ == "__main__":
    main()
