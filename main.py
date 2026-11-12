import time
import cv2

from camera.camera import Camera
from pose.detection import PoseDetector
from pose import squat, bench
from audio import play_audio

camera = Camera()
detector = PoseDetector()

lift_choice = "squat"

was_at_depth = False
lockout_y = None

#Calibration Settings
HOLD_TIME = 2
PAUSE_RANGE = 0.02

hold_start_y = None
hold_start_time = 0

#Prompt lift of choice 

#enter loop for lift of choice

while True:

    frame = camera.get_frame()

    if frame is not None:
        result = detector.detect(frame)
        frame = detector.draw_pose(frame, result)

        if lift_choice == "squat":
            PAUSE_RANGE = 0.02
            at_depth = squat.check_squat(result)
            at_lockout = squat.is_lockout(result, lockout_y)
            current_y = squat.check_hip(result)
        else:
            PAUSE_RANGE = 0.07
            at_depth = bench.check_bench(result)
            at_lockout = bench.is_lockout(result, lockout_y)
            current_y = bench.check_elbow(result)
            

        if lockout_y is None:

            if current_y is None:
                #No person in view
                hold_start_y = None

            elif hold_start_y is None:
                #First frame
                hold_start_y = current_y
                hold_start_time = time.time()

            elif abs(current_y - hold_start_y) > PAUSE_RANGE:
                #Lifter moved too much
                hold_start_y = current_y
                hold_start_time = time.time()

            elif time.time() - hold_start_time >= HOLD_TIME:
                #Good pause
                lockout_y = current_y
                play_audio(1320)

        #DEPTH CHECK
        if at_depth is True:
            cv2.putText(frame, "DEPTH", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            #Ding on depth
            if at_depth is False:
                play_audio()

            was_at_depth = True

        elif at_depth is False:
            cv2.putText(frame, "NO DEPTH", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            was_at_depth = False

        #LOCKOUT CALIBRATION + CHECKS
        if lockout_y is None:
            cv2.putText(frame, "LOCKOUT TO CALIBRATE", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        elif at_lockout is True:
            cv2.putText(frame, "LOCKEDOUT", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif at_lockout is False:
            cv2.putText(frame, "NOT LOCKED OUT", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        
        
        
        cv2.putText(frame, "S = squat   B = bench   R = recalibrate", (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("PowerJudge", frame)

    key = cv2.waitKey(1)

    if key == ord(" "):
        break
    elif key == ord("r"):
        #Forget the saved lockout and recalibrate 
        lockout_y = None
        hold_start_y = None
    elif key == ord("s"):
        lift_choice = "squat"
        lockout_y = None
        hold_start_y = None
        at_depth = False
    elif key == ord("b"):
        lift_choice = "bench"
        lockout_y = None
        hold_start_y = None
        at_depth = False

camera.camera.release()
cv2.destroyAllWindows()