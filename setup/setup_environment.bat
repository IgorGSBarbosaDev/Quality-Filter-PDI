@echo off
echo 🔧 Configurando ambiente Python para PDI Quality Filter...
echo.

REM Adicionar diretório Scripts ao PATH temporariamente
set "SCRIPTS_PATH=C:\Users\u014441\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts"
set "PATH=%SCRIPTS_PATH%;%PATH%"

echo ✅ PATH temporário configurado
echo 📦 Instalando dependências básicas...

python -m pip install --upgrade pip --no-warn-script-location
python -m pip install pandas>=2.0.0 --no-warn-script-location
python -m pip install openpyxl>=3.1.0 --no-warn-script-location
python -m pip install xlrd>=2.0.0 --no-warn-script-location
python -m pip install chardet>=5.0.0 --no-warn-script-location

echo.
echo 🤖 Deseja instalar dependências de IA? (s/n)
set /p install_ai="Resposta: "

if /i "%install_ai%"=="s" (
    echo 📚 Instalando dependências de IA...
    python -m pip install spacy>=3.7.0 --no-warn-script-location
    python -m pip install nltk>=3.8.0 --no-warn-script-location
    python -m pip install scikit-learn>=1.3.0 --no-warn-script-location
    python -m pip install numpy>=1.24.0 --no-warn-script-location
    python -m pip install requests>=2.31.0 --no-warn-script-location
    
    echo 🇧🇷 Baixando modelo português do spaCy...
    python -m spacy download pt_core_news_sm --no-warn-script-location
    
    echo.
    echo 🔥 Deseja instalar IA avançada? (Transformers - requer ~2GB) (s/n)
    set /p install_advanced="Resposta: "
    
    if /i "%install_advanced%"=="s" (
        echo 🧠 Instalando Transformers...
        python -m pip install transformers>=4.35.0 --no-warn-script-location
        python -m pip install torch>=2.0.0 --no-warn-script-location
        python -m pip install sentence-transformers>=2.2.0 --no-warn-script-location
    )
)

echo.
echo ✅ Instalação concluída!
echo 📋 Testando sistema...

python -c "
try:
    from app import PDIAnalyzer
    analyzer = PDIAnalyzer()
    print('✅ Sistema PDI carregado com sucesso!')
    
    # Teste básico
    result = analyzer.analyze_text('Aprender Python', 'Fazer curso online')
    print(f'✅ Teste básico: Score {result[\"overall_score\"]:.2f}')
    
    # Verificar se IA está disponível
    if result.get('analysis_metadata', {}).get('ai_enabled', False):
        print('🤖 IA ativada e funcionando!')
    else:
        print('📊 Sistema funcionando (IA não disponível)')
        
except Exception as e:
    print(f'❌ Erro: {e}')
    print('🔧 Verifique se está no diretório correto do projeto')
"

echo.
echo 🎯 Para adicionar permanentemente ao PATH (opcional):
echo 1. Abra Configurações do Sistema
echo 2. Vá em Variáveis de Ambiente
echo 3. Adicione: %SCRIPTS_PATH%
echo.
echo 🚀 Sistema pronto! Execute: python main_v2.py
pause
