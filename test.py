from enum import auto
from os import stat
from time import sleep
from cozify import hub
from cozify import cloud
from envirophat import light
#import threading
#import keyboard
import sys
import select
import tty
import termios

print("Started operating heavy machinery, status: ", cloud.authenticate())


# SET STARTING VALUES

target = 3000
previousSetBrigthness = 0.5
margin = 100
#automation = True
hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
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
        print(f"Measured: {brightness}. Turned lamp on and set light brightness to {round(toSet,1)}")
        status = True    #setting lamp on
      elif toSet < 1:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=100)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Set light brightness to {round(toSet,1)}")
      else:
        print(f"Measured: {brightness}. Light stays at brightness {round(toSet,1)}")

    # TURN DOWN IF HIGHER THAN TARGET
    elif brightness > target+margin:
      toSet = previousSetBrigthness - 0.05
      if(toSet <= 0 and status):
        print(f"Measured: {brightness}. Turning lamp off")
        status = False
        hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
        previousSetBrigthness = 0
      elif(not status):
        print(f"Measured: {brightness}. Turning is off")
      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=100)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Turned lamp on and set light brightness to {round(toSet,1)}")

      

    else:
      print(f"Measured: {brightness}. In target")

    
    sleep(0.2)
    return previousSetBrigthness
  except:
    print("error connecting to cozify", sys.exc_info()[0])
    sleep(0.2)



def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def main():

  # SET STARTING VALUES

  global previousSetBrigthness

  run = True
  #code starts here

  old_settings = termios.tcgetattr(sys.stdin)
  try:
    tty.setcbreak(sys.stdin.fileno())

    while run:
      try: 
        if isData():
          c = sys.stdin.read(1)
          if c == '\x1b':         # x1b is ESC
            run = False
          elif c == 'w':
            run = False
          elif c == 's':
            run = False

        Automation()
        
      except KeyboardInterrupt :
        run = False

  finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)



main()