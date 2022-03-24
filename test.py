from enum import auto
from os import stat
from time import sleep
from urllib.parse import DefragResult
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
default = int(input("Tell target pls:"))
target = default
previousSetBrigthness = 0.5
margin = max(target/8, 10)
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
      toSet = min(previousSetBrigthness + 0.02,1)
      if not status:        #checking is lamp off
        hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=200)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Turned lamp on and set light brightness to {round(toSet,2)}")
        status = True    #setting lamp on
      elif toSet < 1:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=50)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Set light brightness to {round(toSet,2)}")
      else:
        print(f"Measured: {brightness}. Light stays at brightness {round(toSet,2)}")

    # TURN DOWN IF HIGHER THAN TARGET
    elif brightness > target+margin:
      toSet = previousSetBrigthness - 0.02
      if(toSet <= 0 and status):
        print(f"Measured: {brightness}. Turning lamp off")
        status = False
        hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
        previousSetBrigthness = 0
      elif(not status):
        print(f"Measured: {brightness}. Turning is off")
      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=50)
        previousSetBrigthness = toSet
        print(f"Measured: {brightness}. Turned lamp on and set light brightness to {round(toSet,2)}")

      

    else:
      print(f"Measured: {brightness}. In target")

    
    sleep(0.1)
    return previousSetBrigthness
  except:
    print("error connecting to cozify", sys.exc_info()[0])
    sleep(0.1)



def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def main():

  # SET STARTING VALUES

  global previousSetBrigthness
  global target
  global default
  global status

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
            target += 100
            print("target modified to ", target)
          elif c == 's':
            target -= 100
            print("target modified to ", target)
          elif c == 'r':
            target = default
            print("target modified to ", target)
          elif c == 'd':
            hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
            status = False
            print('Turned lamp off')
          elif c == 'e':
            hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
            status = True
            print('Turned lamp on')
          else:
            print("unknown keyboard input")

        Automation()
        
      except KeyboardInterrupt :
        run = False

  finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)



main()