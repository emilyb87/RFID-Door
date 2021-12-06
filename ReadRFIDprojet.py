#!/usr/bin/env python
# -*- coding: utf8 -*-
# Version modifiee de la librairie https://github.com/mxgxw/MFRC522-python

import RPi.GPIO as GPIO
import MFRC522
import signal
import time

#leds setup
led_rouge = 36
led_vert = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_rouge, GPIO.OUT)
GPIO.output(led_rouge, GPIO.LOW)
GPIO.setup(led_vert, GPIO.OUT)
GPIO.output(led_vert, GPIO.LOW)

##Servo motor
OFFSE_DUTY = 0.5        #define pulse offset of servo
SERVO_MIN_DUTY = 2.5+OFFSE_DUTY     #define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 12.5+OFFSE_DUTY    #define pulse duty cycle for maximum angle of servo
servoPin = 12

def map( value, fromLow, fromHigh, toLow, toHigh):  # map a value from one range to another range
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

def setup():
    global p
    GPIO.setmode(GPIO.BOARD)         # use PHYSICAL GPIO Numbering
    GPIO.setup(servoPin, GPIO.OUT)   # Set servoPin to OUTPUT mode
    GPIO.output(servoPin, GPIO.LOW)  # Make servoPin output LOW level

    p = GPIO.PWM(servoPin, 50)     # set Frequece to 50Hz
    p.start(0)                     # Set initial Duty Cycle to 0
    
def servoWrite(angle):      # make the servo rotate to specific angle, 0-180 
    if(angle<0):
        angle = 0
    elif(angle > 180):
        angle = 180
    p.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY)) # map the angle to duty cycle and output it
    
def loop():
    print("sweep!")
    for dc in range(0, 181, 1):   # make servo rotate from 0 to 180 deg
        servoWrite(dc)     # Write dc value to servo
        time.sleep(0.001)
    time.sleep(0.5)
    for dc in range(180, -1, -1): # make servo rotate from 180 to 0 deg
        servoWrite(dc)
        time.sleep(0.001)
    time.sleep(0.5)

continue_reading = True

def accept():
	print("Accepte, veuillez entrer.")
        loop()
	GPIO.output(led_vert, GPIO.HIGH)
	time.sleep(3)
	GPIO.output(led_vert, GPIO.LOW)

    

def refuse():
	print("Refuse, vous n'etes pas employe.")
	GPIO.output(led_rouge, GPIO.HIGH)
	time.sleep(3)
	GPIO.output(led_rouge, GPIO.LOW)

# Fonction qui arrete la lecture proprement 
def end_read(signal,frame):
    global continue_reading
    print ("Lecture terminée")
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()


print ("Passer le tag RFID a lire")
while continue_reading:
    
    # Detecter les tags
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Une carte est detectee
    if status == MIFAREReader.MI_OK:
        print ("Carte detectee")
    
    # Recuperation UID
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:
        print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
    
        # Clee d authentification par defaut
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Selection du tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authentification
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 1, key, uid)
        #if status == MIFAREReader.MI_OK:
            #MIFAREReader.MFRC522_Read(1)
            #MIFAREReader.MFRC522_StopCrypto1()
        #else:
        #	print("Erreur d\'Authentification")
        #print(text)
	#ascii_values = [ord(character) for character in text]
    
	#with open("numEmployes.txt") as f:
	#	lines = f.readlines()
	#for line in lines:
	#	if text == line:
	#		accept()
    #    print(line)

        text = MIFAREReader.MFRC522_Readstr(1)
    # Using readlines()
        file1 = open('numEmployes.txt', 'r')
        Lines = file1.readlines()
        print (text)
    # Strips the newline character
        for line in Lines:
            if str(line) == str(text):
                accept()
                break
                print(line)
                print (text)
	    
        refuse()

	#print("text")
	
	
		

