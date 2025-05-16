import RenderingFRAME as fr
import time

spct = "HSQCdata/HSQC-250404-EtOH-frHL-SA-ECH.txt"
start = time.time()
test = fr.FilePNG(2200, 2300, 16, background='w', name=spct.split('/')[-1].strip('.txt'))
#test = fr.FilePNG(160, 154, 16, background='w', name='punane')
#test.legacyletterwrite(40, 40, "10", 'd', scale=3)
#test.legacyletterwrite(40-17, 40+40, "3", 'd', scale=2)
# test.pixfill((100,100), (200, 200), color=(0, 255, 0))
# test.pixfill([115, 105], [125, 135])
# test.letterwrite(120, 120, "tere!", 'r')
# test.graph((100,100), (200, 200), -2, 2)
test.gradientgraph(spct,
                   (2, 5),
                   (25, 85),
                   0.25,
                   5,
                   (32000, 32000, 32000),
                   'd',
                   4,
                   (150,200),
                   (2000, 2000),
                   25000,
                   True,
                   (65535, 0, 0),
                   (32000, 65535, 32000),
                   (65535, 65535, 65535),
                   (0, 0, 65535),
                   1000,
                   5,
                   (2230, 1000),
                   (2280, 2000))
#test.gradientgraph(spct, (2, 5),(30, 90),0.25,5,(32000, 32000, 32000),'d',4,(150,200),(2000, 2000),35000,True,(65535, 0, 0),(32000, 65535, 32000),(65535, 65535, 65535),(0, 0, 65535), 500, 5, (2200, 1000), (2250, 2000))
test.legacyletterwrite(50, 1000, spct.split('/')[-1].strip('.txt'), 'd', 6)
test.legacyletterwrite(1770, 90, '13C (ppm)', 'd', 4)
test.legacyletterwrite(2100, 400, '1H (ppm)', 'd', 4)
test.filewrite()
end = time.time()
elapsed = end - start
print(f'\nOperation time total: {elapsed:.2f} seconds')