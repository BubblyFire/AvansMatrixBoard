import time
import board
import neopixel
from .bitmapfont import *

class MatrixBoard:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def init(self):
        self._pixels = neopixel.NeoPixel(board.D18, self._width * self._height, auto_write=False, brightness=0.3)
        self.clear()
        self.show()

        self._bf = BitmapFont(self._width, self._height, self._draw_pixel)
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
        print(f"Printing line {row}")
        self._bf.text(x, row * self._bf._font_height + 3, text, color)

    def clear_line(self, row):
        print(f"Clearing line {row}")
        base_y = row * self._bf._font_height + 3
        for x in range(self._width):
            for y in range(self._bf._font_height):
                self._draw_pixel(x, y + base_y, (0, 0, 0))

    def clear(self):
        self._pixels.fill((0, 0, 0))

    def show(self):
        self._pixels.show()
