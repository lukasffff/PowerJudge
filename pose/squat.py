LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26

LOCKOUT_THRESHOLD = 0.05  # Adjust threshold as needed

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

def check_hip(result):
    if not result.pose_landmarks:
        return None

    landmarks = result.pose_landmarks[0]

    return (landmarks[LEFT_HIP].y + landmarks[RIGHT_HIP].y) / 2 

def is_lockout(result, lockout_hip_y):
    if lockout_hip_y is None:
        return None

    hip_y = check_hip(result)

    if hip_y is None:
        return None

    return hip_y <= lockout_hip_y + LOCKOUT_THRESHOLD