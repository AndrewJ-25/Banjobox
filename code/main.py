"""
REPL: screen /dev/tty.usbmodem101 115200
kill: screen -X -S 97181.ttys001.RE550 quit
ctrl D soft reset
    or
ctrl A, => k =>y

OLED shows 16 characters

exec(open("main.py").read())
"""
print("pls workk ahahaha:)")
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import time
import sht31

#define pins
#do not use pull up/down if irl one already in place
BUTTON_PIN = Pin(28, Pin.IN, Pin.PULL_UP)
DIRECTION_PIN = Pin(9, Pin.IN, Pin.PULL_UP)
STEP_PIN = Pin(1, Pin.IN, Pin.PULL_UP)
PWM_PIN = Pin(0)

#instantiate objects
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000) #freq: clock speed
oled = SSD1306_I2C(128, 32, i2c)
#pwm = PWM(PWM_PIN, freq=440, duty_u16=0)
sensor = sht31.SHT31(i2c)

oled.fill(0)
oled.text("pls work ahahah", 0, 0)
oled.show()
time.sleep(2)

#more definitions :D
MODES = ["TONE", "SENSE"]
NOTES = [
    ["G4", 392.00],
    ["D3", 146.83],
    ["G3", 196.00],
    ["B3", 246.94],
    ["D4", 293.66]
]

#concerning debouncing
last_button = 0
time_last_pressed = 0
DEBOUNCE_TIME = 50

#note selection
current_note = 0
previous_note = current_note
num_notes = len(NOTES)

#mode selection
current_mode = 0
previous_mode = -1
num_modes = len(MODES)

#SHT31 interval
READ_INTERVAL = 1
time_last_reading = time.ticks_ms()

#idk wut this is
previous_value = True

#main loop
while True:
    now = time.ticks_ms()
    button = BUTTON_PIN.value()

    #clear display
    oled.fill(0)

    #tone mode
    if current_mode == 0:
        """
        # check if mode has just been changed
        if current_mode != previous_mode:
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
        """

        oled.fill(0)
        oled.text("Tone", 0, 0)
        oled.text(NOTES[current_note][0], 0, 10)

    #sense mode
    elif current_mode == 1:
        """
        if current_mode != previous_mode:  # check if mode has just been changed
            pwm.duty_u16(0) #stop playing tone
            previous_mode = current_mode
        """

        if time.ticks_diff(now, time_last_reading) > READ_INTERVAL:
            temp, humidity = sensor.get_temp_humi()
            print(f"Temperature: {temp}°C Humidity: {humidity}%")
            time_last_reading = now

            oled.fill(0)
            oled.text("Sense", 0, 0)
            oled.text(f"{round(temp,1)}°C {round(humidity)}%", 0, 10)

    #check if button pressed to change mode
    #button logic: True for not pressed, False for pressed
    print(BUTTON_PIN.value())
    if button and not last_button: #ie if pressed and not pressed before
        if time.ticks_diff(now, time_last_pressed) > DEBOUNCE_TIME:
            print("button pushed")
            # change mode
            current_mode = (current_mode + 1) % num_modes
            time_last_pressed = now

    last_button = button

    #update display
    oled.show()
