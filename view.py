# Importando SQlite
import sqlite3 as lite
import pandas as pd

# Criando Conexão
con = lite.connect('dados.db')


#! Funções de Inserir

# Inserir Categoria
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = 'INSERT INTO Categoria (nome) VALUES (?)'
        cur.execute(query,i)


# Inserir Receitas
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = 'INSERT INTO Receitas (categoria, adicionado_em,valor) VALUES (?,?,?)'
        cur.execute(query,i)


# Inserir Gastos
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = 'INSERT INTO Gastos (categoria, retirado_em,valor) VALUES (?,?,?)'
        cur.execute(query,i)

#! Funções Para deletar

# Deletar Receitas
def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = 'DELETE FROM Receitas WHERE id=?'
        cur.execute(query, i)


# Deletar Gastos
def deletar_gastos(i):
    with con:
        cur = con.cursor()
        query = 'DELETE FROM Gastos WHERE id=?'
        cur.execute(query, i)

# Resetar Banco De Dados
def limpar_banco():
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Receitas")
        cur.execute("DELETE FROM Gastos")
        cur.execute("DELETE FROM Categoria")

#! Funções Para Visualizar Dados

# Ver Categoria
def ver_categoria():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Categoria')
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


# Ver Receitas
def ver_receitas():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Receitas')
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


# Ver Gastos
def ver_gastos():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Gastos')
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

# Função para dados da tabela
def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)
    
    return tabela_lista

# Função para ver dados do grafico de bar
def bar_valores():
    # Receita total
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i)


# Função grafico bar
def bar_valores():
    # Receita Total
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)


    # Despesas Total
    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])

    gastos_total = sum(gastos_lista)

    # Saldo Total
    saldo_total = receita_total - gastos_total

    return [receita_total, gastos_total, saldo_total]

# Função Gráfico Pie
def pie_valores():
    gastos = ver_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns = ['id', 'Categoria', 'Data', 'valor'])
    dataframe = dataframe.groupby('Categoria')['valor'].sum()

    lista_quantia = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return([lista_categorias, lista_quantia])
    
# Função percentagem
def percentagem_valor():
    # Receita Total
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)


    # Despesas Total
    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])

    gastos_total = sum(gastos_lista)

    # percentagem Total
    if receita_total <= 0:
        total = 0
    else:
        total = (gastos_total / receita_total) * 100

    return [total]

