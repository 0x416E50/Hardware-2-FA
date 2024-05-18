## To add a tag, first read the tag id using [RFID_reader.py](https://github.com/0x416E50/Hardware-2-FA-/blob/main/RFID_reader.py). The tag appears in the shell as shown. 

![image](https://github.com/0x416E50/Hardware-2-FA-/assets/167105040/b6fb3060-6fdf-40e4-80ee-e8ee6ddcc403)

To add a tag, connect a micro USB cable to the Raspberry Pi Pico. Open Thonny IDE, and open main.py. There, in line numebr 27, there is the function **def_RFID_tag**.
It's a dictionary, that is responsible to store all the registered tags, their Pins, and the respective GPIO pin that triggers the relay. 
Add the tag, following the order

        def validate_rfid_tag(uid):
                  users = {
                      <uid>: ('User1', <Pin>, <GPIO Pin>)
                  }

![image](https://github.com/0x416E50/Hardware-2-FA-/assets/167105040/9b2a0b87-b3a1-46ea-b9a1-a43156f41bc3)

Save the program file and run it. 
