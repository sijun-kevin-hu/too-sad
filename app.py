import time
import numpy as np
import webbrowser
import cv2 as cv
from deepface import DeepFace

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
frame_count = 0
frame_count_limit = 20
recent_emotions = []
recent_emotions_limit = 10
dominant_emotion = "Detecting..."

happy_video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1'

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
    last_trigger_time = 0
    cooldown_seconds = 30
    # Our operations on the frame come here
    if frame_count % frame_count_limit == 0:
        dominant_emotion, sadness_confidence, face_confidence = analyze_emotion(frame)
        print("Dominant emotion: ", dominant_emotion)
        print("Sadness Confidence: ", sadness_confidence)
        print("Confidence: ", face_confidence)
        if (face_confidence > 0.8):
            update_recent_emotion(dominant_emotion, sadness_confidence)
            
        print(recent_emotions)
        
        if isSad():
            current_time = time.time()
            if current_time - last_trigger_time > cooldown_seconds:
                print("Opening video!")           
                webbrowser.open(happy_video_url)
                last_trigger_time = current_time
                
    # Display the resulting frame
    cv.putText(frame, dominant_emotion, (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
    cv.imshow('frame', frame)
    if cv.waitKey(30) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()