# 📋 Como Usar o Sistema de Análise de Qualidade PDI

## 🚀 Visão Geral

Este sistema analisa automaticamente a qualidade de Planos de Desenvolvimento Individual (PDI) usando 5 métricas específicas, fornecendo classificação e recomendações de melhoria.

## 📦 Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install pandas openpyxl xlrd chardet
```

ou usando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Estrutura do Projeto

```
Quality Filter PDI/
├── app/                    # Sistema principal
├── tests/                  # Testes unitários
├── examples/               # Exemplos
├── main_v2.py             # Interface CLI
└── README.md              # Documentação
```

## 🎯 Formas de Uso

### Método 1: Interface CLI (Mais Fácil)

Execute o sistema interativo:

```bash
python main_v2.py
```

O sistema apresentará um menu:

```
🚀 SISTEMA DE ANÁLISE DE QUALIDADE PDI
==================================================

📋 Escolha uma opção:
1. Analisar arquivo CSV/Excel
2. Análise de texto individual
3. Sair

Opção (1-3): 
```

#### Opção 1: Analisar Arquivo
- Digite o caminho do arquivo CSV ou Excel
- Escolha o tamanho da amostra (ou Enter para arquivo completo)
- Aguarde a análise
- Visualize os resultados na tela

#### Opção 2: Análise Individual
- Digite o objetivo do PDI
- Digite as ações planejadas
- Receba análise instantânea com score e recomendações

### Método 2: Programaticamente (Python)

```python
from app import PDIAnalyzer

# Criar analisador
analyzer = PDIAnalyzer()

# Análise de texto individual
resultado = analyzer.analyze_text(
    objetivo="Desenvolver competências em Python",
    acoes="Completar curso de 40 horas até dezembro"
)

print(f"Score: {resultado['overall_score']:.2f}")
print(f"Nível: {resultado['quality_level']}")

# Análise de arquivo
resultado = analyzer.analyze_file("meus_pdis.csv")
if resultado['success']:
    print(f"Total analisado: {resultado['total_analyzed']}")
    print(f"Resumo: {resultado['summary']}")
```

## 📊 Métricas de Qualidade

O sistema avalia PDIs usando 5 métricas:

### 1. **Clareza (25%)**
- Facilidade de compreensão
- Estrutura das sentenças
- Uso de linguagem clara

**Exemplo Bom:**
> "Desenvolver competências específicas em gestão de projetos ágeis"

**Exemplo Ruim:**
> "Melhorar coisas"

### 2. **Especificidade (25%)**
- Presença de números e datas
- Termos técnicos específicos
- Detalhamento das ações

**Exemplo Bom:**
> "Completar 40 horas de treinamento SAP módulo FI até março de 2024"

**Exemplo Ruim:**
> "Fazer treinamento"

### 3. **Completude (25%)**
- Comprimento adequado do texto
- Cobertura de aspectos importantes
- Densidade de informações

**Exemplo Bom:**
> "Realizar curso completo de Python, aplicar em 3 projetos práticos e documentar aprendizados"

**Exemplo Ruim:**
> "Estudar Python"

### 4. **Estrutura (15%)**
- Organização do conteúdo
- Uso de conectores lógicos
- Fluxo de ideias

**Exemplo Bom:**
> "Primeiro completar o curso, depois aplicar em projetos e finalmente obter certificação"

### 5. **Critérios SMART (10%)**
- **S**pecífico, **M**ensurável, **A**lcançável, **R**elevante, **T**emporal

**Exemplo SMART:**
> "Obter certificação PMP até dezembro de 2024 através de curso de 60 horas e exame oficial"

## 🏆 Classificação de Qualidade

### Alta Qualidade (≥60%)
✅ PDI bem estruturado e específico
- Contém todos os elementos necessários
- Objetivos claros e ações detalhadas
- Critérios SMART presentes

### Média Qualidade (30-59%)
⚠️ PDI adequado com melhorias possíveis
- Estrutura básica presente
- Alguns detalhes faltando
- Pode ser aprimorado

### Baixa Qualidade (<30%)
❌ PDI requer reformulação significativa
- Muito vago ou genérico
- Falta informações essenciais
- Necessita reescrita completa

## 📁 Formatos de Arquivo Suportados

### CSV
```csv
objetivo,acoes
"Desenvolver Python","Curso de 40h até dezembro"
"Melhorar liderança","Liderar 2 projetos"
```

### Excel (.xlsx, .xls)
| objetivo | acoes |
|----------|-------|
| Desenvolver Python | Curso de 40h até dezembro |
| Melhorar liderança | Liderar 2 projetos |

### Colunas Reconhecidas Automaticamente
- **Objetivos:** `objetivo`, `objetivos`, `meta`, `metas`, `objetivo de desenvolvimento`
- **Ações:** `acoes`, `ações`, `acao`, `ação`, `ações planejadas`, `plano`

## 💡 Exemplos Práticos

### Exemplo 1: PDI de Alta Qualidade

**Objetivo:**
> "Desenvolver competências avançadas em análise de dados utilizando Python e SQL para melhorar a tomada de decisões estratégicas"

**Ações:**
> "Completar curso de Data Science de 80 horas até março de 2024, aplicar conhecimentos em 3 projetos reais do departamento e obter certificação em Python for Data Analysis"

**Resultado:** Score 0.78 (Alta qualidade)

### Exemplo 2: PDI de Baixa Qualidade

**Objetivo:**
> "Melhorar habilidades"

**Ações:**
> "Estudar mais"

**Resultado:** Score 0.15 (Baixa qualidade)

## 🔧 Solucionando Problemas

### Problema: Arquivo não é reconhecido
**Solução:** Verifique se:
- O arquivo está no formato CSV ou Excel
- As colunas têm nomes reconhecidos
- O arquivo não está vazio

### Problema: Encoding incorreto
**Solução:** O sistema tenta automaticamente:
- utf-8
- latin-1
- iso-8859-1
- cp1252

### Problema: Resultados inesperados
**Solução:** Verifique se:
- Os textos não estão muito curtos
- Há informações suficientes nos campos
- Os objetivos e ações estão claros

## 📈 Interpretando Resultados

### Scores Detalhados
```python
{
    'overall_score': 0.65,        # Score geral (0-1)
    'quality_level': 'Alta',      # Classificação
    'clarity_score': 0.70,        # Clareza
    'specificity_score': 0.80,    # Especificidade
    'completeness_score': 0.60,   # Completude
    'structure_score': 0.55,      # Estrutura
    'smart_criteria_score': 0.40  # Critérios SMART
}
```

### Recomendações Automáticas
O sistema fornece sugestões específicas:
- "Melhore a clareza: use frases mais simples"
- "Adicione mais detalhes: números, datas e termos específicos"
- "Aplique critérios SMART: torne os objetivos mensuráveis"

## 🧪 Executando Testes

```bash
python -m unittest tests.test_pdi_analyzer -v
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os exemplos neste guia
2. Execute os testes para validar a instalação
3. Consulte o arquivo README.md
4. Abra uma issue no repositório

## 🎯 Dicas para PDIs de Alta Qualidade

### ✅ Faça
- Use números e datas específicas
- Inclua termos técnicos relevantes
- Descreva "como", "quando" e "onde"
- Estruture em sentenças completas
- Aplique critérios SMART

### ❌ Evite
- Textos muito curtos ou vagos
- Objetivos genéricos como "melhorar"
- Ações imprecisas como "estudar mais"
- Linguagem incerta ("talvez", "acho que")
- Falta de prazos ou métricas

---

**🎉 Agora você está pronto para usar o Sistema de Análise de Qualidade PDI!**
