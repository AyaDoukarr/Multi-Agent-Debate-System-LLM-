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
from core.llm import check_api_key, call_llm


st.set_page_config(
    page_title="Débat IA Multi-Agents",
    page_icon="🤖",
    layout="wide"
)

load_css()
check_api_key()
init_session_state()

if "page" not in st.session_state:
    st.session_state.page = "home"

if "preset_topic" not in st.session_state:
    st.session_state.preset_topic = ""

if "debat_genere" not in st.session_state:
    st.session_state.debat_genere = None

if "history" not in st.session_state:
    st.session_state.history = []

if "debate_context" not in st.session_state:
    st.session_state.debate_context = ""

if "follow_up_history" not in st.session_state:
    st.session_state.follow_up_history = []


def load_home_css() -> None:
    try:
        with open("ui/home.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Le fichier ui/home.css est introuvable.")


def go_to_home() -> None:
    st.session_state.page = "home"
    st.session_state.preset_topic = ""
    st.rerun()


def go_to_app(topic: str = "") -> None:
    st.session_state.page = "app"
    st.session_state.preset_topic = topic
    st.rerun()


def show_home() -> None:
    load_home_css()

    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">Débat IA Multi-Agents</div>
            <div class="hero-subtitle">
                Application interactive simulant un débat intelligent entre plusieurs agents IA
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Agents du système</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="card agent-card-green"><h4>Agent POUR</h4><p>Défend le sujet avec des arguments structurés.</p></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="card agent-card-red"><h4>Agent CONTRE</h4><p>Propose un point de vue opposé et répond aux objections.</p></div>',
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            '<div class="card agent-card-yellow"><h4>Modérateur</h4><p>Analyse les échanges et produit une synthèse équilibrée.</p></div>',
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            '<div class="card agent-card-blue"><h4>Juge IA</h4><p>Attribue des scores selon plusieurs critères.</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Techniques utilisées</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="card tech-card-indigo"><h4>ReAct</h4><p>Analyse, action, observation et réaction.</p></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="card tech-card-cyan"><h4>Self-Correction</h4><p>Analyse critique et synthèse du modérateur.</p></div>',
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            '<div class="card tech-card-pink"><h4>Évaluation</h4><p>Notation automatique selon plusieurs critères.</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Fonctionnement général</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="process-box">
            <p>
                1. L’utilisateur choisit ou saisit un sujet.<br>
                2. Les agents POUR et CONTRE génèrent leurs arguments.<br>
                3. Chaque agent répond aux arguments adverses.<br>
                4. Le modérateur produit une synthèse.<br>
                5. Le juge IA attribue des scores et le système affiche un graphique final.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Sujets de démonstration</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("IA et développeurs", use_container_width=True):
            go_to_app("L'intelligence artificielle va-t-elle remplacer les développeurs ?")

    with c2:
        if st.button("Télétravail", use_container_width=True):
            go_to_app("Le télétravail est-il meilleur que le travail au bureau ?")

    with c3:
        if st.button("Réseaux sociaux", use_container_width=True):
            go_to_app("Les réseaux sociaux font-ils plus de mal que de bien ?")

    st.markdown(
        """
        <div class="info-box">
            Vous pouvez choisir un sujet proposé ou cliquer sur le bouton ci-dessous
            pour saisir librement votre propre sujet.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("Commencer", use_container_width=True):
        go_to_app("")


def render_saved_debate(data: dict, show_judge: bool) -> None:
    st.markdown("---")
    st.subheader("📌 Résultats du débat")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🟢 Agent POUR")
        st.write(data["pour_round1"])
        st.markdown("### Réponse du camp POUR")
        st.write(data["pour_round2"])

    with col2:
        st.markdown("## 🔴 Agent CONTRE")
        st.write(data["contre_round1"])
        st.markdown("### Réponse du camp CONTRE")
        st.write(data["contre_round2"])

    st.markdown("---")
    st.markdown("## ⚖️ Modérateur")
    st.write(data["final_summary"])

    if show_judge:
        st.markdown("---")
        st.markdown("## 🧠 Analyse du juge IA")
        st.write(data["judge_result"])

        if data["scores"] is not None:
            st.markdown("## 📊 Graphique des scores")
            plot_scores(data["scores"])

            total_pour = sum(data["scores"]["POUR"].values())
            total_contre = sum(data["scores"]["CONTRE"].values())

            c1, c2, c3 = st.columns(3)
            c1.metric("Score total POUR", f"{total_pour}/30")
            c2.metric("Score total CONTRE", f"{total_contre}/30")

            if total_pour > total_contre:
                c3.metric("Camp gagnant", "POUR")
            elif total_contre > total_pour:
                c3.metric("Camp gagnant", "CONTRE")
            else:
                c3.metric("Camp gagnant", "ÉGALITÉ")

    st.markdown("---")
    st.download_button(
        label="📥 Télécharger le débat complet",
        data=data["full_debate_text"],
        file_name="debat_multi_agents.txt",
        mime="text/plain"
    )


def show_follow_up_section() -> None:
    if not st.session_state.debate_context:
        return

    st.markdown("---")
    st.markdown("## 💬 Poser une nouvelle question sur ce débat")

    st.caption(
        "Cette fonctionnalité permet de continuer la discussion sans relancer un nouveau débat. "
        "Le système garde le contexte du débat déjà généré."
    )

    follow_up_question = st.text_input(
        "Votre nouvelle question",
        placeholder="Exemple : Quel camp est le plus convaincant sur le plan logique ?",
        key="follow_up_question_input"
    )

    if st.button("Envoyer la question", use_container_width=True, key="follow_up_button"):
        if not follow_up_question.strip():
            st.warning("Veuillez entrer une question.")
        else:
            with st.spinner("Génération de la réponse..."):
                system_prompt = """
Tu es un assistant qui répond à des questions en se basant sur le contexte d’un débat déjà généré.
Tu dois répondre de manière claire, concise et structurée.
"""

                user_prompt = f"""
Contexte du débat :
{st.session_state.debate_context}

Question de l'utilisateur :
{follow_up_question}
"""

                follow_up_answer = call_llm(system_prompt, user_prompt, temperature=0.5)

            st.session_state.follow_up_history.append(
                {
                    "question": follow_up_question,
                    "answer": follow_up_answer,
                }
            )

    if st.session_state.follow_up_history:
        st.markdown("### Historique des questions complémentaires")
        for i, item in enumerate(st.session_state.follow_up_history, start=1):
            st.markdown(f"**Question {i} :** {item['question']}")
            st.write(item["answer"])


def show_app() -> None:
    render_header()
    settings = render_sidebar(st.session_state.history)

    top_left, top_right = st.columns([1, 4])
    with top_left:
        if st.button("← Accueil", use_container_width=True):
            go_to_home()
    with top_right:
        st.caption("Astuce : choisis un sujet clair et polémique pour une meilleure démonstration.")

    topic = st.text_input(
        "Entrez un sujet de débat :",
        value=st.session_state.preset_topic if st.session_state.preset_topic else settings["selected_example"],
        placeholder="Exemple : L'intelligence artificielle va-t-elle remplacer les développeurs ?"
    )

    col_action_1, col_action_2 = st.columns([1, 3])
    with col_action_1:
        launch = st.button("Lancer le débat", use_container_width=True)
    with col_action_2:
        st.caption("Les réponses apparaissent progressivement pendant la génération.")

    if not launch and st.session_state.debat_genere is not None:
        render_saved_debate(st.session_state.debat_genere, settings["show_judge"])
        show_follow_up_section()
        return

    if launch:
        if not topic.strip():
            st.warning("Veuillez entrer un sujet.")
            st.stop()

        progress = st.progress(0, text="Initialisation du débat...")
        live_status = st.empty()

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

        if settings["live_mode"]:
            live_status.info("🟢 Agent POUR réfléchit...")
            time.sleep(1)

        pour_round1 = agent_pour(topic, settings["num_args"], settings["tone"])
        progress.progress(20, text="Agent POUR terminé")
        pour_box_1.success("✅ Réponse initiale du camp POUR générée")
        pour_box_1.write(pour_round1)

        if settings["live_mode"]:
            live_status.info("🔴 Agent CONTRE réfléchit...")
            time.sleep(1)

        contre_round1 = agent_contre(topic, settings["num_args"], settings["tone"])
        progress.progress(40, text="Agent CONTRE terminé")
        contre_box_1.success("✅ Réponse initiale du camp CONTRE générée")
        contre_box_1.write(contre_round1)

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

        st.session_state.debate_context = f"""
Sujet du débat :
{topic}

Arguments initiaux du camp POUR :
{pour_round1}

Arguments initiaux du camp CONTRE :
{contre_round1}

Réponse du camp POUR :
{pour_round2}

Réponse du camp CONTRE :
{contre_round2}

Synthèse du modérateur :
{final_summary}

Analyse du juge IA :
{judge_result}
"""

        st.session_state.follow_up_history = []
        st.session_state.history.append(topic)
        st.session_state.preset_topic = ""

        show_follow_up_section()


if st.session_state.page == "home":
    show_home()
else:
    show_app()