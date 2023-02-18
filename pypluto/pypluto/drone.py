import socket #To form the connection between the drone and the laptop
import time
import math
import sys
from select import select
from .enforce import enforce_types #To wrap the pluto class
if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

MSP_STATUS=101          # out cmd cycletime & errors_count & sensor present & box activation & current setting number
MSP_RAW_IMU=102         # 9 DOF 
MSP_ATTITUDE=108        # 2 angles 1 heading
MSP_ALTITUDE=109        # altitude, variometer
MSP_ANALOG=110          # vbat, powermetersum, rssi if available on RX

MSP_SET_RAW_RC=200      # 8 rc channel
MSP_SET_COMMAND=217     # setting commands 
RETRY_COUNT=3           # no of retries before getting required data


@enforce_types
class pluto:
   
    def __init__(self, DroneIP="192.168.4.1", DronePort=23): #default pluto settings
        self.DRONEIP = DroneIP
        self.DRONEPORT = DronePort
        self.BUFFER_SIZE = 4096
        #Initailizing the values
        self.roll=1500                    
        self.pitch=1500                 
        self.throttle=1500 
        self.yaw=1500                      
        self.aux1=1200
        self.aux2=1000
        self.aux3=1500
        self.aux4=1200
        
        self.buffer_rc=bytearray([])               # rc data that has to be sent continuously 
        self.trim(0,0,0,0) #To stabalize the drone. Initally the trim values are set to 0 and can be changed according to the drift of the drone

    def connect(self):
        '''
        Function to form the connection with thr drone
        '''
        try:
            self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.mySocket.connect((self.DRONEIP, self.DRONEPORT))
            print("pluto connected")
        except:
            print("Cannot connect to pluto, please try again...")

    def disconnect(self):
        '''
        Function to close the connection
        '''
        self.mySocket.close()
        print("pluto disconnected")

    def trim(self,Roll,Pitch,Throttle,Yaw):
        '''
        Function to set the trim values to make the drone stable
        '''
        Roll=max(-100,min(Roll,100))
        Pitch=max(-100,min(Pitch,100))
        Throttle=max(-100,min(Throttle,100))
        Yaw=max(-100,min(Yaw,100))
        #Update the values
        self.roll=1500 + Roll
        self.pitch=1500 + Pitch
        self.throttle=1500 + Throttle
        self.yaw=1500 + Yaw
        
        self.rc=[self.roll, self.pitch, self.throttle, self.yaw, self.aux1, self.aux2, self.aux3, self.aux4]
    
    def create_sendMSPpacket(self, msg_type, msg):
        '''
        Function to compose and send message packets to the drone
        '''
        self.buffer=bytearray([])                   # data to be sent
        headerArray=bytearray([36,77,60])           # header array "$","M","<"
        self.buffer.extend(headerArray)
        msg_len=2*len(msg)
        self.buffer.append(msg_len)
        self.buffer.append(msg_type)
        if(msg_len>0):
          for b in msg:
            LSB=b%256
            MSB=math.floor(b/256)
            self.buffer.append(LSB)
            self.buffer.append(MSB)
        CRCValue=0
        for b in self.buffer[3:]:
            CRCValue=CRCValue^b
        self.buffer.append(CRCValue)
    
        if(msg_type==200):
            self.buffer_rc=self.buffer[:]
            self.sendPacket(self.buffer)
        else:
            self.sendPacket(self.buffer_rc)
            self.sendPacket(self.buffer)

    def arm(self):  
        '''
        Function to arm the drone
        ''' 
        self.rc[2]=1000
        self.rc[-1]=1500
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        time.sleep(1)
       
    def disarm(self):
        '''
        Function to disarm the drone
        '''
        self.rc[2]=1300
        self.rc[-1]=1200
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        time.sleep(1)
       
    def box_arm(self):
        '''
        Function called before takeoff, user does not directly use it
        '''
        self.rc[2]=1500
        self.rc[-1]=1500
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        time.sleep(0.5)
       
    def clamp_rc(self,x:int):
        #Not called by the user
        return max(1000, min(2000,x))

    def roll_speed(self,value,duration=0):
        '''
        Function to set the roll (x-axis movement) to the drone
        '''
        no_of_loops=10*duration 
        self.rc[0]=self.clamp_rc(self.roll + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
           
    def pitch_speed(self,value,duration=0):
        '''
        Function to set the pitch (y-axis movement) to the drone
        ''' 
        no_of_loops=10*duration 
        self.rc[1]=self.clamp_rc(self.pitch + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)

    def throttle_speed(self,value,duration=0): 
        '''
        Function to set the throttle (z-axis movement) to the drone
        '''
        no_of_loops=10*duration 
        self.rc[2]=self.clamp_rc(self.throttle + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
        
    def yaw_speed(self,value,duration=0):
        '''
        Function to set the yaw (rotation about z-axis) to the drone
        '''
        no_of_loops=10*duration 
        self.rc[3]=self.clamp_rc(self.yaw + value)    
       
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)

    def set_all_speed(self,roll,pitch,throttle,yaw,duration=0):
        no_of_loops=10*duration
        self.rc[0]=self.clamp_rc(self.roll + roll)
        self.rc[1]=self.clamp_rc(self.pitch + pitch)
        self.rc[2]=self.clamp_rc(self.throttle + throttle)
        self.rc[3]=self.clamp_rc(self.yaw + yaw)
        while(no_of_loops>0):
         self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
         no_of_loops=no_of_loops-1
         time.sleep(0.1)
        if(duration==0):
            self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)
           
    def reset_speed(self):
        '''
        Function to reset the roll, pitch, throttle, yaw values for the drone
        '''
        self.rc[:4]=[self.roll,self.pitch,self.throttle,self.yaw]
        self.create_sendMSPpacket(MSP_SET_RAW_RC,self.rc)

    def takeoff(self):
        '''
        Function to takeoff the drone 
        '''
        self.box_arm()
        cmd=[1]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.throttle_speed(0,3)
        
    def land(self):
        '''
        Function to land the drone
        '''
        cmd=[2]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.throttle_speed(0,5)
        self.disarm()

    def flip(self):
        '''
        Function for backflip
        '''
        cmd=[3]
        self.create_sendMSPpacket(MSP_SET_COMMAND,cmd)
        self.throttle_speed(0,3)

    def read16(self,arr):
        '''
        Function to unpack the byte array to extract the values
        Will not be used by the user directly
        '''
        if((arr[1]&0x80) ==0):
            return ((arr[1] << 8) + (arr[0]&0xff))             # for positive values 
        else:
            return (-65535 + (arr[1] << 8) + (arr[0]&0xff))    # for negative values

    
    ################################################## MSP_ALTITUDE #############################################################


    def get_height(self):
            '''
            Function to return the value of height from the sensors of the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             i=0
             while(i<len(data) and data[i]!=109 ):
                i+=1
             if(i+3<len(data)):
              return self.read16(data[i+1:i+3])

    def get_vario(self):
            '''
            Function to return the value of rate of change of altitude from the sensors of the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_ALTITUDE,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             i=0
             while(i<len(data) and data[i]!=109 ):
                i+=1
             if(i+7<len(data)):
              return self.read16(data[i+5:i+7])

    
    ###################################################### MSP_ATTITUDE #########################################################


    def get_roll(self):
            '''
            Function to return the value of roll from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=108 ):
                 i+=1
                if(i+3<len(data)):
                 return self.read16(data[i+1:i+3])/10

    def get_pitch(self):
            '''
            Function to return the value of pitch from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=108 ):
                 i+=1
                if(i+5<len(data)):
                 return self.read16(data[i+3:i+5])/10

    def get_yaw(self):
            '''
            Function to return the value of yaw from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_ATTITUDE,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=108 ):
                 i+=1
                if(i+7<len(data)):
                 return self.read16(data[i+5:i+7])


    ###################################################### MSP_RAW_IMU ##########################################################
    

    def get_acc_x(self):
            '''
            Function to return the value of accelerometer(x-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                 i+=1
                if(i+3<len(data)):
                 return self.read16(data[i+1:i+3])

    def get_acc_y(self):
            '''
            Function to return the value of accelerometer(y-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+5<len(data)):
                    return self.read16(data[i+3:i+5])

    def get_acc_z(self):
            '''
            Function to return the value of accelerometer(z-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+7<len(data)):
                    return self.read16(data[i+5:i+7])

    def get_gyro_x(self):
            '''
            Function to return the value of gyrometer(x-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+9<len(data)):
                    return self.read16(data[i+7:i+9])

    def get_gyro_y(self):
            '''
            Function to return the value of gyrometer(y-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+11<len(data)):
                    return self.read16(data[i+9:i+11])

    def get_gyro_z(self):
            '''
            Function to return the value of gyrometer(z-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+13<len(data)):
                    return self.read16(data[i+11:i+13])
    
    def get_mag_x(self):
            '''
            Function to return the value of magnetometer(x-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+15<len(data)):
                    return self.read16(data[i+13:i+15])
    
    def get_mag_y(self):
            '''
            Function to return the value of magnetometer(y-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+17<len(data)):
                    return self.read16(data[i+15:i+17])

    def get_mag_z(self):
            '''
            Function to return the value of magnetometer(z-axis) from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_RAW_IMU,data) 
            for i in range(RETRY_COUNT):
                data=self.recievePacket()
                i=0
                while(i<len(data) and data[i]!=102 ):
                    i+=1
                if(i+19<len(data)):
                    return self.read16(data[i+17:i+19])


###################################################### MSP_ANALOG ###############################################################


    def get_battery(self):
            '''
            Function to return the value of battery in volts from the drone
            '''
            data=[]
            self.create_sendMSPpacket(MSP_ANALOG,data) 
            for i in range(RETRY_COUNT):
             data=self.recievePacket()
             i=0
             while(i<len(data) and data[i]!=110 ):
                i+=1
             if(i+1<len(data)):
              return data[i+1]/10
   

    '''Function to send and recieve data packets'''
    def sendPacket(self,buff):
        self.mySocket.send(buff)

    def recievePacket(self):
       return self.mySocket.recv(self.BUFFER_SIZE)

    
    
###################################################### KEYBOARD_CONTROL #########################################################

    
    def getKey(self,settings):
        """
        Function Name: getKey
        Input: None
        Output: keyboard charecter pressed
        Logic: Determine the keyboard key pressed
        Example call: getkey()
        """
        
        if sys.platform == 'win32':
            # getwch() returns a string on Windows
            key = msvcrt.getwch()
            #print("Key sent from Windows: '", key, "'")
        else:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
                if (key == '\x1b'): # \x1b is Escape key
                    key = sys.stdin.read(2)
                sys.stdin.flush()
            else:
                key = ''

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
            #print("Key sent from Linux: ", key)
        return key
        
    def saveTerminalSettings(self):
        if sys.platform == 'win32':
            return None
        return termios.tcgetattr(sys.stdin)

    def restoreTerminalSettings(self,old_settings):
        if sys.platform == 'win32':
            return termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def indentify_key(self,key_value):

        if key_value == 70:
            if self.armed:
                self.disarm()
                self.armed = False
            else:
                self.arm()
                self.armed = True

        elif key_value == 10:
            #print("Forward key detected")
            self.pitch_speed(100) # forward

        elif key_value == 30:
            #print("Left key detected")
            self.roll_speed(-100) # left

        elif key_value == 40:
            #print("Right key detected")
            self.roll_speed(100) # right

        elif key_value == 80:
            self.reset_speed()

        elif key_value == 50:
            self.throttle_speed(400) # increase height

        elif key_value == 60:
            self.throttle_speed(-200) # decrease_height

        elif key_value == 110:
            #print("Backward key detected")
            self.pitch_speed(-100) # backwards

        elif key_value == 130:
            self.takeoff()

        elif key_value == 140:
            self.land()
        
        elif key_value == 100:
            self.flip()

        elif key_value == 150:
            self.yaw_speed(-300) # yaw left

        elif key_value == 160:
            self.yaw_speed(300) # yaw right
    
        elif key_value == 42: # windows special key
            key2 = msvcrt.getwch()
            #print("Special key detected: ", key2)
            
            # check for windows special key type
            if key2 == 'H': # up arrow
                #print("Forward key detected")
                self.pitch_speed(100) # forward

            elif key2 == 'K': # left arrow
                #print("Left key detected")
                self.roll_speed(-100) # left

            elif key2 == 'M': # right arrow'
                #print("Right key detected")
                self.roll_speed(100) # right

            elif key2 == 'P': # down arrow
                #print("Backward key detected")
                self.pitch_speed(-100)
        
    def keyboard_control(self,stat=False):
        
        self.disarm()
        self.armed = False
        msg="""   
            Control Your Drone!
            ---------------------------
            spacebar : arm or disarm
            w : increase height
            s : decrease height
            q : take off
            e : land
            a : yaw left
            d : yaw right
            Up arrow : go forward
            Down arrow : go backward
            Left arrow : go left
            Right arrow : go right
            CTRL+C to quit
        """
        print(msg)
        self.keyboard_controls={  #dictionary containing the key pressed abd value associated with it
                            '[A': 10, # up arrow fwd pitch
                            '[D': 30, # left arrow left roll
                            '[C': 40, # right arrow right roll
                            'w':50, # increase throttle
                            's':60, # decrease throttle
                            ' ': 70, # arm disarm
                            'r':80, # reset
                            't':90, # autopilot
                            'p':100, #backflip
                            '[B':110, # down arrow bkwd pitch
                            'n':120,
                            'q':130, # take off
                            'e':140, # land
                            'a':150, # left yaw
                            'd':160, # right yaw
                            '+' : 15,
                            '1' : 25,
                            '2' : 30,
                            '3' : 35,
                            '4' : 45,
                            # Windows arrow key 
                            'à': 42
                            # 'àH': 10, # up arrow fwd pitch (Windows)
                            # 'àK': 30, # left arrow left roll (Windows)
                            # 'àM': 40, # right arrow right roll (Windows)
                            # 'àP': 110 # down arrow bkwd pitch (Windows)
                            }

        self.win_arrowkey = False

        self.settings = self.saveTerminalSettings()   
        try:
            while(True):
                if(stat):
                    print("Roll :",self.get_roll(), "Pitch :",self.get_pitch(), "Yaw :",self.get_yaw(), "Battery :",self.get_battery())
                key = self.getKey(self.settings)
                if key in self.keyboard_controls.keys():
                    #print("executed" , self.keyboard_controls[key] , "]]]")
                    self.indentify_key(self.keyboard_controls[key])

                else:
                    self.reset_speed()
                    #print("Other key: ", key)
                    if (key == '\x03'):
                        #print("Ctrl+C detected")
                        self.disarm() # Ctrl+C break
                        break

        except Exception as e:
            print(e)

        finally:
            print(key)
            self.restoreTerminalSettings(self.settings)

