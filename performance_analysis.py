#!/usr/bin/env python3
"""
Análise de Performance - Quality Filter PDI
"""

import time
import sys
import os
import tracemalloc
import pandas as pd

# Adicionar o caminho do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from quality_filter_pdi.services.quality_metrics_service import QualityMetricsService
from quality_filter_pdi.services.pdi_analysis_service import PDIAnalysisService
from quality_filter_pdi import QualityFilterPDI

def benchmark_metrics():
    """Benchmark dos métodos de cálculo de métricas"""
    print("🔍 ANÁLISE DE PERFORMANCE - MÉTRICAS")
    print("=" * 50)
    
    service = QualityMetricsService()
    texto = "Aprender Python para desenvolvimento web através de curso online e projeto prático com framework Django"
    
    # Teste de clarity
    start = time.time()
    for _ in range(1000):
        service.calculate_clarity(texto)
    clarity_time = (time.time() - start) * 1000
    
    # Teste de specificity
    start = time.time()
    for _ in range(1000):
        service.calculate_specificity(texto)
    specificity_time = (time.time() - start) * 1000
    
    # Teste de completeness
    start = time.time()
    for _ in range(1000):
        service.calculate_completeness(texto)
    completeness_time = (time.time() - start) * 1000
    
    # Teste de structure
    start = time.time()
    for _ in range(1000):
        service.calculate_structure(texto)
    structure_time = (time.time() - start) * 1000
    
    print(f"📝 Clarity (1000x):      {clarity_time:.2f}ms")
    print(f"🎯 Specificity (1000x):  {specificity_time:.2f}ms")
    print(f"📋 Completeness (1000x): {completeness_time:.2f}ms")
    print(f"🏗️ Structure (1000x):     {structure_time:.2f}ms")
    print(f"⭐ Total por PDI:        {(clarity_time + specificity_time + completeness_time + structure_time)/1000:.2f}ms")

def benchmark_full_analysis():
    """Benchmark da análise completa"""
    print("\n🔍 ANÁLISE DE PERFORMANCE - PDI COMPLETO")
    print("=" * 50)
    
    analyzer = QualityFilterPDI()
    
    objetivo = "Aprender Python para desenvolvimento web"
    acoes = "Fazer curso online de Django, criar projeto portfolio, estudar 2h por dia"
    
    # Análise única
    start = time.time()
    for _ in range(100):
        analyzer.analyze_single_pdi(objetivo, acoes)
    single_time = (time.time() - start) * 1000
    
    print(f"📊 Análise PDI única (100x): {single_time:.2f}ms")
    print(f"📊 Tempo por PDI:           {single_time/100:.2f}ms")

def benchmark_batch_processing():
    """Benchmark de processamento em lote"""
    print("\n🔍 ANÁLISE DE PERFORMANCE - LOTE")
    print("=" * 50)
    
    # Criar dados de teste
    test_data = []
    for i in range(500):
        test_data.append({
            'objetivo': f"Objetivo de teste {i+1} para análise de performance",
            'acoes': f"Ações específicas {i+1} com detalhamento completo"
        })
    
    df = pd.DataFrame(test_data)
    
    analyzer = QualityFilterPDI()
    
    # Análise em lote
    start = time.time()
    result = analyzer.analyze_pdis_from_dataframe(df.head(100))  # 100 PDIs
    batch_time = time.time() - start
    
    print(f"📦 Lote 100 PDIs:     {batch_time:.2f}s")
    print(f"📦 Tempo por PDI:     {batch_time/100*1000:.2f}ms")
    print(f"📦 PDIs por segundo:  {100/batch_time:.1f}")

def memory_analysis():
    """Análise de uso de memória"""
    print("\n🧠 ANÁLISE DE MEMÓRIA")
    print("=" * 50)
    
    tracemalloc.start()
    
    analyzer = QualityFilterPDI()
    
    # Snapshot inicial
    snapshot1 = tracemalloc.take_snapshot()
    
    # Processar dados
    for i in range(100):
        analyzer.analyze_single_pdi(
            f"Objetivo teste {i}",
            f"Ações teste {i}"
        )
    
    # Snapshot final
    snapshot2 = tracemalloc.take_snapshot()
    
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print("🔝 Top 3 diferenças de memória:")
    for stat in top_stats[:3]:
        print(f"   {stat}")
    
    tracemalloc.stop()

def identify_bottlenecks():
    """Identificar gargalos de performance"""
    print("\n🚨 IDENTIFICAÇÃO DE GARGALOS")
    print("=" * 50)
    
    analyzer = QualityFilterPDI()
    
    texto_curto = "Aprender Python"
    texto_medio = "Aprender Python para desenvolvimento web através de curso online"
    texto_longo = "Aprender Python para desenvolvimento web através de curso online com framework Django, criando aplicações completas, estudando banco de dados PostgreSQL, implementando APIs REST, trabalhando com autenticação e autorização, deployment em servidores cloud"
    
    for nome, texto in [("Curto", texto_curto), ("Médio", texto_medio), ("Longo", texto_longo)]:
        start = time.time()
        for _ in range(100):
            analyzer.analyze_single_pdi(texto, "Ações correspondentes")
        tempo = (time.time() - start) * 1000
        print(f"📏 Texto {nome:6}: {tempo/100:.2f}ms por PDI")

def suggest_optimizations():
    """Sugerir otimizações"""
    print("\n🚀 SUGESTÕES DE OTIMIZAÇÃO")
    print("=" * 50)
    
    suggestions = [
        "1. 📦 CACHE: Implementar cache em memória para textos repetidos",
        "2. 🔄 LAZY LOADING: Carregar módulos AI apenas quando necessário",
        "3. ⚡ VECTORIZAÇÃO: Usar NumPy para cálculos matemáticos",
        "4. 🧵 MULTIPROCESSING: Processamento paralelo para lotes grandes",
        "5. 📊 PROFILING: Usar cProfile para identificar hotspots específicos",
        "6. 🗄️ BATCH PROCESSING: Processar em chunks menores para economia de memória",
        "7. 🔧 OTIMIZAÇÃO DE REGEX: Compilar regex uma vez e reutilizar",
        "8. 📝 TEXT PREPROCESSING: Cache de tokenização e normalização",
        "9. 🎯 EARLY TERMINATION: Parar cálculos quando resultado é óbvio",
        "10. 💾 MEMORIA: Usar __slots__ em classes para reduzir overhead"
    ]
    
    for suggestion in suggestions:
        print(f"   {suggestion}")

if __name__ == "__main__":
    print("🔍 ANÁLISE DE PERFORMANCE - QUALITY FILTER PDI")
    print("=" * 60)
    
    try:
        benchmark_metrics()
        benchmark_full_analysis()
        benchmark_batch_processing()
        memory_analysis()
        identify_bottlenecks()
        suggest_optimizations()
        
        print("\n✅ ANÁLISE CONCLUÍDA!")
        print("📊 Veja os resultados acima para identificar oportunidades de otimização.")
        
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        import traceback
        traceback.print_exc()
