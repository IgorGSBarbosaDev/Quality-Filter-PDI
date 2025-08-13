# 📊 Quality Filter PDI - Sistema de Análise de Qualidade de PDI

## 🎯 **Visão Geral**

Sistema avançado para análise automatizada de qualidade de Planos de Desenvolvimento Individual (PDI) com suporte a Inteligência Artificial.

### ✨ **Funcionalidades Principais**

- 🔍 **Análise de Qualidade**: 5 métricas especializadas
- 🤖 **Classificação de Habilidades**: Hard/Soft Skills com IA
- 📊 **Processamento em Lote**: CSV e Excel
- 🧠 **IA Integrada**: spaCy, Transformers, APIs Cloud
- 📈 **Relatórios Detalhados**: Insights e recomendações

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
├── 🎨 examples/                    # Exemplos de uso
├── 🔧 setup/                       # Scripts de configuração
├── 📂 data/                        # Dados de exemplo
│   └── samples/                   # Amostras de PDI
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
