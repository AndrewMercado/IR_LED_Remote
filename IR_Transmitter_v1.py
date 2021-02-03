#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 01:13:54 2021

@author: andrew
"""

import RPi.GPIO as GPIO
from time import sleep
import os

GPIO.setmode(GPIO.BCM)

LED = 20 #set up led pin
GPIO.setup(LED, GPIO.OUT) #set up led pin

GPIO.output(LED,0) #set led to low


def decode_hex(button_code):
    binary = bin(int(f'{button_code[2:]}',16))
    return binary[4:]
    



def remote_choices():
    remotes = {}
    counter = 0
    for root, dirs, files in os.walk("."):
        for filename in files:
            if '.txt' in filename:
                counter += 1
                remotes[counter] = filename
    print('Which remote would you like to choose?')
    for items in remotes:
        print(f'{items} - {remotes[items]}')
    remote_num = int(input('... '))
    print(f'You chose the {remotes[remote_num][0:-4]} remote')
    return remotes[remote_num]



def button_choices(file):
    f = open(f'{file}','r')  #open file
    buttons = {} # assign dictionary to store button codes
    print('\nAvaliable buttons:\n')
    for line in f: #loop through lines in the remote file
        print(line.split(' - ')[0]) #print the name of each button
        buttons[line.split(' - ')[0]] = line.split(' - ')[1][0:-1] #store buttons to their corresponding code in dictioanry
        
    f.close() #close file
    return buttons # return saved dictionary



################### replace Fan.txt with remote_choices()
file = 'Fan.txt'



while True:
    
    buttons = button_choices(file) #display buttons
    
    '''
    button_choice = input('Which button would you like to send? (Type "Done" to quit.):').capitalize()
    '''
    ################################
    button_choice = 'Power'
    
    if button_choice not in buttons:
        print('Closing Program')
        break
    
    

    binary_code = decode_hex(buttons[f'{button_choice}'])
    
    
    print(binary_code)
    
    #Send NEC protocol leading pulse burst and space
    GPIO.output(LED,1)
    sleep(0.009)
    GPIO.output(LED,0)
    sleep(0.0045)
    
    #send 32 bit command
    for i in binary_code:
        if i == '1':
            GPIO.output(LED,1)
            sleep(0.00165)
        else:
            GPIO.output(LED,1)
            sleep(0.00054)
        GPIO.output(LED,0)
        sleep(0.00060)

    
            
    print('Command Sent')


    sleep(.01)
    
