from enum import auto
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
    if hub.ping:
      print("connected to device")
    #devices = hub.devices()
    #for id, dev in devices.items():
    # print(id,dev['name'])
    brightness = light.light()
    print('measure1:', brightness)

    toSet = 0.5

    # TURN UP IF LOWER THAN TARGET
    if brightness < target-margin:
      toSet = min(previousSetBrigthness + 0.05,1)
      if not status:
        print("Turning lamp on")
        hub.device_on('eba972f3-c624-436f-b49a-e4bae033eb2c')
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=200)
        previousSetBrigthness = toSet
        status = True
      elif toSet < 1:
        hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=200)
        previousSetBrigthness = toSet
        print("successfully modified brightness to ",toSet)
      else:
        print("sdfihl")

    # TURN DOWN IF HIGHER THAN TARGET
    elif brightness > target+margin:
      toSet = previousSetBrigthness - 0.05
      if(toSet <= 0):
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