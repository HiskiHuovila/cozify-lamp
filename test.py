from enum import auto
from os import stat
from time import sleep
from turtle import color
from urllib.parse import DefragResult
from cozify import hub
from cozify import cloud
from envirophat import light
import colour
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
automation = True
prevColor = 2700
colormargin = 1000
colorstatus = True
debug = False


# AUTOMATION LOOP
def Automation():

  global target
  global previousSetBrigthness
  global margin
  global prevColor
  global status
  global debug
  global colorstatus

  try:
    brightness = light.light()
    r, g, b = brightness.rgb()

    XYZ = colour.sRGB_to_XYZ([r,g,b] / 255)
    xy = colour.XYZ_to_xy(XYZ)
    CCT = colour.xy_to_CCT(xy, 'hernandez1999')

    toSet = 0.5

    # TURN UP IF LOWER THAN TARGET
    if brightness < target-margin:
      toSet = min(previousSetBrigthness + 0.02,1)

      if not status:        #checking is lamp off
        hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=20)
        previousSetBrigthness = toSet
        status = True    #setting lamp on
        if debug: 
          print(f"Measured: {brightness}. Turned lamp on and set light brightness to {round(toSet,2)}")

      elif toSet < 1:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=20)
        previousSetBrigthness = toSet
        if debug:
          print(f"Measured: {brightness}. Set light brightness to {round(toSet,2)}")

      else:
        if debug:
          print(f"Measured: {brightness}. Light stays at brightness {round(toSet,2)}")

    # TURN DOWN IF HIGHER THAN TARGET
    elif brightness > target+margin:
      toSet = previousSetBrigthness - 0.02

      if(toSet <= 0 and status):
        status = False
        hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
        previousSetBrigthness = 0
        if debug:
          print(f"Measured: {brightness}. Turning lamp off")

      elif(not status):
        if debug:
          print(f"Measured: {brightness}. Turning is off")

      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=20)
        previousSetBrigthness = toSet
        if debug:
          print(f"Measured: {brightness}. Turned lamp on and set light brightness to {round(toSet,2)}")

    else:
      if debug:
       print(f"Measured: {brightness}. In target")

    # COLOR TEMPERATURE
    if colorstatus:
      if(CCT < 2200):
        if(prevColor > 2250):
          hub.light_temperature('eba972f3-c624-436f-b49a-e4bae033eb2c', temperature=2200, transition=20)
          prevColor = 2200

      elif(CCT > 4500):
        if(prevColor < 4450):
          hub.light_temperature('eba972f3-c624-436f-b49a-e4bae033eb2c', temperature=4500, transition=20)
          prevColor = 4500

      else:
        if( abs(CCT - prevColor) > margin):
          hub.light_temperature('eba972f3-c624-436f-b49a-e4bae033eb2c', temperature=CCT, transition=20)
          prevColor = CCT
          
    if debug:
      print(f"Measured color: {CCT}. Lamp Color: {prevColor}")

    sleep(0.1)
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
  global automation
  global debug
  global colorstatus

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
          elif c == 'e':
            if status:
              hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
              status = False
              automation = False
              print('Turned lamp off')
            if not status:
              hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
              status = True
              automation = True
              print('Turned lamp on')
          elif c == 'd':
            colorstatus = not colorstatus
            print(f'Color automation: {colorstatus}')
          elif c == 'q':
            target += 1000
            print("target modified to ", target)
          elif c == 'a':
            target -= 1000
            print("target modified to ", target)
          elif c == 't':
            print(f'Target: {target}\nBrightness: {previousSetBrigthness}\nColor Temperature: {prevColor}\nAutomation mode: {automation}\nDebug mode: {debug}')
          elif c == 'g':
            debug = not debug
            print(f'Debug mode {debug}')
          elif c == 'h':
            print(f'HELP:\nToggle automation off/on -> e \nTurn target up/down by 100 -> d / s\nTurn target up/down by 1000 -> q / a \nReset target to original -> r\nShow status -> t\nToggle debug mode -> g\nExit application  -> ESC')
          else:
            print("unknown keyboard input")

        if automation:
          Automation()
        
      except KeyboardInterrupt :
        run = False

  finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)



main()