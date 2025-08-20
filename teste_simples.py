#!/usr/bin/env python3

try:
    from quality_filter_pdi import QualityFilterPDI
    analyzer = QualityFilterPDI()
    result = analyzer.analyze_single_pdi('Aprender Python', 'Fazer curso online')
    print('SUCCESS: Análise única funcionou')
    print(f'Score: {result.get("overall_score", "N/A")}')
    print(f'Colunas: {list(result.keys())}')
    if "smart_criteria_score" in result:
        print('ERRO: smart_criteria_score ainda presente')
    else:
        print('SUCCESS: smart_criteria_score removido')
except Exception as e:
    print(f'ERRO: {e}')
    import traceback
    traceback.print_exc()
