import network
import time

class WiFi:
    def __init__(self):
        self.hotspot_configure()
        #self.router_configure()

    def hotspot(self):pass
    def router(self):pass


    def hotspot_configure(self):
        ap = network.WLAN(network.AP_IF)
        ap.active(False)
        time.sleep(2)
        ap.config(essid='picow', password='picow123')
        ap.active(True)
        while not ap.active():time.sleep(1)
        ip = ap.ifconfig()[0]
        with open('example.txt', 'w') as file:
            file.write(str(ap.config('essid')))

        print('Access Point active. IP:', ip)
        return ip

    def router_configure(self, ssid='Devil', password='annyeo12'):
        sta = network.WLAN(network.STA_IF)
        sta.active(False)
        time.sleep(1)
        sta.active(True)
        sta.connect(ssid, password)
        while not sta.isconnected():time.sleep(1)
        ip = sta.ifconfig()[0]
        print('Connected to router. IP:', ip)
        return ip
WiFi()
