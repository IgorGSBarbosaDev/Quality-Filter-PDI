from typing import Dict, List, Tuple, Set
from enum import Enum
import re


class SkillType(Enum):
    HARD_SKILL = "Hard Skill"
    SOFT_SKILL = "Soft Skill"
    HYBRID = "Híbrida"
    UNKNOWN = "Indefinida"


class SkillClassifier:
    
    def __init__(self):
        self.hard_skills_keywords = {
            "excel", "powerbi", "power bi", "tableau", "sql", "python", "java", "javascript",
            "sap", "oracle", "salesforce", "autocad", "photoshop", "illustrator", "figma",
            "contabilidade", "financeiro", "juridico", "engenharia", "medicina", "enfermagem",
            "programacao", "programação", "desenvolvimento", "sistema", "software", "hardware",
            "rede", "servidor", "banco de dados", "algoritmo", "machine learning", "ia",
            "inteligencia artificial", "cloud", "aws", "azure", "google cloud", "docker",
            "kubernetes", "linux", "windows", "macos", "cisco", "microsoft", "adobe",
            "marketing digital", "seo", "sem", "google ads", "facebook ads", "analytics",
            "certificacao", "certificação", "norma", "iso", "pmp", "scrum", "agile",
            "lean", "six sigma", "itil", "cobit", "cisa", "cissp", "pci", "lgpd",
            "legislacao", "legislação", "tributario", "tributário", "trabalhista",
            "idioma", "ingles", "inglês", "espanhol", "frances", "francês", "alemao", "alemão",
            "operacao", "operação", "producao", "produção", "qualidade", "processo",
            "ferramenta", "equipamento", "maquina", "máquina", "tecnico", "técnico",
            "curso", "treinamento", "capacitacao", "capacitação", "workshop"
        }
        
        self.soft_skills_keywords = {
            "lideranca", "liderança", "comunicacao", "comunicação", "trabalho em equipe",
            "colaboracao", "colaboração", "empatia", "inteligencia emocional",
            "inteligência emocional", "criatividade", "inovacao", "inovação",
            "resolucao de problemas", "resolução de problemas", "pensamento critico",
            "pensamento crítico", "adaptabilidade", "flexibilidade", "resiliencia",
            "resiliência", "proatividade", "iniciativa", "autonomia", "responsabilidade",
            "etica", "ética", "honestidade", "integridade", "confianca", "confiança",
            "motivacao", "motivação", "engajamento", "dedicacao", "dedicação",
            "organizacao", "organização", "planejamento", "gestao do tempo",
            "gestão do tempo", "priorização", "foco", "concentracao", "concentração",
            "paciencia", "paciência", "tolerancia", "tolerância", "diplomacia",
            "negociacao", "negociação", "persuasao", "persuasão", "influencia",
            "influência", "carisma", "networking", "relacionamento", "interpessoal",
            "feedback", "escuta ativa", "observacao", "observação", "analise",
            "análise", "síntese", "sintese", "julgamento", "tomada de decisao",
            "tomada de decisão", "visao estrategica", "visão estratégica",
            "orientacao para resultados", "orientação para resultados", "mentoria"
        }
        
        self.technical_patterns = [
            r'\bcertificaç[ãa]o\s+\w+',
            r'\bcurso\s+(?:de|em)\s+\w+',
            r'\bsistema\s+\w+',
            r'\bferramenta\s+\w+',
            r'\bsoftware\s+\w+',
            r'\btecnologia\s+\w+',
            r'\bmódulo\s+\w+',
            r'\bplataforma\s+\w+',
            r'\bidioma\s+\w+',
            r'\bnível\s+(?:básico|intermediário|avançado)',
            r'\b(?:excel|sap|python|java|sql)\b',
            r'\b(?:aws|azure|oracle|salesforce)\b'
        ]
    
    def classify_skill(self, objetivo: str, acoes: str = "") -> Tuple[SkillType, float, Dict]:
        if not objetivo or not objetivo.strip():
            return SkillType.UNKNOWN, 0.0, {}
        
        combined_text = f"{objetivo} {acoes}".lower().strip()
        
        hard_score = self._calculate_hard_skill_score(combined_text)
        soft_score = self._calculate_soft_skill_score(combined_text)
        
        hard_keywords = self._find_keywords(combined_text, self.hard_skills_keywords)
        soft_keywords = self._find_keywords(combined_text, self.soft_skills_keywords)
        technical_patterns = self._find_technical_patterns(combined_text)
        
        details = {
            "hard_score": round(hard_score, 3),
            "soft_score": round(soft_score, 3),
            "hard_keywords_found": hard_keywords,
            "soft_keywords_found": soft_keywords,
            "technical_patterns_found": technical_patterns,
            "analysis_text": combined_text[:100] + "..." if len(combined_text) > 100 else combined_text
        }
        
        if hard_score >= 0.6 and soft_score >= 0.6:
            return SkillType.HYBRID, max(hard_score, soft_score), details
        elif hard_score >= 0.4 and hard_score > soft_score:
            return SkillType.HARD_SKILL, hard_score, details
        elif soft_score >= 0.4 and soft_score > hard_score:
            return SkillType.SOFT_SKILL, soft_score, details
        elif hard_score >= 0.3 or soft_score >= 0.3:
            if hard_score > soft_score:
                return SkillType.HARD_SKILL, hard_score, details
            else:
                return SkillType.SOFT_SKILL, soft_score, details
        else:
            return SkillType.UNKNOWN, max(hard_score, soft_score), details
    
    def _calculate_hard_skill_score(self, text: str) -> float:
        score = 0.0
        
        keyword_matches = sum(1 for keyword in self.hard_skills_keywords if keyword in text)
        if keyword_matches > 0:
            score += min(keyword_matches * 0.25, 0.7)
        
        pattern_matches = sum(1 for pattern in self.technical_patterns 
                            if re.search(pattern, text, re.IGNORECASE))
        if pattern_matches > 0:
            score += min(pattern_matches * 0.3, 0.6)
        
        technical_indicators = [
            "certificaç", "curso", "treinamento", "sistema", "ferramenta",
            "software", "tecnologia", "técnic", "operaç", "process", "módulo",
            "versão", "nível", "proficiência", "dominar", "aplicar"
        ]
        
        indicator_matches = sum(1 for indicator in technical_indicators 
                              if indicator in text)
        if indicator_matches > 0:
            score += min(indicator_matches * 0.15, 0.4)
        
        if re.search(r'\d+\s*(?:horas?|dias?|semanas?)', text):
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_soft_skill_score(self, text: str) -> float:
        score = 0.0
        
        keyword_matches = sum(1 for keyword in self.soft_skills_keywords if keyword in text)
        if keyword_matches > 0:
            score += min(keyword_matches * 0.3, 0.7)
        
        behavioral_indicators = [
            "desenvolv", "melhor", "aprimor", "fortale", "habilidade",
            "competência", "comportament", "atitude", "postura", "relacionament",
            "capacidade", "aptidão", "interpessoal", "social", "emocional"
        ]
        
        indicator_matches = sum(1 for indicator in behavioral_indicators 
                              if indicator in text)
        if indicator_matches > 0:
            score += min(indicator_matches * 0.2, 0.5)
        
        soft_verbs = [
            "comunicar", "liderar", "colaborar", "influenciar", "motivar",
            "inspirar", "orientar", "mentorear", "negociar", "persuadir"
        ]
        
        verb_matches = sum(1 for verb in soft_verbs if verb in text)
        if verb_matches > 0:
            score += min(verb_matches * 0.25, 0.4)
        
        return min(score, 1.0)
    
    def _find_keywords(self, text: str, keywords: Set[str]) -> List[str]:
        found = []
        for keyword in keywords:
            if keyword in text:
                found.append(keyword)
        return found[:5]
    
    def _find_technical_patterns(self, text: str) -> List[str]:
        found = []
        for pattern in self.technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found.extend(matches)
        return found[:3]
    
    def get_skill_recommendations(self, skill_type: SkillType, details: Dict) -> List[str]:
        recommendations = []
        
        if skill_type == SkillType.HARD_SKILL:
            recommendations.extend([
                "✅ Especifique versões de software/ferramentas",
                "✅ Inclua certificações ou níveis de proficiência",
                "✅ Defina métricas mensuráveis de competência",
                "✅ Mencione aplicação prática da habilidade"
            ])
        elif skill_type == SkillType.SOFT_SKILL:
            recommendations.extend([
                "✅ Inclua situações práticas de aplicação",
                "✅ Defina comportamentos observáveis",
                "✅ Estabeleça indicadores de melhoria",
                "✅ Considere feedback 360° como avaliação"
            ])
        elif skill_type == SkillType.HYBRID:
            recommendations.extend([
                "✅ Separe aspectos técnicos dos comportamentais",
                "✅ Defina métricas para cada componente",
                "✅ Planeje desenvolvimento em fases distintas"
            ])
        else:
            recommendations.extend([
                "⚠️ Especifique melhor o tipo de habilidade",
                "⚠️ Inclua mais detalhes sobre o objetivo",
                "⚠️ Defina se é competência técnica ou comportamental"
            ])
        
        return recommendations
