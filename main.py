import cv2

from camera.camera import Camera
from pose.detection import PoseDetector

camera = Camera()
detector = PoseDetector()


while True:

    frame = camera.get_frame()

    if frame is not None:
        result = detector.detect(frame)
        frame = detector.draw_pose(frame, result)
        cv2.imshow("PowerJudge", frame)

    if cv2.waitKey(1) == ord(" "):
        break

camera.camera.release()
cv2.destroyAllWindows()