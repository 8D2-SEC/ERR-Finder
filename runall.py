import subprocess
import os

scripts = [
    ("Recolectando URLs con py", ["python", "py"]),
    ("Escaneando vulnerabilidades", ["python3", "scan.py", "-f", "targets.txt"]),
    ("Extrayendo correos", ["python", "scancorreo.py"]),
    ("Enviando correos", ["python", "emails.py"])
]

for desc, command in scripts:
    print(f"\n=== {desc} ===")
    try:
        if not os.path.isfile(command[1]):
            print(f"[ERROR] El archivo {command[1]} no existe.")
            continue

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falló al ejecutar {command[1]}: {e}")
