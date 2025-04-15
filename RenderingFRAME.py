import math

import png
import font5X7 as fonts



class Pixel:
    presetdict = dict({
        'r': [1, 0, 0],
        'g': [0, 1, 0],
        'b': [0, 0, 1],
        'w': [1, 1, 1],
        'd': [0, 0, 0]}) #red, greed, blue, white, black

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
        letterboxrows = fonts.sizerow
        letterboxcols = len(text) * fonts.deadspace - fonts.deadspace


        for char in list(text.lower()):
            letterboxcols += 1 + fonts.capi_let_minmax[char][1][1]-fonts.capi_let_minmax[char][0][1]

        if (letterboxcols % 2) == 0:
            letterboxcols += 1
        minrowcoltip = (posrow - ((letterboxrows - 1) / 2), poscol - ((letterboxcols - 1) / 2))
        centr1stchar = (minrowcoltip[0] + ((fonts.capi_let_minmax[list(text.lower())[0]][1][0]-fonts.capi_let_minmax[list(text.lower())[0]][0][0]) / 2), minrowcoltip[1] + ((fonts.capi_let_minmax[list(text.lower())[0]][1][1]-fonts.capi_let_minmax[list(text.lower())[0]][0][1]) / 2))

        if len(text) == 1:
            for pix in fonts.capitalletters[char]:
                pixrow = - pix[0] + centr1stchar[0]
                pixcol = pix[1] + centr1stchar[1]
                self.data.update({(pixrow, pixcol): Pixel(colorbitcount=self.colorbitnum, preset=textcolor)})
            return 0
        index = 0
        for char in list(text.lower()):
            for pix in fonts.capitalletters[char]:
                pixrow = - pix[0] + centr1stchar[0]
                pixcol =pix[1] + centr1stchar[1]
                self.data.update({(pixrow, pixcol): Pixel(colorbitcount=self.colorbitnum, preset=textcolor)})
            centr1stchar = (posrow, (centr1stchar[1] + (fonts.deadspace + 1 + fonts.capi_let_minmax[list(text.lower())[index]][1][1] - fonts.capi_let_minmax[list(text.lower())[index + 1]][0][1])))
            if index < len(text)-2:
                index += 1

    def pixfill(self, from_pos, to_pos, color=(0, 0, 0)):
        colorRN = list(color)
        op_from = [0, 0]
        op_to = [0, 0]
        row = 0
        col = 0
        if from_pos[0] > to_pos[0]:
            op_from[0] = to_pos[0]
            op_to[0] = from_pos[0]
        else:
            op_from[0] = from_pos[0]
            op_to[0] = to_pos[0]
        if from_pos[1] > to_pos[1]:
            op_from[1] = to_pos[1]
            op_to[1] = from_pos[1]
        else:
            op_from[1] = from_pos[1]
            op_to[1] = to_pos[1]

        row = op_from[0]
        col = op_from[1]

        while row <= op_to[0]:
            while (col <= op_to[1]):
                self.data.update({(row, col): Pixel(colorbitcount=self.colorbitnum, red=colorRN[0], green=colorRN[1], blue=colorRN[2])})
                col += 1
            col = op_from[1]
            row += 1

    def graph(self, graph_area_min, graph_area_max, xmin, xmax, colorc=(0, 0, 0)): #func(): [Pixel], y_minmax, x_minmax
        g = Functionplot(graph_area_min, graph_area_max, xmin, xmax, self.colorbitnum, color=colorc)
        self.data.update(g.functionpixeldata)
        yrange = g.yrange
        if yrange[0] <= 0 <= yrange[1]:
            self.pixfill(((graph_area_min[0]+round(yrange[1]*g.px2[0])),graph_area_min[1]),((graph_area_min[0]+round(yrange[1]*g.px2[0])),graph_area_max[1]), color=(0, 0, 255))
        elif yrange[0] > 0:
            self.pixfill(((graph_area_min[0]), graph_area_min[1]), ((graph_area_min[0]), graph_area_max[1]), color=(0, 0, 255))
        elif yrange[1] < 0:
            self.pixfill(((graph_area_min[0]), graph_area_max[1]), ((graph_area_max[0]), graph_area_max[1]), color=(0, 0, 255))

        if xmin <= 0 <= xmax:
            self.pixfill((graph_area_min[0], graph_area_min[1]+round((0 - xmin)*g.px2[1])),((graph_area_max[0],graph_area_min[1]+round((0 - xmin)*g.px2[1]))), color=(0, 0, 255))
        elif xmin > 0:
            self.pixfill(((graph_area_max[0]), graph_area_min[1]), ((graph_area_max[0]), graph_area_max[1]), color=(0, 0, 255))
        elif xmax < 0:
            self.pixfill(((graph_area_min[0]), graph_area_min[1]), ((graph_area_min[0]), graph_area_max[1]), color=(0, 0, 255))

    def gradientgraph (self, importdata, xrange, yrange, graph_area_min, graph_area_max, sens, islog=False, colormin=(1, 0, 0), colornull=(1, 1, 1), colorzero=(0, 0, 0), colormax=(0, 0, 1)):
        mesh = Ordere3dmesh(importdata)
        mesh.pixelprintout(self, xrange, yrange, graph_area_min, graph_area_max, sens, islog, colormin, colornull, colorzero, colormax)




class Functionplot: #parent class, will plot f(x) = ax + b
    def __init__(self, graph_area_min, graph_area_max, xmin, xmax, colorbit, color=(0, 0, 0)):
        self.graph_area_minpoint = graph_area_min
        self.graph_area_range = (graph_area_max[0]-graph_area_min[0], graph_area_max[1]-graph_area_min[1]) #graph range in px
        if (graph_area_max[0] < graph_area_min[0]) or (graph_area_max[1] < graph_area_min[1]): # check if min max are in right order
            print(f'while making a graph some parsed coordinates are mixed up!: from {graph_area_min} to {graph_area_max}')
        self.xmin = xmin
        self.xmax = xmax
        self.xrange = xmax - xmin
        self.yrange = (0, 0)
        self.px2 = (0,0)
        self.color = list(color)
        self.colorbit = colorbit
        self.functionpixeldata = dict({})  # (row, col): Pixel
        self.functionplotting()

    def functionplotting(self, a=1, b=0):
        xdependantdata = [] # [f(x), f(x+step), x]
        stepx = self.xrange / self.graph_area_range[1]
        xpos = self.xmin
        ymin = (a*xpos+b)
        ymax = (a*xpos+b)
        while xpos < self.xmax: #calculate min and max value for every x pixel
            xdependantdata.append([(a*xpos+b), (a*(xpos+stepx)+b), xpos])
            xpos += stepx
            if (a*xpos+b) < ymin:
                ymin = a*xpos+b
            if (a*xpos+b) > ymax:
                ymax = a*xpos+b
            if (xpos+stepx) < ymin:
                ymin = xpos+stepx
            if (xpos+stepx) > ymin:
                ymax = xpos+stepx
        px2y = self.graph_area_range[0] / (ymax - ymin)
        px2x = self.graph_area_range[1] / self.xrange
        for dot in xdependantdata:
            pxposition_y = self.graph_area_minpoint[0] + (((ymax-dot[0])*px2y)//1) #calculate the starting y pixel of given x pixle position
            pxposition_deltay = self.graph_area_minpoint[0] + (((ymax-dot[1])*px2y)//1)
            pxposition_x =  self.graph_area_minpoint[1] + (((dot[2]-self.xmin)*px2x)//1) #calculate the given x pixel position

            if (pxposition_y == pxposition_deltay):
                self.functionpixeldata.update({(pxposition_y + 1, pxposition_x): Pixel(red=self.color[0], green=self.color[1], blue=self.color[2], colorbitcount=self.colorbit)})
            else:
                if round(pxposition_y) > round(pxposition_deltay):
                    ypixels = range(round(pxposition_deltay), round(pxposition_y), 1)
                else:
                    ypixels = range(round(pxposition_y), round(pxposition_deltay), 1)
                for ypixel in ypixels:
                    self.functionpixeldata.update({(ypixel + 1, pxposition_x): Pixel(red=self.color[0],
                                                                                 green=self.color[1],
                                                                                 blue=self.color[2],
                                                                                 colorbitcount=self.colorbit)})
        self.yrange=(ymin, ymax)
        self.px2 = (px2y, px2x)

class Ordere3dmesh:
    def __init__(self, datapath):
        self.datapath = datapath
        self.data = dict() #(f1, f2): val_float))
        self.nrows = 0
        self.ncols = 0
        self.f1SW = 0.0
        self.f2SW = 0.0
        self.f1left = 0.0
        self.f1right = 0.0
        self.f2left = 0.0
        self.f2right = 0.0
        self.stepperrow = 0.0
        self.steppercol = 0.0

        self.loaddata()

    def loaddata(self):
        rowRN = 0
        colRN = 0

        with open(self.datapath, 'r') as f:
            for line in f:
                if line[0] == '#' or line[0] == '\n':
                    if line[0:5] == '# row':
                        rowRN = int(line.strip('\n').split(' ')[3])
                        colRN = self.ncols - 1
                    elif line[0:8] == '# F1LEFT':
                        self.f1SW = float(line.split(' ')[3]) - float(line.split(' ')[7])
                        self.f1left = float(line.split(' ')[3])
                        self.f1right = float(line.split(' ')[7])
                    elif line[0:8] == '# F2LEFT':
                        self.f2SW = float(line.split(' ')[3]) - float(line.split(' ')[7])
                        self.f2left = float(line.split(' ')[3])
                        self.f2right = float(line.split(' ')[7])
                    elif line[0:7] == '# NROWS':
                        self.nrows = int(line.split(' ')[3])
                        self.stepperrow = self.f1SW / self.nrows
                    elif line[0:7] == '# NCOLS':
                        self.ncols = int(line.split(' ')[3])
                        self.steppercol = self.f2SW / self.ncols

                else:
                    line = line.strip('\n')
                    self.data.update({(self.nrows - rowRN, colRN): float(line.strip('\n'))})
                    colRN -= 1

        f.close()

    def pixelprintout(self, target, xrange, yrange, graph_area_min, graph_area_max, sens, islog, colormin, colorzero, colornull, colormax):
        #calculate how many pixels one ppm of spectral data would be, since there is a given range in both axies, it might varie betweenm function calls

        f1_2px = (yrange[1] - yrange[0]) / (graph_area_max[1] - graph_area_min[1])
        f2_2px = (xrange[1] - xrange[0]) / (graph_area_max[0] - graph_area_min[0])

        # calulate the color gradient values that are used to represent spectral data with colors
        # colormin represent minimum value(negative) or furthest negative value from zero that spectra can have
        # colormax represent maximum value(negative) or furthest negative value from zero that spectra can have
        # colorzero is the color value that pixel will approach while its value gets near to zero
        # colornull is the color of a pixel that has no data or has value that is under sens

        # colorvectors are calculated to later be multiplied by scalar value, this allows to easily calulate given pixel color value
        # calculate needed matrix of pixel in given spectra
        # startrow = yrange[0] #pxval f1
        # endrow = yrange[1] #pxval f1
        # startcol = xrange[0] # pxval f2
        # endcol = xrange[1] self.steppercol #pxval f2

        vec_zero2min = (colormin[0] - colorzero[0], colormin[1] - colorzero[1], colormin[2] - colorzero[2]) #RGB
        vec_zero2max = (colormax[0] - colorzero[0], colormax[1] - colorzero[1], colormax[2] - colorzero[2]) #RGB

        min = 0.0
        max = 0.0
        syndots = [] # [f1, f2, pxrow, pxcol, float_val]
        rowRN = yrange[0] #f1
        colRN = xrange[0] #f2
        while rowRN <= yrange[1]:
            while colRN <= xrange[1]:
                val = self.fatneighbours(rowRN, colRN)
                if (abs(val) >= sens):
                    syndots.append([rowRN, colRN, round(graph_area_min[0] + (rowRN - yrange[0])/f1_2px), round(graph_area_max[1] - (colRN - xrange[0])/f2_2px), val])
                    if max < val:
                        max = val
                    elif min > val:
                        min = val
                else:
                    target.data.update({(round(graph_area_min[0] + (rowRN - yrange[0])/f1_2px), round(graph_area_max[1] - (colRN - xrange[0])/f2_2px)): Pixel(colornull[0], colornull[1], colornull[2], target.colorbitnum)})
                colRN += f2_2px
            colRN = xrange[0]
            rowRN += f1_2px

        if islog:
            min = -math.log(abs(min))
            max = math.log(abs(max))
        #calculate pixel color values
        for dot in syndots:
            val = dot[4]
            neg = False
            if val < 0.0:
                neg = True
                val = -val
            colorRN = colorzero
            if islog and neg:
                val = -math.log10(val)
            else:
                val = math.log10(val)
            if val < 0.0:
                colorRN = (round(colorzero[0] + vec_zero2min[0] * (val/min)), round(colorzero[1] + vec_zero2min[1] * (val/min)), round(colorzero[2] + vec_zero2min[2] * (val/min)))
            elif val > 0.0:
                colorRN = (round(colorzero[0] + vec_zero2max[0] * (val/max)), round(colorzero[1] + vec_zero2max[1] * (val/max)), round(colorzero[2] + vec_zero2max[2] * (val/max)))
            else:
                print(f'baddot> ordered3dmesh > pixelprintout > calculate oixel color: dot {dot}')
            target.data.update({(dot[2], dot[3]): Pixel(colorRN[0], colorRN[1], colorRN[2], target.colorbitnum)})

    def fatneighbours(self, f1, f2):
        # calculate the value of artificial point in position (f1, f2) depending on their neighbours weighted average

        rowRN = round(f1//self.stepperrow)
        colRN = round(f2//self.steppercol)
        weight = 0
        val_weight = 0

        distanse = math.sqrt((rowRN*self.stepperrow - f1)**2 + ((colRN*self.steppercol - f2)**2))
        if distanse == 0.0:
            return self.data[(rowRN, colRN)]
        else:
            weight += 1/(distanse**2)
            val_weight += (self.data[(rowRN, colRN)] / (distanse**2))

        rowRN = f1 // self.stepperrow + 1
        colRN = f2 // self.steppercol

        distanse = math.sqrt((rowRN * self.stepperrow - f1) ** 2 + ((colRN * self.steppercol - f2) ** 2))
        if distanse == 0.0:
            return self.data[(rowRN, colRN)]
        else:
            weight += 1 / (distanse ** 2)
            val_weight += self.data[(rowRN, colRN)] / (distanse ** 2)

        rowRN = f1 // self.stepperrow
        colRN = f2 // self.steppercol + 1

        distanse = math.sqrt((rowRN * self.stepperrow - f1) ** 2 + ((colRN * self.steppercol - f2) ** 2))
        if distanse == 0.0:
            return self.data[(rowRN, colRN)]
        else:
            weight += 1 / (distanse ** 2)
            val_weight += self.data[(rowRN, colRN)] / (distanse ** 2)

        rowRN = f1 // self.stepperrow + 1
        colRN = f2 // self.steppercol + 1

        distanse = math.sqrt((rowRN * self.stepperrow - f1) ** 2 + ((colRN * self.steppercol - f2) ** 2))
        if distanse == 0.0:
            return self.data[(rowRN, colRN)]
        else:
            weight += 1 / (distanse ** 2)
            val_weight += self.data[(rowRN, colRN)] / (distanse ** 2)

        return val_weight/weight



#test = Pixel(preset='g', colorbitcount=16)
#print(test.color)
test = FilePNG(1000, 1000, 16, background='w', name='punane')
# test.pixfill((100,100), (200, 200), color=(0, 255, 0))
# test.pixfill([115, 105], [125, 135])
# test.letterwrite(120, 120, "tere!", 'r')
# test.graph((100,100), (200, 200), -2, 2)
test.gradientgraph("HSQCdata/HSQC-250404-EtOH-frHL-SA-ECH.txt", (2, 6), (20, 80), (5,5), (995, 995), 10000, True, (65535, 0, 0),(32000, 32000, 32000), (0, 0, 0),  (0, 0, 65535))
test.filewrite()
