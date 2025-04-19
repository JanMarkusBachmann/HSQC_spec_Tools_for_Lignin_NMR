import customtkinter as ctk
import tkinter.filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")

        self.elemnts = []
        self.filereadpath = ''
        self.filereadpathline = 'Press and select file'
        self.currentfontdict = dict()
        self.currentfontdictsizes = dict()

        self.firstwindows()

    def repack(self):
        for obj in self.elemnts:
            obj.pack(pady = 10)
    def depack(self):
        for obj in self.elemnts:
            obj.pack_forget()
        self.elemnts = []
    def firstwindows(self):
        self.depack()
        self.title('Font creation and modification tool')
        self.elemnts.append(ctk.CTkLabel(self, text="Hello! This is a font creation and modification tool.\nPlease select what you want to do."))
        self.elemnts.append(ctk.CTkButton(self, text="Read and modify a font from .py file", command=self.readfont))
        self.elemnts.append(ctk.CTkButton(self, text="create a font and save it as .py file", command=self.createfont))
        self.repack()

    def readfont(self):
        self.depack()
        if self.filereadpathline == 'Press and select file':
            self.title('Font creation and modification tool: Select file')
        else:
            self.title(f'Font creation and modification tool: {self.filereadpathline}')
        self.elemnts.append(ctk.CTkLabel(self, text="Please select .py file that you want to read"))
        self.elemnts.append(ctk.CTkButton(self, text=self.filereadpathline, command=self.pathselect))
        self.elemnts.append(ctk.CTkButton(self, text='Edit font', command=self.readandeditfont))
        self.elemnts.append(ctk.CTkButton(self, text='Back', fg_color='red', hover_color='orange', command=self.firstwindows))
        self.repack()

    def createfont(self):
        self.depack()

        self.repack()

    def pathselect(self):
        path = str(tkinter.filedialog.askopenfile())
        self.filereadpath = path.split("'")[1]
        self.filereadpathline = self.filereadpath.split('/')[-1]
        self.readfont()

    def readandeditfont(self):
        #read
        self.fonteditor()

    def fonteditor(self):
        self.depack()

        self.repack()


app = App()
app.mainloop()