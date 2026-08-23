# Triage des branches `codex/*` non fusionnées

Généré le 2026-08-22 par analyse programmatique (`git diff --name-status main...<branche>` pour chacune, pas seulement les noms de branches) — voir méthode en bas de page. Statut : **CONFIRMÉ** pour tout ce qui est décrit ici (diffs réellement lus, pas supposés à partir des noms).

## Contexte corrigé

Un audit précédent (cycle 1, dans `patrickgarnon/sanojagroup`) avait conclu que ce dépôt n'avait « pas de branche `main` ». **C'était une erreur** : l'appel API `list_branches` était paginé à 30 résultats et n'affichait pas `main`, qui existe bel et bien et contient déjà **26 commits, 12 fusions**, une suite de 5 tests qui passent (`python -m pytest tests/`), un module `scripts/make_scenario_builder/` fonctionnel (client Make.com, boucle autopilot, providers OpenRouter/Runway/ElevenLabs), un dashboard Flask, un `support_assistant/` Flask, et des ressources de contenu (prompts, scénarios Make, templates). Voir la correction dans `docs/ASSET_REGISTER.md` de `sanojagroup`.

**Sur les 56 branches `codex/*` créées historiquement, 13 sont déjà fusionnées dans `main`. Les 42 restantes sont analysées ci-dessous.** Chacune ne contient qu'**un seul commit d'écart avec `main`** (confirmé par `git rev-list --count`), ce qui signifie que ce sont des tentatives parallèles indépendantes, pas une chaîne de travail cumulative.

## Ce qui a été vérifié concrètement

- Fusion d'essai de la branche la plus prometteuse (`codex/set-up-pytest-and-basic-tests`) dans `main` : **1 conflit réel** dans `support_assistant/app.py` (`git merge --no-commit` confirmé, conflit non résolu automatiquement — nécessite une revue de code, pas un merge aveugle).
- Presque toutes les branches ci-dessous modifient `support_assistant/app.py` d'une façon incompatible avec les autres — **elles ne peuvent pas être fusionnées en bloc**, une seule par grappe de fonctionnalité peut être retenue.

## Grappes de fonctionnalités en doublon (une seule branche à retenir par grappe)

### 🔴 Priorité haute — fonctionnalités manquantes dans `main`, forte valeur

| Grappe | Branches candidates | Recommandation |
|---|---|---|
| **Suite de tests + 4 intégrations (ElevenLabs, Make, Runway, Shopify)** | `codex/set-up-pytest-and-basic-tests` | **Meilleure candidate globale** — ajoute `support_assistant/integrations/{elevenlabs,make,runway,shopify}.py` + `tests/test_{elevenlabs,make,runway,shopify}.py` + `pytest.ini` + `docs/README.md` en un seul commit cohérent. Fusion testée : 1 conflit dans `support_assistant/app.py`, résolvable avec une revue de ~30 min. **Recommandé comme prochaine PR à traiter, avant les grappes ci-dessous** (elle couvre déjà 3 des 4 grappes suivantes). |
| Retry / backoff réseau | `codex/add-retry-module-with-backoff` (`src/core/retry.py`) · `codex/creer-un-decorateur-retry-avec-configuration` (`nexus/utils/retry.py`) · `codex/creer-utilitaire-de-retry-avec-journalisation` (`src/utils/retry.py`) | Le prompt maître (§3) exige retry+backoff sur toute intégration externe — **vrai manque** dans `main`. 3 implémentations parallèles, aucune fusionnée. À comparer et choisir une seule ; les 2 autres devraient être fermées comme redondantes. |
| Cache pour appels API coûteux | `codex/add-caching-layer-for-expensive-operations` · `codex/encapsulate-heavy-calls-with-caching` · `codex/implement-caching-for-api-access-functions` (`src/utils/cache.py`) · `codex/implement-lru-cache-with-redis-option` (`src/core/cache.py`, option Redis) | 4 implémentations parallèles. `implement-lru-cache-with-redis-option` semble la plus complète (option Redis + `api_client.py` + `file_reader.py`). À valider par lecture de code avant de choisir. |

### 🟡 Priorité moyenne — fonctionnalités déjà partiellement présentes dans `main`

| Grappe | Branches candidates | Recommandation |
|---|---|---|
| ElevenLabs (au-delà du provider déjà mergé) | `codex/add-elevenlabs-audio-generation-feature` · `codex/create-elevenlabs-integration-and-endpoint` · `codex/implement-audio-file-generation-and-retrieval` | 3 implémentations distinctes de la génération audio. Couvertes en partie par `set-up-pytest-and-basic-tests` (voir priorité haute) — traiter celle-ci en premier peut rendre ces 3 redondantes. |
| Runway (au-delà du provider déjà mergé) | `codex/add-runway-api-integration-and-ui` · `codex/add-runway_service.py-and-rest-endpoints` · `codex/implement-runway-video-generation-api` | Idem — probablement redondant une fois `set-up-pytest-and-basic-tests` traitée. |
| Shopify (aucun client Shopify dans `main` actuellement) | `codex/add-shopify-service-module-and-endpoints` · `codex/create-shopify-client-and-endpoints` · `codex/create-shopify-integration-module-and-websocket` · `codex/implement-fetch_recent_sales-function` | 4 implémentations parallèles d'un vrai manque (aucun client Shopify n'existe encore dans `main`, contrairement à Make/Runway/ElevenLabs). Pertinent pour connecter VitaMenu (`docs/INTEGRATION_MAP.md` de `sanojagroup`). À traiter après la grappe pytest. |
| Fonctionnalités Make/Runway additionnelles sur `support_assistant/app.py` | `codex/add-buttons-for-make-and-runway-scenarios` · `codex/add-make-and-runway-features-with-notifications` · `codex/add-post-endpoints-for-execution-and-video-generation` · `codex/create-make-api-integration-and-stats-endpoint` · `codex/implement-make-api-integration` · `codex/implement-make_service.py-with-api-integration` | 6 variantes qui modifient toutes `support_assistant/app.py` de façon incompatible entre elles. Probablement redondant avec la grappe pytest (priorité haute). À revisiter seulement si celle-ci ne couvre pas un besoin spécifique. |
| Documentation | `codex/update-readme-and-add-documentation` (ajoute `docs/DEVELOPMENT.md`, `examples/full_config.yaml`) | Valeur réelle mais modifie aussi `support_assistant/app.py` — à fusionner après la grappe pytest pour éviter un conflit inutile. |

### ⚪ Priorité basse — probablement obsolètes (fonctionnalité déjà fusionnée différemment dans `main`)

| Grappe | Branches | Pourquoi obsolète |
|---|---|---|
| Dashboard en FastAPI | `codex/add-dashboard-package-with-fastapi-server` · `codex/add-fastapi-or-flask-setup-with-templates` · `codex/create-fastapi-dashboard-package` | `main` a déjà choisi **Flask** pour `dashboard/app.py` (fusionné). Ces branches proposent une architecture FastAPI concurrente — les fusionner introduirait deux frameworks web. À fermer, sauf décision explicite de migrer vers FastAPI. |
| Tailwind / thème sombre | `codex/add-tailwindcss-and-ui-components` · `codex/configure-tailwind-with-dark-mode-support` | `main` a déjà fusionné un dashboard Tailwind avec mode sombre (commit `3bb7015`, PR `codex/configurer-tailwind-avec-theme-sombre`). Ces 2 branches sont des tentatives parallèles non retenues. |
| Logging structuré | `codex/add-configurable-logging-module` (`nexus/logging.py`) · `codex/creer-module-de-logging-personnalise` (`src/core/logging.py`) | `main` a déjà `logging_utils.py` fusionné et utilisé par `main.py`. Redondant sauf si ces variantes apportent une capacité manquante (à vérifier au cas par cas si besoin futur). |
| Restructuration `src/` concurrente | `codex/add-src/nexus-directory-with-python-modules` · `codex/create-src/-directory-with-packages` · `codex/creer-structure-de-dossier-et-classes` | `main` a déjà une structure `src/core/` + `src/interfaces/` fusionnée (PR `create-autopilot-engine-module` + `extract-and-organize-graal-nexus-ai`). Ces 3 branches proposent des architectures `src/` concurrentes et incompatibles. À fermer. |
| Exécution asynchrone | `codex/adapter-autopilotengine-pour-asyncio` (`autopilot_engine.py` à la racine) · `codex/use-asyncio-or-concurrent.futures-in-executor` (`src/core/executor.py`) | Idée valable (paralléliser l'autopilot) mais 2 implémentations concurrentes et incompatibles avec la structure déjà fusionnée. À revisiter comme fonctionnalité neuve plus tard, pas comme fusion telle quelle. |
| Duplicata de `support_assistant/app.py` | `codex/create-ai-support-assistant-app-wtmq9o` | Recrée `support_assistant/app.py` depuis zéro — la version fusionnée dans `main` (`create-ai-support-assistant-app`, sans suffixe) est déjà en place et plus avancée. Fermer. |
| Ancien module Make monolithique | `codex/add-chain_http_modules-method-to-makescenariobuilder` | Modifie `make_scenario_builder.py` à la racine, la version pré-refactorisation. `main` a depuis modularisé ce code dans `scripts/make_scenario_builder/` (package avec tests). Vérifier si la méthode ajoutée manque au package actuel avant de fermer définitivement. |
| **⚠️ Nom trompeur** — `codex/locate-and-fix-an-important-bug` | — | Malgré son nom, cette branche ne corrige **aucun bug** : elle ajoute une extraction du zip dans des dossiers numérotés (`1-Agents-AI/`, `2-Scenarios-Make/`, etc.) qui dupliquent `config/agents/`, `config/scenarios/`, `prompts/` déjà présents dans `main` sous d'autres noms. Probablement un titre de branche mal généré par Codex. Aucune action recommandée au-delà de la fermer, sauf si Patrick se souvient d'un bug spécifique à chercher ailleurs. |
| Tests d'intégration standalone | `codex/set-up-pytest-and-basic-tests` | *(déjà classée en priorité haute ci-dessus — ne pas dupliquer l'effort)* |

## Recommandation d'ordre de traitement

1. **`codex/set-up-pytest-and-basic-tests`** — revue du conflit dans `support_assistant/app.py`, puis fusion. Couvre ElevenLabs + Make + Runway + Shopify + tests en un seul geste.
2. Choisir **une** implémentation de retry/backoff parmi les 3 candidates (priorité haute) — requis par le prompt maître §3 pour toute intégration externe.
3. Choisir **une** implémentation de cache parmi les 4 candidates.
4. Fermer explicitement (ou convertir en issues si l'idée reste valable) : les 3 branches FastAPI, les 2 branches Tailwind, les 2 branches logging, les 3 branches de restructuration `src/`, le duplicata `support_assistant/app.py`, et `locate-and-fix-an-important-bug`.

**Aucune fusion n'a été exécutée par cette session** au-delà du test de fusion (`--no-commit`, annulé). Choisir entre des implémentations concurrentes de la même fonctionnalité est une décision de produit/architecture qui revient à Patrick, conformément au prompt maître §6 (« ne demande une décision à Patrick que si elle change matériellement... l'architecture »).

## Méthode

```bash
for b in <chaque branche codex/*>; do
  git rev-list --count main.."origin/$b"          # commits d'écart
  git diff --name-status main..."origin/$b"        # fichiers touchés
  git log -1 --format=%s "origin/$b"                # message du dernier commit
done
git checkout -B _try-merge-pytest origin/main
git merge --no-commit --no-ff origin/codex/set-up-pytest-and-basic-tests   # test de fusion réel
```
