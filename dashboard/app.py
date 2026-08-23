import os

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/shopify')
def shopify():
    return render_template('shopify.html', title='Shopify')


@app.route('/make')
def make():
    return render_template('make.html', title='Make')


@app.route('/runway')
def runway():
    return render_template('runway.html', title='Runway')


@app.route('/elevenlabs')
def elevenlabs():
    return render_template('elevenlabs.html', title='ElevenLabs')


if __name__ == '__main__':
    # Le mode debug de Flask active un débogueur interactif qui permet
    # l'exécution de code arbitraire si le port est jamais exposé au-delà
    # de localhost. Désactivé par défaut ; à activer explicitement en
    # développement seulement via FLASK_DEBUG=1.
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode)
