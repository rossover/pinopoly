#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

def close_all(signal,frame):
    global continue_reading
    print("Turning off")
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, close_all)
rfid_device = MFRC522.MFRC522()

print("Started, press CTRL+C to stop")

while continue_reading:
    # detect touch of the card, get status and tag type
    (status,TagType) = rfid_device.MFRC522_Request(rfid_device.PICC_REQIDL)

    # check if card detected or not
    if status == rfid_device.MI_OK:
        print("Card detected")

    # Get the RFID card uid and status
    (status,uid) = rfid_device.MFRC522_Anticoll()

    # If status is alright, continue to the next stage
    if status == rfid_device.MI_OK:
        # Print UID
        print("Card read UID: %s%s%s%s" % (hex(uid[0]).split('x')[-1], hex(uid[1]).split('x')[-1], hex(uid[2]).split('x')[-1], hex(uid[3]).split('x')[-1]))

        # default key of FF FF FF FF FF FF
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        # select the scanned tag
        rfid_device.MFRC522_SelectTag(uid)
        
        # try to authenticate
        status = rfid_device.MFRC522_Auth(rfid_device.PICC_AUTHENT1A, 8, key, uid)

        # if authenticated, read sector 8 and end
        if status == rfid_device.MI_OK:
            rfid_device.MFRC522_Read(8)
            rfid_device.MFRC522_StopCrypto1()
        else:
            print("Authentication error")