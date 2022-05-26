import cv2
import argparse
import time
import numpy as np


class detectFaces:

    def __init__(self):
        self.detector = cv2.dnn.readNetFromCaffe(
            'deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')
        self.embedder = cv2.dnn.readNetFromTorch('openface_nn4.small2.v1.t7')

    def detectSingle(self, image):
        (h, w) = image.shape[:2]
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        self.detector.setInput(imageBlob)
        detections = self.detector.forward()

        if len(detections) > 0:
            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]

            if confidence > 0.3:

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                return [startX, startY, endX, endY]
        return [0, 0, 0, 0]

    def detectMultiple(self, image):
        (h, w) = image.shape[:2]
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        self.detector.setInput(imageBlob)
        detections = self.detector.forward()
        if len(detections) == 0:
            return [[0, 0, 0, 0]]
        boundingBoxes = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.3:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                boundingBoxes.append((startX, startY, endX, endY))
        return boundingBoxes

    def getFaceEncoding(self, face):
        faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                         (0, 0, 0), swapRB=True, crop=False)
        self.embedder.setInput(faceBlob)
        return np.array(self.embedder.forward())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=True)
    args = parser.parse_args()
    detector = detectFaces()
    img = cv2.imread(args.image)
    img = cv2.resize(img, (960, 720))

    while True:
        # test detectSingle
        start = time.time()
        detector.detectSingle(img)
        print(time.time() - start)

        # test detectMultiple
        start = time.time()
        detector.detectMultiple(img)
        print(time.time() - start)
