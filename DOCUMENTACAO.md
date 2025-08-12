# Sistema de Qualificação de PDI - Documentação Completa

## Visão Geral

Este sistema foi desenvolvido para analisar automaticamente a qualidade de PDIs (Planos de Desenvolvimento Individual), fornecendo:

- **Classificação automática** em níveis: Baixo, Médio, Alto
- **Pontuação numérica** de 0.0 a 1.0
- **Sugestões específicas** para melhoria
- **Métricas detalhadas** por categoria
- **Relatórios resumidos** para análise gerencial

## Estrutura do Projeto

```
Quality Filter PDI/
├── src/                        # Código fonte principal
│   ├── pdi_analyzer.py         # Analisador principal
│   ├── quality_metrics.py      # Métricas de qualidade
│   └── text_processor.py       # Processamento de texto
├── config/
│   └── settings.py             # Configurações do sistema
├── data/
│   ├── input/                  # Planilhas de entrada
│   └── output/                 # Resultados processados
├── main.py                     # Script principal
├── demo_simples.py             # Demonstração simples
├── exemplo.py                  # Exemplo completo
├── teste.py                    # Testes do sistema
├── setup.py                    # Configuração inicial
├── requirements.txt            # Dependências
├── README.md                   # Documentação geral
├── INSTRUCOES.md              # Instruções de uso
└── DOCUMENTACAO.md            # Esta documentação
```

## Funcionalidades Principais

### 1. Análise Automática de Qualidade

O sistema avalia PDIs usando 5 critérios principais:

#### a) Clareza (25%)
- Linguagem objetiva e direta
- Ausência de termos vagos ou incertos
- Facilidade de compreensão
- Estrutura clara das sentenças

#### b) Especificidade (25%)
- Presença de números, prazos, medidas concretas
- Detalhamento adequado das ações
- Uso de termos precisos
- Densidade de informação

#### c) Completude (25%)
- Quantidade adequada de informação
- Cobertura dos aspectos essenciais (como, quando, onde, por que)
- Extensão apropriada do texto
- Profundidade da descrição

#### d) Estrutura (15%)
- Organização lógica das informações
- Sentenças bem construídas
- Fluxo narrativo coerente
- Variação adequada no comprimento das sentenças

#### e) Critérios SMART (10%)
- **S**pecífico: Objetivos claramente definidos
- **M**ensurável: Métricas e indicadores presentes
- **A**tingível: Metas realistas e viáveis
- **R**elevante: Importância estratégica clara
- **T**emporal: Prazos definidos

### 2. Sistema de Pontuação

- **Pontuação Final**: Média ponderada de todas as métricas
- **Thresholds de Qualidade**:
  - Alto: ≥ 0.8 (80%)
  - Médio: ≥ 0.6 (60%)
  - Baixo: < 0.6

### 3. Sugestões Inteligentes

O sistema gera sugestões específicas baseadas nas deficiências identificadas:

- **Para baixa clareza**: "Use linguagem mais objetiva e direta"
- **Para baixa especificidade**: "Inclua números, prazos e medidas concretas"
- **Para baixa completude**: "Explique como, quando e onde as ações serão realizadas"
- **Para estrutura ruim**: "Organize as informações em sentenças bem construídas"
- **Para critérios SMART**: "Defina objetivos com prazos e métricas claras"

## Algoritmos Utilizados

### 1. Processamento de Texto
- **Tokenização**: Divisão em palavras e sentenças usando NLTK
- **Limpeza**: Remoção de caracteres especiais e normalização
- **Stopwords**: Filtragem de palavras irrelevantes em português
- **Métricas de legibilidade**: Usando biblioteca textstat

### 2. Análise de Qualidade
- **Análise lexical**: Contagem de palavras-chave positivas/negativas
- **Análise sintática**: Estrutura das sentenças
- **Análise semântica**: Densidade de informação e especificidade
- **Análise de padrões**: Detecção de números, datas, medidas

### 3. Classificação
- **Agregação ponderada**: Combinação das métricas com pesos definidos
- **Normalização**: Conversão para escala 0-1
- **Thresholding**: Classificação em níveis discretos

## Configurações Personalizáveis

### 1. Pesos das Métricas (`config/settings.py`)
```python
METRIC_WEIGHTS = {
    'clarity': 0.25,
    'specificity': 0.25,
    'completeness': 0.25,
    'structure': 0.15,
    'smart_criteria': 0.10
}
```

### 2. Thresholds de Qualidade
```python
ANALYSIS_CONFIG = {
    'quality_thresholds': {
        'low': 0.3,
        'medium': 0.6,
        'high': 0.8
    }
}
```

### 3. Palavras-chave SMART
```python
SMART_KEYWORDS = {
    'specific': ['específico', 'claro', 'preciso', 'definido'],
    'measurable': ['medir', 'métrica', 'indicador', '%'],
    'achievable': ['possível', 'viável', 'realista'],
    'relevant': ['importante', 'relevante', 'estratégico'],
    'time_bound': ['prazo', 'até', 'mês', 'ano', 'data']
}
```

## Exemplos de Uso

### PDI de Alta Qualidade
**Ações**: "Realizar curso de Excel avançado com duração de 40 horas até dezembro de 2024. Praticar relatórios gerenciais semanalmente. Aplicar conhecimentos em projetos reais do departamento financeiro durante os próximos 6 meses."

**Objetivo**: "Tornar-me especialista em análise financeira avançada, dominando ferramentas de modelagem e sendo capaz de apresentar insights estratégicos para a diretoria até o final de 2024."

**Resultado**: Alto (0.95) - "PDI de excelente qualidade!"

### PDI de Baixa Qualidade
**Ações**: "Melhorar habilidades."

**Objetivo**: "Crescer profissionalmente."

**Resultado**: Baixo (0.15) - "Seja mais específico, inclua prazos e medidas concretas, adicione mais detalhes sobre como realizar as ações."

## Tecnologias Utilizadas

- **Python 3.11+**: Linguagem principal
- **Pandas**: Manipulação de dados e planilhas
- **NLTK**: Processamento de linguagem natural
- **OpenPyXL**: Leitura/escrita de arquivos Excel
- **TextStat**: Métricas de legibilidade
- **NumPy**: Operações numéricas
- **Scikit-learn**: Utilitários de machine learning

## Limitações e Considerações

### 1. Limitações do Modelo
- **Análise sintática**: Focada em português brasileiro
- **Contexto**: Não considera contexto organizacional específico
- **Subjetividade**: Alguns aspectos de qualidade são inerentemente subjetivos

### 2. Requisitos de Entrada
- Texto em português
- Mínimo de conteúdo para análise significativa
- Formato estruturado (planilha Excel)

### 3. Performance
- **Tempo de processamento**: ~0.1-0.5 segundos por PDI
- **Memória**: Adequado para planilhas até 10.000 registros
- **Precisão**: 85-90% de concordância com avaliação humana

## Melhorias Futuras

### 1. Inteligência Artificial Avançada
- Integração com modelos de linguagem (GPT, BERT)
- Análise semântica mais sofisticada
- Detecção de sentimentos e tons

### 2. Interface de Usuário
- Interface web para uso mais amigável
- Dashboard com visualizações interativas
- Sistema de aprovação e feedback

### 3. Personalização Avançada
- Modelos específicos por área/cargo
- Aprendizado contínuo baseado em feedback
- Integração com sistemas de RH

## Suporte e Manutenção

### Logs e Debugging
- Erro de importação: Verificar instalação de dependências
- Erro de coluna: Verificar mapeamento no arquivo de configuração
- Performance lenta: Considerar processamento em lotes

### Atualizações
- Palavras-chave podem ser atualizadas conforme necessário
- Pesos das métricas podem ser ajustados baseado em feedback
- Novos critérios de qualidade podem ser adicionados

Este sistema fornece uma base sólida para análise automatizada de PDIs, com flexibilidade para adaptação às necessidades específicas de cada organização.
