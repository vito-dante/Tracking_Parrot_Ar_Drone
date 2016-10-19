import cv2
from .figure import FigureStatus

# Color space
# The values below were obtained using ImageJ (image-> adjust-> threshold)
MIN_H = 22
MAX_H = 71
MIN_S = 43
MAX_S = 204
MIN_V = 97
MAX_V = 203

class Ball(FigureStatus):

    def __init__(self):
        super(Ball, self).__init__()
        self.greenLower = (29, 86, 6)
        self.greenUpper = (64, 255, 255)

    def segmentaObjetosColorRoi(self):
        cv2.GaussianBlur(self.cv_image, (11, 11), 0)
        hsv = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        cv2.dilate(mask, None, iterations=2)

    # analyzes the image related components
    def detectaObjetoMasRedondo(self):

        cnts = cv2.findContours(self.mask.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            m00 = M["m00"]
            x = int(M['m10'] / m00)
            y = int(M['m01'] / m00)
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(self.frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                self.actualizarSituacion(x, y, 5)
            cv2.circle(self.frame, center, 5, (0, 0, 255), -1)
            return self.frame
        else:
            self.actualizarSituacion(-1, -1, -1)


    def findObject(self, image):
        # self.ToOpenCV(image)
        self.cv_image = image
        self.segmentaObjetosColorRoi()
        self.detectaObjetoMasRedondo()
        return self.frame
