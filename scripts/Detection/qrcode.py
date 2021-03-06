import cv2
import zbar
from PIL import Image
from .figure import FigureStatus
import rospy

class qrCode(FigureStatus):
    def __init__(self, sizeA=70, sizeB=85):
        super(qrCode, self).__init__(sizeA, sizeB)
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')
        self.myName = "Vito Marca Vilte"

    def find_object(self, image):
        gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY, dstCn=0)
        pil = Image.fromarray(gray)
        width, height = pil.size
        raw = pil.tobytes()
        pil = zbar.Image(width, height, 'Y800', raw)
        self.scanner.scan(pil)
        for symbol in pil:
            # check if is my name is in the qrCode
            if symbol.data==self.myName:
                points = symbol.location
                #Draw square detection RED
                for i in xrange(3):
                    cv2.line(image, points[i], points[i+1], (255, 0, 0), 5)
                cv2.line(image, points[3], points[0], (255, 0, 0), 5)
                a = points[2][0]
                c = points[0][0]
                d = points[2][1]
                e = points[0][1]
                x = ((a - c )/2.0) + c
                y = ((d - e)/2.0) + e
                size = a - c
                rospy.loginfo("x:{} y:{} ball w: {} ".format(x, y, size))
                self.update_position_object(x, y, size)
            else:
                self.update_position_object(-1, -1, -1)
        return image
