import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time
import threading
import matplotlib.pyplot as plt
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
    
    

# --- PERFORMANCE TRACKING SETUP ---
frame_times = []
voice_trigger_times = []

while True:
    start_time = time.time()  # <--- ADD THIS
    
    ret, frame = cap.read()
    # ... [Rest of your existing code] ...
    
    # Inside your loop, where you check current_voice_command:
    if current_voice_command != "":
        # Log that a voice command was active during this frame index
        voice_trigger_times.append(len(frame_times))
        
    # At the very end of the loop (just before the waitKey):
    frame_times.append(time.time() - start_time) # <--- ADD THIS
    
    if cv2.waitKey(1) == ord('q'): break

# --- PERFORMANCE VISUALIZATION ---
def plot_optimization_results(times, triggers):
    plt.figure(figsize=(12, 6))
    
    # Plot frame latency
    plt.plot(times, label='Frame Processing Time (s)', color='#1f77b4', alpha=0.8)
    
    # Highlight Voice Recognition Events
    for i, frame_idx in enumerate(triggers):
        plt.axvline(x=frame_idx, color='red', linestyle='--', alpha=0.6, 
                    label='Voice Command Triggered' if i == 0 else "")

    # Benchmark lines
    plt.axhline(y=0.033, color='green', linestyle=':', label='30 FPS Target (0.033s)')
    plt.axhline(y=0.066, color='orange', linestyle=':', label='15 FPS Minimum (0.066s)')

    plt.title('Air Canvas Optimization: Vision + Voice Concurrency')
    plt.xlabel('Frame Number')
    plt.ylabel('Latency (Seconds)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.show()

# Run the plot
if len(frame_times) > 0:
    plot_optimization_results(frame_times, voice_trigger_times)  
    
    
def plot_performance_summary(times):
    # Categorize frame latencies
    smooth = len([t for t in times if t <= 0.033])  # > 30 FPS
    acceptable = len([t for t in times if 0.033 < t <= 0.066])  # 15-30 FPS
    lagging = len([t for t in times if t > 0.066])  # < 15 FPS

    categories = ['Smooth (>30 FPS)', 'Acceptable (15-30 FPS)', 'Lagging (<15 FPS)']
    counts = [smooth, acceptable, lagging]
    colors = ['#2ca02c', '#ff7f0e', '#d62728'] # Green, Orange, Red

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, counts, color=colors, edgecolor='black', alpha=0.8)

    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{height} frames', ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.title('Air Canvas Optimization: Frame Stability Distribution')
    plt.ylabel('Number of Frames')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # Add a summary box
    avg_fps = 1 / (sum(times)/len(times)) if times else 0
    plt.annotate(f'Average Performance: {avg_fps:.1f} FPS', 
                 xy=(0.75, 0.9), xycoords='axes fraction',
                 bbox=dict(boxstyle="round", fc="white", ec="gray"))

    plt.show()

# Call this at the very end
plot_performance_summary(frame_times)  

cap.release()
cv2.destroyAllWindows()