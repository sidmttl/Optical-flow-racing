import cv2
from LucasKanade import *
import sys

class Controller():
    def __init__(self):
        self.flipImage = True
        self.vc = cv2.VideoCapture(0)
        if not self.vc.isOpened():
            exit(-1)
        
        cv2.namedWindow("Control Window")
        cv2.moveWindow("Control Window", 10,10)
        cv2.namedWindow("Live Camera")
        cv2.moveWindow("Live Camera",10,350)

        self.rval, self.frame = self.capture(self.vc)
        if self.rval:
            self.of = self.InitOpticaFlow(self.frame)
        
        self.sensitivity = 1
        
    def GetInput(self):
        if(not self.rval):
            print("ERROR: Frame retrieval failed(rval == 0)")
            sys.exit(-1)
        self.rval, frame = self.capture(self.vc)

        ### do it
        video_frame = cv2.resize(frame,(400,300),fx=0,fy=0,interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Live Camera", video_frame)
        img, disp_x = self.of.apply(frame)
        img = cv2.resize(img,(400,300),fx=0,fy=0,interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Control Window", img)

        ### key operation
        key = cv2.waitKey(1)
        if key == 27:         # exit on ESC
            print('Closing...')
            exit()
        elif key == ord('s'):   # save
            cv2.imwrite('img_raw.png',frame)
            cv2.imwrite('img_w_flow.png',img)
            print("Saved raw frame as 'img_raw.png' and displayed as 'img_w_flow.png'")
        elif key == ord('f'):   # save
            self.flipImage = not self.flipImage
            print("Flip image: " + {True:"ON", False:"OFF"}.get(self.flipImage))
        print("disp_x",disp_x)
        if(disp_x > 50*self.sensitivity):
            return 1
        elif(disp_x < -50*self.sensitivity):
            return -1
        else:
            return 0

    def __del__(self):
        self.vc.release()
        cv2.destroyWindow("Control Window")
        cv2.destroyWindow("Live Camera")

    def capture(self, vc):
        rval, frame = vc.read()
        if rval and self.flipImage:
            frame = cv2.flip(frame, 1)
        return (rval, frame)
    
    def InitOpticaFlow(self, prevFrame):
        of = CreateOpticalFlow()
        of.set1stFrame(prevFrame)
        return of

    def setSensitivity(self, val):
        self.sensitivity = val