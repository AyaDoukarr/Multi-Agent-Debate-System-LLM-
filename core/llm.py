import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def check_api_key():
    if not api_key:
        st.error("Clé API introuvable. Ajoute OPENAI_API_KEY dans ton fichier .env")
        st.stop()


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
        return content.strip() if content else "Aucune réponse générée."
    except Exception as e:
        return f"Erreur lors de l'appel au modèle : {e}"