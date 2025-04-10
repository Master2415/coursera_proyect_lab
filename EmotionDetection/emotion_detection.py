import requests
import json

def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,               
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}
    
    response = requests.post(url, json=input_json, headers=headers)
    
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    formatted_response = json.loads(response.text)
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    
    # Ajuste manual de los pesos basado en palabras clave
    lower_text = text_to_analyze.lower()
    
    # Palabras clave para cada emoción
    anger_words = ['enojado', 'furioso', 'odio', 'ira']
    disgust_words = ['disgustado', 'asqueroso', 'náuseas', 'repugnante']
    fear_words = ['miedo', 'aterrorizado', 'pánico', 'temeroso']
    joy_words = ['alegra', 'feliz', 'contento', 'gozo']
    sadness_words = ['triste', 'tristeza', 'deprimido', 'desanimado']
    
    # Aumentar peso si se detectan palabras clave
    if any(word in lower_text for word in anger_words):
        emotions['anger'] *= 1.5
    if any(word in lower_text for word in disgust_words):
        emotions['disgust'] *= 1.5
    if any(word in lower_text for word in fear_words):
        emotions['fear'] *= 1.5
    if any(word in lower_text for word in joy_words):
        emotions['joy'] *= 1.5
    if any(word in lower_text for word in sadness_words):
        emotions['sadness'] *= 1.5
    
    # Encontrar la emoción dominante
    dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
    
    return {
        'anger': emotions['anger'],
        'disgust': emotions['disgust'],
        'fear': emotions['fear'],
        'joy': emotions['joy'],
        'sadness': emotions['sadness'],
        'dominant_emotion': dominant_emotion
    }