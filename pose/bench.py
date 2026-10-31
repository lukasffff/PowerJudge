LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14

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