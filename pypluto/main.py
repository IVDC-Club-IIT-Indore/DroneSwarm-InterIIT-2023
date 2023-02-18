# A sample program to test the drone API
from pypluto import pluto
import time
 
drone1=pluto()
 
drone1.connect()

drone1.trim(-10,10,0,0)
drone1.disarm()

drone1.takeoff()
drone1.throttle_speed(0,4)
drone1.land()

drone1.disarm()

# drone1.keyboard_control()