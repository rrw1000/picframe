from picographics import PicoGraphics , DISPLAY_INKY_FRAME_7 as DISPLAY
from jpegdec import JPEG

graphics = PicoGraphics(DISPLAY)
j = JPEG(graphics)
print("Opening file")
j.open_file("1703773289.9373736_0.jpg")
print("Decode")
j.decode()
print("Update screen")
graphics.update()
