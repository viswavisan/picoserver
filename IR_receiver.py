
from machine import Timer, Pin,freq
from array import array
from utime import ticks_us, ticks_diff
import time


def print_error(data):
    _errors = {IR_RX.BADSTART : 'Invalid start pulse',
           IR_RX.BADBLOCK : 'Error: bad block',
           IR_RX.BADREP : 'Error: repeat',
           IR_RX.OVERRUN : 'Error: overrun',
           IR_RX.BADDATA : 'Error: invalid data',
           IR_RX.BADADDR : 'Error: invalid address'}
    if data in _errors:print(_errors[data])
    else:print('Unknown error code:', data)

class IR_RX():
    REPEAT = -1
    BADSTART = -2
    BADBLOCK = -3
    BADREP = -4
    OVERRUN = -5
    BADDATA = -6
    BADADDR = -7

    def __init__(self, pin, nedges, tblock, callback, *args):
        self._pin = pin
        self._nedges = nedges
        self._tblock = tblock
        self.callback = callback
        self.args = args
        self._errf = lambda _ : None
        self.verbose = False

        self._times = array('i',  (0 for _ in range(nedges + 1)))  # +1 for overrun
        pin.irq(handler = self._cb_pin, trigger = (Pin.IRQ_FALLING | Pin.IRQ_RISING))
        self.edge = 0
        self.tim = Timer(-1)
        self.cb = self.decode

    def _cb_pin(self, line):
        t = ticks_us()
        if self.edge <= self._nedges:
            if not self.edge:
                self.tim.init(period=self._tblock , mode=Timer.ONE_SHOT, callback=self.cb)
            self._times[self.edge] = t
            self.edge += 1

    def do_callback(self, cmd, addr, ext, thresh=0):
        self.edge = 0
        if cmd >= thresh:
            print(cmd)
            #self.callback(cmd, addr, ext, *self.args)
        else:self._errf(cmd)

    def error_function(self, func):
        self._errf = func

    def close(self):
        self._pin.irq(handler = None)
        self.tim.deinit()

class NEC_ABC(IR_RX):
    def __init__(self, pin, extended, callback, *args):
        super().__init__(pin, 68, 80, callback, *args)
        self._extended = extended
        self._addr = 0

    def decode(self, _):
        try:
            if self.edge > 68:
                raise RuntimeError(self.OVERRUN)
            width = ticks_diff(self._times[1], self._times[0])
            if width < 4000:raise RuntimeError(self.BADSTART)
            width = ticks_diff(self._times[2], self._times[1])
            if width > 3000:
                if self.edge < 68:raise RuntimeError(self.BADBLOCK)
                val = 0
                for edge in range(3, 68 - 2, 2):
                    val >>= 1
                    if ticks_diff(self._times[edge + 1], self._times[edge]) > 1120:val |= 0x80000000
            elif width > 1700:raise RuntimeError(self.REPEAT if self.edge == 4 else self.BADREP)
            else:raise RuntimeError(self.BADSTART)
            addr = val & 0xff
            cmd = (val >> 16) & 0xff
            if cmd != (val >> 24) ^ 0xff:raise RuntimeError(self.BADDATA)
            if addr != ((val >> 8) ^ 0xff) & 0xff:
                if not self._extended:raise RuntimeError(self.BADADDR)
                addr |= val & 0xff00
            self._addr = addr
        except RuntimeError as e:
            cmd = e.args[0]
            addr = self._addr if cmd == self.REPEAT else 0
        self.do_callback(cmd, addr, 0, self.REPEAT)

class NEC_8(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, False, callback, *args)

class NEC_16(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, True, callback, *args)

def callback(data):
    print(data)
    return

pin_ir = Pin(12, Pin.IN)
ir = NEC_8(pin_ir, callback)
ir.error_function(print_error)

try:
    while True:pass
except KeyboardInterrupt:ir.close()