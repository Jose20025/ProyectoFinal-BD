import customtkinter as ctk
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        self.geometry('500x700')
        self.iconbitmap('./image/icono.ico')

        self.loginPage = ctk.CTkFrame(self, width=500, height=700)

        image = ctk.CTkImage(dark_image=Image.open(
            './image/fondo.jpg'), size=(500, 700))
        background_label = ctk.CTkLabel(self.loginPage, image=image, text='')
        background_label.pack()

        self.userFrame = ctk.CTkFrame()
        self.usernamelabel = ctk.CTkLabel(
            self.loginPage, text='Username')
        self.usernamelabel.place(x=90, y=460)

        self.loginPage.pack()


app = App()
app.mainloop()
