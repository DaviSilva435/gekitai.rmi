import Pyro4
from const import *

#Bibliotecas para manipulação e construção da interface gráfica no Tkinter:
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

root = tk.Tk()
root.withdraw()

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server(object):
    def __init__(self):
        self.channels = {}  # registered channels { channel --> (nick, client callback) list }
        self.nicks = []
    def getChannels(self):
        return list(self.channels.keys())

    def getNicks(self):
        return self.nicks

    def join(self, channel, nick, callback):
        if not channel or not nick:
            raise ValueError("Invalido nome ou canal")
        if nick in self.nicks:
            raise ValueError('Este usuario já existe')
        if channel not in self.channels:
            print('Criando um novo canal %s' % channel)
            self.channels[channel] = []
        self.channels[channel].append((nick, callback))
        self.nicks.append(nick)
        print("%s JOINED %s" % (nick, channel))
        self.publish(channel, nick,  nick )
        return [nick for (nick, c) in self.channels[channel]]

    def publish(self, channel, nick, msg):
        if channel not in self.channels:
            print('IGNORED UNKNOWN CHANNEL %s' % channel)
            return
        for (n, c) in self.channels[channel][:]:  # use a copy of the list
            try:
                print(msg)
                c.receiveMessage(nick, msg)  # oneway call
            except Pyro4.errors.ConnectionClosedError:
                # connection dropped, remove the listener if it's still there
                # check for existence because other thread may have killed it already
                if (n, c) in self.channels[channel]:
                    self.channels[channel].remove((n, c))
                    print('Removed dead listener %s %s' % (n, c))

def conexao(text_area):
    Pyro4.Daemon.serveSimple({
        Server: "gekitai.server"
    })

    print(f"Ready to listen")

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