# AP Comment Reply Generator

A simple Streamlit app to generate thoughtful, AP-style replies to social media comments using Claude.

---

## 🚀 Run Locally (Linux)

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd app
```

### 2. Install virtual environment support
```bash
sudo apt update
sudo apt install python3-venv
```

### 3. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set environment variable
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

### 6. Run the app
```bash
streamlit run main.py
```

---

## 🌐 Deploy (Streamlit Cloud)

1. Push your code to GitHub  
2. Go to https://streamlit.io/cloud  
3. Create a new app and select your repo  
4. In **Secrets**, add:
```
ANTHROPIC_API_KEY=your_api_key_here
```
5. Deploy  

---

Done. Open the app and start generating replies.