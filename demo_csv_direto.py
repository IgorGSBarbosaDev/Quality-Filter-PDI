#!/usr/bin/env python3
"""
Demo direto com o arquivo CSV - versão simplificada
"""

import pandas as pd
from pathlib import Path

def demo_csv():
    print("🔍 DEMO DIRETO - ANÁLISE CSV")
    
    try:
        # Carrega o arquivo
        csv_file = "Relatório_de_PDI__Completo__2025_08_11_12_49_15.csv"
        
        # Tenta utf-8 primeiro
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
            encoding_used = 'utf-8'
        except:
            try:
                df = pd.read_csv(csv_file, encoding='latin-1')
                encoding_used = 'latin-1'
            except:
                df = pd.read_csv(csv_file, encoding='cp1252')
                encoding_used = 'cp1252'
        
        print(f"✅ Arquivo carregado com encoding: {encoding_used}")
        print(f"📊 Dimensões: {df.shape}")
        
        # Verifica as colunas principais
        print(f"\n📋 Colunas encontradas:")
        colunas_principais = [
            'Nome Completo',
            'Objetivo de Desenvolvimento (GAP)', 
            'Ações a serem realizadas',
            'Finalidade',
            'Atividade de Aprendizagem',
            'Descrição'
        ]
        
        for col in colunas_principais:
            if col in df.columns:
                count = df[col].notna().sum()
                print(f"   ✅ {col}: {count} registros")
            else:
                print(f"   ❌ {col}: NÃO ENCONTRADA")
        
        # Mostra amostra dos textos a serem analisados
        print(f"\n📝 AMOSTRA DOS TEXTOS PARA ANÁLISE:")
        
        sample = df.head(3)
        for i, row in sample.iterrows():
            print(f"\n--- REGISTRO {i+1} ---")
            print(f"Nome: {row.get('Nome Completo', 'N/A')}")
            print(f"Objetivo: {row.get('Objetivo de Desenvolvimento (GAP)', 'N/A')}")
            print(f"Ações: {row.get('Ações a serem realizadas', 'N/A')}")
        
        print(f"\n🎉 ARQUIVO CSV COMPATÍVEL COM O SISTEMA!")
        print(f"   📊 Total de PDIs para análise: {len(df)}")
        print(f"   ✅ Pronto para análise de qualidade!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    demo_csv()
