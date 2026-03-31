# 📓 CloudScript Journal

> A free, private, and hassle-free CLI journaling tool that saves your entries locally and backs them up to your personal Google Drive — **encrypted**.

---

## 🌟 Why CloudScript Journal?

Journaling is one of the most powerful habits you can build — for personal reflection, tracking professional growth, and preserving memories. But most tools fall short in one of two ways: **they're not private**, or **they're not easy enough to actually use consistently**.

CloudScript Journal was built to solve both problems:

- ✅ **Frictionless** — Just run the script and start typing. No app to open, no UI to navigate.
- ✅ **Private** — Your diary is encrypted with AES before being uploaded anywhere. Not even Google can read it.
- ✅ **Backed up** — Your encrypted diary ZIP is automatically synced to your own Google Drive storage.
- ✅ **Free** — No subscriptions, no accounts to create (beyond Google Drive which you already have).
- ✅ **Cross-platform** — Works on Linux, macOS, and Windows.

> 🚀 **Coming soon:** A companion project that will let you semantically search through all your diary entries and ask questions about your past experiences — stay tuned!

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Linux](#linux-setup)
  - [macOS](#macos-setup)
  - [Windows](#windows-setup)
- [Google Cloud Console Setup](#google-cloud-console-setup)
- [Configuration in the Script](#configuration-in-the-script)
- [Running the App](#running-the-app)
- [First Run Walkthrough](#first-run-walkthrough)
- [File Structure](#file-structure)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)

---

## ⚙️ How It Works

```
You type your journal entry in the terminal
        ↓
Entry is saved as a plain text file locally (named by date)
        ↓
All diary files are compressed into a ZIP archive
        ↓
ZIP is encrypted with AES using your chosen password
        ↓
(Optional) Encrypted ZIP is uploaded/updated on your Google Drive
```

On every subsequent run, the script remembers your target directory and password (stored locally via a pickle file), so you won't need to re-enter them.

---

## ✨ Features

- 📅 **Date-aware entries** — Log entries for today, yesterday, or any custom date
- 🔒 **AES-encrypted ZIP** — Your diary is protected before it ever leaves your machine
- ☁️ **Google Drive backup** — Backs up to a folder of your choosing in your own Drive
- 🔄 **Smart update** — If the backup ZIP already exists on Drive, it updates it rather than creating duplicates
- 💾 **Persistent settings** — Remembers your directory and password after the first run
- 🖥️ **Cross-platform** — Linux, macOS, Windows compatible
- 🆓 **Completely free** — Uses Google Drive's free storage tier (15 GB)

---

## 🧰 Prerequisites

Before you start, make sure you have the following installed:

- **Python 3.7+** — [Download here](https://www.python.org/downloads/)
- **pip** — Usually bundled with Python. Verify with `pip --version`
- **Git** *(optional, for cloning)* — [Download here](https://git-scm.com/)

---

## 📦 Installation

It is **strongly recommended** to use a Python virtual environment. This keeps the dependencies for this project isolated from your system Python and prevents version conflicts.

---

### 🐧 Linux Setup

**Step 1: Clone or download the project**
```bash
git clone https://github.com/yourusername/cloudscript-journal.git
cd cloudscript-journal
```

**Step 2: Install the `venv` module** *(if not already installed)*
```bash
sudo apt install python3-venv   # For Debian/Ubuntu-based systems
```

**Step 3: Create a virtual environment**
```bash
python3 -m venv diary_env
```

**Step 4: Activate the virtual environment**
```bash
source diary_env/bin/activate
```
> You should see `(diary_env)` appear at the start of your terminal prompt.

**Step 5: Install the required packages**
```bash
pip install pyzipper google-api-python-client google-auth-oauthlib google-auth-httplib2
```

---

### 🍎 macOS Setup

**Step 1: Clone or download the project**
```bash
git clone https://github.com/yourusername/cloudscript-journal.git
cd cloudscript-journal
```

**Step 2: Create a virtual environment**
```bash
python3 -m venv diary_env
```

**Step 3: Activate the virtual environment**
```bash
source diary_env/bin/activate
```
> You should see `(diary_env)` appear at the start of your terminal prompt.

**Step 4: Install the required packages**
```bash
pip install pyzipper google-api-python-client google-auth-oauthlib google-auth-httplib2
```

---

### 🪟 Windows Setup

**Step 1: Clone or download the project**

Either clone via Git:
```cmd
git clone https://github.com/yourusername/cloudscript-journal.git
cd cloudscript-journal
```
Or download the ZIP from GitHub and extract it.

**Step 2: Create a virtual environment**

Open **Command Prompt** or **PowerShell** in the project folder:
```cmd
python -m venv diary_env
```

**Step 3: Activate the virtual environment**

In **Command Prompt**:
```cmd
diary_env\Scripts\activate.bat
```

In **PowerShell**:
```powershell
diary_env\Scripts\Activate.ps1
```
> If PowerShell gives an error about execution policy, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Step 4: Install the required packages**
```cmd
pip install pyzipper google-api-python-client google-auth-oauthlib google-auth-httplib2
```

---

## ☁️ Google Cloud Console Setup

To enable the Google Drive backup feature, you need to create a Google Cloud project and generate OAuth credentials. Follow these steps carefully:

---

### Step 1 — Go to Google Cloud Console

Visit [https://console.cloud.google.com/](https://console.cloud.google.com/) and sign in with the Google account that owns the Drive you want to back up to.

---

### Step 2 — Create a New Project

1. Click the **project dropdown** at the top-left (next to the Google Cloud logo)
2. Click **"New Project"**
3. Give it a name (e.g., `cloudscript-journal`) and click **"Create"**
4. Wait a moment, then make sure your new project is **selected** in the dropdown

---

### Step 3 — Enable the Google Drive API

1. In the left sidebar, go to **"APIs & Services" → "Library"**
2. Search for **"Google Drive API"**
3. Click on it, then click **"Enable"**

---

### Step 4 — Configure the OAuth Consent Screen

1. Go to **"APIs & Services" → "OAuth consent screen"**
2. Select **"External"** and click **"Create"**
3. Fill in the required fields:
   - **App name**: anything (e.g., `Drive Uploader`)
   - **User support email**: your email address
   - **Developer contact email**: your email address
4. Click **"Save and Continue"** through the Scopes and Test Users steps (no changes needed on those pages)
5. Click **"Back to Dashboard"**

---

### Step 5 — Create OAuth 2.0 Credentials

1. Go to **"APIs & Services" → "Credentials"**
2. Click **"+ Create Credentials"** → **"OAuth client ID"**
3. Set **Application type** to **"Desktop app"**
4. Give it a name (e.g., `diary-desktop`) and click **"Create"**
5. A dialog will appear — click **"Download JSON"**
6. **Rename** the downloaded file to `credentials.json`
7. **Place** `credentials.json` in the **same folder as your Python script**

---

### Step 6 — Add Yourself as a Test User

1. Go to **"APIs & Services" → "OAuth consent screen"**
2. Scroll down to the **"Test users"** section
3. Click **"+ Add Users"** and enter your Google email address
4. Click **"Save"**

> ⚠️ This step is important! Without adding yourself as a test user, Google will block the OAuth login when you try to connect from the script.

---

### Step 7 — Create a Google Drive Folder & Copy the Folder ID

1. Open [Google Drive](https://drive.google.com/) and create a **new folder** (e.g., `My Diary Backup`)
2. Open that folder — look at the URL in your browser. It will look something like:
   ```
   https://drive.google.com/drive/u/1/folders/djfkwfkwjkf12-fefjkwfjkw
   ```
3. The part **after `/folders/`** is your **Folder ID**. In this example: `djfkwfkwjkf12-fefjkwfjkw`
4. Copy this ID — you'll need it in the next step.

---

## 🛠️ Configuration in the Script

Open `Diary_input.py` in any text editor and find this line near the bottom:

```python
gdrive_folder_id = '16meQ9b2wxpSKd-wF73fH01kaoIq84ebs'  # change this with your target folder id
```

Replace the placeholder value with **your own Folder ID** that you copied in the previous step:

```python
gdrive_folder_id = 'YOUR_FOLDER_ID_HERE'
```

Save the file. That's the only code change required.

---

## ▶️ Running the App

Make sure your virtual environment is **activated** before running (you should see `(diary_env)` in your terminal prompt).

### 🐧 Linux & 🍎 macOS
```bash
python3 Diary_input.py
```

### 🪟 Windows
```cmd
python Diary_input.py
```

> On the **first run**, a browser window will open asking you to sign in to Google and grant the app permission to access your Drive. This only happens once — the credentials are saved in `token.json` for future runs.

---

## 🗺️ First Run Walkthrough

Here's what to expect when you run the script for the first time:

```
Hello John!!.
Hope you're having a great day.

Please enter the date for which you want to add contents:
1: for Today, 0 for Yesterday. Else, write a custom date...
> 1

Start entering your inputs (if you want to end, simply type 'END'/'end' on a new line):
> Today I learned about Python virtual environments. Very useful!
> END
Got it!

Using the directory: '/home/john/Documents'. I would save the directory: john_diary_contents in this.
Would I proceed with this?
Y/n: > Y
Ok!

Enter a suitable, strong password for your export zip file:
> ••••••••••

Zipping & encoding your export.

Do you want to backup the diary on cloud?:
Y/n > Y

[Browser opens for Google sign-in on first run]

File uploaded.
```

On subsequent runs, the script will remember your **directory** and **password**, and your Google credentials will already be stored in `token.json` — so there will be no browser prompt.

---

## 📁 File Structure

After a few runs, your project directory will look like this:

```
cloudscript-journal/
│
├── Diary_input.py            ← The main script
├── credentials.json          ← Your Google OAuth credentials (keep private!)
├── token.json                ← Auto-generated after first Google sign-in (keep private!)
├── diary_input.pickle        ← Saves your directory & password for future runs
│
└── (your Documents folder)/
    ├── john_diary_contents/  ← Individual diary entry files (named by date)
    │   ├── 2025-07-10
    │   ├── 2025-07-11
    │   └── ...
    └── diary_content_webpush.zip  ← Encrypted ZIP, also uploaded to Google Drive
```

---

## 🔐 Security Notes

- **AES Encryption**: The ZIP file is encrypted using AES (via `pyzipper`) before uploading. Google Drive cannot read the contents.
- **Your password is stored locally** in `diary_input.pickle` for convenience (so you don't re-enter it every run). Keep this file safe.
- **`credentials.json` and `token.json`** grant access to your Google Drive. Do **not** commit these to version control. They are already in `.gitignore` if you clone this repo.
- **Individual diary text files** are stored unencrypted locally inside the `_diary_contents` folder. The encryption only applies to the ZIP export sent to Google Drive.

---

## 🐛 Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'pyzipper'` | Packages not installed or venv not active | Activate venv and run `pip install pyzipper` |
| `FileNotFoundError: credentials.json` | Credentials file missing | Download from Google Cloud Console and place in same folder as script |
| `Access blocked: This app's request is invalid` | You aren't added as a test user | Add your Google email in OAuth consent screen → Test Users |
| `Token has been expired or revoked` | `token.json` is stale | Delete `token.json` and re-run the script to re-authenticate |
| Google Drive upload fails | Folder ID is wrong | Double-check `gdrive_folder_id` in the script |
| Custom date not accepted | Incorrect format | Use `D/M` or `DD/MM` or `DD/MM/YYYY` |

---

## 📄 License

This project is open-source. Feel free to use, modify, and distribute it. Attribution appreciated!

---

## 🙌 Contributing

Pull requests and suggestions are welcome. If you find a bug or have a feature idea, open an issue!

---

*Built with ❤️ for privacy-first journaling.*
