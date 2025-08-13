import json
import re
from typing import Dict, List, Optional
import requests

class CloudAIAnalyzer:
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        self.api_key = api_key
        self.provider = provider
        self.base_urls = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        }
        
        if not api_key:
            print("⚠️ API key não fornecida. Usando análise local.")
            self.use_local = True
        else:
            self.use_local = False
    
    def analyze_pdi_with_ai(self, objetivo: str, acoes: str = "") -> Dict:
        if self.use_local:
            return self._local_analysis(objetivo, acoes)
        
        try:
            if self.provider == "openai":
                return self._openai_analysis(objetivo, acoes)
            elif self.provider == "gemini":
                return self._gemini_analysis(objetivo, acoes)
        except Exception as e:
            print(f"⚠️ Erro na API: {e}. Usando análise local.")
            return self._local_analysis(objetivo, acoes)
    
    def _openai_analysis(self, objetivo: str, acoes: str) -> Dict:
        prompt = f"""
        Analise este PDI (Plano de Desenvolvimento Individual) e forneça insights detalhados:

        OBJETIVO: {objetivo}
        AÇÕES: {acoes}

        Por favor, analise e retorne um JSON com:
        1. quality_score (0-1): Qualidade geral do PDI
        2. skill_type: "hard_skill", "soft_skill", "hybrid", ou "unknown"
        3. clarity_level: "high", "medium", ou "low"
        4. specificity_level: "high", "medium", ou "low"
        5. suggestions: Lista de 3-5 sugestões de melhoria
        6. time_bound: boolean se tem prazo definido
        7. measurable: boolean se tem métricas mensuráveis
        8. ai_insights: Insights únicos que só IA pode fornecer

        Responda APENAS com JSON válido.
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0.3
        }
        
        response = requests.post(self.base_urls["openai"], headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            
            try:
                return json.loads(ai_response)
            except json.JSONDecodeError:
                return self._extract_json_from_text(ai_response)
        else:
            raise Exception(f"API Error: {response.status_code}")
    
    def _gemini_analysis(self, objetivo: str, acoes: str) -> Dict:
        prompt = f"""
        Analise este PDI brasileiro e retorne insights em JSON:
        Objetivo: {objetivo}
        Ações: {acoes}
        
        JSON com: quality_score, skill_type, suggestions, ai_insights
        """
        
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        url = f"{self.base_urls['gemini']}?key={self.api_key}"
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            
            try:
                return json.loads(ai_response)
            except json.JSONDecodeError:
                return self._extract_json_from_text(ai_response)
        else:
            raise Exception(f"Gemini API Error: {response.status_code}")
    
    def _extract_json_from_text(self, text: str) -> Dict:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        return self._local_analysis("", "")
    
    def _local_analysis(self, objetivo: str, acoes: str) -> Dict:
        full_text = f"{objetivo} {acoes}".lower()
        
        # Análise de qualidade básica
        quality_indicators = ['específico', 'mensurar', 'até', 'através', 'para']
        quality_score = sum(1 for indicator in quality_indicators if indicator in full_text) / len(quality_indicators)
        
        # Classificação de habilidade
        hard_keywords = ['python', 'excel', 'sap', 'sql', 'certificação', 'sistema']
        soft_keywords = ['liderança', 'comunicação', 'equipe', 'empatia', 'relacionamento']
        
        hard_count = sum(1 for keyword in hard_keywords if keyword in full_text)
        soft_count = sum(1 for keyword in soft_keywords if keyword in full_text)
        
        if hard_count > soft_count:
            skill_type = "hard_skill"
        elif soft_count > hard_count:
            skill_type = "soft_skill"
        elif hard_count > 0 and soft_count > 0:
            skill_type = "hybrid"
        else:
            skill_type = "unknown"
        
        # Sugestões básicas
        suggestions = []
        if quality_score < 0.5:
            suggestions.append("Adicione mais detalhes específicos ao objetivo")
        if not re.search(r'\b(?:até|em|durante)\s+\w+', full_text):
            suggestions.append("Inclua um prazo específico")
        if not acoes:
            suggestions.append("Defina ações concretas para alcançar o objetivo")
        
        return {
            "quality_score": quality_score,
            "skill_type": skill_type,
            "clarity_level": "high" if "específico" in full_text else "medium",
            "specificity_level": "high" if quality_score > 0.6 else "medium",
            "suggestions": suggestions or ["PDI bem estruturado"],
            "time_bound": bool(re.search(r'\b(?:até|em|durante)\s+\w+', full_text)),
            "measurable": bool(re.search(r'\d+', full_text)),
            "ai_insights": [
                "Análise local realizada sem conexão com APIs",
                f"Tipo de habilidade identificado: {skill_type}",
                f"Score de qualidade calculado: {quality_score:.2f}"
            ]
        }
    
    def generate_improvement_plan(self, objetivo: str, acoes: str, current_analysis: Dict) -> Dict:
        quality_score = current_analysis.get('quality_score', 0.5)
        skill_type = current_analysis.get('skill_type', 'unknown')
        
        improvement_plan = {
            "priority_areas": [],
            "action_steps": [],
            "timeline_suggestion": "",
            "resources": []
        }
        
        # Áreas prioritárias baseadas no score
        if quality_score < 0.4:
            improvement_plan["priority_areas"].extend([
                "Clareza do objetivo",
                "Especificidade das ações",
                "Definição de métricas"
            ])
        elif quality_score < 0.7:
            improvement_plan["priority_areas"].extend([
                "Detalhamento das ações",
                "Estabelecimento de prazos"
            ])
        
        # Passos específicos por tipo de habilidade
        if skill_type == "hard_skill":
            improvement_plan["action_steps"].extend([
                "1. Especifique versões/níveis de proficiência",
                "2. Inclua certificações relevantes",
                "3. Defina projetos práticos de aplicação"
            ])
            improvement_plan["resources"].extend([
                "Documentação oficial da tecnologia",
                "Cursos especializados online",
                "Laboratórios práticos"
            ])
        elif skill_type == "soft_skill":
            improvement_plan["action_steps"].extend([
                "1. Defina comportamentos observáveis",
                "2. Estabeleça situações de prática",
                "3. Inclua feedback 360°"
            ])
            improvement_plan["resources"].extend([
                "Workshops comportamentais",
                "Coaching/mentoring",
                "Avaliações comportamentais"
            ])
        
        # Sugestão de timeline
        if not current_analysis.get('time_bound'):
            improvement_plan["timeline_suggestion"] = "Sugestão: 3-6 meses com marcos mensais"
        
        return improvement_plan
    
    def batch_analyze_pdis(self, pdis_list: List[Dict]) -> List[Dict]:
        results = []
        
        for i, pdi in enumerate(pdis_list):
            print(f"Analisando PDI {i+1}/{len(pdis_list)}...")
            
            objetivo = pdi.get('objetivo', '')
            acoes = pdi.get('acoes', '')
            
            analysis = self.analyze_pdi_with_ai(objetivo, acoes)
            improvement = self.generate_improvement_plan(objetivo, acoes, analysis)
            
            result = {
                **pdi,
                'ai_analysis': analysis,
                'improvement_plan': improvement,
                'analysis_timestamp': self._get_timestamp()
            }
            
            results.append(result)
        
        return results
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
