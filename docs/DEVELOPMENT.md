# Guide de développement

Ce document explique comment étendre les agents IA et les scénarios Make du projet **Graal Nexus AI**.

## 🔧 Étendre les agents

1. Créer un nouveau fichier JSON dans `1-Agents-AI/` décrivant l'agent.
2. Définir les objectifs, prompts et paramètres spécifiques.
3. Ajouter l'agent dans votre configuration (voir `examples/`).

## 🛠 Étendre les scénarios

1. Dupliquer un fichier `.make.json` depuis `2-Scenarios-Make/`.
2. Ajuster les modules et connexions dans Make selon vos besoins.
3. Mettre à jour les variables d'environnement (`MAKE_SCENARIO_ID`) pour pointer vers le nouveau scénario.

## 🧪 Tests locaux

- Lancer `python -m py_compile support_assistant/app.py` pour vérifier la syntaxe.
- Exécuter `pytest` pour lancer les tests (aucun test n'est encore fourni).

## 🚀 Contribution

Les contributions sont les bienvenues via pull request. Pensez à documenter toute nouvelle variable d'environnement ou dépendance.
