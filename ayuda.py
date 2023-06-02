import customtkinter as ctk
from tkinter import IntVar, StringVar, ttk
from CTkMessagebox import CTkMessagebox as msg
import pyodbc
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        global user, password, lugar

        super().__init__()
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        self.geometry('500x700')
        self.title('Login')
        self.iconbitmap('./image/icono.ico')
        self.resizable(0, 0)
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
        old.pack_forget()
        self.geometry(f'{ancho}x{alto}')
        self.title(titulo)
        self.centrarVentana(ancho, alto)
        self.update()
        new.pack()


class LoginPage(ctk.CTkFrame):
    def __init__(self, master: App = None):
        super().__init__(master=master, width=500, height=700)

        self.padre = master
        self.lugar = None

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
        self.boton.place(x=230, y=180)

        self.combobox = ctk.CTkComboBox(
            self.userFrame, values=['Veterinaria', 'Hotel'], state='readonly')
        self.combobox.set('Veterinaria')
        self.combobox.place(x=30, y=180)

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
                    msg(title='Error en la conexion',
                        message='Usuario o contraseña incorrectos', icon='cancel')

                else:
                    user.set(self.user)
                    password.set(self.passwd)
                    print(user.get())
                    self.lugar = self.combobox.get()
                    self.eleccion()

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

    def eleccion(self):
        if self.lugar == 'Veterinaria':
            self.padre.cambioVentana(
                self, self.padre.mainPageVeterinaria, 1000, 600, 'Cute Pets - Veterinaria')
        else:
            self.padre.cambioVentana(
                self, self.padre.mainPageHotel, 1000, 600, 'Cute Pets - Hotel')


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

        self.ModificarPageV = ModificarPageV(self)

        ctk.CTkButton(self, text='Consultas', width=210,
                      height=40).place(x=20, y=30)

        ctk.CTkButton(self, text='Insertar', width=210,
                      height=40).place(x=20, y=100)

       
        ctk.CTkButton(self, text='Modificar', width=210,
                      height=40,command=self.aModificar).place(x=20, y=170)

        ctk.CTkButton(self, text='Eliminar', width=210,
                      height=40).place(x=20, y=240)

        ctk.CTkButton(self, text='Consulta Personalizada', width=210,
                      height=40).place(x=20, y=310)

        self.imagen = ctk.CTkImage(dark_image=Image.open(
            './image/logo_sinletras.jpg'), size=(210, 180))

        ctk.CTkLabel(
            self, width=190, height=160, image=self.imagen, text='').place(x=20, y=400)
        
    def aModificar(self):
        self.padre.cambioVentana(self, self.ModificarPageV, 700, 480, "Modificar Mascota")
        
class ModificarPageV(ctk.CTkFrame):
    
    def __init__(self,master:VeterinariaPage):
        super().__init__(master=master.padre,width=700,height=480)
        
        self.padre = master
        self.ancestro = self.padre.padre
        self.conexion = pyodbc.connect(
                        f'DRIVER={{SQL Server}};SERVER={conexiones["mateo_vet"][1]};DATABASE=FinalVeterinaria;UID=mateo_vet;PWD=Passw0rd')
        self.cursor = self.conexion.cursor()

        ctk.CTkButton(self,text='Volver',command=self.aPrincipal).place(x=10,y=10)

        ctk.CTkLabel(self,text='Buscar').place(x=30,y=60)
        self.espacioBuscar = ctk.CTkEntry(self,width=150,height=20)
        self.espacioBuscar.place(x=30,y=90)
        self.botonBuscar = ctk.CTkButton(self,width=80,height=25,text='Buscar',command=self.BuscarMascotas)
        self.botonBuscar.place(x=95,y=118)
        
        self.eleccionCampo = StringVar()
        self.botonRadAlias = ctk.CTkRadioButton(self,text='Alias',variable=self.eleccionCampo,value='Alias',command=self.EleccionCampo)
        self.botonRadAlias.place(x=220,y=90)
        self.botonRadFam = ctk.CTkRadioButton(self,text='Familia',variable=self.eleccionCampo,value='Apellido',command=self.EleccionCampo)
        self.botonRadFam.place(x=310,y=90)
        self.botonRadEspecie = ctk.CTkRadioButton(self,text='Especie',variable=self.eleccionCampo,value='Especie',command=self.EleccionCampo)
        self.botonRadEspecie.place(x=410,y=90)
        
        self.eleccionEspecie = StringVar()
        self.CBoxEspecie = ctk.CTkComboBox(self,variable=self.eleccionEspecie,values=['Canino', 'Felino'], state='disabled')
        self.CBoxEspecie.place(x=520,y=88)
        
        self.Tabla = ctk.CTkFrame(self,width=640,height=210)
        self.Tabla.place(x=35,y=160)
       
        self.Cod = StringVar()
        ctk.CTkLabel(self,text='Código de Mascota').place(x=32,y=390)
        self.textoCod = ctk.CTkEntry(self,width=120,height=30,textvariable=self.Cod)
        self.textoCod.place(x=30,y=420)
        self.botonIr = ctk.CTkButton(self,text='Ir a perfil',width=90,height=30,command=self.aPerfil)
        self.botonIr.place(x=570,y=420)
        
        self.atributos=[]

    def EleccionCampo(self):
        self.campoElegido = str(self.eleccionCampo.get())
        if self.campoElegido == 'Especie':
            self.espacioBuscar.delete(0,30)
            self.espacioBuscar.configure(state='disabled')
            self.CBoxEspecie.configure(state='readonly')
        else:
            self.CBoxEspecie.set('')
            self.espacioBuscar.configure(state='normal')
            self.CBoxEspecie.configure(state='disabled')

    def BuscarMascotas(self):
        if self.campoElegido=='Especie':
            self.textoBuscar = self.eleccionEspecie.get()
        else:
            self.textoBuscar = self.espacioBuscar.get()
        
        self.cursor.execute('exec BuscarMascota ?,? ',(self.campoElegido,self.textoBuscar))
        resultados = self.cursor.fetchall()
        print(' ')
        for r in resultados:
            print(r)
    
    def Reporte(self):
        self.cursor.execute('exec ReporteAtendidos2 ?,? ',('2022-12-15','2023-01-01'))
        resultados = self.cursor.fetchall()
        for r in resultados:
            print(r) 
    
    def aPrincipal(self):
        self.ancestro.cambioVentana(self, self.padre,1000,600,'Cute Pets - Veterinaria')

    def aPerfil(self):
        
        self.cursor.execute('exec InfoMascota ?',str(self.Cod.get()))
        info = self.cursor.fetchone()
        for k in info:
            self.atributos.append(k)
        print(self.atributos)
        
        self.PerfilMascotaV = PerfilMascotaV(self,self.atributos)
        self.atributos=[]
        self.ancestro.cambioVentana(self, self.PerfilMascotaV,290,540, "Perfil")

class PerfilMascotaV(ctk.CTkFrame):
    def __init__(self, master:ModificarPageV, atributos):
        super().__init__(master=master.padre.padre,width=290,height=540)
        self.padre = master
        self.atributos = atributos
        print(self.atributos)
        self.ancestro = self.padre.padre.padre
        self.conexion = pyodbc.connect(
                        f'DRIVER={{SQL Server}};SERVER={conexiones["mateo_vet"][1]};DATABASE=FinalVeterinaria;UID=mateo_vet;PWD=Passw0rd')
        self.cursor = self.conexion.cursor()

        ctk.CTkButton(self,text='Cerrar',command=self.aModificar).place(x=10,y=10)
        ctk.CTkLabel(self,text='Código de').place(x=36,y=70)
        ctk.CTkLabel(self,text='Mascota').place(x=41,y=92)
        self.CodMuestra = ctk.CTkEntry(self,state='readonly',textvariable=self.padre.Cod,width=70,height=20)
        self.CodMuestra.place(x=120,y=78)

        ctk.CTkLabel(self,text='Datos Personales').place(x=105,y=150)
    
        ctk.CTkLabel(self,text='Alias').place(x=20,y=180)
        self.aliasNuevo = ctk.CTkEntry(self,width=90,height=20)
        self.aliasNuevo.place(x=18,y=205)
        self.aliasNuevo.insert(0,self.atributos[0])

        self.pelo = StringVar()
        self.colores = {
            'Felino':['Negro','Blanco','Gris','Naranja','Cafe','Manchado'],
            'Canino':['Negro','Blanco','Gris','Dorado','Cafe','Manchado']
            }
        ctk.CTkLabel(self,text='Color de pelo').place(x=20,y=270)
        self.peloNuevo = ctk.CTkComboBox(self,width=90,height=20,variable=self.pelo,values=self.colores[self.atributos[6]],state='readonly')
        self.peloNuevo.place(x=18,y=295)
        self.peloNuevo.set(self.atributos[1])

        self.size = StringVar()
        ctk.CTkLabel(self,text='Tamaño').place(x=20,y=360)
        self.sizeNuevo = ctk.CTkComboBox(self,width=90,height=20,values=['S','M','G'],variable=self.size,state='readonly')
        self.sizeNuevo.place(x=18,y=385)
        self.sizeNuevo.set(self.atributos[3])
    
        self.raza = StringVar()
        self.razas = {
            'Felino': ['Siames', 'Siberiano', 'Mestizo', 'Bengali', 'Yoda', 'Birmano', 'Persa', 'Azul ruso'],
            'Canino': ['Labrador', 'Pastor Aleman', 'Caniche', 'Cocker', 'Chihuahua', 'Bulldog', 'Yorkshire', 'Pastor Ingles', 'Pincher']
        }
        ctk.CTkLabel(self,text='Raza').place(x=170,y=180)
        self.razaNuevo = ctk.CTkComboBox(self,width=90,height=20,variable=self.raza,values=self.razas[self.atributos[6]],state='readonly')
        self.razaNuevo.place(x=168,y=205)
        self.razaNuevo.set(self.atributos[2])

        self.aux = StringVar()
        self.aux.set(self.atributos[4])
        ctk.CTkLabel(self,text='Familia').place(x=170,y=270)
        self.famNuevo = ctk.CTkEntry(self,width=90,height=20,state='readonly',textvariable=self.aux)
        self.famNuevo.place(x=168,y=295)

        ctk.CTkLabel(self,text='Codigo Familia').place(x=170,y=325)
        self.IdCliente = ctk.CTkEntry(self,width=90,height=20)
        self.IdCliente.place(x=168,y=350)
        self.IdCliente.insert(0,self.atributos[5])
        
        self.famBuscarBoton = ctk.CTkButton(self,text='Ver familias',width=60,height=20)
        self.famBuscarBoton.place(x=170,y=390)
        
        self.guardarBoton = ctk.CTkButton(self,text='Guardar cambios',command=self.ModificarMascota)
        self.guardarBoton.place(x=78,y=480) 

    def aModificar(self):
        self.ancestro.cambioVentana(self, self.padre,700,480,'Modificar Mascota')

    def ModificarMascota(self):
        self.comprobando = []
        if self.aliasNuevo.get()!=self.atributos[0]:
            print('distinto alias')
            self.comprobando.append('exec ')
        if self.peloNuevo.get()!=self.atributos[1]:
            print('distinto color de pelo')

        if self.sizeNuevo.get()!=self.atributos[3]:
            print('distinto tamaño')

        if self.razaNuevo.get()!=self.atributos[2]:
            print('distinta raza')

        if self.IdCliente.get()!=self.atributos[5]:
            print('asociado a nuevo cliente')

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

conexiones = {'josek': ['password', 'JoseK-Laptop\SQLEXPRESS'],
              'nangui': ['soychurro', 'BrunoPC'],
              'mateo_vet':['Passw0rd','MATEO\MSSQLSERVER01']}

app = App()
user = StringVar()
password = StringVar()
app.mainloop()
