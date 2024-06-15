import time
from rpi_ws281x import PixelStrip, Color, ws

def hsv2rgb(h, s, v):
    i = int(h*6)
    f = h*6 - i
    p = v * (1 - s)
    q = v * (1 - f*s)
    t = v * (1 - (1-f)*s)
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    if i == 1:
        r, g, b = q, v, p
    if i == 2:
        r, g, b = p, v, t
    if i == 3:
        r, g, b = p, q, v
    if i == 4:
        r, g, b = t, p, v
    if i == 5:
        r, g, b = v, p, q
    return int(r*255), int(g*255), int(b*255)

class Led():
    def __init__(self):
        self.LED_COUNT = 32     # LEDの数
        LED_PIN = 10            # SPI0 MOSI (GPIO10)
        LED_FREQ_HZ = 800000    # LED信号の周波数（800kHz）
        LED_DMA = 10            # DMAチャネルを使う
        LED_BRIGHTNESS = 64     # LEDの明るさ（0-255）
        LED_INVERT = False      # 信号を反転させるかどうか
        LED_CHANNEL = 0
        self.strip = PixelStrip(self.LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, strip_type=ws.WS2811_STRIP_GRB)
        self.strip.begin()

    def colorWipe(self, color, wait_ms=100):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        time.sleep(wait_ms / 1000.0)

    def turn_off(self):
        self.colorWipe(Color(0, 0, 0))

    def rainbow(self, dir=0, phase_shift=0, saturation=1.0, value=0.2):
        for i in range(0, self.LED_COUNT):
            hue = (i+dir*phase_shift) % self.LED_COUNT / self.LED_COUNT
            r, g, b = hsv2rgb(hue, saturation, value)
            self.strip.setPixelColor(i, Color(r, g, b))
        self.strip.show()
        time.sleep(10 / 1000.0)        


def main():
    led = Led()
    start_time = time.time()
    rotation_time = 2.0
    try:
        while True:
            elapsed_time = time.time() - start_time
            phase_shift = (elapsed_time / rotation_time) * led.LED_COUNT % led.LED_COUNT
            led.rainbow(dir=-1, phase_shift=phase_shift)

    except KeyboardInterrupt:
        led.turn_off()  # 終了時にLEDをオフにする

if __name__ == "__main__":
    main()
