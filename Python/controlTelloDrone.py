from djitellopy import Tello
import argparse
import cv2
import os
import keyboard


class RyzeTello:
    def __init__(self, speed, save_session, save_path):
        # Initialize Tello object
        self.tello = Tello()

        # Set starting parameters
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.send_rc_control = False

        self.speed = speed
        self.save_session = save_session
        self.save_path = save_path

        if self.save_session:
            os.makedirs(self.save_path, exist_ok=True)

    def run(self):
        if not self.tello.connect():
            print("Tello not connected")
            return
        elif not self.tello.set_speed(self.speed):
            print('Not set speed to lowest possible')
            return
        elif not self.tello.streamoff():
            print("Could not stop video stream")
            return
        elif not self.tello.streamon():
            print("Could not start video stream")
            return

        self.tello.get_battery()

        frame_read = self.tello.get_frame_read()
        imgCount = 0

        while True:
            if frame_read.stopped:
                frame_read.stop()
                break
            
            frame = frame_read.frame

            if self.save_session:
                cv2.imwrite(f'{self.save_path}/{imgCount}.jpg', frame)
                imgCount += 1

            k = cv2.waitKey(20)
            
            if keyboard.is_pressed('esc'):  # break when ESC is pressed
                break
            elif keyboard.is_pressed('t'):
                self.tello.takeoff()
                self.send_rc_control = True
            elif keyboard.is_pressed('l'):
                self.tello.land()
                self.send_rc_control = False

            if self.send_rc_control:
                # fligh forward and back
                if keyboard.is_pressed('w'):
                    self.for_back_velocity = self.speed
                elif keyboard.is_pressed('s'):
                    self.for_back_velocity = -self.speed
                else:
                    self.for_back_velocity = 0
                
                # fligh left & right
                if keyboard.is_pressed('d'):
                    self.left_right_velocity = self.speed
                elif keyboard.is_pressed('a'):
                    self.left_right_velocity = -self.speed
                else:
                    self.left_right_velocity = 0
    
                # fligh up & down
                if keyboard.is_pressed('up'):
                    self.up_down_velocity = self.speed
                elif keyboard.is_pressed('down'):
                    self.up_down_velocity = -self.speed
                else:
                    self.up_down_velocity = 0

                # turn right or left
                if keyboard.is_pressed('right'):
                    self.yaw_velocity = self.speed
                elif keyboard.is_pressed('left'):
                    self.yaw_velocity = -self.speed
                else:
                    self.yaw_velocity = 0

                print(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity, self.yaw_velocity)
                # Send velocities to Drone
                self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity, self.yaw_velocity)

            # cv2.putText(frame, f'Battery: {str(self.tello.get_battery())[:2]}%', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('Tello Drone', frame)
        
        # Destroy cv2 windows and end drone connection 
        cv2.destroyAllWindows()
        self.tello.end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--speed', type=int, default=40, help='Speed of drone')
    parser.add_argument('-sa', '--save_session', action='store_true', help='Record flight')
    parser.add_argument('-sp', '--save_path', type=str, default="session/", help="Path where images will get saved")
    args = parser.parse_args()

    drone = RyzeTello(args.speed, args.save_session, args.save_path)
    drone.run()
