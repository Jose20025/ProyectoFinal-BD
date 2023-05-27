import customtkinter as ctk
from tkinter import StringVar, ttk
from CTkMessagebox import CTkMessagebox as msg
import pyodbc
from PIL import Image

conexiones = {'josek': ['password', 'JoseK-Laptop\SQLEXPRESS'],
              'nangui': ['soychurro', 'BrunoPC']}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        self.geometry('500x700')
        self.title('Login')
        self.iconbitmap('./image/icono.ico')
        self.resizable(0, 0)
        self.eleccionPage = Eleccion(self)
        self.mainPageHotel = HotelPage(self)
        self.mainPageVeterinaria = VeterinariaPage(self)

        self.loginPage = LoginPage(self)
        self.loginPage.pack()

        self.centrarVentana(500, 700)

    def centrarVentana(self, ancho, alto):
        self.update()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f'{ancho}x{alto}+{x}+{y-20}')

    def cambioVentana(self, old: ctk.CTkFrame, new: ctk.CTkFrame, ancho, alto, titulo):
        old.destroy()
        self.geometry(f'{ancho}x{alto}')
        self.title(titulo)
        self.centrarVentana(ancho, alto)
        self.update()
        new.pack()


class LoginPage(ctk.CTkFrame):
    def __init__(self, master: App = None):
        super().__init__(master=master, width=500, height=700)

        self.padre = master

        self.logo = ctk.CTkLabel(self, image=ctk.CTkImage(light_image=Image.open(
            './image/logo-transparente.png'), dark_image=Image.open('./image/logo-transparente.png'), size=(400, 370)), width=400, height=340, text='',

            corner_radius=5)
        self.logo.place(x=50, y=40)

        # User Frame
        self.userFrame = ctk.CTkFrame(self, width=400, height=230)

        ctk.CTkLabel(
            self.userFrame, text='Username').place(x=40, y=20)

        self.username = ctk.CTkEntry(
            self.userFrame, width=340, height=30, placeholder_text='Ingrese su usuario')
        self.username.place(x=30, y=45)
        self.username.bind('<Return>', self.login)

        ctk.CTkLabel(
            self.userFrame, text='Password').place(x=40, y=100)

        self.password = ctk.CTkEntry(
            self.userFrame, width=340, height=30, placeholder_text='Ingrese su contraseña', show='*')
        self.password.place(x=30, y=125)
        self.password.bind('<Return>', self.login)

        self.boton = ctk.CTkButton(
            self.userFrame, text='Login', command=self.login)
        self.boton.place(x=135, y=180)

        self.userFrame.place(x=50, y=430)

    def login(self, event=None):

        global user, password

        self.user = self.username.get()
        self.passwd = self.password.get()
        if self.user and self.passwd:
            if self.user in conexiones and self.passwd == conexiones[self.user][0]:
                try:
                    self.conexion = pyodbc.connect(
                        f'DRIVER={{SQL Server}};SERVER={conexiones[self.user][1]};DATABASE=FinalVeterinaria;UID={self.user};PWD={self.passwd}')
                    self.conexion.close()

                except:
                    msg(title='Error en la conexion',
                        message='Usuario o contraseña incorrectos', icon='cancel')

                else:
                    user.set(self.user)
                    password.set(self.passwd)
                    print(user.get())
                    self.padre.cambioVentana(
                        self.padre.loginPage, self.padre.eleccionPage, 400, 250, 'Eleccion')

            else:
                msg(title='Error en la conexion',
                    message='Usuario o contraseña incorrectos', icon='cancel')
        elif not self.user and self.passwd:
            msg(title='Usuario es requerido',
                message='El campo de username no puede estar vacio', icon='cancel')
        elif not self.passwd and self.user:
            msg(title='La contraseña es requerida',
                message='El campo de contraseña no puede estar vacio', icon='cancel')
        else:
            msg(title='Campos requeridos',
                message='Los dos campos no pueden estar vacios', icon='cancel')


class Eleccion(ctk.CTkFrame):
    def __init__(self, master: App = None):
        super().__init__(master=master, width=400, height=250)
        self.padre = master

        ctk.CTkLabel(self, text='¿A donde quieres entrar?',
                     width=150, height=50, anchor=ctk.CENTER).place(x=130, y=20)

        ctk.CTkButton(self, text='Veterinaria', width=160,
                      height=90, anchor=ctk.CENTER, command=self.veterinaria).place(x=20, y=90)

        ctk.CTkButton(self, text='Hotel', width=160,
                      height=90, anchor=ctk.CENTER, command=self.hotel).place(x=220, y=90)

    def hotel(self):
        self.padre.mainPageHotel.tablaFrame.setTabla(
            'select M.* from Mascotas M inner join Estadias E on M.CodMascota = E.CodMascota order by M.CodMascota')
        self.padre.cambioVentana(
            self, self.padre.mainPageHotel, 1000, 600, 'Cute Pets - Hotel')

    def veterinaria(self):
        self.padre.mainPageVeterinaria.tablaFrame.setTabla(
            'select distinct M.* from Mascotas M inner join HistorialesPeso H on M.CodMascota = H.CodMascota')
        self.padre.cambioVentana(
            self, self.padre.mainPageVeterinaria, 1000, 600, 'Cute Pets - Veterinaria')


class HotelPage(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master=master, width=1000, height=600)

        self.padre = master
        self.cursor = None

        self.tablaFrame = Tabla(self, 640, 340)

        ctk.CTkButton(self, text='Consultas', width=210,
                      height=40).place(x=20, y=30)

        ctk.CTkButton(self, text='Insertar', width=210,
                      height=40).place(x=20, y=100)

        ctk.CTkButton(self, text='Modificar', width=210,
                      height=40).place(x=20, y=170)

        ctk.CTkButton(self, text='Eliminar', width=210,
                      height=40).place(x=20, y=240)

        ctk.CTkButton(self, text='Consulta Personalizada', width=210,
                      height=40).place(x=20, y=310)

        self.imagen = ctk.CTkImage(dark_image=Image.open(
            './image/logo_sinletras.jpg'), size=(210, 180))

        ctk.CTkLabel(
            self, width=190, height=160, image=self.imagen, text='').place(x=20, y=400)


class VeterinariaPage(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master=master, width=1000, height=600)

        self.padre = master

        self.tablaFrame = Tabla(self, 640, 340)

        ctk.CTkButton(self, text='Consultas', width=210,
                      height=40).place(x=20, y=30)

        ctk.CTkButton(self, text='Insertar', width=210,
                      height=40).place(x=20, y=100)

        ctk.CTkButton(self, text='Modificar', width=210,
                      height=40).place(x=20, y=170)

        ctk.CTkButton(self, text='Eliminar', width=210,
                      height=40).place(x=20, y=240)

        ctk.CTkButton(self, text='Consulta Personalizada', width=210,
                      height=40).place(x=20, y=310)

        self.imagen = ctk.CTkImage(dark_image=Image.open(
            './image/logo_sinletras.jpg'), size=(210, 180))

        ctk.CTkLabel(
            self, width=190, height=160, image=self.imagen, text='').place(x=20, y=400)


class Tabla(ctk.CTkFrame):
    def __init__(self, master, ancho, alto):
        super().__init__(master, width=ancho, height=alto)

    def setTabla(self, consulta):
        print(user.get(), password.get())

        self.user = user.get()
        self.password = password.get()

        self.conexion = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={conexiones[self.user][1]};DATABASE=FinalVeterinaria;UID={self.user};PWD={self.password}')
        self.cursor = self.conexion.cursor()

        self.cursor.execute(consulta)

        titulos = []

        for titulo in self.cursor.description:
            titulos.append(titulo[0])

        mascotas = self.cursor.fetchall()

        self.tabla = ttk.Treeview(
            self, columns=titulos[1:], height=20)

        for titulo in titulos:
            if titulo == titulos[0]:
                self.tabla.column('#0', width=100, anchor=ctk.CENTER)
                self.tabla.heading('#0', text=titulo)
            else:
                self.tabla.column(titulo, width=100, anchor=ctk.CENTER)
                self.tabla.heading(titulo, text=titulo)

        for mascota in mascotas:
            atributos = []
            for atributo in mascota:
                atributos.append(atributo)

            self.tabla.insert(
                '', ctk.END, text=atributos[0], values=atributos[1:])

        self.tabla.pack()
        self.conexion.close()

        self.place(x=310, y=10)


class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master=master, width=1000, height=600)


if __name__ == '__main__':
    app = App()
    user = StringVar()
    password = StringVar()
    app.mainloop()
