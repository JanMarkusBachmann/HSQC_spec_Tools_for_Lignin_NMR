import RenderingFRAMEcontinues as frc

xoffset = 0.025
yoffset = 0.75
xrange = (2.4, 4.4)
yrange = (40, 76)
xaxismaj = 0.2
yaxismaj = 2
sens = 20000
ramp = 500
exp = 5
rulermessage = 'Intensiivsus skaala:'

spct = "HSQCdata/HSQC-250404-EtOH-frHL-FEN-ECH.txt"

mesh = frc.Ordere3dmesh(spct)
pngfile = frc.FilePNG(1000, 1000, 16, background='w', name=spct.split('/')[-1].strip('.txt'))

keyRN = ' '

while keyRN != 'q':
    if keyRN == 'q':
        break
    if keyRN != ' ':
        pngfile.pixfill((0, 0), (1000, 1000), (65535, 65535, 65535))
        pngfile.legacyletterwrite(10, 500, spct.split('/')[-1].strip('.txt'), 'd', 2)
        pngfile.legacyletterwrite(945, 90, '13C (ppm)', 'd', 3)
        pngfile.legacyletterwrite(975, 90, '1H (ppm)', 'd', 3)
        pngfile.gradientgraph(mesh,
                              xoffset,
                              yoffset,
                              xrange,
                              yrange,
                              xaxismaj,
                              yaxismaj,
                              (32000, 32000, 32000),
                           'd',
                              3,
                              (75, 75),
                              (825, 925),
                              sens,
                              True,
                              (65535, 0, 0),
                              (32000, 65535, 32000),
                              (65535, 65535, 65535),
                              (0, 0, 65535),
                              ramp,
                              exp,
                              (950, 200),
                              (990, 970),
                              rulermessage)
        pngfile.filewrite()

    print(f'\n\nDo you want to change anything?\nIf you are satisfied with the result, type: q\n0: xrange = {xrange[0]} -> {xrange[1]}\n1: yrange = {yrange[0]} -> {yrange[1]}\n2: xaxismaj = {xaxismaj}\n3: yaxismaj = {yaxismaj}\n4: sens = {sens}\n5: ramp = {ramp}\n6: exp = {exp}\n7: xoffset = {xoffset}\n8: yoffset = {yoffset}\n')
    keyRN = input()
    while keyRN.isnumeric():
        match keyRN:
            case '0':
                print('Enter new xrange in ppm:\n')
                RN = []
                RN.append(float(input('from:')))
                RN.append(float(input('to:')))
                xrange = tuple(RN)
            case '1':
                print('Enter new yrange in ppm:\n')
                RN = []
                RN.append(float(input('from:')))
                RN.append(float(input('to:')))
                yrange = tuple(RN)
            case '2':
                print('Enter new x axis grid size in ppm:\n')
                xaxismaj = float(input('new value:'))
            case '3':
                print('Enter new y axis grid size in ppm:\n')
                yaxismaj = float(input('new value:'))
            case '4':
                print('Enter new sensitivity value')
                sens = float(input('new value:'))
            case '5':
                print('Enter new ramp function parameter')
                ramp = float(input('new value:'))
            case '6':
                print('Enter new exp function parameter')
                exp = float(input('new value:'))
            case '7':
                print('Enter new xoffset value in ppm')
                xoffset = float(input('new value:'))
            case '8':
                print('Enter new yoffset value in ppm')
                yoffset = float(input('new value:'))
        print(f'\n\nDo you want to change anything?\nIf you are satisfied with the result, type: q\n0: xrange = {xrange[0]} -> {xrange[1]}\n1: yrange = {yrange[0]} -> {yrange[1]}\n2: xaxismaj = {xaxismaj}\n3: yaxismaj = {yaxismaj}\n4: sens = {sens}\n5: ramp = {ramp}\n6: exp = {exp}\n7: xoffset = {xoffset}\n8: yoffset = {yoffset}\n')
        keyRN = input()

#test.gradientgraph(spct, (2, 5),(30, 90),0.25,5,(32000, 32000, 32000),'d',4,(150,200),(2000, 2000),35000,True,(65535, 0, 0),(32000, 65535, 32000),(65535, 65535, 65535),(0, 0, 65535), 500, 5, (2200, 1000), (2250, 2000))




