import os
import streamlit as st
from pathlib import Path
import toml

def inject_secrets_to_env():

    def flatten(d, parent=""):
        items = {}
        for k, v in d.items():
            key = f"{parent}_{k}".upper() if parent else k.upper()
            if isinstance(v, dict):
                items.update(flatten(v, key))
            else:
                items[key] = str(v)
        return items

    # Try Streamlit secrets first
    try:
        secrets = st.secrets
        # Force access to trigger error if not available
        _ = secrets.keys()
    except Exception:
        # Fallback: load from project root
        root = Path(__file__).resolve().parents[1]
        secrets_path = root / ".streamlit" / "secrets.toml"

        if not secrets_path.exists():
            raise FileNotFoundError(f"Secrets file not found at {secrets_path}")

        secrets = toml.load(secrets_path)

    flat = flatten(secrets)

    for k, v in flat.items():
        os.environ[k] = v
