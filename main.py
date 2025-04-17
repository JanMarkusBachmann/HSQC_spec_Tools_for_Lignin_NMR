import RenderingFRAME as fr

test = fr.FilePNG(4000, 4000, 16, background='w', name='punane')
#test = fr.FilePNG(105, 22, 16, background='w', name='punane')
#test.letterwrite(10, 52, "punane", 'r', scale=3)
# test.pixfill((100,100), (200, 200), color=(0, 255, 0))
# test.pixfill([115, 105], [125, 135])
# test.letterwrite(120, 120, "tere!", 'r')
# test.graph((100,100), (200, 200), -2, 2)
test.gradientgraph("HSQCdata/HSQC-250404-EtOH-frHL-SA-ECH.txt", (0.5, 9), (5, 140), 0.25, 5, (32000, 32000, 32000), 'r', 4, (100,100), (3900, 3900), 10000, True, (65535, 0, 0),(32000, 65535, 32000), (65535, 65535, 65535),  (0, 0, 65535), 500, 5)
test.filewrite()