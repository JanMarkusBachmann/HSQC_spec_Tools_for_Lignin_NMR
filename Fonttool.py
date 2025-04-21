import customtkinter as ctk
import tkinter.filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")

        self.elemnts = []
        self.filereadpath = ''
        self.filereadpathline = 'Press and select file'
        self.deadspacesize = 1
        self.currentfontdict = dict()
        self.currentfontdictsizes = dict()
        self.currentfontletter = ' '
        self.fonteditor_pxfromzero_rows = 1
        self.fonteditor_pxfromzero_cols = 1
        self.pxframe = Pixelframeing(self, self.fonteditor_pxfromzero_rows, self.fonteditor_pxfromzero_cols)
        self.pxframeletterentry = ctk.CTkEntry(self)
        self.pxframeletterentry.bind('<Key-Return>', self.pxframeletterchange)
        self.pxframelettermessage = ctk.CTkLabel(self, text="Enter the letter that you want to edit and press enter")

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
        self.currentfontdict.clear()
        self.currentfontdictsizes.clear()
        self.fonteditor()
    def increaserow(self):
        self.pxframe.nrows += 1
        self.pxframe.gridreset()
    def decreaserow(self):
        if self.pxframe.nrows > 0:
            self.pxframe.nrows -= 1
            self.pxframe.gridreset()
    def increasecolumn(self):
        self.pxframe.ncols += 1
        self.pxframe.gridreset()
    def decreasecolumn(self):
        if self.pxframe.ncols > 0:
            self.pxframe.ncols -= 1
            self.pxframe.gridreset()
    def pxframeletterchange(self, event):
        RN = self.pxframeletterentry.get()
        if len(RN) > 1:
            self.pxframelettermessage.configure(text="Plase enter a single character!")
        else:
            self.pxframelettermessage.configure(text="Enter the letter that you want to edit and press enter")
            if RN != self.currentfontletter:
                self.currentfontletter = RN
                self.pxframe.gridreset()
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
                    let = line.strip('\t').strip('\n').split(':')[0].strip(' ').strip(',').strip("'")
                    RN = []
                    for cord in line.strip('\t').strip('\n').split(':')[1].split('), '):
                        temp = (cord.strip(' ').strip('(').strip('(').strip(')').strip(')').split(', '))
                        RN.append(tuple((int(temp[0]), int(temp[1].strip('),')))))
                    self.currentfontdict.update({let: tuple(RN)})
                if issizedict:
                    let = line.strip('\t').strip('\n').split(':')[0].strip(' ').strip(',').strip("'")
                    RN = []
                    for cord in line.strip('\t').strip('\n').split(':')[1].split('), '):
                        temp = (cord.strip(' ').strip('(').strip('(').strip(')').strip(')').split(', '))
                        RN.append(tuple((int(temp[0]), int(temp[1]))))
                        #create minmax values for current font rows and cols
                        if abs(int(temp[0])) > self.fonteditor_pxfromzero_rows:
                            self.fonteditor_pxfromzero_rows = abs(int(temp[0]))
                        if abs(int(temp[1])) > self.fonteditor_pxfromzero_cols:
                            self.fonteditor_pxfromzero_cols = abs(int(temp[1]))

                    self.currentfontdictsizes.update({let: tuple(RN)})
                if line[0:16] == 'letters = dict({':
                    isdict = True
                if line == 'minmax = dict({\n':
                    issizedict = True


        self.fonteditor()
    def fonteditor(self):
        self.depack()
        self.pxframe.gridreset()

        self.elemnts.append(ctk.CTkLabel(self, text="Please press on a pixle to activate(white) or deactivate(black) it"))
        self.elemnts.append(ctk.CTkFrame(self))
        rowincB = ctk.CTkButton(self.elemnts[-1], text='Increase row pixels', command=self.increaserow)
        rowincB.pack(side='left', padx=10)
        rowdecB = ctk.CTkButton(self.elemnts[-1], text='decrease row pixels', command=self.decreaserow)
        rowdecB.pack(side='left', padx=10)
        self.elemnts.append(ctk.CTkFrame(self))
        colincB = ctk.CTkButton(self.elemnts[-1], text='Increase row pixels', command=self.increasecolumn)
        colincB.pack(side='left', padx=10)
        coldecB = ctk.CTkButton(self.elemnts[-1], text='decrease row pixels', command=self.decreasecolumn)
        coldecB.pack(side='left', padx=10)
        self.elemnts.append(self.pxframelettermessage)
        self.elemnts.append(self.pxframeletterentry)
        self.elemnts.append(self.pxframe)

        self.repack()

class Pixelframeing(ctk.CTkFrame):
    def __init__(self, master, nrows, ncols, **kwargs):
        super().__init__(master, **kwargs)
        self.appmaster = master
        self.nrows = nrows #int rows
        self.ncols = ncols #int cols
        self.rows = [] #full of Pixelframeingcols objects
        self.buttons = dict() # (row,col): Pxbutton()
        self.gridreset()

    def repack(self):
        for obj in self.rows:
            obj.pack(side='bottom')
    def depack(self):
        for obj in self.rows:
            obj.pack_forget()
        self.rows = []
    def gridreset(self):
        self.depack()
        self.buttons.clear()
        self.nrows = self.appmaster.fonteditor_pxfromzero_rows
        self.ncols = self.appmaster.fonteditor_pxfromzero_cols
        for rownumb in range(-self.nrows, self.nrows + 1):
            self.rows.append(Pixelframeingrow(self, self.ncols, rownumb))

            # check if currentfontdict and size are empty, if not, readin the first char
        if len(self.appmaster.currentfontdict.keys()) != 0:
            try:
                for cord in self.appmaster.currentfontdict[self.appmaster.currentfontletter]:
                    self.buttons[cord].statechange()
            except KeyError:
                self.appmaster.pxframelettermessage.configure(text='This letter has not been made')

        self.repack()

class Pixelframeingrow(ctk.CTkFrame):
    def __init__(self, master, ncols, rownumb, **kwargs):
        super().__init__(master, **kwargs)
        self.framemaster = master
        self.buttons = []
        self.ncols = ncols
        self.rownumb = rownumb

        self.gridreset()

    def repack(self):
        for obj in self.buttons:
            obj.pack(side='left')
    def depack(self):
        for obj in self.buttons:
            obj.pack_forget()
        self.buttons = []
    def gridreset(self):
        self.depack()
        for colnumb in range(-self.ncols, self.ncols + 1):
            self.buttons.append(Pxbutton(self, colnumb, self.rownumb))
        self.repack()

class Pxbutton(ctk.CTkButton):
    def __init__(self, master, col, row, **kwargs):
        super().__init__(master, text='',width=25, height=25, command=self.statechange, **kwargs)
        self.rowmaster = master
        self.row = row
        self.col = col
        self.state = False
        self.configure(fg_color = 'black')
        self.rowmaster.framemaster.buttons.update({(self.row, self.col): self})

    def statechange(self):
        if self.state == False:
            self.state = True
        elif self.state == True:
            self.state = False
        if self.state == False:
            self.configure(fg_color = 'black')
        else:
            self.configure(fg_color = 'white')
    def __del__(self):
        # Remove button from rowmaster.framemaster.buttons list if it exists
        if (self.row, self.col) in self.rowmaster.framemaster.buttons.keys():
            self.rowmaster.framemaster.buttons.pop((self.row, self.col))

        # Remove the button from rowmaster elements list
        if self in self.rowmaster.buttons:
            self.rowmaster.buttons.remove(self)

app = App()
app.mainloop()