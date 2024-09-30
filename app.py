from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

app = Flask(__name__)
app.secret_key = 'la_tua_chiave_segreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modello utente
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Caricamento dell'utente
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Logica di verifica delle credenziali (per il test usiamo credenziali fisse)
        if username == 'admin' and password == 'password':
            user = User(id=1)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenziali non valide')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/process_url', methods=['POST'])
@login_required
def process_url():
    ads_url = request.form['ads_url']
    # Validazione dell'URL
    if not ads_url.startswith('http'):
        return render_template('dashboard.html', error='URL non valido')
    # Passa l'URL alla funzione che simula il recupero e l'elaborazione dei dati
    data = retrieve_and_process_data(ads_url)
    return render_template('results.html', data=data)
import urllib.parse

def retrieve_and_process_data(ads_url):
    # Parsing dell'URL per estrarre parametri (simulato)
    parsed_url = urllib.parse.urlparse(ads_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    search_query = query_params.get('q', [''])[0]
    
    # Simulazione del comportamento in base ai parametri estratti
    # Ad esempio, utilizziamo il parametro 'q' per personalizzare i dati fittizi
    data = generate_mock_data(search_query)
    return data

def generate_mock_data(search_query):
    # Dati fittizi di esempio
    mock_data = [
        {
            'nome_pagina': 'Brand Alpha',
            'numero_inserzioni': 10,
            'sito_web': 'https://www.brandalpha.com',
            'data_pubblicazione': '2023-10-01'
        },
        {
            'nome_pagina': 'Brand Beta',
            'numero_inserzioni': 7,
            'sito_web': 'https://www.brandbeta.com',
            'data_pubblicazione': '2023-09-25'
        },
        {
            'nome_pagina': 'Brand Gamma',
            'numero_inserzioni': 5,
            'sito_web': 'https://www.brandgamma.com',
            'data_pubblicazione': '2023-09-15'
        }
    ]
    # Se c'è una query di ricerca, filtra i dati fittizi
    if search_query:
        filtered_data = [item for item in mock_data if search_query.lower() in item['nome_pagina'].lower()]
        return filtered_data
    return mock_data



if __name__ == '__main__':
    app.run(debug=True)
