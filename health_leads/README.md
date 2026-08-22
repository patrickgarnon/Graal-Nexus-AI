# Graal Health Leads — Jouvence du Graal

Microservice FastAPI **indépendant** de capture de leads pour Jouvence du
Graal (Protocole Sommeil & Récupération 2026). Il ne modifie ni ne dépend du
pipeline autopilot Make.com/Flask existant à la racine du repo
(`main.py`, `webhook.py`, `support_assistant/`) — les deux tournent côte à
côte, sur des ports distincts.

## 📂 Arborescence

```
graal-nexus-ai/
└── health_leads/
    ├── __init__.py
    ├── config.py           # Configuration (préfixe GRAAL_HEALTH_*)
    ├── main.py              # Application FastAPI + endpoints
    ├── pdf_generator.py     # ReportLab — Protocole Sommeil 2026 (en mémoire)
    ├── brevo_client.py      # Client async Brevo
    ├── sheets_client.py     # Client async → webhook Apps Script
    ├── tests/
    │   ├── __init__.py
    │   ├── test_health_leads.py
    │   └── test_pdf_generator.py
    ├── requirements.txt
    ├── .env.example
    └── pytest.ini
```

## 🔧 Installation

```bash
cd health_leads
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example ../.env   # à la racine du repo, remplir les valeurs GRAAL_HEALTH_*
```

## ▶️ Lancement local

```bash
# depuis la racine du repo graal-nexus-ai/
uvicorn health_leads.main:app --reload --port 8100
```

> Port 8100 volontairement distinct de `webhook.py` (port 8000) pour
> permettre l'exécution simultanée des deux services.

## ✅ Tests

```bash
cd health_leads
pytest -v
```

## 🧪 Tests cURL

```bash
curl http://localhost:8100/health

curl -X POST "http://localhost:8100/api/v1/graal/lead-capture" \
     -H "Content-Type: application/json" \
     -d '{"email": "patrick.garnon@sanoja.ai", "first_name": "Patrick", "consent_given": true}'

# Rejet — consentement manquant (400)
curl -i -X POST "http://localhost:8100/api/v1/graal/lead-capture" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "first_name": "Test", "consent_given": false}'
```

## 🚀 Déploiement

Même approche que le backend Sanoja (voir `sanoja-website/README.md`) :
Docker ou VPS + Gunicorn/Uvicorn workers. Éviter le serverless stateless
(BackgroundTasks + rate limiter en mémoire).

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY health_leads/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY health_leads/ ./health_leads/
EXPOSE 8100
CMD ["uvicorn", "health_leads.main:app", "--host", "0.0.0.0", "--port", "8100"]
```

## 🔐 Conformité

- Consentement LPRPDE/RGPD explicite requis (400 sinon).
- PDF généré en mémoire (`io.BytesIO`), aucune écriture disque.
- Rate limiting 5 req/min/IP par défaut.
- Disclaimer légal santé inclus (aucune promesse de guérison/diagnostic).
