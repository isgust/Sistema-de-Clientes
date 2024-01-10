from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)


app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")


#Configuração do banco de dados
DATABASE =os.path.join(os.path.dirname(__file__), 'clientes.db')

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor =  conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL    
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS ADM (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    
    cursor.execute('INSERT INTO ADM (username, password) VALUES (?, ?)', ('user', '123'))
    conn.commit()
    conn.close()
    print(" Tabela criada com sucesso")
    


create_table()


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ADM WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('cadastro'))
        else:
            error = "Dados invalidos"
            return render_template('index.html', error=error)

    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/clientes')
def listar_clientes():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    print("Clientes Cadastrados:", clientes)
    for cliente in clientes:
        print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, Email: {cliente['email']}, Telefone; {cliente['telefone']}")
    return render_template('listar_clientes.html', clientes=clientes)

@app.route('/cadastrar', methods=['POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
            conn.commit()
            print(f"Cliente cadastrado - Nome: {nome}, Email: {email}, Telefone: {telefone}")
        except Exception as e:
            conn.rollback()
            print(f"Erro durante o cadastro: {e}")
        finally:
            conn.close()
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
        
        
     
