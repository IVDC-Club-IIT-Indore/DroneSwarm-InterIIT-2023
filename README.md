<div id="top"></div>

# Drone Swarm Python
## Inter-IIT Tech Meet 11.0: Bronze medal winning solution to [Drona Aviation](https://github.com/DronaAviation)'s Pluto Drone Swarm Challenge

Team Members: [Yeeshukant Singh](https://github.com/Yeeshukant), [Kshitij Bhat](https://github.com/KshitijBhat), [Harsh Bardhan](https://github.com/harshahb), [Rohan Jha](https://github.com/rohanjha04), [Sairaj Loke](https://github.com/SairajLoke), [Akshit Raizada](https://github.com/AkshitRaizada), [Omkar Shirgaonkar](https://github.com/BulzEye), [Shivankar Sharma](https://github.com/Shivankar007)

Original Repo: https://github.com/DaemonLab/Drone-Swarm-InterIIT-2023

API for controlling The Pluto 1.2 nano drone

![Pluto1 2-ISO-Front](https://user-images.githubusercontent.com/79806119/214293414-403e11c9-3395-4ed4-a8a5-4aa190e86979.png)

[![](https://img.shields.io/badge/License-GPLv3-blue.svg)]()

<!-- TABLE OF CONTENTS (ADD ONCE SUBTOPICS START COMING TOGETHER)-->


## Table of Contents
 

 <p><a href="#ProjD">1. Project Description</a></p>
 <p><a href="#RepoS">2. Repository Structure</a></p>
 <p><a href="#TechS">3. Tech Stack</a></p>
 <p><a href="#GetSL">4. Getting Started ( Linux / Windows) </a></p>
 
 - <p><a href="#PreR">a. Prerequisite</a></p>
 - <p><a href="#SetU">b. Setting Up </a></p>

	 - Python Env for Linux(Optional)
	- pypluto package in Linux
	- pypluto package in Windows

<p><a href="#Usg">5. Usage</a></p>

-	a. Pre-Programmed Execution
-  b. Camera Feedback Execution
-  c. Keyboard Control
-  d. Manually stopping (killing) the drone


<p><a href="#Video">6. Video</a></p>


 

<!-- PROJECT DESCRIPTION -->
<div id="ProjD"></div>

## 1. Project Description 

*Task 1*: 
Develop a Python wrapper for India's one and only number-one-selling educational nano drone, The Pluto.

*Task 2*: 
Hovering a pluto drone on a particular height using ArUco Tag. 
Set a web camera (which is not included in the kit) on the ceiling.
- A. Get a pose estimation of the drone using ArUco tag on the drone.
- B. Add PID to the script for controlling the droneC
- C. Hover the drone in one position.
- D. Move the drone in rectangular motion (1 x 2 meter)

*Task 3*: 
Pluto Swarming (A second drone will be provided - both the drones should fly
at the same time)
A. Generate one more ArUco tag and place it on the second drone.
B. Initially, Drone2 will be at position0, and drone1 will be at position1. Write
commands to move Drone1 from position1 to position2. When Drone1 reaches
position2, drone2 should follow drone1 and reach position1 automatically.
C. Same way, create a rectangle motion. (1 x 2 meter)
D. Record a video and make the final submission similarly as the previous one.


<p align="right">(<a href="#top">back to top</a>)</p>



<div id="RepoS"></div>


## 2. Repository structure
<pre>
├─ docs
│    ├─ Task1.md
|    ├─ keyboard_control.md
│    └─ Task2.md
│  
├─ pypluto
│    ├─ pypluto
│    │   ├─ Camera
│    │   |   ├─ CAM_CONFIGS_lenovo.py
│    │   |   └─ marker.py
│    │   |
│    │   ├─ Control
│    │   |   └─ PIDmain.py
│    │   | 
│    │   ├─ __init__.py
│    │   ├─ drone.py
│    │   └─ enforce.py
│    │  
│    ├─ kill.py
│    ├─ main.py
│    └─ master.py
│    
├─ PrimusV4-Pluto_1_2-1.hex  
│
└─ requirements.txt

</pre>

<div id="TechS"></div>

## 3. Tech Stack 

- python>=3.7
- numpy==1.17.4
- opencv_contrib_python==4.6.0.66
- setuptools==45.2.0
- matplotlib==3.1.2


<p align="right">(<a href="#top">back to top</a>)</p>



<div id="GetSL"></div>

## 4. Getting Started 

<div id="PreR"></div>

### Prerequisites

<!-- *Put setup instructions here.* -->

The API is tested with the ```PrimusV4-Pluto_1_2-1.hex``` firmware installed on Pluto Drone.
Ensure that git is installed on the system.

If ```pip3``` is not installed, install it using the following command in Terminal

```shell
$ sudo apt update
$ sudo apt install python3-pip
``` 

<div id="PyEnv"></div>

<details open>
<summary> Setting up a Python-Environment (optional) </summary>
<br>


```shell
$ pip install virtualenv
```
Now check your installation
```
$ virtualenv --version
```
Now create a virtual environment inside an appropriate folder, type
this in terminal for specific python-3 version
```
$ virtualenv -p /usr/bin/python3 Drone_Env
```
After this command, a folder named  **Drone_Env**  will be created. 

Now at last we just need to activate it, using the command
```
$ source Drone_Env/bin/activate
```
Now you are in a Drone's Python virtual environment , follow the <a href="#SetU">following cmds</a> for installation of packages

Note:
You can deactivate environment using
```
$ deactivate 
```
</details>


<div id="SetU"></div>

## Setting up pypluto package in Linux

```
$ git clone https://github.com/team53-interiit-11/Drona-Aviation-Team53
$ cd pypluto
```
Install the External Dependencies using the following command 
```
pip install -r requirements.txt
```

<p align="right">(<a href="#top">back to top</a>)</p>


<div id="GetSW"></div>

**Note: For MacOS, follow the same procedure as Linux**

## Setting up pypluto package in Windows
Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) using cmd prompt
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
To install run the following command using cmd prompt
```
python /path/to/get-pip.py
```
 Run the following commands:
```
$ git clone https://github.com/team53-interiit-11/Drona-Aviation-Team53
$ cd pypluto
```

Install the External Dependencies using the following command 
```
pip install -r requirements.txt
```


<p align="right">(<a href="#top">back to top</a>)</p>


<div id="Usg"></div>

### 5. Usage

#### a. Pre-Programmed Execution
<!-- *Explain API cmds here.... might need a more detailed version like (make another section for structure)* -->

Use the ```main.py``` template file for pre-programming the drone movement( without using any external camera) .<br> 

Following is a sample program.
note: you might need to change the trim values depending on your drone.
```python
from pypluto import pluto

if __name__ == '__main__':
	#initializing the drone
	drone=pluto()
	drone.connect()
	drone.disarm()
	
	#drone plan execution
	drone.trim(-2,2,0,0)
	drone.takeoff()
	drone.throttle_speed(0,3)
	
	#closing the execution
	drone.land()
	drone.disarm()

```

For detailed explanation of use of various movement functions, refer to [Task1.md](/docs/Task1.md) <br>

#### b. Camera Feedback Execution

Instructions for controlling the drone using camera setup can be found in the
[Task2.md](/docs/Task2.md)


#### c. Keyboard Control

User can also control the drone from keyboard by running the ```keyboard.py``` file in terminal/command prompt. 
Instructions for control via keyboard can be found in [keyboard_control.md](/docs/keyboard_control.md)


### d. Manually stopping (killing) the drone

In case the drone does not arm after running ```main.py```, which may happen due to improper disarming of the drone, you can run ```kill.py``` instead of disconnecting the drone to disarm it properly and then run ```main.py``` to get regular operation

<div id="Video"></div>

#### 6. Video

Link to Drive : https://drive.google.com/file/d/1zlupXXNTnhAbURaeVlbYnx64emY9gVFm/view?usp=sharing

Hover Task: 0:00 to 0:32

Control Task: 0:33 to 1:39

<p align="right">(<a href="#top">back to top</a>)</p>

<div id="RoadM"></div>
