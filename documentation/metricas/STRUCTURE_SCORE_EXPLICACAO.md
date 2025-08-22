# 🏗️ AVALIAÇÃO DO STRUCTURE_SCORE

## 📋 Visão Geral

O `structure_score` avalia a **estrutura e organização** do texto do PDI. Ele verifica se o texto está bem formatado, tem conectores lógicos, pontuação adequada e estrutura de frases apropriada.

---

## 🔢 Fórmula de Cálculo

O `structure_score` é calculado com base em **5 critérios principais**, com score máximo de **1.0 (10.0 na escala final)**:

### **Score Base: 0.2 pontos**
- Todo texto válido já recebe **0.2 pontos** como base

### **1. Conectores Lógicos: até 0.1 pontos**
Sistema verifica presença de conectores que demonstram organização do pensamento:

```python
conectores = ['e', 'mas', 'porém', 'então', 'assim', 'portanto', 'além disso']
```

- **+0.1 pontos** se pelo menos um conector for encontrado
- Indica que o texto tem **fluxo lógico** e **organização**

### **2. Capitalização Adequada: 0.2 pontos**
Verifica se o texto inicia com letra maiúscula:

```python
# Exemplo CORRETO: +0.2 pontos
"Desenvolver habilidades em Python..."

# Exemplo INCORRETO: 0 pontos
"desenvolver habilidades em python..."
```

### **3. Pontuação: 0.2 pontos**
Verifica presença de pontuação final (`.`, `!`, `?`):

```python
# Exemplo CORRETO: +0.2 pontos
"Aprender Python para desenvolvimento web."

# Exemplo INCORRETO: 0 pontos
"Aprender Python para desenvolvimento web"
```

### **4. Múltiplas Frases: até 0.3 pontos**
Analisa a quantidade de frases no texto:

```python
if sentences > 1:
    structure_score += min(0.3, sentences * 0.1)
```

- **1 frase**: 0 pontos extras
- **2 frases**: +0.2 pontos
- **3 frases**: +0.3 pontos
- **4+ frases**: +0.3 pontos (máximo)

---

## 📊 Exemplos Práticos

### **Exemplo 1: Structure Score BAIXO (0.2/1.0)**
```
Texto: "aprender python"
```

**Análise:**
- ✅ Score base: +0.2
- ❌ Conectores: 0 (não tem)
- ❌ Capitalização: 0 (não inicia com maiúscula)
- ❌ Pontuação: 0 (não tem ponto final)
- ❌ Múltiplas frases: 0 (só 1 frase)

**Total: 0.2/1.0 = 2.0/10.0**

### **Exemplo 2: Structure Score MÉDIO (0.6/1.0)**
```
Texto: "Aprender Python para desenvolvimento web."
```

**Análise:**
- ✅ Score base: +0.2
- ❌ Conectores: 0 (não tem conectores)
- ✅ Capitalização: +0.2 (inicia com "A")
- ✅ Pontuação: +0.2 (tem ponto final)
- ❌ Múltiplas frases: 0 (só 1 frase)

**Total: 0.6/1.0 = 6.0/10.0**

### **Exemplo 3: Structure Score ALTO (1.0/1.0)**
```
Texto: "Desenvolver habilidades em Python e Django. Fazer cursos online, então praticar em projetos pessoais. Além disso, participar de comunidades de desenvolvedores."
```

**Análise:**
- ✅ Score base: +0.2
- ✅ Conectores: +0.1 ("e", "então", "além disso")
- ✅ Capitalização: +0.2 (inicia com "D")
- ✅ Pontuação: +0.2 (tem pontos finais)
- ✅ Múltiplas frases: +0.3 (3 frases = 0.3 pontos)

**Total: 1.0/1.0 = 10.0/10.0**

---

## 🎯 O que o Structure Score Avalia

### ✅ **ASPECTOS POSITIVOS**
- **Organização textual**: Uso de conectores lógicos
- **Formatação adequada**: Capitalização e pontuação
- **Estrutura desenvolvida**: Múltiplas frases bem construídas
- **Profissionalismo**: Texto bem apresentado

### ❌ **ASPECTOS NEGATIVOS**
- **Texto mal formatado**: Sem maiúsculas ou pontuação
- **Frases simples demais**: Apenas uma frase curta
- **Falta de conectores**: Ideias desconectadas
- **Apresentação inadequada**: Texto "desleixado"

---

## 📈 Impacto no Score Final

O `structure_score` representa **uma das 5 dimensões** da qualidade do PDI:

```python
overall_score = (
    clarity_score * 0.25 +
    specificity_score * 0.25 +
    completeness_score * 0.20 +
    structure_score * 0.15 +      # 15% do score total
    smart_criteria_score * 0.15
)
```

### **Peso: 15% do score total**
- Um texto com structure_score = 1.0 contribui com **1.5 pontos** (15%)
- Um texto com structure_score = 0.2 contribui com **0.3 pontos** (3%)

---

## 💡 Dicas para Melhorar Structure Score

### **1. Use Capitalização Adequada**
```
❌ "aprender python"
✅ "Aprender Python"
```

### **2. Adicione Pontuação**
```
❌ "Desenvolver habilidades em Python"
✅ "Desenvolver habilidades em Python."
```

### **3. Use Conectores Lógicos**
```
❌ "Fazer curso. Praticar projetos."
✅ "Fazer curso e então praticar projetos."
```

### **4. Desenvolva em Múltiplas Frases**
```
❌ "Aprender Python."
✅ "Aprender Python através de cursos online. Praticar com projetos pessoais."
```

---

## 🔍 Implementação Técnica

```python
def calculate_structure(self, text: str) -> float:
    structure_score = 0.2  # Score base
    
    # Conectores lógicos
    conectores = ['e', 'mas', 'porém', 'então', 'assim', 'portanto', 'além disso']
    for connector in conectores:
        if connector.lower() in text.lower():
            structure_score += 0.1
            break  # Só conta uma vez
    
    # Capitalização adequada
    if text.strip() and text.strip()[0].isupper():
        structure_score += 0.2
    
    # Pontuação final
    if any(p in text for p in ['.', '!', '?']):
        structure_score += 0.2
    
    # Múltiplas frases
    sentences = text.count('.') + text.count('!') + text.count('?')
    if sentences > 1:
        structure_score += min(0.3, sentences * 0.1)
    
    return min(1.0, structure_score)
```

---

## 🎯 Resumo

O **Structure Score** é um indicador da **qualidade formal** do texto:

- **0.0-0.3**: Texto mal estruturado (pontuação, capitalização)
- **0.4-0.6**: Estrutura básica adequada
- **0.7-0.8**: Boa estrutura com conectores
- **0.9-1.0**: Excelente estrutura com múltiplas frases organizadas

É uma métrica que incentiva a **qualidade na apresentação** e **organização lógica** dos PDIs.
