import time
import streamlit as st

from agents.debate_agents import (
    agent_pour,
    agent_contre,
    rebuttal_agent,
    moderator_agent,
)
from agents.judge_agent import judge_agent
from core.parser import parse_judge_scores
from ui.styles import load_css
from ui.components import plot_scores, render_header, render_sidebar
from utils.session import init_session_state
from core.llm import check_api_key


st.set_page_config(
    page_title="Débat IA Multi-Agents",
    page_icon="🤖",
    layout="wide"
)

load_css()
check_api_key()
init_session_state()

render_header()

settings = render_sidebar(st.session_state.history)

topic = st.text_input(
    "Entrez un sujet de débat :",
    value=settings["selected_example"],
    placeholder="Exemple : L'intelligence artificielle va-t-elle remplacer les développeurs ?"
)

col_action_1, col_action_2 = st.columns([1, 3])
with col_action_1:
    launch = st.button("Lancer le débat", use_container_width=True)
with col_action_2:
    st.caption("Astuce : choisis un sujet clair et polémique pour une meilleure démonstration.")


if launch:
    if not topic.strip():
        st.warning("Veuillez entrer un sujet.")
        st.stop()

    progress = st.progress(0, text="Initialisation du débat...")
    live_status = st.empty()

    # Zone résultats créée immédiatement
    result_container = st.container()

    with result_container:
        st.markdown("---")
        st.subheader("📌 Résultats du débat")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("## 🟢 Agent POUR")
            pour_box_1 = st.empty()
            st.markdown("### Réponse du camp POUR")
            pour_box_2 = st.empty()

        with col2:
            st.markdown("## 🔴 Agent CONTRE")
            contre_box_1 = st.empty()
            st.markdown("### Réponse du camp CONTRE")
            contre_box_2 = st.empty()

        st.markdown("---")
        st.markdown("## ⚖️ Modérateur")
        moderator_box = st.empty()

        judge_box = None
        chart_box = None
        metrics_box = None

        if settings["show_judge"]:
            st.markdown("---")
            st.markdown("## 🧠 Analyse du juge IA")
            judge_box = st.empty()

            st.markdown("## 📊 Graphique des scores")
            chart_box = st.empty()

            metrics_box = st.empty()

    # Messages d'attente initiaux
    pour_box_1.info("⏳ Génération de la position initiale du camp POUR...")
    pour_box_2.info("⏳ En attente de la réfutation du camp POUR...")
    contre_box_1.info("⏳ Génération de la position initiale du camp CONTRE...")
    contre_box_2.info("⏳ En attente de la réfutation du camp CONTRE...")
    moderator_box.info("⏳ Le modérateur attend les échanges pour produire sa synthèse...")

    if settings["show_judge"] and judge_box is not None:
        judge_box.info("⏳ Le juge IA attend la fin du débat pour noter les deux camps...")
    if settings["show_judge"] and chart_box is not None:
        chart_box.info("⏳ Le graphique apparaîtra après l'évaluation du juge IA...")
    if settings["show_judge"] and metrics_box is not None:
        metrics_box.info("⏳ Les scores finaux seront affichés après l'évaluation...")

    if settings["live_mode"]:
        live_status.info("🚀 Le débat commence...")

    # =========================
    # Tour 1 - Agent POUR
    # =========================
    if settings["live_mode"]:
        live_status.info("🟢 Agent POUR réfléchit...")
        time.sleep(1)

    pour_round1 = agent_pour(topic, settings["num_args"], settings["tone"])
    progress.progress(20, text="Agent POUR terminé")

    pour_box_1.success("✅ Réponse initiale du camp POUR générée")
    pour_box_1.write(pour_round1)

    # =========================
    # Tour 1 - Agent CONTRE
    # =========================
    if settings["live_mode"]:
        live_status.info("🔴 Agent CONTRE réfléchit...")
        time.sleep(1)

    contre_round1 = agent_contre(topic, settings["num_args"], settings["tone"])
    progress.progress(40, text="Agent CONTRE terminé")

    contre_box_1.success("✅ Réponse initiale du camp CONTRE générée")
    contre_box_1.write(contre_round1)

    # =========================
    # Tour 2 - Réfutation POUR
    # =========================
    if settings["live_mode"]:
        live_status.info("🟢 Agent POUR prépare sa réfutation...")
        time.sleep(1)

    pour_round2 = rebuttal_agent(
        role_name="POUR",
        topic=topic,
        own_arguments=pour_round1,
        other_arguments=contre_round1,
        tone=settings["tone"],
    )
    progress.progress(60, text="Réponse du camp POUR terminée")

    pour_box_2.success("✅ Réfutation du camp POUR générée")
    pour_box_2.write(pour_round2)

    # =========================
    # Tour 2 - Réfutation CONTRE
    # =========================
    if settings["live_mode"]:
        live_status.info("🔴 Agent CONTRE prépare sa réfutation...")
        time.sleep(1)

    contre_round2 = rebuttal_agent(
        role_name="CONTRE",
        topic=topic,
        own_arguments=contre_round1,
        other_arguments=pour_round1,
        tone=settings["tone"],
    )
    progress.progress(75, text="Réponse du camp CONTRE terminée")

    contre_box_2.success("✅ Réfutation du camp CONTRE générée")
    contre_box_2.write(contre_round2)

    # =========================
    # Modérateur
    # =========================
    if settings["live_mode"]:
        live_status.info("⚖️ Le modérateur analyse le débat...")
        time.sleep(1)

    final_summary = moderator_agent(
        topic=topic,
        pour_round1=pour_round1,
        contre_round1=contre_round1,
        pour_round2=pour_round2,
        contre_round2=contre_round2,
    )
    progress.progress(90, text="Synthèse du modérateur terminée")

    moderator_box.success("✅ Synthèse du modérateur générée")
    moderator_box.write(final_summary)

    # =========================
    # Juge IA
    # =========================
    judge_result = ""
    scores = None

    if settings["show_judge"]:
        if settings["live_mode"]:
            live_status.info("🧠 Le juge IA évalue le débat...")
            time.sleep(1)

        judge_result = judge_agent(
            topic=topic,
            pour_text=f"{pour_round1}\n\n{pour_round2}",
            contre_text=f"{contre_round1}\n\n{contre_round2}",
        )
        scores = parse_judge_scores(judge_result)

        if judge_box is not None:
            judge_box.success("✅ Analyse du juge IA générée")
            judge_box.write(judge_result)

        if chart_box is not None:
            with chart_box.container():
                plot_scores(scores)

        if metrics_box is not None:
            total_pour = sum(scores["POUR"].values())
            total_contre = sum(scores["CONTRE"].values())

            with metrics_box.container():
                c1, c2, c3 = st.columns(3)
                c1.metric("Score total POUR", f"{total_pour}/30")
                c2.metric("Score total CONTRE", f"{total_contre}/30")

                if total_pour > total_contre:
                    c3.metric("Camp gagnant", "POUR")
                elif total_contre > total_pour:
                    c3.metric("Camp gagnant", "CONTRE")
                else:
                    c3.metric("Camp gagnant", "ÉGALITÉ")

    progress.progress(100, text="Débat terminé")

    if settings["live_mode"]:
        live_status.success("✅ Débat terminé avec succès.")

    full_debate_text = f"""
SUJET DU DÉBAT
{topic}

==============================
AGENT POUR - TOUR 1
==============================
{pour_round1}

==============================
AGENT CONTRE - TOUR 1
==============================
{contre_round1}

==============================
RÉPONSE DU CAMP POUR
==============================
{pour_round2}

==============================
RÉPONSE DU CAMP CONTRE
==============================
{contre_round2}

==============================
MODÉRATEUR
==============================
{final_summary}

==============================
JUGE IA
==============================
{judge_result if judge_result else "Juge désactivé"}
"""

    st.session_state.debat_genere = {
        "topic": topic,
        "pour_round1": pour_round1,
        "contre_round1": contre_round1,
        "pour_round2": pour_round2,
        "contre_round2": contre_round2,
        "final_summary": final_summary,
        "judge_result": judge_result,
        "scores": scores,
        "full_debate_text": full_debate_text,
    }

    st.session_state.history.append(topic)

