from enum import auto
from time import sleep
from cozify import hub
from cozify import cloud
from envirophat import light
import threading
import keyboard
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
def Automation():

  global target
  global previousSetBrigthness
  global margin
  global automation
  global status

  try:
    #if hub.ping:
    #  print("connected to device")
    #devices = hub.devices()
    #for id, dev in devices.items():
    # print(id,dev['name'])
    brightness = light.light()
    print('measure1:', brightness)

    toSet = 0

    # TURN UP IF LOWER THAN TARGET
    if brightness < target-margin:
      toSet = min(prev + 0.05,1)
      if not status:
        print("Turning lamp on")
        hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
        status = True
      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=200)
        previousSetBrigthness = toSet
        print("successfully modified brightness to ",toSet)

    # TURN DOWN IF HIGHER THAN TARGET
    elif brightness > target+margin:
      toSet = prev - 0.05
      if(toSet <= 0 & status):
        print("Turning lamp off ")
        status = False
        hub.device_off('eba972f3-c624-436f-b49a-e4bae033eb2c')
        previousSetBrigthness = 0
      else:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=200)
        previousSetBrigthness = toSet

      print("successfully modified brightness to ", toSet)

    else:
      print("Gang Gang, in target")

    
    sleep(0.5)
    return previousSetBrigthness
  except:
    print("error connecting to cozify", sys.exc_info()[0])
    sleep(0.1)

def main():

  # SET STARTING VALUES

  global previousSetBrigthness

  #code starts here
  while 1:
    try: 
      Automation()
      print(f"{previousSetBrigthness}")
      
    except KeyboardInterrupt :
      run = False

main()