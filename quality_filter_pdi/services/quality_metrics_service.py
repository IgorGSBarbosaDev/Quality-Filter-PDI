from typing import Dict, List
from ..core.config import SMART_KEYWORDS, POSITIVE_INDICATORS, NEGATIVE_INDICATORS
from ..utils.text_utils import TextUtils


class QualityMetricsService:
    
    def __init__(self):
        self.smart_keywords = SMART_KEYWORDS
        self.positive_indicators = POSITIVE_INDICATORS
        self.negative_indicators = NEGATIVE_INDICATORS
    
    def calculate_clarity(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            words = TextUtils.tokenize(text)
            sentences = TextUtils.count_sentences(text)
            
            if not words or sentences == 0:
                return 0.0
            
            avg_word_length = TextUtils.calculate_avg_word_length(text)
            words_per_sentence = len(words) / sentences
            
            if len(words) < 3:
                return 0.2
            elif len(words) > 50:
                clarity_score = max(0.3, 1.0 - (words_per_sentence - 10) * 0.02)
            else:
                clarity_score = min(1.0, 0.5 + (len(words) * 0.05))
            
            if avg_word_length > 8:
                clarity_score *= 0.8
            
            if TextUtils.has_proper_case(text):
                clarity_score *= 1.1
            
            if TextUtils.has_punctuation(text):
                clarity_score *= 1.05
            
            return min(1.0, clarity_score)
            
        except Exception:
            return 0.0
    
    def calculate_specificity(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            specificity_score = 0.1
            
            if TextUtils.has_numbers(text):
                specificity_score += 0.3
                number_count = TextUtils.count_numbers(text)
                specificity_score += min(0.2, number_count * 0.05)
            
            technical_terms = TextUtils.extract_technical_terms(text)
            if technical_terms:
                specificity_score += min(0.3, len(technical_terms) * 0.1)
            
            keywords = ['específico', 'detalhado', 'preciso', 'exato', 'claro']
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    specificity_score += 0.1
            
            return min(1.0, specificity_score)
            
        except Exception:
            return 0.0
    
    def calculate_completeness(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            word_count = TextUtils.count_words(text)
            sentence_count = TextUtils.count_sentences(text)
            
            if word_count < 5:
                return 0.1
            
            completeness_score = min(0.6, word_count * 0.02)
            
            completeness_score += min(0.2, sentence_count * 0.05)
            
            important_elements = ['quando', 'como', 'onde', 'o que', 'por que', 'quem']
            for element in important_elements:
                if element.lower() in text.lower():
                    completeness_score += 0.05
            
            if len(text) > 100:
                completeness_score += 0.1
            
            return min(1.0, completeness_score)
            
        except Exception:
            return 0.0
    
    def calculate_structure(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            structure_score = 0.2
            
            connectors = ['e', 'mas', 'porém', 'então', 'assim', 'portanto', 'além disso']
            for connector in connectors:
                if connector.lower() in text.lower():
                    structure_score += 0.1
            
            if TextUtils.has_proper_case(text):
                structure_score += 0.2
            
            if TextUtils.has_punctuation(text):
                structure_score += 0.2
            
            sentences = TextUtils.count_sentences(text)
            if sentences > 1:
                structure_score += min(0.3, sentences * 0.1)
            
            return min(1.0, structure_score)
            
        except Exception:
            return 0.0
    
    def calculate_smart_criteria(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            smart_score = 0.0
            text_lower = text.lower()
            
            for category, keywords in self.smart_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        smart_score += 0.15
                        break
            
            return min(1.0, smart_score)
            
        except Exception:
            return 0.0
    
    def calculate_negative_impact(self, text: str) -> float:
        if not TextUtils.validate_text_quality(text):
            return 0.0
        
        try:
            negative_score = 0.0
            text_lower = text.lower()
            
            for indicator in self.negative_indicators:
                if indicator.lower() in text_lower:
                    negative_score += 0.1
            
            return min(0.5, negative_score)
            
        except Exception:
            return 0.0
    
    def calculate_overall_quality(self, clarity: float, specificity: float, 
                                completeness: float, structure: float, 
                                smart_criteria: float = 0.0) -> Dict[str, float]:
        """
        Calcula a qualidade geral do PDI com base nos critérios principais.
        
        NOTA: O parâmetro smart_criteria é mantido para compatibilidade, 
        mas não é mais usado no cálculo (peso = 0.0).
        Análise mostrou que remover SMART melhora as notas em 100% dos casos.
        """
        weights = {
            'clarity': 0.278,       # 27.8% (anteriormente 25.0%)
            'specificity': 0.278,   # 27.8% (anteriormente 25.0%)
            'completeness': 0.278,  # 27.8% (anteriormente 25.0%)
            'structure': 0.167,     # 16.7% (anteriormente 15.0%)
            'smart_criteria': 0.0   # 0.0% (anteriormente 10.0%) - REMOVIDO
        }
        
        overall_score = (
            clarity * weights['clarity'] +
            specificity * weights['specificity'] +
            completeness * weights['completeness'] +
            structure * weights['structure']
            # smart_criteria removido do cálculo
        )
        
        if overall_score >= 0.6:
            quality_level = 'Alta'
        elif overall_score >= 0.3:
            quality_level = 'Média'
        else:
            quality_level = 'Baixa'
        
        return {
            'overall_score': overall_score,
            'quality_level': quality_level,
            'clarity_score': clarity,
            'specificity_score': specificity,
            'completeness_score': completeness,
            'structure_score': structure,
            'smart_criteria_score': smart_criteria  # Mantido para compatibilidade
        }
    
    def generate_score_explanation(self, clarity: float, specificity: float, 
                                 completeness: float, structure: float, 
                                 smart_criteria: float, negative_impact: float = 0.0) -> str:
        """
        Gera uma explicação detalhada de como a nota foi calculada
        NOTA: smart_criteria é mantido para compatibilidade mas tem peso 0
        """
        weights = {
            'clarity': 0.278,       # 27.8% (rebalanceado)
            'specificity': 0.278,   # 27.8% (rebalanceado)
            'completeness': 0.278,  # 27.8% (rebalanceado)
            'structure': 0.167,     # 16.7% (rebalanceado)
            'smart_criteria': 0.0   # 0.0% (removido)
        }
        
        # Calcular contribuições de cada critério
        contributions = {
            'Clareza': clarity * weights['clarity'] * 100,
            'Especificidade': specificity * weights['specificity'] * 100,
            'Completude': completeness * weights['completeness'] * 100,
            'Estrutura': structure * weights['structure'] * 100
            # SMART removido do cálculo
        }
        
        total_score = sum(contributions.values())
        
        # Ajustar por impacto negativo
        if negative_impact > 0:
            penalty = negative_impact * 10
            total_score = max(0, total_score - penalty)
        
        explanation = f"\n{'='*60}\n"
        explanation += "📊 DETALHAMENTO DA AVALIAÇÃO\n"
        explanation += f"{'='*60}\n\n"
        
        explanation += f"🎯 NOTA FINAL: {total_score:.1f}/100\n\n"
        
        explanation += "📋 BREAKDOWN POR CRITÉRIO:\n"
        explanation += "-" * 40 + "\n"
        
        for criterion, score in contributions.items():
            weight_pct = {
                'Clareza': 27.8,
                'Especificidade': 27.8, 
                'Completude': 27.8,
                'Estrutura': 16.7
                # SMART removido (era 10%)
            }[criterion]
            
            raw_score = score / weight_pct * 100
            
            explanation += f"• {criterion:15} ({weight_pct:4.1f}%): {score:5.1f} pontos "
            explanation += f"(base: {raw_score:.1f}/100)\n"
        
        if negative_impact > 0:
            explanation += f"\n⚠️  PENALIDADES:\n"
            explanation += f"• Indicadores negativos: -{negative_impact * 10:.1f} pontos\n"
        
        explanation += f"\n🔍 ANÁLISE DETALHADA:\n"
        explanation += "-" * 40 + "\n"
        
        # Análise por critério
        if clarity >= 0.8:
            explanation += "✅ CLAREZA (EXCELENTE): Texto muito claro e compreensível\n"
        elif clarity >= 0.6:
            explanation += "✅ CLAREZA (BOA): Texto claro com pequenos ajustes possíveis\n"
        elif clarity >= 0.4:
            explanation += "⚠️  CLAREZA (REGULAR): Texto necessita melhorar clareza\n"
        else:
            explanation += "❌ CLAREZA (BAIXA): Texto confuso, necessita reescrita\n"
        
        if specificity >= 0.8:
            explanation += "✅ ESPECIFICIDADE (EXCELENTE): Muito específico e detalhado\n"
        elif specificity >= 0.6:
            explanation += "✅ ESPECIFICIDADE (BOA): Razoavelmente específico\n"
        elif specificity >= 0.4:
            explanation += "⚠️  ESPECIFICIDADE (REGULAR): Falta mais detalhes específicos\n"
        else:
            explanation += "❌ ESPECIFICIDADE (BAIXA): Muito vago, adicionar detalhes\n"
        
        if completeness >= 0.8:
            explanation += "✅ COMPLETUDE (EXCELENTE): Informações muito completas\n"
        elif completeness >= 0.6:
            explanation += "✅ COMPLETUDE (BOA): Informações adequadas\n"
        elif completeness >= 0.4:
            explanation += "⚠️  COMPLETUDE (REGULAR): Faltam algumas informações\n"
        else:
            explanation += "❌ COMPLETUDE (BAIXA): Informações insuficientes\n"
        
        if structure >= 0.8:
            explanation += "✅ ESTRUTURA (EXCELENTE): Muito bem estruturado\n"
        elif structure >= 0.6:
            explanation += "✅ ESTRUTURA (BOA): Bem estruturado\n"
        elif structure >= 0.4:
            explanation += "⚠️  ESTRUTURA (REGULAR): Estrutura pode melhorar\n"
        else:
            explanation += "❌ ESTRUTURA (BAIXA): Estrutura inadequada\n"
        
        # SMART removido das explicações - não é mais usado no cálculo
        
        explanation += f"\n🎯 CLASSIFICAÇÃO GERAL:\n"
        if total_score >= 80:
            explanation += "🌟 EXCELENTE - PDI de alta qualidade\n"
        elif total_score >= 60:
            explanation += "✅ BOM - PDI de boa qualidade\n"
        elif total_score >= 40:
            explanation += "⚠️  REGULAR - PDI necessita melhorias\n"
        else:
            explanation += "❌ INADEQUADO - PDI necessita reescrita\n"
        
        explanation += f"\n{'='*60}\n"
        
        return explanation
    
    def generate_feedback_for_responsible(self, clarity: float, specificity: float, 
                                        completeness: float, structure: float, 
                                        smart_criteria: float, negative_impact: float = 0.0,
                                        overall_score: float = 0.0) -> str:
        """
        Gera feedback específico e direto para o responsável pelo PDI
        explicando o motivo da nota recebida
        NOTA: smart_criteria é mantido para compatibilidade mas tem peso 0
        """
        # Calcular nota final se não fornecida
        if overall_score == 0.0:
            weights = {
                'clarity': 0.278,       # 27.8% (rebalanceado)
                'specificity': 0.278,   # 27.8% (rebalanceado)
                'completeness': 0.278,  # 27.8% (rebalanceado)
                'structure': 0.167,     # 16.7% (rebalanceado)
                'smart_criteria': 0.0   # 0.0% (removido)
            }
            
            overall_score = (
                clarity * weights['clarity'] +
                specificity * weights['specificity'] +
                completeness * weights['completeness'] +
                structure * weights['structure']
                # smart_criteria removido do cálculo
            ) * 100
            
            if negative_impact > 0:
                overall_score = max(0, overall_score - (negative_impact * 10))
        
        # Determinar nível da nota
        if overall_score >= 80:
            nivel = "EXCELENTE"
            emoji = "🌟"
        elif overall_score >= 60:
            nivel = "BOM"
            emoji = "✅"
        elif overall_score >= 40:
            nivel = "REGULAR"
            emoji = "⚠️"
        else:
            nivel = "INADEQUADO"
            emoji = "❌"
        
        feedback = f"{emoji} FEEDBACK PARA O SEU PDI - NOTA: {overall_score:.1f}/100 ({nivel})\n\n"
        
        # Explicação principal baseada na nota
        if overall_score >= 80:
            feedback += "🎉 PARABÉNS! Seu PDI está excelente!\n"
            feedback += "Seu objetivo está muito bem definido e suas ações são claras e específicas. "
            feedback += "Continue mantendo este padrão de qualidade.\n\n"
        elif overall_score >= 60:
            feedback += "👍 Bom trabalho! Seu PDI está bem estruturado.\n"
            feedback += "Há alguns pontos que podem ser melhorados para torná-lo ainda mais efetivo.\n\n"
        elif overall_score >= 40:
            feedback += "📝 Seu PDI precisa de algumas melhorias importantes.\n"
            feedback += "Com os ajustes sugeridos abaixo, você pode torná-lo muito mais efetivo.\n\n"
        else:
            feedback += "🔄 Seu PDI necessita ser reformulado.\n"
            feedback += "Não se preocupe! Com as orientações abaixo, você pode criar um PDI de alta qualidade.\n\n"
        
        # Feedback específico por critério com ações práticas
        feedback += "💡 PRINCIPAIS MOTIVOS DA SUA NOTA:\n\n"
        
        # Clareza
        if clarity < 0.4:
            feedback += "🔍 CLAREZA - Precisa melhorar:\n"
            feedback += "• Seu objetivo não está claro o suficiente\n"
            feedback += "• Reescreva usando palavras mais simples e diretas\n"
            feedback += "• Evite termos vagos como 'melhorar', 'desenvolver' sem especificar o quê\n\n"
        elif clarity < 0.7:
            feedback += "🔍 CLAREZA - Pode melhorar:\n"
            feedback += "• Seu objetivo está razoavelmente claro, mas pode ser mais direto\n"
            feedback += "• Tente ser mais específico sobre o que exatamente quer alcançar\n\n"
        else:
            feedback += "🔍 CLAREZA - Muito bom! ✅\n"
            feedback += "• Seu objetivo está claro e fácil de entender\n\n"
        
        # Especificidade
        if specificity < 0.4:
            feedback += "🎯 ESPECIFICIDADE - Precisa melhorar:\n"
            feedback += "• Faltam detalhes importantes no seu PDI\n"
            feedback += "• Adicione números, prazos, nomes de cursos, certificações específicas\n"
            feedback += "• Exemplo: Em vez de 'fazer curso', diga 'Curso X de 40 horas na plataforma Y'\n\n"
        elif specificity < 0.7:
            feedback += "🎯 ESPECIFICIDADE - Pode melhorar:\n"
            feedback += "• Você tem alguns detalhes, mas pode ser mais específico\n"
            feedback += "• Adicione mais informações sobre prazos, quantidades e recursos\n\n"
        else:
            feedback += "🎯 ESPECIFICIDADE - Excelente! ✅\n"
            feedback += "• Seu PDI tem detalhes específicos e mensuráveis\n\n"
        
        # Completude
        if completeness < 0.4:
            feedback += "📋 COMPLETUDE - Precisa melhorar:\n"
            feedback += "• Seu PDI está muito resumido e faltam informações\n"
            feedback += "• Explique melhor COMO vai alcançar seu objetivo\n"
            feedback += "• Detalhe mais suas ações e inclua cronograma\n\n"
        elif completeness < 0.7:
            feedback += "📋 COMPLETUDE - Pode melhorar:\n"
            feedback += "• Você tem as informações básicas, mas pode expandir\n"
            feedback += "• Adicione mais detalhes sobre o processo de execução\n\n"
        else:
            feedback += "📋 COMPLETUDE - Muito completo! ✅\n"
            feedback += "• Seu PDI tem todas as informações necessárias\n\n"
        
        # Estrutura
        if structure < 0.4:
            feedback += "🏗️ ESTRUTURA - Precisa melhorar:\n"
            feedback += "• Organize melhor suas ideias\n"
            feedback += "• Use pontuação e separe as informações em tópicos\n"
            feedback += "• Conecte melhor objetivo e ações\n\n"
        elif structure < 0.7:
            feedback += "🏗️ ESTRUTURA - Pode melhorar:\n"
            feedback += "• Sua estrutura está boa, mas pode ser mais organizada\n"
            feedback += "• Use conectores para ligar melhor as ideias\n\n"
        else:
            feedback += "🏗️ ESTRUTURA - Bem organizado! ✅\n"
            feedback += "• Seu PDI está bem estruturado e fácil de seguir\n\n"
        
        # Critérios SMART
        if smart_criteria < 0.4:
            feedback += "📊 CRITÉRIOS SMART - Precisa melhorar:\n"
            feedback += "• Seu objetivo não atende aos critérios SMART\n"
            feedback += "• Torne-o mais Específico, Mensurável, Atingível, Relevante e com Tempo definido\n"
            feedback += "• Exemplo: 'Obter certificação X até dezembro com nota mínima Y'\n\n"
        elif smart_criteria < 0.7:
            feedback += "📊 CRITÉRIOS SMART - Pode melhorar:\n"
            feedback += "• Seu objetivo atende parcialmente aos critérios SMART\n"
            feedback += "• Adicione mais elementos como prazos específicos e métricas\n\n"
        else:
            feedback += "📊 CRITÉRIOS SMART - Excelente! ✅\n"
            feedback += "• Seu objetivo atende muito bem aos critérios SMART\n\n"
        
        # Penalidades
        if negative_impact > 0:
            feedback += "⚠️ PONTOS DE ATENÇÃO:\n"
            feedback += f"• Foram identificados alguns indicadores negativos que reduziram sua nota em {negative_impact * 10:.1f} pontos\n"
            feedback += "• Revise termos muito vagos ou negativos no seu PDI\n\n"
        
        # Próximos passos
        feedback += "🚀 PRÓXIMOS PASSOS PARA MELHORAR:\n"
        
        if overall_score < 40:
            feedback += "1. Reescreva seu objetivo de forma mais clara e específica\n"
            feedback += "2. Adicione prazos definidos e métricas mensuráveis\n"
            feedback += "3. Detalhe melhor suas ações com recursos e cronograma\n"
            feedback += "4. Organize as informações de forma mais estruturada\n"
        elif overall_score < 60:
            feedback += "1. Adicione mais detalhes específicos (números, datas, nomes)\n"
            feedback += "2. Melhore a conexão entre objetivo e ações\n"
            feedback += "3. Inclua métricas para medir seu progresso\n"
        elif overall_score < 80:
            feedback += "1. Faça pequenos ajustes para tornar ainda mais específico\n"
            feedback += "2. Revise se todas as informações estão completas\n"
            feedback += "3. Verifique se atende totalmente aos critérios SMART\n"
        else:
            feedback += "1. Continue mantendo este excelente padrão\n"
            feedback += "2. Use seu PDI como exemplo para futuros objetivos\n"
            feedback += "3. Acompanhe regularmente seu progresso\n"
        
        return feedback
    
    def generate_concise_reasons(self, clarity: float, specificity: float, 
                                completeness: float, structure: float, 
                                smart_criteria: float, negative_impact: float = 0.0,
                                overall_score: float = 0.0) -> dict:
        """
        Gera 3 motivos concisos e diretos para a nota recebida
        Sem emojis, sem textos longos - apenas os pontos principais
        NOTA: smart_criteria é mantido para compatibilidade mas tem peso 0
        """
        # Calcular nota final se não fornecida
        if overall_score == 0.0:
            weights = {
                'clarity': 0.278,       # 27.8% (rebalanceado)
                'specificity': 0.278,   # 27.8% (rebalanceado)
                'completeness': 0.278,  # 27.8% (rebalanceado)
                'structure': 0.167,     # 16.7% (rebalanceado)
                'smart_criteria': 0.0   # 0.0% (removido)
            }
            
            overall_score = (
                clarity * weights['clarity'] +
                specificity * weights['specificity'] +
                completeness * weights['completeness'] +
                structure * weights['structure']
                # smart_criteria removido do cálculo
            ) * 100
            
            if negative_impact > 0:
                overall_score = max(0, overall_score - (negative_impact * 10))
        
        # Identificar os 3 principais problemas/pontos fortes
        # SMART removido da análise
        criteria_scores = {
            'clareza': clarity,
            'especificidade': specificity,
            'completude': completeness,
            'estrutura': structure
        }
        
        # Ordenar critérios por pontuação (do menor para o maior)
        sorted_criteria = sorted(criteria_scores.items(), key=lambda x: x[1])
        
        motivos = []
        
        # Analisar os 3 critérios com menor pontuação para identificar problemas
        for criterio, score in sorted_criteria[:3]:
            if criterio == 'clareza':
                if score < 0.4:
                    motivos.append("Objetivo muito vago e confuso")
                elif score < 0.7:
                    motivos.append("Objetivo precisa ser mais claro")
                else:
                    motivos.append("Clareza adequada")
            
            elif criterio == 'especificidade':
                if score < 0.4:
                    motivos.append("Faltam detalhes específicos e números")
                elif score < 0.7:
                    motivos.append("Precisa mais detalhes específicos")
                else:
                    motivos.append("Especificidade adequada")
            
            elif criterio == 'completude':
                if score < 0.4:
                    motivos.append("Informações muito incompletas")
                elif score < 0.7:
                    motivos.append("Faltam informações importantes")
                else:
                    motivos.append("Informações suficientes")
            
            elif criterio == 'estrutura':
                if score < 0.4:
                    motivos.append("Texto mal organizado")
                elif score < 0.7:
                    motivos.append("Estrutura pode melhorar")
                else:
                    motivos.append("Bem estruturado")
        
        # Se a nota é muito baixa, focar nos problemas mais críticos
        if overall_score < 40:
            motivos = [
                "Objetivo extremamente vago",
                "Faltam detalhes essenciais",
                "Não especifica como executar"
            ]
        
        # Se a nota é boa, focar nos pontos de melhoria
        elif overall_score >= 70:
            # Para notas altas, identificar pequenos ajustes
            lowest_criteria = sorted_criteria[0]
            if lowest_criteria[1] < 0.8:  # Se o critério mais baixo ainda pode melhorar
                if lowest_criteria[0] == 'especificidade':
                    motivos[0] = "Pode adicionar mais números e datas"
                elif lowest_criteria[0] == 'completude':
                    motivos[0] = "Pode detalhar mais as ações"
                elif lowest_criteria[0] == 'clareza':
                    motivos[0] = "Pode ser mais direto e claro"
            else:
                motivos[0] = "PDI de boa qualidade geral"
        
        # Considerar impacto negativo
        if negative_impact > 0.1:
            motivos[-1] = "Contém termos negativos ou vagos"
        
        # Garantir que temos exatamente 3 motivos
        while len(motivos) < 3:
            motivos.append("Análise complementar necessária")
        
        # Limitar a 3 motivos
        motivos = motivos[:3]
        
        return {
            'motivo_1': motivos[0],
            'motivo_2': motivos[1],
            'motivo_3': motivos[2]
        }
