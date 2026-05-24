# Instagram & YouTube Video/Audio Downloader

A Python script that downloads videos and audio from Instagram and YouTube in the highest quality possible.

## Features

✨ **Key Features:**
- Downloads from Instagram and YouTube
- Choose to download: **Video only**, **Audio only (MP3)**, or **Both**
- Automatically uses the highest quality available
- Downloads to `~/Downloads/Videos/` folder
- User-friendly interactive menu
- Error handling for invalid URLs and network issues

## Prerequisites

Make sure you have:
- **Python 3.7+** installed
- **FFmpeg** installed (required for audio conversion)

### Install FFmpeg

**On macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**On Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

## Installation & Setup

1. **Clone or download this script**

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install yt-dlp
```

## Web App (Netlify + Render)

This repo now supports a split deployment:
- Frontend: React + Vite + Framer Motion in the [frontend](frontend) folder (Netlify)
- Backend: Flask API in [app.py](app.py) (Render)

Step-by-step guide: [NETLIFY_RENDER_DEPLOYMENT.md](NETLIFY_RENDER_DEPLOYMENT.md)

## Usage

Run the script:
```bash
python3 video_audio_downloader.py
```

### Steps:

1. **Paste a link** from Instagram or YouTube
2. **Choose what to download:**
   - Option 1: Video only (highest quality MP4)
   - Option 2: Audio only (MP3 format)
   - Option 3: Both video and audio
3. **Wait for download** to complete
4. **Files are saved** in `~/Downloads/Videos/`

### Example:

```
📎 Paste the Instagram/YouTube link (or 'q' to quit): https://www.youtube.com/watch?v=dQw4w9WgXcQ

==================================================
What would you like to download?
==================================================
1. Video only (highest quality)
2. Audio only (MP3)
3. Both video and audio
==================================================
Enter your choice (1, 2, or 3): 1

==================================================
Starting download...
==================================================

✓ Download completed successfully!
File saved to: /Users/username/Downloads/Videos/Video_Title.mp4
```

## Troubleshooting

### "FFmpeg not found" error
- Install FFmpeg (see Prerequisites section above)

### "Instagram link not working"
- Instagram videos may have restrictions
- Make sure the account is public and the post is accessible
- Some videos may not be downloadable due to platform restrictions

### "YouTube age-restricted content"
- Some videos have age restrictions that prevent downloading

### "No suitable format found"
- The video might be private or deleted
- Check if the link is correct and the video is publicly accessible

## Notes

- **Respect copyright**: Only download content you have permission to download
- **Quality depends**: Download quality depends on what's available on the platform
- **Storage**: Videos can be large (100MB - 1GB+), ensure you have enough space
- **Network**: Large files may take time to download depending on connection speed

## License

Use this script responsibly and respect creators' copyright and terms of service.

---

**Enjoy downloading!** 🎬
