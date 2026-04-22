"""
TODO:

"""

from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import time, sht31

#define pins
#do not use pull up/down if irl one already in place
BUTTON_PIN = Pin(2, Pin.IN)
DIRECTION_PIN = Pin(9, Pin.IN)
STEP_PIN = Pin(1, Pin.IN)
PWM_PIN = Pin(0)

#instantiate objects
i2c = I2C(1, scl=Pin(5), sda=Pin(4), freq=200000) #freq: clock speed
oled = SSD1306_I2C(128, 32, i2c)
pwm = PWM(PWM_PIN, freq=440, duty_u16=0)
sensor = sht31.SHT31(i2c)

#more definitions :D
MODES = ["TONE", "SENSE"]
NOTES = [
    ["G4", 392.00],
    ["D3", 146.83],
    ["G3", 196.00],
    ["B3", 246.94],
    ["D4", 293.66]
]

time_last_reading = 0
time_last_pressed = 0
now = time.ticks_ms()
READ_INTERVAL = 1000
DEBOUNCE_TIME = 20

current_note = 0
previous_note = current_note
num_notes = len(NOTES)

current_mode = 0
previous_mode = -1
num_modes = len(MODES)

previous_value = True
button_down = False

while True: #main loop
    now = time.ticks_ms()

    #clear display
    oled.fill(0)

    if current_mode == 0:
        if current_mode != previous_mode: #check if mode has just been changed
            pwm.duty_u16(32768)
            previous_mode = current_mode

        if previous_note != current_note: #check if note has just been changed
            #start playing tone
            pwm.freq(int(NOTES[current_note][1]))
            pwm.duty_u16(32768)
            previous_note = current_note

        # rotary encoder logic: check if note needs to be changed
        step = STEP_PIN.value()
        direction = DIRECTION_PIN.value()
        if previous_value != step:  # if STEP_PIN has changed
            if not step:
                if not direction:
                    print("turned left")
                    current_note -= 1 #previous note
                else:
                    print("turned right")
                    current_note += 1  #next note
                current_note %= num_notes
            previous_value = step

        oled.text("Tone", 0, 0)
        oled.text(NOTES[current_note][0], 0, 10)

    elif current_mode == 1:

        if current_mode != previous_mode:  # check if mode has just been changed
            pwm.duty_u16(0) #stop playing tone
            previous_mode = current_mode

        if time.ticks_diff(now, time_last_reading) > READ_INTERVAL:
            temp, humidity = sensor.get_temp_humi()
            print(f"Temperature: {temp}°C Humidity: {humidity}%")
            time_last_pressed = now

        oled.text("Sense", 0, 0)
        oled.text(f"{temp}°C {humidity}%", 0, 10)

    #check if button pressed to change mode
    #button logic: True for not pressed, False for pressed
    if not BUTTON_PIN.value() and not button_down: #ie if pressed and not pressed before
        if time.ticks_diff(now, time_last_pressed) > DEBOUNCE_TIME:
            print("button pushed")
            current_mode += 1 #change mode
            current_mode %= num_modes
            time_last_pressed = now
            button_down = True

    if BUTTON_PIN.value() and button_down: #ie if released and pressed before
        button_down = False

    #update display
    oled.show()
