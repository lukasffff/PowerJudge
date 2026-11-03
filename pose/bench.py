LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14

LOCKOUT_THRESHOLD = 0.05  # Adjust threshold as needed

def check_bench(result):
    if not result.pose_landmarks:
        return None

    landmarks = result.pose_landmarks[0]

    left_shoulder = landmarks[LEFT_SHOULDER]
    right_shoulder = landmarks[RIGHT_SHOULDER]
    left_elbow = landmarks[LEFT_ELBOW]
    right_elbow = landmarks[RIGHT_ELBOW]

    left_depth = left_elbow.y >= left_shoulder.y
    right_depth = right_elbow.y >= right_shoulder.y

    if left_depth and right_depth:
        return True
    else:
        return False

def check_elbow(result):
    if not result.pose_landmarks:
        return None

    landmarks = result.pose_landmarks[0]

    return (landmarks[LEFT_ELBOW].y + landmarks[RIGHT_ELBOW].y) / 2 

def is_lockout(result, lockout_elbow_y):
    if lockout_elbow_y is None:
        return None

    elbow_y = check_elbow(result)

    if elbow_y is None:
        return None

    return elbow_y <= lockout_elbow_y + LOCKOUT_THRESHOLD