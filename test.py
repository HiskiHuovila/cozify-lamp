from enum import auto
from time import sleep
from cozify import hub
from cozify import cloud
from envirophat import light
import threading
import keyword
import select
import sys

print("Started operating heavy machinery, status: ", cloud.authenticate())
# ORIGINAL TARGETS

ogtarget = 3000
moodtarget = 3000

# SET STARTING VALUES

target = ogtarget
moodtarget = moodtarget
previousSetBrigthness = 0.5
margin = 100
automation = True
status = True

# AUTOMATION LOOP
def Automation(target, prev, margin, status):

  try:
    #if hub.ping:
    #  print("connected to device")
    #devices = hub.devices()
    #for id, dev in devices.items():
    # print(id,dev['name'])
    brightness = light.light()
    print('measure1:', brightness)

    toSet = 0
    newprev = prev

    # TURN UP IF LOWER THAN TARGET
    if brightness < target-margin:
      toSet = min(prev + 0.05,1)
      if not status:
        print("Turning lamp on")
        hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
        status = True
      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=500)
        newprev = toSet
        print("successfully modified brightness to ",toSet)

    # TURN DOWN IF HIGHER THAN TARGET
    elif brightness > target+margin:
      toSet = prev - 0.05
      if(toSet <= 0):
        print("Turning lamp off ")
        status = False
        hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
        newprev = 0
      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=500)
        newprev = toSet

      print("successfully modified brightness to ", toSet)

    else:
      print("Gang Gang, in target")

    
    sleep(0.5)
    return newprev
  except:
    print("error connecting to cozify", sys.exc_info()[0])
    sleep(0.5)

def main():

  # SET STARTING VALUES


  global target
  global previousSetBrigthness
  global margin
  global automation
  global status

  #code starts here
  while 1:
    try: 
      if automation:
        newprev = Automation(target,previousSetBrigthness,margin,status)
        previousSetBrigthness = newprev
        print(f"{previousSetBrigthness}")
      
    except KeyboardInterrupt :
      run = False

thread = threading.Thread(target=main)
thread.start()

run = True
while run:
  try:
    #SETTING BRIGHTNESSS TARGET
    if keyword.is_pressed('q'):
      target =- 100
    if keyword.is_pressed('e'):
      target =+ 100
    
    # COLOR TEMPERATURE DOESN DO SHIT RIGHTNOW
    if keyword.is_pressed('a'):
      moodtarget =- 100
    if keyword.is_pressed('s'):
      moodtarget =+ 100

    # TOGGLE AUTOMATION
    if keyword.is_pressed('t'):
      automation = not automation
  except KeyboardInterrupt:
    run = False
  except:
    print('There was a ****** error!')

thread.do_run = False
thread.join()