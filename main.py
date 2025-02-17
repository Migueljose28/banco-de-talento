from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

app.secret_key = 'admin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

lm = LoginManager(app)
lm.login_view = 'login'


#FUNÇÕES DE VALIDAÇÃO
def hash_senha(senha):
    return generate_password_hash(senha)

def verificar_senha(senha, senha_hash):
    return check_password_hash(senha_hash, senha)

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_cpf(cpf):
    return len(cpf) == 14

def validar_senha(senha):
    return len(senha) >= 6


#FUNÇÃO PARA CARREGAR USUÁRIOS
from models import User
@lm.user_loader
def load_user(id):
    return db.session.query(User).filter_by(id=id).first()


#ROTA PRINCIPAL
@app.route('/')
@login_required
def index():
    return render_template('index.html', usuario=current_user)


#ROTA DE USUÁRIOS
from flask import jsonify
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = db.session.query(User).all()
    usuarios_data = [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]
    return jsonify(usuarios_data)


#ROTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']
        usuario_login = db.session.query(User).filter_by(nome=nome).first()

        if usuario_login and verificar_senha(senha, usuario_login.senha):
            login_user(usuario_login)
            return redirect(url_for('index'))
        else:
            mensagem = "Usuário ou senha inválidos, tente novamente."
            return render_template("login.html", mensagem=mensagem)

#ROTA DE REGISTRO
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']
        email = request.form['emailForm']
        telefone = request.form['telefoneForm']
        cpf = request.form['cpfForm']

        if not validar_email(email):
            mensagem = "E-mail inválido."
            return render_template('registrar.html', mensagem=mensagem)

        if not validar_cpf(cpf):
            mensagem = "CPF inválido."
            return render_template('registrar.html', mensagem=mensagem)

        if not validar_senha(senha):
            mensagem = "Senha muito curta, deve ter pelo menos 6 caracteres."
            return render_template('registrar.html', mensagem=mensagem)

        user_existente = User.query.filter_by(email=email, telefone=telefone, cpf=cpf).first()
        if user_existente:
            mensagem = "Usuário já existente! Escolha outro e-mail."
            return render_template('registrar.html', mensagem=mensagem)

        user = User(nome=nome, senha=hash_senha(senha), email=email, telefone=telefone, cpf=cpf)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))

#ROTA DE LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)