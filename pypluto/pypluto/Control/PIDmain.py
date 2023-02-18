from multiprocessing import Pipe
from pypluto.drone import pluto
import numpy as np
import time

#Target coords
target_array = [
    [375, 162],
    [538, 160],
    [652, 158],
    [788, 152],
    [882, 175],
    [920, 240],
    [922, 332],
    [886, 402],
    [776, 422],
    [632, 428],
    [486, 432],
    [402, 412],
    [365, 355],
    [364, 248],
    [375, 162],
]

# xTarget,  yTarget, heightTarget = 646, 348, 0.8 # for hover at point

target_array2=[]
target_array2.append(target_array[0])
x_target,  y_target, height_target = target_array[0][0],target_array[0][1], 0.8  #pixel, pixel , height(m)

Drone1=pluto()

Drone1.connect()

drone=Drone1

#pid gains

KPx, KPy, KPz, KPyaw = 0.8, 0.4, 380 , 50
KIx, KIy, KIz, KIyaw = 0.02, 0.01, 0, 0
KDx, KDy, KDz, KDyaw = 18, 25, 10, 0


#currently global , 
#for deciding drone's final yaw orientation 
YAW_TARGET = 1.5708

def pid(pose, target, Err, ErrI):
    """
    PID Control Loop
    """
    x_error, y_error, z_error, yaw_error = Err
    x_errorI, y_errorI, z_errorI, yaw_errorI = ErrI

    x_target, y_target, height_target = target



    x_error_old = x_error
    y_error_old = y_error
    z_error_old = z_error
    yaw_error_old = yaw_error

    x,   y,   z,   yaw = pose

    x_error = x_target-x
    y_error = y_target-y
    z_error = height_target-z
    yaw_error = YAW_TARGET-yaw


    x_errorI += x_error
    y_errorI += y_error
    z_errorI += z_error
    yaw_errorI += yaw_error

    # compute derivative (variation) of errors (D)
    x_errorD = x_error-x_error_old
    y_errorD = y_error-y_error_old
    z_errorD = z_error-z_error_old
    yaw_errorD = yaw_error-yaw_error_old

    # compute commands
    xCommand = KPx*x_error + KIx*x_errorI + KDx*x_errorD
    yCommand = KPy*y_error + KIy*y_errorI + KDy*y_errorD
    zCommand = KPz*z_error + KIz*z_errorI + KDz*z_errorD

    yaw_command    = int( KPyaw*yaw_error + KIyaw*yaw_errorI + KDyaw*yaw_errorD)
    pitch_command = int( np.cos(yaw)*xCommand + np.sin(yaw)*yCommand)
    roll_command  = int( -np.sin(yaw)*xCommand + np.cos(yaw)*yCommand ) 
    throttle_command = int(zCommand)
    Err = [x_error, y_error, z_error, yaw_error]
    ErrI = [x_errorI, y_errorI, z_errorI, yaw_errorI]
    
    return roll_command, pitch_command, throttle_command, yaw_command, Err, ErrI


def PID_main(conn):
    """
    Function to recieve data from pid file and 
    using drone_api velocity fns 
    we can send the cmd to drone from here 
    as soon as we recieve them
    """
    global x_target,  y_target, height_target, drone
    

    # initialize PID controller
    x_error, y_error, z_error, yaw_error = 0, 0, 0, 0
    x_errorI, y_errorI, z_errorI, yaw_errorI = 0, 0, 0, 0
    x_errorD, y_errorD, z_errorD, yaw_errorD = 0, 0, 0, 0
    x_error_old, y_error_old, z_error_old, yaw_error_old = 0, 0, 0, 0

    Err = [x_error, y_error, z_error, yaw_error]
    ErrI = [x_errorI, y_errorI, z_errorI, yaw_errorI]
    path = [[0,0,0,0]]
    
    #Drone1.trim(-8,20,0,0) # iit
    Drone1.trim(23, 5,0,0)
    Drone1.disarm()
    # Drone2.disarm
    # drone.arm()
    Drone1.arm()
    # Drone2.arm()
    Drone1.throttle_speed(300,2)
    # Drone2.throttle_speed(50,1)
    # Drone1.takeoff()
    print("takeoff")

    tReachCount=0
    # default values when not detected
    roll_command, pitch_command, throttle_command, yaw_command = 0, 0, 50, 0

    start = time.time()
    target = 0

    roll_log = []
    pitch_log = []

    while True:


        try:
            pose_dict = None

            if (conn.poll()):                
                pose_dict = conn.recv()
                
            
            if not pose_dict:
                
                now_time = time.time()
                timeout_limit = now_time - start 

                roll_command, pitch_command, throttle_command, yaw_command = 0, 0, 50, 0

                if timeout_limit > 8 : 
                    print("Aruco not detected ,landing")
                    drone.land()
                    break
                
          
            elif (not pose_dict)==False:
                if drone==Drone1:
                    try:
                        pose=pose_dict['0']
                    except KeyError:
                        pass

                start = time.time()
                roll_command, pitch_command, throttle_command, yaw_command, Err, ErrI = pid(pose, [x_target,  y_target, height_target], Err, ErrI)
                
                # Clipping commands
                if (roll_command>100):
                    roll_command=100
                elif (roll_command<-100):
                    roll_command=-100
                if (pitch_command>70):
                    pitch_command=70
                elif (pitch_command<-70):
                    pitch_command=-70

                if np.sqrt((x_target-pose[0])**2+(y_target-pose[1])**2)<25:
                    # print(f"Pose: {pose}")
                    print("Target Reached.")
                    drone.reset_speed()
                    tReachCount += 1
                    if tReachCount>=5:
                        target += 1
                        if target==15:
                            print("Task Completed\nLanding")
                            break
                        x_target,  y_target = target_array[target]
                        tReachCount=0

   
            # Set all speeds at once
            drone.set_all_speed(roll_command, pitch_command, throttle_command, yaw_command)
            

            time.sleep(0.04)
       
            '''this sleep adjusts the running of this files while loop, 
            so that the rate of receiving from marker files is almost matched 
            to that of this file sending commands to drone using api '''
            
            
            if not roll_command==0:
                print(f"\nFrequecy checker(sending) , rcmd: {roll_command}, pcmd: {pitch_command}, tcmd:{throttle_command},  yawcmd:{yaw_command}")

        except KeyboardInterrupt:
            break



    Drone1.land()
    Drone1.disarm()
   
