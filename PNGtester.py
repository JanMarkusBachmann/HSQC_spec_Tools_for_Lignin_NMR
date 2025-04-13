import png

def create_gradient(width, height):
    image = []
    for y in range(height):
        row = []
        for x in range(width):
            # Create RGB gradient
            row.extend([
                255,    # Red
                255,   # Green
                255    # Blue
            ])
        image.append(row)
    return image

# Create and save gradient
width, height = 256, 256
gradient = create_gradient(width, height)
gradient[128][129]=0
gradient[128][130]=0
gradient[128][131]=0
writer = png.Writer(width, height, bitdepth=8, greyscale=False)
with open('gradient.png', 'wb') as f:
    writer.write(f, gradient)