# Multi-Agent Debate System

Ce projet consiste à créer une application de débat basée sur des agents intelligents utilisant des modèles de langage (LLM).  
Le principe est simple : deux agents débattent d’un sujet (POUR / CONTRE), un modérateur analyse les échanges, et un juge attribue des scores.

Le projet a été réalisé dans le cadre d’un TP en intelligence artificielle.

---

## 🎯 Objectif

L’objectif était de :

- simuler un débat entre plusieurs agents  
- utiliser des techniques de raisonnement (pas juste générer du texte)  
- analyser les arguments et produire une synthèse  
- créer une interface simple avec Streamlit  

---

## ⚙️ Fonctionnement

Le système repose sur plusieurs agents :

- **Agent POUR** : défend le sujet  
- **Agent CONTRE** : donne un avis opposé  
- **Modérateur** : résume et analyse les arguments  
- **Juge IA** : attribue des scores (logique, clarté, persuasion)  

Les agents interagissent entre eux pour construire un débat structuré.

---

## 🧠 Choix des techniques de raisonnement

On a utilisé deux techniques principales :

### ReAct (Reason + Act)

Chaque agent suit un cycle :

- analyser le sujet  
- produire des arguments  
- observer la réponse adverse  
- répondre  

👉 Cette technique permet d’avoir un vrai échange et pas des réponses isolées.

---

### Self-Correction

Le modérateur :

- compare les arguments  
- détecte les points faibles  
- produit une synthèse  

👉 Cela permet d’avoir un résultat plus équilibré.

---

## 🛠️ Technologies utilisées

- Python  
- Streamlit  
- API LLM  
- Architecture en modules (agents, core, ui, utils)

---

## 🚀 Installation

Cloner le projet :

```bash
git clone https://github.com/AyaDoukarr/projet-ai.git
cd projet-ai
Installer les dépendances :

pip install -r requirements.txt
🔑 Configuration

Créer un fichier .env et ajouter la clé API :

OPENAI_API_KEY=your_key
▶️ Lancer l’application
streamlit run app.py

Puis ouvrir :

http://localhost:8501
📁 Structure du projet
agents/     → logique des agents
core/       → communication avec le LLM
ui/         → interface Streamlit
utils/      → gestion de session
app.py      → point d’entrée
📌 Remarques
les réponses peuvent varier selon le sujet
le système dépend du modèle utilisé
le but est surtout de montrer le raisonnement multi-agents
👥 Auteurs
Aya Doukarr
Aya Es-Smahi
