# Hardware-2-FA
A Raspberry Pi pico controled, hardware level 2-factor authentication system using a Raspberry Pi Pico in Micropython.
## **Requirements**
- KY-040 Binary encoder.
- MFRC-522 RFID reader & RFID tags.
- Raspberry Pi Pico/Pico W
- SSD1306 OLED 128*64
- Relays as per requirement
### Connections:
![circuit connections](https://github.com/0x416E50/Hardware-2-FA-/assets/167105040/4af39e42-1c13-4239-a752-102c237139a0)
Connect the Components according to the diagram above. **_The relay connections are to be made according to the required pins mentioned in your code._**
## Implementation:
Save the Library files of SSD1306, MFRC 522, KY 040 as follows:
- SSD1306 : [ssd1306.py](https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py)
- KY 040 Rotary encoder: [rotary_irq_esp.py](https://github.com/miketeachman/micropython-rotary/blob/master/rotary_irq_esp.py),[rotary_irq_rp2.py](https://github.com/miketeachman/micropython-rotary/blob/master/rotary_irq_rp2.py)
- MFRC 522: [mfrc522.py](https://github.com/danjperron/micropython-mfrc522/blob/master/mfrc522.py)

### Note: **Pin is enteres by rotating the binary encoder anti clockwise. Pin is entered from left to right. Pressing on the rotary encoder saves the digit and move to the next digit.**  Entering '0' 4 times resets the circuit. 

Save them in the Raspberry Pi Pico.
Now save the [main.py](https://github.com/0x416E50/Hardware-2-FA-/blob/main/main.py) to run the program. 
To read new tags, save and run [RFID_reader.py](https://github.com/0x416E50/Hardware-2-FA-/blob/main/RFID_reader.py)
Make sure to change the uid, usernames, pin and GPIO pin.
