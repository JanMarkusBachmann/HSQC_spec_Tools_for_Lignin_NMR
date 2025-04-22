from collections import deque

import customtkinter as ctk
import tkinter.filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")

        self.elemnts = []
        self.filereadpath = ''
        self.filereadpathline = 'Press and select file'
        self.deadspacesize = 1
        self.currentfontdict = dict()
        self.currentfontdictsizes = dict()
        self.currentlettersLabel = ctk.CTkLabel(self, text=f'Current letters in font: {" ".join(self.currentfontdict.keys())}')
        self.currentfontletter = ' '
        self.fonteditor_pxfromzero_rows = 1
        self.fonteditor_pxfromzero_cols = 1
        self.pxframe = Pixelframeing(self, self.fonteditor_pxfromzero_rows, self.fonteditor_pxfromzero_cols)
        self.pxframeletterentry = ctk.CTkEntry(self)
        self.pxframeletterentry.bind('<Key-Return>', self.pxframeletterchange)
        self.pxframelettermessage = ctk.CTkLabel(self, text="Enter the letter that you want to edit and press enter")

        self.currentlettermin = (-1, -1)
        self.currentlettermax = (1, 1)

        self.colminmaxframe = ctk.CTkFrame(self)

        self.colminmaxlabel = ctk.CTkLabel(self.colminmaxframe, text='Min/Max col pixels: from > ')
        self.colminmaxlabel.pack(side='left')
        self.currentlettercolminEntry = ctk.CTkEntry(self.colminmaxframe)
        self.currentlettercolminEntry.pack(side='left')
        self.colminmaxlabelto = ctk.CTkLabel(self.colminmaxframe, text=' > to > ').pack(side='left')
        self.currentlettercolmaxEntry = ctk.CTkEntry(self.colminmaxframe)
        self.currentlettercolmaxEntry.pack(side='left')

        self.rowminmaxframe = ctk.CTkFrame(self)

        self.rowminmaxlabel = ctk.CTkLabel(self.rowminmaxframe, text='Min/Max row pixels: from > ')
        self.rowminmaxlabel.pack(side='left')
        self.currentletterrowminEntry = ctk.CTkEntry(self.rowminmaxframe)
        self.currentletterrowminEntry.pack(side='left')
        self.rowminmaxlabelto = ctk.CTkLabel(self.rowminmaxframe, text=' > to > ').pack(side='left')
        self.currentletterrowmaxEntry = ctk.CTkEntry(self.rowminmaxframe)
        self.currentletterrowmaxEntry.pack(side='left')
        self.savefilename = ''


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
        self.fonteditor_pxfromzero_rows += 1
        self.readrowcolminmax()
        self.pxframe.gridreset()
    def decreaserow(self):
        if self.fonteditor_pxfromzero_rows > 0:
            self.fonteditor_pxfromzero_rows -= 1
            self.readrowcolminmax()
            self.pxframe.gridreset()
    def increasecolumn(self):
        self.fonteditor_pxfromzero_cols += 1
        self.readrowcolminmax()
        self.pxframe.gridreset()
    def decreasecolumn(self):
        if self.fonteditor_pxfromzero_cols > 0:
            self.fonteditor_pxfromzero_cols -= 1
            self.readrowcolminmax()
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
                self.currentlettermin = self.currentfontdictsizes[self.currentfontletter][0]
                self.currentlettermax = self.currentfontdictsizes[self.currentfontletter][1]
                self.colminmaxlabel.configure(text=f'Min/Max col pixels: currently({self.currentlettermin[1]} > {self.currentlettermax[1]}) from > ')
                self.rowminmaxlabel.configure(text=f'Min/Max row pixels: currently({self.currentlettermin[0]} > {self.currentlettermax[0]}) from > ')
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

        self.currentlettersLabel.configure(text=f'Current letters in font: {" ".join(self.currentfontdict.keys())}')
        self.fonteditor()
    def readrowcolminmax(self):
        if (
                self.currentletterrowminEntry.get().strip() != '' and
                self.currentlettercolminEntry.get().strip() != '' and
                self.currentletterrowmaxEntry.get().strip() != '' and
                self.currentlettercolmaxEntry.get().strip() != ''
        ):
            self.currentlettermin = (self.currentletterrowminEntry.get(), self.currentlettercolminEntry.get())
            self.currentlettermax = (self.currentletterrowmaxEntry.get(), self.currentlettercolmaxEntry.get())
        else:
            self.currentlettermin = (-self.fonteditor_pxfromzero_rows, -self.fonteditor_pxfromzero_cols)
            self.currentlettermax = (self.fonteditor_pxfromzero_rows, self.fonteditor_pxfromzero_cols)

        self.colminmaxlabel.configure(
            text=f'Min/Max col pixels: currently({self.currentlettermin[1]} > {self.currentlettermax[1]}) from > ')
        self.rowminmaxlabel.configure(
            text=f'Min/Max row pixels: currently({self.currentlettermin[0]} > {self.currentlettermax[0]}) from > ')
    def addletter(self):
        RN = self.pxframeletterentry.get()
        self.readrowcolminmax()
        if len(RN) > 1:
            self.pxframelettermessage.configure(text="Plase enter a single character!")
        else:
            if RN not in self.currentfontdict.keys():
                self.pxframelettermessage.configure(text=f"Creating a new letter into font: '{RN}'")
                self.currentlettermin = (-self.fonteditor_pxfromzero_rows, -self.fonteditor_pxfromzero_cols)
                self.currentlettermax = (self.fonteditor_pxfromzero_rows, self.fonteditor_pxfromzero_cols)
                self.currentfontletter = RN
                self.currentfontdict.update({RN: tuple()})
                self.currentfontdictsizes.update({RN: tuple([self.currentlettermin, self.currentlettermax])})
                self.pxframe.gridreset()
                self.colminmaxlabel.configure(
                    text=f'Min/Max col pixels: currently({self.currentlettermin[1]} > {self.currentlettermax[1]}) from > ')
                self.rowminmaxlabel.configure(
                    text=f'Min/Max row pixels: currently({self.currentlettermin[0]} > {self.currentlettermax[0]}) from > ')
                self.currentlettersLabel.configure(text=f'Current letters in font: {" ".join(self.currentfontdict.keys())}')
            else:
                self.pxframelettermessage.configure(text=f"Letter already exists! Switched to '{RN}'")
                if RN != self.currentfontletter:
                    self.currentfontletter = RN
                    self.pxframe.gridreset()
                    self.currentlettermin = self.currentfontdictsizes[self.currentfontletter][0]
                    self.currentlettermax = self.currentfontdictsizes[self.currentfontletter][1]
                    self.colminmaxlabel.configure(
                        text=f'Min/Max col pixels: currently({self.currentlettermin[1]} > {self.currentlettermax[1]}) from > ')
                    self.rowminmaxlabel.configure(
                        text=f'Min/Max row pixels: currently({self.currentlettermin[0]} > {self.currentlettermax[0]}) from > ')
    def clearpxboars(self):
        for px in self.currentfontdict[self.currentfontletter]:
            self.pxframe.buttons[px].statechange()
        self.currentfontdict.update({self.currentfontletter: tuple()})
        self.pxframe.gridreset()
    def savecurrentfont(self):
        dialog = ctk.CTkInputDialog(text="Type in a name for the current font:", title="Select saved font name")
        self.savefilename = dialog.get_input()
        if self.savefilename[-4:-1] != '.py':
            self.savefilename += '.py'

        writedata = []
        writedata.append(f'deadspace = {self.deadspacesize}\n')
        writedata.append('letters = dict({\n')
        first = True
        for letter in self.currentfontdict:
            if first:
                if len(self.currentfontdict[letter]) == 0:
                    writedata.append(f'\t"{letter}" : tuple()\n')
                else:
                    writedata.append(f'\t"{letter}" : {self.currentfontdict[letter]}\n')
                first = False
            else:
                if len(self.currentfontdict[letter]) == 0:
                    writedata.append(f'\t,"{letter}" : tuple()\n')
                else:
                    writedata.append(f'\t,"{letter}" : {self.currentfontdict[letter]}\n')
        writedata.append('})\n')
        first = True
        writedata.append('minmax = dict({\n')
        for letter in self.currentfontdictsizes:
            if first:
                writedata.append(f'\t"{letter}" : {self.currentfontdictsizes[letter]}\n')
                first = False
            else:
                writedata.append(f'\t,"{letter}" : {self.currentfontdictsizes[letter]}\n')
        writedata.append('})\n')

        f = open(self.savefilename, "w")
        f.write(''.join(writedata))
        f.close()

        self.firstwindows()
    def fonteditor(self):
        self.depack()
        self.pxframe.gridreset()

        self.elemnts.append(ctk.CTkLabel(self, text="Please press on a pixle to activate(white) or deactivate(black) it"))
        self.elemnts.append(self.currentlettersLabel)

        self.elemnts.append(ctk.CTkFrame(self))
        ctk.CTkButton(self.elemnts[-1], text='Increase row pixels', command=self.increaserow).pack(side='left', padx=10)
        ctk.CTkButton(self.elemnts[-1], text='decrease row pixels', command=self.decreaserow).pack(side='left', padx=10)

        self.elemnts.append(ctk.CTkFrame(self))
        ctk.CTkButton(self.elemnts[-1], text='Increase row pixels', command=self.increasecolumn).pack(side='left', padx=10)
        ctk.CTkButton(self.elemnts[-1], text='decrease row pixels', command=self.decreasecolumn).pack(side='left', padx=10)

        self.elemnts.append(self.pxframelettermessage)
        self.elemnts.append(self.pxframeletterentry)

        self.elemnts.append(ctk.CTkFrame(self))
        ctk.CTkButton(self.elemnts[-1], text="Clear current board", command=self.clearpxboars).pack(side='right',padx=10)
        ctk.CTkButton(self.elemnts[-1], text="Add a new letter", command=self.addletter).pack(side='right', padx=10)
        ctk.CTkButton(self.elemnts[-1], text="Save current font", command=self.savecurrentfont).pack(side='right', padx=10)

        self.elemnts.append(self.pxframe)

        self.readrowcolminmax()
        self.elemnts.append(self.rowminmaxframe)
        self.elemnts.append(self.colminmaxframe)
        self.elemnts.append(ctk.CTkButton(self, text='Save row/col min-max', command=self.readrowcolminmax))


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
        self.rows.append(ctk.CTkFrame(self))
        for colnumb in range(-self.ncols, self.ncols + 1):
            label = ctk.CTkLabel(self.rows[-1], text=str(colnumb))
            label.pack(side='left', padx=8)
            # check if currentfontdict and size are empty, if not, readin the first char
        if len(self.appmaster.currentfontdict.keys()) != 0 and len(self.appmaster.currentfontdict[self.appmaster.currentfontletter]) != 0:
            try:
                for cord in self.appmaster.currentfontdict[self.appmaster.currentfontletter]:
                    self.buttons[cord].statechange()
            except KeyError:
                self.appmaster.pxframelettermessage.configure(text='This letter has not been made yet')

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
        self.buttons.append(ctk.CTkLabel(self, text=str(self.rownumb)))
        for colnumb in range(-self.ncols, self.ncols + 1):
            self.buttons.append(Pxbutton(self, colnumb, self.rownumb))
        self.buttons.append(ctk.CTkLabel(self, text=str(self.rownumb)))
        self.repack()

class Pxbutton(ctk.CTkButton):
    def __init__(self, master, col, row, **kwargs):
        super().__init__(master, text='',width=30, height=30, command=self.pressed, **kwargs)
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
    def pressed(self):
        self.statechange()
        if tuple([self.row, self.col]) not in self.rowmaster.framemaster.appmaster.currentfontdict[self.rowmaster.framemaster.appmaster.currentfontletter] and self.state:
            tempRN = list(self.rowmaster.framemaster.appmaster.currentfontdict[self.rowmaster.framemaster.appmaster.currentfontletter])
            tempRN.append(tuple([self.row, self.col]))
            self.rowmaster.framemaster.appmaster.currentfontdict.update({self.rowmaster.framemaster.appmaster.currentfontletter: tuple(tempRN)})
        elif tuple([self.row, self.col]) in self.rowmaster.framemaster.appmaster.currentfontdict[self.rowmaster.framemaster.appmaster.currentfontletter] and not self.state:
            tempRN = list(self.rowmaster.framemaster.appmaster.currentfontdict[self.rowmaster.framemaster.appmaster.currentfontletter])
            tempRN.remove(tuple([self.row, self.col]))
            self.rowmaster.framemaster.appmaster.currentfontdict.update({self.rowmaster.framemaster.appmaster.currentfontletter: tuple(tempRN)})
    def __del__(self):
        # Remove button from rowmaster.framemaster.buttons list if it exists
        if (self.row, self.col) in self.rowmaster.framemaster.buttons.keys():
            self.rowmaster.framemaster.buttons.pop((self.row, self.col))

        # Remove the button from rowmaster elements list
        if self in self.rowmaster.buttons:
            self.rowmaster.buttons.remove(self)

app = App()
app.mainloop()