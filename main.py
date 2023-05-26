import customtkinter as ctk
from CTkMessagebox import CTkMessagebox as msg
import pyodbc
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        self.geometry('500x700')
        self.title('Login')
        self.iconbitmap('./image/icono.ico')
        self.resizable(0, 0)

        self.conexion = None

        self.loginPage = LoginPage(self)
        self.loginPage.pack()

        self.centrarVentana(500, 700)

        # Eleccion
        self.eleccionPage = Eleccion(self)

        # Main Page
        self.mainPageHotel = MenuPrincipal(self)

    def centrarVentana(self, ancho, alto):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f'{ancho}x{alto}+{x}+{y-20}')

    def cambioVentana(self, old: ctk.CTkFrame, new: ctk.CTkFrame, ancho, alto, titulo):
        old.destroy()
        self.geometry(f'{ancho}x{alto}')
        self.title(titulo)
        self.centrarVentana(ancho, alto)
        new.pack()


class LoginPage(ctk.CTkFrame):
    def __init__(self, master: App = None):
        super().__init__(master=master, width=500, height=700)

        self.padre = master
        self.conexiones = {'josek': ['password', 'JoseK-Laptop\SQLEXPRESS'],
                           'nangui': ['soychurro', 'JoseK-Laptop\SQLEXPRESS']}

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
        user = self.username.get()
        password = self.password.get()
        if user and password:
            if user in self.conexiones and password == self.conexiones[user][0]:
                try:
                    self.padre.conexion = pyodbc.connect(
                        f'DRIVER={{SQL Server}};SERVER={self.conexiones[user][1]};DATABASE=FinalVeterinaria;UID={user};PWD={password}')

                    self.padre.cambioVentana(
                        self.padre.loginPage, self.padre.eleccionPage, 400, 250, 'Eleccion')

                except:
                    msg(title='Error en la conexion',
                        message='Usuario o contraseña incorrectos', icon='cancel')
            else:
                msg(title='Error en la conexion',
                    message='Usuario o contraseña incorrectos', icon='cancel')
        elif not user and password:
            msg(title='Usuario es requerido',
                message='El campo de username no puede estar vacio', icon='cancel')
        elif not password and user:
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
        self.padre.cambioVentana(
            self, self.padre.mainPageHotel, 1000, 600, 'Cute Pets - Hotel')

    def veterinaria(self):
        self.padre.cambioVentana(
            self, self.padre.mainPageHotel, 1000, 600, 'Cute Pets - Hotel')


class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master=master, width=1000, height=600)

        self.padre = master

        ctk.CTkButton(self, text='Consultas', width=210,
                      height=40).place(x=20, y=10)

        ctk.CTkButton(self, text='Insertar', width=210,
                      height=40).place(x=20, y=80)

        ctk.CTkButton(self, text='Modificar', width=210,
                      height=40).place(x=20, y=150)

        ctk.CTkButton(self, text='Eliminar', width=210,
                      height=40).place(x=20, y=220)

        ctk.CTkButton(self, text='Consulta Personalizada', width=210,
                      height=40).place(x=20, y=290)

        self.imagen = ctk.CTkImage(dark_image=Image.open(
            './image/logo_sinletras.jpg'), size=(210, 180))

        ctk.CTkLabel(
            self, width=190, height=160, image=self.imagen, text='').place(x=20, y=380)


app = App()
app.mainloop()
