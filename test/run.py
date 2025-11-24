import time
import board
import neopixel
import bitmapfont

BOARD_WIDTH = 30
BOARD_HEIGHT = 30
BOARD_PIXELS = BOARD_WIDTH * BOARD_HEIGHT

COLOR_WHITE = (255, 255, 255)
COLOR_OFF = (255, 255, 255)

# pixels = neopixel.NeoPixel(board.D18, BOARD_PIXELS, auto_write=False)
# pixels.fill((0, 0, 0))
# pixels.show()

def coord_to_index(x, y):
    if x < 0 or x >= BOARD_WIDTH:
        raise Exception("Invalid X index")
    if y < 0 or y >= BOARD_HEIGHT:
        raise Exception("Invalid Y index") 
    if y % 2 == 0:
        return (x) + (BOARD_HEIGHT - 1 - y) * BOARD_WIDTH
    return ((BOARD_HEIGHT - 1 - y) + 1) * BOARD_WIDTH - (x) - 1

def matrix_pixel(x, y, color):
    try:
        index = coord_to_index(x, y)
    except Exception:
        pass
    else:
        pixels[index] = color

# while True:
#     pixels.fill((0, 255, 0))
#     print('working...')
# pixels.fill((0, 0, 0))

bf = bitmapfont.BitmapFont(BOARD_WIDTH, BOARD_HEIGHT, matrix_pixel)
bf.init()

def scroll_text(text):
    text_width = bf.width(text)

    new_text = text + text

    for i in range(text_width):
        pixels.fill((0, 0, 0))
        bf.text(-i, 0, new_text, (255, 0, 255))
        pixels.show()
        time.sleep(0.1)

# scroll_text("hello world ")
# scroll_text("hello world ")
# scroll_text("hello world ")

render_text()

# matrix_pixel(0, 0, (255, 255, 255))
# matrix_pixel(0, 1, (255, 255, 255))
# matrix_pixel(0, 2, (255, 255, 255))

# for i in range(30):
#     pixels[coord_to_index(i, 30)] = COLOR_WHITE
#     time.sleep(0.1)
#     print(i)
# pixels[coord_to_index(0, 0)] = COLOR_WHITE
# pixels[coord_to_index(0, 1)] = COLOR_WHITE
