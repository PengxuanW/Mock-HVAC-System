#Pengxuan Wu
#48946113
import requests
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import I2CLCD1602
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
from time import sleep, strftime

url = 'http://et.water.ca.gov/api/data?appKey=ab715ae9-b712-4d75-aab9-2ce3542108ed&targets=75&startDate=2024-06-12&endDate=2024-06-12&dataItems=day-rel-hum-avg'

respons = requests.get(url)
print(response.status_code)

humidity = response.json()['Data']['Providers'][0]['Records'][0]['DayRelHumAvg']['Value']


buttonPin = 22
button2Pin = 15
button3Pin = 12
ledPin = 29
ledRedPin = 31
ledBluePin =  32
DHTPin = 11
sensorPin = 13 

okTemp = 0
desired_temp = 70
custom_message = ''
status_changed = False
ac_status_change
door_is_open = 'C'
hvac = 'OFF'
ambient_light = 'OFF'


GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button3Pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(ledRedPin, GPIO.OUT)
GPIO.setup(ledBluePin, GPIO.OUT)
        
def loop():
    mcp.output(3,1)
    lcd.begin(16,2)
    global okTemp
    global custom_message
    global desired_temp
    global door_is_open
    global status_changed
    global ac_status_change
    global hvac
    previous_counts = 0 
    counts = 0
    
    while(True):
        temp_sum = 0
		temp_count = 0
        
        dht = DHT.DHT(DHTPin)
        counts += 1
        print('Measurement counts: ', counts)
        for i in range(0,15):
            chk = dht.readDHT11()
            if (chk == dht.DHTLIB_OK):
                temp_sum += dht.temperature
                temp_count += 1
                if temp_count == 3:
					break
            sleep(0.1)
        okTemp = round((temp_sum / temp_count) * (9/5) + 32) + 0.05 * humidity
        
        if okTemp >= 95:
            door_is_open == 'O'
            GPIO.output(ledPin, GPIO.HIGH)
            GPIO.output(ledRedPin, GPIO.HIGH)
            GPIO.output(ledBluePin, GPIO.HIGH)
            sleep(1)
            GPIO.output(ledPin, GPIO.LOW)
            GPIO.output(ledRedPin, GPIO.LOW)
            GPIO.output(ledBluePin, GPIO.LOW)
            sleep(0.1)
            lcd.clear()
            sleep(0.1)
            lcd.message('fire alarm')
            
		else:
            if (counts - previous_counts) > 9:
                GPIO.output(ledPin, GPIO.LOW) 
                ambient_light = 'Off'
                
            if (door_is_open == 'O'):
                hvac = 'OFF'
            elif (abs(desired_temp - okTemp) < 3) and hvac != 'OFF':
                hvac = 'OFF'
                ac_status_change = True
            elif (okTemp - desired_temp > 3) and hvac != 'AC':
                hvac = 'AC'
                ac_status_change = True
            elif (desired_temp - okTemp > 3) and hvac != 'HEAT':
                hvac = 'HEAT'
                ac_status_change = True
            
            if status_changed:
                sleep(0.1)
                lcd.clear()
                sleep(0.1)
                lcd.setCursor(0,0)
                if door_is_open == 'O':
                    lcd.message('door open!')
                    #door_is_open = 'C'
                else:
                    lcd.message('door closed!')
                    #door_is_open = 'O'
                sleep(3)
                status_changed = False
            elif ac_status_change:
                sleep(0.1)
                lcd.clear()
                sleep(0.1)
                lcd.setCursor(0,0)
                if hvac == 'OFF':
                    lcd.message('HVAC OFF')
                elif hvac == 'HEAT':
                    lcd.message('HEATER ON')
                else:
                    lcd.message('AC ON')
                sleep(3)
                ac_status_change = False
            else:
                if GPIO.input(sensorPin) == GPIO.HIGH:
                    ambient_light = 'On '
                    GPIO.output(ledPin, GPIO.HIGH)
                    previous_counts = counts
                                
                custom_message =  '' + str(desired_temp) + '/' + str(okTemp) + '    Dr:' + str(door_is_open) + '\nH:' + str(hvac) + '  L:' + str(ambient_light)
                lcd.setCursor(0,0)
                lcd.message(custom_message)
                sleep(0.8)
        
        
def destroy():
    lcd.clear()


def toggle_red_led(channel):
    global desired_temp
    global hvac
    global ac_status_change
    GPIO.output(ledRedPin, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(ledRedPin, GPIO.LOW)
    desired_temp += 1
    if (desired_temp - okTemp > 3):
        hvac = 'HEAT'
        ac_status_change = True

def toggle_blue_led(channel):
    global desired_temp
    global hvac
    global ac_status_change
    GPIO.output(ledBluePin, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(ledBluePin, GPIO.LOW)
    desired_temp -= 1
    if (okTemp - desired_temp < 3):
        hvac = 'AC'
        ac_status_change = True

def toggle_door(channel):
    global door_is_open
    global status_changed 
    if(door_is_open == 'C'):
        door_is_open = 'O'
    else:
        door_is_open = 'C'
    status_changed = True
    
PCF8574_address = 0x27
PCF8574A_address = 0x3f

GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback = toggle_red_led, bouncetime = 200)
GPIO.add_event_detect(button2Pin, GPIO.FALLING, callback = toggle_blue_led, bouncetime = 200)
GPIO.add_event_detect(button3Pin, GPIO.FALLING, callback = toggle_door, bouncetime = 200)


try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print('I2C Address Error !')
        exit(1)
        
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print('starting')
    
    try:
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        GPIO.cleanup()
        exit()
        
    
