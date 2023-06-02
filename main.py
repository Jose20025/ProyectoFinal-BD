import ctypes
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning

import pyodbc
from PIL import Image, ImageTk

from models.cliente import Cliente

ctypes.windll.shcore.SetProcessDpiAwareness(2)


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
        self.tabview = ttk.Notebook(self, padding=5)

        self.mascotaFrame = ttk.Frame(self.tabview, width=1000, height=600)
        self.clienteFrame = ttk.Frame(self.tabview, width=1000, height=600)
        self.pesoFrame = ttk.Frame(self.tabview, width=1000, height=600)
        self.vacunaFrame = ttk.Frame(self.tabview, width=1000, height=600)

        self.tabview.add(self.mascotaFrame, text='Mascotas')
        self.tabview.add(self.clienteFrame, text='Clientes')
        self.tabview.add(self.pesoFrame, text='Pesos')
        self.tabview.add(self.vacunaFrame, text='Vacunas')
        self.tabview.pack()

        # ===============================> MascotaFrame
        self.botonesFrameM = ttk.Frame(
            self.mascotaFrame, style='Card.TFrame', width=430, height=360)

        ttk.Button(self.botonesFrameM, text='Consultas',
                   width=40).place(x=20, y=20)

        ttk.Button(self.botonesFrameM, text='Nueva Mascota', width=40,
                   command=self.aInsertarM).place(x=20, y=90)

        ttk.Button(self.botonesFrameM, text='Modificar una mascota',command=self.aModificarM,
                   width=40).place(x=20, y=160)

        ttk.Button(self.botonesFrameM, text='Eliminar una mascota',
                   width=40).place(x=20, y=230)

        ttk.Button(self.botonesFrameM, text='Consulta Personalizada',
                   width=40).place(x=20, y=300)

        self.imagenM = ImageTk.PhotoImage(Image.open(
            './image/logo-transparente.png').resize((200, 170)))

        ttk.Label(self.mascotaFrame, image=self.imagenM).place(x=-25, y=390)

        self.botonesFrameM.place(x=10, y=10)
        # ==============================> MascotaFrame

        # ==============================> ClienteFrame
        ttk.Button(self.clienteFrame, text='Consultas',
                   width=40).place(x=20, y=30)

        ttk.Button(self.clienteFrame, text='Nuevo Cliente', width=40,
                   command=self.aInsertarC).place(x=20, y=100)

        ttk.Button(self.clienteFrame, text='Modificar un cliente',
                   width=40).place(x=20, y=170)

        ttk.Button(self.clienteFrame, text='Eliminar un cliente',
                   width=40).place(x=20, y=240)

        ttk.Button(self.clienteFrame, text='Consulta Personalizada',
                   width=40).place(x=20, y=310)

        self.imagenC = ImageTk.PhotoImage(Image.open(
            './image/logo-transparente.png').resize((200, 170)))

        ttk.Label(self.clienteFrame, image=self.imagenC).place(x=-25, y=390)
        # ==============================> ClienteFrame

    def aInsertarM(self):
        self.eleccionCliente = EleccionCliente(self)
        self.padre.cambioVentana(self, self.eleccionCliente, [
                                 400, 200], 'Eleccion de Cliente')

    def aInsertarC(self):
        self.nuevoCliente = NuevoClientePageOnly(self)
        self.padre.cambioVentana(self, self.nuevoCliente, [
                                 400, 450], 'Eleccion de Cliente')

    def aModificarM(self):
        self.ModificarPageV = ModificarPageV(self)
        self.padre.cambioVentana(self, self.ModificarPageV, [
                                 700, 520], "Modificar Mascota")


class ModificarPageV(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=700, height=520)

        self.padre = master
        ttk.Button(self, text='Volver',
                   command=self.aPrincipal).place(x=10, y=10)

        self.tablaFrame = None

        ttk.Label(self, text='Buscar').place(x=26, y=60)
        self.espacioBuscar = ttk.Entry(self, width=16)
        self.espacioBuscar.place(x=28, y=90)
        self.botonBuscar = ttk.Button(
            self, width=8, text='Buscar', command=self.Buscar)
        self.botonBuscar.place(x=90, y=135)

        self.eleccionCampo = tk.StringVar()
        self.botonRadAlias = ttk.Radiobutton(
            self, text='Alias', variable=self.eleccionCampo, value='Alias', command=self.EleccionCampo)
        self.botonRadAlias.place(x=205, y=90)
        self.botonRadFam = ttk.Radiobutton(
            self, text='Familia', variable=self.eleccionCampo, value='Apellido', command=self.EleccionCampo)
        self.botonRadFam.place(x=300, y=90)
        self.botonRadEspecie = ttk.Radiobutton(
            self, text='Especie', variable=self.eleccionCampo, value='Especie', command=self.EleccionCampo)
        self.botonRadEspecie.place(x=405, y=90)

        self.eleccionEspecie = tk.StringVar()
        self.CBoxEspecie = ttk.Combobox(
            self, values=['Canino', 'Felino'], state='disabled', width=12)
        self.CBoxEspecie.place(x=520, y=88)

        self.Cod = tk.StringVar()
        ttk.Label(self, text='Código de Mascota').place(x=32, y=420)
        self.textoCod = ttk.Entry(self, width=12, textvariable=self.Cod)
        self.textoCod.place(x=30, y=445)
        self.botonIr = ttk.Button(
            self, text='Ir a perfil', width=10, command=self.aPerfil)
        self.botonIr.place(x=570, y=445)
        self.atributos = []

    def EleccionCampo(self):
        self.campoElegido = str(self.eleccionCampo.get())
        if self.campoElegido == 'Especie':
            self.espacioBuscar.delete(0, 30)
            self.espacioBuscar.configure(state='disabled')
            self.CBoxEspecie.configure(state='readonly')
        else:
            self.CBoxEspecie.set('')
            self.espacioBuscar.configure(state='normal')
            self.CBoxEspecie.configure(state='disabled')

    def Buscar(self):

        if self.tablaFrame:
            self.tablaFrame.pack_forget()
            self.tablaFrame.destroy()

        print(self.campoElegido)
        if self.campoElegido == 'Especie':
            self.textoBuscar = self.CBoxEspecie.get()
            print(self.textoBuscar)
        else:
            self.textoBuscar = self.espacioBuscar.get()

        self.tablaFrame = ttk.Frame(self, width=200, height=100)

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec BuscarMascota ?,? ',
                           (self.campoElegido, self.textoBuscar))
            resultados = cursor.fetchall()
            print(' ')

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            print(resultados)
            cursor.close()
            style = ttk.Style()
            style.configure("Custom.Treeview.Heading",
                            background="#a2b1bd",  # Darker background color
                            foreground="#FFFFFF",  # Brighter text color
                            font=("Helvetica", 10))  # Custom font with increased brightness

            tablaEncontrados = ttk.Treeview(
                self.tablaFrame, height=6, columns=titulos[1:], style='Custom.Treeview')
            for i, titulo in enumerate(titulos):
                if i == 0:
                    tablaEncontrados.column('#0', width=100, anchor=tk.CENTER)
                    tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            tablaEncontrados.pack()
            self.tablaFrame.place(x=60, y=210)

    def aPrincipal(self):
        self.padre.padre.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')

    def aPerfil(self):
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            print(self.Cod.get())
            cursor.execute('exec InfoMascota ?', self.Cod.get())
            print('despuecito')
            info = cursor.fetchone()
            for k in info:
                self.atributos.append(k)
            print(self.atributos)

            self.PerfilMascotaV = PerfilMascotaV(self, self.atributos)
            self.atributos = []
            self.padre.padre.cambioVentana(
                self, self.PerfilMascotaV, [410, 600], "Perfil")


class PerfilMascotaV(ttk.Frame):
    def __init__(self, master: ModificarPageV, atributos):
        super().__init__(master=master.padre.padre, width=410, height=600)
        self.padre = master
        self.atributos = atributos
        print(self.atributos)
        self.ancestro = self.padre.padre.padre

        ttk.Button(self, text='Cerrar',
                   command=self.aAnterior).place(x=10, y=10)
        ttk.Label(self, text='Código de').place(x=36, y=70)
        ttk.Label(self, text='Mascota').place(x=41, y=92)
        self.CodMuestra = ttk.Entry(
            self, state='readonly', textvariable=self.padre.Cod, width=10)
        self.CodMuestra.place(x=130, y=78)

        ttk.Label(self, text='Datos Personales', background='#7ce6dd',
                  foreground='#000000', anchor='center').place(x=130, y=150)

        ttk.Label(self, text='Alias').place(x=20, y=190)
        self.aliasNuevo = ttk.Entry(self, width=15)
        self.aliasNuevo.place(x=18, y=215)
        self.aliasNuevo.insert(0, self.atributos[0])

        self.pelo = tk.StringVar()
        self.colores = {
            'Felino': ['Negro', 'Blanco', 'Gris', 'Naranja', 'Cafe', 'Manchado'],
            'Canino': ['Negro', 'Blanco', 'Gris', 'Dorado', 'Cafe', 'Manchado']
        }
        ttk.Label(self, text='Color de pelo').place(x=20, y=280)
        self.peloNuevo = ttk.Combobox(self, width=15, height=20, textvariable=self.pelo,
                                      values=self.colores[self.atributos[6]], state='readonly')
        self.peloNuevo.place(x=18, y=305)
        self.peloNuevo.set(self.atributos[1])

        self.size = tk.StringVar()
        ttk.Label(self, text='Tamaño').place(x=20, y=370)
        self.sizeNuevo = ttk.Combobox(self, width=15, height=20, values=[
                                      'S', 'M', 'G'], textvariable=self.size, state='readonly')
        self.sizeNuevo.place(x=18, y=395)
        self.sizeNuevo.set(self.atributos[3])

        self.raza = tk.StringVar()
        self.razas = {
            'Felino': ['Siames', 'Siberiano', 'Mestizo', 'Bengali', 'Yoda', 'Birmano', 'Persa', 'Azul ruso'],
            'Canino': ['Labrador', 'Pastor Aleman', 'Caniche', 'Cocker', 'Chihuahua', 'Bulldog', 'Yorkshire', 'Pastor Ingles', 'Pincher']
        }
        ttk.Label(self, text='Raza').place(x=230, y=190)
        self.razaNuevo = ttk.Combobox(self, width=15, height=20, textvariable=self.raza,
                                      values=self.razas[self.atributos[6]], state='readonly')
        self.razaNuevo.place(x=230, y=215)
        self.razaNuevo.set(self.atributos[2])

        self.aux = tk.StringVar()
        self.aux.set(self.atributos[4])
        ttk.Label(self, text='Familia').place(x=230, y=280)
        self.famNuevo = ttk.Entry(
            self, width=15, state='readonly', textvariable=self.aux)
        self.famNuevo.place(x=230, y=305)

        ttk.Label(self, text='Codigo Familia').place(x=230, y=370)
        self.IdCliente = ttk.Entry(self, width=15)
        self.IdCliente.place(x=230, y=395)
        self.IdCliente.insert(0, self.atributos[5])

        self.famBuscarBoton = ttk.Button(
            self, text='Ver familias', width=12, command=self.buscarFamilia)
        self.famBuscarBoton.place(x=230, y=440)

        self.guardarBoton = ttk.Button(
            self, text='Guardar cambios', command=self.ModificarMascota)
        self.guardarBoton.place(x=230, y=530)

    def aAnterior(self):
        self.atributos = []
        self.padre.atributos = []
        self.padre.textoCod.delete(0, tk.END)
        self.ancestro.cambioVentana(
            self, self.padre, [700, 520], 'Modificar Mascota')
        self.destroy()

    def ModificarMascota(self):
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            respuesta = askquestion(
                'Confirmación', '¿Desea guardar los cambios?')
            if respuesta == 'yes':
                print('se guardaron los cambios')

                if self.aliasNuevo.get() != self.atributos[0]:
                    print('distinto alias')
                    cursor.execute('exec ModificarMascota ?,?,?,?',
                                   (self.atributos[7], 'Alias', self.aliasNuevo.get(), 0))
                    cursor.commit()

                if self.peloNuevo.get() != self.atributos[1]:
                    print('distinto color de pelo')
                    print(self.peloNuevo.get())
                    cursor.execute('exec ModificarMascota ?,?,?,?',
                                   (self.atributos[7], 'Color_pelo', self.peloNuevo.get(), 0))
                    cursor.commit()

                if self.sizeNuevo.get() != self.atributos[3]:
                    print('distinto tamaño')
                    cursor.execute('exec ModificarMascota ?,?,?,?',
                                   (self.atributos[7], 'Tamaño', self.sizeNuevo.get(), 0))
                    cursor.commit()

                if self.razaNuevo.get() != self.atributos[2]:
                    print('distinta raza')
                    cursor.execute('exec ModificarMascota ?,?,?,?',
                                   (self.atributos[7], 'Raza', self.razaNuevo.get(), 0))
                    cursor.commit()

                if self.IdCliente.get() != self.atributos[5]:
                    print('asociado a nuevo cliente')
                    cursor.execute('exec ModificarMascota ?,?,?,?',
                                   (self.atributos[7], 'IdCliente', self.IdCliente.get(), 0))
                    cursor.commit()
            else:
                print('que maricon')
            conexion.commit()
            cursor.execute(
                f"select * from Mascotas where CodMascota = '{self.atributos[7]}' ")
            print(cursor.fetchone())
            cursor.close()

    def buscarFamilia(self):
        self.eleccionFamilia = EleccionFamilia(self)
        self.ancestro.cambioVentana(self, self.eleccionFamilia, [
                                    400, 200], 'Eleccion de Familia')


class EleccionFamilia(ttk.Frame):
    def __init__(self, master: PerfilMascotaV):
        super().__init__(master=master.padre.padre.padre, width=400, height=200)

        self.padre = master
        self.ancestro = self.padre.padre.padre.padre
        ttk.Button(self, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)
        ttk.Label(self, text='¿Que familia quiere buscar?').place(x=90, y=70)
        ttk.Button(self, text='Existente', width=15, command=self.existente,
                   style='Accent.TButton').place(x=20, y=140)
        ttk.Button(self, text='Nueva Familia', width=15,
                   style='Accent.TButton', command=self.nuevo).place(x=225, y=140)

    def existente(self):
        self.clienteExistentePage = FamiliaExistentePage(self)
        self.ancestro.cambioVentana(self, self.clienteExistentePage, [
                                    380, 340], 'Cliente Existente')

    def nuevo(self):
        self.clienteNuevoPage = NuevaFamiliaPage(self)
        self.ancestro.cambioVentana(self, self.clienteNuevoPage, [
                                    400, 450], 'Nueva Familia')

    def cancelar(self):
        self.ancestro.cambioVentana(self, self.padre, [410, 600], "Perfil")


class FamiliaExistentePage(ttk.Frame):
    def __init__(self, master: EleccionFamilia):
        super().__init__(master=master.padre.padre.padre.padre, width=380, height=340)

        self.padre = master
        self.ancestro = self.padre.padre.padre.padre.padre
        self.cliente = None

        ttk.Button(self, width=10, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)
        ttk.Label(self, text='Familia a buscar').place(x=20, y=70)

        self.label = ttk.Label(self, text='').place(x=80, y=120)

        self.familia = ttk.Entry(self, width=25)
        self.familia.place(x=20, y=100)

        ttk.Button(self, text='Ver todas', width=10,
                   command=self.verFamilias).place(x=135, y=160)
        ttk.Button(self, text='Buscar', width=6,
                   command=self.buscar).place(x=275, y=100)

        self.IdCli = tk.StringVar()
        ttk.Label(self, text='Código Cliente').place(x=20, y=255)
        self.campoId = ttk.Entry(self, width=12, textvariable=self.IdCli)
        self.campoId.place(x=20, y=280)
        self.aceptarBoton = ttk.Button(
            self, text='Aceptar', state='disabled', command=self.aceptar)
        self.aceptarBoton.place(x=250, y=280)

        self.familiasFrame = None
        self.familiasBuscFrame = None

    def cancelar(self):
        self.ancestro.cambioVentana(
            self, self.padre, [400, 200], 'Elección de familia')
        self.destroy()

    def verFamilias(self):

        if self.familiasFrame:
            self.familiasFrame.destroy()

        popup = tk.Toplevel(self, width=500, height=500)
        popup.title('Familias')

        self.familiasFrame = ttk.Frame(popup, width=500, height=500)

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'select Apellido,NroCuenta,Telefono,IdCliente from Clientes')
            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()
            cursor.close()

            tabla = ttk.Treeview(self.familiasFrame,
                                 height=20, columns=titulos[1:])

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

                tabla.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            tabla.pack()
            self.familiasFrame.pack()

    def buscar(self):
        if self.familiasBuscFrame:
            self.familiasBuscFrame.destroy()

        familia = self.familia.get()
        if familia == '':
            showwarning(title='Error', message='El campo debe de estar lleno')
            return

        popup = tk.Toplevel(self, width=500, height=500)
        popup.title('Familias')
        self.familiasBuscFrame = ttk.Frame(popup, width=500, height=500)

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:

            cursor = conexion.cursor()
            cursor.execute(
                'select * from Clientes where Apellido = ?', familia)

            resultados = cursor.fetchall()

            titulos = []
            for t in cursor.description:
                titulos.append(t[0])

            cursor.close()

            print(len(resultados))
            if len(resultados) >= 1:
                self.aceptarBoton.configure(
                    state='normal', style='Accent.TButton')
                showinfo(title='Exito', message='Familia(s) encontrada(s)')
            else:
                showerror(title='Error', message='Cliente(s) no encontrado(s)')

            tabla = ttk.Treeview(self.familiasBuscFrame,
                                 height=20, columns=titulos[1:])

            for i, titulo in enumerate(titulos):
                if i == 0:
                    tabla.column('#0', width=100, anchor=tk.CENTER)
                    tabla.heading('#0', text=titulo, anchor=tk.CENTER)
                else:
                    tabla.column(titulo, width=100, anchor=tk.CENTER)
                    tabla.heading(titulo, text=titulo, anchor=tk.CENTER)

            for cliente in resultados:
                atributos = []
                for atributo in cliente:
                    atributos.append(atributo)
                print(atributos)
                tabla.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            tabla.pack()
            self.familiasBuscFrame.pack()

    def aceptar(self):
        IdEscrito = self.campoId.get()

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'exec VerificarExistenciaCliente ?,?', (IdEscrito, 1))
            bit = cursor.fetchone()
            bit = bit[0]
            if bit:
                cursor.execute(
                    'select Apellido from Clientes where IdCliente = ?', (IdEscrito))
                resultado = cursor.fetchone()
                apellido = resultado[0]
                print(apellido)
                cursor.close()
                self.padre.padre.aux.set(apellido)
                self.padre.padre.IdCliente.delete(0, 30)
                self.padre.padre.IdCliente.insert(0, IdEscrito)
                respuesta = showinfo(
                    title='Exito', message='Se ha enviado el Id del Cliente a la modificación')
                if respuesta:
                    self.ancestro.cambioVentana(
                        self, self.padre.padre, [410, 600], "Perfil")
            else:
                cursor.rollback()
                showerror(
                    title='Error', message='El cliente no existe. Agréguelo o escriba otro correctamente')


class NuevaFamiliaPage(ttk.Frame):
    def __init__(self, master: EleccionFamilia):
        super().__init__(master.padre, height=450, width=400)

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


class InsertarPageV(ttk.Frame):
    def __init__(self, master: VeterinariaPage = None, cliente: Cliente = None):
        super().__init__(master.padre, width=400, height=400)

        self.padre = master
        self.cliente: Cliente = cliente

        self.razas = {
            1: ['Siames', 'Siberiano', 'Mestizo', 'Bengali', 'Yoda', 'Birmano', 'Persa', 'Azul ruso'],
            2: ['Labrador', 'Pastor Aleman', 'Caniche', 'Cocker', 'Chihuahua', 'Bulldog', 'Yorkshire', 'Pastor Ingles', 'Pincher', 'Husky']
        }

        self.colores = ['Cafe', 'Blanco', 'Negro',
                        'Gris', 'Dorado', 'Verde', 'Naranja']

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

        ttk.Label(self, text='Fecha (dia-mes-año)').place(x=220, y=230)

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
                self, self.padre, [1000, 600], 'Veterinaria - Cute Pets')
            self.destroy()

    def confirmar(self):
        fecha = self.fechaNac.get()
        if fecha != '':
            if self.verificarFecha(fecha):
                fecha = self.fechaOrdenada(fecha)
                alias = self.alias.get()
                size = self.sizeCBox.get()
                color = self.colorCBox.get()
                raza = self.razaCBox.get()
                especie = 'Canino' if self.cambioEspecieVar.get() == 2 else 'Felino'

                lista = [alias, especie, raza, color, fecha, size, 0]

                if all(elemento != '' for elemento in lista):
                    lista.insert(0, self.cliente.getId())
                    with pyodbc.connect(
                            f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                        cursor = conexion.cursor()

                        cursor.execute(
                            'exec RegistrarMascota ?,?,?,?,?,?,?,?', lista)

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

                        cursor.close()
                        conexion.commit()

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
                dia, mes, año = map(int, fecha_descompuesta)
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

    def fechaOrdenada(self, fecha):
        fecha_descompuesta = fecha.split('-')

        dia, mes, año = map(int, fecha_descompuesta)

        fechaTemp = datetime(año, mes, dia)
        fechaEscrita = f'{fechaTemp.date()}'

        return fechaEscrita

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
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=400, height=200)

        self.padre = master

        ttk.Label(self, text='¿A que cliente quieres enlazar?').place(
            x=90, y=50)

        ttk.Button(self, text='Existente', width=15,
                   command=self.existente, style='Accent.TButton').place(x=20, y=140)

        ttk.Button(self, text='Nuevo Cliente', width=15,
                   style='Accent.TButton', command=self.nuevo).place(x=225, y=140)

    def existente(self):
        self.clienteExistentePage = ClienteExistentePage(
            self.padre)
        self.padre.padre.cambioVentana(
            self, self.clienteExistentePage, [300, 300], 'Cliente Existente')
        self.destroy()

    def nuevo(self):
        self.clienteNuevoPage = NuevoClientePage(self.padre)
        self.padre.padre.cambioVentana(
            self, self.clienteNuevoPage, [400, 450], 'Nuevo Cliente')
        self.destroy()


class ClienteExistentePage(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=300, height=300)

        self.padre = master
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
        self.insertarPage = InsertarPageV(self.padre, self.cliente)
        self.padre.padre.cambioVentana(self, self.insertarPage, [
                                       400, 400], 'Insertar Mascota')
        self.destroy()


class NuevoClientePageOnly(ttk.Frame):
    def __init__(self, master: VeterinariaPage = None):
        super().__init__(master.padre, height=450, width=400)

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

            bit, idcliente = info[0]

            if bit:
                cursor.commit()
                showinfo(title='Exito',
                         message='El cliente ha sido agregado correctamente!')
                self.padre.padre.cambioVentana(
                    self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
            else:
                showerror(
                    title='Error', message='Ha ocurrido un error al insertar el cliente')
                cursor.rollback()

            cursor.close()
            conexion.commit()


class NuevoClientePage(ttk.Frame):
    def __init__(self, master: VeterinariaPage = None):
        super().__init__(master.padre, height=450, width=400)

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

            bit, idcliente = info[0]

            if bit:
                atributos.insert(0, idcliente)
                self.cliente = Cliente(atributos[:-1])
                showinfo(title='Exito',
                         message='El cliente se ha creado con exito!')
                self.insertarPage = InsertarPageV(self.padre, self.cliente)
                self.padre.padre.cambioVentana(self, self.insertarPage, [
                                               400, 400], 'Insertar Mascota')
                self.destroy()
            else:
                showerror(
                    title='Error', message='Ha ocurrido un error al insertar el cliente')

            cursor.close()
            conexion.commit()


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    conexiones = {'josek': ['password', 'JoseK-Laptop\SQLEXPRESS'],
                  'nangui': ['soychurro', 'BrunoPC'],
                  'mateo_vet': ['Passw0rd', 'MATEO\MSSQLSERVER01']}

    app = App()
    user = tk.StringVar()
    password = tk.StringVar()
    app.mainloop()
