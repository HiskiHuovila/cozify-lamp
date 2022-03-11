from time import sleep
from cozify import hub
from cozify import cloud
# from envirophat import light
#cloud.authenticate()
cloud.ping()
def Main():
  try:
    devices = hub.devices()
    for id, dev in devices.items():
      print(id,dev['name'])
    #brightness = light.light()
    #toSet = brightness / 100
    hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', 1, transition=0)
    sleep(300)
  except:
    sleep(5)

run = True
while(run):
  try: 
    Main()
  except KeyboardInterrupt :
    run = False
