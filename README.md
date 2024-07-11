# Mock-HVAC-System
This is a microcontroller & IoT system oriented project to mimick a Heating, Ventilation, Air Conditioning system. 
Tools used: 
1. a RaspberryPi 4B as the main microcontroller, RaspberryPi OS
2. a DHT-11 as the temperature sensor, a PIR motion sensor, a Hitachi HD44780U LCD as the main UI, and some pushbuttons + LEDs as secondary ways to interact with the system. 
3. other pieces of data such as local humidity, air quality index, and wind speed are gathered through the California Department of Water Resources API - https://et.water.ca.gov/Rest/Index. 
4. Python programming language

an overview of the system (lcd display is cutoff at the right of the image):
![overview](https://github.com/PengxuanW/portfolio/blob/main/images/hvac_overview.png?raw=true)

lcd display message example:
![lcd](https://github.com/PengxuanW/portfolio/blob/main/images/hvac_lcd.png?raw=true)

written report on the overall system:
[link](https://github.com/PengxuanW/Mock-HVAC-System/blob/main/report_final.pdf)

demo video link (Google Drive link):
[demo](https://drive.google.com/file/d/141ADcKhIx0Zh9J3aVPO4HO3q5jgL2FzZ/view?usp=sharing)
