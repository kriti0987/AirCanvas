# AIR CANVAS (DRAW THROUGH HAND GESTURES)




# The Problem 
1. Noise with jitter makes trajectory tip unmanagable and sensitive.  
2. Voice-to-text conversion:  Making the model versatile and technically independent, introducing multilingual text generation.


# Objective
1. Voice-to-text conversion through speech recognition.

# Tech Stack
1. Programming Language: Python
2. Library: Numpy, Deque
3. Machine Learning (ML) : Mediapipe
4. Computer Vision (OpenCv)
5. Natural Language Processing (NLP)-based Speech Recognition

# Hardware Requirement 
Camera, Screen.

# Procedure

The process is divided in Five phases:

**Phase 1: Environment & UI Initialization**

1. Defining the Canvas: Creating a blank numpy array (paintWindow) to serve as your digital paper.UI Design: Programming the draw_ui function to place static buttons (Clear, Blue, Red, etc.) at the top of the frame.
   
2. Data Structures: Using deque buffers to store the $(x, y)$ coordinates of your drawings for each color.
   
**Phase 2: Computer Vision Integration (MediaPipe)**

1. Hand Tracking: Integrating mp.solutions.hands to detect the 21 landmarks of the human hand in real-time.
2. Landmark Isolation: Specifically targeting Landmark 8 (Index Finger Tip) for drawing and Landmark 4 (Thumb) to create a "pinch" or "proximity" trigger for the draw condition.
   
3. Input Smoothing: Implementing a smooth_buffer to average out the jitter from the camera feed, ensuring your lines look clean and not jagged.
   
**Phase 3: Natural Language Processing (Speech Recognition)**

1. Multithreading: This is a critical step. By starting the listen_for_commands function in a separate threading.Thread, you ensure the camera feed doesn't freeze while the computer is "listening."
   
2. Command Parsing: Using the Google Speech API to convert audio into text strings like "red" or "clear," which then update the colorIndex globally.
   
**Phase 4: Main Loop & Drawing Logic**
1. Input Processing: The while loop continuously captures camera frames, flips them for a natural "mirror" effect, and processes them through the MediaPipe model.
   
2. Interactive Controls: Logic that checks if your finger is over a UI button or if your hand posture matches the "drawing" state.
   
3. Rendering: Using cv2.line to connect all the saved points in your deques and display them on both the live camera feed and the white canvas.
   
**Phase 5: Optimization & Benchmarking**
   
1. Latency Tracking: Using time.time() to measure the exact processing cost of each frame.
   
3. Visualization: Using matplotlib to generate the Pulse and Bar charts that prove system runs


# Outcome

<img width="1200" height="600" alt="Image" src="https://github.com/user-attachments/assets/4393c3f9-3b38-4ab3-95d3-1e5147e675fc" />

<img width="1200" height="600" alt="Image" src="https://github.com/user-attachments/assets/38040ada-dd0e-49bc-92fe-00e4396ab3f1" />

<img width="1200" height="600" alt="Image" src="https://github.com/user-attachments/assets/29f47d6e-6ca8-4689-b26a-31249702e568" />

<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/e016cfda-31bb-42d0-86ee-a2f0412b5c07" />

<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/973b3d59-99a0-49d5-9f43-765abf68600f" />

Average Frame Rate: 42.5 FPS.

Performance Gain: Operates at 41.6% above the industry-standard real-time threshold (30 FPS).

This ensures that digital ink follows the user's index finger with high spatial precision and zero perceived latency.



