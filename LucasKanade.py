import numpy as np
import cv2

class LucasKanadeOpticalFlow():
    def __init__(self):
        # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 100,
                                    qualityLevel = 0.3,
                                    minDistance = 7,
                                    blockSize = 7 )

        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                               maxLevel = 2,
                               criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # some random colors for aesthetics
        self.color = np.random.randint(0,255,(100,3))

    def set1stFrame(self, frame):
        self.old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask = None, **self.feature_params)
        #mask image for drawing purposes
        self.mask = np.zeros_like(frame)
        self.sum_x = 0

    def apply(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, frame_gray,
                                               self.p0, None, **self.lk_params)

        #Select good points
        good_new = p1[st==1]
        good_old = self.p0[st==1]

        #variable to store average x displacement of Good Points
        temp_x = 0

        #draw the tracks
        for i, (new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            temp_x += a-c
            self.mask = cv2.line(self.mask, (a,b), (c,d), self.color[i].tolist(), 2)
            frame = cv2.circle(frame, (a,b), 5, self.color[i].tolist(), -1)
        img = cv2.add(frame, self.mask)

        #calculate average x displacement from initial
        temp_x/= p1.shape[0]
        self.sum_x += temp_x

        print("sum_x = ", self.sum_x)

        #update the previous frame and previous points
        self.old_gray = frame_gray.copy()
        self.p0 = good_new.reshape(-1,1,2)

        return img


def CreateOpticalFlow():
    return LucasKanadeOpticalFlow()
    
