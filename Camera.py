import cv2 as cv
import numpy as np

import Publish


class Camera:
    cap: cv.VideoCapture

    def __init__(self):
        self.cap = cv.VideoCapture('evl4.mp4')
        self.last = None

    def take(self):
        ret, img = self.cap.read()

        if ret:
            blur = cv.GaussianBlur(img, (15, 15), 0)
            if self.last is not None:
                gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
                diff = cv.absdiff(gray, self.last)
                mask = cv.inRange(diff, 127, 255)
                blur = cv.bitwise_and(blur, blur, mask=mask)
                self.last = gray

                hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
                lower_blue = np.array([95, 64, 127])
                upper_blue = np.array([130, 255, 255])

                mask = cv.inRange(hsv, lower_blue, upper_blue)

                contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                big_contours = []
                for contour in contours:
                    area = cv.contourArea(contour)
                    if 0 < area < 255:
                        big_contours.append(contour)
                cv.drawContours(img, big_contours, -1, (0, 0, 255), cv.FILLED)

                return img
            else:
                self.last = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

                return img

        return None


if __name__ == "__main__":
    cam = Camera()
    publisher = Publish.Publisher()

    imgs = []
    wr = cv.VideoWriter('blue3.mp4', cv.VideoWriter_fourcc('m', 'p', '4', 'v'), 15,
                        (int(cam.cap.get(3)), int(cam.cap.get(4))))
    while True:
        img = cam.take()
        publisher.send_on() # for testing
        if img is None:
            continue#break
        wr.write(img)
        cv.imshow("blue", cam.take())
        #publisher.send_on()  # or send_off

        k = cv.waitKey(5)
        if k == 27:
            break
    input()
    wr.release()
