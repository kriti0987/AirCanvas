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

The process is divided in six phases:
1. Environment & Dependency Setup
   1.**Library Integration**: Install and import OpenCV (vision), MediaPipe (tracking), NumPy (matrices), and SpeechRecognition (audio).
   2. **Data Structure Design**: Initialize deques (double-ended queues) to store the (x, y) coordinates of the drawing. Used separate queues for different colors to keep the drawing persistent.






