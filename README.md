# 🤖 Graal Nexus AI – Autopilot System

## 🚀 Description
Système IA autonome multi-niches :
- ✅ Make (Scénarios 100 % automatisés)
- ✅ Prompts optimisés Lyra 2.0
- ✅ Tunnels de vente IA
- ✅ Publication et viralisation YouTube/TikTok
- ✅ Génération de revenus passifs (Autopilot)

---

## 📂 Contenu
- **Graal-Nexus-AI.zip** → Contient les fichiers de configuration, prompts, et scénarios Make.
- **/docs** → Guides d'installation et intégration.
- **/scripts** → Automatisations GitHub → Make.

---

## 🔗 Intégrations
- Make
- Notion
- ClickUp
- YouTube, TikTok, Instagram
- Stripe, Shopify, Amazon Affilié

---

## ⚡ Objectif
Créer un moteur autonome capable de générer, publier et monétiser du contenu en boucle pour atteindre **1M$ de revenus passifs en < 12 mois**.

---

## 👤 Auteur
**Patrick Garnon** – Projet Graal Ultima Thulé

## 🛠 Support Assistant Web App
Un prototype Flask permettant de déclencher un scénario Make avec un jeton API fourni par l'utilisateur.

### ▶️ Lancer l'application
```bash
cd support_assistant
pip install -r requirements.txt
python app.py
```

Ouvrir ensuite http://localhost:5000 pour saisir le jeton API Make et l'ID du scénario.
L'adresse du propriétaire est configurée dans `support_assistant/app.py` via `OWNER_EMAIL`.

### 🧠 Cache et parallélisation

- Les appels à l'API Make sont mis en cache via `functools.lru_cache` (32 entrées). Cela évite de répéter des requêtes identiques.
- Le cache est propre au processus et peut être vidé manuellement via l'endpoint `POST /cache/clear` ou automatiquement lorsque la capacité est atteinte.
- Pour publier sur plusieurs scénarios en parallèle, indiquez plusieurs IDs séparés par des virgules. Le traitement s'effectue via `ThreadPoolExecutor` pour accélérer les publications multicanales.
