from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C

#define pins
#do not use pull up/down if irl one already in place
BUTTON_PIN = Pin(0, Pin.In)
DIRECTION_PIN = Pin(0, Pin.In)
STEP_PIN = Pin(0, Pin.In)
PWM_PIN = PWM(0, freq=440, duty_u16=0)


#define objects
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000) #freq: clock speed
oled = SSD1306_I2C(128, 64, i2c)

#more definitions :D
MODES = ["TONE", "SENSE"]
NOTES = [
    ["A", 440]
]

current_note = 0
previous_note = current_note
num_notes = len(NOTES)

current_mode = 0
previous_mode = 0
num_modes = len(MODES)

previous_value = True
button_down = False

while True: #main loop

    if MODES[current_mode] == "TONE":
        if current_mode != previous_mode: #check if mode has just been changed
            PWM_PIN.duty_u16(32768)
            previous_mode = current_mode

        if previous_note != current_note: #check if note has just been changed
            #start playing tone
            PWM_PIN.freq(NOTES[current_note][1])
            PWM_PIN.duty_u16(32768)
            previous_note = current_note

        # rotary encoder logic: check if note needs to be changed
        if previous_value != STEP_PIN.value():  # if STEP_PIN has changed
            if STEP_PIN.value() == False:
                if DIRECTION_PIN.value() == False:
                    print("turned left")
                    current_note -= 1 #previous note
                else:
                    print("turned right")
                    current_note += 1  #next note
                current_note %= num_notes
            previous_value = STEP_PIN.value()

    elif MODES[current_mode] == "SENSE":
        if current_mode != previous_mode:  # check if mode has just been changed
            PWM_PIN.duty_u16(0) #stop playing tone
            previous_mode = current_mode

    #check if button pressed to change mode
    #button logic: True for not pressed, False for pressed
    if not BUTTON_PIN.value() and not button_down: #ie if pressed and not pressed before
        print("button pushed")
        current_mode += 1 #change mode
        current_mode %= num_modes
        button_down = True
    if BUTTON_PIN.value() and button_down: #ie if released and pressed before
        button_down = False
