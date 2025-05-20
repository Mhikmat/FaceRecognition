# 🧠 Face Recognition with Siamese Network + Home Assistant

Welcome! This project is a complete, beginner-friendly facial recognition system built with Python, TensorFlow, and Kivy — and even integrates with **Home Assistant** to trigger automations when a specific person is detected.

I forked and improved this from the original by [@nicknochnack](https://github.com/nicknochnack/FaceRecognition). The original repo was great — but some things were outdated or missing. I fixed bugs, made it easier to run, and documented everything for you! 🎯

---

## 📸 What it Does

- Detects if a specific person appears on camera
- Compares the face using a trained Siamese neural network
- Triggers **Home Assistant automations** via webhook when verified (or unverified)
- Can also receive external commands to scan using a simple `curl` command

---

## 🧰 Prerequisites

### ✅ Make sure you have:

- **Anaconda** (for managing environments and launching Jupyter)
- **Git** (to clone the project)
- **Python 3.9+**
- Optional: **CUDA & cuDNN** for GPU acceleration (much faster training!)

---

## 🧪 Step-by-Step Installation (Windows)

### 🧱 1. Make Your Environment with Anaconda

Download: https://www.anaconda.com/download/success  
We use Anaconda to manage dependencies and avoid conflicts.

Once installed, open **Anaconda Prompt** and check:
```bash
conda --version
python --version
```

---

### 🧲 2. Install Git & Clone the Project

Install Git if not already:
```bash
winget install --id Git.Git -e --source winget
```

Clone this repository:
```bash
cd C:
git clone https://github.com/Mhikmat/FaceRecognition.git
```

---

### 💻 3. Make and Activate a Virtual Environment

```bash
cd C:
python -m venv FaceRecognitionEnv
cd FaceRecognitionEnv
.\Scripts\Activate
```

---

### 📚 4. Set Up Jupyter Lab

Install Jupyter and make the kernel:
```bash
pip install ipykernel jupyterlab
python -m ipykernel install --name=FaceRecognitionEnv
jupyter kernelspec list
```

---

### 🚀 5. Open Jupyter Lab

```bash
cd ..\FaceRecognition
jupyter lab
```

> Run the notebook `updated_facial_verification.ipynb`  
> Press `Shift + Enter` to execute each cell.

---

### 📸 6. Image Collection for Training

- If the camera doesn’t work, edit the code to try a different device:
```python
cv2.VideoCapture(0)  ➝  cv2.VideoCapture(1)
```

- Collect:
  - ~300 **anchor** images (`a` key)
  - ~300 **positive** images (`p` key)

---

### 🧠 7. Train the Model

In the notebook, continue running until the model is saved (`model.keras`).  
This is the file you'll later move into the app.

---

## 📦 Setting Up the FaceID App

### 🧩 8. Prepare Files

- Put your trained `model.keras` inside `FaceIDApp/`
- In `faceid.py`, modify the model loading line:
```python
self.model = tf.keras.models.load_model('model.keras', custom_objects={'L1Dist': L1Dist})
```

- Inside `FaceIDApp/verification_images`, add ~30 images (copied from anchor/positive)

---

## 🏠 Home Assistant Integration

### 🔗 9. Webhooks to Automate Actions

Your `faceid.py` already has webhook logic:

```python
# Verified
http://homeassistant.local:8123/api/webhook/faceid_verified

# Unverified
http://homeassistant.local:8123/api/webhook/faceid_unverified
```

In Home Assistant:
- Go to ⚙️ Settings → Automations → ➕ New Automation
- Choose “Webhook” as the trigger
- Use `faceid_verified` or `faceid_unverified` as the webhook ID
- Set actions like turning on lights or sending a notification

---

## 🌐 External Scan Command

You can trigger the scan remotely using a simple `curl`:
```bash
curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d "{\"status\": \"scan\"}"
```

---

## 🟢 Run the App

Inside the `FaceIDApp` folder:
```bash
python faceid.py
```

---

## 📝 Summary

✅ Model training via Jupyter  
✅ Live camera detection  
✅ Verified = webhook trigger  
✅ Unverified = webhook trigger  
✅ External trigger via API  
✅ Home Assistant integration

---

## 💡 Tips

- More verification images = better accuracy  
- Make sure lighting is consistent  
- GPU will greatly reduce training time (install CUDA Toolkit)

---

## 📥 Bonus

You can find a full **Batch Setup Script** in the repo:  
➡️ `README_FaceRecognition_Setup.bat`

Just run it and follow the prompts.

---

## 🙌 Credits

Forked from [nicknochnack/FaceRecognition](https://github.com/nicknochnack/FaceRecognition)  
Adapted and improved by [@Mhikmat](https://github.com/Mhikmat)
