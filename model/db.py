import sqlite3
from model.G import g

"""
Esse arquivo contém os códigos da 
abertura e do fechamento da conexão e 
da manipulação das contas e do saldo 
dessas contas
"""

#################################BANCO DE DADOS############################

#abre o banco de dados
def get_db():
    if "db" not in g:
        #se a conexão não existir, cria uma nova 
        db = sqlite3.connect("model/dados.db")
        #adiciona a conexão na variável global
        g["db"]=db
    return g["db"]

#fecha o banco de dados 
def close(db):
    db = g.pop('db', None)
    if db is not None:
        db.close()

#################################CONTA#####################################

#criar uma conta
def cria_conta(nome,tipo):
    con = get_db()
    con.execute("INSERT INTO contas VALUES (NULL,?,?,0)", [nome, tipo])
    con.commit()
"""
Tipos:
    1-Dinheiro
    2-Conta bancária
    3-Investimento
"""
#retorna todas as contas cadastradas
def retorna_contas():
    con = get_db()
    return con.execute("SELECT * FROM contas").fetchall()

# #retorna uma conta pelo id
# def retorna_conta_id(id):
#     con = get_db()
#     return con.execute("SELECT * FROM contas WHERE id_conta = ?", [id]).fetchone()

#retorna uma conta pelo nome
def retorna_conta_nome(nome):
    con = get_db()
    return con.execute("SELECT * FROM contas WHERE nome = ?", [nome]).fetchone()

#atualiza o valor do saldo
def atualiza_saldo(valor, id):
    con = get_db()
    con.execute("UPDATE conta SET saldo = ? WHERE id_conta = ?", [valor, id])
    con.commit()

    
#################################MANIPULAÇÕES##############################

#adiciona ganho
def adiciona_ganho(valor, descricao, conta):
    con = get_db()
    con.execute("INSERT INTO ganhos VALUES (NULL, ?, ?)", [valor, descricao, conta])
    atualiza_saldo(valor,conta)

#adiciona retirada
def adiciona_retirada(valor, descricao, conta):
    con = get_db()
    con.execute("INSERT INTO retiradas VALUES (NULL, ?, ?)", [valor, descricao, conta])
    atualiza_saldo(valor,conta)