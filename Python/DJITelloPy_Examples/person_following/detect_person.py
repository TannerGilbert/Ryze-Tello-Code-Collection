import cv2
import argparse
import time
import numpy as np


class detectPerson:

    def __init__(self):
        self.detector = cv2.dnn.readNetFromCaffe(
            'MobileNetSSD_deploy.prototxt', 'MobileNetSSD_deploy.caffemodel')

    def detectSingle(self, image):
        (h, w) = image.shape[:2]
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        self.detector.setInput(imageBlob)
        detections = self.detector.forward()

        if len(detections) > 0:
            i = np.argmax(detections[0, 0, :, 2])
            label = detections[0, 0, i, 1]
            confidence = detections[0, 0, i, 2]

            if confidence > 0.7 and label == 15:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                return [startX, startY, endX, endY]
        return [0, 0, 0, 0]

    def detectMultiple(self, image):
        (h, w) = image.shape[:2]
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        self.detector.setInput(imageBlob)
        detections = self.detector.forward()
        if len(detections) == 0:
            return [[0, 0, 0, 0]]
        boundingBoxes = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            label = detections[0, 0, i, 1]
            if confidence >= 0.7 and label == 15:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                boundingBoxes.append((startX, startY, endX, endY))
        return boundingBoxes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=True)
    args = parser.parse_args()
    detector = detectPerson()
    img = cv2.imread(args.image)
    img = cv2.resize(img, (960, 720))

    while True:
        start = time.time()
        print(detector.detectMultiple(img))
        print(time.time() - start)
