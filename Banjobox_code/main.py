from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000) #freq: clock speed
oled = SSD1306_I2C(128, 64, i2c) #change to match my display
