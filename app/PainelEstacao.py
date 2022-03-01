from tkinter import Button, Entry, Frame, Label, Scrollbar, Tk, ttk, messagebox
from tkinter.font import Font
from tkinter.constants import END
from PIL import Image, ImageTk
import mysql.connector as mysql
from dotenv import load_dotenv, dotenv_values
import sys

login = Tk()

cor_fundo = "#e9e9e9"
cor_verde_principal = "#36b987"
cor_verde = "#3cc47c"

config = load_dotenv('.env')
values = dotenv_values('.env')

HOST=values['HOST']
DATABASE=values['DATABASE']
USER=values['USER']
PASSWORD=values['PASSWORD']
LOGON=values['LOGON']
PASSWD=values['PASSWD']


class Login:
    def __init__(self):
        self.login_window = login
        self.login_window.title('Login Estação Meteorológica')
        self.login_window.geometry('400x150')
        if sys.platform.startswith('win'):
            self.login_window.iconbitmap('app_icon.ico')
        self.login_window.resizable(False, False)
        self.widgets()
        self.login_window.mainloop()
    

    def widgets(self):
        self.nome_label = Label(self.login_window, text='Nome', font=Font(family='Verdana', size=11))
        self.nome_label.place(relx=0.01, rely=0.01)
        self.senha_label = Label(self.login_window, text='Senha', font=Font(family='Verdana', size=11))
        self.senha_label.place(relx=0.01, rely=0.4)

        self.nome = Entry(self.login_window, font=Font(family='Verdana', size=11))
        self.nome.place(relx=0.01, rely=0.15, relwidth=0.98)
        self.senha = Entry(self.login_window, font=Font(family='Verdana', size=11))
        self.senha.place(relx=0.01, rely=0.55, relwidth=0.98)

        self.send = Button(self.login_window, text="OK", font=Font(family='Verdana', size=11),
                           command=self.test_credenciais)
        self.send.place(relx=0.01, rely=0.75, relwidth=0.5)
        self.cancel = Button(self.login_window, text="Cancelar", font=Font(family='Verdana', size=11),
                             command=self.login_window.destroy)
        self.cancel.place(relx=0.52, rely=0.75, relwidth=0.47)
    

    def test_credenciais(self):
        if str(self.nome.get()).strip() == str(LOGON) and str(self.senha.get()).strip() == str(PASSWD):
            self.login_window.destroy()
            App()
        else: 
            self.nome.delete(0, END)
            self.senha.delete(0, END)
            messagebox.showinfo("Erro nas credenciais", "Nome e/ou senha incorretos!")


class DB:
    def conectar(self):
        self.conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        # print('Conectado a', self.conn.get_server_info())
        self.cursor = self.conn.cursor()
    

    def desconectar(self):
        self.cursor.close()
        self.conn.close()

    
    def limpar_entries(self):
        self.id_entry.delete(0, END)
        self.data_entry.delete(0, END)
        self.hora_entry.delete(0, END)
        self.tempr_entry.delete(0, END)
        self.umid_entry.delete(0, END)
        self.pressao_entry.delete(0, END)
        self.lum_entry.delete(0, END)


    def atualizar_dados_tempo(self):
        self.get_dados_tempo()
        messagebox.showinfo('Dados Atualizados', 'Dados foram atualizados de acordo com o Banco de Dados.')


    def get_dados_tempo(self):
        self.listaUser.delete(*self.listaUser.get_children())
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
        

class App(DB, Login):
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.fonts()
        self.frames()
        self.widgets_frame()
        self.lista_estacao()
        self.lista_projetos()
        self.get_dados_tempo()
        self.painel_edicao()
        self.root.mainloop()

    def tela(self):
        self.root.title('Painel da Estação Meteorológica')
        self.root.configure(background=cor_fundo)
        self.root.geometry('900x600')
        if sys.platform.startswith('win'):
            self.image_icon = ImageTk.PhotoImage(Image.open('app_icon.ico'))
            self.root.iconbitmap('app_icon.ico')
        # self.root.state('zoomed') # Fullscreen
        self.root.resizable(True, True)
        self.root.minsize(width=900, height=500)

    def fonts(self):
        self.font = Font(family='Verdana', size=9)
        self.font_bold = Font(family='Verdana', size=10, weight='bold')
        self.font_mono = Font(family='Inconsolata', size=10)

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
    

    def painel_edicao(self):
        # Labels e Entrys
        self.title = Label(self.aba1, text='Consulta e edição dos dados da estação', bg=cor_fundo, font=self.font_bold)
        self.title.place(relx=0.01, rely=0.01)


        self.id = Label(self.aba1, text='ID', bg=cor_fundo, font=self.font)
        self.id.place(relx=0.6, rely=0.01)
        self.id_entry = Entry(self.aba1, font=self.font, bg=cor_fundo)
        self.id_entry.place(relx=0.64, rely=0.01, relwidth=0.05, relheight=0.045)

        self.data = Label(self.aba1, text='Data', bg=cor_fundo, font=self.font)
        self.data.place(relx=0.01, rely=0.07)
        self.data_entry = Entry(self.aba1, font=self.font)
        self.data_entry.place(relx=0.055, rely=0.07, relwidth=0.1, relheight=0.045)

        self.lum = Label(self.aba1, text='Luminosidade', bg=cor_fundo, font=self.font)
        self.lum.place(relx=0.16, rely=0.07)
        self.lum_entry = Entry(self.aba1, font=self.font)
        self.lum_entry.place(relx=0.285, rely=0.07, relwidth=0.08, relheight=0.045)

        self.pressao = Label(self.aba1, text='Pressão atm.', bg=cor_fundo, font=self.font)
        self.pressao.place(relx=0.16, rely=0.14)
        self.pressao_entry = Entry(self.aba1, font=self.font)
        self.pressao_entry.place(relx=0.285, rely=0.14, relwidth=0.08, relheight=0.045)

        self.hora = Label(self.aba1, text='Hora', bg=cor_fundo, font=self.font)
        self.hora.place(relx=0.41, rely=0.07)
        self.hora_entry = Entry(self.aba1, font=self.font)
        self.hora_entry.place(relx=0.5, rely=0.07, relwidth=0.079, relheight=0.045)

        self.umid = Label(self.aba1, text='Umidade', bg=cor_fundo, font=self.font)
        self.umid.place(relx=0.01, rely=0.14)
        self.umid_entry = Entry(self.aba1, font=self.font)
        self.umid_entry.place(relx=0.09, rely=0.14, relwidth=0.064, relheight=0.045)

        self.tempr = Label(self.aba1, text='Temperatura', bg=cor_fundo, font=self.font)
        self.tempr.place(relx=0.38, rely=0.14)
        self.tempr_entry = Entry(self.aba1, font=self.font)
        self.tempr_entry.place(relx=0.5, rely=0.14, relwidth=0.08, relheight=0.045)

        # Botoes
        self.adicionar = Button(self.aba1, text="Adicionar", font=self.font,command=self.atualizar_dados_tempo)
        self.adicionar.place(relx=0.6, rely=0.14, relwidth=0.115, relheight=0.05)
        self.buscar = Button(self.aba1, text="Buscar", font=self.font,command=self.atualizar_dados_tempo)
        self.buscar.place(relx=0.6, rely=0.07, relwidth=0.115, relheight=0.05)
        self.limpar = Button(self.aba1, text="Limpar", font=self.font,command=self.limpar_entries)
        self.limpar.place(relx=0.74, rely=0.01, relwidth=0.115, relheight=0.05)
        self.apagar = Button(self.aba1, text="Apagar", font=self.font,command=self.atualizar_dados_tempo)
        self.apagar.place(relx=0.74, rely=0.075, relwidth=0.115, relheight=0.05)
        self.reescrever = Button(self.aba1, text="Reescrever", font=self.font,command=self.atualizar_dados_tempo)
        self.reescrever.place(relx=0.74, rely=0.14, relwidth=0.115, relheight=0.05)
        self.atualizar = Button(self.aba1, text="Atualizar", font=self.font,command=self.atualizar_dados_tempo)
        self.atualizar.place(relx=0.88, rely=0.14, relwidth=0.115, relheight=0.05)
        
        # Imagem logo
        if sys.platform.startswith('win'):
            self.logo = Label(self.aba1, image=self.image_icon, bg=cor_fundo)
            self.logo.place(relx=0.88, rely=0.01, relwidth=0.115, relheight=0.115)
        

    def lista_estacao(self):
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", bd=1, font=('Verdana', 9))
        self.style.configure("mystyle.Treeview.Heading", font=('Verdana', 9, 'bold'))

        self.listaUser = ttk.Treeview(self.aba1, height=3,
                                      column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'),
                                      style='mystyle.Treeview')
        self.listaUser.heading('#0', text='')
        self.listaUser.heading('#1', text='ID')
        self.listaUser.heading('#2', text='Data')
        self.listaUser.heading('#3', text='Hora')
        self.listaUser.heading('#4', text='Temperatura °C')
        self.listaUser.heading('#5', text='Umidade %')
        self.listaUser.heading('#6', text='Pressão atm. hPa')
        self.listaUser.heading('#7', text='Luminosidade lm')

        self.listaUser.column('#0', width=-100)
        self.listaUser.column('#1', width=-30)
        self.listaUser.column('#2', width=10)
        self.listaUser.column('#3', width=0)
        self.listaUser.column('#4', width=40)
        self.listaUser.column('#5', width=10)
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
    Login()
