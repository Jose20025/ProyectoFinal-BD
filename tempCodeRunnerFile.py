
        super().__init__(master=master.padre, width=700, height=520)

        self.padre = master
        ttk.Button(self, text='Volver',
                   command=self.aPrincipal).place(x=10, y=10)

        self.tablaFrame = None