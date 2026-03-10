from core.llm import call_llm


def judge_agent(topic: str, pour_text: str, contre_text: str) -> str:
    system_prompt = """
Tu es un juge de débat neutre, rigoureux et concis.

Tu dois noter chaque camp sur 10 pour :
- Logique
- Clarté
- Persuasion

Tu dois répondre STRICTEMENT au format suivant :

POUR
Logique: X/10
Clarté: X/10
Persuasion: X/10
Commentaire: ...

CONTRE
Logique: X/10
Clarté: X/10
Persuasion: X/10
Commentaire: ...

Verdict: ...
"""
    user_prompt = f"""
Sujet : {topic}

Camp POUR :
{pour_text}

Camp CONTRE :
{contre_text}

Évalue les deux camps.
"""
    return call_llm(system_prompt, user_prompt, 0.3)