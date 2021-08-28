import numpy as np
import cv2


# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

capFlag = 1

# Open both cameras
if capFlag:
    cap_right = cv2.VideoCapture(0, cv2.CAP_DSHOW)                    
    cap_left =  cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not(cap_right.isOpened() and cap_left.isOpened()):
        exit()
else:
    path = "img/stereo_calibration/"
    fname = "1/frame1_1629687726.jpg"
    fname2 = "2/frame2_1629687726.jpg"
    cap_right = cv2.imread(path + fname2)
    cap_left = cv2.imread(path + fname)


while(1):

    if capFlag:
        succes_right, frame_right = cap_right.read()
        succes_left, frame_left = cap_left.read()
    else:
        frame_right = cap_right
        frame_left = cap_left

    # Undistort and rectify images
    frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                     
    # Show the frames
    cv2.imshow("frame right", frame_right) 
    cv2.imshow("frame left", frame_left)


    # Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()