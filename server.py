import Pyro4
from const import *

#Bibliotecas para manipulação e construção da interface gráfica no Tkinter:
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

root = tk.Tk()
root.withdraw()

@Pyro4.expose
class Server():
    def get_usernames(name):
        return usernames[clients.index(name)]

    def set_clients(name):
        usernames.append(name)

    def globalMessage(message):
        print("globalMessage: " + str(message))
        for client in clients:
            client.send(message)

    def handleMessages(self, teste):
        print(teste)

def conexao(text_area):
    Pyro4.Daemon.serveSimple(
        {
            Server: "Gekitai",
        },
        host="127.0.0.1",
        port=210,
        ns=False,
        verbose=True,
    )
    print(f"Ready to listen")
    # text_area.insert(tk.INSERT, "Servidor conectado!\n")
    # while True:
    #     try:
    #         # Aceitando a conexao
    #         client, address = server.accept()
    #
    #         # Adicionando a conexao a uma lista
    #         print(f"Nova conexao no endereco: {str(address)}")
    #         clients.append(client)
    #         response = '{"event":"getUser", "index": "'+str(clients.index(client))+'"}'
    #         client.send(response.encode(DEFAULT_ENCODING))
    #         username = client.recv(2048).decode(DEFAULT_ENCODING)
    #         usernames.append(username)
    #
    #         # Printa no terminal e no servidor
    #         text_area.insert(tk.INSERT, f'{username} acaba de entrar no chat!\n'.encode(DEFAULT_ENCODING))
    #         #globalMessage(f'{"event":"CHAT, "message": {username} acaba de entrar no chat!}\n'.encode(DEFAULT_ENCODING))
    #
    #         user_thread = threading.Thread(target=handleMessages,args=(client,))
    #         user_thread.start()
    #     except:
    #         pass


def janela_servidor():
    newWindow = Toplevel(root)
    newWindow.title("Socket: Servidor")
    newWindow.geometry("476x220")

    newWindow.protocol("WM_DELETE_WINDOW", janela_aviso)

    text_area = ScrolledText(newWindow, wrap=WORD, fg='blue', width=42, height=7, font=("Callibri", 9))
    text_area.place(x=120, y=79)
    text_area.focus()

    conexao(text_area)

def janela_aviso():
    newWindow = Toplevel(root)
    newWindow.title("Servidor: Aviso!")
    newWindow.geometry("360x205")

    sim_button = Button(newWindow, text='SIM', width=12, command=lambda:action_sim(newWindow))
    sim_button.place(x=124, y=154)

    nao_button = Button(newWindow, text='NÃO', width=12, command=lambda:action_nao(newWindow))
    nao_button.place(x=240, y=154)

def action_sim(Toplevel):
    Toplevel.destroy()
    Toplevel.quit()
    root.destroy()

def action_nao(Toplevel):
    Toplevel.destroy()

if __name__ == "__main__":
    janela_servidor()
    #threading.Thread(target=janela_servidor).start() # Mostrar janela do servidor
    root.mainloop()