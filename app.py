import time
import random
import webbrowser
import cv2 as cv
import sys
from plyer import notification
from log_utils import log_event
from config import frame_count_limit, recent_emotions_limit, cooldown_seconds, happy_videos, happy_messages
from emotion_utils import analyze_emotion, update_recent_emotion, is_sad

def main():
    # Initialize camera
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        input("Press Enter to exit...")
        sys.exit()

    # Initialize variables
    frame_count = 0
    recent_emotions = []
    last_trigger_time = 0
    dominant_emotion = "Detecting..."
    
    print("=" * 50)
    print("EMOTION DETECTION APP STARTED")
    print("=" * 50)
    print("The app is now monitoring your emotions...")
    print("Press 'q' in the camera window to quit")
    print("Or press Ctrl+C in this terminal to stop")
    print("=" * 50)

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            # Check if frame is read correctly
            if not ret:
                print("Can't receive frame (stream end?). Exiting...")
                break

            frame_count += 1

            # Analyze emotion periodically
            if frame_count % frame_count_limit == 0:
                dominant_emotion, sadness_confidence, face_confidence = analyze_emotion(frame)
                log_event(dominant_emotion, sadness_confidence, face_confidence, "Detected emotion")
                print(f"Detected Dominant emotion: {dominant_emotion}. Sadness Confidence: {sadness_confidence}. Face Confidence: {face_confidence}")
                
                if face_confidence > 0.8:
                    update_recent_emotion(recent_emotions, dominant_emotion, sadness_confidence, recent_emotions_limit)
                    log_event(dominant_emotion, sadness_confidence, face_confidence, "Updated recent emotions")
                    
                    if is_sad(recent_emotions, recent_emotions_limit):
                        print("Detected sadness. Triggering.")
                        log_event(dominant_emotion, sadness_confidence, face_confidence, "Detected sadness. Triggering action.")
                        
                        current_time = time.time()
                        
                        if current_time - last_trigger_time > cooldown_seconds:
                            happy_video_url = random.choice(happy_videos)
                            happy_message = random.choice(happy_messages)
                            
                            notification.notify(
                                title="TOO SAD ALERT",
                                message=happy_message,
                                timeout=10,
                                app_icon='./sun.png'
                            )
                            webbrowser.open(happy_video_url)
                            last_trigger_time = current_time
                            print(f"Notification Sent + YouTube link opened")
                            log_event(dominant_emotion, sadness_confidence, face_confidence, "Notification Sent + YouTube link opened")

            # Display the camera feed with emotion overlay
            cv.putText(frame, f"Emotion: {dominant_emotion}", (10, 30), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv.imshow('Emotion Detection - Press Q to Quit', frame)
            
            # Check for quit command
            if cv.waitKey(1) & 0xFF == ord('q'):
                print("\nQuitting application...")
                break

    except KeyboardInterrupt:
        print("\n\nApplication stopped by user (Ctrl+C)")
    
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("The application will now close.")
    
    finally:
        # Clean up resources
        print("Cleaning up...")
        cap.release()
        cv.destroyAllWindows()
        print("Application closed successfully.")
        print("Thank you for using the Emotion Detection App!")

if __name__ == "__main__":
    main()