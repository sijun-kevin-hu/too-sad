import numpy as np
import cv2 as cv
from deepface import DeepFace

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
frame_count = 0
frame_count_limit = 20
recent_emotions = []
recent_emotions_limit = 15
dominant_emotion = "Detecting..."

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
        

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    frame_count += 1
    # Our operations on the frame come here
    if frame_count % frame_count_limit == 0:
        dominant_emotion, sadness_confidence, face_confidence = analyze_emotion(frame)
        
        if (face_confidence > 0.8):
            update_recent_emotion(dominant_emotion, sadness_confidence)
        
        print("Emotion: ", dominant_emotion)
        print("Sadness Confidence: ", sadness_confidence)
        print("Confidence: ", face_confidence)
        print("Recent List: ", recent_emotions)
                
    # Display the resulting frame
    cv.putText(frame, dominant_emotion, (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
    cv.imshow('frame', frame)
    if cv.waitKey(30) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()