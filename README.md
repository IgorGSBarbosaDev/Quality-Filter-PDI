# Sistema de Análise de Qualidade PDI

## Visão Geral

Sistema inteligente para avaliar automaticamente a qualidade de Planos de Desenvolvimento Individual (PDI), fornecendo métricas detalhadas e classificação de qualidade.

## Características

- ✅ **Análise Automática**: Avalia PDIs usando 5 métricas de qualidade
- 📊 **Métricas Detalhadas**: Clareza, Especificidade, Completude, Estrutura e Critérios SMART
- 📁 **Suporte a Arquivos**: CSV e Excel com detecção automática de encoding
- 🏗️ **Arquitetura Modular**: Código organizado com princípios SOLID
- 🧪 **Testes Incluídos**: Suite completa de testes unitários

## Estrutura do Projeto

```
Quality Filter PDI/
├── app/                          # Aplicação principal
│   ├── core/                     # Configurações centrais
│   │   └── config.py            # Constantes e configurações
│   ├── services/                 # Camada de serviços
│   │   ├── file_service.py      # Serviços de arquivo
│   │   ├── pdi_analysis_service.py  # Análise de PDI
│   │   └── quality_metrics_service.py  # Cálculo de métricas
│   ├── utils/                    # Utilitários
│   │   └── text_utils.py        # Processamento de texto
│   ├── __init__.py              # Exports da aplicação
│   └── pdi_analyzer.py          # Interface principal
├── tests/                        # Testes unitários
│   └── test_pdi_analyzer.py     # Testes do sistema
├── examples/                     # Exemplos e demonstrações
│   └── demo.py                  # Script de demonstração
├── docs/                         # Documentação
├── scripts/                      # Scripts auxiliares
└── main_v2.py                   # Interface CLI
```

## Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd "Quality Filter PDI"
```

2. **Instale as dependências**:
```bash
pip install pandas openpyxl xlrd chardet
```

## Uso Rápido

### Análise de Texto

```python
from app import PDIAnalyzer

analyzer = PDIAnalyzer()

# Analisar PDI individual
resultado = analyzer.analyze_text(
    objetivo="Desenvolver competências em análise de dados",
    acoes="Completar curso de 60h e aplicar em 2 projetos"
)

print(f"Score: {resultado['overall_score']:.2f}")
print(f"Nível: {resultado['quality_level']}")
```

### Análise de Arquivo

```python
# Analisar arquivo CSV/Excel
resultado = analyzer.analyze_file("meus_pdis.csv")

if resultado['success']:
    print(f"Total analisado: {resultado['total_analyzed']}")
    print(f"Resumo: {resultado['summary']}")
```

### Interface de Linha de Comando

```bash
python main_v2.py
```

## Métricas de Qualidade

### 1. Clareza (25%)
- Complexidade de leitura
- Estrutura das sentenças
- Uso de linguagem clara

### 2. Especificidade (25%)
- Presença de números e datas
- Termos técnicos específicos
- Detalhamento das ações

### 3. Completude (25%)
- Comprimento adequado do texto
- Cobertura de aspectos importantes
- Densidade de informações

### 4. Estrutura (15%)
- Organização do conteúdo
- Uso de conectores
- Fluxo lógico

### 5. Critérios SMART (10%)
- Específico, Mensurável, Atingível
- Relevante, Temporal
- Presença de indicadores SMART

## Classificação de Qualidade

- **Alta (≥60%)**: PDI bem estruturado e específico
- **Média (30-59%)**: PDI adequado com melhorias possíveis  
- **Baixa (<30%)**: PDI requer reformulação significativa

## Formato de Arquivos

### CSV/Excel - Colunas Suportadas:
- `objetivo` / `objetivos` / `meta` / `metas`
- `acoes` / `ações` / `acao` / `ação` / `plano`

### Exemplo de CSV:
```csv
objetivo,acoes
"Desenvolver habilidades em Python","Completar curso de 40h até dezembro"
"Melhorar liderança","Liderar 2 projetos e fazer mentoria"
```

## Demonstração

Execute o script de demonstração:

```bash
python examples/demo.py
```

## Testes

Execute os testes unitários:

```bash
python -m unittest tests/test_pdi_analyzer.py
```

## Configuração

Personalize as configurações em `app/core/config.py`:

```python
# Pesos das métricas
METRIC_WEIGHTS = {
    'clarity': 0.25,
    'specificity': 0.25,
    'completeness': 0.25,
    'structure': 0.15,
    'smart_criteria': 0.10
}

# Limites de qualidade
QUALITY_THRESHOLDS = {
    'high': 0.6,
    'medium': 0.3
}
```

## Exemplos de Uso

### PDI de Alta Qualidade
```
Objetivo: Desenvolver competências avançadas em gestão de projetos ágeis
Ações: Completar certificação PSM I até março, aplicar em 3 projetos piloto
Score: 0.75 (Alta qualidade)
```

### PDI de Baixa Qualidade
```
Objetivo: Melhorar habilidades
Ações: Estudar mais
Score: 0.20 (Baixa qualidade)
```

## API Principal

### PDIAnalyzer

```python
class PDIAnalyzer:
    def analyze_text(self, objetivo: str, acoes: str) -> dict
    def analyze_file(self, file_path: str) -> dict
    def get_quality_recommendations(self, analysis_result: dict) -> list
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Entre em contato via email

---

**Desenvolvido com ❤️ para melhorar a qualidade dos PDIs**
- **Clareza**: Uso de linguagem clara e objetiva
- **Especificidade**: Detalhamento das ações e objetivos
- **Completude**: Presença de informações essenciais
- **Estrutura**: Organização lógica do conteúdo
- **Métrica SMART**: Específico, Mensurável, Atingível, Relevante, Temporal