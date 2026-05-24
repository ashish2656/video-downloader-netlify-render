# 🚀 DEPLOYMENT GUIDE - PythonAnywhere

## Step-by-Step Setup for PythonAnywhere (24/7 Hosting)

### PART 1: CREATE PYTHONANYWHERE ACCOUNT

1. **Go to PythonAnywhere:**
   - Website: https://www.pythonanywhere.com/
   - Click "Sign up" (top right)
   - Choose **FREE** account (good enough!)
   - Sign up with email or GitHub

2. **Verify your email** and log in

---

### PART 2: UPLOAD YOUR FILES

1. **After login, go to "Files" tab** (left sidebar)

2. **Create a new folder:**
   - Click "New folder" button
   - Name: `video-downloader`

3. **Upload your project files:**
   - Open the `video-downloader` folder
   - Click "Upload a file" and select:
     - `app.py`
     - `requirements.txt`
   - Create a `templates` folder inside
   - Upload `templates/index.html` inside that folder

   **Directory structure should look like:**
   ```
   video-downloader/
   ├── app.py
   ├── requirements.txt
   └── templates/
       └── index.html
   ```

---

### PART 3: CREATE A WEB APP

1. **Go to "Web" tab** (left sidebar)

2. **Click "Add a new web app"**
   - Choose "Python" (not "Manual configuration")
   - Select **Python 3.10** (or latest)
   - Click "Next"

3. **Select Flask**
   - Look for "Flask 3.0.0" option
   - Click it
   - It will auto-create the file structure

---

### PART 4: CONFIGURE THE WEB APP

1. **Go back to Web tab**

2. **Click on your web app** (it should show a URL like `yourname.pythonanywhere.com`)

3. **Update the WSGI configuration file:**
   - Scroll down to "Code" section
   - Click on the WSGI file (usually at `/var/www/yourname_pythonanywhere_com_wsgi.py`)
   
4. **Replace the content with this:**
   ```python
   import sys
   path = '/home/yourname/video-downloader'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from app import app as application
   ```
   
   **Replace `yourname` with your PythonAnywhere username!**

5. **Save the file** (Ctrl+S)

---

### PART 5: INSTALL DEPENDENCIES

1. **Open a Bash console:**
   - Go to "Consoles" tab
   - Click "Bash" (start a new console)

2. **Run these commands:**
   ```bash
   cd /home/yourname/video-downloader
   mkvirtualvenv --python=/usr/bin/python3.10 venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   Wait for it to finish. It will install:
   - Flask
   - yt-dlp
   - All dependencies

3. **Check if FFmpeg is installed:**
   ```bash
   which ffmpeg
   ```
   
   If it shows a path, you're good! If not:
   ```bash
   apt-get install ffmpeg
   ```
   (This might not work on free tier, but yt-dlp usually handles it)

---

### PART 6: GO LIVE!

1. **Back to "Web" tab**

2. **Click the green "Reload" button** (top right)
   - Wait 10 seconds for it to restart

3. **Your website is now live!** 🎉
   - URL: `https://yourname.pythonanywhere.com/`

---

### PART 7: KEEP IT RUNNING 24/7

✅ **PythonAnywhere automatically keeps your app running!**
- Your free account gives **100 CPU seconds per day** (plenty for downloads)
- Premium accounts get unlimited CPU

---

## ✅ TESTING YOUR APP

1. **Visit your URL:** `https://yourname.pythonanywhere.com/`

2. **Test it:**
   - Paste a YouTube or Instagram link
   - Choose download type
   - Click "Start Download"
   - Watch the status update

---

## ⚠️ IMPORTANT NOTES

### Free vs Paid Tier Limits:

| Feature | Free | Paid ($5/mo) |
|---------|------|------|
| CPU seconds/day | 100 | Unlimited |
| Storage | 512 MB | 1 GB+ |
| Bandwidth | Limited | Unlimited |
| Always-on | Yes | Yes |
| Custom domain | No | Yes |

### Storage Issue:
- Free tier has **512 MB** storage
- Large downloads might exceed this
- **Solution:** Paid plan ($5/month) → 1+ GB storage

### Download Issues:
1. **If Instagram videos don't download:** Some accounts/posts are private
2. **If YouTube is slow:** Normal - depends on video size
3. **"Permission denied" error:** Contact PythonAnywhere support

---

## 🆘 TROUBLESHOOTING

### App not loading?
1. Go to "Web" tab
2. Check "Error log" at the bottom
3. Scroll down to see error messages
4. Fix issues and reload

### 500 Error?
1. Check error log
2. Verify `app.py` path matches the WSGI file
3. Ensure all files are uploaded correctly

### Downloads not working?
1. Check file permissions in Bash console:
   ```bash
   cd /home/yourname/video-downloader
   ls -la
   ```
2. Try test download with CLI first:
   ```bash
   python app.py
   ```

---

## 📈 NEXT STEPS (Optional Upgrades)

### Add Custom Domain:
- Go to "Web" → "Add a domain"
- Use your custom domain (requires paid account)

### Monitor Usage:
- "Web" tab → "Logs"
- See who's using your app

### Backup Your Files:
- "Files" tab → Download files regularly

---

## 🎉 YOU'RE DONE!

Your video downloader is now live 24/7! 🚀

**Your website URL:** `https://yourname.pythonanywhere.com/`

Share it with friends and they can download videos anytime!

---

## 💡 QUICK COMMAND REFERENCE

```bash
# Access your app folder
cd /home/yourname/video-downloader

# Activate virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Test locally (bash console)
python app.py

# View logs
tail -f /var/log/yourname.pythonanywhere.com.log
```

---

Still having issues? Email PythonAnywhere support or check their docs: https://help.pythonanywhere.com/
