from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
tasks = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {'status': 'pending'}
    return jsonify({'task_id': task_id})

@app.route('/api/status/<task_id>')
def status(task_id):
    return jsonify(tasks.get(task_id, {'status': 'error'}))
