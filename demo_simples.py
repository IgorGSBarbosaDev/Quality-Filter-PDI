"""
Demonstração simples do sistema de análise de PDI
"""

def analyze_pdi_simple(acoes, objetivo):
    """
    Análise simplificada de PDI sem dependências externas
    """
    # Análise básica de qualidade
    score = 0.0
    suggestions = []
    
    # Verifica comprimento
    acoes_words = len(acoes.split()) if acoes else 0
    objetivo_words = len(objetivo.split()) if objetivo else 0
    
    if acoes_words >= 10:
        score += 0.2
    else:
        suggestions.append("• Expanda as ações planejadas (mínimo 10 palavras)")
    
    if objetivo_words >= 10:
        score += 0.2
    else:
        suggestions.append("• Expanda o objetivo de desenvolvimento (mínimo 10 palavras)")
    
    # Verifica especificidade (números, datas)
    import re
    if re.search(r'\d+', acoes + " " + objetivo):
        score += 0.2
    else:
        suggestions.append("• Inclua números específicos (prazos, quantidades, metas)")
    
    # Verifica palavras-chave de qualidade
    quality_words = ['implementar', 'desenvolver', 'concluir', 'atingir', 'realizar']
    if any(word in (acoes + " " + objetivo).lower() for word in quality_words):
        score += 0.2
    else:
        suggestions.append("• Use verbos de ação mais específicos")
    
    # Verifica palavras que indicam baixa qualidade
    negative_words = ['talvez', 'acho que', 'tentar', 'espero']
    if any(word in (acoes + " " + objetivo).lower() for word in negative_words):
        score -= 0.1
        suggestions.append("• Evite linguagem incerta - seja mais assertivo")
    else:
        score += 0.2
    
    # Determina nível
    if score >= 0.8:
        level = "Alto"
    elif score >= 0.6:
        level = "Médio"
    else:
        level = "Baixo"
    
    if not suggestions:
        suggestions.append("• PDI de boa qualidade!")
    
    return {
        'level': level,
        'score': round(score, 2),
        'suggestions': " ".join(suggestions)
    }

def main():
    print("Sistema Simplificado de Análise de PDI")
    print("=" * 40)
    
    # Exemplos de PDI
    exemplos = [
        {
            'nome': 'João Silva',
            'acoes': 'Realizar curso de Excel avançado com duração de 40 horas até dezembro de 2024. Praticar relatórios gerenciais semanalmente.',
            'objetivo': 'Tornar-me especialista em análise financeira avançada até dezembro de 2024.'
        },
        {
            'nome': 'Maria Santos',
            'acoes': 'Fazer alguns cursos de liderança.',
            'objetivo': 'Desenvolver habilidades de liderança.'
        },
        {
            'nome': 'Carlos Oliveira',
            'acoes': 'Melhorar habilidades.',
            'objetivo': 'Crescer profissionalmente.'
        }
    ]
    
    for exemplo in exemplos:
        print(f"\nFuncionário: {exemplo['nome']}")
        print(f"Ações: {exemplo['acoes']}")
        print(f"Objetivo: {exemplo['objetivo']}")
        
        resultado = analyze_pdi_simple(exemplo['acoes'], exemplo['objetivo'])
        
        print(f"Nível de Qualidade: {resultado['level']}")
        print(f"Pontuação: {resultado['score']}")
        print(f"Sugestões: {resultado['suggestions']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
