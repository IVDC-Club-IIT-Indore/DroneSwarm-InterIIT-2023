# Task 2

## Camera calibration
The camera used the task 2 is Lenovo 300 FHD Webcam with FHD 1080P 2.1 Megapixel CMOS Camera and an Ultra-Wide 95 Lens.
- To calibrate the camera, first print a checkerboard and paste it on a piece of cardboard/wood.
- Then, run ```pics.py``` to click a few images of the board in different angles(around 30). Press 'c' to click the photo and 'q' to end the program when done.
- Now, update the rows and columns in ```camera.py``` according to the size of the board.
- **Do not include the outermost lines when counting the rows and columns.** <br>
- Now, make appropiate changes in path of the image folder(if any) in ```camera.py``` and run the code.
- It will return a JSON file containing the camera matrix and the distortion coefficients.
- Use those matrices in ```marker.py``` in Camera directory.

## Pose Estimation
The pose of the drone is obtained from the Aruco marker attached on the drone. The cv2.aruco library, available in the opencv-contrib-python package, is used to detect the drone and its pose, specifically it's x-y coordinates in pixels, height in meters and yaw in radians.



## PID control

<p align="center">
  <img src="https://user-images.githubusercontent.com/85498394/214069904-bb4d0453-a588-4788-a607-307372c79802.jpg" alt="Task 2"/>
</p>


## Running

To run the PID control task, run ``master.py`` which will further start two parallel processes for pose estimation and PID control.
