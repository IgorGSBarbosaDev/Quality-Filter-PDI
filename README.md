# 📊 Quality Filter PDI - Sistema de Análise de Qualidade de PDI

## 🎯 **Visão Geral**

Sistema avançado para análise automatizada de qualidade de Planos de Desenvolvimento Individual (PDI) com suporte a Inteligência Artificial.

### ✨ **Funcionalidades Principais**

- 🔍 **Análise de Qualidade**: 5 métricas especializadas
- 🤖 **Classificação de Habilidades**: Hard/Soft Skills com IA  
- 📊 **Processamento em Lote**: CSV e Excel
- 🧠 **IA Integrada**: spaCy, Transformers, APIs Cloud
- 📈 **Relatórios Detalhados**: Insights e recomendações
- 🎯 **Explicação de Notas**: Breakdown detalhado de cada avaliação
- 💬 **Feedback Personalizado**: Orientações diretas para o responsável pelo PDI

## 📁 **Estrutura do Projeto**

```
Quality Filter PDI/
├── 📦 quality_filter_pdi/          # Pacote principal
│   ├── 🧠 ai/                      # Módulos de IA
│   │   ├── ai_text_analyzer.py     # IA básica (spaCy/NLTK)
│   │   ├── advanced_ai_analyzer.py # IA avançada (Transformers)
│   │   └── cloud_ai_analyzer.py    # IA cloud (GPT/Gemini)
│   ├── 🔧 core/                    # Configurações centrais
│   │   └── config.py               # Constantes e configurações
│   ├── 🎯 services/                # Serviços de negócio
│   │   ├── pdi_analysis_service.py # Análise de PDI
│   │   ├── quality_metrics_service.py # Métricas de qualidade
│   │   ├── file_service.py         # Processamento de arquivos
│   │   └── skill_classifier.py     # Classificação de habilidades
│   ├── 🛠️ utils/                   # Utilitários
│   │   └── text_utils.py           # Processamento de texto
│   └── pdi_analyzer.py             # Interface principal
├── 💻 cli/                         # Interface de linha de comando
│   └── main.py                     # Aplicação principal
├── 📚 documentation/               # Documentação completa
│   ├── COMO_USAR.md               # Guia de uso
│   ├── GUIA_COMPLETO.md           # Documentação completa
│   ├── IMPLEMENTACAO_IA.md        # Guia de IA
│   └── CONFIGURACAO_AMBIENTE.md   # Setup do ambiente
├── 🧪 tests/                       # Testes automatizados
│   ├── unit/                      # Testes unitários
│   └── integration/               # Testes de integração
├── 🎨 examples/                    # Exemplos práticos de uso
│   ├── 01_uso_basico.py           # Uso básico do sistema
│   ├── 02_feedback_responsavel.py # Feedback personalizado
│   ├── 03_motivos_concisos.py     # Motivos de avaliação
│   ├── 04_explicacao_notas.py     # Explicações detalhadas
│   ├── 05_relatorio_completo.py   # Relatório completo
│   └── *.csv                      # Dados de exemplo
├── 🔧 setup/                       # Scripts de configuração
└── 📄 output/                      # Resultados de análise
```

## 🚀 **Instalação Rápida**

### 1. **Setup Automático (Recomendado)**
```bash
# Execute o script de configuração
PowerShell -ExecutionPolicy Bypass -File setup/setup_environment.ps1
```

### 2. **Instalação Manual**
```bash
# Dependências básicas
pip install pandas openpyxl xlrd chardet

# IA básica (opcional)
pip install spacy nltk scikit-learn
python -m spacy download pt_core_news_sm

# IA avançada (opcional)
pip install transformers torch sentence-transformers
```

## 💻 **Uso Básico**

### Interface Interativa
```bash
python cli/main.py
```

### Uso Programático
```python
from quality_filter_pdi import PDIAnalyzer

analyzer = PDIAnalyzer()

# Análise individual
resultado = analyzer.analyze_text(
    objetivo="Aprender Python para Data Science",
    acoes="Fazer curso online, praticar projetos"
)

print(f"Score: {resultado['overall_score']:.2f}")
print(f"Qualidade: {resultado['quality_level']}")
print(f"Habilidade: {resultado['skill_classification']['skill_type']}")

# Análise de arquivo
resultado = analyzer.analyze_file("pdis.csv")
```

## 📊 **Métricas de Qualidade**

| Métrica | Peso | Descrição |
|---------|------|-----------|
| **Clareza** | 25% | Compreensibilidade do objetivo |
| **Especificidade** | 25% | Nível de detalhamento |
| **Completude** | 25% | Presença de informações necessárias |
| **Estrutura** | 15% | Organização do texto |
| **SMART** | 10% | Aderência aos critérios SMART |

### 🎯 **Nova Funcionalidade: Explicação Detalhada das Notas**

Cada PDI analisado agora inclui uma **explicação completa** de como a nota foi calculada:

```
============================================================
📊 DETALHAMENTO DA AVALIAÇÃO
============================================================

🎯 NOTA FINAL: 78.5/100

📋 BREAKDOWN POR CRITÉRIO:
----------------------------------------
• Clareza        (25%): 21.3 pontos (base: 85.0/100)
• Especificidade (25%): 20.0 pontos (base: 80.0/100)
• Completude     (25%): 18.8 pontos (base: 75.0/100)
• Estrutura      (15%): 10.5 pontos (base: 70.0/100)
• Critérios SMART(10%):  6.5 pontos (base: 65.0/100)

🔍 ANÁLISE DETALHADA:
----------------------------------------
✅ CLAREZA (EXCELENTE): Texto muito claro e compreensível
✅ ESPECIFICIDADE (EXCELENTE): Muito específico e detalhado
⚠️  COMPLETUDE (REGULAR): Faltam algumas informações
✅ ESTRUTURA (BOA): Bem estruturado
✅ SMART (BOA): Atende razoavelmente aos critérios SMART

🎯 CLASSIFICAÇÃO GERAL:
✅ BOM - PDI de boa qualidade
============================================================
```

**Benefícios:**
- ✅ **Transparência total** na avaliação
- ✅ **Feedback específico** para melhorias  
- ✅ **Compreensão clara** dos critérios
- ✅ **Facilita correções** direcionadas

A explicação é salva na coluna `score_explanation` do arquivo CSV gerado.

### 💬 **Nova Funcionalidade: Feedback Personalizado para o Responsável**

Cada PDI analisado agora inclui um **feedback direto e personalizado** para o responsável, explicando de forma clara o motivo da nota recebida:

```
🌟 FEEDBACK PARA O SEU PDI - NOTA: 85.2/100 (EXCELENTE)

🎉 PARABÉNS! Seu PDI está excelente!
Seu objetivo está muito bem definido e suas ações são claras e específicas.

💡 PRINCIPAIS MOTIVOS DA SUA NOTA:

🔍 CLAREZA - Muito bom! ✅
• Seu objetivo está claro e fácil de entender

🎯 ESPECIFICIDADE - Excelente! ✅  
• Seu PDI tem detalhes específicos e mensuráveis

🚀 PRÓXIMOS PASSOS PARA MELHORAR:
1. Continue mantendo este excelente padrão
2. Use seu PDI como exemplo para futuros objetivos
3. Acompanhe regularmente seu progresso
```

**Características do Feedback:**
- ✅ **Linguagem direta e amigável** para o colaborador
- ✅ **Orientações práticas** para cada critério
- ✅ **Ações específicas** para melhoria
- ✅ **Tom motivacional** e construtivo

**Duas colunas complementares no arquivo:**
- `score_explanation`: Explicação técnica detalhada (para analistas/RH)
- `feedback_responsavel`: Feedback direto para o responsável do PDI

O feedback é salvo na coluna `feedback_responsavel` do arquivo CSV gerado.

## 🎯 **Classificação de Habilidades**

### Hard Skills
- Competências técnicas mensuráveis
- Exemplos: Python, Excel, AWS, SQL
- Confiança baseada em palavras-chave técnicas

### Soft Skills  
- Competências comportamentais
- Exemplos: Liderança, Comunicação, Trabalho em equipe
- Confiança baseada em termos comportamentais

### Híbridas
- Combinação de aspectos técnicos e comportamentais
- Exemplos: Gestão de projetos, Análise de dados

## 🤖 **Recursos de IA**

### IA Básica (spaCy/NLTK)
- ✅ Análise semântica em português
- ✅ Extração de entidades automática
- ✅ Detecção de intenções
- ✅ Zero custo e offline

### IA Avançada (Transformers)
- 🧠 BERT português para contexto
- 📊 Análise de sentimento profunda
- 🎯 Classificação contextual
- 📈 Precisão 85%+

### IA Cloud (APIs)
- 🌟 GPT-4/Gemini integration
- 💡 Insights únicos de IA
- 📝 Sugestões contextuais
- 🎯 Análise multi-dimensional

## 📈 **Exemplos de Resultados**

### Análise Básica
```json
{
  "overall_score": 7.5,
  "quality_level": "Alta",
  "skill_classification": {
    "skill_type": "Hard Skill",
    "confidence": 0.85
  }
}
```

### Com IA Ativada
```json
{
  "overall_score": 7.8,
  "quality_level": "Alta", 
  "ai_enhanced": true,
  "ai_insights": {
    "semantic_coherence": 0.90,
    "smart_suggestions": [
      "Especifique versão Python (3.11+)",
      "Adicione projeto prático",
      "Defina certificação objetivo"
    ]
  }
}
```

## 🧪 **Testes**

```bash
# Testes unitários
python -m pytest tests/unit/

# Testes de integração  
python -m pytest tests/integration/

# Teste completo do sistema
python tests/integration/test_system.py
```

## 📚 **Documentação**

- 📖 [Guia Completo](documentation/GUIA_COMPLETO.md)
- 🤖 [Implementação de IA](documentation/IMPLEMENTACAO_IA.md)
- 🔧 [Configuração do Ambiente](documentation/CONFIGURACAO_AMBIENTE.md)
- 💻 [Como Usar](documentation/COMO_USAR.md)

## 🎨 **Exemplos**

Consulte a pasta `examples/` para:
- Demo com CSV direto
- Projeto completo
- Relatórios finais
- Validações

## ⚙️ **Configuração**

### Personalizar Métricas
```python
# Em quality_filter_pdi/core/config.py
METRIC_WEIGHTS = {
    'clarity': 0.30,        # Aumentar peso da clareza
    'specificity': 0.25,
    'completeness': 0.25,
    'structure': 0.10,
    'smart_criteria': 0.10
}
```

### Ajustar Limiares
```python
QUALITY_THRESHOLDS = {
    'low': 0.3,
    'medium': 0.6,
    'high': 0.8
}
```

## 🎯 **Roadmap**

### ✅ Versão 2.0 (Atual)
- [x] Análise de qualidade completa
- [x] Classificação de habilidades
- [x] IA integrada
- [x] Interface CLI
- [x] Estrutura reorganizada

### 🔄 Versão 2.1 (Próxima)
- [ ] Interface web
- [ ] Dashboard analytics
- [ ] API REST
- [ ] Modelos customizados

### 🚀 Versão 3.0 (Futuro)
- [ ] IA generativa para PDIs
- [ ] Recomendações de carreira
- [ ] Análise preditiva
- [ ] Integração com sistemas HR

## 👥 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está licenciado sob a MIT License.

## 🎉 **Status do Projeto**

**✅ Produção Ready**
- Sistema completo e testado
- IA integrada e funcional
- Documentação completa
- Estrutura profissional

---

**🚀 Pronto para uso! Execute `python cli/main.py` e comece a analisar seus PDIs!**
