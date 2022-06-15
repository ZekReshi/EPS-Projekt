from logging import lastResort
import time
from typing import Dict, List, Tuple
import cv2 as cv
import numpy as np

import Publish


class Camera:
    cap: cv.VideoCapture
    lights: Dict[int, List[Tuple[int, int]]]
    filtered_lights: List[Tuple[int, int]]
    found: bool

    def __init__(self):
        self.cap = cv.VideoCapture('evl4.mp4')
        self.last = None
        self.processed_image = None
        self.lights = {}
        self.filtered_lights = []
        self.found = False
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
        if self.processed_image is None:
            return None

        lower_blue = np.array([95, 64, 127])
        upper_blue = np.array([130, 255, 255])

        mask = cv.inRange(self.processed_image, lower_blue, upper_blue)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 20:
            return
        contour_positions = []
        for contour in contours:
            area = cv.contourArea(contour)
            if 0 < area < 255:
                M = cv.moments(contour)
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                contour_positions.append((x, y))
        self.lights[0] = contour_positions

    def filter_blue_lights(self):
        self.filtered_lights = []
        for light in self.lights[0]:
            appended = False
            for i in range(9):
                for position in self.lights[i + 1]:
                    if light[0] * position[0] + light[1] * position[1] < 1000000:
                        self.filtered_lights.append(light)
                        appended = True
                        break
                if appended:
                    break

    def get_blue_lights_image(self):
        self.process_frame()

        if self.found:
            for i in range(10):
                for light in self.filtered_lights:
                    cv.circle(self.img, light, 10, (0, 0, 255), cv.FILLED)

        return self.img

    def process_frame(self):
        self.process_picture()
        self.detect_blue_lights()
        self.filter_blue_lights()

        self.found = len(self.filtered_lights) > 0


if __name__ == "__main__":
    cam = Camera()
    publisher = Publish.Publisher()
    points = 0
    on = False
    imgs = []
    last_sent = time.time()
    wr = cv.VideoWriter('blue4.mp4', cv.VideoWriter_fourcc('m', 'p', '4', 'v'), 15,
                        (int(cam.cap.get(3)), int(cam.cap.get(4))))
    while True:
        img = cam.get_blue_lights_image()

        if cam.found:
            if points < 10:
                points += 5
                if points >= 10:
                    if not on:
                        last_sent = time.time()
                        print("ON")
                        publisher.send(not on)
                    on = True
        else:
            if points > 0:
                points -= 1
                if points == 0:
                    on = False

        t = time.time()
        if t - last_sent >= 1:
            publisher.send(on)
            last_sent = t
            print(on)

        if img is None:
            continue #break
        wr.write(img)
        cv.imshow("blue", img)

        k = cv.waitKey(5)
        if k == 27:
            break
    input()
    wr.release()
