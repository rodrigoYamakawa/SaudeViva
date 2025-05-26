from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24) # Necessary for session management and flash messages
DATABASE = '/home/ubuntu/saudeviva_poc/saudeviva.db'

# --- Database Setup ---
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(
'schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- Routes ---
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # In a real app, hash and check password
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()

        if user and user['password'] == password: # WARNING: Plain text password check!
            session['username'] = user['username']
            session['user_id'] = user['id']
            flash('Login bem-sucedido!')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # In a real app, hash password before storing
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            db.commit()
            flash('Usuário registrado com sucesso! Faça o login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe.')
            return redirect(url_for('register'))
        finally:
            db.close()
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Você saiu da sua conta.')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Você precisa fazer login para acessar o dashboard.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = get_db()
    glucose_readings = db.execute(
        'SELECT level, timestamp FROM glucose_readings WHERE user_id = ? ORDER BY timestamp DESC',
        (user_id,)
    ).fetchall()
    db.close()

    # Simulate personalized health tip
    tips = [
        "Lembre-se de verificar sua glicose antes das refeições.",
        "Uma caminhada de 30 minutos pode ajudar a controlar seus níveis de açúcar.",
        "Priorize alimentos integrais e evite açúcares processados.",
        "Beba bastante água ao longo do dia.",
        "Monitore seus pés diariamente para evitar complicações."
    ]
    health_tip = random.choice(tips)

    # Convert timestamp strings to datetime objects for formatting in template
    formatted_readings = []
    for reading in glucose_readings:
        try:
            # Assuming timestamp is stored as ISO format string or similar
            dt_object = datetime.fromisoformat(reading['timestamp'])
        except ValueError:
             # Fallback if format is different or already a datetime object (less likely with sqlite3)
             # This might need adjustment based on how timestamps are actually stored/retrieved
             dt_object = datetime.now() # Placeholder, adjust as needed

        formatted_readings.append({'level': reading['level'], 'timestamp': dt_object})


    return render_template('dashboard.html', username=session['username'], glucose_readings=formatted_readings, health_tip=health_tip)

@app.route('/add_glucose', methods=['POST'])
def add_glucose():
    if 'username' not in session:
        flash('Sessão expirada. Faça login novamente.')
        return redirect(url_for('login'))

    try:
        level = int(request.form['glucose_level'])
        timestamp_str = request.form['timestamp'] # Comes from datetime-local input
        # Convert local datetime string to a standardized format if needed, e.g., ISO
        # For simplicity, storing as string provided by input
        timestamp = timestamp_str
        user_id = session['user_id']

        db = get_db()
        db.execute('INSERT INTO glucose_readings (user_id, level, timestamp) VALUES (?, ?, ?)',
                   (user_id, level, timestamp))
        db.commit()
        db.close()
        flash('Nível de glicose registrado com sucesso!')
    except ValueError:
        flash('Nível de glicose inválido.')
    except Exception as e:
        flash(f'Erro ao registrar glicose: {e}')

    return redirect(url_for('dashboard'))

# --- Schema for DB Initialization ---
# (Content for schema.sql)
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL
# );
#
# CREATE TABLE IF NOT EXISTS glucose_readings (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER NOT NULL,
#     level INTEGER NOT NULL,
#     timestamp TEXT NOT NULL, -- Store as ISO format string or TEXT from datetime-local
#     FOREIGN KEY (user_id) REFERENCES users (id)
# );

if __name__ == '__main__':
    # Create schema.sql if it doesn't exist
    schema_path = '/home/ubuntu/saudeviva_poc/src/schema.sql'
    if not os.path.exists(schema_path):
        schema_content = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL -- WARNING: Storing plain text passwords!
        );

        CREATE TABLE IF NOT EXISTS glucose_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            level INTEGER NOT NULL,
            timestamp TEXT NOT NULL, -- Storing as TEXT from datetime-local input
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        with open(schema_path, 'w') as f:
            f.write(schema_content)
        print(f"Created {schema_path}")

    # Initialize DB if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()
        print(f"Initialized database at {DATABASE}")

    # Run the app
    # Listen on 0.0.0.0 to be accessible externally if needed (e.g., via deploy_expose_port)
    app.run(host='0.0.0.0', port=5000, debug=True)

