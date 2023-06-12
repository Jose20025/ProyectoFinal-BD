import ctypes
import tkinter as tk
from datetime import date
from tkinter import ttk
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning
import pyodbc
from PIL import Image, ImageTk
from models.cliente import Cliente
from models.mascota import Mascota
from models.persona import Persona

import sv_ttk

ctypes.windll.shcore.SetProcessDpiAwareness(2)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Aplicando el tema
        # self.tk.call('source', 'azure.tcl')
        # self.tk.call('set_theme', 'dark')
        sv_ttk.set_theme('dark')

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
        self.lugarCBox.set('Hotel')
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
    def __init__(self, master: App = None):
        super().__init__(master=master, width=1000, height=600)

        self.padre = master

        self.tabview = ttk.Notebook(self, padding=4)
        self.huespedFrame = ttk.Frame(self.tabview, width=1000, height=600)
        self.checkOutFrame = ttk.Frame(self.tabview, width=1000, height=600)
        self.reporteFrame = ttk.Frame(self.tabview, width=1000, height=600)

        self.tabview.add(self.huespedFrame, text='Huespedes')
        self.tabview.add(self.checkOutFrame, text='Check Out')
        self.tabview.add(self.reporteFrame, text='Reportes')

        self.tabview.bind("<<NotebookTabChanged>>", self.CambiandoSize)

        self.tabview.pack()

        ##### ZONA DE HUESPEDES #####

        ttk.Button(self.huespedFrame, text='Registrar Huésped',
                   command=self.aEleccionFamilia, width=30).place(x=20, y=20)
        ttk.Button(self.huespedFrame, text='Modificación de huésped',
                   width=30, command=self.aModificarHuesped).place(x=20, y=90)
        ttk.Button(self.huespedFrame, text='Registrar Estadía',
                   width=30, command=self.aRegistrarEstadia).place(x=20, y=160)
        ttk.Button(self.huespedFrame, text='Modificar estadía',
                   width=30, command=self.aModificarEstadia).place(x=20, y=230)

        ### PROCESO DE CHECKOUT ###

        ttk.Button(self.checkOutFrame, text='Obtener Estadías Actuales',
                   command=self.obtenerEstadias).place(x=60, y=30)
        
        self.hoy = tk.StringVar()
        self.hoy.set(date.today())
        ttk.Label(self.checkOutFrame ,text='Fecha de hoy').place(x=380,y=40)
        self.espacioHoy = ttk.Entry(self.checkOutFrame,textvariable=self.hoy,state='readonly',width=12)
        self.espacioHoy.place(x=380,y=75)

        self.codigo = tk.StringVar()
        ttk.Label(self.checkOutFrame,
                  text='Código de mascota').place(x=30, y=360)
        self.espacioCod = ttk.Entry(
            self.checkOutFrame, width=12, state='normal', textvariable=self.codigo)
        self.espacioCod.place(x=30, y=395)

        self.checkin = tk.StringVar()
        ttk.Label(self.checkOutFrame, text='CheckIn').place(x=290, y=360)
        self.espacioFecha = ttk.Entry(
            self.checkOutFrame, width=14, state='normal', textvariable=self.checkin)
        self.espacioFecha.place(x=290, y=395)

        self.habitacion = tk.StringVar()
        ttk.Label(self.checkOutFrame, text='Habitación').place(x=550, y=360)
        self.espacioHab = ttk.Entry(
            self.checkOutFrame, width=8, state='normal', textvariable=self.habitacion)
        self.espacioHab.place(x=550, y=395)

        ttk.Button(self.checkOutFrame, text='Realizar Check Out',
                   width=18, command=self.obtenerCheckOut).place(x=250, y=480)
        self.tablaFrame = None
        self.tablaCheckOut = None

        self.popup = None


        # ZONA DE REPORTE ENTRE FECHAS #
    	
        ttk.Label(self.reporteFrame,text='Huéspedes atendidos',background='#274d32').place(x=130,y=30)

        ttk.Label(self.reporteFrame,text='Desde').place(x=40,y=70)
        self.fecha1 = ttk.Entry(self.reporteFrame,width=14)
        self.fecha1.place(x=40,y=105)

        ttk.Label(self.reporteFrame,text='Hasta').place(x=240,y=70)
        self.fecha2 = ttk.Entry(self.reporteFrame,width=14)
        self.fecha2.place(x=240,y=105)

        ttk.Button(self.reporteFrame,text='Obtener Reporte',command=self.obtenerReporte).place(x=40,y=200)

    def obtenerReporte(self):
        if self.popup:
            self.popup.destroy()
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('ReporteAtendidos2 ?,? ',(self.fecha1.get(),self.fecha2.get()))
            resultados = cursor.fetchall()
            titulos = cursor.description
            self.popup = tk.Toplevel(self)
            self.popup.title('Reporte de Check Out')
            self.popup.geometry('600x600')

            self.personasFrame = ttk.Frame(self.popup, width=500, height=500)

            cursor.close()

            scroll = ttk.Scrollbar(self.popup, orient='vertical')

            self.tabla = ttk.Treeview(self.personasFrame, height=50,
                                  yscrollcommand=scroll.set)
            self.tabla.bind('<Double-1>', self.seleccion)

            scroll.config(command=self.tabla.yview)

            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tabla.column('#0', width=600,anchor='w')
                    self.tabla.heading('#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tabla.column(titulo, width=600,anchor='w')
                    self.tabla.heading(titulo, text=titulo, anchor=tk.CENTER)

            for persona in resultados:
                atributos = []
                for atributo in persona:
                    atributos.append(atributo)

                self.tabla.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tabla.pack()
            scroll.pack(side='right', fill='y')

            self.personasFrame.pack()



    def aEleccionFamilia(self):
        self.EleccionFamilia = EleccionFamiliaH(self)
        self.padre.cambioVentana(self, self.EleccionFamilia, [
                                 400, 200], 'Elección de cliente')

    def aModificarHuesped(self):
        self.ModificarHuesped = ModificarPageH(self)
        self.padre.cambioVentana(self, self.ModificarHuesped, [
                                 700, 520], "Buscar huéspedes")

    def aRegistrarEstadia(self):
        self.RegistrarEstadia = RegistrarPageH(self)
        self.padre.cambioVentana(self, self.RegistrarEstadia, [
                                 700, 520], 'Buscar huéspedes')

    def aModificarEstadia(self):
        self.BuscarEstadia = BuscarEstadia(self)
        self.padre.cambioVentana(self, self.BuscarEstadia, [
                                 700, 520], 'Búsqueda de estadías')

    def CambiandoSize(self, event):
        eleccionTab = self.tabview.tab(self.tabview.select(), "text")
        if eleccionTab == 'Check Out':
            self.padre.geometry('700x600')
        if eleccionTab == 'Reportes':
            self.padre.geometry("420x300")
        else:
            self.padre.geometry("1000x600")
        if self.tablaFrame:
            self.tablaFrame.destroy()
        if self.popup:
            self.popup.destroy()

    def obtenerCheckOut(self):
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('CheckOutHuesped2 ?,?,?,?',(self.checkin.get(),self.hoy.get(),self.codigo.get(),self.habitacion.get()))
            resultados = cursor.fetchall()
            titulos = cursor.description
            self.popup = tk.Toplevel(self)
            self.popup.title('Reporte de Check Out')
            self.popup.geometry('600x600')

            self.personasFrame = ttk.Frame(self.popup, width=500, height=500)

            cursor.close()

            scroll = ttk.Scrollbar(self.popup, orient='vertical')

            self.tabla = ttk.Treeview(self.personasFrame, height=50,
                                  yscrollcommand=scroll.set)
            self.tabla.bind('<Double-1>', self.seleccion)

            scroll.config(command=self.tabla.yview)

            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tabla.column('#0', width=600)
                    self.tabla.heading('#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tabla.column(titulo, width=600)
                    self.tabla.heading(titulo, text=titulo, anchor=tk.CENTER)

            for persona in resultados:
                atributos = []
                for atributo in persona:
                    atributos.append(atributo)

                self.tabla.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tabla.pack()
            scroll.pack(side='right', fill='y')

            self.personasFrame.pack()
        
    def obtenerEstadias(self):

        if self.tablaFrame:
            self.tablaFrame.pack_forget()
            self.tablaFrame.destroy()

        self.tablaFrame = ttk.Frame(self, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec ObtenerEstadiasActuales')
            resultados = cursor.fetchall()

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()

            self.tablaEncontrados = ttk.Treeview(
                self.tablaFrame, height=6, columns=titulos[1:])
            self.tablaEncontrados.bind('<Double-1>', self.seleccion)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontrados.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontrados.pack()
            self.tablaFrame.place(x=30, y=180)

    def seleccion(self, event=None):
        registro = self.tablaEncontrados.focus()

        self.espacioCod.configure(state='normal')
        self.espacioFecha.configure(state='normal')
        self.espacioHab.configure(state='normal')

        self.espacioCod.delete(0, tk.END)
        self.espacioFecha.delete(0, tk.END)
        self.espacioHab.delete(0, tk.END)

        self.espacioCod.insert(0, self.tablaEncontrados.item(registro)['text'])
        self.espacioFecha.insert(
            0, self.tablaEncontrados.item(registro)['values'][2])
        self.espacioHab.insert(
            0, self.tablaEncontrados.item(registro)['values'][3])

        self.espacioCod.configure(state='readonly')
        self.espacioFecha.configure(state='readonly')
        self.espacioHab.configure(state='readonly')


class EleccionFamiliaH(ttk.Frame):
    def __init__(self, master: HotelPage):
        super().__init__(master=master.padre, width=400, height=200)

        self.padre = master
        self.ancestro = self.padre.padre
        ttk.Button(self, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)
        ttk.Label(self, text='¿Usted que tipo de cliente es?').place(x=90, y=70)
        ttk.Button(self, text='Existente', width=15, command=self.existente,
                   style='Accent.TButton').place(x=20, y=140)
        ttk.Button(self, text='Nuevo', width=15,
                   style='Accent.TButton', command=self.nuevo).place(x=225, y=140)

    def existente(self):
        self.clienteExistentePage = FamiliaExistentePageH(self)
        self.ancestro.cambioVentana(self, self.clienteExistentePage, [
                                    380, 340], 'Cliente existente')

    def nuevo(self):
        self.clienteNuevoPage = NuevaFamiliaPageH(self)
        self.ancestro.cambioVentana(self, self.clienteNuevoPage, [
                                    400, 450], 'Nuevo Cliente')

    def cancelar(self):
        self.ancestro.cambioVentana(
            self, self.padre, [1000, 600], "Cute Pets - Hotel")


class FamiliaExistentePageH(ttk.Frame):
    def __init__(self, master: EleccionFamiliaH):
        super().__init__(master=master.padre.padre, width=380, height=340)

        self.padre = master
        self.ancestro = self.padre.padre.padre
        self.cliente = None

        ttk.Button(self, width=10, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)
        ttk.Label(self, text='Cliente a buscar').place(x=20, y=70)

        self.label = ttk.Label(self, text='').place(x=80, y=120)

        self.familia = ttk.Entry(self, width=25)
        self.familia.place(x=20, y=100)

        ttk.Button(self, text='Ver todos', width=10,
                   command=self.verFamilias).place(x=135, y=160)
        ttk.Button(self, text='Buscar', width=6,
                   command=self.buscarFamilia).place(x=275, y=100)

        self.IdCli = tk.StringVar()
        ttk.Label(self, text='Código Cliente').place(x=20, y=255)
        self.campoId = ttk.Entry(self, width=12, textvariable=self.IdCli)
        self.campoId.place(x=20, y=280)
        self.aceptarBoton = ttk.Button(
            self, text='Aceptar', state='disabled', command=self.aceptar)
        self.aceptarBoton.place(x=250, y=280)

        self.popupFam = None
        self.popupBuscFam = None

    def cancelar(self):
        self.ancestro.cambioVentana(
            self, self.padre, [400, 200], 'Elección de Cliente')
        self.destroy()

    def verFamilias(self):

        if self.popupFam:
            self.popupFam.destroy()
        if self.popupBuscFam:
            self.popupBuscFam.destroy()

        self.popupFam = tk.Toplevel(self, width=500, height=500)
        self.popupFam.title('Clientes')

        self.familiasFrame = ttk.Frame(self.popupFam, width=500, height=500)

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'select Apellido,NroCuenta,Telefono,IdCliente from Clientes')
            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()
            cursor.close()

            self.tablaFamilias = ttk.Treeview(self.familiasFrame,
                                              height=20, columns=titulos[1:])
            self.tablaFamilias.bind('<Double-1>', self.seleccion)

            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaFamilias.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaFamilias.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaFamilias.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaFamilias.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for cliente in clientes:
                atributos = []
                for atributo in cliente:
                    atributos.append(atributo)

                self.tablaFamilias.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaFamilias.pack()
            self.familiasFrame.pack()

    def seleccion(self, event=None):
        familia = self.tablaFamilias.focus()
        codigo = self.tablaFamilias.item(familia)['values'][2]

        self.campoId.config(state='normal')
        self.campoId.delete(0, tk.END)
        self.campoId.insert(0, codigo)
        self.campoId.config(state='readonly')
        self.aceptarBoton.config(state='normal', style='Accent.TButton')

    def buscarFamilia(self):
        if self.popupFam:
            self.popupFam.destroy()
        if self.popupBuscFam:
            self.popupBuscFam.destroy()

        familia = self.familia.get()
        if familia == '':
            showwarning(title='Error', message='El campo debe de estar lleno')
            return

        self.popupBuscFam = tk.Toplevel(self, width=500, height=500)
        self.popupBuscFam.title('Familias')
        self.familiasBuscFrame = ttk.Frame(
            self.popupBuscFam, width=500, height=500)

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:

            cursor = conexion.cursor()
            cursor.execute(
                'select Apellido,NroCuenta,Telefono,IdCliente from Clientes where Apellido = ?', familia)

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

            self.tablaBuscarFam = ttk.Treeview(self.familiasBuscFrame,
                                               height=20, columns=titulos[1:])

            self.tablaBuscarFam.bind('<Double-1>', self.seleccionBusc)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaBuscarFam.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaBuscarFam.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaBuscarFam.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaBuscarFam.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for cliente in resultados:
                atributos = []
                for atributo in cliente:
                    atributos.append(atributo)
                print(atributos)
                self.tablaBuscarFam.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaBuscarFam.pack()
            self.familiasBuscFrame.pack()

    def seleccionBusc(self, event=None):
        familia = self.tablaBuscarFam.focus()
        codigo = self.tablaBuscarFam.item(familia)['values'][2]
        print(codigo)
        self.campoId.config(state='normal')
        self.campoId.delete(0, tk.END)
        self.campoId.insert(0, codigo)
        self.campoId.config(state='readonly')
        self.aceptarBoton.config(state='normal', style='Accent.TButton')

    def aceptar(self):
        if self.popupFam:
            self.popupFam.destroy()
        if self.popupBuscFam:
            self.popupBuscFam.destroy()
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
                datos_registro = [apellido, IdEscrito]
                cursor.close()
                respuesta = showinfo(
                    title='Exito', message='Se han enviado los datos del Cliente para el registro del huésped')
                if respuesta:
                    print(datos_registro)
                    self.InsertarPageH = InsertarPageH(self, datos_registro)
                    self.ancestro.cambioVentana(
                        self, self.InsertarPageH, [500, 540], "Registro de huésped")
            else:
                cursor.rollback()
                showerror(
                    title='Error', message='El cliente no existe. Agréguelo o escriba otro correctamente')


class NuevaFamiliaPageH(ttk.Frame):
    def __init__(self, master: EleccionFamiliaH):
        super().__init__(master.padre.padre, height=450, width=400)

        self.padre = master
        self.ancestro = self.padre.padre.padre

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

        ttk.Button(self, text='Registrar',
                   command=self.aceptar).place(x=275, y=400)

    def cancelar(self):
        self.ancestro.cambioVentana(
            self, self.padre, [400, 200], 'Elección de Familia')
        self.destroy()

    def aceptar(self):
        apellido = self.apellido.get()
        nrocuenta = self.nrocuenta.get()
        telefono = self.telefono.get()
        direccion = self.direccion.get()

        if apellido.isnumeric() or not apellido.isalpha():
            showwarning('Error de campo', 'Formato de apellido no válido')
            return
        if len(str(nrocuenta)) != 10 or not str(nrocuenta).isnumeric():
            showwarning('Error de campo',
                        'Formato de Número de cuenta no válido')
            return
        if len(str(telefono)) < 8 or not str(telefono).isnumeric():
            showwarning('Error de campo', 'Formato de teléfono no válido')
            return
        if direccion.isnumeric():
            showwarning('Error de campo', 'Formato de dirección no válida')
            return

        atributos = [apellido, nrocuenta, direccion, telefono, 0]
        campos_registro = [apellido]

        if any(elemento == '' for elemento in atributos):
            showwarning(title='Error',
                        message='Todos los campos deben estar llenos')
            return

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            print('hola1')
            cursor.execute('exec RegistrarCliente ?,?,?,?,?', atributos)
            print('hola')
            resultados = cursor.fetchall()
            verificacion = resultados[0][0]
            IdParaPerfil = resultados[0][1]
            if verificacion:
                cursor.execute('commit')
                showinfo(
                    'Exito', 'Se ha registrado al cliente y enviado sus datos para el registro del huésped')
                campos_registro.append(IdParaPerfil)
                self.InsertarPageH = InsertarPageH(self, campos_registro)
                self.ancestro.cambioVentana(self, self.InsertarPageH, [
                                            460, 540], "Registro de huésped")
            else:
                cursor.execute('rollback')
                showwarning(
                    'Error en la inserción. Posible cliente duplicado o datos erroneos')


class InsertarPageH(ttk.Frame):
    def __init__(self, master: FamiliaExistentePageH | NuevaFamiliaPageH, campos_registro):
        super().__init__(master.padre.padre.padre, width=460, height=540)

        self.padre = master
        self.datosCliente = campos_registro
        self.ancestro = self.padre.padre.padre.padre

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

        ttk.Button(self, text='Registrar', style='Accent.TButton',
                   command=self.confirmar).place(x=275, y=440)

        self.apellido = tk.StringVar()
        self.codigo = tk.StringVar()
        self.apellido.set(self.datosCliente[0])
        self.codigo.set(self.datosCliente[1])
        print(self.apellido, self.codigo)

        ttk.Label(self, text='Apellido').place(x=20, y=345)
        self.campoApellido = ttk.Entry(
            self, textvariable=self.apellido, state='readonly').place(x=20, y=380)
        ttk.Label(self, text='Código Cliente').place(x=260, y=345)
        ttk.Entry(self, state='readonly', textvariable=self.codigo,
                  width=12).place(x=260, y=380)

    def volverAtras(self):

        respuesta = askquestion(title='Confirmacion', message='¿Estas seguro?')

        if respuesta == 'yes':
            self.padre.ancestro.cambioVentana(
                self, self.padre, [460, 540], "Registro de huésped")
            self.destroy()
        else:
            return

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

                if alias.isnumeric() or not alias.isalpha():
                    showwarning('Error de campo', 'Alias no válido')
                    return

                lista = [self.codigo.get(), alias, especie, raza,
                         color, fecha, size, 0]

                with pyodbc.connect(
                        f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                    cursor = conexion.cursor()

                    cursor.execute(
                        'exec RegistrarMascota ?,?,?,?,?,?,?,?', lista)

                    bit = cursor.fetchone()
                    bit = bit[0]

                    if bit:
                        cursor.commit()
                        respuesta = showinfo(
                            title='Exito', message='Se ha registrado al huésped')

                        if respuesta:
                            self.ancestro.cambioVentana(self, self.padre.padre.padre, [
                                                        1000, 600], 'Cute Pets - Hotel')
                    else:
                        cursor.rollback()
                        showerror(title='Error',
                                  message='Ha ocurrido un error al agregar la mascota')

                    cursor.close()
                    conexion.commit()

    def verificarFecha(self, fecha):
        if '-' in fecha:
            fecha_descompuesta = fecha.split('-')

            if len(fecha_descompuesta) == 3:
                dia, mes, año = map(int, fecha_descompuesta)
                try:
                    date(año, mes, dia)
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

        fechaTemp = date(año, mes, dia)
        fechaEscrita = f'{fechaTemp}'

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


class ModificarPageH(ttk.Frame):
    def __init__(self, master: HotelPage):
        super().__init__(master=master.padre, width=700, height=520)

        self.padre = master
        ttk.Button(self, text='Volver',
                   command=self.aPrincipal).place(x=10, y=10)

        self.tablaFrame = None

        ttk.Label(self, text='Ingrese su búsqueda').place(x=26, y=60)
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
            self, text='Cliente', variable=self.eleccionCampo, value='Apellido', command=self.EleccionCampo)
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

        if self.espacioBuscar.get() == '':
            if self.campoElegido == 'Especie':
                self.textoBuscar = self.CBoxEspecie.get()
            else:
                if self.textoBuscar == '':
                    showwarning(title='Error de campo',
                                message='Campo de búsqueda vacío')
                    return
        else:
            self.textoBuscar = self.espacioBuscar.get()

        self.tablaFrame = ttk.Frame(self, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec BuscarHuespedes ?,? ',
                           (self.campoElegido, self.textoBuscar))

            resultados = cursor.fetchall()

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()

            self.tablaEncontrados = ttk.Treeview(
                self.tablaFrame, height=6, columns=titulos[1:])
            self.tablaEncontrados.bind('<Double-1>', self.seleccion)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontrados.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontrados.pack()
            self.tablaFrame.place(x=60, y=195)

    def seleccion(self, event=None):
        familia = self.tablaEncontrados.focus()
        codigo = self.tablaEncontrados.item(familia)['text']

        self.textoCod.config(state='normal')
        self.textoCod.delete(0, tk.END)
        self.textoCod.insert(0, codigo)
        self.textoCod.config(state='readonly')

    def aPrincipal(self):
        self.padre.padre.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Hotel')

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

            self.PerfilMascotaV = PerfilMascotaH(self, self.atributos)
            self.atributos = []
            self.padre.padre.cambioVentana(
                self, self.PerfilMascotaV, [400, 450], "Perfil Huésped")


class PerfilMascotaH(ttk.Frame):
    def __init__(self, master: ModificarPageH, atributos):
        super().__init__(master=master.padre.padre, width=400, height=450)
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

        self.aux = tk.StringVar()
        self.aux.set(self.atributos[4])
        ttk.Label(self, text='Familia').place(x=20, y=280)
        self.famNuevo = ttk.Entry(
            self, width=15, state='readonly', textvariable=self.aux)
        self.famNuevo.place(x=18, y=305)

        self.size = tk.StringVar()
        self.size.set(self.atributos[3])
        ttk.Label(self, text='Tamaño').place(x=230, y=190)
        self.sizeNuevo = ttk.Combobox(self, width=15, height=20, values=[
                                      'S', 'M', 'G'], textvariable=self.size, state='readonly')
        self.sizeNuevo.place(x=230, y=215)

        self.guardarBoton = ttk.Button(
            self, text='Guardar cambios', command=self.ModificarMascota)
        self.guardarBoton.place(x=230, y=380)

    def aAnterior(self):
        self.atributos = []
        self.padre.atributos = []
        self.padre.textoCod.delete(0, tk.END)
        if self.padre.tablaFrame:
            self.padre.tablaFrame.pack_forget()
            self.padre.tablaFrame.destroy()
        self.ancestro.cambioVentana(
            self, self.padre, [700, 520], 'Modificar Mascota')
        self.destroy()

    def ModificarMascota(self):
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            respuesta = askquestion(
                'Confirmación', '¿Desea guardar los cambios?')
            if respuesta == 'yes':
                showinfo('Exito', 'Cambios guardados')

                if self.aliasNuevo.get() != self.atributos[0]:
                    if self.aliasNuevo.get().isnumeric():
                        print('alias es numerico')
                        showerror('Error de campo',
                                  'El Alias no puede ser numérico')
                        return
                    else:
                        print('distinto alias')
                        cursor.execute('exec ModificarMascota ?,?,?,?',
                                       (self.atributos[7], 'Alias', self.aliasNuevo.get(), 0))
                        cursor.commit()

                if self.sizeNuevo.get() != self.atributos[3]:
                    print('distinto tamaño')
                    cursor.execute('exec ModificarMascota ?,?,?,?',
                                   (self.atributos[7], 'Tamaño', self.sizeNuevo.get(), 0))
                    cursor.commit()

            cursor.execute('commit')
            if self.padre.tablaFrame:
                self.padre.tablaFrame.pack_forget()
                self.padre.tablaFrame.destroy()
            self.ancestro.cambioVentana(
                self, self.padre, [700, 520], 'Buscar huéspedes')


class RegistrarPageH(ttk.Frame):
    def __init__(self, master: HotelPage):
        super().__init__(master=master.padre, height=520, width=700)
        self.padre = master
        self.ancestro = self.padre.padre

        ttk.Button(self, text='Volver',
                   command=self.aPrincipal).place(x=10, y=10)

        self.tablaFrame = None

        ttk.Label(self, text='Ingrese su búsqueda').place(x=26, y=60)
        self.espacioBuscar = ttk.Entry(self, width=16)
        self.espacioBuscar.place(x=28, y=90)
        self.botonBuscar = ttk.Button(
            self, width=8, text='Buscar', command=self.Buscar)
        self.botonBuscar.place(x=90, y=135)

        self.deVeterinaria = tk.BooleanVar()
        self.vetchk = ttk.Checkbutton(
            self, text='¿Es paciente?', variable=self.deVeterinaria)
        self.vetchk.place(x=300, y=20)

        self.eleccionCampo = tk.StringVar()
        self.botonRadAlias = ttk.Radiobutton(
            self, text='Alias', variable=self.eleccionCampo, value='Alias', command=self.EleccionCampo)
        self.botonRadAlias.place(x=205, y=90)
        self.botonRadFam = ttk.Radiobutton(
            self, text='Cliente', variable=self.eleccionCampo, value='Apellido', command=self.EleccionCampo)
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
            self, text='Ir al registro', width=11, command=self.aRegistro)
        self.botonIr.place(x=570, y=445)
        self.atributos = []
        self.habitaciones = []

    def aRegistro(self):
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec VerificarEstadiaExistente ?,? ',(self.Cod.get(),0))
            bit = cursor.fetchone()[0]
            print(bit)
            if bit:
                showinfo('Aviso','La mascota está hospedada actualmente')
                return
            cursor.execute('InfoMascota ?', (self.Cod.get()))
            datos = cursor.fetchone()
            for d in datos:
                self.atributos.append(d)
            cursor.execute(
                "select NroHab from Habitaciones where Disponible= 'D' order by try_cast(NroHab as int), NroHab desc")
            habs = cursor.fetchall()
            for h in habs:
                self.habitaciones.append(h[0])

        self.RegistroEstadia = RegistroEstadia(
            self, self.atributos, self.habitaciones)
        self.ancestro.cambioVentana(self, self.RegistroEstadia, [
                                    510, 620], 'Registro de estadía')

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
        self.textoBuscar = self.espacioBuscar.get()
        self.campoElegido = str(self.eleccionCampo.get())
        if self.espacioBuscar.get() == '':
            if self.campoElegido == 'Especie':
                self.textoBuscar = self.CBoxEspecie.get()
            else:
                if self.textoBuscar == '':
                    showwarning(title='Error de campo',
                                message='Formato de búsqueda no válido')
                    return
        else:
            self.textoBuscar = self.espacioBuscar.get()
        self.tablaFrame = ttk.Frame(self, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            if self.deVeterinaria.get():
                cursor.execute('exec BuscarMascota ?,? ',
                               (self.campoElegido, self.textoBuscar))
            else:
                cursor.execute('exec BuscarHuespedes ?,? ',
                               (self.campoElegido, self.textoBuscar))
            resultados = cursor.fetchall()

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()

            self.tablaEncontrados = ttk.Treeview(
                self.tablaFrame, height=6, columns=titulos[1:])
            self.tablaEncontrados.bind('<Double-1>', self.seleccion)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontrados.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontrados.pack()
            self.tablaFrame.place(x=60, y=195)

    def seleccion(self, event=None):
        familia = self.tablaEncontrados.focus()
        codigo = self.tablaEncontrados.item(familia)['text']

        self.textoCod.config(state='normal')
        self.textoCod.delete(0, tk.END)
        self.textoCod.insert(0, codigo)
        self.textoCod.config(state='readonly')

    def aPrincipal(self):
        self.padre.padre.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Hotel')


class RegistroEstadia(ttk.Frame):
    def __init__(self, master: RegistrarPageH, atributos, habitaciones):
        super().__init__(master=master.padre.padre, width=510, height=620)

        self.habitaciones = habitaciones
        self.atributos = atributos
        self.padre = master
        self.ancestro = self.padre.padre.padre
        ttk.Button(self, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)

        self.fecha = tk.StringVar()
        self.fecha.set(date.today())
        ttk.Label(self, text='Fecha de hoy').place(x=170, y=32)
        ttk.Entry(self, state='readonly', textvariable=self.fecha,
                  width=14).place(x=300, y=30)

        self.CodMascota = tk.StringVar()
        self.CodMascota.set(self.atributos[7])
        ttk.Label(self, text='Código Mascota').place(x=20, y=120)
        ttk.Entry(self, textvariable=self.CodMascota,
                  state='readonly', width=8).place(x=20, y=155)

        ttk.Label(self, text='Habitación').place(x=200, y=120)
        self.HabCBox = ttk.Combobox(
            self, state='readonly', width=7, values=self.habitaciones)
        self.HabCBox.place(x=200, y=155)

        ttk.Label(self, text='Dias').place(x=340, y=120)
        self.cantDias = ttk.Entry(self, width=5)
        self.cantDias.place(x=340, y=155)

        ttk.Label(self, text='Especiales',
                  background='#58bf85').place(x=50, y=240)
        ttk.Label(self, text='Adicionales',
                  background='#58bf85').place(x=190, y=240)
        ttk.Label(self, text='Cantitdad',
                  background='#58bf85').place(x=330, y=240)

        self.food = tk.BooleanVar()
        self.med = tk.BooleanVar()
        self.paseo = tk.BooleanVar()
        self.juego = tk.BooleanVar()
        self.ducha = tk.BooleanVar()
        self.corte = tk.BooleanVar()

        self.foodchk = ttk.Checkbutton(
            self, text='Alimentacion', variable=self.food)
        self.foodchk.place(x=20, y=300)
        self.medchk = ttk.Checkbutton(
            self, text='Cuidado médico', variable=self.med)
        self.medchk.place(x=20, y=350)
        self.paseochk = ttk.Checkbutton(
            self, text='Paseos', variable=self.paseo)
        self.paseochk.place(x=200, y=300)
        self.juegochk = ttk.Checkbutton(
            self, text='Juego', variable=self.juego)
        self.juegochk.place(x=200, y=350)
        self.duchachk = ttk.Checkbutton(
            self, text='Baños', variable=self.ducha)
        self.duchachk.place(x=200, y=400)
        self.cortechk = ttk.Checkbutton(
            self, text='Corte uñas', variable=self.corte)
        self.cortechk.place(x=200, y=450)

        self.espacioPaseo = ttk.Entry(self, width=5, state='normal')
        self.espacioPaseo.place(x=340, y=300)
        self.espacioJuego = ttk.Entry(self, width=5, state='normal')
        self.espacioJuego.place(x=340, y=350)
        self.espacioDucha = ttk.Entry(self, width=5, state='normal')
        self.espacioDucha.place(x=340, y=400)

        ttk.Button(self, text='Registrar',
                   command=self.registrar).place(x=380, y=560)

    def registrar(self):

        habitacion = self.HabCBox.get()
        dias = int(self.cantDias.get())
        cod = self.atributos[7]

        if not self.espacioDucha.get().isnumeric() and self.espacioDucha.get() != '':
            showwarning('Error de campo', 'Indique una cantidad correcta')
            return
        if not self.espacioJuego.get().isnumeric() and self.espacioJuego.get() != '':
            showwarning('Error de campo', 'Indique una cantidad correcta')
            return
        if not self.espacioPaseo.get().isnumeric() and self.espacioPaseo.get() != '':
            showwarning('Error de campo', 'Indique una cantidad correcta')
            return

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec RegistrarEstadia ?,?,?,?,?', (
                str(date.today()), cod, habitacion, dias, 0))
            bit1 = cursor.fetchone()
            cursor.commit()

            if bit1:
                if self.food.get():
                    cursor.execute('exec RegistrarRequerimiento ?,?,?,?,?,?,?', (
                        cod, 'S04', str(date.today()), None, habitacion, dias, 0))
                    cursor.commit()

                if self.med.get():
                    cursor.execute('exec RegistrarRequerimiento ?,?,?,?,?,?,?', (
                        cod, 'S05', str(date.today()), None, habitacion, dias, 0))
                    cursor.commit()

                if self.paseo.get():
                    cursor.execute('exec RegistrarRequerimiento ?,?,?,?,?,?,?', (
                        cod, 'S03', str(date.today()), int(self.espacioPaseo.get()), habitacion, dias, 0))
                    cursor.commit()

                if self.juego.get():
                    cursor.execute('exec RegistrarRequerimiento ?,?,?,?,?,?,?', (
                        cod, 'S06', str(date.today()), int(self.espacioJuego.get()), habitacion, dias, 0))
                    cursor.commit()

                if self.ducha.get():
                    cursor.execute('exec RegistrarRequerimiento ?,?,?,?,?,?,?', (
                        cod, 'S01', str(date.today()), int(self.espacioDucha.get()), habitacion, dias, 0))
                    cursor.commit()

                if self.corte.get():
                    cursor.execute('exec RegistrarRequerimiento ?,?,?,?,?,?,?', (
                        cod, 'S02', str(date.today()), 1, habitacion, dias, 0))
                    cursor.commit()
            else:
                showerror('Error de registro',
                          'Ocurrio un error al registrar la estadía')
                return

            showinfo('Exito', 'Estadía registrada \nVolviendo al inicio')
            cursor.execute('commit')
            conexion.commit()

        self.ancestro.cambioVentana(self, self.padre.padre, [
                                    1000, 600], 'Cute Pets - Hotel')

    def cancelar(self):
        self.destroy()
        self.ancestro.cambioVentana(
            self, self.padre, [700, 520], 'Buscar huéspedes')


class BuscarEstadia(ttk.Frame):
    def __init__(self, master: HotelPage):
        super().__init__(master=master.padre, width=700, height=520)

        self.padre = master
        self.ancestro = self.padre.padre
        self.tablaFrame = None

        ttk.Button(self, text='Volver', command=self.volver).place(x=10, y=10)

        ttk.Button(self, text='Obtener Estadías Actuales',
                   command=self.obtenerEstadias).place(x=240, y=70)

        self.codigo = tk.StringVar()
        ttk.Label(text='Código de mascota').place(x=30, y=360)
        self.espacioCod = ttk.Entry(
            self, width=12, state='normal', textvariable=self.codigo)
        self.espacioCod.place(x=30, y=395)

        self.checkin = tk.StringVar()
        ttk.Label(self, text='CheckIn').place(x=290, y=360)
        self.espacioFecha = ttk.Entry(
            self, width=14, state='normal', textvariable=self.checkin)
        self.espacioFecha.place(x=290, y=395)

        self.habitacion = tk.StringVar()
        ttk.Label(self, text='Habitación').place(x=550, y=360)
        self.espacioHab = ttk.Entry(
            self, width=8, state='normal', textvariable=self.habitacion)
        self.espacioHab.place(x=550, y=395)

        ttk.Button(self, text='Ir a modificar', width=12,
                   command=self.aEdicion).place(x=550, y=460)

        self.dias = 0
        self.hab = None

    def obtenerEstadias(self):

        if self.tablaFrame:
            self.tablaFrame.pack_forget()
            self.tablaFrame.destroy()

        self.tablaFrame = ttk.Frame(self, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec ObtenerEstadiasActuales')
            resultados = cursor.fetchall()

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()

            self.tablaEncontrados = ttk.Treeview(
                self.tablaFrame, height=6, columns=titulos[1:])
            self.tablaEncontrados.bind('<Double-1>', self.seleccion)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontrados.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontrados.pack()
            self.tablaFrame.place(x=30, y=140)

    def seleccion(self, event=None):
        registro = self.tablaEncontrados.focus()

        self.espacioCod.configure(state='normal')
        self.espacioFecha.configure(state='normal')
        self.espacioHab.configure(state='normal')

        self.espacioCod.delete(0, tk.END)
        self.espacioFecha.delete(0, tk.END)
        self.espacioHab.delete(0, tk.END)

        self.espacioCod.insert(0, self.tablaEncontrados.item(registro)['text'])
        self.espacioFecha.insert(
            0, self.tablaEncontrados.item(registro)['values'][2])
        self.espacioHab.insert(
            0, self.tablaEncontrados.item(registro)['values'][3])
        self.dias = self.tablaEncontrados.item(registro)['values'][4]

        self.hab = self.tablaEncontrados.item(registro)['values'][3]

        self.espacioCod.configure(state='readonly')
        self.espacioFecha.configure(state='readonly')
        self.espacioHab.configure(state='readonly')

        self.habitaciones = []
        self.servicios = []

    def volver(self):
        self.destroy()
        self.ancestro.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Hotel')

    def aEdicion(self):
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'select NroHab from Habitaciones where Disponible=?', ('D'))
            habs = cursor.fetchall()
            for h in habs:
                self.habitaciones.append(h[0])
            cursor.execute('exec ServiciosSolicitados ?,?,?', (self.espacioCod.get(
            ), self.espacioFecha.get(), self.espacioHab.get()))
            servicios = cursor.fetchall()
            for s in servicios:
                self.servicios.append(s)

            print(servicios)
        self.EdicionEstadia = EdicionEstadia(
            self, self.habitaciones, self.servicios, self.dias, self.hab)
        self.ancestro.cambioVentana(self, self.EdicionEstadia, [
                                    510, 620], 'Edición de estadía')


class EdicionEstadia(ttk.Frame):
    def __init__(self, master: BuscarEstadia, habitaciones, servicios, dias, hab):
        super().__init__(master=master.padre.padre, width=510, height=620)
        self.servicios = servicios
        self.habitaciones = habitaciones
        self.padre = master
        self.dias = dias
        self.hab = hab
        self.ancestro = self.padre.padre.padre
        ttk.Button(self, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)

        self.CodMascota = tk.StringVar()
        self.CodMascota.set(self.padre.espacioCod.get())
        ttk.Label(self, text='Código Mascota', width=14).place(x=20, y=120)
        ttk.Entry(self, textvariable=self.CodMascota,
                  state='readonly', width=8).place(x=20, y=155)

        ttk.Label(self, text='Habitación').place(x=200, y=120)
        self.HabCBox = ttk.Combobox(
            self, state='readonly', width=7, values=self.habitaciones)
        self.HabCBox.place(x=200, y=155)

        self.fecha = tk.StringVar()
        self.fecha.set(self.padre.espacioFecha.get())
        ttk.Label(self, text='Fecha CheckIn').place(x=340, y=120)
        ttk.Entry(self, textvariable=self.fecha,
                  state='readonly', width=12).place(x=340, y=155)

        ttk.Label(self, text='Servicios Solicitados',
                  background='#58bf85').place(x=80, y=240)

        self.food = tk.BooleanVar()
        self.med = tk.BooleanVar()
        self.paseo = tk.BooleanVar()
        self.juego = tk.BooleanVar()
        self.ducha = tk.BooleanVar()
        self.corte = tk.BooleanVar()

        self.foodchk = ttk.Checkbutton(
            self, text='Alimentacion', variable=self.food)
        self.foodchk.place(x=20, y=300)
        self.medchk = ttk.Checkbutton(
            self, text='Cuidado médico', variable=self.med)
        self.medchk.place(x=20, y=350)
        self.paseochk = ttk.Checkbutton(
            self, text='Paseos', variable=self.paseo)
        self.paseochk.place(x=200, y=300)
        self.juegochk = ttk.Checkbutton(
            self, text='Juego', variable=self.juego)
        self.juegochk.place(x=200, y=350)
        self.duchachk = ttk.Checkbutton(
            self, text='Baños', variable=self.ducha)
        self.duchachk.place(x=200, y=400)
        self.cortechk = ttk.Checkbutton(
            self, text='Corte uñas', variable=self.corte)
        self.cortechk.place(x=200, y=450)

        self.espacioPaseo = ttk.Entry(self, width=5, state='normal')
        self.espacioPaseo.place(x=340, y=300)
        self.espacioJuego = ttk.Entry(self, width=5, state='normal')
        self.espacioJuego.place(x=340, y=350)
        self.espacioDucha = ttk.Entry(self, width=5, state='normal')
        self.espacioDucha.place(x=340, y=400)

        for k in self.servicios:
            if k[0] == 'Baño':
                self.ducha.set(True)
                self.espacioDucha.insert(0, k[1])
            if k[0] == 'Corte uñas':
                self.corte.set(True)
            if k[0] == 'Paseo':
                self.paseo.set(True)
                self.espacioPaseo.insert(0, k[1])
            if k[0] == 'Alimentacion':
                self.food.set(True)
            if k[0] == 'Cuidado medico':
                self.med.set(True)
            if k[0] == 'Juegos':
                self.juego.set(True)
                self.espacioJuego.insert(0, k[1])

        self.guardado = {}

        for k in self.servicios:
            self.guardado[k[0]] = k[1]

        ttk.Button(self, text='Guardar Cambios',
                   command=self.modificar).place(x=340, y=550)

    def cancelar(self):
        self.destroy()
        self.ancestro.cambioVentana(
            self, self.padre, [700, 520], 'Búsqueda de estadías')

    def modificar(self):

        with pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            resp = askquestion('Confirmación', '¿Desea guardar los cambios?')
            if resp == 'yes':
                showinfo('Éxito', 'Cambios guardados')
            else:
                return

    # viendo cantidad de duchas
            if 'Baño' in self.guardado:
                print('ducha seleccionado antes')
                if self.ducha.get() == True:
                    if int(self.espacioDucha.get()) != self.guardado['Baño']:
                        cursor.execute('ModificarRequerimiento ?,?,?,?,?,?,? ',
                                       ('S01', self.fecha.get(), self.CodMascota.get(), self.hab, 'Cantidad', int(self.espacioDucha.get()), 0))
                        cursor.commit()
                else:
                    cursor.execute('EliminarRequerimiento ?,?,?,?,?',
                                   ('S01', self.fecha.get(), self.CodMascota.get(), self.hab, 0))
                    cursor.commit()
            else:
                if self.ducha.get():
                    print('nuevo baño')
                    cursor.execute('RegistrarRequerimiento ?,?,?,?,?,?,?',
                                   (self.CodMascota.get(), 'S01', self.fecha.get(), int(self.espacioDucha.get()), self.hab, self.padre.dias, 0))
                    cursor.commit()

    # viendo corte de uñas

            if 'Corte uñas' in self.guardado:
                print('corte seleccionado antes')

                if self.corte.get() != True:
                    cursor.execute('EliminarRequerimiento ?,?,?,?,?',
                                   ('S02', self.fecha.get(), self.CodMascota.get(), self.hab, 0))
                    cursor.commit()
            else:
                if self.ducha.get():
                    print('nuevo ducha')
                    cursor.execute('RegistrarRequerimiento ?,?,?,?,?,?,?',
                                   (self.CodMascota.get(), 'S01', self.fecha.get(), int(self.espacioDucha.get()), self.hab, self.padre.dias, 0))
                    cursor.commit()
    # viendo paseos

            if 'Paseo' in self.guardado:
                print('paseo seleccionado antes')

                if self.ducha.get() == True:
                    if int(self.espacioPaseo.get()) != self.guardado['Paseo']:
                        cursor.execute('ModificarRequerimiento ?,?,?,?,?,?,? ',
                                       ('S03', self.fecha.get(), self.CodMascota.get(), self.hab, 'Cantidad', int(self.espacioPaseo.get()), 0))
                        cursor.commit()
                else:
                    cursor.execute('EliminarRequerimiento ?,?,?,?,?',
                                   ('S03', self.fecha.get(), self.CodMascota.get(), self.hab, 0))
                    cursor.commit()
            else:
                if self.paseo.get():
                    print('nuevo paseo')
                    cursor.execute('RegistrarRequerimiento ?,?,?,?,?,?,?',
                                   (self.CodMascota.get(), 'S03', self.fecha.get(), int(self.espacioPaseo.get()), self.hab, self.padre.dias, 0))
                    cursor.commit()

    # viendo alimentación especial

            if 'Alimentacion' in self.guardado:
                print('comida seleccionado antes')

                if self.food.get() != True:
                    cursor.execute('EliminarRequerimiento ?,?,?,?,?',
                                   ('S04', self.fecha.get(), self.CodMascota.get(), self.hab, 0))
                    cursor.commit()
            else:
                if self.food.get():
                    print('nuevo comida')
                    cursor.execute('RegistrarRequerimiento ?,?,?,?,?,?,?',
                                   (self.CodMascota.get(), 'S04', self.fecha.get(), None, self.hab, self.padre.dias, 0))
                    cursor.commit()

    # viendo atencion médica

            if 'Cuidado medico' in self.guardado:
                print('mecico seleccionado antes')

                if self.med.get() != True:
                    cursor.execute('EliminarRequerimiento ?,?,?,?,?',
                                   ('S05', self.fecha.get(), self.CodMascota.get(), self.hab, 0))
                    cursor.commit()
            else:
                if self.med.get():
                    print('nuevo comida')
                    cursor.execute('RegistrarRequerimiento ?,?,?,?,?,?,?',
                                   (self.CodMascota.get(), 'S05', self.fecha.get(), None, self.hab, self.padre.dias, 0))
                    cursor.commit()
    # viendo juegos

            if 'Juegos' in self.guardado:
                print('juego seleccionado antes')

                if self.juego.get() == True:
                    if int(self.espacioJuego.get()) != self.guardado['Juegos']:
                        cursor.execute('ModificarRequerimiento ?,?,?,?,?,?,? ',
                                       ('S06', self.fecha.get(), self.CodMascota.get(), self.hab, 'Cantidad', int(self.espacioPaseo.get()), 0))
                        cursor.commit()
                else:
                    cursor.execute('EliminarRequerimiento ?,?,?,?,?',
                                   ('S06', self.fecha.get(), self.CodMascota.get(), self.hab, 0))
                    cursor.commit()
            else:
                if self.juego.get():
                    print('nuevo juego')
                    cursor.execute('RegistrarRequerimiento ?,?,?,?,?,?,?',
                                   (self.CodMascota.get(), 'S06', self.fecha.get(), int(self.espacioJuego.get()), self.hab, self.padre.dias, 0))
                    cursor.commit()

            if self.HabCBox.get() != self.padre.hab:
                print('cambio de habitación')
                cursor.execute('ModificarEstadia ?,?,?,?,?,? ',
                               (self.fecha.get(),self.CodMascota.get(),self.hab,'NroHab',self.HabCBox.get(),0))

            cursor.execute('commit')

        self.ancestro.cambioVentana(self, self.padre.padre, [
                                    1000, 600], 'Cute Pets - Hotel')


## VETERINARIA ##


class VeterinariaPage(ttk.Frame):
    def __init__(self, master: App = None):
        super().__init__(master=master, width=1000, height=600)

        self.padre = master

        self.tabview = ttk.Notebook(self, padding=4)
        # self.tabview.bind('<<NotebookTabChanged>>',self.CambiandoSize)

        self.mascotaFrame = ttk.Frame(self.tabview, width=1000, height=600)
        self.clienteFrame = ttk.Frame(self.tabview, width=1000, height=600)
        self.pesoFrame = ttk.Frame(self.tabview, width=1800, height=600)
        self.vacunaFrame = ttk.Frame(self.tabview, width=1000, height=600)

        self.tabview.add(self.mascotaFrame, text='Mascotas')
        self.tabview.add(self.clienteFrame, text='Clientes')
        self.tabview.add(self.pesoFrame, text='Pesos')
        self.tabview.add(self.vacunaFrame, text='Vacunas')

        self.tabview.pack()

        #### SECCIÓN DE MASCOTAS #####

        self.botonesFrameM = ttk.Frame(
            self.mascotaFrame, style='Card.TFrame', width=335, height=360)

        # TODO boton de consultas para mascotas
        ttk.Button(self.botonesFrameM, text='Consultas',
                   width=30).place(x=20, y=20)

        ttk.Button(self.botonesFrameM, text='Nueva Mascota', width=30,
                   command=self.aInsertarM).place(x=20, y=90)

        ttk.Button(self.botonesFrameM, text='Información', command=self.aInfoM,
                   width=40).place(x=20, y=160)

        ttk.Button(self.botonesFrameM, text='Edición', command=self.aModificarM,
                   width=40).place(x=20, y=230)

        self.imagenM = ImageTk.PhotoImage(Image.open(
            './image/logo-transparente.png').resize((200, 170)))

        ttk.Label(self.mascotaFrame, image=self.imagenM).place(x=-25, y=370)

        self.inicializarTablaM()
        self.botonesFrameM.place(x=10, y=10)
        # ==============================> MascotaFrame

        # ==============================> ClienteFrame
        self.botonesFrameC = ttk.Frame(
            self.clienteFrame, style='Card.TFrame', width=335, height=360)
        self.botonesFrameM.place(x=0, y=0)

        #### SECCIÓN DE CLIENTES #####

        ttk.Button(self.clienteFrame, text='Consultas',
                   width=40).place(x=20, y=30)

        # TODO boton de consultas para clientes
        ttk.Button(self.botonesFrameC, text='Consultas',
                   width=30).place(x=20, y=20)

        ttk.Button(self.botonesFrameC, text='Nuevo Cliente', width=30,
                   command=self.aInsertarC).place(x=20, y=90)

        ttk.Button(self.botonesFrameC, text='Modificar un cliente',
                   width=30, command=self.aModificarC).place(x=20, y=160)

        ttk.Button(self.botonesFrameC, text='Eliminar un cliente',
                   width=30).place(x=20, y=230)

        ttk.Button(self.botonesFrameC, text='Agregar una persona a una familia', command=self.nuevaPersonaFamilia,
                   width=30).place(x=20, y=300)

        self.imagenC = ImageTk.PhotoImage(Image.open(
            './image/logo-transparente.png').resize((200, 170)))

        ttk.Label(self.clienteFrame, image=self.imagenC).place(x=-25, y=370)
        self.inicializarTablaC()
        self.botonesFrameC.place(x=10, y=10)
        # ==============================> ClienteFrame
        ttk.Label(self.clienteFrame, image=self.imagenC).place(x=-25, y=390)

        #### SECCIÓN DE PESOS #####

        self.tablaMascotasPesos = None
        ttk.Label(self.pesoFrame, text='Ingrese su búsqueda').place(x=26, y=25)
        self.espacioBuscarPeso = ttk.Entry(self.pesoFrame, width=16)
        self.espacioBuscarPeso.place(x=28, y=60)
        self.botonBuscar = ttk.Button(
            self.pesoFrame, width=8, text='Buscar', command=self.Buscar)
        self.botonBuscar.place(x=90, y=105)

        self.eleccionCampo = tk.StringVar()
        self.botonRadAlias = ttk.Radiobutton(
            self.pesoFrame, text='Alias', variable=self.eleccionCampo, value='Alias', command=self.EleccionCampo)
        self.botonRadAlias.place(x=205, y=60)
        self.botonRadFam = ttk.Radiobutton(
            self.pesoFrame, text='Familia', variable=self.eleccionCampo, value='Apellido', command=self.EleccionCampo)
        self.botonRadFam.place(x=300, y=60)
        self.botonRadEspecie = ttk.Radiobutton(
            self.pesoFrame, text='Especie', variable=self.eleccionCampo, value='Especie', command=self.EleccionCampo)
        self.botonRadEspecie.place(x=405, y=60)

        self.eleccionEspecie = tk.StringVar()
        self.CBoxEspecie = ttk.Combobox(
            self.pesoFrame, values=['Canino', 'Felino'], state='disabled', width=12)
        self.CBoxEspecie.place(x=520, y=58)

        self.Cod = tk.StringVar()
        ttk.Label(self.pesoFrame, text='Código de Mascota').place(x=480, y=410)
        self.textoCod = ttk.Entry(
            self.pesoFrame, width=12, textvariable=self.Cod)
        self.textoCod.place(x=480, y=445)

        barra = ttk.Separator(self.pesoFrame, orient=tk.VERTICAL)
        barra.place(x=665, y=0, height=590, width=2)

        ttk.Label(self.pesoFrame, text='Fecha de hoy').place(x=775, y=30)
        self.fecha = tk.StringVar()
        self.fecha.set(date.today())
        self.peso = tk.StringVar()
        self.FechaHoy = ttk.Entry(
            self.pesoFrame, width=11, textvariable=self.fecha)
        self.FechaHoy.place(x=775, y=65)
        ttk.Label(self.pesoFrame, text='Peso registrado').place(x=700, y=250)
        self.espacioPeso = ttk.Entry(
            self.pesoFrame, width=12, textvariable=self.peso)
        self.espacioPeso.place(x=700, y=285)
        self.botonRegPeso = ttk.Button(
            self.pesoFrame, width=9, text='Registrar', command=self.RegistrarPeso)
        self.botonRegPeso.place(x=850, y=285)

        self.botonHistPeso = ttk.Button(
            self.pesoFrame, width=14, text='Obtener historial de pesos', command=self.ObtenerHistorialPesos)
        self.botonHistPeso.place(x=710, y=490)

        self.popupPesos = None

        #### SECCION DE VACUNAS ####

        self.tablaMascotasVacunas = None

        ttk.Label(self.vacunaFrame, text='Ingrese su búsqueda').place(
            x=26, y=25)
        self.espacioBuscarVac = ttk.Entry(self.vacunaFrame, width=16)
        self.espacioBuscarVac.place(x=28, y=60)
        self.botonBuscarVac = ttk.Button(
            self.vacunaFrame, width=8, text='Buscar', command=self.BuscarVac)
        self.botonBuscarVac.place(x=90, y=105)

        self.eleccionCampoVac = tk.StringVar()
        self.botonRadAliasVac = ttk.Radiobutton(
            self.vacunaFrame, text='Alias', variable=self.eleccionCampoVac, value='Alias', command=self.EleccionCampo)
        self.botonRadAliasVac.place(x=205, y=60)
        self.botonRadFamVac = ttk.Radiobutton(
            self.vacunaFrame, text='Familia', variable=self.eleccionCampoVac, value='Apellido', command=self.EleccionCampo)
        self.botonRadFamVac.place(x=300, y=60)
        self.botonRadEspecieVac = ttk.Radiobutton(
            self.vacunaFrame, text='Especie', variable=self.eleccionCampoVac, value='Especie', command=self.EleccionCampo)
        self.botonRadEspecieVac.place(x=405, y=60)

        self.eleccionEspecieVac = tk.StringVar()
        self.CBoxEspecieVac = ttk.Combobox(
            self.vacunaFrame, values=['Canino', 'Felino'], state='disabled', width=12, textvariable=self.eleccionEspecieVac)
        self.CBoxEspecieVac.place(x=520, y=58)

        self.CodVac = tk.StringVar()
        ttk.Label(self.vacunaFrame, text='Código de Mascota').place(
            x=480, y=410)
        self.textoCodVac = ttk.Entry(
            self.vacunaFrame, width=12, textvariable=self.CodVac)
        self.textoCodVac.place(x=480, y=445)

        barra = ttk.Separator(self.vacunaFrame, orient=tk.VERTICAL)
        barra.place(x=665, y=0, height=590, width=2)

        ttk.Label(self.vacunaFrame, text='Fecha de hoy').place(x=775, y=30)
        self.vac = tk.StringVar()
        self.FechaHoy = ttk.Entry(
            self.vacunaFrame, width=11, textvariable=self.fecha)
        self.FechaHoy.place(x=775, y=65)

        self.vacDisponibles = {
            'Felino': ['Antirrabica', 'Triple Felina', 'Hepatitis'],
            'Canino': ['Antirrabica', 'Parvovirus']
        }

        self.vacunaElegida = tk.StringVar()
        ttk.Label(self.vacunaFrame, text='Vacuna').place(x=700, y=180)
        self.vacunaCBox = ttk.Combobox(
            self.vacunaFrame, state='disabled', textvariable=self.vacunaElegida)
        self.vacunaCBox.place(x=700, y=210)

        self.proveedorElegido = tk.StringVar()
        ttk.Label(self.vacunaFrame, text='Proveedor').place(x=700, y=270)
        self.proveedorCBox = ttk.Combobox(self.vacunaFrame, state='disabled', values=[
                                          'Tecnofarma', 'Biogenetics'], textvariable=self.proveedorElegido)
        self.proveedorCBox.place(x=700, y=300)

        self.botonRegVac = ttk.Button(
            self.vacunaFrame, width=12, text='Registrar', command=self.RegistrarVacunacion)
        self.botonRegVac.place(x=760, y=360)

        self.historialVacBoton = ttk.Button(
            self.vacunaFrame, text='Obtener historial de vacunas', command=self.ObtenerHistorialVac)
        self.historialVacBoton.place(x=710, y=490)
        self.popupVac = None

    def RegistrarPeso(self):
        codigo = self.textoCod.get()
        peso = self.espacioPeso.get()
        if ',' in peso:
            peso = peso.replace(',', '.')
        if codigo == '':
            showerror('Error de campo', 'No ha indicado la mascota')
        elif not self.es_decimal(peso):
            showerror('Error de campo', 'El peso debe ser un dato numérico')
        else:
            with pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                cursor = conexion.cursor()
                cursor.execute('RegistrarPeso ?,?,?,?',
                               (date.today(), codigo, peso, 0))
                bit = cursor.fetchone()
                bit = bit[0]
                if bit:
                    cursor.execute('commit')
                    showinfo('Éxito', 'Registro de peso realizado')
                    self.espacioPeso.delete(0, 30)
                    self.textoCod.delete(0, 30)
                else:
                    cursor.execute('rollback')
                    showwarning('Error', 'Ya ha registrado el peso hoy')
                conexion.commit()
                cursor.close()

        self.Cod.set('')

    def RegistrarVacunacion(self):
        codigo = self.textoCodVac.get()
        vacuna = self.vacunaCBox.get()
        proveedor = self.proveedorCBox.get()
        if codigo == '':
            showerror('Error de campo', 'No ha indicado la mascota')
        else:
            with pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                cursor = conexion.cursor()
                cursor.execute('RegistrarVacunacion ?,?,?,?,?',
                               (date.today(), codigo, vacuna, proveedor, 0))
                bit = cursor.fetchone()
                bit = bit[0]
                if bit:
                    cursor.execute('commit')
                    showinfo('Éxito', 'Vacunación registrada')
                    self.espacioBuscarVac.delete(0, 30)
                    self.textoCodVac.delete(0, 30)
                else:
                    cursor.execute('rollback')
                    showwarning('Error', 'Ya ha registrado esa vacuna')
                conexion.commit()
                cursor.close()

        self.CodVac.set('')

    def es_decimal(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def ObtenerHistorialPesos(self):
        if self.popupPesos:
            self.popupPesos.destroy()
        codigo = self.textoCod.get()
        if codigo == '':
            showerror('Error de campo', 'No ha indicado la mascota')
        else:

            self.popupPesos = tk.Toplevel(
                self.pesoFrame, width=500, height=500)
            self.popupPesos.title('Pesos históricos')

            self.historialFrame = ttk.Frame(
                self.popupPesos, width=500, height=500)

            with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                cursor = conexion.cursor()
                cursor.execute('exec HistorialPeso ?', (codigo))
                titulos = []
                for titulo in cursor.description:
                    titulos.append(titulo[0])

                datos = cursor.fetchall()
                cursor.close()

                self.tablaPesos = ttk.Treeview(self.historialFrame,
                                               height=20, columns=titulos[1:])
                self.tablaPesos.bind('<Double-1>', self.seleccion)

                for i, titulo in enumerate(titulos):
                    if i == 0:
                        self.tablaPesos.column(
                            '#0', width=150, anchor=tk.CENTER)
                        self.tablaPesos.heading(
                            '#0', text=titulo, anchor=tk.CENTER)
                    else:
                        self.tablaPesos.column(
                            titulo, width=150, anchor=tk.CENTER)
                        self.tablaPesos.heading(
                            titulo, text=titulo, anchor=tk.CENTER)

                for cliente in datos:
                    atributos = []
                    for atributo in cliente:
                        atributos.append(atributo)

                    self.tablaPesos.insert(
                        '', tk.END, text=atributos[0], values=atributos[1:])

                self.tablaPesos.pack()
                self.historialFrame.pack()

    def ObtenerHistorialVac(self):
        if self.popupVac:
            self.popupVac.destroy()
        codigo = self.textoCodVac.get()
        if codigo == '':
            showerror('Error de campo', 'No ha indicado la mascota')
        else:

            self.popupVac = tk.Toplevel(
                self.vacunaFrame, width=500, height=500)
            self.popupVac.title('Historia Vacunas')

            self.historialVacFrame = ttk.Frame(
                self.popupVac, width=500, height=500)

            with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                cursor = conexion.cursor()
                cursor.execute('exec HistorialVacunas ?', (codigo))
                titulos = []
                for titulo in cursor.description:
                    titulos.append(titulo[0])

                datos = cursor.fetchall()
                cursor.close()

                self.tablaVacunas = ttk.Treeview(self.vacunaFrame,
                                                 height=20, columns=titulos[1:])
                self.tablaVacunas.bind('<Double-1>', self.seleccion)

                for i, titulo in enumerate(titulos):
                    if i == 0:
                        self.tablaVacunas.column(
                            '#0', width=150, anchor=tk.CENTER)
                        self.tablaVacunas.heading(
                            '#0', text=titulo, anchor=tk.CENTER)
                    else:
                        self.tablaVacunas.column(
                            titulo, width=150, anchor=tk.CENTER)
                        self.tablaVacunas.heading(
                            titulo, text=titulo, anchor=tk.CENTER)

                for cliente in datos:
                    atributos = []
                    for atributo in cliente:
                        atributos.append(atributo)

                    self.tablaVacunas.insert(
                        '', tk.END, text=atributos[0], values=atributos[1:])

                self.tablaVacunas.pack()
                self.historialVacFrame.pack()

    # def CambiandoSize(self, event):
    #     eleccionTab = event.widget.index("current")
    #     nombreTab = event.widget.tab(eleccionTab, option="text")
    #     if nombreTab == 'Pesos':
    #         self.master.geometry('1200x600')
    #     else:
    #         self.master.geometry("1000x600")

    def EleccionCampo(self):
        self.campoElegido = str(self.eleccionCampo.get())
        self.campoElegidoVac = str(self.eleccionCampoVac.get())

        if self.campoElegido == 'Especie':
            self.espacioBuscarPeso.delete(0, 30)
            self.espacioBuscarPeso.configure(state='disabled')
            self.CBoxEspecie.configure(state='readonly')
        else:
            self.CBoxEspecie.set('')
            self.espacioBuscarPeso.configure(state='normal')
            self.CBoxEspecie.configure(state='disabled')

        if self.campoElegidoVac == 'Especie':
            self.espacioBuscarVac.delete(0, 30)
            self.espacioBuscarVac.configure(state='disabled')
            self.CBoxEspecieVac.configure(state='readonly')
        else:
            self.CBoxEspecieVac.set('')
            self.espacioBuscarVac.configure(state='normal')
            self.CBoxEspecieVac.configure(state='disabled')

    def Buscar(self):

        if self.tablaMascotasPesos:
            self.tablaMascotasPesos.destroy()

        if self.espacioBuscarPeso.get() == '':
            if self.campoElegido == 'Especie':
                self.textoBuscarPeso = self.CBoxEspecie.get()
            else:
                print('es numero')
                showwarning(title='Error de campo',
                            message='Campo de búsqueda vacío')
                return

        else:
            self.textoBuscarPeso = self.espacioBuscarPeso.get()

        self.tablaMascotasPesos = ttk.Frame(
            self.pesoFrame, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec BuscarMascota ?,? ',
                           (self.campoElegido, self.textoBuscarPeso))
            resultados = cursor.fetchall()

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()
            self.tablaEncontrados = ttk.Treeview(
                self.tablaMascotasPesos, height=6, columns=titulos[1:])
            self.tablaEncontrados.bind('<Double-1>', self.seleccion)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontrados.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontrados.pack()
            self.tablaMascotasPesos.place(x=60, y=180)

    def BuscarVac(self):
        if self.tablaMascotasVacunas:
            self.tablaMascotasVacunas.destroy()

        self.textoBuscarVac = self.espacioBuscarVac.get()

        if self.espacioBuscarVac.get() == '':
            if self.campoElegidoVac == 'Especie':
                self.textoBuscarVac = self.CBoxEspecieVac.get()
            else:
                if self.textoBuscarVac == '':
                    print('es numero')
                    showwarning(title='Error de campo',
                                message='Campo de búsqueda vacío')
                    return
        self.tablaMascotasVacunas = ttk.Frame(
            self.vacunaFrame, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec BuscarMascota ?,? ',
                           (self.campoElegidoVac, self.textoBuscarVac))
            resultados = cursor.fetchall()

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()
            self.tablaEncontradosVac = ttk.Treeview(
                self.tablaMascotasVacunas, height=6, columns=titulos[1:])
            self.tablaEncontradosVac.bind('<Double-1>', self.seleccionVac)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontradosVac.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontradosVac.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontradosVac.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontradosVac.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontradosVac.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontradosVac.pack()
            self.tablaMascotasVacunas.place(x=60, y=180)

    def seleccion(self, event=None):
        familia = self.tablaEncontrados.focus()
        codigo = self.tablaEncontrados.item(familia)['text']

        self.textoCod.config(state='normal')
        self.textoCod.delete(0, tk.END)
        self.textoCod.insert(0, codigo)
        self.textoCod.config(state='readonly')

    def seleccionVac(self, event=None):
        familiaVac = self.tablaEncontradosVac.focus()
        codigoVac = self.tablaEncontradosVac.item(familiaVac)['text']
        especie = self.tablaEncontradosVac.item(familiaVac)['values'][2]

        self.textoCodVac.config(state='normal')
        self.textoCodVac.delete(0, tk.END)
        self.textoCodVac.insert(0, codigoVac)
        self.textoCodVac.config(state='readonly')

        self.proveedorCBox.set('')
        self.vacunaCBox.set('')
        self.vacunaCBox.configure(
            values=self.vacDisponibles[especie], state='readonly')
        self.proveedorCBox.configure(state='readonly')

    def aModificarC(self):
        self.eleccionCliente = EleccionClienteModificar(self)
        self.padre.cambioVentana(self, self.eleccionCliente, [
                                 700, 500], 'Eleccion de Cliente')

    def nuevaPersonaFamilia(self):
        self.personaAFamilia = EleccionPersona(self)
        self.padre.cambioVentana(self, self.personaAFamilia, [
                                 400, 200], 'Eleccion de Persona')

    def inicializarTablaM(self):
        self.tablaFrameM = ttk.Frame(
            self.mascotaFrame, style='Card.TFrame', width=615, height=530)

        # Tabla con SQL
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select CodMascota, Alias, Raza, Color_pelo, Especie from Mascotas order by CodMascota')

            titulos = []

            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        self.tablaM = ttk.Treeview(self.tablaFrameM, height=18,
                                   padding=5, columns=titulos[1:], selectmode='none', show='tree headings')

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tablaM.column('#0', width=100, anchor='w')
                self.tablaM.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                if titulo == 'Apellido':
                    self.tablaM.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'NroCuenta':
                    self.tablaM.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'Direccion':
                    self.tablaM.column(titulo, width=150, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaM.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tablaM.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tablaM.place(x=10, y=10)

        separador = ttk.Separator(self.tablaFrameM, orient='horizontal')
        separador.place(x=10, y=470, width=600)

        # Botones
        ttk.Button(self.tablaFrameM, text='Mascotas', command=self.mostrarMascotas,
                   width=30).place(x=10, y=480)
        ttk.Button(self.tablaFrameM, text='Mascotas y Dueños', width=30, command=self.mascotasDueños).place(
            x=310, y=480)

        self.tablaFrameM.place(x=360, y=10)

    def mascotasDueños(self):
        self.tablaM.destroy()

        # Tabla con SQL
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select M.Alias, C.Apellido from Mascotas M inner join Clientes C on C.IdCliente = M.IdCliente')

            titulos = []

            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        self.tablaM = ttk.Treeview(self.tablaFrameM, height=18,
                                   padding=5, columns=titulos[1:], selectmode='none', show='tree headings')

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tablaM.column('#0', width=100, anchor='w')
                self.tablaM.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                self.tablaM.column(titulo, width=100, anchor=tk.CENTER)
                self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tablaM.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tablaM.place(x=130, y=10)

    def mostrarMascotas(self):
        self.tablaM.destroy()

        # Tabla con SQL
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select CodMascota, Alias, Raza, Color_pelo, Especie from Mascotas order by CodMascota')

            titulos = []

            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        self.tablaM = ttk.Treeview(self.tablaFrameM, height=18,
                                   padding=5, columns=titulos[1:], selectmode='none', show='tree headings')

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tablaM.column('#0', width=100, anchor='w')
                self.tablaM.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                if titulo == 'Apellido':
                    self.tablaM.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'NroCuenta':
                    self.tablaM.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'Direccion':
                    self.tablaM.column(titulo, width=150, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaM.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaM.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tablaM.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tablaM.place(x=10, y=10)

    def inicializarTablaC(self):
        self.tablaFrameC = ttk.Frame(
            self.clienteFrame, style='Card.TFrame', width=615, height=530)

        # Tabla con SQL
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('select * from Clientes order by IdCliente')

            titulos = []

            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        self.tablaC = ttk.Treeview(self.tablaFrameC, height=18,
                                   padding=5, columns=titulos[1:], selectmode='none', show='tree headings')

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tablaC.column('#0', width=100, anchor='w')
                self.tablaC.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                if titulo == 'Apellido':
                    self.tablaC.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'NroCuenta':
                    self.tablaC.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'Direccion':
                    self.tablaC.column(titulo, width=150, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaC.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tablaC.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tablaC.place(x=10, y=10)

        separador = ttk.Separator(self.tablaFrameC, orient='horizontal')
        separador.place(x=10, y=470, width=600)

        # Botones
        ttk.Button(self.tablaFrameC, text='Clientes', command=self.mostrarClientes,
                   width=30).place(x=10, y=480)
        ttk.Button(self.tablaFrameC, text='Mascotas por Cliente', width=30, command=self.mascotasPorCliente).place(
            x=310, y=480)

        self.tablaFrameC.place(x=360, y=10)

    def mascotasPorCliente(self):
        self.tablaC.destroy()

        # Tabla con SQL
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select C.IdCliente, C.Apellido, COUNT(P.Nombre) as Cantidad from Clientes C inner join Encargados E on E.IdCliente = C.IdCliente inner join Personas P on E.CI = P.CI group by C.IdCliente, C.Apellido order by C.IdCliente')

            titulos = []

            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        self.tablaC = ttk.Treeview(self.tablaFrameC, height=18,
                                   padding=5, columns=titulos[1:], selectmode='none', show='tree headings')

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tablaC.column('#0', width=100, anchor='w')
                self.tablaC.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                self.tablaC.column(titulo, width=100, anchor=tk.CENTER)
                self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tablaC.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tablaC.place(x=130, y=10)

    def mostrarClientes(self):
        self.tablaC.destroy()

        # Tabla con SQL
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('select * from Clientes order by IdCliente')

            titulos = []

            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        self.tablaC = ttk.Treeview(self.tablaFrameC, height=18,
                                   padding=5, columns=titulos[1:], selectmode='none', show='tree headings')

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tablaC.column('#0', width=100, anchor='w')
                self.tablaC.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                if titulo == 'Apellido':
                    self.tablaC.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'NroCuenta':
                    self.tablaC.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)
                elif titulo == 'Direccion':
                    self.tablaC.column(titulo, width=150, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaC.column(titulo, width=100, anchor=tk.CENTER)
                    self.tablaC.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tablaC.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tablaC.place(x=10, y=10)

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

    def aInfoM(self):
        self.InfoPage = InfoPage(self)
        self.padre.cambioVentana(self, self.InfoPage, [
                                 1000, 520], 'Información de mascota')


class InfoPage(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=1000, height=520)

        self.padre = master
        ttk.Button(self, text='Volver',
                   command=self.aPrincipal).place(x=10, y=10)
        self.padre = master
        self.ancestro = self.padre.padre
        self.tablaFrame = None

        ttk.Label(self, text='Ingrese su búsqueda').place(x=26, y=60)
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
        ttk.Label(self, text='Código de Mascota').place(x=32, y=410)
        self.textoCod = ttk.Entry(self, width=14, textvariable=self.Cod)
        self.textoCod.place(x=30, y=445)

        self.histPesoBoton = ttk.Button(
            self, width=13, text='Historial pesos', command=self.ObtenerHistorialPesos)
        self.histPesoBoton.place(x=245, y=445)

        self.histMedBoton = ttk.Button(
            self, width=12, text='Vacunaciones', command=self.ObtenerVacunaciones)
        self.histMedBoton.place(x=455, y=445)

        ttk.Separator(self, orient=tk.VERTICAL).place(
            x=685, y=0, height=590, width=2)

        ttk.Label(self, text='Peso más reciente').place(x=740, y=60)
        self.pesoReciente = tk.StringVar()
        self.popupPesos = None
        self.espacioPesoReciente = ttk.Entry(
            self, width=10, textvariable=self.pesoReciente, state='readonly')
        self.espacioPesoReciente.place(x=740, y=95)

        ttk.Label(self, text='Última vacuna recibica').place(x=740, y=205)
        self.vacunaReciente = tk.StringVar()
        self.popupVacunaciones = None
        self.espacioVacReciente = ttk.Entry(
            self, width=12, textvariable=self.vacunaReciente, state='readonly')
        self.espacioVacReciente.place(x=740, y=240)

        ttk.Label(self, text='Última situación médica').place(x=740, y=350)
        self.situacionReciente = tk.StringVar()
        self.espacioSituReciente = ttk.Entry(
            self, width=12, textvariable=self.situacionReciente, state='readonly')
        self.espacioSituReciente.place(x=740, y=385)

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
        self.textoBuscarPeso = self.espacioBuscar.get()

        if self.espacioBuscar.get() == '':
            if self.campoElegido == 'Especie':
                self.textoBuscarPeso = self.CBoxEspecie.get()
            else:
                if self.textoBuscarPeso == '':
                    print('es numero')
                    showwarning(title='Error de campo',
                                message='Formato de búsqueda no válido')
                    return
        self.tablaFrame = ttk.Frame(self, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec BuscarMascota ?,? ',
                           (self.campoElegido, self.textoBuscarPeso))
            resultados = cursor.fetchall()
            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()
            self.tablaEncontrados = ttk.Treeview(
                self.tablaFrame, height=6, columns=titulos[1:])
            self.tablaEncontrados.bind('<Double-1>', self.seleccion)

            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontrados.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontrados.pack()
            self.tablaFrame.place(x=60, y=195)

    def seleccion(self, event=None):

        # aqui hay que actualizar los datos de las entries para peso,vacunacion y consulta

        familia = self.tablaEncontrados.focus()
        codigo = self.tablaEncontrados.item(familia)['text']

        self.textoCod.config(state='normal')
        self.textoCod.delete(0, tk.END)
        self.textoCod.insert(0, codigo)
        self.textoCod.config(state='readonly')
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('exec PesoReciente ?', (codigo))
            datosPeso = cursor.fetchone()
            if datosPeso:
                self.pesoReciente.set(datosPeso[0])
            else:
                self.pesoReciente.set('-Ninguno-')

            cursor.execute('exec VacunaReciente ?', (codigo))
            datosVac = cursor.fetchone()
            if datosVac:
                self.vacunaReciente.set(datosVac[0])
            else:
                self.vacunaReciente.set('-Ninguna-')

            cursor.execute('exec SituacionReciente ?', (codigo))
            datosSitu = cursor.fetchone()
            if datosSitu:
                self.situacionReciente.set(datosSitu[0])
            else:
                self.situacionReciente.set('-Ninguna-')

            cursor.close()

    def aPrincipal(self):
        if self.popupPesos:
            self.popupPesos.destroy()
        if self.popupVacunaciones:
            self.popupVacunaciones.destroy()
        self.ancestro.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')

    def ObtenerHistorialPesos(self):
        if self.popupPesos:
            self.popupPesos.destroy()
        codigo = self.textoCod.get()
        if codigo == '':
            showerror('Error de campo', 'No ha indicado la mascota')
        else:

            self.popupPesos = tk.Toplevel(self, width=500, height=500)
            self.popupPesos.title('Pesos históricos')

            self.historialFrame = ttk.Frame(
                self.popupPesos, width=500, height=500)

            with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                cursor = conexion.cursor()
                cursor.execute('exec HistorialPeso ?', (codigo))
                titulos = []
                for titulo in cursor.description:
                    titulos.append(titulo[0])

                datos = cursor.fetchall()
                cursor.close()

                self.tablaPesos = ttk.Treeview(self.historialFrame,
                                               height=20, columns=titulos[1:])
                self.tablaPesos.bind('<Double-1>', self.seleccion)

                for i, titulo in enumerate(titulos):
                    if i == 0:
                        self.tablaPesos.column(
                            '#0', width=160, anchor=tk.CENTER)
                        self.tablaPesos.heading(
                            '#0', text=titulo, anchor=tk.CENTER)
                    else:
                        self.tablaPesos.column(
                            titulo, width=160, anchor=tk.CENTER)
                        self.tablaPesos.heading(
                            titulo, text=titulo, anchor=tk.CENTER)

                for cliente in datos:
                    atributos = []
                    for atributo in cliente:
                        atributos.append(atributo)

                    self.tablaPesos.insert(
                        '', tk.END, text=atributos[0], values=atributos[1:])

                self.tablaPesos.pack()
                self.historialFrame.pack()

    def ObtenerVacunaciones(self):
        if self.popupVacunaciones:
            self.popupVacunaciones.destroy()
        codigo = self.textoCod.get()
        if codigo == '':
            showerror('Error de campo', 'No ha indicado la mascota')
        else:

            self.popupVacunaciones = tk.Toplevel(self, width=500, height=500)
            self.popupVacunaciones.title('Historia de vacunaciones')

            self.historialFrame = ttk.Frame(
                self.popupVacunaciones, width=500, height=500)

            with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                cursor = conexion.cursor()
                cursor.execute('exec HistorialVacunacion ?', (codigo))
                titulos = []
                for titulo in cursor.description:
                    titulos.append(titulo[0])

                datos = cursor.fetchall()
                if not datos:
                    self.popupVacunaciones.destroy()
                    showwarning(
                        'Aviso', 'No se encuentran vacunaciones registradas')
                    return
                cursor.close()

                self.tablaVacunas = ttk.Treeview(self.historialFrame,
                                                 height=20, columns=titulos[1:])
                self.tablaVacunas.bind('<Double-1>', self.seleccion)

                for i, titulo in enumerate(titulos):
                    if i == 0:
                        self.tablaVacunas.column(
                            '#0', width=160, anchor=tk.CENTER)
                        self.tablaVacunas.heading(
                            '#0', text=titulo, anchor=tk.CENTER)
                    else:
                        self.tablaVacunas.column(
                            titulo, width=160, anchor=tk.CENTER)
                        self.tablaVacunas.heading(
                            titulo, text=titulo, anchor=tk.CENTER)

                for cliente in datos:
                    atributos = []
                    for atributo in cliente:
                        atributos.append(atributo)

                    self.tablaVacunas.insert(
                        '', tk.END, text=atributos[0], values=atributos[1:])

                self.tablaVacunas.pack()
                self.historialFrame.pack()


class EleccionClienteModificar(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master.padre, width=700, height=500)

        self.padre = master
        self.campo = tk.IntVar()

        ttk.Radiobutton(self, text='ID del Cliente',
                        variable=self.campo, value=1, command=self.habilitar).place(x=30, y=30)
        ttk.Radiobutton(self, text='Apellido',
                        variable=self.campo, value=2, command=self.habilitar).place(x=30, y=70)
        ttk.Radiobutton(self, text='Numero de Cuenta',
                        variable=self.campo, value=3, command=self.habilitar).place(x=30, y=110)
        ttk.Radiobutton(self, text='Telefono',
                        variable=self.campo, value=4, command=self.habilitar).place(x=30, y=150)
        ttk.Radiobutton(self, text='Todos los Clientes',
                        variable=self.campo, value=5, command=self.habilitar).place(x=30, y=190)

        self.campoBuscar = ttk.Entry(self, width=20, state='disabled')
        self.campoBuscar.place(x=30, y=270)

        ttk.Label(self, text='Campo').place(x=30, y=240)

        self.botonBuscar = ttk.Button(self, text='Buscar', command=self.buscar)
        self.botonBuscar.place(x=30, y=320)

        ttk.Button(self, text='Volver', command=self.volver).place(x=10, y=450)

        self.tablaFrame = ttk.Frame(
            self, style='Card.TFrame', width=390, height=480)
        self.tablaFrame.place(x=300, y=10)

        self.tabla = None

    def volver(self):
        respuesta = askquestion(title='Confirmacion', message='¿Estas seguro?')

        if respuesta == 'yes':
            self.padre.padre.cambioVentana(
                self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
            self.destroy()

    def habilitar(self):
        self.botonBuscar.config(style='Accent.TButton')

        if self.campo.get() != 5:
            self.campoBuscar.config(state='normal')
            self.campoBuscar.focus()
        else:
            self.campoBuscar.config(state='disabled')

    def seleccion(self, event=None):
        item = self.tabla.focus()

        clienteItem = self.tabla.item(item)
        idCliente = clienteItem['text']

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select * from Clientes where IdCliente = ?', idCliente)

            atributos = cursor.fetchone()

        cliente = Cliente(atributos)

        self.perfil = PerfilClienteModificable(self.padre, cliente)
        self.padre.padre.cambioVentana(
            self, self.perfil, [500, 400], 'Modificar cliente')

    def buscar(self):
        campoBuscar = self.campoBuscar.get()

        campos = {1: 'IdCliente', 2: 'Apellido', 3: 'NroCuenta', 4: 'Telefono'}
        campo = self.campo.get()

        if campoBuscar == '' and campo != 5:
            showwarning(title='Error',
                        message='El campo buscar no puede estar vacio')
            return

        if campo != 5:
            consulta = f'select IdCliente, Apellido, Telefono from Clientes where {campos[campo]} = ?'

        if self.tabla:
            self.tabla.destroy()

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            if campo != 5:
                cursor.execute(consulta, campoBuscar)
            else:
                cursor.execute(
                    'select IdCliente, Apellido, Telefono from Clientes')

            titulos = []

            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            if not clientes:
                showwarning(
                    title='Ups!', message='No se ha encontrado a ningun cliente!')

        self.tabla = ttk.Treeview(
            self.tablaFrame, height=19, columns=titulos[1:])
        self.tabla.bind('<Double-1>', self.seleccion)

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tabla.column('#0', width=100, anchor='w')
                self.tabla.heading('#0', text=titulo, anchor='center')
            else:
                self.tabla.column(titulo, width=100, anchor='center')
                self.tabla.heading(titulo, text=titulo, anchor='center')

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)
            self.tabla.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tabla.place(x=20, y=10)


class PerfilClienteModificable(ttk.Frame):
    def __init__(self, master: VeterinariaPage, cliente: Cliente):
        super().__init__(master.padre, width=500, height=400)
        self.cliente = cliente
        self.padre = master

        ttk.Label(self, text='Perfil del Cliente').place(x=180, y=20)

        ttk.Separator(self).place(x=170, y=50, width=140)

        ttk.Label(self, text='ID').place(x=225, y=55)
        self.idCliente = ttk.Entry(self, width=6, justify='center')
        self.idCliente.place(x=200, y=80)
        self.idCliente.insert(0, self.cliente.idcliente)
        self.idCliente.config(state='readonly')

        ttk.Label(self, text='Apellido').place(x=10, y=130)
        self.apellidoCliente = ttk.Entry(self, width=15)
        self.apellidoCliente.insert(0, self.cliente.apellido)
        self.apellidoCliente.place(x=10, y=160)

        ttk.Label(self, text='Numero de Cuenta').place(x=300, y=130)
        self.nroCuenta = ttk.Entry(self, width=10)
        self.nroCuenta.insert(0, self.cliente.nrocuenta)
        self.nroCuenta.place(x=320, y=160)

        ttk.Label(self, text='Telefono').place(x=10, y=220)
        self.telefono = ttk.Entry(self, width=10)
        self.telefono.insert(0, self.cliente.telefono)
        self.telefono.place(x=10, y=250)

        ttk.Label(self, text='Direccion').place(x=160, y=220)
        self.direccion = ttk.Entry(self, width=35)
        self.direccion.insert(0, self.cliente.direccion)
        self.direccion.place(x=160, y=250)

        ttk.Button(self, text='Guardar cambios',
                   command=self.guardarCambios).place(x=340, y=350)

    def guardarCambios(self):
        apellido = self.apellidoCliente.get()
        telefono = self.telefono.get()
        nrocuenta = self.nroCuenta.get()
        direccion = self.direccion.get()

        respuesta = askquestion(title='Guardar cambios',
                                message='¿Desea guardar los cambios?')

        if respuesta == 'no':
            self.padre.padre.cambioVentana(
                self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
            self.destroy()
            return

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            if apellido != self.cliente.apellido:
                cursor.execute('exec ModificarCliente ?,?,?,?', [
                               self.cliente.idcliente, 'Apellido', apellido, 0])
                cursor.commit()

            if telefono != self.cliente.telefono:
                cursor.execute('exec ModificarCliente ?,?,?,?', [
                               self.cliente.idcliente, 'Telefono', telefono, 0])
                cursor.commit()

            if nrocuenta != self.cliente.nrocuenta:
                cursor.execute('exec ModificarCliente ?,?,?,?', [
                               self.cliente.idcliente, 'NroCuenta', nrocuenta, 0])
                cursor.commit()

            if direccion != self.cliente.direccion:
                cursor.execute('exec ModificarCliente ?,?,?,?', [
                               self.cliente.idcliente, 'Direccion', direccion, 0])
                cursor.commit()

            conexion.commit()
            showinfo(title='Exito', message='Se han guardado los cambios')

        self.padre.padre.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
        self.destroy()


class EleccionPersona(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=400, height=200)

        self.padre = master

        ttk.Label(self, text='¿A que persona quieres enlazar?').place(
            x=90, y=50)

        ttk.Button(self, text='Existente', width=15,
                   command=self.existente, style='Accent.TButton').place(x=20, y=140)

        ttk.Button(self, text='Nueva Persona', width=15,
                   style='Accent.TButton', command=self.nuevo).place(x=225, y=140)

    def existente(self):
        self.personaExistentePage = PersonaExistentePage(
            self.padre)
        self.padre.padre.cambioVentana(
            self, self.personaExistentePage, [300, 300], 'Persona Existente')
        self.destroy()

    def nuevo(self):
        self.personaNuevaPage = NuevaPersonaPage(self.padre)
        self.padre.padre.cambioVentana(
            self, self.personaNuevaPage, [400, 300], 'Nueva Persona')
        self.destroy()


class PersonaExistentePage(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=300, height=300)

        self.padre = master

        ttk.Button(self, width=10, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)

        ttk.Label(self, text='CI de la Persona').place(x=20, y=70)

        self.label = ttk.Label(self, text='').place(x=80, y=120)

        self.familia = ttk.Entry(self, width=25, state='readonly')
        self.familia.place(x=20, y=100)

        ttk.Button(self, text='Ver Personas', width=10,
                   command=self.verPersonas).place(x=20, y=145)

        self.aceptarBoton = ttk.Button(
            self, text='Aceptar', state='disabled', command=self.aceptar)
        self.aceptarBoton.place(x=175, y=250)

    def cancelar(self):
        self.padre.padre.cambioVentana(
            self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
        self.destroy()

    def verPersonas(self):

        self.popup = tk.Toplevel(self)
        self.popup.title('Personas')
        self.popup.geometry(
            f'+{self.winfo_screenwidth()//2}+{self.winfo_screenmmheight()//2}')

        self.personasFrame = ttk.Frame(self.popup, width=500, height=500)

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('select * from Personas')

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            personas = cursor.fetchall()

            cursor.close()

        scroll = ttk.Scrollbar(self.popup, orient='vertical')

        self.tabla = ttk.Treeview(self.personasFrame, height=20,
                                  columns=titulos[1:], yscrollcommand=scroll.set)
        self.tabla.bind('<Double-1>', self.seleccion)

        scroll.config(command=self.tabla.yview)

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tabla.column('#0', width=100, anchor=tk.CENTER)
                self.tabla.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                self.tabla.column(titulo, width=200, anchor=tk.CENTER)
                self.tabla.heading(titulo, text=titulo, anchor=tk.CENTER)

        for persona in personas:
            atributos = []
            for atributo in persona:
                atributos.append(atributo)

            self.tabla.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tabla.pack()
        scroll.pack(side='right', fill='y')

        self.personasFrame.pack()

    def seleccion(self, event=None):
        persona = self.tabla.focus()
        # print(self.tabla.item(persona)['text'])
        ci = self.tabla.item(persona)['text']

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select * from Personas where CI = ?', ci)

            atributos = cursor.fetchone()

            self.persona = Persona(atributos)

        self.familia.config(state='normal')
        self.familia.delete(0, tk.END)
        self.familia.insert(0, ci)
        self.familia.config(state='readonly')

        self.aceptarBoton.config(state='normal', style='Accent.TButton')

        self.popup.destroy()

    def aceptar(self):
        self.eleccionCliente = EleccionClientePersona(self.padre, self.persona)
        self.padre.padre.cambioVentana(self, self.eleccionCliente, [
                                       400, 200], 'Eleccion de Cliente')


class NuevaPersonaPage(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=400, height=300)

        self.padre = master

        ttk.Label(self, text='Nueva Persona').place(x=140, y=10)

        ttk.Separator(self).place(x=10, y=40, width=380)

        ttk.Label(self, text='Carnet de Identidad').place(x=120, y=60)
        self.ci = ttk.Entry(self, justify='center')
        self.ci.place(x=100, y=90)

        ttk.Label(self, text='Nombre').place(x=10, y=150)
        self.nombre = ttk.Entry(self, width=40)
        self.nombre.place(x=10, y=180)

        ttk.Button(self, text='Registrar', width=30,
                   command=self.registrar).place(x=60, y=250)

    def registrar(self):
        ci = self.ci.get()
        nombre = self.nombre.get()

        if any(elemento == '' for elemento in [ci, nombre]):
            showwarning(title='Error',
                        message='Todos los campos deben de estar llenos')
            return

        try:
            ci = int(ci)
        except Exception:
            showerror(title='Error',
                      message='El carnet de identidad debe de ser numerico')
            return

        persona = Persona([ci, nombre])

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select * from Personas where CI = ?', persona.getCI())

            if cursor.fetchone():
                showerror(
                    'Error', 'Ya se encuentra una persona con ese mismo carnet de identidad, ingrese otro')
                return

        self.eleccionCliente = EleccionClientePersona(self.padre, persona)
        self.padre.padre.cambioVentana(self, self.eleccionCliente, [
                                       400, 200], 'Eleccion de Cliente')
        self.destroy()


class EleccionClientePersona(ttk.Frame):
    def __init__(self, master: VeterinariaPage, persona: Persona):
        super().__init__(master=master.padre, width=400, height=200)

        self.padre = master
        self.persona = persona

        ttk.Label(self, text='¿A que cliente quieres enlazar?').place(
            x=90, y=50)

        ttk.Button(self, text='Existente', width=15,
                   command=self.existente, style='Accent.TButton').place(x=20, y=140)

        ttk.Button(self, text='Nuevo Cliente', width=15,
                   style='Accent.TButton', command=self.nuevo).place(x=225, y=140)

    def existente(self):
        self.clienteExistentePage = ClienteExistentePersonaPage(
            self.padre, self.persona)
        self.padre.padre.cambioVentana(
            self, self.clienteExistentePage, [300, 300], 'Cliente Existente')
        self.destroy()

    def nuevo(self):
        self.clienteNuevoPage = NuevoClientePersonaPage(
            self.padre, self.persona)
        self.padre.padre.cambioVentana(
            self, self.clienteNuevoPage, [400, 450], 'Nuevo Cliente')
        self.destroy()


class NuevoClientePersonaPage(ttk.Frame):
    def __init__(self, master: VeterinariaPage = None, persona: Persona = None):
        super().__init__(master.padre, height=450, width=400)

        self.padre = master
        self.persona = persona

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

            cursor.close()
            conexion.commit()

        if bit:
            atributos.insert(0, idcliente)

            lista = self.persona.getAtributos() + [idcliente, 0]

            with pyodbc.connect(
                    f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
                cursor = conexion.cursor()

                cursor.execute('exec RegistrarPersona ?,?,?,?', lista)

                bit2 = cursor.fetchone()[0]

            if bit2:
                showinfo(title='Exito',
                         message='El cliente se ha creado con exito y se ha enlazado con la persona!')
                self.padre.padre.cambioVentana(
                    self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
            else:
                showerror(
                    title='Error', message='Ha ocurrido un error al enlazar a la persona')
        else:
            showerror(
                title='Error', message='Ha ocurrido un error al crear el cliente')


class ClienteExistentePersonaPage(ttk.Frame):
    def __init__(self, master: VeterinariaPage, persona: Persona):
        super().__init__(master=master.padre, width=300, height=300)

        self.padre = master
        self.persona = persona

        ttk.Button(self, width=10, text='Cancelar',
                   command=self.cancelar).place(x=10, y=10)

        ttk.Label(self, text='Familia a buscar').place(x=20, y=70)

        self.label = ttk.Label(self, text='').place(x=80, y=120)

        self.familia = ttk.Entry(self, width=25, state='readonly')
        self.familia.place(x=20, y=100)

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

        self.popup = tk.Toplevel(self)
        self.popup.title('Familias')
        self.popup.geometry(
            f'+{self.winfo_screenwidth()//2}+{self.winfo_screenmmheight()//2}')

        self.familiasFrame = ttk.Frame(self.popup, width=500, height=500)

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('select Apellido, IdCliente from Clientes')

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        scroll = ttk.Scrollbar(self.popup, orient='vertical')

        self.tabla = ttk.Treeview(self.familiasFrame, height=20,
                                  columns=titulos[1:], yscrollcommand=scroll.set)
        self.tabla.bind('<Double-1>', self.seleccion)

        scroll.config(command=self.tabla.yview)

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tabla.column('#0', width=100, anchor=tk.CENTER)
                self.tabla.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                self.tabla.column(titulo, width=100, anchor=tk.CENTER)
                self.tabla.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tabla.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tabla.pack()
        scroll.pack(side='right', fill='y')

        self.familiasFrame.pack()

    def seleccion(self, event=None):
        familia = self.tabla.focus()
        # print(self.tabla.item(familia)['text'])
        codigo = self.tabla.item(familia)['values'][0]

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select * from Clientes where IdCliente = ?', [codigo])

            atributos = cursor.fetchone()

            self.cliente = Cliente(atributos)

        self.familia.config(state='normal')
        self.familia.delete(0, tk.END)
        self.familia.insert(0, codigo)
        self.familia.config(state='readonly')

        self.aceptarBoton.config(state='normal', style='Accent.TButton')

        self.popup.destroy()

    def aceptar(self):
        cliente = self.cliente
        persona = self.persona

        idcliente = cliente.getId()

        lista = persona.getAtributos() + [idcliente] + [0]

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select * from Personas where CI = ?', persona.getCI())

            if cursor.fetchone():
                cursor.execute('insert into Encargados values (?,?)', [
                               cliente.getId(), persona.getCI()])
                cursor.commit()

                showinfo(
                    title='Exito', message='La persona fue agregada correctamente y ha sido enlazada a este cliente')
                self.padre.padre.cambioVentana(
                    self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
                self.destroy()
            else:
                cursor.execute('exec RegistrarPersona ?,?,?,?', lista)

                bit = cursor.fetchone()[0]

                if bit:
                    cursor.commit()
                    showinfo(
                        title='Exito', message='La persona fue agregada correctamente y ha sido enlazada a este cliente')
                    self.padre.padre.cambioVentana(
                        self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
                    self.destroy()

                else:
                    showerror(
                        'Error', 'El numero de carnet ya se encuentra usado, ingrese otro')
                    cursor.rollback()

            conexion.commit()


class ModificarPageV(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=700, height=520)

        self.padre = master
        ttk.Button(self, text='Volver',
                   command=self.aPrincipal).place(x=10, y=10)

        self.tablaFrame = None

        ttk.Label(self, text='Ingrese su búsqueda').place(x=26, y=60)
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
        self.textoBuscarPeso = self.espacioBuscar.get()

        if self.espacioBuscar.get() == '':
            if self.campoElegido == 'Especie':
                self.textoBuscar = self.CBoxEspecie.get()
            else:
                if self.textoBuscar == '':
                    print('es numero')
                    showwarning(title='Error de campo',
                                message='Formato de búsqueda no válido')
                    return
        self.tablaFrame = ttk.Frame(self, width=200, height=100)
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec BuscarMascota ?,? ',
                           (self.campoElegido, self.textoBuscar))
            resultados = cursor.fetchall()

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            cursor.close()
            self.tablaEncontrados = ttk.Treeview(
                self.tablaFrame, height=6, columns=titulos[1:])
            self.tablaEncontrados.bind('<Double-1>', self.seleccion)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaEncontrados.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaEncontrados.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaEncontrados.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for dato in resultados:
                atributos = []
                for atributo in dato:
                    atributos.append(atributo)

                self.tablaEncontrados.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaEncontrados.pack()
            self.tablaFrame.place(x=60, y=195)

    def seleccion(self, event=None):
        familia = self.tablaEncontrados.focus()
        codigo = self.tablaEncontrados.item(familia)['text']

        self.textoCod.config(state='normal')
        self.textoCod.delete(0, tk.END)
        self.textoCod.insert(0, codigo)
        self.textoCod.config(state='readonly')

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
        if self.padre.tablaFrame:
            self.padre.tablaFrame.pack_forget()
            self.padre.tablaFrame.destroy()
        self.ancestro.cambioVentana(
            self, self.padre, [700, 520], 'Modificar Mascota')
        self.destroy()

    def ModificarMascota(self):
        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            respuesta = askquestion(
                'Confirmación', '¿Desea guardar los cambios?')
            if respuesta == 'yes':
                showinfo('Exito', 'Cambios guardados')

                if self.aliasNuevo.get() != self.atributos[0]:
                    if self.aliasNuevo.get().isnumeric():
                        print('alias es numerico')
                        showerror('Error de campo',
                                  'El Alias no puede ser numérico')
                        return
                    else:
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
            cursor.execute('commit')
            if self.padre.tablaFrame:
                self.padre.tablaFrame.pack_forget()
                self.padre.tablaFrame.destroy()
            self.ancestro.cambioVentana(
                self, self.padre, [700, 520], 'Modificar Mascota')

    def buscarFamilia(self):
        self.eleccionFamilia = EleccionFamilia(self)
        self.ancestro.cambioVentana(self, self.eleccionFamilia, [
                                    400, 200], 'Elección de Familia')


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
                                    380, 340], 'Familia Existente')

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
                   command=self.buscarFamilia).place(x=275, y=100)

        self.IdCli = tk.StringVar()
        ttk.Label(self, text='Código Cliente').place(x=20, y=255)
        self.campoId = ttk.Entry(self, width=12, textvariable=self.IdCli)
        self.campoId.place(x=20, y=280)
        self.aceptarBoton = ttk.Button(
            self, text='Aceptar', state='disabled', command=self.aceptar)
        self.aceptarBoton.place(x=250, y=280)

        self.popupFam = None
        self.popupBuscFam = None

    def cancelar(self):
        self.ancestro.cambioVentana(
            self, self.padre, [400, 200], 'Elección de familia')
        self.destroy()

    def verFamilias(self):

        if self.popupFam:
            self.popupFam.destroy()
        if self.popupBuscFam:
            self.popupBuscFam.destroy()

        self.popupFam = tk.Toplevel(self, width=500, height=500)
        self.popupFam.title('Familias')

        self.familiasFrame = ttk.Frame(self.popupFam, width=500, height=500)

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'select Apellido,NroCuenta,Telefono,IdCliente from Clientes')
            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()
            cursor.close()

            self.tablaFamilias = ttk.Treeview(self.familiasFrame,
                                              height=20, columns=titulos[1:])
            self.tablaFamilias.bind('<Double-1>', self.seleccion)

            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaFamilias.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaFamilias.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaFamilias.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaFamilias.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for cliente in clientes:
                atributos = []
                for atributo in cliente:
                    atributos.append(atributo)

                self.tablaFamilias.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaFamilias.pack()
            self.familiasFrame.pack()

    def seleccion(self, event=None):
        familia = self.tablaFamilias.focus()
        codigo = self.tablaFamilias.item(familia)['values'][2]

        self.campoId.config(state='normal')
        self.campoId.delete(0, tk.END)
        self.campoId.insert(0, codigo)
        self.campoId.config(state='readonly')
        self.aceptarBoton.config(state='normal', style='Accent.TButton')

    def buscarFamilia(self):
        if self.popupFam:
            self.popupFam.destroy()
        if self.popupBuscFam:
            self.popupBuscFam.destroy()

        familia = self.familia.get()
        if familia == '':
            showwarning(title='Error', message='El campo debe de estar lleno')
            return

        self.popupBuscFam = tk.Toplevel(self, width=500, height=500)
        self.popupBuscFam.title('Familias')
        self.familiasBuscFrame = ttk.Frame(
            self.popupBuscFam, width=500, height=500)

        with pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:

            cursor = conexion.cursor()
            cursor.execute(
                'select Apellido,NroCuenta,Telefono,IdCliente from Clientes where Apellido = ?', familia)

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

            self.tablaBuscarFam = ttk.Treeview(self.familiasBuscFrame,
                                               height=20, columns=titulos[1:])

            self.tablaBuscarFam.bind('<Double-1>', self.seleccionBusc)
            for i, titulo in enumerate(titulos):
                if i == 0:
                    self.tablaBuscarFam.column(
                        '#0', width=100, anchor=tk.CENTER)
                    self.tablaBuscarFam.heading(
                        '#0', text=titulo, anchor=tk.CENTER)
                else:
                    self.tablaBuscarFam.column(
                        titulo, width=100, anchor=tk.CENTER)
                    self.tablaBuscarFam.heading(
                        titulo, text=titulo, anchor=tk.CENTER)

            for cliente in resultados:
                atributos = []
                for atributo in cliente:
                    atributos.append(atributo)
                print(atributos)
                self.tablaBuscarFam.insert(
                    '', tk.END, text=atributos[0], values=atributos[1:])

            self.tablaBuscarFam.pack()
            self.familiasBuscFrame.pack()

    def seleccionBusc(self, event=None):
        familia = self.tablaBuscarFam.focus()
        codigo = self.tablaBuscarFam.item(familia)['values'][2]
        print(codigo)
        self.campoId.config(state='normal')
        self.campoId.delete(0, tk.END)
        self.campoId.insert(0, codigo)
        self.campoId.config(state='readonly')
        self.aceptarBoton.config(state='normal', style='Accent.TButton')

    def aceptar(self):
        if self.popupFam:
            self.popupFam.destroy()
        if self.popupBuscFam:
            self.popupBuscFam.destroy()
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
        super().__init__(master.padre.padre.padre.padre, height=450, width=400)

        self.padre = master
        self.ancestro = self.padre.padre.padre.padre.padre

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
        self.ancestro.cambioVentana(
            self, self.padre, [400, 200], 'Elección de Familia')
        self.destroy()

    def aceptar(self):
        apellido = self.apellido.get()
        nrocuenta = self.nrocuenta.get()
        telefono = self.telefono.get()
        direccion = self.direccion.get()

        if apellido.isnumeric() or not apellido.isalpha():
            showwarning('Error de campo', 'Formato de apellido no válido')
            return
        if len(str(nrocuenta)) != 10 or not str(nrocuenta).isnumeric():
            showwarning('Error de campo',
                        'Formato de Número de cuenta no válido')
            return
        if len(str(telefono)) < 8 or not str(telefono).isnumeric():
            showwarning('Error de campo', 'Formato de teléfono no válido')
            return
        if direccion.isnumeric():
            showwarning('Error de campo', 'Formato de dirección no válida')
            return

        atributos = [apellido, nrocuenta, direccion, telefono, 0]

        if any(elemento == '' for elemento in atributos):
            showwarning(title='Error',
                        message='Todos los campos deben estar llenos')
            return

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            print('hola1')
            cursor.execute('exec RegistrarCliente ?,?,?,?,?', atributos)
            print('hola')
            resultados = cursor.fetchall()
            verificacion = resultados[0][0]
            IdParaPerfil = resultados[0][1]
            if verificacion:
                cursor.execute('commit')
                showinfo(
                    'Exito', 'Cliente registrado exitosamente \nDatos enviados a al perfil')
                self.padre.padre.aux.set(apellido)
                self.padre.padre.IdCliente.delete(0, 30)
                self.padre.padre.IdCliente.insert(0, IdParaPerfil)
                self.ancestro.cambioVentana(
                    self, self.padre.padre, [410, 600], "Perfil")
            else:
                cursor.execute('rollback')
                showwarning(
                    'Error en la inserción. Posible cliente duplicado o datos erroneos')


class InsertarMascotaV(ttk.Frame):
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

                        resultado = cursor.fetchone()
                        bit = resultado[0]

                        if bit:
                            codMascota = resultado[1]
                            lista.insert(0, codMascota)

                            mascota = Mascota(lista[:-1])

                            cursor.commit()
                            respuesta = showinfo(title='Exito',
                                                 message='Se ha agregado a la mascota correctamente!')

                            if respuesta:
                                self.registrarPesoPage = RegistrarPrimerPeso(
                                    self.padre, mascota)
                                self.padre.padre.cambioVentana(
                                    self, self.registrarPesoPage, [300, 200], 'Registrar Peso')
                                self.destroy()

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
                    date(año, mes, dia)
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

        fechaTemp = date(año, mes, dia)
        fechaEscrita = f'{fechaTemp}'

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


class RegistrarPrimerPeso(ttk.Frame):
    def __init__(self, master: VeterinariaPage = None, mascota: Mascota = None):
        super().__init__(master=master.padre, width=300, height=200)

        self.mascota = mascota
        self.padre = master

        ttk.Label(self, text='Introduce el peso de la mascota').place(
            x=25, y=10)

        ttk.Separator(self).place(x=5, y=40, width=290)

        self.peso = ttk.Entry(self, width=10)
        self.peso.place(x=100, y=50)

        ttk.Label(self, text='Kg').place(x=220, y=55)

        ttk.Button(self, text='Registrar', width=20,
                   style='Accent.TButton', command=self.registrar).place(x=50, y=150)

    def registrar(self):
        peso = self.peso.get()
        codmascota = self.mascota.getCod()
        fechaHoy = date.now()
        fechaPeso = f'{fechaHoy.year}-{fechaHoy.month}-{fechaHoy.day}'

        if peso == '':
            showerror(title='Error',
                      message='El campo debe de estar lleno')
            return

        if ',' in peso:
            peso.replace(',', '.')

        try:
            peso = float(peso)
        except Exception:
            showerror(title='Error', message='Error en el formato del peso')
            return

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()
            cursor.execute('exec RegistrarPeso ?,?,?,?', [
                           fechaPeso, codmascota, peso, 0])

            resultado = cursor.fetchone()

            bit = resultado[0]

            if bit:
                respuesta = showinfo(
                    title='Exito', message='Se ha registrado el peso correctamente')
                cursor.commit()
                self.padre.padre.cambioVentana(
                    self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')
                self.destroy()
            else:
                cursor.rollback()

            conexion.commit()


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

        self.familia = ttk.Entry(self, width=25, state='readonly')
        self.familia.place(x=20, y=100)

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

        self.popup = tk.Toplevel(self)
        self.popup.title('Familias')
        self.popup.geometry(
            f'+{self.winfo_screenwidth()//2}+{self.winfo_screenmmheight()//2}')

        self.familiasFrame = ttk.Frame(self.popup, width=500, height=500)

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute('select Apellido, IdCliente from Clientes')

            titulos = []
            for titulo in cursor.description:
                titulos.append(titulo[0])

            clientes = cursor.fetchall()

            cursor.close()

        scroll = ttk.Scrollbar(self.popup, orient='vertical')

        self.tabla = ttk.Treeview(self.familiasFrame, height=20,
                                  columns=titulos[1:], yscrollcommand=scroll.set)
        self.tabla.bind('<Double-1>', self.seleccion)

        scroll.config(command=self.tabla.yview)

        for i, titulo in enumerate(titulos):
            if i == 0:
                self.tabla.column('#0', width=100, anchor=tk.CENTER)
                self.tabla.heading('#0', text=titulo, anchor=tk.CENTER)
            else:
                self.tabla.column(titulo, width=100, anchor=tk.CENTER)
                self.tabla.heading(titulo, text=titulo, anchor=tk.CENTER)

        for cliente in clientes:
            atributos = []
            for atributo in cliente:
                atributos.append(atributo)

            self.tabla.insert(
                '', tk.END, text=atributos[0], values=atributos[1:])

        self.tabla.pack()
        scroll.pack(side='right', fill='y')

        self.familiasFrame.pack()

    def seleccion(self, event=None):
        familia = self.tabla.focus()
        # print(self.tabla.item(familia)['text'])
        codigo = self.tabla.item(familia)['values'][0]

        with pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}') as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                'select * from Clientes where IdCliente = ?', [codigo])

            atributos = cursor.fetchone()

            self.cliente = Cliente(atributos)

        self.familia.config(state='normal')
        self.familia.delete(0, tk.END)
        self.familia.insert(0, codigo)
        self.familia.config(state='readonly')

        self.aceptarBoton.config(state='normal', style='Accent.TButton')

        self.popup.destroy()

    def aceptar(self):
        self.insertarPage = InsertarMascotaV(self.padre, self.cliente)
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

        if len(str(nrocuenta)) >= 10:
            showwarning(
                title='Error', message='El numero de cuenta es invalido (max 10 caracteres)')
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
                self.insertarPage = InsertarMascotaV(self.padre, self.cliente)
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
                  'mateov': ['1234', 'MATEO\MSSQLSERVER01']}

    app = App()
    user = tk.StringVar()
    password = tk.StringVar()
    app.mainloop()
