import cv2
import numpy as np

CAMERA_HEIGHT = 1.9 

Aruco_ref_dist = 2.2 # may be same as camera ht if we use it as a reference
Aruco_ht_pixels_grnd =15 #ht in pixels when aruco on ground( reference dist)
Aruco_width_pixels_grnd = 15 #wdth in pixels when aruco on ground( reference dist)
Aruco_len_pixels_grnd = 15

#matrix_coefficients - Intrinsic matrix of the calibrated camera
MATRIX_COEFFICIENTS = np.array([[
            1447.9804004365824,
            0.0,
            617.3063266183908
        ],
        [
            0.0,
            1448.4116664252433,
            289.02239681156016
        ],
        [
            0.0,
            0.0,
            1.0
        ]])

#distortion_coefficients - Distortion coefficients associated with our camera
DISTORTION_COEFFICIENTS = np.array([
            0.0397515407032859,
            1.259291585298002,
            -0.010631456171277863,
            -0.00784841820297665,
            -5.925444820936321
        ])
    
class Aruco:

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.                    DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    def __init__(self, arucoType):
        self.arucoType = arucoType
        self.arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT[self.arucoType])
        self.arucoParams = cv2.aruco.DetectorParameters_create()

    def detectMarkers(self,img):
        
        return cv2.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)

    def get_pose(self, corners, ids, image, desiredVec, display=True):

        is_detected = False
        pose = None

        
        if len(corners) > 0:
            
            for (markerCorner, markerID) in zip(corners, ids):

                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(np.array(corners), 0.02, cameraMatrix=MATRIX_COEFFICIENTS, distCoeffs=DISTORTION_COEFFICIENTS)

                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                topRight = np.array([int(topRight[0]), int(topRight[1])])
                bottomRight = np.array([int(bottomRight[0]), int(bottomRight[1])])
                bottomLeft = np.array([int(bottomLeft[0]), int(bottomLeft[1])])
                topLeft = np.array([int(topLeft[0]), int(topLeft[1])])

                #-----------------------------------for drone ht calc

                deltax1 = topRight[0]- bottomRight[0]
                deltay1 = topRight[1]- bottomRight[1]
                len1 = np.sqrt( np.power(deltax1,2) + np.power(deltay1,2)  )
                dist_l1 = Aruco_ref_dist*(1-(Aruco_len_pixels_grnd/ len1))
                dist_l1 = round(dist_l1 , 3)

                deltax2 = topLeft[0]- bottomLeft[0]
                deltay2 = topLeft[1]- bottomLeft[1]
                len2 = np.sqrt( np.power(deltax2,2) + np.power(deltay2,2)  )
                dist_l2 = Aruco_ref_dist*(1-(Aruco_len_pixels_grnd/ len2))
                dist_l2 = round(dist_l2 , 3)


                deltax3 = topRight[0]- topLeft[0]
                deltay3 = topRight[1]- topLeft[1]
                width1 = np.sqrt( np.power(deltax3,2) + np.power(deltay3,2)  )
                dist_w1 = Aruco_ref_dist*(1-(Aruco_width_pixels_grnd/ width1))
                dist_w1 = round(dist_w1 , 3)

                deltax4 = bottomRight[0]- bottomLeft[0]
                deltay4 = bottomRight[1]- bottomLeft[1]
                width2 = np.sqrt( np.power(deltax4,2) + np.power(deltay4,2)  )
                dist_w2 = Aruco_ref_dist*(1-(Aruco_width_pixels_grnd/ width2))
                dist_w2 = round(dist_w2 , 3)


                distmax = round( max( max(dist_l1 , dist_l2 ) , max( dist_w1 , dist_w2) ) ,3  )

                if distmax < 0 :
                    distmax = 0 
                #------------------------------------
                
 
                cX, cY = (topLeft + bottomRight)//2
                hX, hY = (topLeft + topRight)//2
                tX, tY = hX-cX, hY-cY
                yaw = np.arctan2(tY, tX) 


                    
                drone_height = CAMERA_HEIGHT - tvec[0,0,2]

                pose = np.array([cX,cY, drone_height,yaw]) 
                is_detected = True
                if display:
                    cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                    

                    cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                    
                    cv2.arrowedLine(image, (cX,cY), (hX,hY),(0, 0, 255))

                    cv2.putText(image , f"distmax:{distmax}  ",
                    (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            
        if display:
            for i in range(len(desiredVec[0])):

                dX,dY = desiredVec[0][i]
                cv2.circle(image, (dX, dY), 7, (255, 0, 0), -1)

            cv2.imshow("Image", image)        

                
        return pose, is_detected, image, 



def marker_publisher(connCam):  #connCam

    cameraID = 2 # your camera id on pc
    target_array = [
    [375, 162],
    [538, 160],
    [652, 158],
    [788, 152],
    [914, 149],
    [920, 240],
    [922, 332],
    [921, 422],
    [776, 422],
    [632, 428],
    [486, 432],
    [365, 432],
    [365, 355],
    [364, 248],
    [375, 162],
]

    cap = cv2.VideoCapture(cameraID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    aruco_obj = Aruco("DICT_4X4_50")

    while cap.isOpened(): 

        ret, image = cap.read()               
        
        #Aruco Detection , pose Estimation Block

        pose_dict={}
        corners, ids, rejected = aruco_obj.detectMarkers(image)
 
        if len(corners)>0:
            for i in range(0,len(ids)):
                pose, is_detected, detected_markers  = aruco_obj.get_pose(corners[i], ids, image, [target_array], display=True)
                cv2.imshow("Image", detected_markers)
                pose_dict[str(ids[i][0])]=pose

        else:
            for i in range(len(target_array)):

                dX,dY = target_array[i]
                cv2.circle(image, (dX, dY), 7, (255, 0, 0), -1)

            cv2.imshow("Image", image)
        
        connCam.send(pose_dict)



        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    marker_publisher(connCam='')
