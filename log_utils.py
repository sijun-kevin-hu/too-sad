from datetime import datetime

def log_event(emotion, sadness_confidence, face_confidence, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("too_sad_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} | {emotion} | sadness confidence: {sadness_confidence:.2f} | face confidnece: {face_confidence:.2f} | action: {action}\n")
