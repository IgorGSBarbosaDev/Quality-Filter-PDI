import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.skill_classifier import SkillClassifier, SkillType

classifier = SkillClassifier()

test_skills = [
    "Aprender Python",
    "Desenvolver liderança", 
    "Certificação AWS",
    "Comunicação eficaz",
    "SQL e bancos de dados",
    "Trabalho em equipe"
]

print("=== TESTE CLASSIFICADOR DE HABILIDADES ===\n")

for skill in test_skills:
    result = classifier.classify_skill(skill)
    print(f"Habilidade: {skill}")
    print(f"Tipo: {result['skill_type']}")
    print(f"Confiança: {result['confidence']:.2f}")
    print(f"Recomendação: {result['recommendation']}")
    print("-" * 50)
