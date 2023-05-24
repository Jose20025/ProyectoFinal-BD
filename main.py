import customtkinter as ctk
import pyodbc
from tabulate import tabulate
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        self.geometry('500x700')
        self.conexion = None
        self.iconbitmap('./image/icono.ico')

        self.loginPage = ctk.CTkFrame(self, width=500, height=700)

        image = ctk.CTkImage(dark_image=Image.open(
            './image/fondo2.jpg'), size=(500, 1000))
        background_label = ctk.CTkLabel(self.loginPage, image=image, text='')
        background_label.pack()

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

        self.boton = ctk.CTkButton(
            self.userFrame, text='Login', command=self.login)
        self.boton.place(x=130, y=180)

        self.userFrame.place(x=50, y=430)

    def login(self):
        user = self.username.get()
        password = self.password.get()
        if user and password:
            try:
                self.conexion = pyodbc.connect(
                    f'DRIVER={{SQL Server}};SERVER=JoseK-Laptop\SQLEXPRESS;DATABASE=FinalVeterinaria;UID={user};PWD={password}')

                cursor = self.conexion.cursor()

                cursor.execute('select * from Clientes')
                resultado = cursor.fetchall()

                nombreColumnas = [columna[0] for columna in cursor.description]

                tabla = tabulate(resultado, headers=nombreColumnas,
                                 tablefmt='fancy_grid')

                print(tabla)

                cursor.close()
                conexion.close()

            except:
                pass


app = App()
app.mainloop()
