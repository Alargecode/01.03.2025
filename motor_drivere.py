import signal
import RPi.GPIO as gpio
# import angle_read
import signal
from threading import Thread
from time import sleep
import RPi.GPIO as gpio

# import angle_read

EN = 26
DIR = 19
STEP = 13

CW = 1
CCW = 0


class motor_driver:
    # select
    # 1- sadece 1 adet step motor
    # 2- bi normal(step) 1 açı motoru(step)
    # 3- bir adet dc motor 1 adet açı -(step)
    # soft
    # True = soft start
    # False = no soft start

    def __init__(self, select, soft):
        
        self.soft_time = 1
        self.max_speed = 200
        
        tick = -1
        tick_goal = 0
        pin_state = 0
        gpio.setup(EN, gpio.OUT)
        gpio.setup(DIR, gpio.OUT)
        gpio.setup(STEP, gpio.OUT)
        gpio.output(DIR, CW)

        self.motor_pwm = gpio.PWM(STEP, 100)


    def calculate_ticks(self, distance=60, speed=150, direction=1):
        
            # speed decided in the standard ISO 8295 is 100mm/min
            # travel distance decided by me is 60 mm
            # vida aralığı 2mm
            # 1 tick 1 derece olsa :D
            # 180 tick 1 mm
            # dakikada 100 mm için 18000 tick
            # saniyede 300 tick
            # 0.003 saniyede 1 tick
        mm_per_tick = 180*30  # kalibrasyon için
            # 60mm için 60*180 tick
        ticks = speed * mm_per_tick

        drive_time = (distance / speed) * 60

        frequency = ticks / 90

        frequency = round(frequency, 3)
        return drive_time, frequency, direction

    def motor_run(self, drive_time, frequency, direction):
       
        gpio.output(EN, 0)
        sleep(0.00005)
        gpio.output(DIR, direction)
        sleep(0.000005)
        self.motor_pwm.ChangeFrequency(frequency)
        self.motor_pwm.start(50)
            #            self.motor_pwm.ChangeDutyCycle()
        signal.signal(signal.SIGALRM, self.handler)
        signal.setitimer(signal.ITIMER_REAL, drive_time, 0)


    def motor_start(self, frequency, direction):
        print(frequency)
        gpio.output(EN, 0)
        sleep(0.00005)
        gpio.output(DIR, direction)
        sleep(0.000005)
        frequency = int(frequency)
        self.motor_pwm.ChangeFrequency(frequency)
        self.motor_pwm.start(50)
            
    def handler(self, signum, _):
        self.stop_motor()

    def stop_motor(self):
        
        self.motor_pwm.stop()
        sleep(0.00005)
        gpio.output(EN, 1)

    def send_tick(self, ticks):
        # change it to pin_status != pin_status
        # gpio.input(pin)
        if self.tick > 0:  # countdown the ticks
            self.tick = self.tick - 1
        elif self.tick == -1:  # if tick counter is reset set the counter
            self.tick = ticks
        elif self.tick == 0:
            signal.setitimer(signal.ITIMER_REAL, 0, 0)  # if ticks done stop timer
            self.tick = -1  # reset counter

        pin_state = gpio.input(STEP)
        if pin_state == 1:
            gpio.output(STEP, gpio.LOW)  # output the reverse state to turn motor
        else:
            gpio.output(STEP, gpio.HIGH)
