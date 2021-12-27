from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import mysql.connector as mysql
from PIL import Image, ImageTk
from dotenv import load_dotenv, dotenv_values


root = Tk()
root.iconbitmap('app_icon.ico')

font = Font(family='Verdana', size=9)
font_bold = Font(family='Verdana', size=10, weight='bold')
font_mono = Font(family='Inconsolata', size=10)

cor_fundo = "#e9e9e9"
cor_verde_principal = "#36b987"
cor_verde = "#3cc47c"

config = load_dotenv('.env')
values = dotenv_values('.env')

HOST=values['HOST']
DATABASE=values['DATABASE']
USER=values['USER']
PASSWORD=values['PASSWORD']


class DB:
    def conectar(self):
        self.conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        # print('Conectado a', self.conn.get_server_info())
        self.cursor = self.conn.cursor()
    

    def desconectar(self):
        self.cursor.close()
        self.conn.close()


    def get_dados_tempo(self):
        self.conectar()
        self.cursor.execute(
            """
            SELECT
                id,datac,horac,temperatura,umidade,pressao,luminosidade
            FROM 
                `estacao`
            ORDER BY
                id DESC;
            """
            )
        self.lista = self.cursor.fetchall()
        # print(self.lista)
        for item in self.lista:
            self.listaUser.insert("", END, values=item)
        self.desconectar()
        

class App(DB):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames()
        self.widgets_frame()
        self.lista_estacao()
        self.lista_projetos()
        self.get_dados_tempo()
        self.root.mainloop()


    def tela(self):
        self.root.title('Painel da Estação Meteorológica')
        self.root.configure(background=cor_fundo)
        self.root.geometry('900x600')
        self.root.resizable(True, True)
        self.root.minsize(width=700, height=500)

    def frames(self):
        self.frame1 = Frame(self.root, bd=4, bg=cor_verde_principal,
                            highlightbackground=cor_verde,
                            highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    
    def widgets_frame(self):
        self.abas = ttk.Notebook(self.frame1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background=cor_fundo)
        self.aba2.configure(background=cor_fundo)

        self.abas.add(self.aba1, text='  Dados meteorológicos  ')
        self.abas.add(self.aba2, text='  Projetos  ')

        self.abas.place(relx=0, rely=0, relwidth=0.999, relheight=0.999)
    

    def lista_estacao(self):
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", bd=1, font=('Verdana', 9))
        self.style.configure("mystyle.Treeview.Heading", font=('Verdana', 9, 'bold'))

        self.listaUser = ttk.Treeview(self.aba1, height=3,
                                      column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'),
                                      style='mystyle.Treeview')
        self.listaUser.heading('#0', text='', anchor=CENTER)
        self.listaUser.heading('#1', text='ID')
        self.listaUser.heading('#2', text='Data')
        self.listaUser.heading('#3', text='Hora')
        self.listaUser.heading('#4', text='Temperatura')
        self.listaUser.heading('#5', text='Umidade')
        self.listaUser.heading('#6', text='Pressão atm.')
        self.listaUser.heading('#7', text='Luminosidade')

        self.listaUser.column('#0', width=0)
        self.listaUser.column('#1', width=0)
        self.listaUser.column('#2', width=50)
        self.listaUser.column('#3', width=50)
        self.listaUser.column('#4', width=50)
        self.listaUser.column('#5', width=50)
        self.listaUser.column('#6', width=50)
        self.listaUser.column('#7', width=50)

        self.listaUser.place(relx=0.01, rely=0.2, relwidth=0.95, relheight=0.78)

        self.scrollLista = Scrollbar(self.aba1, orient='vertical')
        self.listaUser.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.2, relwidth=0.035, relheight=0.78)
    

    def lista_projetos(self):
        self.style_proj = ttk.Style()
        self.style_proj.configure("mystyle.Treeview", bd=1, font=('Verdana', 9))
        self.style_proj.configure("mystyle.Treeview.Heading", font=('Verdana', 9, 'bold'))

        self.listaProj = ttk.Treeview(self.aba2, height=3,
                                      column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'),
                                      style='mystyle.Treeview')
        self.listaProj.heading('#0', text='ID')
        self.listaProj.heading('#1', text='Título')
        self.listaProj.heading('#2', text="Descrição")
        self.listaProj.heading('#3', text='Link Imagem 1')
        self.listaProj.heading('#4', text='Link Imagem 2')
        self.listaProj.heading('#5', text='Código')
        self.listaProj.heading('#6', text='Link Youtube')
        self.listaProj.heading('#7', text='Autor')

        self.listaProj.column('#0', width=1)
        self.listaProj.column('#1', width=25)
        self.listaProj.column('#2', width=25)
        self.listaProj.column('#3', width=50)
        self.listaProj.column('#4', width=25)
        self.listaProj.column('#5', width=15)
        self.listaProj.column('#6', width=50)
        self.listaProj.column('#7', width=50)

        self.listaProj.place(relx=0.01, rely=0.2, relwidth=0.95, relheight=0.78)

        self.scrollLista2 = Scrollbar(self.aba2, orient='vertical')
        self.listaProj.configure(yscroll=self.scrollLista2.set)
        self.scrollLista2.place(relx=0.96, rely=0.2, relwidth=0.035, relheight=0.78)

if __name__ == '__main__':
    App()
