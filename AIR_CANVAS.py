import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time
import threading
import speech_recognition as sr

# --- 1. INITIALIZATION ---
# Points arrays
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
colorIndex = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

# Shared variable for the voice command
current_voice_command = ""

# --- 2. VOICE THREAD ---
def listen_for_commands():
    global current_voice_command
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                # Short timeout and phrase limit to keep it responsive
                audio = r.listen(source, phrase_time_limit=2)
                command = r.recognize_google(audio).lower()
                current_voice_command = command
                print(f"Voice detected: {command}")
            except:
                continue

# Start background thread
threading.Thread(target=listen_for_commands, daemon=True).start()

# --- 3. CANVAS SETUP ---
paintWindow = np.zeros((471,636,3)) + 255
# (Standard UI rectangles and text code)
def draw_ui(img):
    img = cv2.rectangle(img, (40,1), (140,65), (0,0,0), 2)
    img = cv2.rectangle(img, (160,1), (255,65), (255,0,0), 2)
    img = cv2.rectangle(img, (275,1), (370,65), (0,255,0), 2)
    img = cv2.rectangle(img, (390,1), (485,65), (0,0,255), 2)
    img = cv2.rectangle(img, (505,1), (600,65), (0,255,255), 2)
    cv2.putText(img, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    return img

paintWindow = draw_ui(paintWindow)

# Mediapipe and Buffers
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
smooth_buffer = deque(maxlen=3)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = draw_ui(frame)

    # --- 4. VOICE COMMAND LOGIC (Apply Choice) ---
    if "blue" in current_voice_command: colorIndex = 0; current_voice_command = ""
    elif "green" in current_voice_command: colorIndex = 1; current_voice_command = ""
    elif "red" in current_voice_command: colorIndex = 2; current_voice_command = ""
    elif "yellow" in current_voice_command: colorIndex = 3; current_voice_command = ""
    elif "clear" in current_voice_command:
        bpoints, gpoints, rpoints, ypoints = [deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)]
        blue_index = green_index = red_index = yellow_index = 0
        paintWindow[67:,:,:] = 255
        current_voice_command = ""

    # --- 5. VISION & DRAWING LOGIC ---
    result = hands.process(framergb)
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                landmarks.append([int(lm.x * 640), int(lm.y * 480)])
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

        # Smoothing
        smooth_buffer.append((landmarks[8][0], landmarks[8][1]))
        pts_arr = np.array(smooth_buffer)
        center = (int(np.mean(pts_arr[:, 0])), int(np.mean(pts_arr[:, 1])))
        thumb = (landmarks[4][0], landmarks[4][1])

        cv2.circle(frame, center, 3, (0,255,0), -1)

        # Draw Condition
        if (thumb[1] - center[1] < 40): # Adjust this if drawing doesn't start
            bpoints.append(deque(maxlen=512)); blue_index += 1
            gpoints.append(deque(maxlen=512)); green_index += 1
            rpoints.append(deque(maxlen=512)); red_index += 1
            ypoints.append(deque(maxlen=512)); yellow_index += 1
        elif center[1] <= 65: # UI Button logic
            if 40 <= center[0] <= 140: # Clear
                bpoints, gpoints, rpoints, ypoints = [deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)]
                blue_index = green_index = red_index = yellow_index = 0
                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255: colorIndex = 0
            elif 275 <= center[0] <= 370: colorIndex = 1
            elif 390 <= center[0] <= 485: colorIndex = 2
            elif 505 <= center[0] <= 600: colorIndex = 3
        else: # Standard drawing
            if colorIndex == 0: bpoints[blue_index].appendleft(center)
            elif colorIndex == 1: gpoints[green_index].appendleft(center)
            elif colorIndex == 2: rpoints[red_index].appendleft(center)
            elif colorIndex == 3: ypoints[yellow_index].appendleft(center)
    else:
        # Prevent disconnects when hand is lost
        bpoints.append(deque(maxlen=512)); blue_index += 1
        gpoints.append(deque(maxlen=512)); green_index += 1
        rpoints.append(deque(maxlen=512)); red_index += 1
        ypoints.append(deque(maxlen=512)); yellow_index += 1

    # Render Lines
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None: continue
                cv2.line(frame, points[i][j][k-1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k-1], points[i][j][k], colors[i], 2)

    cv2.putText(frame, f"VOICE: {current_voice_command}", (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()