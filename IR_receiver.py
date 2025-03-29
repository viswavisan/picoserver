
from machine import Timer, Pin
from array import array
from utime import ticks_us, ticks_diff


class IR_RX():

    def __init__(self):
        self._pin = Pin(12, Pin.IN)
        self._nedges = 28
        self._tblock = 30
        self._errf = lambda _ : None
        self.verbose = False

        self._times = array('i',  (0 for _ in range(self._nedges + 1))) 
        self._pin.irq(handler = self._cb_pin, trigger = (Pin.IRQ_FALLING | Pin.IRQ_RISING))
        self.edge = 0
        self.tim = Timer(-1)
        self.cb = self.decode

    def _cb_pin(self, line):
        t = ticks_us()
        if self.edge <= self._nedges:
            if not self.edge: self.tim.init(period=self._tblock , mode=Timer.ONE_SHOT, callback=self.cb)
            self._times[self.edge] = t
            self.edge += 1

    def close(self):
        self._pin.irq(handler = None)
        self.tim.deinit()

    def decode(self, _):
        try:
            nedges = self.edge
            print(nedges)
            if not 14 <= nedges <= 28:raise RuntimeError(-5 if nedges > 28 else -2)
            bits,bit,v,x = 1,1,1,0
            while bits < 14:
                if x > nedges - 2:raise RuntimeError(-4)
                width = ticks_diff(self._times[x + 1], self._times[x])
                print(width)
                if not 500 < width < 3500:
                    self.verbose and print('Bad block 3 Width', width, 'x', x)
                    raise RuntimeError(-3)
                short = width < 1334
                if not short:bit ^= 1
                v <<= 1
                v |= bit
                bits += 1
                x += 1 + int(short)
            self.verbose and print(bin(v))

            val = (v & 0x3f) | (0 if ((v >> 12) & 1) else 0x40)
            addr = (v >> 6) & 0x1f
            ctrl = (v >> 11) & 1

        except RuntimeError as e:val, addr, ctrl = e.args[0], 0, 0

        #do actions
        self.edge = 0
        if val>=0:
            print(val, addr, ctrl)
        else: print('error',val)
        

ir=IR_RX()

try:
    while True:pass
except KeyboardInterrupt:ir.close()