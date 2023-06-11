import tkinter as tk
import requests
import socket
import urllib.parse
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

def exibir_telaUrl():
    tela_boas_vindas.pack_forget()
    tela_url.pack()
       
def resetar_tela():
    tela_url.pack_forget()
    tela_boas_vindas.pack()
    
def exibir_telas():
    tela_boas_vindas.pack_forget()
    tela_url.pack()

def adicionar_url():
    url = entry_url.get()
    if validar_url(url):
        inserir_url(url)
        exibir_urls()
        entry_url.delete(0, tk.END)

def alterar_url():
    selected_index = listbox_urls.curselection()
    if selected_index:
        new_url = entry_url.get()
        if validar_url(new_url):
            url_id = listbox_urls.get(selected_index)[0]
            atualizar_url(url_id, new_url)
            exibir_urls()
            entry_url.delete(0, tk.END)

def excluir_url():
    selected_index = listbox_urls.curselection()
    if selected_index:
        url_id = listbox_urls.get(selected_index)[0]
        excluir_url_db(url_id)
        exibir_urls()

def validar_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def validar_urls():
    historico_urls_validas = []
    historico_urls_invalidas = []
    
    for url in listbox_urls.get(0, tk.END):
        if validar_url(url[1]):
            historico_urls_validas.append(url[1])
        else:
            historico_urls_invalidas.append(url[1])
    
    messagebox.showinfo("Histórico de URLs", f"URLs válidas:\n{historico_urls_validas}\n\nURLs inválidas:\n{historico_urls_invalidas}")

    # Abre a tela de detalhes quando o botão "Detalhes" é clicado
    selected_index = listbox_urls.curselection()
    if selected_index:
        url = listbox_urls.get(selected_index)[1]
        exibir_detalhes(url)

def importar_urls():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            urls = file.readlines()
            for url in urls:
                url = url.strip()
                if url:
                    if validar_url(url):
                        inserir_url(url)
                    else:
                        print(f"URL inválida: {url}")
        exibir_urls()

def criar_tabela():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT)"
    )
    conn.commit()
    conn.close()

def inserir_url(url):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()

def excluir_url_db(url_id):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE id=?", (url_id,))
    conn.commit()
    conn.close()

def atualizar_url(url_id, new_url):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET url=? WHERE id=?", (new_url, url_id))
    conn.commit()
    conn.close()

def exibir_urls():
    listbox_urls.delete(0, tk.END)
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls")
    urls = cursor.fetchall()
    for url in urls:
        listbox_urls.insert(tk.END, url)
    conn.close()

    # Adiciona o botão "Detalhes"
    button_detalhes = tk.Button(window, text="Detalhes", command=validar_urls, bg='black', fg='pink', font=(12))
    button_detalhes.pack()

def exibir_detalhes(url):
    # Realiza a validação da URL
    if not validar_url(url):
        messagebox.showerror("Erro", "URL inválida")
        return
    
    # Obtém o tempo de resposta da conexão
    try:
        response = requests.get(url)
        tempo_resposta = response.elapsed.total_seconds()
    except requests.exceptions.RequestException:
        messagebox.showerror("Erro", "Não foi possível obter o tempo de resposta da conexão")
        return
    
    # Obtém o endereço IP do servidor que respondeu à validação
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        endereco_ip = socket.gethostbyname(host)
    except:
        messagebox.showerror("Erro", "Não foi possível obter o endereço IP do servidor")
        return
    
    # Obtém o cabeçalho devolvido
    cabeçalho = response.headers
    
    # Exibe os detalhes em uma nova janela
    detalhes_window = tk.Toplevel(window)
    detalhes_window.title("Detalhes da Conexão")
    detalhes_window.geometry("400x300")
    detalhes_window.configure(background='pink')
    
    # Cria os rótulos para exibir os detalhes
    label_tempo_resposta = tk.Label(detalhes_window, text="Tempo de Resposta: {:.2f} segundos".format(tempo_resposta), background='pink', font=(12))
    label_tempo_resposta.pack(pady=10)
    
    label_endereco_ip = tk.Label(detalhes_window, text="Endereço IP do Servidor: {}".format(endereco_ip), background='pink', font=(12))
    label_endereco_ip.pack()
    
    label_cabecalho = tk.Label(detalhes_window, text="Cabeçalho:", background='pink', font=(12))
    label_cabecalho.pack(pady=10)
    
    text_cabecalho = tk.Text(detalhes_window)
    text_cabecalho.insert(tk.END, str(cabeçalho))
    text_cabecalho.pack(pady=10, expand=True, fill=tk.BOTH)
    
    detalhes_window.mainloop()


# Cria a tabela no banco de dados (se ainda não existir)
criar_tabela()

# Cria a janela principal
window = tk.Tk()
window.title("Cadastro de URLs")
window.geometry("1024x1080")
window.configure(background='pink')

# Janela de boas-vindas
tela_boas_vindas = tk.Frame(window)
tela_boas_vindas.configure(background="pink")
tela_boas_vindas.pack(side=tk.TOP)

rotulo_boas_vindas = tk.Label(
    tela_boas_vindas, text="Bem-vindo! Aqui você poderá: Incluir, Alterar, Adicionar, Listar e Validar URLs", bg='pink', font=(12))
rotulo_boas_vindas.pack(pady=300)

botao_telaurl = tk.Button(
    tela_boas_vindas, text="Ir para Pagina de URLs", command=exibir_telas, bg='black', fg='pink', font=(12))
botao_telaurl.pack()

# Cria os elementos da interface
tela_url = tk.Frame(window)
tela_url.configure(background='pink')
tela_url.pack(side=tk.TOP)


label_url = tk.Label(window, text="URL:", background='pink', font=(20))
label_url.pack()

entry_url = tk.Entry(window)
entry_url.pack()

button_adicionar = tk.Button(window, text="Validar e Adicionar", command=adicionar_url, bg='black', fg='pink', font=(12))
button_adicionar.pack()

button_alterar = tk.Button(window, text="Alterar", command=alterar_url, bg='black', fg='pink', font=(12))
button_alterar.pack()

button_excluir = tk.Button(window, text="Excluir", command=excluir_url, bg='black', fg='pink', font=(12))
button_excluir.pack()

listbox_urls = tk.Listbox(window)
listbox_urls.pack()

button_validar = tk.Button(window, text="Validar URLs", command=validar_urls, bg='black', fg='pink', font=(12))
button_validar.pack()

button_importar = tk.Button(window, text="Importar", command=importar_urls, bg='black', fg='pink', font=(12))
button_importar.pack()

exibir_urls()
window.mainloop()
