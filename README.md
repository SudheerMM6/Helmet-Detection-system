# Helmet Detection and Warning System

A road-safety demo that combines an Express dashboard with a Streamlit video workflow for detecting helmet violations from uploaded traffic footage.

## What It Does

- Provides a password-protected Express dashboard for selecting monitoring locations.
- Opens a Streamlit workflow for video upload and frame-by-frame detection.
- Uses a custom YOLOv5 model file for detection.
- Saves detected frames locally during processing.

## Tech Stack

- Node.js, Express, EJS
- Streamlit, Python, OpenCV
- PyTorch and YOLOv5

## Project Structure

```text
Automatic-Helmet-Detection-and-Warning-System/
  server.js              Express app entry point
  router.js              Login, dashboard, and logout routes
  views/                 EJS login page and dashboard HTML
  public/                CSS and dashboard images
  python_streamlit/      Streamlit detection app, model, and sample video
```

## Local Setup

Install Node dependencies:

```bash
npm install
```

Create `.env` from `.env.example`:

```env
PORT=3000
SESSION_SECRET=replace_with_a_long_random_value
DASHBOARD_USER=admin@example.com
DASHBOARD_PASSWORD=replace_with_a_demo_password
```

Start the Express dashboard:

```bash
npm start
```

Open:

```text
http://localhost:3000
```

## Streamlit Setup

Install Python dependencies:

```bash
cd python_streamlit
pip install -r requirements.txt
```

Run the detection workflow:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Checks

Run the JavaScript syntax check:

```bash
npm test
```

Run a Python syntax check:

```bash
python -m py_compile python_streamlit/app.py
```

## Notes

- The included model file is required for local detection.
- The included video is a local demo sample.
- This project is a prototype, not a production traffic enforcement system.
