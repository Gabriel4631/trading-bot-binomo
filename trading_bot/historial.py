import os
import json
from datetime import datetime

RUTA_HISTORIAL = "historial.json"

def guardar_operacion(activo, resultado, monto):
    historial = leer_historial()
    fecha = datetime.now().strftime("%Y-%m-%d")
    operacion = {
        "fecha": fecha,
        "activo": activo,
        "resultado": resultado,
        "monto": monto
    }
    historial.append(operacion)
    with open(RUTA_HISTORIAL, "w") as archivo:
        json.dump(historial, archivo, indent=4)

def leer_historial():
    if not os.path.exists(RUTA_HISTORIAL):
        return []
    with open(RUTA_HISTORIAL, "r") as archivo:
        return json.load(archivo)

def borrar_historial():
    if os.path.exists(RUTA_HISTORIAL):
        os.remove(RUTA_HISTORIAL)
    with open(RUTA_HISTORIAL, "w") as archivo:
        json.dump([], archivo)
