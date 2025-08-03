import time
import numpy as np
import random
import webbrowser
import cv2 as cv
from plyer import notification
from deepface import DeepFace

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
frame_count = 0
frame_count_limit = 20
recent_emotions = []
recent_emotions_limit = 10
last_trigger_time = 0
dominant_emotion = "Detecting..."

happy_videos = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=9bZkp7q19f0",
    "https://www.youtube.com/watch?v=J---aiyznGQ",
    "https://www.youtube.com/watch?v=lXMskKTw3Bc",
]

happy_messages = [
    "Cheer up! 🌈 Here's something to make you smile.",
    "Feeling down? 😄 Take a quick happy break!",
    "TooSad detected sadness! Launching happiness...",
    "Your happiness matters. Here's a mood boost 🎵",
]

# Helper to update recent emotions
def update_recent_emotion(emotion, sadness_confidence):
    if len(recent_emotions) >= recent_emotions_limit:
        recent_emotions.pop(0)
        recent_emotions.append((emotion, sadness_confidence))
    else:
        recent_emotions.append((emotion, sadness_confidence))

# Analyzes the emotion on current frame
def analyze_emotion(frame):
    try:    
        # Uses DeepFace to analyze emotion in frame
        result = DeepFace.analyze(frame, ["emotion"], enforce_detection=False)

        dominant_emotion = result[0]['dominant_emotion']
        sadness_confidence = result[0]['emotion']['sad']
        face_confidence = result[0]['face_confidence']
        
        return ((dominant_emotion, sadness_confidence, face_confidence))
    except Exception as e:
        print("No face detected:", e)
        raise Exception(e)

# Uses the recent_emotions to check if user is sad        
def isSad():
    if (len(recent_emotions) == recent_emotions_limit):
        dominant_emotions = []
        for emotion_tuple in recent_emotions:
            dominant_emotions.append(emotion_tuple[0])
        
        mode_emotion = max(set(dominant_emotions), key=dominant_emotions.count)
        return mode_emotion == 'sad'

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    frame_count += 1
    cooldown_seconds = 30
    # Our operations on the frame come here
    if frame_count % frame_count_limit == 0:
        dominant_emotion, sadness_confidence, face_confidence = analyze_emotion(frame)
        print(f"Detected Dominant emotion: {dominant_emotion}. Sadness Confidence: {sadness_confidence}")
        if (face_confidence > 0.8):
            update_recent_emotion(dominant_emotion, sadness_confidence)
            
        print(recent_emotions)
        
        if isSad():
            print("Detected sadness. Triggering.")
            current_time = time.time()
            happy_video_url = random.choice(happy_videos)
            happy_message = random.choice(happy_messages)
            
            if current_time - last_trigger_time > cooldown_seconds:
                notification.notify(
                    title="TOO SAD ALERT",
                    message=happy_message,
                    timeout=10,
                    app_icon='./sun.png'
                )
                webbrowser.open(happy_video_url)
                last_trigger_time = current_time
                print(f"Notification Sent + YouTube link opened")
                
    # Display the resulting frame
    # cv.putText(frame, dominant_emotion, (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
    # cv.imshow('frame', frame)
    # if cv.waitKey(30) == ord('q'):
    #     break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()