import network
import time

def enable_hotspot():
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    time.sleep(2)
    ap.config(essid='picow', password='picow123')
    ap.active(True)
    while not ap.active():time.sleep(1)
    return {'status':'success','message':f'hotspot enabled:{ap.ifconfig()[0]}'}

def connect_wifi(ssid='Devil', password='annyeo12'):
    sta = network.WLAN(network.STA_IF)
    sta.active(False)
    time.sleep(1)
    sta.active(True)
    sta.connect(ssid, password)
    for i in range(10):
        if sta.isconnected():break
        else:
            if i==9:return {'status':'failure','message':'Not connected'}
            print('reconnecting')
            time.sleep(1)
    return {'status':'success','message':f'Connected with {sta.ifconfig()[0]}'}
