import sqlite3

"""
Esse arquivo contém os códigos da 
abertura e do fechamento da conexão e 
da manipulação das contas e do saldo 
dessas contas
"""

#################################BANCO DE DADOS############################
dataCon=None
#Abre o banco de dados
def get_db():
    global dataCon
    if dataCon != None:
        #Já tem uma conexão
        return dataCon
    else:
        #Não tem conexão
        db = sqlite3.connect("model/dados.db")
        #Armazena na variável global
        dataCon = db
        return db   

#fecha o banco de dados 
def close(db):
    db.close()

#################################CONTA#####################################

#criar uma conta
def cria_conta(nome,tipo):
    con = get_db()
    con.execute("INSERT INTO contas (nome, tipo) VALUES (?,?)", [nome, tipo])
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

#remove uma conta pelo nome
def remove_conta_nome(id):
    con = get_db()
    con.execute("DELETE from contas WHERE id_conta = ?", [id])
    con.commit()

#atualiza o valor do saldo
def atualiza_saldo(idConta):
    #Soma todos os ganhos relacionados a essa conta
    ganhos = retorna_ganhos_id(idConta)
    ganho=0
    if ganhos != None: 
        for item in ganhos:
            ganho += item[1]

    #Soma todos as retiradas relacionados a essa conta
    retiradas = retorna_retiradas_id(idConta)
    retirada=0
    if ganhos != None:
        for item in retiradas:
            retirada += item[1]

    #Calcula o saldo
    saldo = ganho - retirada
    saldo = float(saldo)
    con = get_db()
    con.execute("UPDATE contas SET saldo = ? WHERE id_conta = ?", [saldo, idConta])
    con.commit()

    
#################################MANIPULAÇÕES##############################

#adiciona ganho
def adiciona_ganho(valor, descricao, conta):
    con = get_db()
    con.execute("INSERT INTO ganhos (valor, descricao,id_conta) VALUES (?, ?, ?)", [valor, descricao, conta])
    atualiza_saldo(conta)

#retorna ganhos de uma conta
def retorna_ganhos_id(conta):
    con = get_db()
    return con.execute("SELECT * FROM ganhos WHERE id_conta=?", [conta]).fetchall()

#adiciona retirada
def adiciona_retirada(valor, descricao, conta):
    con = get_db()
    con.execute("INSERT INTO retiradas (valor, descricao,id_conta) VALUES (?, ?, ?)", [valor, descricao, conta])
    atualiza_saldo(conta)

#retorna retiradas de uma conta
def retorna_retiradas_id(conta):
    con = get_db()
    return con.execute("SELECT * FROM retiradas WHERE id_conta=?", [conta]).fetchall()