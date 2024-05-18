import time
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
from rotary_irq_esp import RotaryIRQ
from mfrc522 import MFRC522
def setup_pin(pin_number, mode, pull=None):
    return Pin(pin_number, mode, pull)
def setup_rotary_encoder(pin_clk, pin_dt, min_val, max_val):
    return RotaryIRQ(pin_num_clk=pin_clk,
                     pin_num_dt=pin_dt,
                     min_val=min_val,
                     max_val=max_val,
                     incr=1,
                     reverse=False,
                     range_mode=RotaryIRQ.RANGE_BOUNDED)
def get_final_value(digits):
    return int(''.join(map(str, digits)))
def initialize_oled():
    i2c = SoftI2C(scl=Pin(14), sda=Pin(15))
    oled_width = 128
    oled_height = 64
    return SSD1306_I2C(oled_width, oled_height, i2c)
def display_message(oled, message, line=0):
    oled.fill(0)
    oled.text(message, 0, line * 10)
    oled.show()
def validate_rfid_tag(uid):
    users = {
        141106900: ('User1', 2003, 17), # 141106900 is the uid of the rfid tag, 2003 is the pin, 17 is the related GPIO Pin
        <uid>: ('<GPIO pin>', <pin>, <GPIO pin>)
    }
    return users.get(int.from_bytes(bytes(uid), "little", False), None)
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)
oled = initialize_oled()
display_message(oled, 'Welcome!')
r = setup_rotary_encoder(12, 13, 0, 9)
switch_pin = setup_pin(16, Pin.IN, Pin.PULL_UP)
while True:
    username = None
    pin = None
    gpio_pin = None
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)   
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()        
        if stat == reader.OK:
            card_id = int.from_bytes(bytes(uid), "little", False)
            print("CARD ID:", card_id)
            username_pin_gpio = validate_rfid_tag(uid)
            print("Validation Result:", username_pin_gpio)
            if username_pin_gpio is not None:
                username, pin, gpio_pin = username_pin_gpio
            else:
                display_message(oled, 'Invalid tag', 1)
                time.sleep(1.5)
                continue  # Restart the loop if invalid tag
            display_message(oled, username, 0)
            time.sleep(1.50)
            display_message(oled, 'Enter PIN', 1)   
            start_time = time.time()
            digits = [0, 0, 0, 0]
            digit_index = 0
            pin_entry_complete = False  # Flag to indicate PIN entry completion
            while time.time() - start_time < 60:  # Wait for 60 seconds for PIN entry
                value = r.value()
                if value >= 0:  
                    digits[digit_index] = value
                    oled.fill(0)
                    oled.text('Entered Pin:', 0, 0)
                    oled.text(''.join(map(str, digits)), 0, 20)
                    oled.show()
                    print('Entered Digit {}: {}'.format(digit_index + 1, digits))
                if switch_pin.value() == 0:
                    if digit_index < 3:  # Check if digit_index is within range
                        digit_index += 1
                        print('Switch Pressed - Move to Digit {}'.format(digit_index + 1))
                        time.sleep(0.1)
                    else:
                        pin_entry_complete = True
                        break  # Exit the loop to avoid further digit entry
                time.sleep_ms(50)
            if pin_entry_complete:
                entered_pin = get_final_value(digits)
                if entered_pin == pin:
                    display_message(oled, 'Success', 3)
                    print("Success")
                    gpio_pin = setup_pin(gpio_pin, Pin.OUT)  # Initialize GPIO pin for relay
                    gpio_pin.value(1)  # Activate the GPIO pin
                    time.sleep(2)  # Display success message for 2 seconds
                    gpio_pin.value(0)  # Deactivate the GPIO pin
                elif entered_pin == 0:
                    continue  # Restart the loop if entered PIN is 0000
                else:
                    display_message(oled, 'Wrong PIN entered,\ntry again later', 2)
                    time.sleep(2)  # Display message for 2 seconds before restarting
    else:
        display_message(oled, 'Welcome!')
