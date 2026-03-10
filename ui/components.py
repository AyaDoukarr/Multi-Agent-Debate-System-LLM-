import matplotlib.pyplot as plt
import streamlit as st


def render_header():
    st.markdown('<div class="main-title">🤖 Débat IA Multi-Agents</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Une application de débat intelligent avec architecture multi-agents, modération et évaluation automatique.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="box">
        <b>Agents présents :</b>
        <ul>
        <li>un agent <b>POUR</b></li>
        <li>un agent <b>CONTRE</b></li>
        <li>un agent <b>MODÉRATEUR</b></li>
        <li>un <b>JUGE IA</b> pour noter la qualité du débat</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ### 🧠 Techniques de raisonnement utilisées

        - **ReAct** : chaque agent analyse le sujet, produit une réponse, observe l’adversaire puis réagit.
        - **Self-Correction** : le modérateur compare les arguments, critique leurs limites et produit une synthèse finale.
        - **Évaluation automatique** : un juge IA attribue des scores de logique, clarté et persuasion.
        """
    )


def render_sidebar(history):
    st.sidebar.title("⚙️ Paramètres")

    example_topics = [
        "L'intelligence artificielle va-t-elle remplacer les développeurs ?",
        "Le télétravail est-il meilleur que le travail au bureau ?",
        "Les réseaux sociaux font-ils plus de mal que de bien ?",
        "Faut-il interdire l'usage du téléphone portable à l'école ?",
        "L'intelligence artificielle est-elle un danger pour l'emploi ?",
        "Les examens à distance sont-ils une bonne idée ?",
    ]

    selected_example = st.sidebar.selectbox("Sujet d'exemple", [""] + example_topics)
    num_args = st.sidebar.slider("Nombre d’arguments", 2, 5, 3)
    tone = st.sidebar.selectbox(
        "Ton du débat",
        ["académique", "professionnel", "convaincant", "formel"],
        index=0
    )
    show_judge = st.sidebar.checkbox("Activer le juge IA", value=True)
    live_mode = st.sidebar.checkbox("Mode débat en direct", value=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🕘 Historique des débats")

    if history:
        for i, item in enumerate(reversed(history[-10:]), start=1):
            st.sidebar.write(f"{i}. {item}")
    else:
        st.sidebar.write("Aucun débat généré pour le moment.")

    return {
        "selected_example": selected_example,
        "num_args": num_args,
        "tone": tone,
        "show_judge": show_judge,
        "live_mode": live_mode,
    }


def plot_scores(scores):
    labels = ["Logique", "Clarté", "Persuasion"]
    pour_scores = [scores["POUR"][label] for label in labels]
    contre_scores = [scores["CONTRE"][label] for label in labels]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(labels, pour_scores, marker="o", linewidth=2, label="POUR")
    ax.plot(labels, contre_scores, marker="o", linewidth=2, label="CONTRE")
    ax.set_ylim(0, 10)
    ax.set_ylabel("Score /10")
    ax.set_title("Comparaison des scores du débat")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)