## Commands

### Initialisation
Initialising drone object with ```Drone IP``` and ```Port``` as arguements. If nothing is given as arguement, the default values defined in ```pluto.py``` are used.
```python
client = Drone("192.168.4.1","23")
```
### Connecting and disconnecting the drone
For connecting the drone, initialise an object of class pluto and call 
```python
client.connect()
```
To disconnect the drone
```python
client.disconnect()
```

### Arming and Disarming the drone
For arming and disarming the drone, use the following functions
```python
client.arm() # arm the drone
```
```python
client.disarm() # disarm the drone
```

### Takeoff and Landing
```python
client.takeoff() # take off
client.land() # land
```

### Flips
To perform a backflip. 
```python
client.flip()
```

### Steering the drone in a particular direction
The drone can be steered in a particular direction by setting the values of throttle, pitch, roll and yaw. ( range of values is from : -600 to 600)
```python
client.roll_speed(100,duration=2)     #A roll of 100 for 2 seconds
client.pitch_speed(100,duration=2)    #A pitch of 100 for 2 seconds
client.throttle_speed(100,duration=2) #A throttle of 100 for 2 seconds
client.yaw_speed(100,duration=2)      #A yaw of 100 for 2 seconds
```

To send all values at once 

```python
# roll,pitch,throttle,yaw of value 100 each for 2 seconds
client.set_all_speed(100,100,100,100,duration=2)

```
To reset the drone commands to the intial values, call
```python
client.reset_speed()
```

### Setting Trim
To balance the drift in drone at central values of ```Roll, Pitch,Throttle, Yaw```, the trim function
```python
client.trim(5,-5,0,0)
```
The argument format is
```
(roll, pitch, throttle, yaw)
```
The sign of values should be opposite to which the drift is observed.<br>
For Roll: right hand side -> positive<br>
For Pitch: forward -> positive<br>
For Throttle: upwards  -> positive<br>
For Yaw: Clockwise -> positive

### For receiving data from the drone
To receive data from the drone, the following functions can be called:
```python
client.get_height()     #Returns height of the drone
client.get_vario()      #Returns the rate of change of height
client.get_roll()       #Returns the value of roll of the drone
client.get_pitch()      #Returns the value of pitch of the drone
client.get_yaw()        #Returns the value of yaw of the drone
client.acc_x()          #Returns the value of accelerometer(x-axis) of the drone
client.acc_y()          #Returns the value of accelerometer(y-axis) of the drone
client.acc_z()          #Returns the value of accelerometer(z-axis) of the drone
client.get_gyro_x()     #Returns the value of gyrometer(x-axis) of the drone
client.get_gyro_y()     #Returns the value of gyrometer(y-axis) of the drone
client.get_gyro_z()     #Returns the value of gyrometer(z-axis) of the drone
client.get_mag_x()      #Returns the value of magnetometer(x-axis) of the drone
client.get_mag_y()      #Returns the value of magnetometer(y-axis) of the drone
client.get_mag_z()      #Returns the value of magnetometer(z-axis) of the drone
client.get_battery()    #Returns the value of battery of the drone in volts
