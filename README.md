# 🎧 PDF Read-Aloud Converter

A Streamlit web app that converts any PDF into spoken MP3 audio.
Perfect for turning lecture notes and study guides into audio you can
listen to on the go.

---

## 🗂️ Project Structure

```
pdf_audio_app/
├── app.py              ← The main application
├── requirements.txt    ← All Python dependencies
└── README.md           ← This file
```

---

## 💻 Running Locally (Step-by-Step)

### Step 1 — Make sure Python is installed
Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux)
and type:

```bash
python --version
```

You should see something like `Python 3.10.x`. If not, download Python
from https://www.python.org/downloads/

---

### Step 2 — Create a project folder and add the files
Create a folder on your computer called `pdf_audio_app` and place
`app.py`, `requirements.txt`, and `README.md` inside it.

---

### Step 3 — (Recommended) Create a virtual environment
A virtual environment keeps this project's packages separate from your
other Python projects, preventing version conflicts.

```bash
# Navigate into your project folder first
cd path/to/pdf_audio_app

# Create the virtual environment (only need to do this once)
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# You'll see (venv) appear at the start of your terminal line.
# This means you're now inside the virtual environment.
```

---

### Step 4 — Install the dependencies

```bash
pip install -r requirements.txt
```

This installs Streamlit, gTTS, and pdfplumber. It may take a minute.

---

### Step 5 — Run the app

```bash
streamlit run app.py
```

Streamlit will automatically open your browser to:
`http://localhost:8501`

That's it! Your app is running. Upload any PDF and click Generate Audio.

To stop the app, press `Ctrl + C` in the terminal.

---

## 🌐 Deploying to the Web (Free — Streamlit Cloud)

Streamlit Cloud lets you host your app online for free so you can
access it from any device, including your phone.

### Step 1 — Push your code to GitHub

If you don't have a GitHub account, create one free at https://github.com

Then create a new repository (e.g. `pdf-audio-app`) and upload your
three files (`app.py`, `requirements.txt`, `README.md`) to it.

The quickest way to do this from your terminal:

```bash
# Initialise git in your project folder
git init

# Stage all files
git add .

# Commit them
git commit -m "Initial commit"

# Link to your GitHub repo (replace YOUR_USERNAME with your actual username)
git remote add origin https://github.com/YOUR_USERNAME/pdf-audio-app.git

# Push to GitHub
git push -u origin main
```

---

### Step 2 — Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository (`pdf-audio-app`), set the branch to `main`,
   and set the main file path to `app.py`.
4. Click **"Deploy!"**

Streamlit Cloud will install your requirements automatically and give you
a public URL like:
`https://YOUR_USERNAME-pdf-audio-app-app-xxxx.streamlit.app`

You can open that URL on your phone and use the full app!

---

## 📱 Using on Your Phone

Once deployed on Streamlit Cloud, simply open the public URL in your
phone's browser. The app is fully responsive. You can upload a PDF from
your phone's file storage, generate the audio, and stream or download
the MP3 directly to your device.

---

## ⚠️ Known Limitations

- **gTTS requires an internet connection.** The audio generation step
  contacts Google's servers. The app will not work fully offline.
- **Scanned PDFs won't work** unless they have an OCR text layer.
  If your PDF is just pictures of pages, the text extractor will find
  nothing. Run it through Adobe Acrobat or a free OCR tool first.
- **Very large PDFs** (100+ pages) may take a while to process and
  could hit Streamlit Cloud's memory limits on the free tier. For best
  results, upload PDFs under ~50 pages at a time.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | Web app framework |
| gTTS (Google Text-to-Speech) | Text to MP3 audio |
| pdfplumber | PDF text extraction |
| Python 3.10+ | Programming language |
