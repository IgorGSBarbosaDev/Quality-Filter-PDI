# 🔧 Configuração de Ambiente Python - Soluções para PATH

## 🚨 **Problema Identificado**
O Python foi instalado via Microsoft Store, e os scripts não estão no PATH do sistema.

**Diretório em questão:**
```
C:\Users\u014441\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts
```

## 🎯 **Soluções Implementadas**

### ✅ **Solução 1: Script Automático (Recomendado)**
Execute o arquivo `setup_environment.bat`:

```cmd
setup_environment.bat
```

**O que o script faz:**
- ✅ Configura PATH temporário
- ✅ Instala dependências básicas
- ✅ Opção para instalar IA
- ✅ Testa o sistema automaticamente
- ✅ Remove avisos de PATH

### ✅ **Solução 2: Configuração Manual Temporária**
```powershell
# No PowerShell, execute:
$env:PATH += ";C:\Users\u014441\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts"

# Instalar dependências
python -m pip install -r requirements.txt --no-warn-script-location
```

### ✅ **Solução 3: Configuração Permanente**
1. Pressione `Win + R`, digite `sysdm.cpl`
2. Clique em "Variáveis de Ambiente"
3. Em "Variáveis do usuário", selecione "Path" e clique "Editar"
4. Clique "Novo" e adicione:
   ```
   C:\Users\u014441\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts
   ```
5. Clique "OK" em todas as janelas

### ✅ **Solução 4: Usar pip com --no-warn-script-location**
```bash
python -m pip install pacote --no-warn-script-location
```

## 🚀 **Instalação Rápida (Recomendada)**

### Passo 1: Execute o script automático
```cmd
setup_environment.bat
```

### Passo 2: Teste o sistema
```cmd
python main_v2.py
```

## 📦 **Verificação de Instalação**

### Teste Básico
```python
python -c "
from app import PDIAnalyzer
analyzer = PDIAnalyzer()
result = analyzer.analyze_text('Teste', 'Ação teste')
print(f'✅ Sistema funcionando! Score: {result[\"overall_score\"]:.2f}')
"
```

### Teste com IA (se instalada)
```python
python -c "
from app import PDIAnalyzer
analyzer = PDIAnalyzer()
result = analyzer.analyze_text('Aprender Python para IA')
if 'ai_insights' in result:
    print('🤖 IA ativada!')
else:
    print('📊 Sistema básico ativo')
"
```

## 🔧 **Troubleshooting**

### Problema: "Comando não encontrado"
**Solução:** Execute `setup_environment.bat` ou configure PATH manualmente

### Problema: "ModuleNotFoundError"
**Solução:** 
```bash
python -m pip install -r requirements.txt --no-warn-script-location
```

### Problema: Erro de permissão
**Solução:** Execute como administrador ou use `--user`:
```bash
python -m pip install --user pacote --no-warn-script-location
```

### Problema: spaCy modelo não encontrado
**Solução:**
```bash
python -m spacy download pt_core_news_sm --no-warn-script-location
```

## 🎯 **Configurações por Cenário**

### 📊 **Uso Básico (Sem IA)**
```bash
python -m pip install pandas openpyxl xlrd chardet --no-warn-script-location
```

### 🤖 **Uso com IA Básica**
```bash
python -m pip install pandas openpyxl xlrd chardet spacy nltk scikit-learn --no-warn-script-location
python -m spacy download pt_core_news_sm --no-warn-script-location
```

### 🧠 **Uso com IA Avançada**
```bash
python -m pip install -r requirements_ai.txt --no-warn-script-location
```

## 📋 **Verificação Final**

Depois da configuração, teste:

```bash
# 1. Verificar PATH
echo $env:PATH | Select-String "Scripts"

# 2. Verificar instalação
python -c "import pandas, app; print('✅ Tudo funcionando!')"

# 3. Testar sistema completo
python main_v2.py
```

## 🎉 **Status Esperado Após Configuração**

```
✅ Python 3.11.9 detectado
✅ PATH configurado
✅ Dependências instaladas
✅ Sistema PDI funcionando
🤖 IA disponível (se instalada)
📊 Pronto para análise!
```

Execute `setup_environment.bat` e você estará pronto em 2 minutos! 🚀
