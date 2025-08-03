from deepface import DeepFace

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

# Helper to update recent emotions
def update_recent_emotion(recent_emotions, emotion, sadness_confidence, limit):
    if len(recent_emotions) >= limit:
        recent_emotions.pop(0)
        recent_emotions.append((emotion, sadness_confidence))
    else:
        recent_emotions.append((emotion, sadness_confidence))

# Uses the recent_emotions to check if user is sad. Limit is to check the length of list  
def is_sad(recent_emotions, limit):
    if (len(recent_emotions) == limit):
        dominant_emotions = []
        for emotion_tuple in recent_emotions:
            dominant_emotions.append(emotion_tuple[0])
        
        mode_emotion = max(set(dominant_emotions), key=dominant_emotions.count)
        return mode_emotion == 'sad'