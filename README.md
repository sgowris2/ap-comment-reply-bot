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

### 5. Set up secrets

Create a `.streamlit` folder and add a `secrets.toml` file:

```bash
mkdir -p .streamlit
```

Copy from the example:

```bash
cp streamlit.toml.example .streamlit/secrets.toml
```

Then update values in `.streamlit/secrets.toml`:

* `api_keys.anthropic` → your Anthropic API key
* `auth.password_pepper` → a secure random string
* `auth.admin` and `auth.users` → credentials (use hashed passwords — see below)
* `supabase` → your project credentials (if used)

---

### 🔐 Hashing Passwords (Recommended)

Passwords should be stored as **bcrypt hashes**, not plain text.

You can use the provided utility:

```bash
python utils/hash_password.py
```

You’ll be prompted to:

* Enter password
* Enter pepper (should match `auth.password_pepper` in `secrets.toml`)

The script will output a hashed password like:

```
$2b$12$...
```

Copy this value into your `.streamlit/secrets.toml`:

```toml
[auth.admin]
username = "admin"
password = "$2b$12$..."
```

⚠️ Important:

* Use the **same pepper** during hashing and in `secrets.toml`
* Do not commit real credentials to Git

---

### 6. Run the app

```bash
streamlit run main.py
```

---

## 🌐 Deploy (Streamlit Cloud)

1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Create a new app and select your repo
4. In **Secrets**, paste the contents of your `secrets.toml` (same structure as example)
5. Deploy

---

Done. Open the app and start generating replies.
