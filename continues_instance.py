import RenderingFRAMEcontinues as frc

xoffset = 0.0
yoffset = 0.0
xrange = (2, 5)
yrange = (25, 85)
xaxismaj = 0.25
yaxismaj = 5
sens = 20000
ramp = 700
exp = 4
rulermessage = 'Intensiivsus skaala:'

spct = "HSQCdata/HSQC-250404-EtOH-frHL-SA-ECH.txt"

mesh = frc.Ordere3dmesh(spct)
pngfile = frc.FilePNG(2100, 2970, 16, background='w', name=spct.split('/')[-1].strip('.txt'))
pngfile.legacyletterwrite(50, 1000, spct.split('/')[-1].strip('.txt'), 'd', 6)
pngfile.legacyletterwrite(2670, 90, '13C (ppm)', 'd', 4)
pngfile.legacyletterwrite(2600, 400, '1H (ppm)', 'd', 4)

keyRN = ' '

while keyRN != 'q':
    if keyRN == 'q':
        break
    if keyRN != ' ':
        pngfile.gradientgraph(mesh,
                              xoffset,
                              yoffset,
                              xrange,
                              yrange,
                              xaxismaj,
                              yaxismaj,
                              (32000, 32000, 32000),
                           'd',
                              4,
                              (150, 150),
                              (2500, 1950),
                              sens,
                              True,
                              (65535, 0, 0),
                              (32000, 65535, 32000),
                              (65535, 65535, 65535),
                              (0, 0, 65535),
                              ramp,
                              exp,
                              (2830, 1000),
                              (2880, 2000),
                              rulermessage)
        pngfile.filewrite()

    print(f'\n\nDo you want to change anything?\nIf you are satisfied with the result, type: q\n0: xrange = {xrange[0]} -> {xrange[1]}\n1: yrange = {yrange[0]} -> {yrange[1]}\n2: xaxismaj = {xaxismaj}\n3: yaxismaj = {yaxismaj}\n4: sens = {sens}\nramp = {ramp}\n5: exp = {exp}\n6: xoffset = {xoffset}\n7: yoffset = {yoffset}\n')
    keyRN = input()



#test.gradientgraph(spct, (2, 5),(30, 90),0.25,5,(32000, 32000, 32000),'d',4,(150,200),(2000, 2000),35000,True,(65535, 0, 0),(32000, 65535, 32000),(65535, 65535, 65535),(0, 0, 65535), 500, 5, (2200, 1000), (2250, 2000))




