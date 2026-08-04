import streamlit as st
import json
import subprocess
import sys
from pathlib import Path
import os

# ---------- For port detection ----------
try:
    import serial.tools.list_ports
    PORTS_AVAILABLE = True
except ImportError:
    PORTS_AVAILABLE = False
    st.warning("pyserial not installed. Install it with: pip install pyserial")

# ---------- Page config ----------
st.set_page_config(page_title="ESP32 Config Flasher", layout="centered")
st.title("⚙️ ESP32 Configuration & Flashing")

# ---------- Defaults ----------
DEFAULT_CONFIG = {
    "wifi": {
        "ssid": "Diva AP",
        "password": "Diva@2024"
    },
    "server": {
        "url": "http://192.168.1.50/api"
    }
}

CONFIG_FILE = Path("config_data/config.json")

# ---------- Load existing config ----------
if CONFIG_FILE.exists():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        config = DEFAULT_CONFIG
else:
    config = DEFAULT_CONFIG

# ---------- UI Inputs ----------
st.subheader("📶 Wi‑Fi Settings")
ssid = st.text_input("SSID", value=config.get("wifi", {}).get("ssid", DEFAULT_CONFIG["wifi"]["ssid"]))
password = st.text_input("Password", value=config.get("wifi", {}).get("password", DEFAULT_CONFIG["wifi"]["password"]), type="password")

st.subheader("🌐 Server Settings")
url = st.text_input("Server URL", value=config.get("server", {}).get("url", DEFAULT_CONFIG["server"]["url"]))

# ---------- COM Port Selection ----------
st.subheader("🔌 Serial Port")
if PORTS_AVAILABLE:
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if not ports:
        st.warning("No COM ports detected. Please connect your ESP32 and refresh.")
        selected_port = st.text_input("Or enter port manually", value="COMX")
    else:
        # Default to COM4 if present, otherwise first in list
        default_port = "COM4" if "COM4" in ports else ports[0]
        selected_port = st.selectbox("Select COM port", ports, index=ports.index(default_port) if default_port in ports else 0)
else:
    selected_port = st.text_input("Serial port (e.g., COM1)", value="COM2")

# ---------- Save & Flash Button ----------
if st.button("💾 Save & Update", type="primary"):
    # 1. Build new config
    new_config = {
        "wifi": {
            "ssid": ssid,
            "password": password
        },
        "server": {
            "url": url
        }
    }

    # 2. Write config.json
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=4)
        st.success("✅ config.json saved successfully.")
    except Exception as e:
        st.error(f"❌ Failed to write config.json: {e}")
        st.stop()

    # 3. Run spiffs_builder.py
    st.subheader("🔨 Building SPIFFS image")
    with st.spinner("Running spiffs_builder.py ..."):
        try:
            result_build = subprocess.run(
                [sys.executable, "spiffs_builder.py"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                cwd=Path.cwd()
            )
            st.code(result_build.stdout, language="text")
            if result_build.stderr:
                st.code(result_build.stderr, language="text")
            if result_build.returncode != 0:
                st.error("❌ spiffs_builder.py failed.")
                st.stop()
            else:
                st.success("✅ spiffs_builder.py finished.")
        except FileNotFoundError:
            st.error("❌ spiffs_builder.py not found in the current directory.")
            st.stop()

    # 4. Run flash_spiffs.py with the selected port
    st.subheader("📤 Flashing SPIFFS to ESP32")
    with st.spinner(f"Running flash_spiffs.py on {selected_port} ..."):
        try:
            result_flash = subprocess.run(
                [sys.executable, "flash_spiffs.py", "--port", selected_port],
                capture_output=True,
                text=True,
                encoding='utf-8',
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                cwd=Path.cwd()
            )
            st.code(result_flash.stdout, language="text")
            if result_flash.stderr:
                st.code(result_flash.stderr, language="text")

            # Check for success message or return code
            if result_flash.returncode == 0 :
                st.success("✅ SPIFFS flash terminé – everything succeeded!")
            else:
                st.error("❌ Erreur flash – please check the output above.")
        except FileNotFoundError:
            st.error("❌ flash_spiffs.py not found in the current directory.")
            st.stop()

    st.balloons()