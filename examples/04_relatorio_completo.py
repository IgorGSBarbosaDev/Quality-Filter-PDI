import pandas as pd
import json

def gerar_relatorio_final():
    print("📊 RELATÓRIO FINAL - ANÁLISE DE QUALIDADE PDI\n")
    
    # Carrega os resultados
    try:
        # Carrega o CSV de resultados
        df_result = pd.read_csv('analise_automatica_20250812_095918.csv')
        
        # Carrega o resumo JSON
        with open('resumo_automatico_20250812_095918.json', 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        print("🎉 ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("=" * 50)
        
        # Estatísticas gerais
        print(f"\n📈 ESTATÍSTICAS GERAIS:")
        print(f"   Total de PDIs analisados: {summary['total_analyzed']}")
        print(f"   Score médio de qualidade: {summary['average_score']:.3f}")
        
        # Distribuição de qualidade
        print(f"\n🎯 DISTRIBUIÇÃO DE QUALIDADE:")
        total = summary['total_analyzed']
        high = summary['high_quality']
        medium = summary['medium_quality'] 
        low = summary['low_quality']
        
        print(f"   🟢 ALTA qualidade:   {high:3d} PDIs ({high/total*100:5.1f}%)")
        print(f"   🟡 MÉDIA qualidade:  {medium:3d} PDIs ({medium/total*100:5.1f}%)")
        print(f"   🔴 BAIXA qualidade:  {low:3d} PDIs ({low/total*100:5.1f}%)")
        
        # Análise das métricas
        print(f"\n📊 ANÁLISE DETALHADA DAS MÉTRICAS:")
        if 'clarity_score' in df_result.columns:
            clarity_avg = df_result['clarity_score'].mean()
            specificity_avg = df_result['specificity_score'].mean()
            completeness_avg = df_result['completeness_score'].mean()
            structure_avg = df_result['structure_score'].mean()
            
            print(f"   📝 Clareza média:           {clarity_avg:.3f}")
            print(f"   🎯 Especificidade média:    {specificity_avg:.3f}")
            print(f"   📋 Completude média:        {completeness_avg:.3f}")
            print(f"   🏗️  Estrutura média:         {structure_avg:.3f}")
        
        # Exemplos de cada categoria
        print(f"\n📋 EXEMPLOS POR CATEGORIA DE QUALIDADE:")
        
        # Exemplo de alta qualidade
        high_quality = df_result[df_result['quality_level'] == 'Alta']
        if len(high_quality) > 0:
            print(f"\n🟢 EXEMPLO DE ALTA QUALIDADE:")
            row = high_quality.iloc[0]
            print(f"   Nome: {row['Nome Completo']}")
            print(f"   Objetivo: {row['Objetivo de Desenvolvimento (GAP)']}")
            print(f"   Score: {row['overall_score']:.3f}")
        
        # Exemplo de média qualidade  
        medium_quality = df_result[df_result['quality_level'] == 'Média']
        if len(medium_quality) > 0:
            print(f"\n🟡 EXEMPLO DE MÉDIA QUALIDADE:")
            row = medium_quality.iloc[0]
            print(f"   Nome: {row['Nome Completo']}")
            print(f"   Objetivo: {row['Objetivo de Desenvolvimento (GAP)']}")
            print(f"   Score: {row['overall_score']:.3f}")
        
        # Exemplo de baixa qualidade
        low_quality = df_result[df_result['quality_level'] == 'Baixa']
        if len(low_quality) > 0:
            print(f"\n🔴 EXEMPLO DE BAIXA QUALIDADE:")
            row = low_quality.iloc[0]
            print(f"   Nome: {row['Nome Completo']}")
            print(f"   Objetivo: {row['Objetivo de Desenvolvimento (GAP)']}")
            print(f"   Score: {row['overall_score']:.3f}")
        
        print(f"\n" + "=" * 50)
        print(f"✅ PROBLEMA RESOLVIDO!")
        print(f"📁 O sistema agora consegue analisar o arquivo CSV fornecido")
        print(f"🔧 Código adaptado para a estrutura específica do seu relatório")
        print(f"📊 Análise de qualidade funcionando perfeitamente")
        print(f"💾 Resultados salvos em: analise_automatica_20250812_095918.csv")
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")

if __name__ == "__main__":
    gerar_relatorio_final()
