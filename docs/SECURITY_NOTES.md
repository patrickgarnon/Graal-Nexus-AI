# Constats de sécurité — cycle 2026-08-22

Constats réels trouvés en lisant le code de `main`, pas des suppositions. Statut : CONFIRMÉ.

## Corrigé ce cycle

- **`dashboard/app.py` et `support_assistant/app.py` lançaient Flask avec `debug=True` en dur.** Le débogueur interactif de Flask/Werkzeug permet l'exécution de code arbitraire si le port est jamais exposé au-delà de `localhost`. Corrigé : `debug` est maintenant lu depuis `FLASK_DEBUG` (défaut `0`/désactivé). Vérifié avec un test client Flask (`app.debug == False` par défaut) et compilation Python des deux fichiers.

## Non corrigé — nécessite une revue de conception, pas un correctif mécanique

- **`support_assistant/app.py`, route `GET /make` : le jeton API Make est lu depuis `request.args` (paramètre d'URL)**, puis réaffiché dans un champ `<input type="text">` (pas `type="password"`) du template `make.html`. Un jeton API dans l'URL se retrouve dans l'historique du navigateur, les logs de proxy/serveur et l'en-tête `Referer` de toute requête sortante depuis cette page. Recommandation : faire transiter le jeton uniquement via `POST`/session côté serveur, jamais en paramètre `GET`. Non corrigé ici car cela change le contrat de l'API (les templates construisent des liens avec `?api_token=...`) — à traiter avec la fusion de `codex/set-up-pytest-and-basic-tests` (voir `docs/BRANCH_TRIAGE.md`), qui touche les mêmes routes.
- **`support_assistant/app.py` définit `OWNER_EMAIL = "patrickgarnon09@gmail.com"` en dur, mais cette variable n'est utilisée nulle part ailleurs dans le fichier** (confirmé par recherche exhaustive). C'est à la fois du code mort et une adresse courriel personnelle commitée dans l'historique Git. Non supprimé ici pour ne pas détruire une intention potentielle (peut-être prévue pour une notification par courriel non encore branchée) — à clarifier avec Patrick : soit l'implémenter réellement (notification à l'installation), soit la retirer.
- **Aucune protection CSRF** sur les routes `POST /install` et `POST /make/trigger/<scenario_id>`. Si `support_assistant` est un jour exposé publiquement, un site tiers pourrait forcer le navigateur de l'utilisateur à déclencher un scénario Make à son insu. À corriger avant toute exposition au-delà d'un usage local/de confiance.

## Pas un problème

- `webhook.py` contient la chaîne `export WEBHOOK_SECRET="supersecret"` — c'est un exemple dans la docstring d'usage (`Usage:: export WEBHOOK_SECRET="supersecret"`), pas un secret réel commité. Vérifié en lisant le fichier en entier.
- Recherche exhaustive de motifs `api_key`/`secret`/`token`/`password` suivis d'une valeur littérale dans `.py`/`.json`/`.env*` : aucun secret réel trouvé dans `main`.
