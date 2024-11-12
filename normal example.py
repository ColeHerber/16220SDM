from brain import Brain
from time import sleep
##############################################
# SETUP
##############################################

brain = Brain()

servos = brain.servos

servo1 = brain.servo1
servo2 = brain.servo1
servo3 = brain.servo1
servo4 = brain.servo1

motorA = brain.motorA
motorB = brain.motorB

##############################################
# INDIVIDUAL CALLS EXAMPLES
##############################################

motorA.full_positive()
motorB.full_positive()

servo1.max()
servo2.max()
servo3.max()
servo4.max()

sleep(1)

motorA.stop()
motorB.stop()

input("Try to move the small motors really quick,press enter when your hands are away")


motorA.full_negative()
motorB.full_negative()

servo1.min()
servo2.min()
servo3.min()
servo4.min()
    
sleep(2)

motorA.coast()
motorB.coast()

input("Try to move the small motors again really quick,press enter when your hands are away")

##############################################
# RAMP EXAMPLES
##############################################

for s in servos:
    s.mid()

for i in range(0,-100,-1):
    motorA.speed(i)
    motorB.speed(i)
    sleep(0.1)

for i in range(-100,100):
    motorA.speed(i)
    motorB.speed(i)
    for s in servos:
        s.to_percent(i)
    sleep(0.1)


##############################################
# Drive EXAMPLES
##############################################
input("""MAKE SURE YOUR DRIVETRIAN IS OFF THE GROUND \n,
      CHECK THE DIRECTIONS THEY SPIN FOR YOUR OWN CODE, BOTH are spinning forwards""")
brain.drive(0,50)
brain.drive(1,50)
sleep(5)

#both should be braked, by default will brake when speed is 0
brain.drive(0,0, stop=True)
brain.drive(1,0)

input("Feel the drive train motors now, press enter when your hands are away")

brain.drive(0,-100)
brain.drive(1,-100)
sleep(3)

for i in range(0,-100):
    brain.drive(0,i)

for i in range(-100,100):
    brain.drive(0,i)
