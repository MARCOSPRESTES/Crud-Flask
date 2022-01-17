#CRUD FLASK COM SQLALCHEMY
#IMPORTS
from flask import Flask, render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, scoped_session


app = Flask(__name__, template_folder='templates')
#CONFIGURA CONEXÃO COM BANCO DE DADOS.
engine = create_engine('mssql+pymssql://sa:Ma123456$@localhost:1433/CRUDF')
session = scoped_session(sessionmaker(autocommit=False, bind=engine))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:Ma123456$@localhost:1433/CRUDF'

db = SQLAlchemy(app)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto = db.Column(db.String(255))
    descricao = db.Column(db.String(255))
    valor = db.Column(db.Float)

    def __init__(self, produto, descricao, valor):
        self.produto = produto
        self.descricao = descricao
        self.valor = valor


@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        produto=Produto(request.form['produto'], request.form['descricao'], request.form['valor'])
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.produto = request.form['produto']
        produto.descricao = request.form['descricao']
        produto.valor = request.form['valor']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', produto=produto)


@app.route('/delete/<int:id>')
def delete(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))





if __name__=='__main__':
    db.create_all()
    app.run(debug=True)