import numpy as np
import cv2 as cv
import glob
import json
from datetime import datetime

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

rows = 9
columns = 7
objp = np.zeros((rows*columns,3), np.float32)
objp[:,:2] = np.mgrid[0:columns,0:rows].T.reshape(-1,2)

objpoints = []
imgpoints = []

images = glob.glob('calibrate*.png')
print(len(images), "images found")

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    chessboard_flags = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE
    ret, corners = cv.findChessboardCorners(gray, (columns,rows), chessboard_flags)

    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        cv.drawChessboardCorners(img, (columns,rows), corners2, ret)
        cv.imshow('img', img)
        cv.imwrite(f"chessboard_corners_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", img)
        cv.waitKey(1500)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

camera = {}

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

for variable in ['ret', 'mtx', 'dist', 'rvecs', 'tvecs']:
    camera[variable] = eval(variable)

with open("camera.json", 'w') as f:
    json.dump(camera, f, indent=4, cls=NumpyEncoder)

cv.destroyAllWindows()