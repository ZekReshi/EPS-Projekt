from typing import Dict, List
import cv2 as cv
import numpy as np

import Publish


class Camera:
    cap: cv.VideoCapture
    lights: Dict[int, List]

    def __init__(self):
        self.cap = cv.VideoCapture('evl4.mp4')
        self.last = None
        self.processed_image = None
        self.lights = {}
        for i in range(10):
            self.lights[i] = []

    def process_picture(self):
        ret, self.img = self.cap.read()

        if ret:
            for i in range(9):
                self.lights[9 - i] = self.lights[8 - i]

            blur = cv.GaussianBlur(self.img, (15, 15), 0)
            if self.last is not None:
                gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
                diff = cv.absdiff(gray, self.last)
                mask = cv.inRange(diff, 127, 255)
                blur = cv.bitwise_and(blur, blur, mask=mask)
                self.processed_image = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
                self.last = gray
            else:
                self.last = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

        return None

    def detect_blue_lights(self):
        self.process_picture()

        if self.processed_image is None:
            return None

        lower_blue = np.array([95, 64, 127])
        upper_blue = np.array([130, 255, 255])

        mask = cv.inRange(self.processed_image, lower_blue, upper_blue)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour_positions = []
        for contour in contours:
            area = cv.contourArea(contour)
            if 0 < area < 255:
                M = cv.moments(contour)
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                contour_positions.append((x, y))
        self.lights[0] = contour_positions

        for i in range(10):
            positions = self.lights[i]
            for position in positions:
                cv.circle(self.img, position, 10, (0, 0, 255), cv.FILLED)

        return self.img


if __name__ == "__main__":
    cam = Camera()
    publisher = Publish.Publisher()

    imgs = []
    wr = cv.VideoWriter('blue3.mp4', cv.VideoWriter_fourcc('m', 'p', '4', 'v'), 15,
                        (int(cam.cap.get(3)), int(cam.cap.get(4))))
    while True:
        img = cam.detect_blue_lights()
        publisher.send_on() # for testing
        if img is None:
            continue#break
        wr.write(img)
        cv.imshow("blue", img)
        #publisher.send_on()  # or send_off

        k = cv.waitKey(5)
        if k == 27:
            break
    input()
    wr.release()
