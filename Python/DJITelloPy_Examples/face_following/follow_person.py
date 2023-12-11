import argparse
import os

import cv2
import numpy as np
from detect_face import detectFaces
from djitellopy import Tello

# TODO: Add better distance values
sizes = [406, 304, 202, 136]


class Drone:
    def __init__(self, speed, forward_backward_speed, steering_speed, up_down_speed, save_session, save_path, distance,
                 safety_x, safety_y, safety_z, face_recognition, face_path):
        # Initialize Drone
        self.tello = Tello()

        # Initialize Person Detector
        self.detector = detectFaces()
        self.face_recognition = face_recognition
        self.face_encoding = self.detector.getFaceEncoding(
            cv2.imread(face_path))

        self.speed = speed
        self.fb_speed = forward_backward_speed
        self.steering_speed = steering_speed
        self.ud_speed = up_down_speed
        self.save_session = save_session
        self.save_path = save_path
        self.distance = distance
        self.safety_x = safety_x
        self.safety_y = safety_y
        self.safety_z = safety_z

        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.flight_mode = False
        self.send_rc_control = False
        self.dimensions = (960, 720)

        if self.save_session:
            os.makedirs(self.save_path, exist_ok=True)

    def run(self):
        self.tello.connect()
        self.tello.streamon()

        self.tello.get_battery()

        frame_read = self.tello.get_frame_read()

        count = 0
        while True:
            if frame_read.stopped:
                frame_read.stop()
                break

            # Listen for key presses
            k = cv2.waitKey(20)

            if k == 8:
                self.flight_mode = not self.flight_mode
            elif k == 27:
                break
            elif k == ord('t'):
                self.tello.takeoff()
                self.send_rc_control = True
            elif k == ord('l'):
                self.tello.land()
                self.send_rc_control = False

            # read frame
            frameBGR = frame_read.frame

            if self.save_path:
                cv2.imwrite(f'{self.save_path}/{count}.jpg', frameBGR)
                count += 1

            x_min, y_min, x_max, y_max = 0, 0, 0, 0

            # detect person and get coordinates
            if self.face_recognition:
                boundingBoxes = self.detector.detectMultiple(frameBGR)
                for x_mi, y_mi, x_ma, y_ma in boundingBoxes:
                    image = frameBGR[y_mi:y_ma, x_mi:x_ma]
                    if image.shape[0] != 0 and image.shape[1] != 0:
                        face_encoding = self.detector.getFaceEncoding(image)
                        dist = np.linalg.norm(
                            self.face_encoding - face_encoding)
                        if dist < 0.95:
                            x_min, y_min, x_max, y_max = x_mi, y_mi, x_ma, y_ma
                            cv2.rectangle(frameBGR, (x_mi, y_mi),
                                          (x_ma, y_ma), (0, 255, 0), 2)
                        else:
                            cv2.rectangle(frameBGR, (x_mi, y_mi),
                                          (x_ma, y_ma), (255, 0, 0), 2)
            else:
                x_min, y_min, x_max, y_max = self.detector.detectSingle(
                    frameBGR)
                cv2.rectangle(frameBGR, (x_min, y_min),
                              (x_max, y_max), (255, 0, 0), 2)

            if not self.flight_mode and self.send_rc_control and x_max != 0 and y_max != 0:
                # these are our target coordinates
                targ_cord_x = int((x_min + x_max) / 2)
                targ_cord_y = int((y_min + y_max) / 2)

                # This calculates the vector from your face to the center of the screen
                vTrue = np.array(
                    (int(self.dimensions[0]/2), int(self.dimensions[1]/2), sizes[self.distance]))
                vTarget = np.array((targ_cord_x, targ_cord_y, (x_max-x_min)*2))
                vDistance = vTrue - vTarget

                # turn drone
                if vDistance[0] < -self.safety_x:
                    self.yaw_velocity = self.steering_speed
                elif vDistance[0] > self.safety_x:
                    self.yaw_velocity = -self.steering_speed
                else:
                    self.yaw_velocity = 0

                # for up & down
                if vDistance[1] > self.safety_y:
                    self.up_down_velocity = self.ud_speed
                elif vDistance[1] < -self.safety_y:
                    self.up_down_velocity = -self.ud_speed
                else:
                    self.up_down_velocity = 0

                # forward & backward
                if vDistance[2] > self.safety_z:
                    self.for_back_velocity = self.fb_speed
                elif vDistance[2] < self.safety_z:
                    self.for_back_velocity = -self.fb_speed
                else:
                    self.for_back_velocity = 0

                # always set left_right_velocity to 0
                self.left_right_velocity = 0

                # Draw the target as a circle
                cv2.circle(frameBGR, (targ_cord_x, targ_cord_y),
                           10, (0, 255, 0), 2)

                # Draw the safety zone
                cv2.rectangle(frameBGR, (targ_cord_x - self.safety_x, targ_cord_y - self.safety_y), (targ_cord_x + self.safety_x, targ_cord_y + self.safety_y),
                              (0, 255, 0), 2)
            elif not self.flight_mode and self.send_rc_control and x_max == 0 and y_max == 0:
                self.for_back_velocity = 0
                self.left_right_velocity = 0
                self.yaw_velocity = 0
                self.up_down_velocity = 0
            elif self.flight_mode and self.send_rc_control:
                # fligh forward and back
                if k == ord('w'):
                    self.for_back_velocity = self.speed
                elif k == ord('s'):
                    self.for_back_velocity = -self.speed
                else:
                    self.for_back_velocity = 0

                # fligh left & right
                if k == ord('d'):
                    self.left_right_velocity = self.speed
                elif k == ord('a'):
                    self.left_right_velocity = -self.speed
                else:
                    self.left_right_velocity = 0

                # fligh up & down
                if k == 38:
                    self.up_down_velocity = self.speed
                elif k == 40:
                    self.up_down_velocity = -self.speed
                else:
                    self.up_down_velocity = 0

                # turn
                if k == 37:
                    self.yaw_velocity = self.speed
                elif k == 39:
                    self.yaw_velocity = -self.speed
                else:
                    self.yaw_velocity = 0

            if self.send_rc_control:
                # Send velocities to Drone
                self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                           self.yaw_velocity)

            cv2.imshow('Tello Drone', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        # Destroy cv2 windows and end drone connection
        cv2.destroyAllWindows()
        self.tello.end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-os', '--overwrite_speed', type=int,
                        default=30, help='Speed for manual use')
    parser.add_argument('-fbs', '--forward_backward_speed', type=int, default=20,
                        help='Speed of forward and backward movement drone')
    parser.add_argument('-ss', '--steering_speed', type=int, default=40,
                        help='Steering speed')
    parser.add_argument('-uds', '--up_down_speed', type=int, default=20,
                        help='Speed of up and down movement drone')
    parser.add_argument('-sa', '--save_session',
                        action='store_true', help='Record flight')
    parser.add_argument('-sp', '--save_path', type=str,
                        default="session/", help="Path where images will get saved")
    parser.add_argument('-d', '--distance', type=int, default=0,
                        help='use -d to change the distance of the drone. Range 0-2')
    parser.add_argument('-sx', '--safety_x', type=int, default=100,
                        help='use -sx to change the safety bound on the x axis . Range 0-480')
    parser.add_argument('-sy', '--safety_y', type=int, default=55,
                        help='use -sy to change the safety bound on the y axis . Range 0-360')
    parser.add_argument('-sz', '--safety_z', type=int, default=30,
                        help='use -sz to change the safety bound on the z axis.')
    parser.add_argument('-fr', '--face_recognition',
                        action='store_true', help='Use Face Recognition')
    parser.add_argument('-fi', '--face_image', type=str,
                        required=True, help='Image of face to follow')
    args = parser.parse_args()

    drone = Drone(args.overwrite_speed, args.forward_backward_speed, args.steering_speed, args.up_down_speed,
                  args.save_session, args.save_path, args.distance, args.safety_x, args.safety_y, args.safety_z,
                  args.face_recognition, args.face_image)
    drone.run()
