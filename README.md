# Multi-Agent Debate System (LLM)

Ce projet implémente une architecture **multi-agents** basée sur des LLM, dans laquelle deux agents débattent d’un sujet proposé par l’utilisateur tandis qu’un troisième agent agit comme modérateur pour produire une synthèse équilibrée.

Le projet a été réalisé dans le cadre d’un TP en IA générative portant sur les **agents intelligents, le raisonnement avancé et l’intégration via Streamlit** :contentReference[oaicite:1]{index=1}.

---

## 🎯 Objectif

L’objectif était de concevoir une application interactive capable :

- de simuler un débat structuré entre deux agents  
- d’implémenter des techniques explicites de raisonnement  
- de produire une synthèse cohérente et argumentée  
- d’offrir une interface simple via Streamlit  

---

## ⚙️ Architecture

Le système repose sur trois agents :

### 🟢 Agent 1 — Position A  
Analyse le sujet proposé et développe une argumentation structurée.

### 🔵 Agent 2 — Position B  
Propose un point de vue opposé en répondant aux arguments du premier agent.

### 🟣 Modérateur  
Observe les échanges, identifie les points forts/faibles et produit une conclusion équilibrée.

---

## 🧠 Techniques de raisonnement utilisées

Le projet implémente plusieurs approches :

### ReAct (principal)

Chaque agent suit une boucle :

1. Analyse du sujet  
2. Production d’arguments  
3. Observation de la réponse adverse  
4. Réponse adaptée  

### Self-Correction

Le modérateur critique les arguments produits et génère une synthèse cohérente.

👉 Ces techniques ont été choisies car le sujet demandait explicitement d’intégrer des mécanismes de raisonnement et non un simple chatbot :contentReference[oaicite:2]{index=2}.

---

## 🛠️ Stack technique

- Python  
- LLM (via API)  
- Streamlit  
- Architecture modulaire (agents / core / utils)

---

## 🚀 Installation

Cloner le repo :

```bash
git clone https://github.com/AyaDoukarr/projet-ai.git
cd projet-ai
````

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

Créer le fichier `.env` :

```bash
cp .env.template .env
```

Ajouter la clé API :

```
OPENAI_API_KEY=ta_clef
```

---

## ▶️ Lancer l’application

```bash
streamlit run app.py
```

Puis ouvrir :

```
http://localhost:8501
```

---

## 📁 Structure du projet

```
projet-ai/
│── agents/     # logique des agents
│── core/       # orchestration
│── ui/         # interface Streamlit
│── utils/
│── app.py
│── requirements.txt
```

---

## 📌 Remarques

* Le comportement dépend fortement du prompt et du sujet proposé
* Certains débats peuvent produire des réponses variables selon le contexte
* Le projet vise surtout à illustrer la logique d’orchestration multi-agents

---

## 👤 Auteur

Aya Doukarr
