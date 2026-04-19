from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C

#define pins
pwm_pin = Pin(0, Pin.OUT)
button_pin = Pin(0, Pin.In)
direction_pin = Pin(0, Pin.In)
step_pin = Pin(0, Pin.In)

#define objects
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000) #freq: clock speed
oled = SSD1306_I2C(128, 64, i2c) #change to match my display
pwm = PWM(pwm_pin, freq=50, duty_u16=32768)  # create a PWM object on pwm_pin, frequency 50Hz, 50% duty (percentage on)

#more definitions :D
NOTES = {
    "A4":67
}
TONE = "tone"
SENSE = "sense"
mode = TONE

def is_playing():
    return False

def button_status():
    return False

def encoder_status():
    if True:
        return "right"
    else:
        return "left"


while True: #main loop
    if mode == "TONE":
        pass

    if button_status():
        tone = not tone