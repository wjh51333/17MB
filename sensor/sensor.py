# humidity > 50 % ->open the door
# humidity < 40 % ->close the door

#!/usr/bin/python

import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

#connect sensor
led_R = 20
led_Y = 21
PIR_sensor = 17
servomotor_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_R, GPIO.OUT)
GPIO.setup(led_Y, GPIO.OUT)
GPIO.setup(PIR_sensor, GPIO.IN)
GPIO.setup(servomotor_pin, GPIO.OUT)

print("PIR Ready..")
time.sleep(5)
successcnt = 0
notcnt = 0
#PMW: change pulse
p = GPIO.PWM(servomotor_pin, 50)

sensor_args = {
    '11': Adafruit_DHT.DHT11,
    '22': Adafruit_DHT.DHT22,
    '2302': Adafruit_DHT.AM2302
}

if len(sys.argv) == 3 and sys.argv[1] in sensor_args :
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
    
else : #ERROR occurs HERE !!!
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print(
        'Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO' +
        ' pin #4'
    )
    sys.exit(1)

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
flag = 0
p.start(0)
p.ChangeDutyCycle(2.5)
#0
print("servo, humidity Ready..")


try :
    while True :
        curHum=0
        break_condition=0
        #PIR sensor
        if GPIO.input(PIR_sensor) == 1 :
            GPIO.output(led_Y, 1)
            GPIO.output(led_R, 0)
            print("Motion Detected !")
            successcnt += 1
            time.sleep(1)
        
        if GPIO.input(PIR_sensor) == 0 :
            GPIO.output(led_R, 1)
            GPIO.output(led_Y, 0)
            print("not detected !")
            time.sleep(1)
            notcnt = 1
       
        if successcnt == 5 :
            print("type1")
            break_condition=1
            successcnt = 0
            responseString = '{"state":"connected", "type":"1", "message":""}'
        
        if notcnt == 1 :
            notcnt = 0
            successcnt = 0
            
        #servo motor
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None :
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            
            if curHum != format(humidity) :
                curHum = format(humidity)
                break_condition=1
                if break_condition == 1 :
                    print("type 3")
                else :
                    print("type 2")
                
            if humidity > 69 :
                if flag == 0 :
                    flag = 1
                    cnt = 0
                    p.ChangeDutyCycle(7.5)#90
                    time.sleep(1)
                    p.ChangeDutyCycle(5.0)
                    time.sleep(1)
                    p.ChangeDutyCycle(2.5)#0
                    time.sleep(1)
            elif humidity <= 69 :
                if flag == 1 :
                    p.ChangeDutyCycle(7.5)#0
                flag = 0
            time.sleep(1)
        else :
            print('Failed to get reading. Try again!')
            sys.exit(1)

        if break_condition==1:
            print("break")
            break
except KeyboardInterrupt :
    print("Stopped by User")
    p.stop()
    GPIO.cleanup()
