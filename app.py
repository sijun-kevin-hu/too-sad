import time
import random
import webbrowser
import cv2 as cv
import sys
from plyer import notification
from log_utils import log_event
from config import frame_count_limit, recent_emotions_limit, cooldown_seconds, happy_videos, happy_messages
from emotion_utils import analyze_emotion, update_recent_emotion, is_sad

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    sys.exit()
    
frame_count = 0
recent_emotions = []
last_trigger_time = 0
dominant_emotion = "Detecting..."


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
        log_event(dominant_emotion, sadness_confidence, face_confidence, "Detected emotion")
        print(f"Detected Dominant emotion: {dominant_emotion}. Sadness Confidence: {sadness_confidence}")
        if (face_confidence > 0.8):
            update_recent_emotion(recent_emotions, dominant_emotion, sadness_confidence, recent_emotions_limit)
            log_event(dominant_emotion, sadness_confidence, face_confidence, "Updated recent emotions")
                    
        if is_sad(recent_emotions, recent_emotions_limit):
            print("Detected sadness. Triggering.")
            log_event(dominant_emotion, sadness_confidence, face_confidence, "Detected sadness. Triggering action.")
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
                log_event(dominant_emotion, sadness_confidence, face_confidence, "Notification Sent + YouTube link po")
                
    # Display the resulting frame
    # cv.putText(frame, dominant_emotion, (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
    # cv.imshow('frame', frame)
    # if cv.waitKey(30) == ord('q'):
    #     break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()