<h1 align="center">📤 File Uploader</h1>

<p align="center">
  <strong>Fast. Simple. Shareable.</strong>
  <br>
  A lightweight Flask file uploader powered by Gofile.
</p>

<p align="center">
  <a href="https://file-uploader-25hn.onrender.com">
    <img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-Open%20Uploader-7C3AED?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://github.com/Hidden-Rhythm/file-uploader">
    <img src="https://img.shields.io/badge/💻%20SOURCE-GitHub-18181B?style=for-the-badge&logo=github" alt="Source Code">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Gofile-API-6B46C1?style=flat-square" alt="Gofile">
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render">
</p>

---

<h2 align="center">🚀 Live Demo</h2>

<p align="center">
  <a href="https://file-uploader-25hn.onrender.com">
    <strong>→ Open File Uploader</strong>
  </a>
</p>

<p align="center">
  Upload a file, let the server send it to Gofile,<br>
  and get a shareable download link back.
</p>

---

## ✨ Features

|    | Feature                   |                                                |
| -- | ------------------------- | ---------------------------------------------- |
| 📁 | **File Uploads**          | Upload files directly from the browser         |
| ☁️ | **Gofile Storage**        | Files are uploaded through the Gofile API      |
| 🔗 | **Shareable Links**       | Get a download link after upload               |
| 📂 | **Folder Support**        | Optionally upload to a Gofile folder           |
| 💬 | **Discord Notifications** | Receive upload activity through a webhook      |
| 🧹 | **Filename Handling**     | Uploaded filenames are sanitized               |
| ⚡  | **Lightweight**           | Simple Flask backend with minimal dependencies |
| 🚀 | **Render Ready**          | Includes Render deployment configuration       |

---

## 🔄 Upload Flow

```text
       ┌───────────────┐
       │     Browser   │
       └───────┬───────┘
               │
               │  Upload
               ▼
       ┌───────────────┐
       │ Flask Backend │
       └───────┬───────┘
               │
               │  Process
               ▼
       ┌───────────────┐
       │   Gofile API  │
       └───────┬───────┘
               │
               │  Download URL
               ▼
       ┌───────────────┐
       │     Browser   │
       └───────────────┘
```

With Discord notifications enabled:

```text
Upload
  │
  ├── File information
  ├── File size
  ├── Download link
  └── Request information
          │
          ▼
    Discord Webhook
```

---

## 🛠️ Built With

| Technology              | Role                |
| ----------------------- | ------------------- |
| 🐍 **Python**           | Application backend |
| 🌶️ **Flask**           | Web framework       |
| ☁️ **Gofile API**       | File storage        |
| 🌐 **Requests**         | HTTP requests       |
| 🧹 **Werkzeug**         | Filename handling   |
| 💬 **Discord Webhooks** | Notifications       |
| ⚡ **Gunicorn**          | Production server   |
| ☁️ **Render**           | Deployment          |

---

## 📂 Project Structure

```text
file-uploader/
│
├── app.py
├── requirements.txt
├── render.yaml
│
└── static/
    └── ...
```

---

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Hidden-Rhythm/file-uploader.git
cd file-uploader
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure credentials

The application requires the credentials used for the Gofile integration and, when enabled, the Discord webhook.

Keep these credentials private.

For production deployments, environment variables are recommended instead of hardcoding secrets inside the application.

### 4. Start the server

```bash
python app.py
```

The application runs on:

```text
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

### `GET /`

Loads the main uploader interface.

### `POST /api/upload`

Uploads a file through the application.

**Form data:**

| Parameter  | Required | Description               |
| ---------- | :------: | ------------------------- |
| `file`     |     ✅    | File to upload            |
| `folderId` |     ❌    | Optional Gofile folder ID |

### `GET /api/account-info`

Returns the Gofile account information used by the application.

---

## 💬 Discord Notifications

When configured, the application can send upload activity to a Discord webhook.

Depending on the configuration, notifications may include:

* 📄 Filename
* 📦 File size
* 🔗 Download URL
* 🌐 IP information
* 💻 Device information
* 🖥️ Browser / OS information
* 📍 Approximate location information

---

## ☁️ Deployment

The repository includes a `render.yaml` configuration for Render.

### Production command

```bash
gunicorn app:app --timeout 120
```

### Current deployment

**Render:** `file-uploader-25hn.onrender.com`

---

## 🔐 Configuration Note

For a public deployment:

* Keep API credentials private
* Keep Discord webhook URLs private
* Prefer environment variables for secrets
* Rotate credentials if they have previously been exposed
* Avoid committing sensitive configuration to GitHub

---

<p align="center">
  <br>
  <strong>📤 Upload. Share. Done.</strong>
  <br><br>
  <a href="https://file-uploader-25hn.onrender.com">
    🚀 <strong>Open the Live Demo</strong>
  </a>
  <br><br>
  <sub>Built with Flask + Gofile</sub>
</p>
