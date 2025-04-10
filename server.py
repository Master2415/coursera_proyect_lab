"""
Módulo principal del servidor Flask para la detección de emociones (versión consola).
"""

from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    """
    Endpoint para analizar emociones en el texto proporcionado.
    
    Returns:
        JSON: Respuesta con los resultados del análisis de emociones.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        return jsonify({
            "error": "Invalid text! Please try again.",
            "status": 400
        }), 400
    
    response = emotion_detector(text_to_analyze)
    
    if response is None or response['dominant_emotion'] is None:
        return jsonify({
            "error": "Invalid text! Please try again.",
            "status": 400
        }), 400
    
    return jsonify({
        "anger": response['anger'],
        "disgust": response['disgust'],
        "fear": response['fear'],
        "joy": response['joy'],
        "sadness": response['sadness'],
        "dominant_emotion": response['dominant_emotion'],
        "status": 200
    })

@app.route('/')
def index():
    """
    Endpoint principal que muestra instrucciones para uso por consola.
    """
    return """
    <h1>API de Detección de Emociones</h1>
    <p>Usar desde consola con:</p>
    <code>curl "http://localhost:5000/emotionDetector?textToAnalyze=TU_TEXTO_AQUI"</code>
    """

if __name__ == '__main__':
    print("""
    Servidor de Detección de Emociones iniciado.
    Puedes probar los endpoints con:
    
    1. curl "http://localhost:5000/emotionDetector?textToAnalyze=Estoy%20muy%20feliz%20hoy"
    2. curl "http://localhost:5000/emotionDetector?textToAnalyze=Estoy%20enojado"
    3. curl "http://localhost:5000/emotionDetector?textToAnalyze=" (para probar error)
    
    Presiona CTRL+C para detener el servidor.
    """)
    app.run(host='0.0.0.0', port=5000)