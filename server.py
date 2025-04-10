from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector')
def emotion_detector_route():
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)
    
    if response is None:
        return "Invalid text! Please try again."
    
    return f"For the given statement, the system response is 'anger': {response['anger']}, " \
           f"'disgust': {response['disgust']}, 'fear': {response['fear']}, " \
           f"'joy': {response['joy']} and 'sadness': {response['sadness']}. " \
           f"The dominant emotion is {response['dominant_emotion']}."

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)