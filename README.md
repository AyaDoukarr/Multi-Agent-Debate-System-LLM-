# Multi-Agent Debate System

Ce projet consiste à développer une application de débat basée sur des agents intelligents utilisant des modèles de langage (LLM).  
Le système permet de simuler un débat entre deux agents ayant des positions opposées, avec un modérateur qui analyse les échanges et un juge qui attribue des scores.

Ce travail a été réalisé dans le cadre d’un TP en intelligence artificielle.
## Objectif

L’objectif du projet est de :

- simuler un débat structuré entre plusieurs agents  
- intégrer des techniques de raisonnement (et pas seulement générer du texte)  
- produire une analyse critique et une synthèse  
- proposer une interface simple avec Streamlit  

## Fonctionnement

Le système repose sur plusieurs agents :

- Agent POUR : défend le sujet  
- Agent CONTRE : propose un point de vue opposé  
- Modérateur : analyse les arguments et produit une synthèse  
- Juge IA : évalue les réponses selon plusieurs critères  

Les agents interagissent entre eux pour construire un débat progressif et structuré.


## Techniques de raisonnement

Deux techniques principales ont été utilisées :

### ReAct (Reason + Act)

Chaque agent suit une boucle :

- analyse du sujet  
- génération d’arguments  
- observation des réponses adverses  
- réaction adaptée  

Cette approche permet de simuler un raisonnement dynamique et un vrai échange entre agents.

### Self-Correction

Le modérateur joue un rôle d’analyse :

- comparaison des arguments  
- identification des points forts et faibles  
- production d’une synthèse équilibrée  

Cela permet d’améliorer la qualité globale du débat.


## Technologies utilisées

- Python  
- Streamlit  
- API LLM  
- Architecture modulaire (agents, core, ui, utils)


## Installation

Cloner le projet :

```bash
git clone https://github.com/AyaDoukarr/projet-ai.git
cd projet-ai
```
Installer les dépendances :
```bash
pip install -r requirements.txt
```
Configuration

Créer un fichier .env et ajouter la clé API :
```bash
OPENAI_API_KEY=your_key
```
Lancer l’application
```bash
streamlit run app.py
```
Puis ouvrir dans le navigateur :

Puis ouvrir dans le navigateur :

http://localhost:8501


## Structure du projet

```text
agents/     # logique des agents
core/       # communication avec le LLM
ui/         # interface utilisateur
utils/      # gestion de session
app.py      # point d’entrée
```
## Remarques
les réponses peuvent varier selon le sujet
le système dépend du modèle utilisé
le projet vise surtout à illustrer le raisonnement multi-agents

## 👤 Auteurs

Aya Doukar

Aya Es-smahi
