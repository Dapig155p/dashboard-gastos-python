import customtkinter as ctk
from customtkinter import CTkProgressBar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from CTkMessagebox import CTkMessagebox
from tkcalendar import Calendar, DateEntry
from datetime import date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from PIL import Image, ImageTk
from view import bar_valores, limpar_banco, percentagem_valor, inserir_categoria, inserir_gastos, inserir_receita, ver_categoria, ver_gastos, ver_receitas, tabela, deletar_gastos, deletar_receitas, pie_valores


ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

#! Criando Janela

janela = ctk.CTk()
janela.title("Dashboard de Gastos Pessoais by: Santiago") 
janela.geometry('900x650')
janela.configure(fg_color="#1a1a1a") 
janela.resizable(width=False, height=False)
style = ttk.Style(janela)
style.theme_use('clam')

#! Criando Frames Para Divisão da Tela

frameCima = ctk.CTkFrame(janela, width=1043, height=50, fg_color='#222222', corner_radius=0)
frameCima.grid(row=0, column=0, sticky="nsew")

frameMeio = ctk.CTkFrame(janela, width=1043, height=361, fg_color='#222222', corner_radius=0)
frameMeio.grid(row=1, column=0, sticky="nsew", pady=2, padx=0)

frameBaixo = ctk.CTkFrame(janela, width=1043, height=300, fg_color="#222222", corner_radius=0)
frameBaixo.grid(row=2, column=0, sticky="nsew", pady=0, padx=10)


#! Trabalhando no Frame Cima

# Acessando a Imagem
app_img = ctk.CTkImage(light_image=Image.open('dashicon.png'), dark_image=Image.open('dashicon.png'), size=(45, 45))
app_logo = ctk.CTkLabel(frameCima, image=app_img, text=' Planilha de Gastos Mensais', compound='left', padx=10, anchor='nw', font=('Verdana', 20, 'bold'), fg_color="transparent")
app_logo.place(x=10, y=5)


global tree
# Função Inserir Categoria
def inserir_categoria_b():
    nome = e_categoria.get()
    lista_inserir = [nome]

    if nome == '':
        CTkMessagebox(
            title="Erro de Entrada",
            message="Preencha todos os campos para continuar!",
            icon="cancel",          
            option_1="Entendido",
            button_color="#5C40C4",  
            button_hover_color="#8A2BE2",
            bg_color="#1a1a1a",      
            fg_color="#222222"
        )
        return # Aqui ele para se estiver vazio.

    # ESTAS LINHAS ABAIXO DEVEM FICAR NA MESMA DIREÇÃO DO "if"
    # Inserindo os dados no banco
    inserir_categoria(lista_inserir)
    
    CTkMessagebox(
        title="Sucesso", 
        message="Os dados foram inseridos com sucesso.",
        icon="check", 
        option_1="OK",
        button_color="#40C461",
        bg_color="#1a1a1a", 
        fg_color="#222222"
    )

    e_categoria.delete(0, 'end')

    # Atualizando o ComboBox
    categorias_função = ver_categoria()
    categoria = [i[1] for i in categorias_função] 
    combo_categoria_despesas.configure(values=categoria) # Use .configure para garantir a atualização

# Função inserir receitas
def inserir_receitas_b():
    nome = 'Receita'
    data = e_cal_receitas.get()
    quantia = e_valor_receitas.get()

    lista_inserir = [nome, data, quantia]

    
    if data == '' or quantia == '':
        CTkMessagebox(
            title="Erro de Entrada",
            message="Preencha todos os campos para continuar!",
            icon="cancel",          
            option_1="Entendido",
            button_color="#5C40C4",  
            button_hover_color="#8A2BE2",
            bg_color="#1a1a1a",      
            fg_color="#222222"
        )
        return

    
    inserir_receita(lista_inserir)

    
    CTkMessagebox(
        title="Sucesso", 
        message="Os dados foram inseridos com sucesso.",
        icon="check", 
        option_1="OK",
        button_color="#40C461",
        bg_color="#1a1a1a", 
        fg_color="#222222"
    )

    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')


    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()


# Função inserir despesas
def inserir_despesas_b():
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    quantia = e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    
    if data == '' or quantia == '':
        CTkMessagebox(
            title="Erro de Entrada",
            message="Preencha todos os campos para continuar!",
            icon="cancel",          
            option_1="Entendido",
            button_color="#5C40C4",  
            button_hover_color="#8A2BE2",
            bg_color="#1a1a1a",      
            fg_color="#222222"
        )
        return

    
    inserir_gastos(lista_inserir)

    
    CTkMessagebox(
        title="Sucesso", 
        message="Os dados foram inseridos com sucesso.",
        icon="check", 
        option_1="OK",
        button_color="#40C461",
        bg_color="#1a1a1a", 
        fg_color="#222222"
    )

    combo_categoria_despesas.set("Selecione...")
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    
    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()

# Função Deletar
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        
        # Se a lista estiver vazia força o erro
        if not treev_lista:
            raise IndexError

        valor = treev_lista[0]
        nome = treev_lista[1]

        # Criando uma caixa de confirmação antes de deletar
        pergunta = CTkMessagebox(
            title="Confirmar Exclusão",
            message=f"Deseja realmente deletar: {nome}?",
            icon="question",
            option_1="Não",
            option_2="Sim",
            button_color="#5C40C4",
            bg_color="#1a1a1a",
            fg_color="#222222"
        )

        if pergunta.get() == "Sim":
            if nome == 'Receita':
                deletar_receitas([valor])
            else:
                deletar_gastos([valor])

            # Mensagem de Sucesso
            CTkMessagebox(
                title="Sucesso", 
                message="Os dados foram deletados com sucesso.",
                icon="check", 
                option_1="OK",
                button_color="#40C461",
                bg_color="#1a1a1a", 
                fg_color="#222222"
            )

            # Atualizando Dados do Dashboard
            mostrar_renda()
            percentagem()
            grafico_bar()
            resumo()
            grafico_pie()

    except IndexError:
        CTkMessagebox(
            title="Erro de Seleção",
            message="Selecione um dos dados na tabela para excluir.",
            icon="cancel",          
            option_1="Entendido",
            button_color="#5C40C4",  
            bg_color="#1a1a1a",      
            fg_color="#222222"
        )
        

def reset_mensal():
    confirmar = CTkMessagebox(
        title="Reset Mensal",
        message="Deseja limpar todos os dados da Tabela?",
        icon="warning",
        option_1="Cancelar",
        option_2="Limpar Tudo",
        button_color="#EB2F0E", 
        bg_color="#1a1a1a",
        fg_color="#222222"
    )

    if confirmar.get() == "Limpar Tudo":
        
        limpar_banco()
        
        CTkMessagebox(title="Sucesso", message="Banco de dados resetado!", icon="check")
        
        mostrar_renda()
        percentagem()
        grafico_bar()
        resumo()
        grafico_pie()
 

img_reset = ctk.CTkImage(light_image=Image.open('deletar.png'), dark_image=Image.open('deletar.png'), size=(20, 20))

botao_reset = ctk.CTkButton(
    frameCima, 
    image=img_reset,
    text='', 
    width=40,       
    height=40,       
    corner_radius=15, 
    fg_color="transparent", 
    hover_color="#EB2F0E",
    anchor="center",
    command=reset_mensal
)

botao_reset.place(x=840, y=5)


#! Percentagem

def percentagem():
    l_nome = ctk.CTkLabel(frameMeio, text='Porcentagem de Gasto da Receita', height=1, anchor='nw', font=('Verdana', 12), fg_color='transparent')
    l_nome.place(x=7, y=15)

    bar = ctk.CTkProgressBar(frameMeio, width=190, height=25, corner_radius=0, progress_color='#5C40C4')
    bar.place(x=10, y=35)
    valor = percentagem_valor()[0]
    bar.set(valor / 100)

    l_percentagem = ctk.CTkLabel(frameMeio, text=f'{valor:,.2f}%', anchor='nw', font=('Verdana', 12), fg_color='transparent')
    l_percentagem.place(x=75, y=65)
    
# Função Para Gráfico Bars
def grafico_bar():
    
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()
    cores = ["#8A2BE2", "#A020F0", "#BF94FF"] 

    figura = plt.Figure(figsize=(4, 3.45), dpi=60, facecolor='#222222')
    ax = figura.add_subplot(111)
    ax.set_facecolor('#222222') 

    
    ax.bar(lista_categorias, lista_valores, color=cores, width=0.9)

    c = 0
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2, i.get_height() + 100,
                f'R$ {lista_valores[c]:,.0f}',
                ha='center', fontsize=12, color='white', fontstyle='italic')
        c += 1

    
    ax.tick_params(axis='x', colors='white', labelsize=12) 
    ax.tick_params(axis='y', colors='white') 
    
    
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.yaxis.grid(False) 
    ax.xaxis.grid(False)

    
    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=80) 
   
# Função de Resumo total
def resumo():
    valor = bar_valores()

    l_linha = ctk.CTkLabel(frameMeio, text='', width=215, height=2, fg_color="#5C40C4")
    l_linha.place(x=309, y=55)

    l_sumario = ctk.CTkLabel(frameMeio, text='TOTAL RENDA MENSAL      ', anchor='nw', font=('Verdana', 17, 'bold'), fg_color='transparent', text_color='white')
    l_sumario.place(x=309, y=38)

    l_sumario = ctk.CTkLabel(frameMeio, text=f'R$ {valor[0]:,.2f}', anchor='nw', font=('arial', 20), fg_color='transparent', text_color='white')
    l_sumario.place(x=309, y=80)

    #--------------------------------------------------------

    l_linha = ctk.CTkLabel(frameMeio, text='', width=265, height=2, fg_color="#5C40C4")
    l_linha.place(x=309, y=132)

    l_sumario = ctk.CTkLabel(frameMeio, text='TOTAL DESPESAS MENSAIS ', anchor='nw', font=('Verdana', 17, 'bold'), fg_color='transparent', text_color='white')
    l_sumario.place(x=309, y=115)

    l_sumario = ctk.CTkLabel(frameMeio, text=f'R$ {valor[1]:,.2f}', anchor='nw', font=('arial', 20), fg_color='transparent', text_color='white')
    l_sumario.place(x=309, y=155)

    #-------------------------------------------------------------

    l_linha = ctk.CTkLabel(frameMeio, text='', width=245, height=2, fg_color="#5C40C4")
    l_linha.place(x=309, y=207)

    l_sumario = ctk.CTkLabel(frameMeio, text='TOTAL SALDO DA CAIXA      ', anchor='nw', font=('Verdana', 17, 'bold'), fg_color='transparent', text_color='white')
    l_sumario.place(x=309, y=190)

    l_sumario = ctk.CTkLabel(frameMeio, text=f'R$ {valor[2]:,.2f}', anchor='nw', font=('arial', 20), fg_color='transparent', text_color='white')
    l_sumario.place(x=309, y=230)

# Função Grafico de pizza

frame_gra_pie = ctk.CTkFrame(frameMeio, width=580, height=250)
frame_gra_pie.place(x=445, y=5)

def grafico_pie():
    figura = plt.Figure(figsize=(5, 3), dpi=90, facecolor='#222222')
    ax = figura.add_subplot(111)
    ax.set_facecolor('#222222')

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]
    cores_pie = ['#8A2BE2', '#A020F0', '#5865F2']

    explode = [0.05] * len(lista_categorias)

    wedges, texts, autotexts = ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.3), autopct='%1.1f%%', colors=cores_pie, shadow=True, startangle=90)

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')

    legenda = ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))
    legenda.get_frame().set_facecolor('#222222')
    legenda.get_frame().set_edgecolor('#5C40C4')
    for text in legenda.get_texts():
        text.set_color('white')

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)


# Criando Frames dentro do Frame Baixo
frame_renda = ctk.CTkFrame(frameBaixo, width=300, height=250, fg_color='#222222')
frame_renda.grid(row=0, column=0)

frame_operaçoes = ctk.CTkFrame(frameBaixo, width=220, height=250, fg_color='#222222')
frame_operaçoes.grid(row=0, column=1, padx=5)

frame_configuração= ctk.CTkFrame(frameBaixo, width=220, height=250, fg_color='#222222')
frame_configuração.grid(row=0, column=2, padx=5)


#! Tabela Renda Mensal

# Criando Legenda
app_tabela = ctk.CTkLabel(frameMeio, text='Tabela Receitas e Despesas', anchor='nw', font=('Verdana', 17), fg_color="transparent")
app_tabela.place(x=15, y=330)

# Função Para mostrar renda
def mostrar_renda():
    tabela_head = ['#Id','Categoria','Data','Quantia']
    lista_itens = tabela()
    global tree

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#222222", foreground="white", rowheight=30, fieldbackground="#222222", borderwidth=0)
    style.map('Treeview', background=[('selected', '#5C40C4')]) 
    style.configure("Treeview.Heading", background="#1a1a1a", foreground="#BF94FF", relief="flat", font=('Verdana', 10, 'bold'))

    tree = ttk.Treeview(frame_renda, selectmode="extended", columns=tabela_head, show="headings", height=7)
    
    tree.grid(column=0, row=0, sticky='ew', padx=20, pady=(5, 10))
    
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    vsb.grid(column=1, row=0, sticky='ns', pady=(5, 10)) 
    
    tree.configure(yscrollcommand=vsb.set)

    hd=["center", "center", "center", "center"]
    h=[40, 120, 100, 100] 
    
    for n, col in enumerate(tabela_head):
        tree.heading(col, text=col.title(), anchor='center')
        tree.column(col, width=h[n], anchor=hd[n])
        
    for item in lista_itens:
        tree.insert('', 'end', values=item)


#! Configurações Despesas

l_info = ctk.CTkLabel(frame_operaçoes, text='Insira Novas Despesas', height=1, anchor='nw', font=('Verdana', 13, 'bold'))
l_info.place(x=10, y=10)

# Categoria 

l_categoria = ctk.CTkLabel(frame_operaçoes, text='Categoria', height=1, anchor='nw', font=('Ivy', 13, 'bold'))
l_categoria.place(x=10, y=40)

# Pegando Categorias
categoria_função = ver_categoria()
categoria = []

for i in categoria_função:
    categoria.append(i[1])

combo_categoria_despesas = ctk.CTkComboBox(frame_operaçoes, width=110, font=('Ivy', 10), values=[""])
combo_categoria_despesas['values'] = (categoria if categoria else [""])
combo_categoria_despesas.set("Selecione...")
combo_categoria_despesas.place(x=80, y=36)

# Calendario despesas
l_cal_despesas = ctk.CTkLabel(frame_operaçoes, text='Data', height=1, anchor='nw', font=('Ivy', 13, 'bold'))
l_cal_despesas.place(x=10, y=70)

e_cal_despesas = DateEntry(frame_operaçoes, width=15, background='#5C40C4', foreground='white', borderwidth=2, locale='pt_BR')
e_cal_despesas.place(x=80, y=71)

# Valor
l_valor_despesas = ctk.CTkLabel(frame_operaçoes, text='Quantia Total', height=1, anchor='nw', font=('Ivy', 11, 'bold'))
l_valor_despesas.place(x=3, y=100)

e_valor_despesas = ctk.CTkEntry(frame_operaçoes, width=115, height=1)
e_valor_despesas.place(x=80, y=97)

# Botão Inserir
img_add_despesas = ctk.CTkImage(light_image=Image.open('add.png'), dark_image=Image.open('add.png'), size=(20, 20))

botao_inserir_despesas = ctk.CTkButton(
    frame_operaçoes, 
    image=img_add_despesas, 
    text='ADICIONAR', 
    compound='left', 
    command=inserir_despesas_b,
    font=('Ivy', 10, 'bold'), 
    fg_color="#40C461",     
    hover_color="#3F961D",   
    width=50,               
    height=20,              
    corner_radius=10,        
    text_color="white"
)
botao_inserir_despesas.place(x=80, y=125)

# Botão Excluir
l_excluir = ctk.CTkLabel(frame_operaçoes, text='Excluir Ação', height=1, anchor='nw', font=('Ivy', 11, 'bold'))
l_excluir.place(x=3, y=195)

img_delete = ctk.CTkImage(light_image=Image.open('deletar.png'), dark_image=Image.open('deletar.png'), size=(20, 20))

botao_deletar = ctk.CTkButton(
    frame_operaçoes, 
    image=img_delete, 
    text='DELETAR', 
    command=deletar_dados,
    compound='left', 
    font=('Ivy', 10, 'bold'), 
    fg_color="#EB2F0E",     
    hover_color="#8D3B22",   
    width=50,               
    height=20,              
    corner_radius=10,        
    text_color="white"
)
botao_deletar.place(x=80, y=190)


#! Configurações Receitas

l_info = ctk.CTkLabel(frame_configuração, text='Insira Novas Receitas', height=1, anchor='nw', font=('Verdana', 13, 'bold'))
l_info.place(x=10, y=10)

# Calendario Receitas
l_cal_receitas = ctk.CTkLabel(frame_configuração, text='Data', height=1, anchor='nw', font=('Ivy', 13, 'bold'))
l_cal_receitas.place(x=10, y=40)

e_cal_receitas = DateEntry(frame_configuração, width=15, background='#5C40C4', foreground='white', borderwidth=2, locale='pt_BR')
e_cal_receitas.place(x=80, y=41)

# Valor
l_valor_receitas = ctk.CTkLabel(frame_configuração, text='Quantia Total', height=1, anchor='nw', font=('Ivy', 11, 'bold'))
l_valor_receitas.place(x=3, y=74)

e_valor_receitas = ctk.CTkEntry(frame_configuração, width=125, height=1)
e_valor_receitas.place(x=80, y=71)

# Botão Inserir
img_add_receitas = ctk.CTkImage(light_image=Image.open('add.png'), dark_image=Image.open('add.png'), size=(20, 20))

botao_inserir_receitas = ctk.CTkButton(
    frame_configuração, 
    image=img_add_receitas, 
    text='ADICIONAR', 
    command=inserir_receitas_b,
    compound='left', 
    font=('Ivy', 10, 'bold'), 
    fg_color="#40C461",     
    hover_color="#3F961D",   
    width=50,               
    height=20,              
    corner_radius=10,        
    text_color="white"
)
botao_inserir_receitas.place(x=80, y=111)

# Nova Categoria
l_info = ctk.CTkLabel(frame_configuração, text='Categoria', height=1, anchor='nw', font=('Ivy', 13, 'bold'))
l_info.place(x=10, y=163)

e_categoria = ctk.CTkEntry(frame_configuração, width=125, height=1)
e_categoria.place(x=80, y=160)

# Botão Inserir
img_add_categoria = ctk.CTkImage(light_image=Image.open('add.png'), dark_image=Image.open('add.png'), size=(20, 20))

botao_inserir_categoria = ctk.CTkButton(
    frame_configuração, 
    image=img_add_categoria, 
    text='ADICIONAR',
    command=inserir_categoria_b,
    compound='left', 
    font=('Ivy', 10, 'bold'), 
    fg_color="#40C461",     
    hover_color="#3F961D",   
    width=50,               
    height=20,              
    corner_radius=10,        
    text_color="white"
)
botao_inserir_categoria.place(x=80, y=190)


 
categorias_função = ver_categoria()
categoria = [i[1] for i in categorias_função] 
combo_categoria_despesas.configure(values=categoria)
mostrar_renda()
grafico_pie()
grafico_bar()
percentagem()
resumo()
janela.mainloop()