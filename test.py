from time import sleep
from cozify import hub
from cozify import cloud
from envirophat import light
#cloud.authenticate()
def Main():
  try:
    devices = hub.devices()
    for id, dev in devices.items():
      print(id,dev['name'])
    brightness = light.light()
    print(brightness)
    toSet = (3000 - brightness) / 3000
    if toSet < 0 :
      toSet = 0
    hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=0)
    sleep(10)
  except:
    sleep(5)

run = True
while(run):
  try: 
    Main()
  except KeyboardInterrupt :
    run = False
