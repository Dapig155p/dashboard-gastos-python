# Importando SQlite
import sqlite3 as lite

# Criando Conexão
con = lite.connect('dados.db')

# Criando Tabela de Categoria
with con:
    cur = con.cursor()
    cur.execute('CREATE TABLE Categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)')

# Criando Tabela de Receitas
with con:
    cur = con.cursor()
    cur.execute('CREATE TABLE Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)')

# Criando Tabela de Gastos
with con:
    cur = con.cursor()
    cur.execute('CREATE TABLE Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)')
