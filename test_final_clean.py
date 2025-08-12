from app import PDIAnalyzer

analyzer = PDIAnalyzer()
result = analyzer.analyze_text('Desenvolver Python', 'Fazer curso 40h')
print(f'Score: {result["overall_score"]:.2f} - Nivel: {result["quality_level"]}')
print("✅ Sistema funcionando após remoção de comentários!")
