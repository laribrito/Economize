import sqlite3

"""
Esse arquivo contém os códigos da 
abertura e do fechamento da conexão e 
da manipulação das contas e do saldo 
dessas contas

This file is part of Economize!.

Economize! is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation, either version 3 of
the License, or any later version.

Economize! is distributed in the hope that 
it will be useful, but WITHOUT ANY WARRANTY; without even the 
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Economize!.  If not, see <https://www.gnu.org/licenses/>.
"""

#################################CONEXÕES############################
import os
#Recebe o caminho onde este arquivo está
app_path = os.path.dirname(os.path.abspath(__file__))

#Seleciona a última pasta
ultima = os.path.basename(os.path.normpath(app_path))

#Remove a última palavra (equivalente a sair de uma pasta)
app_path = app_path.replace(f"/{ultima}", "")

#Repete o processo para sair da pasta do aplicativo 
# e salvar o aquivo de dados fora
ultima = os.path.basename(os.path.normpath(app_path))
app_path = app_path.replace(ultima, "")

dataCon=None
#Abre o banco de dados
def get_db():
    global dataCon
    if dataCon != None:
        #Já tem uma conexão
        return dataCon
    else:
        #Não tem conexão
        db = sqlite3.connect(os.path.join(app_path, 'dados.db'))
        #Armazena na variável global
        dataCon = db
        return db   

#fecha o banco de dados 
def close(db):
    db.close()

#################################BANCO DE DADOS############################

#Tenta criar o arquivo.db, mas se o arquivo já existir
# o programa não faz nada
try:
    conn = sqlite3.connect(os.path.join(app_path, 'dados.db'))
    # definindo um cursor
    cursor = conn.cursor()

    # criando as tabelas
    cursor.execute("""
    CREATE TABLE contas(
        id_conta INTEGER            PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        nome     VARCHAR (50)       NOT NULL UNIQUE,
        tipo     INTEGER            NOT NULL,
        saldo    DECIMAL (18, 2)    NOT NULL DEFAULT (0) 
    );
    """)
    
    cursor.execute("""
    CREATE TABLE ganhos(
        id_ganho    INTEGER       PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        valor       DECIMAL       NOT NULL,
        descricao   VARCHAR (100) NOT NULL,
        id_conta                  REFERENCES contas (id_conta) NOT NULL,
        datahora_br DATETIME      DEFAULT (DATETIME('now', 'localtime')) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE retiradas(
        id_retirada INTEGER       PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        valor       DECIMAL       NOT NULL,
        descricao   VARCHAR (100) NOT NULL,
        id_conta                  REFERENCES contas (id_conta) NOT NULL,
        datahora_br DATETIME      DEFAULT (DATETIME('now', 'localtime')) NOT NULL
    );
    """)



    conn.commit()
    conn.close()
except sqlite3.OperationalError:
    pass

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