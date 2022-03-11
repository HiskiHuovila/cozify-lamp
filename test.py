from time import sleep
from cozify import hub
from cozify import cloud
from envirophat import light
#cloud.authenticate()
def Main():
  try:
    #devices = hub.devices()
    #for id, dev in devices.items():
     # print(id,dev['name'])
    brightness = light.light()
    print('measure1:', brightness)
    toSet = (3000 - brightness) / 3000
   
    if brightness > 3000 :
      toSet = 0
      
    hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition=2000)
    sleep(4)
    
    brightness2 = light.light()
    print('measure2:', brightness2)
    avg = (brightness + brightness2)/2
    print('average:', avg)
    toSet =  (3000 - avg) / 3000
    
    if brightness > 3000 :
      toSet = 0
      
    hub.light_brightness('eba972f3-c624-436f-b49a-e4bae033eb2c', toSet, transition = 2000)
    sleep(4)
  except:
    sleep(4)

run = True
while(run):
  try: 
    Main()
  except KeyboardInterrupt :
    run = False