from core.llm import call_llm


def agent_pour(topic: str, num_args: int, tone: str) -> str:
    system_prompt = f"""
Tu es un agent de débat spécialisé dans la position POUR.

Objectifs :
- défendre le sujet avec logique, clarté et structure
- adopter un ton {tone}
- être convaincant sans être agressif
- ne jamais afficher ton raisonnement interne
- afficher uniquement la réponse finale

Structure obligatoire :
1. Position
2. {num_args} arguments
3. Mini-conclusion
"""
    user_prompt = f"""
Sujet du débat : {topic}

Mission :
- Défends la position POUR
- Rédige en français
- Fais des arguments clairs, précis et bien organisés
"""
    return call_llm(system_prompt, user_prompt, 0.8)


def agent_contre(topic: str, num_args: int, tone: str) -> str:
    system_prompt = f"""
Tu es un agent de débat spécialisé dans la position CONTRE.

Objectifs :
- contester le sujet avec logique, clarté et structure
- adopter un ton {tone}
- être convaincant sans être agressif
- ne jamais afficher ton raisonnement interne
- afficher uniquement la réponse finale

Structure obligatoire :
1. Position
2. {num_args} arguments
3. Mini-conclusion
"""
    user_prompt = f"""
Sujet du débat : {topic}

Mission :
- Défends la position CONTRE
- Rédige en français
- Fais des arguments clairs, précis et bien organisés
"""
    return call_llm(system_prompt, user_prompt, 0.8)


def rebuttal_agent(role_name: str, topic: str, own_arguments: str, other_arguments: str, tone: str) -> str:
    system_prompt = f"""
Tu es l'agent {role_name} dans un débat argumentatif.

Ta tâche :
- répondre aux arguments de l'adversaire
- identifier 2 limites ou faiblesses dans son raisonnement
- renforcer ta propre position
- garder un ton {tone}
- rester poli, logique et structuré
- ne jamais afficher ton raisonnement interne

Structure obligatoire :
1. Réponse aux arguments opposés
2. Renforcement de ma position
"""
    user_prompt = f"""
Sujet : {topic}

Tes arguments initiaux :
{own_arguments}

Arguments adverses :
{other_arguments}

Rédige une réponse claire et concise en français.
"""
    return call_llm(system_prompt, user_prompt, 0.7)


def moderator_agent(topic: str, pour_round1: str, contre_round1: str, pour_round2: str, contre_round2: str) -> str:
    system_prompt = """
Tu es un modérateur neutre dans un débat multi-agents.

Rôle :
- analyser objectivement les échanges
- identifier les forces du camp POUR
- identifier les forces du camp CONTRE
- repérer les limites ou faiblesses des deux camps
- produire une conclusion finale équilibrée
- ne jamais afficher ton raisonnement interne

Structure obligatoire :
1. Résumé du camp POUR
2. Résumé du camp CONTRE
3. Analyse critique
4. Conclusion finale neutre
"""
    user_prompt = f"""
Sujet du débat : {topic}

--- TOUR 1 : AGENT POUR ---
{pour_round1}

--- TOUR 1 : AGENT CONTRE ---
{contre_round1}

--- TOUR 2 : RÉPONSE DU CAMP POUR ---
{pour_round2}

--- TOUR 2 : RÉPONSE DU CAMP CONTRE ---
{contre_round2}

Fais une synthèse équilibrée, claire et bien structurée en français.
"""
    return call_llm(system_prompt, user_prompt, 0.5)