import os

ARCHIVO_SALDO = "saldo.txt"

def guardar_saldo(valor):
    with open(ARCHIVO_SALDO, "w") as f:
        f.write(str(valor))

def obtener_saldo_actual():
    if not os.path.exists(ARCHIVO_SALDO):
        return 0
    with open(ARCHIVO_SALDO, "r") as f:
        return int(f.read().strip())
