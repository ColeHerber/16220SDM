from machine import Pin
import time
import machine

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
pwm = machine.PWM(Pin(0), freq=18000, duty_u16=2000)

while True:
   try:
    pwm.duty_u16(32768)
    time.sleep_ms(100)
    pin.toggle()
   except KeyboardInterrupt:
     break

pin.off()
print("Finished.")
