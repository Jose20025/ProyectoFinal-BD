from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo,askquestion 
import tkinter as tk
import pyodbc
from PIL import ImageTk, Image
import ctypes

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
                    print(user.get())
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
        self.ModificarPageV = ModificarPageV(self)

        ttk.Button(self, text='Consultas', width=40).place(x=20, y=30)

        ttk.Button(self, text='Insertar', width=40).place(x=20, y=100)

        ttk.Button(self, text='Modificar', width=40,
                   command=self.aModificar).place(x=20, y=170)

        ttk.Button(self, text='Eliminar', width=40).place(x=20, y=240)

        ttk.Button(self, text='Consulta Personalizada',
                   width=40).place(x=20, y=310)

        self.imagen = ImageTk.PhotoImage(Image.open(
            './image/logo-transparente.png').resize((220, 200)))

        ttk.Label(self, image=self.imagen).place(x=20, y=350)

    def aModificar(self):
        self.padre.cambioVentana(self, self.ModificarPageV, [
            700, 480], "Modificar Mascota")


class ModificarPageV(ttk.Frame):
    def __init__(self, master: VeterinariaPage):
        super().__init__(master=master.padre, width=700, height=480)

        self.padre = master
        print(self.padre)
        self.conexion = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}')
        self.cursor = self.conexion.cursor()

        ttk.Button(self, text='Volver',command=self.aPrincipal).place(x=10, y=10)

        ttk.Label(self, text='Buscar').place(x=26, y=60)
        self.espacioBuscar = ttk.Entry(self, width=16)
        self.espacioBuscar.place(x=28, y=90)
        self.botonBuscar = ttk.Button(self, width=8, text='Buscar', command=self.BuscarMascotas)
        self.botonBuscar.place(x=90, y=135)

        self.eleccionCampo = tk.StringVar()
        self.botonRadAlias = ttk.Radiobutton(self, text='Alias', variable=self.eleccionCampo, value='Alias', command=self.EleccionCampo)
        self.botonRadAlias.place(x=205, y=90)
        self.botonRadFam = ttk.Radiobutton(self, text='Familia', variable=self.eleccionCampo, value='Apellido', command=self.EleccionCampo)
        self.botonRadFam.place(x=300, y=90)
        self.botonRadEspecie = ttk.Radiobutton(self, text='Especie', variable=self.eleccionCampo, value='Especie', command=self.EleccionCampo)
        self.botonRadEspecie.place(x=405, y=90)

        self.eleccionEspecie = tk.StringVar()
        self.CBoxEspecie = ttk.Combobox(self, values=['Canino', 'Felino'], state='disabled',width=12)
        self.CBoxEspecie.place(x=520, y=88)

        self.Cod = tk.StringVar()
        ttk.Label(self, text='Código de Mascota').place(x=32, y=390)
        self.textoCod = ttk.Entry(self, width=12, textvariable=self.Cod)
        self.textoCod.place(x=30, y=420)
        self.botonIr = ttk.Button(self, text='Ir a perfil', width=10, command=self.aPerfil)
        self.botonIr.place(x=570, y=420)

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

    def BuscarMascotas(self):
        print(self.campoElegido)
        if self.campoElegido == 'Especie':
            self.textoBuscar = self.CBoxEspecie.get()
            print(self.textoBuscar)
        else:
            self.textoBuscar = self.espacioBuscar.get()

        self.cursor.execute('exec BuscarMascota ?,? ',(self.campoElegido, self.textoBuscar))
        resultados = self.cursor.fetchall()
        print(' ')
        for r in resultados:
            print(r)

    def Reporte(self):
        self.cursor.execute('exec ReporteAtendidos2 ?,? ',('2022-12-15', '2023-01-01'))
        resultados = self.cursor.fetchall()
        for r in resultados:
            print(r)

    def aPrincipal(self):
        self.padre.padre.cambioVentana(self, self.padre, [1000, 600], 'Cute Pets - Veterinaria')

    def aPerfil(self):

        self.cursor.execute('exec InfoMascota ?', str(self.Cod.get()))
        info = self.cursor.fetchone()
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
        self.conexion = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={conexiones[user.get()][1]};DATABASE=FinalVeterinaria;UID={user.get()};PWD={password.get()}')
        self.cursor = self.conexion.cursor()

        ttk.Button(self, text='Cerrar',command=self.aModificar).place(x=10, y=10)
        ttk.Label(self, text='Código de').place(x=36, y=70)
        ttk.Label(self, text='Mascota').place(x=41, y=92)
        self.CodMuestra = ttk.Entry(self, state='readonly', textvariable=self.padre.Cod, width=10)
        self.CodMuestra.place(x=130, y=78)

        ttk.Label(self, text='Datos Personales',background='#7ce6dd',foreground='#000000',anchor='center').place(x=130, y=150)

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
        self.peloNuevo = ttk.Combobox(self, width=15, height=20, textvariable=self.pelo,values=self.colores[self.atributos[6]], state='readonly')
        self.peloNuevo.place(x=18, y=305)
        self.peloNuevo.set(self.atributos[1])

        self.size = tk.StringVar()
        ttk.Label(self, text='Tamaño').place(x=20, y=370)
        self.sizeNuevo = ttk.Combobox(self, width=15, height=20, values=['S', 'M', 'G'],textvariable=self.size,state='readonly')
        self.sizeNuevo.place(x=18, y=395)
        self.sizeNuevo.set(self.atributos[3])

        self.raza = tk.StringVar()
        self.razas = {
            'Felino': ['Siames', 'Siberiano', 'Mestizo', 'Bengali', 'Yoda', 'Birmano', 'Persa', 'Azul ruso'],
            'Canino': ['Labrador', 'Pastor Aleman', 'Caniche', 'Cocker', 'Chihuahua', 'Bulldog', 'Yorkshire', 'Pastor Ingles', 'Pincher']
        }
        ttk.Label(self, text='Raza').place(x=230, y=190)
        self.razaNuevo = ttk.Combobox(self, width=15, height=20, textvariable=self.raza, values=self.razas[self.atributos[6]], state='readonly')
        self.razaNuevo.place(x=230, y=215)
        self.razaNuevo.set(self.atributos[2])

        self.aux = tk.StringVar()
        self.aux.set(self.atributos[4])
        ttk.Label(self, text='Familia').place(x=230, y=280)
        self.famNuevo = ttk.Entry(self, width=15, state='readonly', textvariable=self.aux)
        self.famNuevo.place(x=230, y=305)

        ttk.Label(self, text='Codigo Familia').place(x=230, y=370)
        self.IdCliente = ttk.Entry(self, width=15)
        self.IdCliente.place(x=230, y=395)
        self.IdCliente.insert(0, self.atributos[5])

        self.famBuscarBoton = ttk.Button(self, text='Ver familias', width=12)
        self.famBuscarBoton.place(x=230, y=440)

        self.guardarBoton = ttk.Button(self, text='Guardar cambios', command=self.ModificarMascota)
        self.guardarBoton.place(x=230, y=530)

    def aModificar(self):
        self.ancestro.cambioVentana(self, self.padre, [700, 480], 'Modificar Mascota')

    def ModificarMascota(self):
        respuesta = askquestion('Confirmación','¿Desea guardar los cambios?')
        if respuesta=='yes':
            print('se guardaron los cambios')
            
            if self.aliasNuevo.get() != self.atributos[0]:
                print('distinto alias')
                self.cursor.execute('exec ModificarMascota ?,?,?'(self.atributos[7],'Alias',self.aliasNuevo.get()))
            
            if self.peloNuevo.get() != self.atributos[1]:
                print('distinto color de pelo')
                self.cursor.execute('exec ModificarMascota ?,?,?'(self.atributos[7],'Color_pelo',self.peloNuevo.get()))

            if self.sizeNuevo.get() != self.atributos[3]:
                print('distinto tamaño')
                self.cursor.execute('exec ModificarMascota ?,?,?'(self.atributos[7],'Tamaño',self.peloNuevo.get()))

            if self.razaNuevo.get() != self.atributos[2]:
                print('distinta raza')
                self.cursor.execute('exec ModificarMascota ?,?,?'(self.atributos[7],'Raza',self.peloNuevo.get()))

            if self.IdCliente.get() != self.atributos[5]:
                print('asociado a nuevo cliente')
                self.cursor.execute('exec ModificarMascota ?,?,?'(self.atributos[7],'IdCliente',self.peloNuevo.get()))
        else:
            print('que maricon')
       

conexiones = {'josek': ['password', 'JoseK-Laptop\SQLEXPRESS'],
              'nangui': ['soychurro', 'BrunoPC'],
              'mateo_vet': ['Passw0rd', 'MATEO\MSSQLSERVER01']}

app = App()
user = tk.StringVar()
password = tk.StringVar()
app.mainloop()
