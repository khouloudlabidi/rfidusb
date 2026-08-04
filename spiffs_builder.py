from pathlib import Path
import subprocess


# ============================================================
# Chemins projet
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MKSPIFFS = BASE_DIR / "tools" / "mkspiffs.exe"

CONFIG_DIR = BASE_DIR / "config_data"

OUTPUT_DIR = BASE_DIR / "config_build"

SPIFFS_BIN = OUTPUT_DIR / "spiffs.bin"


# ============================================================
# Paramètres SPIFFS ESP32
# Compatible :
# Default 4MB with SPIFFS
# (1.2MB APP / 1.5MB SPIFFS)
# ============================================================

SPIFFS_SIZE = "0x160000"   # 1507328 octets
PAGE_SIZE = "256"
BLOCK_SIZE = "4096"


OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# Vérification fichiers source
# ============================================================

def verify_source():

    print("\n===== SOURCE SPIFFS =====")

    if not CONFIG_DIR.exists():

        raise Exception(
            f"Dossier absent : {CONFIG_DIR}"
        )


    files = list(CONFIG_DIR.iterdir())


    if len(files) == 0:

        raise Exception(
            "Le dossier config_data est vide"
        )


    for file in files:

        print(
            file.name,
            file.stat().st_size,
            "octets"
        )


    print("========================\n")



# ============================================================
# Création image SPIFFS
# ============================================================

def build_spiffs():


    # Vérifier mkspiffs

    if not MKSPIFFS.exists():

        raise FileNotFoundError(
            f"mkspiffs introuvable : {MKSPIFFS}"
        )


    # Vérifier config_data

    verify_source()



    # Supprimer ancien fichier

    if SPIFFS_BIN.exists():

        SPIFFS_BIN.unlink()



    cmd = [

        str(MKSPIFFS),

        "-c",
        str(CONFIG_DIR),

        "-b",
        BLOCK_SIZE,

        "-p",
        PAGE_SIZE,

        "-s",
        SPIFFS_SIZE,

        str(SPIFFS_BIN)

    ]


    print("Création SPIFFS...")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )


    if result.returncode != 0:

        print(result.stdout)
        print(result.stderr)

        raise Exception(
            "Erreur création SPIFFS"
        )



    print("\n===== RESULTAT =====")

    print(
        "SPIFFS créé :",
        SPIFFS_BIN
    )


    print(
        "Taille image :",
        SPIFFS_BIN.stat().st_size,
        "octets"
    )


    print("====================\n")


    return str(SPIFFS_BIN)



# ============================================================
# Test direct
# ============================================================

if __name__ == "__main__":


    file = build_spiffs()


    print(
        "Fichier généré :",
        file
    )