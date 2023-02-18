import cv2
from datetime import datetime
from imutils.video import VideoStream
import time

vs = VideoStream(src=2).start()
time.sleep(2.0)

while(True):
    frame = vs.read()

    cv2.imshow('frame',frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        cv2.imwrite(f"calibrate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", frame)

vs.stop()
cv2.destroyAllWindows()