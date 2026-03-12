# Controls the 30x30 NeoPixel LED matrix.
# Handles pixel drawing, text rendering and the serpentine wiring layout.

import time
import board
import neopixel
from .bitmapfont import BitmapFont
from .config import load_matrix_config

class MatrixBoard:
    def __init__(self, width, height):
        """Store board dimensions and load hardware settings from config."""
        self._width = width
        self._height = height

        self._config = load_matrix_config()
        self._scroll_delay = self._config.get("scroll_delay", 0.1)
        self._font_offset = self._config.get("font_baseline_offset", 3)

    def init(self):
        pin_name = self._config.get("pin", "D18")
        pin = getattr(board, pin_name)

        brightness = float(self._config.get("brightness", 0.3))
        auto_write = bool(self._config.get("auto_write", False))

        # Create the NeoPixel strip for the full grid (width * height LEDs)
        self._pixels = neopixel.NeoPixel(pin, self._width * self._height, auto_write=auto_write, brightness=brightness)
        self.clear()
        self.show()

        # Initialise the bitmap font used for text rendering and scrolling
        self._bf = BitmapFont(self._width, self._height, self._draw_pixel)
        self._bf.init()

    def _draw_pixel(self, x, y, color):
        """Set a single pixel at (x, y) to color (r, g, b). Out-of-bounds coords are silently ignored."""
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return
        index = self._coord_to_index(x, y)
        self._pixels[index] = color

    def _coord_to_index(self, x, y):
        # The LED strip is wired in a serpentine pattern:
        # even rows run left to right, odd rows run right to left.
        # Row 0 is at the bottom, so rows are counted from the bottom up.
        if y % 2 == 0:
            return x + (self._height - 1 - y) * self._width
        return (self._height - y) * self._width - x - 1

    def scroll_text(self, text, color):
        """
        Scroll text across the full width of the display.

        The text is duplicated so the loop is seamless — as the first copy
        exits the left edge, the second copy enters from the right.
        Speed is controlled by scroll_delay in config.json.
        """
        text_width = self._bf.width(text)

        # Duplicate the text so the scroll loops seamlessly:
        # as the first copy scrolls off the left, the second copy fills in from the right
        new_text = text + text

        for i in range(text_width):
            self.clear()
            self.render_text(-i, 0, new_text, color)
            self.show()
            time.sleep(self._scroll_delay)

    def render_text(self, x, row, text, color):
        """Render text at pixel column x on the given row (0-indexed font row, not pixel row)."""
        self._bf.text(x, row * self._bf._font_height + self._font_offset, text, color)

    def clear_line(self, row):
        """Erase all pixels in the given font row by filling them with black."""
        base_y = row * self._bf._font_height + self._font_offset
        for x in range(self._width):
            for y in range(self._bf._font_height):
                self._draw_pixel(x, y + base_y, (0, 0, 0))

    def clear(self):
        """Turn off all LEDs (fill the entire strip with black)."""
        self._pixels.fill((0, 0, 0))

    def show(self):
        """Push the current pixel buffer to the physical LEDs."""
        self._pixels.show()
