import ctypes
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning

import pyodbc
from PIL import Image, ImageTk

from models.cliente import Cliente


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Aplicando el tema
        self.tk.call('source', 'azure.tcl')
        self.tk.call('set_theme', 'dark')

        self.iconbitmap('./image/icono.ico')
        self.geometry('500x700')
        self.title('Login')
        self.resizable(0, 0)

        self.loginPage = LoginPage(self)
        self.loginPage.pack()

        # Asignando variables de ventanas
        self.veterinaria = None
        self.hotel = None

        self.centrarVentana([500, 700])

    def cambioVentana(self, old, new, dimensiones: list, titulo):
        self.title(titulo)
        old.pack_forget()
        self.geometry(f'{dimensiones[0]}x{dimensiones[1]}')
        self.centrarVentana(dimensiones)
        new.pack()

    def centrarVentana(self, dimensiones: list):
        x = (self.winfo_screenwidth() // 2) - (dimensiones[0] // 2)
        y = (self.winfo_screenheight() // 2) - (dimensiones[1] // 2)
        self.geometry(f'{dimensiones[0]}x{dimensiones[1]}+{x}+{y-20}')


class LoginPage(ttk.Frame):
    def __init__(self, master: App = None):
        super().__init__(master, width=500, height=700)

        self.padre = master

        self.userFrame = ttk.Frame(
            self, width=400, height=245, style='Card.TFrame')

        self.imagen = ImageTk.PhotoImage(Image.open(
            './image/logo-transparente.png').resize((400, 370)))

        self.label = ttk.Label(self, image=self.imagen, justify=tk.CENTER)
        self.label.place(x=50, y=40)

        ttk.Label(self.userFrame, text='Username').place(x=40, y=20)

        self.username = ttk.Entry(self.userFrame, width=36)
        self.username.place(x=30, y=45)

        ttk.Label(self.userFrame, text='Password').place(x=40, y=100)

        self.password = ttk.Entry(self.userFrame, width=36, show='*')
        self.password.place(x=30, y=125)
        self.password.bind('<Return>', self.login)

        self.loginBoton = ttk.Button(
            self.userFrame, text='Login', style='Accent.TButton', command=self.login)
        self.loginBoton.place(x=260, y=180)

        self.lugarCBox = ttk.Combobox(self.userFrame, values=[
                                      'Veterinaria', 'Hotel'], state='readonly')
        self.lugarCBox.set('Veterinaria')
        self.lugarCBox.place(x=30, y=180)

        self.userFrame.place(x=50, y=430)

    def login(self, event=None):
        self.user = self.username.get()
        self.passwd = self.password.get()
        if self.user and self.passwd:
            if self.user in conexiones and self.passwd == conexiones[self.user][0]:
                try:
                    self.conexion = pyodbc.connect(
                        f'DRIVER={{SQL Server}};SERVER={conexiones[self.user][1]};DATABASE=FinalVeterinaria;UID={self.user};PWD={self.passwd}')
                    self.conexion.close()
                except:
                    showerror(title='Error en la conexion',
                              message='Ha ocurrido un error en la conexion a la base de datos')
                else:
                    user.set(self.user)
                    password.set(self.passwd)
                    self.eleccion(self.lugarCBox.get())
            else:
                showerror(title='Error en la conexion',
                          message='Usuario o contraseña incorrectos')
        elif not self.user and self.passwd:
            showerror(title='Usuario es requerido',
                      message='El campo de username no puede estar vacio')
        elif not self.passwd and self.user:
            showerror(title='La contraseña es requerida',
                      message='El campo de contraseña no puede estar vacio')
        else:
            showerror(title='Campos requeridos',
                      message='Los dos campos no pueden estar vacios')

    def eleccion(self, lugar):
        if lugar == 'Veterinaria':
            self.padre.veterinaria = VeterinariaPage(self.padre)
            self.padre.cambioVentana(
                self, self.padre.veterinaria, [1000, 600], 'Cute Pets - Veterinaria')
        else:
            self.padre.hotel = HotelPage(self.padre)
            self.padre.cambioVentana(
                self, self.padre.hotel, [1000, 600], 'Cute Pets - Hotel')


class HotelPage(ttk.Frame):
    pass


class VeterinariaPage(ttk.Frame):
    def __init__(self, master: App = None):
        super().__init__(master=master, width=1000, height=600)

        self.padre = master

        # Declarando variables para ventanas
        self.insertarPage = None

        ttk.Button(self, text='Consultas', width=40).place(x=20, y=30)

        ttk.Button(self, text='Insertar', width=40,
                   command=self.aInsertar).place(x=20, y=100)

        ttk.Button(self, text='Modificar', width=40).place(x=20, y=170)

        ttk.Button(self, text='Eliminar', width=40).place(x=20, y=240)

        ttk.Button(self, text='Consulta Personalizada',
                   width=40).place(x=20, y=310)

        self.imagen = ImageTk.PhotoImage(Image.open(
            './image/logo-transparente.png').resize((220, 200)))

        ttk.Label(self, image=self.imagen).place(x=20, y=350)

    def aInsertar(self):
        self.insertarPage = InsertarPageV(self)
        self.padre.cambioVentana(self, self.insertarPage, [
                                 400, 400], 'Insertar Mascota')


class InsertarPageV(ttk.Frame):
    def __init__(self, master: VeterinariaPage = None):
        super().__init__(master.padre, width=400, height=400)

        self.atributos = []

        self.padre = master

        self.razas = {
            1: ['Siames', 'Siberiano', 'Mestizo', 'Bengali', 'Yoda', 'Birmano', 'Persa', 'Azul ruso'],
            2: ['Labrador', 'Pastor Aleman', 'Caniche', 'Cocker', 'Chihuahua', 'Bulldog', 'Yorkshire', 'Pastor Ingles', 'Pincher', 'Husky']
        }

        self.colores = ['Cafe', 'Blanco', 'Negro',
                        'Gris', 'Dorado', 'Verde', 'Naranja']

        self.eleccionCliente = None

        ttk.Button(self, text='Volver', command=self.volverAtras,
                   width=6).place(x=10, y=10)

        ttk.Label(self, text='Alias').place(x=20, y=70)

        self.alias = ttk.Entry(self, width=38, state='disabled')
        self.alias.place(x=20, y=95)

        ttk.Label(self, text='Elige una especie').place(x=180, y=10)

        self.especie = tk.StringVar()

        self.cambioEspecieVar = tk.IntVar()
        ttk.Radiobutton(self, text='Felino', value=1, variable=self.cambioEspecieVar,
                        command=self.cambioEspecie).place(x=160, y=40)
        ttk.Radiobutton(self, text='Canino', value=2, variable=self.cambioEspecieVar,
                        command=self.cambioEspecie).place(x=250, y=40)

        ttk.Label(self, text='Raza').place(x=20, y=150)

        self.razaCBox = ttk.Combobox(self, state='disabled', width=15)
        self.razaCBox.set('')
        self.razaCBox.place(x=20, y=175)

        ttk.Label(self, text='Color').place(x=225, y=150)

        self.colorCBox = ttk.Combobox(
            self, state='disabled', values=self.colores, width=15)
        self.colorCBox.set('')
        self.colorCBox.place(x=225, y=175)

        ttk.Label(self, text='Tamaño').place(x=50, y=230)

        self.sizeCBox = ttk.Combobox(
            self, state='disabled', values=['S', 'M', 'G'], width=6)
        self.sizeCBox.set('')
        self.sizeCBox.place(x=50, y=255)

        ttk.Label(self, text='Fecha (yyyy-mm-dd)').place(x=220, y=230)

        self.fechaNac = ttk.Entry(self, width=15, state='disabled')
        self.fechaNac.place(x=220, y=255)

        ttk.Button(self, text='Aceptar', style='Accent.TButton',
                   command=self.confirmar).place(x=275, y=350)

    def volverAtras(self):
        alias = self.alias.get()
        size = self.sizeCBox.get()
        color = self.colorCBox.get()
        raza = self.razaCBox.get()
        fecha = self.fechaNac.get()

        lista = [alias, size, color, raza, fecha]

        if any(elemento != '' for elemento in lista):
            respuesta = askquestion(title='Confirmacion',
                                    message='¿Estas seguro?')

            if respuesta == 'yes':
                self.padre.padre.cambioVentana(
                    self, self.padre, [1000, 600], 'Veterinaria - Cute Pets')
                self.destroy()
            else:
                return
        else:
            self.padre.padre.cambioVentana(
                self, self.padre, 1000, 600, 'Veterinaria - Cute Pets')
            self.destroy()

    def confirmar(self):
        fecha = self.fechaNac.get()
        if fecha != '':
            if self.verificarFecha(fecha):
                alias = self.alias.get()
                size = self.sizeCBox.get()
                color = self.colorCBox.get()
                raza = self.razaCBox.get()
                especie = 'Canino' if self.cambioEspecieVar.get() == 2 else 'Felino'

                lista = [alias, especie, raza, color, fecha, size, 0]

                if all(elemento != '' for elemento in lista):
                    self.eleccionCliente = EleccionCliente(self.padre, lista)
                    self.padre.padre.cambioVentana(
                        self, self.eleccionCliente, [400, 200], 'Enlazar Cliente')

                else:
                    showwarning(title='Error en campos',
                                message='Todos los campos tienen que estar llenados')
            else:
                showerror(title='Error en la fecha',
                          message='Error en el formato de la fecha')
        else:
            showwarning(title='Error en campos',
                        message='Todos los campos tienen que estar llenados')

    def verificarFecha(self, fecha):
        if '-' in fecha:
            fecha_descompuesta = fecha.split('-')

            if len(fecha_descompuesta) == 3:
                año, mes, dia = map(int, fecha_descompuesta)
                try:
                    datetime(año, mes, dia)
                except ValueError:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def cambioEspecie(self):
        especie = self.cambioEspecieVar.get()
        self.especie.set(especie)

        self.alias.config(state='normal')

        self.colorCBox.config(state='readonly')

        self.fechaNac.config(state='normal')

        self.sizeCBox.config(state='readonly')

        self.razaCBox.config(values=self.razas[especie], state='readonly')
        self.razaCBox.set(self.razas[especie][0])


class EleccionCliente(ttk.Frame):
    def __init__(self, master: VeterinariaPage, mascota):
        super().__init__(master=master.padre, width=400, height=200)

        self.padre = master
        self.mascota = mascota

        ttk.Label(self, text='¿A que cliente quieres enlazar?').place(
            x=90, y=50)

        ttk.Button(self, text='Existente', width=15,
                   command=self.existente, style='Accent.TButton').place(x=20, y=140)

        ttk.Button(self, text='Nuevo Cliente', width=15,
                   style='Accent.TButton', command=self.nuevo).place(x=225, y=140)

    def existente(self):
        self.clienteExistentePage = ClienteExistentePage(
            self.padre, self.mascota)
        self.padre.padre.cambioVentana(
            self, self.clienteExistentePage, [300, 300], 'Cliente Existente')

    def nuevo(self):
        self.clienteNuevoPage = NuevoClientePage(self.padre, self.mascota)
        self.padre.padre.cambioVentana(
            self, self.clienteNuevoPage, [400, 450], 'Nuevo Cliente')


class ClienteExistentePage(ttk.Frame):
    def __init__(self, master: VeterinariaPage, mascota):
        super().__init__(master=master.padre, width=300, height=300)

        self.padre = master
        self.mascota = mascota
        self.cliente = None

        ttk.Button(self, width=10, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)

        ttk.Label(self, text='Familia a buscar').place(x=20, y=70)

        self.label = ttk.Label(self, text='').place(x=80, y=120)

        self.familia = ttk.Entry(self, width=25)
        self.familia.place(x=20, y=100)

        ttk.Button(self, text='Buscar', width=6,
                   command=self.buscar).place(x=180, y=145)

        ttk.Button(self, text='Ver Familias', width=10,
                   command=self.verFamilias).place(x=20, y=145)

        self.aceptarBoton = ttk.Button(
            self, text='Aceptar', state='disabled', command=self.aceptar)
        self.aceptarBoton.place(x=175, y=250)

    def cancelar(self):
        self.padre.padre.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
        self.destroy()

    def verFamilias(self):
        popup = tk.Toplevel(self, width=500, height=500)
        popup.title('Familias')

        familiasFrame = ttk.Frame(popup, width=500, height=500)

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('select Apellido, IdCliente from Clientes')

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        tabla = ttk.Treeview(familiasFrame, height=20, columns=titulos[1:])

        for i, titulo in enumerate(titulos):
            if i == 0:
                tabla.column('#0', width=100, anchor=tk.CENTER)
                tabla.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                tabla.column(titulo, width=100, anchor=tk.CENTER)
                tabla.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            tabla.insert('', tk.END, text=atributos[0], values=atributos[1:])

        tabla.pack()

        familiasFrame.pack()

    def buscar(self):
        familia = self.familia.get()

        if familia == '':
            showwarning(title='Error',
                        message='El campo debe de estar lleno')
            return

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:

            cursor = conexion.cursor()

            cursor.execute(
                'select * from Clientes where Apellido = ?', familia)

            resultado = cursor.fetchall()

            if len(resultado) == 1:
                self.cliente = Cliente(resultado[0])
                self.aceptarBoton.configure(
                    state='normal', style='Accent.TButton')
                showinfo(
                    title='Exito', message='El cliente ha sido encontrado con exito, aceptar para continuar')
            else:
                showerror(title='Error', message='Cliente no encontrado')

            cursor.close()

    def aceptar(self):
        self.mascota.insert(0, self.cliente.getId())
        print(self.mascota)

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'exec RegistrarMascota ?,?,?,?,?,?,?,?', self.mascota)

            bit = cursor.fetchone()
            bit = bit[0]

            if bit:
                cursor.commit()
                respuesta = showinfo(title='Exito',
                                     message='Se ha agregado a la mascota correctamente!')

                if respuesta:
                    self.padre.padre.cambioVentana(
                        self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')

            else:
                cursor.rollback()
                showerror(title='Error',
                          message='Ha ocurrido un error al agregar la mascota')


class NuevoClientePage(ttk.Frame):
    def __init__(self, master: VeterinariaPage = None, mascota: list = None):
        super().__init__(master.padre, height=450, width=400)

        self.mascota = mascota
        self.padre = master

        ttk.Button(self, text='Cancelar', command=self.cancelar,
                   width=8).place(x=10, y=10)

        ttk.Label(self, text='Apellido').place(x=20, y=90)
        self.apellido = ttk.Entry(self, width=38)
        self.apellido.place(x=20, y=120)

        ttk.Label(self, text='Numero de Cuenta').place(x=20, y=180)
        self.nrocuenta = ttk.Entry(self, width=18)
        self.nrocuenta.place(x=20, y=210)

        ttk.Label(self, text='Telefono').place(x=215, y=180)
        self.telefono = ttk.Entry(self, width=16)
        self.telefono.place(x=215, y=210)

        ttk.Label(self, text='Direccion').place(x=20, y=270)
        self.direccion = ttk.Entry(self, width=38)
        self.direccion.place(x=20, y=300)

        ttk.Button(self, text='Aceptar',
                   command=self.aceptar).place(x=275, y=400)

    def cancelar(self):
        respuesta = askquestion(title='Confirmacion',
                                message='¿Estas seguro de salir?')

        if respuesta == 'yes':
            self.padre.padre.cambioVentana(
                self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
            self.destroy()

    def aceptar(self):
        apellido = self.apellido.get()
        nrocuenta = self.nrocuenta.get()
        telefono = self.telefono.get()
        direccion = self.direccion.get()

        try:
            nrocuenta = int(nrocuenta)
            telefono = int(telefono)
        except Exception:
            showwarning(title='Error',
                        message='Uno de los datos esta en mal formato')
            return

        atributos = [apellido, nrocuenta, direccion, telefono, 0]

        if any(elemento == '' for elemento in atributos):
            showwarning(title='Error',
                        message='Todos los campos deben estar llenos')
            return

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('exec RegistrarCliente ?,?,?,?,?', atributos)

            info = cursor.fetchall()

            print(info)


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    conexiones = {'josek': ['password', 'JoseK-Laptop\SQLEXPRESS'],
                  'nangui': ['soychurro', 'BrunoPC']}

    app = App()
    user = tk.StringVar()
    password = tk.StringVar()
    app.mainloop()
