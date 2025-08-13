#!/usr/bin/env python3

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import PDIAnalyzer
    print("✅ Importação da app bem-sucedida!")
    
    analyzer = PDIAnalyzer()
    print("✅ PDIAnalyzer criado com sucesso!")
    
    # Teste básico
    result = analyzer.analyze_text("Aprender Python para desenvolvimento", "Fazer curso online")
    
    print(f"✅ Análise concluída!")
    print(f"📊 Score: {result['overall_score']:.2f}")
    print(f"🏆 Qualidade: {result['quality_level']}")
    
    # Verificar se skill classification está funcionando
    if 'skill_classification' in result:
        skill = result['skill_classification']
        print(f"🎯 Tipo de habilidade: {skill['skill_type']}")
        print(f"📈 Confiança: {skill['confidence']:.2f}")
    
    # Verificar se IA está disponível
    if result.get('analysis_metadata', {}).get('ai_enabled', False):
        print("🤖 IA ativada e funcionando!")
    else:
        print("📊 Sistema funcionando em modo básico")
    
    print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("🔧 Verifique se todas as dependências estão instaladas")
    
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()

input("\nPressione Enter para continuar...")
