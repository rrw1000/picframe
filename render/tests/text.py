from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY
import time
graphics = PicoGraphics(DISPLAY)

WHITE = 1
BLACK = 0

graphics.set_pen(WHITE)
graphics.clear()
graphics.set_pen(BLACK)
graphics.text("Hello, Inky!", 0, 0, 600, 4)
graphics.update()


