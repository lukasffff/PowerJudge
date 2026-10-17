import cv2
import mediapipe as mp

#Pose Detection Class
class PoseDetector:

    # Initialize the PoseDetector
    def __init__(self):

        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        RunningMode = mp.tasks.vision.RunningMode

        default_options = PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="assets/models/pose_landmarker.task"
            ),
            running_mode=RunningMode.VIDEO,
            num_poses=1
        )

        self.landmarker = PoseLandmarker.create_from_options(default_options)

        print("Pose Detector Created")

    # Detect Pose in the given frame through converting imagge to RGB and then using the landmarker to detect the pose
    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.landmarker.detect(mp_image)

        return result

    # Draw the detected pose on the frame 
    def draw_pose(self, frame, result):

        if not result.pose_landmarks:
            return frame


        height, width, _ = frame.shape


        landmarks = result.pose_landmarks[0]


        points = []


        for landmark in landmarks:

            x = int(landmark.x * width)
            y = int(landmark.y * height)

            points.append((x, y))


            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )


        connections = [
            (11,12),
            (11,13),
            (13,15),
            (12,14),
            (14,16),

            (11,23),
            (12,24),

            (23,24),

            (23,25),
            (25,27),

            (24,26),
            (26,28)
        ]


        for a,b in connections:

            cv2.line(
                frame,
                points[a],
                points[b],
                (255,0,0),
                3
            )


        return frame