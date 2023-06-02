import tkinter as tk
import urllib.request
import sqlite3


connection = sqlite3.connect('urls.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT
    )
''')

def resetar_tela():
    tela_formulario.pack_forget()
    tela_boas_vindas.pack()

def exibir_formulario():
    tela_boas_vindas.pack_forget()
    tela_formulario.pack()
    listar_urls() 

def adicionar_url():
    url = entrada_url.get()
    if url:
        if validar_url(url):
            cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
            entrada_url.delete(0, tk.END)
            connection.commit()
            listar_urls()
        else:
            # Menssagem de error, url invalido
            print("URL Invalida")

def listar_urls():
    lista_urls.delete(0, tk.END)
    cursor.execute('SELECT url FROM urls')
    urls = cursor.fetchall()
    for url in urls:
        lista_urls.insert(tk.END, url[0])

def alterar_url():
    url_selecionada = lista_urls.curselection()
    if url_selecionada:
        nova_url = entrada_url.get()
        if nova_url:
            cursor.execute('UPDATE urls SET url=? WHERE id=?', (nova_url, url_selecionada[0] + 1))
            entrada_url.delete(0, tk.END)
            connection.commit()
            listar_urls()

def excluir_url():
    url_selecionada = lista_urls.curselection()
    if url_selecionada:
        cursor.execute('DELETE FROM urls WHERE id=?', (url_selecionada[0] + 1,))
        connection.commit()
        listar_urls()

def validar_url(url):
    try:
        urllib.request.urlopen(url)
        return True
    except urllib.request.URLError:
        return False

def validar_todas_urls():
    cursor.execute('SELECT url FROM urls')
    urls = cursor.fetchall()
    for url in urls:
        if validar_url(url[0]):
            print(f"{url[0]} is valid")
        else:
            print(f"{url[0]} is invalid")

janela = tk.Tk()
janela.geometry("1024x1080")
janela.configure(background='pink')

tela_boas_vindas = tk.Frame(janela)
tela_boas_vindas.configure(background="pink")
tela_boas_vindas.pack()


rotulo_boas_vindas = tk.Label(
    tela_boas_vindas, text="Bem-vindo! Aqui você poderá: Incluir, Alterar, Adicionar, Listar e Validar URLs", bg='pink', font=(12))
rotulo_boas_vindas.pack(pady=300)


botao_formulario = tk.Button(
    tela_boas_vindas, text="Ir para Pagina de URLs", command=exibir_formulario, bg='black', fg='pink', font=(12))
botao_formulario.pack()

tela_formulario = tk.Frame(janela)
tela_formulario.configure(background='pink')


rotulo_url = tk.Label(tela_formulario, text="URL:",
                      background='pink', font=(20))
rotulo_url.pack(pady=30)


entrada_url = tk.Entry(tela_formulario)
entrada_url.configure(width=60, font=(20))
entrada_url.pack()


botao_adicionar = tk.Button(
    tela_formulario, text="Adicionar URL", command=adicionar_url, bg='black', fg='pink', font=(12))
botao_adicionar.pack(pady=20)


rotulo_lista_urls = tk.Label(
    tela_formulario, text="URLs cadastradas:", background='pink', font=(12))
rotulo_lista_urls.pack(pady=10)


lista_urls = tk.Listbox(tela_formulario)
lista_urls.configure(width=90)
lista_urls.pack()


botao_alterar = tk.Button(
    tela_formulario, text="Alterar URL", command=alterar_url, bg='black', fg='pink', font=(12))
botao_alterar.pack(side='left', padx=10, pady=5)


botao_excluir = tk.Button(
    tela_formulario, text="Excluir URL", command=excluir_url, bg='black', fg='pink', font=(12))
botao_excluir.pack(side='left', pady=20)


botao_validar = tk.Button(
    tela_formulario, text="Validar URL", command=validar_url, bg='black', fg='pink', font=(12))
botao_validar.pack(side='right', pady=20)


botao_validar_todas = tk.Button(
    tela_formulario, text="Validar todas as URL", command=validar_todas_urls, bg='black', fg='pink', font=(12))
botao_validar_todas.pack(side='right', padx=10, pady=20)


urls_cadastradas = [] 

janela.mainloop()
connection.close()