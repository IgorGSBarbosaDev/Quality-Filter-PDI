"""
Script para configuração inicial do sistema
"""
import nltk
import ssl

def setup_nltk():
    """
    Configura NLTK baixando dados necessários
    """
    try:
        # Para alguns sistemas, pode ser necessário contornar problemas de SSL
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        print("Baixando dados do NLTK...")
        
        # Baixa dados necessários
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        print("Configuração do NLTK concluída!")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar NLTK: {e}")
        return False

if __name__ == "__main__":
    setup_nltk()
