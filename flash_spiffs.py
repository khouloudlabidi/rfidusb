import subprocess
from pathlib import Path


PORT = "COM8"

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
    "460800",

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