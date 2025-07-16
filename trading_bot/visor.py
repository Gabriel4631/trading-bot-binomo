import pytesseract
import cv2
import numpy as np
import pyautogui
import re
import time
import os

# Ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detectar_saldo():
    print("📷 Presioná Ctrl+C para frenar.")
    while True:
        try:
            # Captura de pantalla completa
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Recorte de región del saldo - AJUSTABLE
            x, y, w, h = 1085, 70, 220, 50  # Modificá estas coordenadas si hace falta
            recorte = frame[y:y+h, x:x+w]

            # Preprocesamiento para mejorar OCR
            gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
            _, umbral = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)

            # OCR
            texto = pytesseract.image_to_string(umbral)
            texto_limpio = texto.strip().replace('\n', '')
            print(f"🧾 Texto bruto: {texto_limpio}")

            # Buscar patrón de saldo en formato "Arg$2,236,520.00"
            match = re.search(r"Arg\$?([0-9.,]+)", texto_limpio)
            if match:
                saldo = match.group(1).replace(".", "").replace(",", ".")
                try:
                    saldo_num = float(saldo)
                    print(f"💰 Saldo detectado: {saldo_num}")
                except ValueError:
                    print("❌ No se detectó un saldo válido.")
            else:
                print("❌ No se detectó un saldo válido.")

            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Finalizado por el usuario.")
            break

# Ejecutar
if __name__ == "__main__":
    detectar_saldo()