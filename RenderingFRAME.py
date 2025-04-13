import png
import font5X7 as fonts


class Pixel:
    presetdict = dict({'r': [1, 0, 0], 'g': [0, 1, 0], 'b': [0, 0, 1], 'w': [1, 1, 1], 'd': [0, 0, 0]}) #red, greed, blue, white, black

    def __init__(self, red=0, green=0, blue=0, colorbitcount=8, preset='-'):
        self.color = [int(red), int(green), int(blue)]
        self.colorbitcoef = 2**colorbitcount - 1
        if preset != '-':
            reeed = self.colorbitcoef * Pixel.presetdict[preset][0]
            greeen = self.colorbitcoef * Pixel.presetdict[preset][1]
            blueee = self.colorbitcoef * Pixel.presetdict[preset][2]
            self.color = [reeed, greeen, blueee]

class FilePNG:
    def __init__(self, width, height, colorbit, background='w', name='picture'):
        self.width, self.height = width, height
        self.colorbitnum = colorbit
        self.data = dict() #tuple(row, col): Pixle()
        self.name = name

        for row in range(self.height):
            for col in range(self.width):
                self.data.update({(row, col): Pixel(preset=background)})

    def filewrite(self, newname='-'):
        filename = ''
        if newname != '-':
            filename = f'{newname}.png'
        else:
            filename = f'{self.name}.png'

        filedata = []
        for row in range(self.height):
            rowdata = []
            for col in range(self.width):
                rowdata.extend(self.data[(row, col)].color)
            filedata.append(rowdata)


        writer = png.Writer(self.width, self.height, bitdepth=self.colorbitnum, greyscale=False)
        with open(filename, 'wb') as f:
            writer.write(f, filedata)

    def letterwrite(self, posrow, poscol, text, textcolor='r'):
        textlen = len(text)
        letterboxrows = fonts.sizerow
        letterboxcols = fonts.sizecol * textlen + (fonts.deadspace * (textlen - 1))

        if (letterboxcols % 2) == 0:
            letterboxcols += 1
        minrowcoltip = (posrow - ((letterboxrows - 1) / 2), poscol - ((letterboxcols - 1) / 2))
        centr1stchar = (minrowcoltip[0] + ((letterboxrows - 1) / 2), minrowcoltip[1] + ((fonts.sizecol - 1) / 2))
        letterindex = 0
        for char in list(text.lower()):
            lettercent = (posrow, (centr1stchar[1] + letterindex * (fonts.deadspace + fonts.sizecol))  )
            letterindex += 1
            for pix in fonts.capitalletters[char]:
                pixrow = - pix[0] + lettercent[0]
                pixcol =pix[1] + lettercent[1]
                self.data.update({(pixrow, pixcol): Pixel(colorbitcount=self.colorbitnum, preset=textcolor)})


#test = Pixel(preset='g', colorbitcount=16)
#print(test.color)
test = FilePNG(256, 256, 8, background='r', name='punane')
test.letterwrite(100, 100, "abcdefghij", 'd')
test.filewrite()