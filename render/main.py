"""
This is a fairly simple slideshow app, largely cribbed from the xkcd example
https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/inky_frame/inky_frame_xkcd_daily.py
"""

import gc
import uos
import machine
import jpegdec
import uasyncio
import sdcard
import secrets
import time
import json
import inky_frame
from urllib import urequest
from network_manager import NetworkManager
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY

gc.collect()

# All bright and fresh
STATE = { }

def net_report(mode, status, ip):
    print(f"NET: {mode} {status} {ip}")

for led in [ inky_frame.button_a, inky_frame.button_b, inky_frame.button_c,
             inky_frame.button_d, inky_frame.button_e ]:
    led.led_off()


sd_spi = machine.SPI(0, sck=machine.Pin(18, machine.Pin.OUT), mosi=machine.Pin(19, machine.Pin.OUT), miso=machine.Pin(16, machine.Pin.OUT))
sd = sdcard.SDCard(sd_spi, machine.Pin(22))
uos.mount(sd, "/sd")
gc.collect()

def load_state():
    global STATE
    data = json.loads(open('/state.json', 'r').read())
    if type(data) is dict:
        STATE = data

def save_state():
    with open('/state.json', 'w') as f:
        f.write(json.dumps(STATE))
        f.flush()


inky_frame.button_a.led_on()
load_state()
if inky_frame.woken_by_rtc():
    print("RTC wakeup")
if inky_frame.woken_by_button():
    print("Button wakeup")
inky_frame.button_b.led_on()
done = False
# TODO: add a timeout..
while not done:
    try:
        netman = NetworkManager("GB", status_handler = net_report, client_timeout=10)
        if netman.isconnected():
            print("Disconnecting")
            netman.disconnect()
        uasyncio.get_event_loop().run_until_complete(netman.client(secrets.WIFI_SSID, secrets.WIFI_PASSWORD))
        done= True
    except Exception as e:
        print(f"> {e}")
        inky_frame.button_b.led_toggle()
        time.sleep(1.0)
    gc.collect()

inky_frame.button_c.led_on()
graphics = PicoGraphics(DISPLAY)
GET_ENDPOINT=f"http://{secrets.SERVER_NAME}:14582/current_image.jpg"
FILENAME = "/current.jpg"

done = False
print("Downloading .. ")
while not done:
    try:
        print(f"Downloading from {GET_ENDPOINT} ")
        img_socket = urequest.urlopen(GET_ENDPOINT)
        print("Entering loop")
        data = bytearray(1024)
        with open(FILENAME, "wb") as f:
            while True:
                print("X")
                if img_socket.readinto(data) == 0:
                    break
                f.write(data)
        img_socket.close()
        done = True
    except Exception as e:
        print(f"> {e}")
        inky_frame.button_c.led_toggle()
        time.sleep(2.0)
    gc.collect()
inky_frame.button_d.led_on()
print("Decoding .. ")
jpg = jpegdec.JPEG(graphics)
gc.collect()
jpg.open_file(FILENAME)
jpg.decode()
print("Display")
inky_frame.button_e.led_on()
graphics.update()

inky_frame.button_a.led_off()
network_manager.disconnect()
print("Save state")
save_state()

inky_frame.button_b.led_off()

print("Sleep")
inky_frame.sleep_for(60)
