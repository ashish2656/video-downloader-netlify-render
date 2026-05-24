from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import uuid

app = Flask(__name__)

def _parse_allowed_origins(value):
    if not value or value.strip() == "*":
        return "*"
    return [origin.strip() for origin in value.split(",") if origin.strip()]

allowed_origins = _parse_allowed_origins(os.environ.get("ALLOWED_ORIGINS", "*"))
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

TASKS = {}

@app.route('/')
def index():
    return jsonify({'status': 'ok'})

@app.route('/api/download', methods=['POST'])
def api_download():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        choice = data.get('choice', 'video')
        if not url:
            return jsonify({'error': 'URL required'}), 400
        task_id = f"task_{uuid.uuid4().hex}"
        TASKS[task_id] = {
            'created_at': time.time(),
            'choice': choice,
            'url': url,
            'title': 'Request received'
        }
        return jsonify({'task_id': task_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<task_id>', methods=['GET'])
def api_status(task_id):
    task = TASKS.get(task_id)
    if not task:
        return jsonify({'status': 'error', 'message': 'Task not found'}), 404
    elapsed = time.time() - task['created_at']
    if elapsed < 2:
        return jsonify({'status': 'downloading', 'message': 'Preparing download'})
    return jsonify({'status': 'completed', 'title': task['title']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')))

