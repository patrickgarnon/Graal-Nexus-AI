# Guide de configuration

## Configuration des clés API
Créez un fichier `.env` à la racine du projet en vous basant sur `.env.example` et renseignez les clés API nécessaires :
- `SHOPIFY_API_KEY` et `SHOPIFY_PASSWORD`
- `MAKE_API_TOKEN` et `MAKE_SCENARIO_ID`
- `RUNWAY_API_KEY`
- `ELEVENLABS_API_KEY`

## Lancement du serveur
1. Installez les dépendances :
   ```bash
   pip install -r support_assistant/requirements.txt
   ```
2. Assurez-vous que les variables d'environnement sont chargées.
3. Lancez le serveur Flask :
   ```bash
   python support_assistant/app.py
   ```

## Étapes pour Tailwind
1. Installez les dépendances Node et Tailwind :
   ```bash
   npm install -D tailwindcss
   npx tailwindcss init
   ```
2. Générez les fichiers CSS lors du développement :
   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch
   ```
