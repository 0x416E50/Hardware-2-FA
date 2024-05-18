from mfrc522 import MFRC522
import utime
from machine import Pin, SoftI2C
import ssd1306
rel1=Pin(13,Pin.OUT)
rel1.value(1)
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)
i2c = SoftI2C(scl=Pin(14), sda=Pin(15))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
print("Bring TAG closer...")
print("")
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL) 
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid), "little", False)
            print("CARD ID: " + str(card))           
            oled.fill(0)
            oled.text('ID no:', 0, 0)
            oled.text(str(card), 0, 10)  # Display card ID
            oled.show()
        utime.sleep(0.5)  # Sleep for 1 second before reading next card