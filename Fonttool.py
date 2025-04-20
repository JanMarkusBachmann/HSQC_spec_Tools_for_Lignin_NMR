import customtkinter as ctk
import tkinter.filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")

        self.elemnts = []
        self.filereadpath = ''
        self.filereadpathline = 'Press and select file'
        self.deadspacesize = 1
        self.currentfontdict = dict()
        self.currentfontdictsizes = dict()
        self.currentfontletter = ''
        self.fonteditor_pxfromzero_rows = 0
        self.fonteditor_pxfromzero_cols = 0
        self.pxframe = Pixelframeing(self, self.fonteditor_pxfromzero_rows, self.fonteditor_pxfromzero_cols)

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
        with open(self.filereadpath, 'r') as f:
            isdict = False
            issizedict = False
            for line in f:
                if line[0:9] == 'deadspace':
                    self.deadspacesize = line.split(' ')[-1].strip('\n')
                if line == ('})\n'):
                    isdict = False
                    issizedict = False
                if isdict and line == """    ,' ': tuple()\n""":
                    self.currentfontdict.update({' ': tuple()})
                elif isdict:
                    let = line.strip('\t').strip('\n').split(':')[0].strip(' ').strip(',')
                    RN = []
                    for cord in line.strip('\t').strip('\n').split(':')[1].split('), '):
                        temp = (cord.strip(' ').strip('(').strip('(').strip(')').strip(')').split(', '))
                        RN.append(tuple((int(temp[0]), int(temp[1].strip('),')))))
                    self.currentfontdict.update({let: tuple(RN)})
                    print(f'letter: {let}, list:{RN}')
                if issizedict:
                    let = line.strip('\t').strip('\n').split(':')[0].strip(' ').strip(',')
                    RN = []
                    for cord in line.strip('\t').strip('\n').split(':')[1].split('), '):
                        temp = (cord.strip(' ').strip('(').strip('(').strip(')').strip(')').split(', '))
                        RN.append(tuple((int(temp[0]), int(temp[1]))))
                    self.currentfontdictsizes.update({let: tuple(RN)})
                if line[0:16] == 'letters = dict({':
                    isdict = True
                if line == 'minmax = dict({\n':
                    issizedict = True

        self.currentfontletter = self.currentfontdict.keys()[0]
        self.fonteditor()

    def fonteditor(self):
        self.depack()


        self.repack()

class Pixelframeing(ctk.CTkFrame):
    def __init__(self, master, nrows, ncols, **kwargs):
        super().__init__(master, **kwargs)
        self.nrows = nrows #int rows
        self.ncols = ncols #int cols
        self.elements = [] #full of Pixelframeingcols objects
        self.index = 0
        self.gridreset()

    def repack(self):
        for obj in self.elements:
            obj[1].pack(pady=5, side='down')

    def depack(self):
        for obj in self.elements:
            obj[1].pack_forget()
        self.elements = []

    def gridreset(self):
        self.depack()
        for rownumb in range(-self.nrows, self.nrows + 1):
            self.elements.append([rownumb, Pixelframeingcols(self, self.ncols, rownumb)])

        self.repack()

class Pixelframeingcols(ctk.CTkFrame):
    def __init__(self, master, ncols, rownumb, **kwargs):
        super().__init__(master, **kwargs)
        self.elements = []
        self.index = 0
        self.ncols = ncols
        self.rownumb = rownumb

        self.gridreset()

    def repack(self):
        for obj in self.elements:
            obj[1].pack(padx=5)

    def depack(self):
        for obj in self.elements:
            obj[1].pack_forget()
        self.elements = []

    def gridreset(self):
        self.depack()
        for colnumb in range(-self.ncols, self.ncols + 1):
            self.elements.append([colnumb, ctk.CTkButton(self, width=10, height=10, text='')])
        self.repack()


app = App()
app.mainloop()