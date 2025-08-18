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

### ⚙️ Configuration
Copier le fichier d'exemple et renseigner vos valeurs sensibles :

```bash
cp .env.example .env
# Éditer .env pour définir MAKE_API_KEY, LOG_LEVEL, etc.
```

### 🐳 Docker
Construire l'image et exécuter le conteneur :

```bash
docker build -t graal-support-assistant .
docker run --env-file .env -p 5000:5000 graal-support-assistant
```

Avec Docker Compose :

```bash
docker-compose up --build
```

### ☁️ Déploiement Cloud
- **AWS ECS** :
  1. `docker build -t <account>.dkr.ecr.<region>.amazonaws.com/graal-support-assistant:latest .`
  2. Pousser l'image sur ECR puis créer un service ECS Fargate exposant le port 5000.
  3. Configurer l'Auto Scaling (nombre minimal/maximal de tâches) selon la charge.
- **GCP Cloud Run** :
  1. `gcloud builds submit --tag gcr.io/<project>/graal-support-assistant`
  2. `gcloud run deploy graal-support-assistant --image gcr.io/<project>/graal-support-assistant --platform managed --allow-unauthenticated`
  3. Ajuster le nombre maximal d'instances via `--max-instances` pour le scaling automatique.
