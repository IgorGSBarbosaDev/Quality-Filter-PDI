# Sistema de Qualificação de PDI (Plano de Desenvolvimento Individual)

Este projeto fornece uma solução automatizada para avaliar e classificar a qualidade de PDIs baseado na análise de texto dos campos "Ações planejadas" e "Objetivo de desenvolvimento".

## Funcionalidades

- Análise automatizada da qualidade dos textos de PDI
- Classificação em níveis: Baixo, Médio, Alto
- Sugestões de melhoria personalizadas
- Processamento de planilhas Excel
- Métricas detalhadas de qualidade

## Estrutura do Projeto

```
Quality Filter PDI/
├── src/
│   ├── pdi_analyzer.py      # Classe principal para análise
│   ├── quality_metrics.py   # Métricas de qualidade
│   └── text_processor.py    # Processamento de texto
├── data/
│   ├── input/              # Planilhas de entrada
│   └── output/             # Resultados processados
├── config/
│   └── settings.py         # Configurações
├── main.py                 # Script principal
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Coloque sua planilha na pasta `data/input/`
2. Execute o script principal:
   ```bash
   python main.py
   ```
3. Os resultados serão salvos em `data/output/`

## Critérios de Avaliação

A qualidade é avaliada com base em:
- **Clareza**: Uso de linguagem clara e objetiva
- **Especificidade**: Detalhamento das ações e objetivos
- **Completude**: Presença de informações essenciais
- **Estrutura**: Organização lógica do conteúdo
- **Métrica SMART**: Específico, Mensurável, Atingível, Relevante, Temporal
