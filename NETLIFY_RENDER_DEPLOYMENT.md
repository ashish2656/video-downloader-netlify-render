# Netlify + Render Deployment Guide

## 1) Deploy the Flask API on Render

1. Push this repo to GitHub.
2. Go to https://render.com and create a new Web Service.
3. Connect your GitHub repo.
4. Render should detect Python. If it does not, set:
   - Build command: pip install -r requirements.txt
   - Start command: gunicorn app:app
5. Set environment variables:
   - ALLOWED_ORIGINS = https://your-netlify-site.netlify.app
6. Deploy. Copy your API URL (example: https://your-api.onrender.com).

## 2) Deploy the React UI on Netlify

1. Go to https://netlify.com and create a new site from Git.
2. Select the same repo.
3. Build settings:
   - Base directory: frontend
   - Build command: npm install && npm run build
   - Publish directory: dist
4. Add environment variables:
   - VITE_API_BASE = https://your-api.onrender.com
5. Deploy the site.

## 3) Update CORS (after Netlify URL is final)

1. Go back to Render and update:
   - ALLOWED_ORIGINS = https://your-netlify-site.netlify.app
2. Trigger a manual deploy or wait for auto-deploy.

## 4) Local Development

Backend:

1. Create a virtual environment and install deps:
   - python3 -m venv venv
   - source venv/bin/activate
   - pip install -r requirements.txt
2. Run the API:
   - python app.py

Frontend:

1. Move into the frontend folder:
   - cd frontend
2. Install deps and start dev server:
   - npm install
   - npm run dev
3. Create frontend/.env with:
   - VITE_API_BASE=http://localhost:5000

## Notes

- Netlify is static hosting. The Flask API must stay on Render.
- If requests fail, confirm the Netlify URL matches ALLOWED_ORIGINS.
