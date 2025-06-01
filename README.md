# AirCanvas (Drawing through hand gestures)
Machine Learning Pose Estimation using Computer Vision technique for tracking the movements of a person or an object, greatly aids in the development of automation processes and can enhance human-machine interaction in a variety of applications. The project focuses on MediaPipe hand tracking function based on high-performance palm detection and hand landmark model, OpenCV (Open-Source computer Vision) a Computer Vision, Machine Learning library supporting Python programming language, NLP (Natural Language Processing) and Numpy that helps maintaining an intuitive user experience while lowering latency and improving recognition accuracy. Within the fields of image processing and pattern recognition, air-based writing has become a fascinating and developing field of study that offers promising opportunities to improve human-computer interaction, a novel system that contributes voice typing and gesture control for writing in air. Furthermore, it incorporates gesture-based tracking. The dataset used in this project was selected especially for voice recognition and air-writing tasks. It combines voice samples recorded through an integrated microphone input with gesture-based inputs recorded via a webcam using the MediaPipe framework respectively. Evaluation is done by User accessibility, voice recognition capabilities, and gesture accuracy with MediaPipe's hand-tracking, gesture commands were highly accurate. Real-time responsiveness and low error rates were demonstrated by voice-to-text transcription. This efficacy for hands-free interaction was validated through usability testing. In conclusion, by offering a hands-free, interactive, and easily accessible platform for digital content creation, data representation and speech recognition, this project seeks to go beyond the constraints of current interaction technologies. The system expands on the idea of augmented reality, providing a rich medium for communication and real-time idea visualization.

# Problem Identification

Canvas makes it easy for instructors to manage digital materials, communications, and other aspects of instruction for their courses.
Aims to improve the creative process by removing barriers and allowing artists to immerse themselves.

1. Depth sensing is not possible:  Since depth sensing is not possible, up and down pen movements cannot be followed. Therefore, the fingertip's entire trajectory is traced, and the resulting image would be absurd and not recognized by the model.
   
2. Voice to text conversion:  Making the model versatile and technically independent, introducing multilingual text generation


# Objective
1. The system offers clear hand gestures for real-time system control (Synchronization).

2. Voice to text conversion through speech recognition.



# How it Works?
1. A motion-to- digital converter, based on idea of drawing in air (like waving in air) focuses on hand gesture recognition with the use of computer vision using python programming language, creating a natural human-machine interaction. The system offers clear hand gestures for real-time system control (Synchronization). 

2. The key requirements is the user must be on distance where it can be clearly visible to camera so that camera can take proper input. System captures user movements, allow drawing without keyboard, mouse, or touchpad, uses in virtual reality and hand movement recognition. Enabling more experimental and dynamic artwork, making it an ideal choice for creators. 

3. Can draw anything by capturing the motion of hand using a camera.
   
4. Read the video frames from the camera using NumPy and media pipe.
   
5. Track Index finger and helps to draw, write.

6. Use computer vision algorithms to detect hands (OpenCV), Deque is used to track the hand movement.

7. Use machine learning algorithms to recognize and classify different gestures (mediapipe).

8. Process the recognized gestures and trigger relevant actions or events. (NumPyand deque).

9. Zero(0) degree angle gesture between Thumb and Indexfinger leads to stop drawing on specific location.

10. Another aim is speech to text conversion with the help of speech recognition, which records all the words spoken in any language and converts into text for betterment in online classes, online meets and other educational purposes.  In which

11. Audio signals are converted to digital form, preprocessed to eliminate noise, and then examined using linguistic probabilities to determine phonemes, words, and sentences. The emergence of hands-free control systems, real-time transcription services has greatly increased the popularity of this technology. It is crucial for improving human-computer interaction, making it easier for people to access information, including healthcare, education, customer service, and smart devices.
  
12. Even with its advancements, speech recognition still faces obstacles from multilingual support, background noise, accents, and speech variability. With the use of sophisticated deep learning models, speech recognition will become more accurate in a variety of languages, accents, and noisy environments. Additionally, it may be easily incorporated into intelligent virtual assistants, healthcare diagnostics, and real-time communication.
    
13. Example, Online meets, educational purpose, artistic creativity. Canvas facilitates the management of digital resources, communications, and other course-related teaching elements for instructors aims to enhance the artistic process by lowering obstacles and enabling artists to fully engage 

# Technology Used
Python (Programming Language)

Machine Learning (ML) : Mediapipe.

Speech Recognition

Numpy (Python)

Natural Language Processing (NLP)

# Hardware Requirement 
Camera, Screen.
# Software Requirement
Python, Media-Pipe, OpenCV, NumPy, Speech recognition.

