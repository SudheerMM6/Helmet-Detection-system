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
  python_streamlit/      Streamlit detection app and model file
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

Upload a local `.mp4` or `.avi` file from the Streamlit sidebar. Sample videos are not tracked in Git because video files make the repository heavy. For local testing, place your own sample under `python_streamlit/` or upload it from any folder on your machine.

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

- The model file `python_streamlit/best_motorcycle_final.pt` is required for local detection.
- Set `MODEL_PATH` if you store the model somewhere else.
- Detection quality depends on the model, video angle, lighting, and confidence threshold.
- This project is a prototype, not a production traffic enforcement system.
