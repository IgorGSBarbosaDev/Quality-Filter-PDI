# 🔧 Script de Configuração do Ambiente PDI
Write-Host "🚀 Configurando ambiente Python para PDI Quality Filter..." -ForegroundColor Green
Write-Host ""

# Configurar PATH temporário
$scriptsPath = "C:\Users\u014441\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts"
$env:PATH = "$scriptsPath;$env:PATH"

Write-Host "✅ PATH temporário configurado" -ForegroundColor Green
Write-Host "📦 Instalando dependências básicas..." -ForegroundColor Yellow

# Atualizar pip e instalar dependências básicas
python -m pip install --upgrade pip --no-warn-script-location
python -m pip install pandas>=2.0.0 --no-warn-script-location
python -m pip install openpyxl>=3.1.0 --no-warn-script-location  
python -m pip install xlrd>=2.0.0 --no-warn-script-location
python -m pip install chardet>=5.0.0 --no-warn-script-location

Write-Host ""
$installAI = Read-Host "🤖 Deseja instalar dependências de IA? (s/n)"

if ($installAI -eq "s" -or $installAI -eq "S") {
    Write-Host "📚 Instalando dependências de IA..." -ForegroundColor Yellow
    python -m pip install spacy>=3.7.0 --no-warn-script-location
    python -m pip install nltk>=3.8.0 --no-warn-script-location
    python -m pip install scikit-learn>=1.3.0 --no-warn-script-location
    python -m pip install numpy>=1.24.0 --no-warn-script-location
    python -m pip install requests>=2.31.0 --no-warn-script-location
    
    Write-Host "🇧🇷 Baixando modelo português do spaCy..." -ForegroundColor Cyan
    python -m spacy download pt_core_news_sm --no-warn-script-location
    
    Write-Host ""
    $installAdvanced = Read-Host "🔥 Deseja instalar IA avançada? (Transformers - requer ~2GB) (s/n)"
    
    if ($installAdvanced -eq "s" -or $installAdvanced -eq "S") {
        Write-Host "🧠 Instalando Transformers..." -ForegroundColor Magenta
        python -m pip install transformers>=4.35.0 --no-warn-script-location
        python -m pip install torch>=2.0.0 --no-warn-script-location
        python -m pip install sentence-transformers>=2.2.0 --no-warn-script-location
    }
}

Write-Host ""
Write-Host "✅ Instalação concluída!" -ForegroundColor Green
Write-Host "📋 Testando sistema..." -ForegroundColor Yellow

# Teste do sistema
$testCode = @"
try:
    from app import PDIAnalyzer
    analyzer = PDIAnalyzer()
    print('✅ Sistema PDI carregado com sucesso!')
    
    # Teste básico
    result = analyzer.analyze_text('Aprender Python', 'Fazer curso online')
    print(f'✅ Teste básico: Score {result["overall_score"]:.2f}')
    
    # Verificar se IA está disponível
    if result.get('analysis_metadata', {}).get('ai_enabled', False):
        print('🤖 IA ativada e funcionando!')
    else:
        print('📊 Sistema funcionando (IA não disponível)')
        
except Exception as e:
    print(f'❌ Erro: {e}')
    print('🔧 Verifique se está no diretório correto do projeto')
"@

python -c $testCode

Write-Host ""
Write-Host "🎯 Para adicionar permanentemente ao PATH (opcional):" -ForegroundColor Cyan
Write-Host "1. Abra Configurações do Sistema"
Write-Host "2. Vá em Variáveis de Ambiente"  
Write-Host "3. Adicione: $scriptsPath"
Write-Host ""
Write-Host "🚀 Sistema pronto! Execute: python main_v2.py" -ForegroundColor Green

Read-Host "Pressione Enter para continuar..."
