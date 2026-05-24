from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import glob
import shutil
import threading
import time
import uuid

app = Flask(__name__)

def _parse_allowed_origins(value):
    if not value or value.strip() == "*":
        return "*"
    return [origin.strip() for origin in value.split(",") if origin.strip()]

allowed_origins = _parse_allowed_origins(os.environ.get("ALLOWED_ORIGINS", "*"))
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

DOWNLOADS_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

TASKS = {}
TASKS_LOCK = threading.Lock()

def _update_task(task_id, **updates):
    with TASKS_LOCK:
        task = TASKS.get(task_id)
        if task is None:
            return
        task.update(updates)

def _find_latest_file(task_id):
    matches = glob.glob(os.path.join(DOWNLOADS_DIR, f"{task_id}.*"))
    if not matches:
        return None
    return max(matches, key=os.path.getmtime)

def _build_ydl_options(task_id, choice):
    ffmpeg_available = shutil.which("ffmpeg") is not None
    cookies_file = os.environ.get("COOKIES_FILE")
    options = {
        "outtmpl": os.path.join(DOWNLOADS_DIR, f"{task_id}.%(ext)s"),
        "quiet": True,
        "no_warnings": True
    }

    if cookies_file:
        tmp_cookies_path = os.path.join("/tmp", f"cookies_{task_id}.txt")
        try:
            shutil.copyfile(cookies_file, tmp_cookies_path)
            options["cookiefile"] = tmp_cookies_path
        except Exception:
            options["cookiefile"] = cookies_file

    if choice == "audio":
        options["format"] = "bestaudio/best"
        if ffmpeg_available:
            options["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }
            ]
    elif choice == "both":
        if ffmpeg_available:
            options["format"] = "bestvideo+bestaudio/best"
            options["merge_output_format"] = "mp4"
        else:
            options["format"] = "best"
    else:
        options["format"] = "best"

    return options

def _run_download(task_id, url, choice):
    from yt_dlp import YoutubeDL

    def progress_hook(status):
        if status.get("status") == "downloading":
            message = status.get("_percent_str", "Downloading")
            _update_task(task_id, status="downloading", message=message)

    try:
        _update_task(task_id, status="downloading", message="Starting download")
        ydl_opts = _build_ydl_options(task_id, choice)
        ydl_opts["progress_hooks"] = [progress_hook]

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Download ready")

        file_path = _find_latest_file(task_id)
        if not file_path:
            raise RuntimeError("Download finished but file was not found")

        _update_task(
            task_id,
            status="completed",
            message="Ready to download",
            title=title,
            file_path=file_path,
            download_url=f"/api/download-file/{task_id}"
        )
    except Exception as exc:
        _update_task(task_id, status="error", message=str(exc))

@app.route('/')
def index():
    return jsonify({'status': 'ok'})

@app.route('/api/download', methods=['POST'])
def api_download():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        choice = data.get('choice', 'video').strip().lower()
        if not url:
            return jsonify({'error': 'URL required'}), 400
        if choice not in {"video", "audio", "both"}:
            choice = "video"
        task_id = f"task_{uuid.uuid4().hex}"
        with TASKS_LOCK:
            TASKS[task_id] = {
                'created_at': time.time(),
                'choice': choice,
                'url': url,
                'status': 'queued',
                'message': 'Queued'
            }

        worker = threading.Thread(target=_run_download, args=(task_id, url, choice), daemon=True)
        worker.start()
        return jsonify({'task_id': task_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<task_id>', methods=['GET'])
def api_status(task_id):
    with TASKS_LOCK:
        task = TASKS.get(task_id)
        if not task:
            return jsonify({'status': 'error', 'message': 'Task not found'}), 404
        return jsonify({
            'status': task.get('status', 'queued'),
            'message': task.get('message', ''),
            'title': task.get('title', ''),
            'download_url': task.get('download_url', '')
        })

@app.route('/api/download-file/<task_id>', methods=['GET'])
def api_download_file(task_id):
    with TASKS_LOCK:
        task = TASKS.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        file_path = task.get('file_path')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not ready'}), 404

    return send_from_directory(
        DOWNLOADS_DIR,
        os.path.basename(file_path),
        as_attachment=True,
        download_name=os.path.basename(file_path)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')))

