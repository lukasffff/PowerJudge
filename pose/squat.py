LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26

def check_squat(result):
    if not result.pose_landmarks:
        return None

    landmarks = result.pose_landmarks[0]

    left_hip = landmarks[LEFT_HIP]
    right_hip = landmarks[RIGHT_HIP]
    left_knee = landmarks[LEFT_KNEE]
    right_knee = landmarks[RIGHT_KNEE]

    left_depth = left_hip.y >= left_knee.y
    right_depth = right_hip.y >= right_knee.y

    if left_depth and right_depth:
        return True
    else:
        return False