from time import sleep
import serial
from numpy import sign
from inventorhatmini import InventorHATMini, MOTOR_A, MOTOR_B, SERVO_1, SERVO_2, SERVO_3, SERVO_4
from ioexpander.servo import Servo



class Brain:
    def __init__(self, motorC = False, motorD = False, motor_gear_ratio=16):
        """INPUTS:
                motorC: wether or not to create a motor using servo pins 1 & 2
                motorD: wether or not to create a motor using servo pins 3 & 4"""
         
        self.board = InventorHATMini(init_leds=False, init_servos = (motorC or motorD),motor_gear_ratio=16)
        self.board.enable_motors()

        self.motorA = self.board.motors[MOTOR_A]
        self.motorB = self.board.motors[MOTOR_B]
    #REALLY FUN SERVO SHIT
        if (motorD & motorC):
            #create motor value, and enable 2x
            self.motorC = self.board.motor_from_servo_pins(SERVO_1, SERVO_2)
            self.motorC.enable()

            self.motorD = self.board.motor_from_servo_pins(SERVO_3, SERVO_4)
            self.motorD.enable()

        elif(motorC):
            self.motorC = self.board.motor_from_servo_pins(SERVO_1, SERVO_2)
            #create a motor on servo pins 1 and 2

            self.motorC.enable()

            self.motorD = False
            #set other motor to not exist for shutdown

            self.servo3 = Servo(self.ioe, self.IOE_SERVO_PINS[2])
            self.servo4 = Servo(self.ioe, self.IOE_SERVO_PINS[3])
            #turn the leftover pins into servos

            self.servo3.enable()
            self.servo4.enable()
        elif (motorD):
            self.motorD = self.board.motor_from_servo_pins(SERVO_3, SERVO_4)
            #create a motor on servo pins 3 and 4
            self.motorD.enable()

            self.motorC = False
            #set other motor to not exist for shutdown

            self.servo1 = Servo(self.ioe, self.IOE_SERVO_PINS[0])
            self.servo2 = Servo(self.ioe, self.IOE_SERVO_PINS[1])
            #turn the leftover pins into servos

            self.servo1.enable()
            self.servo2.enable()
            #enable the servos

        else:
            self.servos = [Servo(self.ioe, self.IOE_SERVO_PINS[i]) for i in range(4)]
            [self.servo1,self.servo3,self.servo2,self.servo4] = self.servos
            for s in self.servos:
                s.enable()
                self.motorD = False
                self.motorC = False

    
        sleep(0.5)

        self.ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

        sleep(0.5)

    def drive(self, motor, speed, stop = True):
        """INPUTS:
                motor: 0 or 1, specifies drive motor.
                speed: -100 <= speed <= 100. 100 is full forwards, -100 is full reverse.
                stop: only looked at if speed = 0. Specifies Brake vs coast.
            OUTPUTS:
                ERROR if failure and why.
                Sent if success!.
                """
        
        if (motor > 2):
            return "ERROR, only two driver motors(motor 0 and motor 1)"
        
        if speed == 0:
            direction = int(stop)
        else:
            direction = 0 if speed > 0 else 1
            speed = int(abs(speed)/100 * 255)
        
        message = [speed, direction, motor]
        data = bytearray(message)
        written_amount = self.ser.write(data.encode()) # Send the data over UART
        
        print(written_amount)
        print(data)

        return "Sent"


    def shutdown(self):
        self.board.disable_motors()
        self.ser.close()
        if (self.motorC != False): self.motorC.disable() 
        if (self.motorD != False): self.motorD.disable() 


