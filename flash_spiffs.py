import subprocess
from pathlib import Path
import argparse

#PORT = "COM17"
# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Flash SPIFFS to ESP32"
)

parser.add_argument(
    "--port",
    required=True,
    help="ESP32 COM port (e.g. COM17)"
)

args = parser.parse_args()

PORT = args.port
SPIFFS_BIN = Path(
    "config_build/spiffs.bin"
)


ADDRESS = "0x290000"


if not SPIFFS_BIN.exists():

    raise Exception(
        "spiffs.bin absent"
    )


cmd = [

    "python",
    "-m",
    "esptool",

    "--chip",
    "esp32",

    "--port",
    PORT,

    "--baud",
    "115200",

    "write-flash",

    ADDRESS,

    str(SPIFFS_BIN)

]


print("Flash SPIFFS...")

result = subprocess.run(
    cmd,
    capture_output=True,
    text=True
)


print("\n===== OUTPUT =====")

print(result.stdout)

print(result.stderr)


if result.returncode == 0:

    print(
        "✅ SPIFFS flash terminé"
    )

else:

    print(
        "❌ Erreur flash"
    )