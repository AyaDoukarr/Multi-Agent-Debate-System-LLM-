import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()



GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
) if GROQ_API_KEY else None




def check_api_key() -> None:
    if not GROQ_API_KEY:
        st.error("❌ Clé API Groq introuvable. Ajoute GROQ_API_KEY dans ton fichier .env")
        st.stop()




def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    if client is None:
        return "❌ Erreur : client Groq non initialisé."

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        content = response.choices[0].message.content
        return content.strip() if content else "⚠️ Aucune réponse générée."

    except Exception as e:
        return f"❌ Erreur lors de l'appel au modèle : {e}"




def agent_pro(topic: str) -> str:
    system_prompt = "Tu es un expert qui défend le sujet (position POUR). Donne des arguments convaincants."
    user_prompt = f"Sujet du débat : {topic}"
    return call_llm(system_prompt, user_prompt)


def agent_contre(topic: str) -> str:
    system_prompt = "Tu es un expert critique (position CONTRE). Donne des arguments opposés solides."
    user_prompt = f"Sujet du débat : {topic}"
    return call_llm(system_prompt, user_prompt)


def agent_moderateur(topic: str, pro_argument: str, contre_argument: str) -> str:
    system_prompt = "Tu es un modérateur neutre. Fais une synthèse claire et équilibrée du débat."
    user_prompt = f"""
Sujet : {topic}

Argument POUR :
{pro_argument}

Argument CONTRE :
{contre_argument}

Fais une synthèse.
"""
    return call_llm(system_prompt, user_prompt)




def lancer_debat(topic: str):
    pro = agent_pro(topic)
    contre = agent_contre(topic)
    synthese = agent_moderateur(topic, pro, contre)

    return {
        "pro": pro,
        "contre": contre,
        "synthese": synthese
    }