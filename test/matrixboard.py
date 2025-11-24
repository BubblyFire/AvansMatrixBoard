import time
import board
import neopixel
import bitmapfont

class MatrixBoard:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def init(self):
        self._pixels = neopixel.NeoPixel(board.D18, self._width * self._height, auto_write=False, brightness=1)
        self.clear()
        self.show()

        self._bf = bitmapfont.BitmapFont(self._width, self._height, self._draw_pixel)
        self._bf.init()

    def _draw_pixel(self, x, y, color):
        try:
            index = self._coord_to_index(x, y)
        except Exception as e:
            pass
        else:
            self._pixels[index] = color

    def _coord_to_index(self, x, y):
        if x < 0 or x >= self._width:
            raise Exception("Invalid X index")
        if y < 0 or y >= self._height:
            raise Exception("Invalid Y index") 
        if y % 2 == 0:
            return (x) + (self._height - 1 - y) * self._width
        return ((self._height - 1 - y) + 1) * self._width - (x) - 1

    def scroll_text(self, text, color):
        text_width = self._bf.width(text)

        new_text = text + text

        for i in range(text_width):
            self.clear()
            self.render_text(-i, 0, new_text, color)
            self.show()
            time.sleep(0.1)

    def render_text(self, x, row, text, color):
        self._bf.text(x, row * (self._bf._font_height + 1) + 2, text, color)

    def clear(self):
        self._pixels.fill((0, 0, 0))

    def show(self):
        self._pixels.show()
