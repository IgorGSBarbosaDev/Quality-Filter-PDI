# Instruções de Uso - Sistema de Qualificação de PDI

## Configuração Inicial

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a configuração inicial:**
   ```bash
   python setup.py
   ```

## Como Usar

### Opção 1: Análise de Planilha Completa

1. **Coloque sua planilha Excel na pasta `data/input/`**
   - A planilha deve ter as colunas:
     - "Nome" - nome do colaborador
     - "Matrícula" - código de identificação
     - "Finalidade do objetivo" - posição atual ou desenvolvimento futuro
     - "Ações planejadas" - descrição das ações
     - "Objetivo de desenvolvimento" - meta final

2. **Execute o script principal:**
   ```bash
   python main.py
   ```

3. **Os resultados serão salvos em `data/output/`** com:
   - Planilha original + colunas de análise
   - Relatório resumido em JSON

### Opção 2: Teste com Dados de Exemplo

Execute o exemplo para ver o sistema funcionando:
```bash
python exemplo.py
```

## Resultados da Análise

### Colunas Adicionadas na Planilha:

- **`quality_level`**: Nível de qualidade (Baixo, Médio, Alto)
- **`quality_score`**: Pontuação numérica (0.0 a 1.0)
- **`suggestions`**: Sugestões específicas de melhoria
- **`clarity_score`**: Pontuação de clareza
- **`specificity_score`**: Pontuação de especificidade
- **`completeness_score`**: Pontuação de completude
- **`structure_score`**: Pontuação de estrutura
- **`smart_score`**: Pontuação dos critérios SMART

### Critérios de Avaliação:

1. **Clareza (25%)**
   - Linguagem objetiva e direta
   - Ausência de termos vagos
   - Facilidade de compreensão

2. **Especificidade (25%)**
   - Presença de números, prazos, medidas
   - Detalhamento adequado
   - Uso de termos precisos

3. **Completude (25%)**
   - Quantidade adequada de informação
   - Cobertura dos aspectos essenciais (como, quando, onde, por que)

4. **Estrutura (15%)**
   - Organização lógica
   - Sentenças bem construídas
   - Fluxo narrativo coerente

5. **Critérios SMART (10%)**
   - Específico, Mensurável, Atingível, Relevante, Temporal

### Níveis de Qualidade:

- **Alto**: Pontuação ≥ 0.8 (80%)
- **Médio**: Pontuação ≥ 0.6 (60%)
- **Baixo**: Pontuação < 0.6

## Personalizando o Sistema

### Modificar Thresholds de Qualidade

Edite o arquivo `config/settings.py`:
```python
ANALYSIS_CONFIG = {
    'quality_thresholds': {
        'low': 0.3,      # Limite inferior
        'medium': 0.6,   # Limite médio
        'high': 0.8      # Limite superior
    }
}
```

### Alterar Pesos das Métricas

```python
METRIC_WEIGHTS = {
    'clarity': 0.25,        # Peso da clareza
    'specificity': 0.25,    # Peso da especificidade
    'completeness': 0.25,   # Peso da completude
    'structure': 0.15,      # Peso da estrutura
    'smart_criteria': 0.10  # Peso dos critérios SMART
}
```

### Adaptar Nomes das Colunas

Se sua planilha tem nomes diferentes, edite:
```python
EXCEL_COLUMNS = {
    'nome': 'Nome',
    'matricula': 'Matrícula',
    'finalidade': 'Finalidade do objetivo',
    'acoes_planejadas': 'Ações planejadas',
    'objetivo_desenvolvimento': 'Objetivo de desenvolvimento'
}
```

## Exemplos de Sugestões de Melhoria

### PDI de Baixa Qualidade:
**Ações**: "Melhorar habilidades"
**Sugestões**: 
- Seja mais específico: Inclua números, prazos e medidas concretas
- Adicione mais detalhes: Explique como, quando e onde as ações serão realizadas
- Ações muito breves: Expanda para pelo menos 10 palavras

### PDI de Alta Qualidade:
**Ações**: "Realizar curso de Excel avançado com duração de 40 horas até dezembro de 2024..."
**Sugestões**: PDI de excelente qualidade! Continue mantendo esse padrão.

## Solução de Problemas

### Erro: "Colunas não encontradas"
- Verifique se os nomes das colunas na planilha correspondem aos definidos em `EXCEL_COLUMNS`
- O sistema mostra sugestões de colunas similares encontradas

### Erro: "Módulo não encontrado"
- Execute: `pip install -r requirements.txt`
- Verifique se está no diretório correto do projeto

### Baixa performance
- Para planilhas muito grandes (>1000 linhas), considere processar em lotes
- Reduza a complexidade das análises ajustando as configurações

## Suporte

Para dúvidas ou problemas:
1. Verifique os logs de erro no console
2. Confirme que todas as dependências estão instaladas
3. Teste com o arquivo de exemplo primeiro
