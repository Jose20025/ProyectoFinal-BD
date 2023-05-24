import customtkinter as ctk
import pyodbc
import tkinter.messagebox as msg
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        self.geometry('500x700')
        self.conexion = None
        self.title('Login')
        self.iconbitmap('./image/icono.ico')
        self.resizable(0, 0)

        self.loginPage = ctk.CTkFrame(self, width=500, height=700)

        image = ctk.CTkImage(dark_image=Image.open(
            './image/fondo2.jpg'), size=(500, 1000))
        background_label = ctk.CTkLabel(self.loginPage, image=image, text='')
        background_label.pack()

        self.logo = ctk.CTkLabel(self.loginPage, image=ctk.CTkImage(light_image=Image.open(
            './image/logo.jpg'), dark_image=Image.open('./image/logo.jpg'), size=(400, 340)), width=400, height=340, text='',
            corner_radius=5)
        self.logo.place(x=50, y=40)

        self.loginPage.pack()

        self.userFrame = ctk.CTkFrame(self.loginPage, width=400, height=230)

        ctk.CTkLabel(
            self.userFrame, text='Username').place(x=40, y=20)

        self.username = ctk.CTkEntry(
            self.userFrame, width=340, height=30, placeholder_text='Ingrese su usuario')
        self.username.place(x=30, y=45)

        ctk.CTkLabel(
            self.userFrame, text='Password').place(x=40, y=100)

        self.password = ctk.CTkEntry(
            self.userFrame, width=340, height=30, placeholder_text='Ingrese su contraseña')
        self.password.place(x=30, y=125)

        ctk.CTkButton(
            self.userFrame, text='Login', command=self.login).place(x=230, y=180)

        self.userFrame.place(x=50, y=430)

        # Main Page
        self.mainPage = ctk.CTkFrame(self, width=1000, height=800)

    def login(self):
        user = self.username.get()
        password = self.password.get()
        if user and password:
            try:
                self.conexion = pyodbc.connect(
                    f'DRIVER={{SQL Server}};SERVER=JoseK-Laptop\SQLEXPRESS;DATABASE=FinalVeterinaria;UID={user};PWD={password}')

                self.loginPage.pack_forget()
                self.mainPage.pack()
                self.geometry('1000x600')

            except:
                msg.showerror('Error en la conexion',
                              'Usuario o contraseña incorrectos')
        elif not user and password:
            msg.showerror('Usuario es requerido',
                          'El campo de username no puede estar vacio')
        elif not password and user:
            msg.showerror('La contraseña es requerida',
                          'El campo de contraseña no puede estar vacio')
        else:
            msg.showerror('Campos requeridos',
                          'Los dos campos no pueden estar vacios')


app = App()
app.mainloop()
