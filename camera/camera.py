import cv2

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        print("Camera Object Created")


        if self.camera.isOpened():
            print("Camera is opened")
        else:
            print("Camera is not opened")


    def get_frame(self):
        success, frame = self.camera.read()

        if success:
            return frame
        else:
            print("Failed to capture frame")
            return None
