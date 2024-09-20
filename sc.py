import cv2
import mediapipe as mp
import numpy as np
from playsound import playsound
import threading
import os

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5
)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Status markers
sleep_count = 0
drowsy_count = 0
active_count = 0
current_status = ""
previous_status = ""
status_color = (0, 0, 0)

def compute(ptA, ptB):
    return np.linalg.norm(np.array(ptA) - np.array(ptB))

def blinked(eye):
    up = compute(eye[1], eye[5]) + compute(eye[2], eye[4])
    down = compute(eye[0], eye[3])
    ratio = up / (2.0 * down)

    if ratio > 0.3:  # Eyes open
        return 2
    elif 0.2 < ratio <= 0.3:  # Eyes semi-open (drowsy)
        return 1
    else:  # Eyes closed (sleeping)
        return 0

def brighten_image(image, alpha=1.3, beta=40):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def draw_face_overlay(image, landmarks):
    overlay = np.zeros_like(image)
    face_color = (255, 0, 0)

    for (x, y) in landmarks:
        cv2.circle(overlay, (x, y), 3, face_color, -1)

    face_connections = [(33, 133), (133, 153), (153, 144), (144, 33),
                        (362, 263), (263, 373), (373, 380), (380, 362)]
    
    for (i, j) in face_connections:
        cv2.line(overlay, landmarks[i], landmarks[j], face_color, 2)

    alpha = 0.6
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

def play_alert(alert_type):
    alert_sounds = {
        "SLEEPING": r"D:\Nullclass PVT LTD\Driver-Drowsiness-Detection-master\2.wav",
    }
    
    if alert_type in alert_sounds:
        sound_file = alert_sounds[alert_type]
        if os.path.exists(sound_file):
            playsound(sound_file)
        else:
            print(f"Audio file not found: {sound_file}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    frame = brighten_image(frame)
    current_status = ""

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0]))
                         for lm in face_landmarks.landmark]

            left_eye = [landmarks[i] for i in [33, 160, 158, 133, 153, 144]]
            right_eye = [landmarks[i] for i in [362, 385, 387, 263, 373, 380]]

            left_blink = blinked(left_eye)
            right_blink = blinked(right_eye)

            if left_blink == 0 or right_blink == 0:
                sleep_count += 1
                drowsy_count = active_count = 0
                if sleep_count > 8:
                    current_status = "SLEEPING !!!"
                    status_color = (0, 0, 255)

            elif left_blink == 1 or right_blink == 1:
                sleep_count = active_count = 0
                drowsy_count += 1
                if drowsy_count > 6:
                    current_status = "DROWSY !"
                    status_color = (255, 165, 0)

            else:
                drowsy_count = sleep_count = 0
                active_count += 1
                if active_count > 2:
                    current_status = "ACTIVE :)"
                    status_color = (0, 255, 0)

            cv2.putText(frame, current_status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, status_color, 3)
            draw_face_overlay(frame, landmarks)

    if current_status != previous_status:
        if current_status in ["SLEEPING !!!", "DROWSY !"]:
            threading.Thread(target=play_alert, args=(current_status,)).start()
        previous_status = current_status

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
