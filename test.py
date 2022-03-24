from enum import auto
from os import stat
from time import sleep
from cozify import hub
from cozify import cloud
from envirophat import light
import threading
import keyboard
import sys

print("Started operating heavy machinery, status: ", cloud.authenticate())


# SET STARTING VALUES

target = 3000
previousSetBrigthness = 0.5
margin = 100
#automation = True
status = True   #boolean on off

# AUTOMATION LOOP
def Automation():

  global target
  global previousSetBrigthness
  global margin
  #global automation
  global status  #boolean on off

  try:
    brightness = light.light()

    toSet = 0.5

    # TURN UP IF LOWER THAN TARGET
    if brightness < target-margin:
      toSet = min(previousSetBrigthness + 0.05,1)
      if not status:        #checking is lamp off
        hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=200)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Turned lamp on and set light brightness to {toSet}", end='\x1b[1K\r')
        status = True    #setting lamp on
      elif toSet < 1:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=100)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Set light brightness to {toSet}", end='\x1b[1K\r')
      else:
        print(f"Measured: {brightness}. Light stays at brightness {toSet}", end='\x1b[1K\r')

    # TURN DOWN IF HIGHER THAN TARGET
    elif brightness > target+margin:
      toSet = previousSetBrigthness - 0.05
      if(toSet <= 0 and status):
        print(f"Measured: {brightness}. Turning lamp off", end='\x1b[1K\r')
        status = False
        hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
        previousSetBrigthness = 0
      elif(not status):
        print(f"Measured: {brightness}. Turning is off", end='\x1b[1K\r')
      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=100)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Turned lamp on and set light brightness to {toSet}", end='\x1b[1K\r')

      

    else:
      print(f"Measured: {brightness}. In target", end='\x1b[1K\r')

    
    sleep(0.2)
    return previousSetBrigthness
  except:
    print("error connecting to cozify", sys.exc_info()[0])
    sleep(0.2)

def main():

  # SET STARTING VALUES

  global previousSetBrigthness

  run = True
  #code starts here
  while run:
    try: 
      Automation()
      print(f"{previousSetBrigthness}")
      
    except KeyboardInterrupt :
      run = False

main()