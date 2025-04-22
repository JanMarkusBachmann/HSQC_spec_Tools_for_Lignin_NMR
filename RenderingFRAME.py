import math

import time
import png
import font5X7 as fontsx
import font17x11 as newfont



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

        starttime = time.time()

        print(f'Initializing FilePNG object, coloring canvas of {self.width * self.height} pixels')
        stars = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        counter = 0
        counterstep = (self.width * self.height) // len(stars)
        nstars = 0

        for row in range(self.height):
            for col in range(self.width):

                counter += 1
                if counter >= counterstep:
                    counterstep += (self.width * self.height) // len(stars)
                    print(f'Pixel coloring progress: [{''.join(stars)}]')
                    stars[nstars] = '*'
                    nstars += 1

                self.data.update({(row, col): Pixel(preset=background, colorbitcount=self.colorbitnum)})

        endtime = time.time()
        elapsed = endtime - starttime
        print(f'Pixel coloring progress: [{''.join(stars)}]')
        print(f'Pixel coloring progress: done! Elapsed time: {elapsed:.2f} seconds')

    def filewrite(self, newname='-'):
        filename = ''
        if newname != '-':
            filename = f'{newname}.png'
        else:
            filename = f'{self.name}.png'
        starttime = time.time()
        print(f'Writing {filename}')
        filedata = []
        for row in range(self.height):
            rowdata = []
            for col in range(self.width):
                rowdata.extend(self.data[(row, col)].color)
            filedata.append(rowdata)


        writer = png.Writer(self.width, self.height, bitdepth=self.colorbitnum, greyscale=False)
        with open(filename, 'wb') as f:
            writer.write(f, filedata)
        endtime = time.time()
        elapsed = endtime - starttime
        print(f'Writing {filename}, done! Elapsed time: {elapsed:.2f} seconds')
    def textwrite(self, posrow, poscol, text, textcolor='r', scale=1):

        letterboxrows = newfont.sizerow * scale
        letterboxcols = (len(text) * newfont.deadspace - newfont.deadspace) * scale

        for char in list(text.lower()):
            letterboxcols += (1 + newfont.letters[char][1][1] - newfont.letters[char][0][1]) * scale

        if (letterboxcols % 2) == 0:
            letterboxcols += 1
        if (letterboxrows % 2) == 0:
            letterboxrows += 1

        rowepisode = 0

        while rowepisode < scale:
            colepisode = 0
            while colepisode < scale:
                minrowcoltip = (posrow - ((letterboxrows - 1) / 2) + rowepisode,
                                poscol - ((letterboxcols - 1) / 2) + colepisode)
                centr1stchar = (minrowcoltip[0] + ((newfont.minmax[list(text.lower())[0]][1][0] -
                                                    newfont.minmax[list(text.lower())[0]][0][0]) / 2) * scale,
                                minrowcoltip[1] + ((newfont.minmax[list(text.lower())[0]][1][1] -
                                                    newfont.minmax[list(text.lower())[0]][0][1]) / 2) * scale)

                if len(text) == 1:
                    for pix in newfont.letters[char]:
                        pixrow = - pix[0] * scale + centr1stchar[0]
                        pixcol = pix[1] * scale + centr1stchar[1]
                        self.data.update({(pixrow, pixcol): Pixel(colorbitcount=self.colorbitnum, preset=textcolor)})
                    colepisode += 1
                    continue
                index = 0
                for char in list(text.lower()):
                    for pix in newfont.letters[char]:
                        pixrow = - pix[0] * scale + centr1stchar[0]
                        pixcol = pix[1] * scale + centr1stchar[1]
                        self.data.update({(pixrow, pixcol): Pixel(colorbitcount=self.colorbitnum, preset=textcolor)})
                    centr1stchar = (posrow + rowepisode - 1, (centr1stchar[1] + scale * (
                                newfont.deadspace + 1 + newfont.minmax[list(text.lower())[index]][1][1] -
                                newfont.minmax[list(text.lower())[index + 1]][0][1])))
                    if index < len(text) - 2:
                        index += 1
                colepisode += 1
            rowepisode += 1
    def legacyletterwrite(self, posrow, poscol, text, textcolor='r', scale=1):
        letterboxrows = fontsx.sizerow * scale
        letterboxcols = (len(text) * fontsx.deadspace - fontsx.deadspace) * scale


        for char in list(text.lower()):
            letterboxcols += (1 + fontsx.capi_let_minmax[char][1][1]-fontsx.capi_let_minmax[char][0][1]) * scale

        if (letterboxcols % 2) == 0:
            letterboxcols += 1
        if (letterboxrows % 2) == 0:
            letterboxrows += 1

        rowepisode = 0


        while rowepisode < scale:
            colepisode = 0
            while colepisode < scale:
                minrowcoltip = (posrow - ((letterboxrows - 1) / 2) + rowepisode, poscol - ((letterboxcols - 1) / 2) + colepisode)
                centr1stchar = (minrowcoltip[0] + ((fontsx.capi_let_minmax[list(text.lower())[0]][1][0] -
                                                    fontsx.capi_let_minmax[list(text.lower())[0]][0][0]) / 2) * scale,
                                minrowcoltip[1] + ((fontsx.capi_let_minmax[list(text.lower())[0]][1][1] -
                                                    fontsx.capi_let_minmax[list(text.lower())[0]][0][1]) / 2) * scale)

                if len(text) == 1:
                    for pix in fontsx.capitalletters[char]:
                        pixrow = - pix[0] * scale + centr1stchar[0]
                        pixcol = pix[1] * scale + centr1stchar[1]
                        self.data.update({(pixrow, pixcol): Pixel(colorbitcount=self.colorbitnum, preset=textcolor)})
                    colepisode += 1
                    continue
                index = 0
                for char in list(text.lower()):
                    for pix in fontsx.capitalletters[char]:
                        pixrow = - pix[0] * scale + centr1stchar[0]
                        pixcol =pix[1] * scale + centr1stchar[1]
                        self.data.update({(pixrow, pixcol): Pixel(colorbitcount=self.colorbitnum, preset=textcolor)})
                    centr1stchar = (posrow + rowepisode - 1, (centr1stchar[1] + scale * (fontsx.deadspace + 1 + fontsx.capi_let_minmax[list(text.lower())[index]][1][1] - fontsx.capi_let_minmax[list(text.lower())[index + 1]][0][1])))
                    if index < len(text)-2:
                        index += 1
                colepisode += 1
            rowepisode += 1


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

    def gradientgraph (self, importdata, xrange, yrange, xaxismaj, yaxismaj, axiscolor, textcolor, textscale, graph_area_min, graph_area_max, sens, islog, colormin, colornull, colorzero, colormax, ramp, exp, rulerpxmin, rulerpxmax):
        mesh = Ordere3dmesh(importdata)
        mesh.pixelprintout(self, xrange, yrange, graph_area_min, graph_area_max, sens, islog, colormin, colornull, colorzero, colormax, ramp, exp, rulerpxmin, rulerpxmax)
        px2y = (graph_area_max[0] - graph_area_min[0]) / (yrange[1] - yrange[0])
        px2x = (graph_area_max[1] - graph_area_min[1]) / (xrange[1] - xrange[0])

        xRN = xrange[1]
        while xRN >= xrange[0]:
            self.pixfill((graph_area_min[0], round(graph_area_max[1] - (xRN-xrange[0])*px2x)), (graph_area_max[0], round(graph_area_max[1] - (xRN-xrange[0])*px2x)), color=axiscolor)
            self.legacyletterwrite(graph_area_min[0] - 8 * textscale, round(graph_area_max[1] - (xRN - xrange[0]) * px2x), str(round(xRN, 2)), textcolor=textcolor, scale=textscale)
            self.legacyletterwrite(graph_area_max[0] + 8 * textscale, round(graph_area_max[1] - (xRN - xrange[0]) * px2x), str(round(xRN, 2)), textcolor=textcolor, scale=textscale)
            xRN -= xaxismaj

        yRN = yrange[1]
        while yRN >= yrange[0]:
            self.pixfill((round((yRN-yrange[0]) * px2y + graph_area_min[0]), graph_area_min[1]), (round((yRN-yrange[0])*px2y+graph_area_min[0]), graph_area_max[1]), color=axiscolor)
            self.legacyletterwrite(round((yRN - yrange[0]) * px2y + graph_area_min[0]), graph_area_min[1] - 15 * textscale, str(round(yRN, 2)), textcolor=textcolor, scale=textscale)
            self.legacyletterwrite(round((yRN - yrange[0]) * px2y + graph_area_min[0]), graph_area_max[1] + 15 * textscale, str(round(yRN, 2)), textcolor=textcolor, scale=textscale)

            yRN -= yaxismaj




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
        starttime = time.time()
        print(f'Ordere3dmesh: reading file:{datapath}')
        self.loaddata()
        endtime = time.time()
        elapsed = endtime - starttime
        print(f'Ordere3dmesh: reading complete file:{datapath}! Elapsed time: {elapsed:.2f} seconds')

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

    def pixelprintout(self, target, xrange, yrange, graph_area_min, graph_area_max, sens, islog, colormin, colorzero, colornull, colormax, ramp, exponent, rulerpxmin, rulerpxmax):
        #calculate how many pixels one ppm of spectral data would be, since there is a given range in both axies, it might varie betweenm function calls
        starttimeall = time.time()
        print(f'Ordere3dmesh: pixelprintout, started sorting {(graph_area_max[0] - graph_area_min[0])*(graph_area_max[1] - graph_area_min[1])} pixels')

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

        stars = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        f1_2px = (yrange[1] - yrange[0]) / (graph_area_max[0] - graph_area_min[0])
        f2_2px = (xrange[1] - xrange[0]) / (graph_area_max[1] - graph_area_min[1])

        vec_zero2min = (colormin[0] - colorzero[0], colormin[1] - colorzero[1], colormin[2] - colorzero[2]) #RGB
        vec_zero2max = (colormax[0] - colorzero[0], colormax[1] - colorzero[1], colormax[2] - colorzero[2]) #RGB


        counter = 0
        counterstep = ((graph_area_max[0] - graph_area_min[0])*(graph_area_max[1] - graph_area_min[1]))//len(stars)
        nstars = 0
        min = 0.0
        max = 0.0
        syndots = [] # [f1, f2, pxrow, pxcol, float_val]
        rowRN = yrange[0] #f1
        colRN = xrange[0] #f2
        while rowRN <= yrange[1]:
            while colRN <= xrange[1]:
                counter += 1
                if counter >= counterstep:
                    counterstep += ((graph_area_max[0] - graph_area_min[0])*(graph_area_max[1] - graph_area_min[1])) //len(stars)
                    print(f'Pixel filtering progress: [{''.join(stars)}]')
                    stars[nstars] = '*'
                    nstars += 1
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
        starttimemid=time.time()
        elapsed = starttimemid - starttimeall
        print(f'Pixel filtering progress: [{''.join(stars)}]')
        print(f'Pixel filtering progress: done! Elapsed time: {elapsed:.2f} seconds')
        print(f'Filtered out {(graph_area_max[0] - graph_area_min[0])*(graph_area_max[1] - graph_area_min[1]) - len(syndots)} pixels that are under sensitivity of {sens}')

        if islog:
            min = -math.log10(abs(min))
            max = math.log10(abs(max))
            sens = math.log10(abs(sens))
        #calculate pixel color values

        print(f'Ordere3dmesh: pixelprintout, starting color calculations of {len(syndots)} pixels')
        stars = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        counter = 0
        counterstep = len(syndots) // len(stars)
        nstars = 0

        for dot in syndots:

            counter += 1
            if counter >= counterstep:
                counterstep += len(syndots) // len(stars)
                print(f'Pixel color calculation progress: [{''.join(stars)}]')
                stars[nstars] = '*'
                nstars += 1

            val = dot[4]
            neg = False
            if val < 0.0:
                neg = True
                val = -val
            colorRN = colorzero
            if islog and neg:
                val = -math.log10(val)
            elif islog:
                val = math.log10(val)
            if val < 0.0:
                colorRN = (round(colorzero[0] + vec_zero2min[0] * (math.atan(((val + sens)/(min + sens))**exponent * ramp)*2/math.pi)), round(colorzero[1] + vec_zero2min[1] * (math.atan(((val + sens)/(min + sens))**exponent * ramp)*2/math.pi)), round(colorzero[2] + vec_zero2min[2] * (math.atan(((val + sens)/(min + sens))**exponent * ramp)*2/math.pi)))
            elif val > 0.0:
                colorRN = (round(colorzero[0] + vec_zero2max[0] * (math.atan(((val - sens)/(max - sens))**exponent * ramp)*2/math.pi)), round(colorzero[1] + vec_zero2max[1] * (math.atan(((val - sens)/(max - sens))**exponent * ramp)*2/math.pi)), round(colorzero[2] + vec_zero2max[2] * (math.atan(((val - sens)/(max - sens))**exponent * ramp)*2/math.pi)))
            else:
                print(f'baddot> ordered3dmesh > pixelprintout > calculate oixel color: dot {dot}')
            target.data.update({(dot[2], dot[3]): Pixel(colorRN[0], colorRN[1], colorRN[2], target.colorbitnum)})

        endtimeall = time.time()
        elapsed =  endtimeall - starttimemid
        print(f'Pixel color calculation progress: [{''.join(stars)}]')
        print(f'{len(syndots)} Pixel color calculation: done! Elapsed time: {elapsed:.2f} seconds')

        #create a ruler object

        rulerstartpxrow = rulerpxmin[0] + 1
        rulerstartpxcol = rulerpxmin[1] + 1
        rulerendpxrow = rulerpxmax[0] - 1
        rulerendpxcol = rulerpxmax[1] - 1
        pxRNcol = rulerstartpxcol
        signalvalRN = min
        step = (max - min) / (rulerendpxcol - rulerstartpxcol)
        while pxRNcol <= rulerendpxcol:
            colorRN = colornull
            if abs(signalvalRN) > sens:
                if signalvalRN < 0.0:
                    colorRN = (round(colorzero[0] + vec_zero2min[0] * math.atan(((signalvalRN + sens) / (min + sens)) ** exponent * ramp) * 2 / math.pi), round(
                        colorzero[1] + vec_zero2min[1] * math.atan(((signalvalRN + sens) / (min + sens)) ** exponent * ramp) * 2 / math.pi), round(
                        colorzero[2] + vec_zero2min[2] * math.atan(((signalvalRN + sens) / (min + sens)) ** exponent * ramp) * 2 / math.pi))
                elif signalvalRN > 0.0:
                    colorRN = (round(colorzero[0] + vec_zero2max[0] * math.atan(((signalvalRN - sens) / (max - sens)) ** exponent * ramp) * 2 / math.pi), round(
                        colorzero[1] + vec_zero2max[1] * math.atan(((signalvalRN - sens) / (max - sens)) ** exponent * ramp) * 2 / math.pi), round(
                        colorzero[2] + vec_zero2max[2] * math.atan(((signalvalRN - sens) / (max - sens)) ** exponent * ramp) * 2 / math.pi))
            pxRNrow = rulerstartpxrow
            while pxRNrow <= rulerendpxrow:
                target.data.update({(pxRNrow, pxRNcol): Pixel(colorRN[0], colorRN[1], colorRN[2], target.colorbitnum)})
                pxRNrow += 1
            pxRNcol += 1
            signalvalRN += step

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






