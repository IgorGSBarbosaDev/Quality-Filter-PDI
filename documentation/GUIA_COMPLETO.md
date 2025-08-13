# 📋 Sistema de Análise PDI com Classificação de Habilidades

## 🚀 Visão Geral

Sistema automatizado para avaliar qualidade de PDIs e classificar tipos de habilidades (Hard Skills, Soft Skills, Híbridas).

### ✨ Funcionalidades Principais

1. **Análise de Qualidade**: 5 métricas de avaliação
2. **Classificação de Habilidades**: Hard/Soft Skills com confiança
3. **Suporte Multi-formato**: CSV e Excel
4. **Relatórios Inteligentes**: Insights e recomendações

## 📦 Instalação

### Pré-requisitos
- Python 3.11+
- pip

### Configuração
```bash
cd "Quality Filter PDI"
pip install -r requirements.txt
```

## 🎯 Uso Rápido

### Interface Interativa
```bash
python main_v2.py
```

### Código Python
```python
from app import PDIAnalyzer

analyzer = PDIAnalyzer()

# Análise individual
resultado = analyzer.analyze_text(
    objetivo="Aprender Python para desenvolvimento web",
    acoes="Fazer curso online, praticar projetos"
)

print(f"Score: {resultado['overall_score']:.2f}")
print(f"Qualidade: {resultado['quality_level']}")
print(f"Habilidade: {resultado['skill_classification']['skill_type']}")
print(f"Confiança: {resultado['skill_classification']['confidence']:.2f}")
```

## 📊 Estrutura dos Dados

### Entrada (CSV/Excel)
| Coluna | Descrição |
|--------|-----------|
| Objetivo de Desenvolvimento | Meta principal |
| Ações Planejadas | Estratégias de execução |
| Atividade de Aprendizagem | Métodos específicos |

### Saída Completa
```json
{
  "overall_score": 7.5,
  "quality_level": "Alta",
  "skill_classification": {
    "skill_type": "Hard Skill",
    "confidence": 0.85,
    "recommendation": "Foque em certificações técnicas"
  },
  "clarity_score": 8.0,
  "specificity_score": 7.5,
  "completeness_score": 7.0,
  "structure_score": 8.0,
  "smart_criteria_score": 7.0
}
```

## 🔍 Métricas de Qualidade

### 1. Clareza (25%)
Avalia compreensibilidade e ausência de ambiguidades

### 2. Especificidade (25%)
Mede detalhamento e precisão das informações

### 3. Completude (25%)
Verifica presença de informações necessárias

### 4. Estrutura (15%)
Analisa organização e formatação

### 5. Critérios SMART (10%)
Aderência aos critérios SMART

## 🎯 Classificação de Habilidades

### Hard Skills
- **Características**: Competências técnicas mensuráveis
- **Exemplos**: Python, Excel, AWS, SQL, Certificações
- **Identificação**: Palavras-chave técnicas, tecnologias, ferramentas

### Soft Skills
- **Características**: Competências comportamentais
- **Exemplos**: Liderança, Comunicação, Trabalho em equipe
- **Identificação**: Termos comportamentais, habilidades interpessoais

### Híbridas
- **Características**: Combinação técnica + comportamental
- **Exemplos**: Gestão de projetos, Análise de dados
- **Identificação**: Presença de ambos os tipos

### Sistema de Confiança
- **Alta (0.8-1.0)**: Classificação muito confiável
- **Média (0.6-0.79)**: Classificação provável
- **Baixa (0.4-0.59)**: Classificação incerta
- **Muito Baixa (<0.4)**: Classificação não confiável

## 📈 Exemplos Práticos

### Exemplo 1: Hard Skill
```python
objetivo = "Obter certificação AWS Solutions Architect até dezembro"
acoes = "Estudar documentação oficial, fazer labs práticos"

# Resultado esperado:
# - Tipo: Hard Skill
# - Confiança: 0.90
# - Recomendação: "Foque em certificações técnicas e prática hands-on"
```

### Exemplo 2: Soft Skill
```python
objetivo = "Desenvolver habilidades de liderança de equipe"
acoes = "Participar de workshops, aplicar técnicas em projetos"

# Resultado esperado:
# - Tipo: Soft Skill
# - Confiança: 0.85
# - Recomendação: "Foque em desenvolvimento comportamental e feedback 360°"
```

### Exemplo 3: Habilidade Híbrida
```python
objetivo = "Melhorar gestão de projetos usando metodologias ágeis"
acoes = "Estudar Scrum, aplicar em projetos reais, obter certificação"

# Resultado esperado:
# - Tipo: Hybrid
# - Confiança: 0.80
# - Recomendação: "Combine conhecimento técnico com habilidades de gestão"
```

## 🛠️ Configurações Avançadas

### Personalizar Classificação
Edite `app/services/skill_classifier.py`:

```python
# Adicionar novas palavras-chave
hard_skills_keywords.update({
    'nova_tecnologia', 'ferramenta_especifica'
})

soft_skills_keywords.update({
    'nova_habilidade_comportamental'
})
```

### Ajustar Pesos de Qualidade
Edite `app/core/config.py`:

```python
METRIC_WEIGHTS = {
    'clarity': 0.30,        # Aumentar importância da clareza
    'specificity': 0.25,
    'completeness': 0.25,
    'structure': 0.10,
    'smart_criteria': 0.10
}
```

## 🎪 Interface Interativa

O sistema oferece menu intuitivo:

```
🚀 SISTEMA DE ANÁLISE DE QUALIDADE PDI
==================================================

📋 Escolha uma opção:
1. Analisar arquivo CSV/Excel
2. Análise de texto individual
3. Sair

Opção (1-3): 2

📝 Digite o objetivo de desenvolvimento:
> Aprender Python para análise de dados

📋 Digite as ações planejadas:
> Fazer curso online, praticar com datasets reais

📊 RESULTADO DA ANÁLISE
==============================
📈 Score Geral: 7.50
🏆 Nível de Qualidade: Alta

🎯 CLASSIFICAÇÃO DE HABILIDADE:
   📚 Tipo: Hard Skill
   📊 Confiança: 0.88
   💡 Recomendação: Foque em certificações técnicas e prática hands-on

📋 Detalhamento:
   📝 Clareza: 8.00
   🎯 Especificidade: 7.50
   📖 Completude: 7.00
   🏗️ Estrutura: 8.00
   🎯 SMART: 7.00
```

## 📂 Análise de Arquivos

### Formato CSV Exemplo
```csv
Objetivo de Desenvolvimento,Ações Planejadas,Atividade de Aprendizagem
"Aprender Python para análise de dados","Curso online + projetos práticos","Curso Data Science"
"Desenvolver liderança","Workshops + aplicação prática","Workshop Liderança Ágil"
"Certificação PMP","Estudar PMBOK + simulados","Curso preparatório PMP"
```

### Resultado da Análise
```
📊 RESULTADOS DA ANÁLISE
========================================
📈 Total analisado: 3 PDIs
🟢 Qualidade ALTA: 2 PDIs (66.7%)
🟡 Qualidade MÉDIA: 1 PDIs (33.3%)
🔴 Qualidade BAIXA: 0 PDIs (0.0%)

💾 Resultados salvos em: output/analysis_20240813_100230.csv
```

O arquivo de saída inclui:
- Todas as métricas de qualidade
- Classificação de habilidades
- Nível de confiança
- Recomendações específicas

## 🔧 Troubleshooting

### Problemas Comuns

1. **Arquivo não encontrado**
   ```bash
   # Use caminho absoluto
   C:\Users\usuario\Documents\arquivo.csv
   ```

2. **Encoding de arquivo**
   ```python
   # Sistema detecta automaticamente:
   # UTF-8, Latin-1, ISO-8859-1, CP1252
   ```

3. **Colunas não reconhecidas**
   ```python
   # Verifique mapeamento em config.py
   COLUMN_MAPPING = {
       'objetivo_desenvolvimento': 'Seu_Nome_Coluna'
   }
   ```

### Debug Avançado
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Logs detalhados serão exibidos
```

## 🎨 Extensibilidade

### Adicionar Nova Métrica
1. Edite `QualityMetricsService`
2. Implemente método `calculate_nova_metric()`
3. Atualize pesos em `config.py`

### Melhorar Classificação
1. Expanda keywords em `SkillClassifier`
2. Adicione padrões regex específicos
3. Ajuste algoritmo de confiança

### Custom Reports
1. Modifique `FileService` para novo formato
2. Personalize templates de saída
3. Adicione visualizações

## 📋 Limiares de Qualidade

- **Alta**: Score ≥ 7.0
- **Média**: Score 5.0-6.9  
- **Baixa**: Score < 5.0

## 🎯 Recomendações por Tipo

### Hard Skills
- Foque em certificações técnicas
- Pratique hands-on
- Estude documentação oficial
- Construa portfólio técnico

### Soft Skills
- Busque feedback 360°
- Pratique em situações reais
- Desenvolva auto-conhecimento
- Aplique em contextos diversos

### Híbridas
- Combine teoria e prática
- Equilibre aspectos técnicos e humanos
- Busque projetos multidisciplinares
- Desenvolva visão sistêmica

## 📞 Suporte

Para dúvidas ou melhorias:
1. Consulte este guia
2. Analise exemplos incluídos
3. Verifique logs de erro
4. Teste com dados menores primeiro
