import os
from flask import Flask, render_template, request, jsonify
import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def run_evaluation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        environment = data.get('environment')
        job = data.get('job')
        feedback = data.get('feedback')
        
        if not environment or not job or not feedback:
            return jsonify({'error': 'All three parameters (environment, job, feedback) are required.'}), 400
        
        # Invoke the evaluation logic from main.py
        result = main.evaluate(environment=environment, job=job, feedback=feedback)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Start the server on port 5000
    app.run(debug=True, port=5000)
