from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageOps
from HersheyFonts import HersheyFonts
from tkinter import NW, Tk, Canvas
from threading import Thread
import time
import os
import asyncio

UPDATE_NORMAL = 0
UPDATE_MEDIUM = 1
UPDATE_FAST = 2
UPDATE_TURBO = 3
UPDATE_SUPER_EXTRA_TURBO = 3
SYSTEM_VERY_SLOW = 0
SYSTEM_SLOW = 1
SYSTEM_NORMAL = 2
SYSTEM_FAST = 3
SYSTEM_TURBO = 4
WIDTH = 296
HEIGHT = 128
BUTTON_A = 12
BUTTON_B = 13
BUTTON_C = 14
BUTTON_D = 15
BUTTON_E = 11
BUTTON_UP = 15
BUTTON_DOWN = 11
BUTTON_USER = 23
PIN_CS = 17
PIN_CLK = 18
PIN_MOSI = 19
PIN_DC = 20
PIN_RESET = 21
PIN_BUSY = 26
PIN_VBUS_DETECT = 24
PIN_LED = 25
PIN_VREF_POWER = 27
PIN_1V2_REF = 28
PIN_BATTERY = 29
PIN_ENABLE_3V3 = 10

def pressed_to_wake(*a, **k):
    # Since we are mocking the system as running on USB power, we don't need to worry about the button that is pressed to wake it
    pass

def woken_by_button(*a, **k):
    # Not needed when mocking as USB
    pass

def system_speed(*a, **k):
    # Not needed when mocking as USB
    pass

KEYS = {
    "a":BUTTON_A,
    "s":BUTTON_B,
    "d":BUTTON_C,
    "r":BUTTON_UP,
    "f":BUTTON_DOWN,
    "q":BUTTON_USER,
}

class Gui():
    def __init__(self,scale=2):
        self._scale = scale
        self._size = (WIDTH*scale,HEIGHT*scale)
        self._running = False
        self._keys = set()
        
        self._root = Tk()

        for k,v in KEYS.items():
            self.setupKey(k,v)
        
        self._canvas = Canvas(
            self._root,
            width = self._size[0],
            height = self._size[1]
        )
        self._canvas.pack()
        
        self._img = None

    def setupKey(self,key,code):
        self._root.bind(f"<Key-{key}>",lambda _:self._keys.add(code))
        self._root.bind(f"<KeyRelease-{key}>",lambda _:self._keys.discard(code))
    
    def update(self,image):
        if self._scale != 1:
            image = image.resize(self._size,Image.NEAREST)
        self._img = ImageTk.PhotoImage(image,master = self._root)  
        self._canvas.create_image(0, 0, anchor=NW, image=self._img)
        self._root.update()

    def halt(self):
        while not self._keys:
            self._root.update()
            time.sleep(0.1)

class Badger2040:
    def __init__(self):
        self._canvas = Image.new("L", (WIDTH, HEIGHT), 255)
        self._draw = ImageDraw.Draw(self._canvas)
        self._pen = 0
        self._thickness = 1
        self._font = HersheyFonts()
        self._gui = Gui()

    def measure_text(self,text,scale):
        maxX = 0
        for (x1,y1),(x2,y2) in self._font.lines_for_text(text):
            if x1 > maxX:
                maxX = x1
            if x2 > maxX:
                maxX = x2
        return maxX*scale

    def pen(self, color):
        self._pen = (color * 255) // 15

    def thickness(self, thickness):
        self._thickness = thickness

    def clear(self, *a, **k):
        self.rectangle(0, 0, WIDTH, HEIGHT)

    def rectangle(self, x, y, width, height):
        self._draw.rectangle([x, y, x + width, y + height], fill=self._pen)

    def line(self, x1, y1, x2, y2):
        self._draw.line(
            [x1, y1, x2, y2],
            width=self._thickness, fill=self._pen
        )

    def text(self,text,x,y,scale):
        for (x1,y1),(x2,y2) in self._font.lines_for_text(text):
            self.line(x+x1*scale,y+y1*scale,x+x2*scale,y+y2*scale)
    
    def update(self):
        self._gui.update(self._canvas)

    def halt(self):
        self._gui.halt()

    def image(self, imgData, width, height, x, y):
        img = Image.frombytes("1", (width, height), bytes(imgData))
        img = img.convert("L")
        img = ImageOps.invert(img)
        self._canvas.paste(img, (x, y))

    def font(self,font):
        if font == "sans":
            self._font.load_default_font("futural")
        elif font == "gothic":
            self._font.load_default_font("gothgbt")
        elif font == "cursive":
            self._font.load_default_font("scripts")
        elif font == "serif_italic":
            self._font.load_default_font("timesi")
        elif font == "serif":
            self._font.load_default_font("timesr")
        else:
            raise ValueError(f"Invalid font name {font}")

    def pressed(self, key):
        return key in self._gui._keys

    def is_busy(self, *a, **k):
        NotImplemented
        print(">> is_busy", a, k)

    def partial_update(self, *a, **k):
        NotImplemented
        print(">> partial_update", a, k)

    def invert(self, *a, **k):
        NotImplemented
        print(">> invert", a, k)

    def pixel(self, *a, **k):
        NotImplemented
        print(">> pixel", a, k)

    def icon(self, *a, **k):
        NotImplemented
        print(">> icon", a, k)

    def glyph(self, *a, **k):
        NotImplemented
        print(">> glyph", a, k)

    def measure_glyph(self, *a, **k):
        NotImplemented
        print(">> measure_glyph", a, k)

    def command(self, *a, **k):
        NotImplemented
        print(">> command", a, k)

    def update_speed(self, *a, **k):
        # Not needed, not mocking the updating delay
        print("## update_speed", a, k)

    def led(self, *a, **k):
        # Not needed, not visualizing the LED
        print("## led", a, k)