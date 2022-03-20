from time import sleep
from cozify import hub
from cozify import cloud
from envirophat import light
import select
import sys

target = 3000
previousSetBrigthness = 0.5
margin = 100
automation = true

#cloud.authenticate()
def Automation():
  try:
    #if hub.ping:
    #  print("connected to device")
    #devices = hub.devices()
    #for id, dev in devices.items():
     # print(id,dev['name'])
    brightness = light.light()
    print('measure1:', brightness)
    

    if brightness > target+margin:
      toSet = previousSetBrigthness + 0.1
      hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=1000)
      previousSetBrigthness = toSet

    if brightness < target-margin:
      toSet = previousSetBrigthness - 0.1
      hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=1000)
      previousSetBrigthness = toSet
    else:
      print("Gang Gang, in target")

    sleep(2)
  except:
    sleep(2)


#code starts here
run = True
while(run):
  try: 
    input = select.select([sys.stdin], [], [], 1)[0]
    if input:
        value = sys.stdin.readline().rstrip()
 
        if (value == "num0"):
            automation = not automation
            print(f"Automation set to {automation}")
        else:
            print("keypressed: ", value)
    else:
      if automation:
        Automation()
        print(f"{previousSetBrigthness}")
    
  except KeyboardInterrupt :
    run = False