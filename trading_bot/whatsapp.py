import pywhatkit as kit
import datetime

whatsapp_activado = True
numero_destino = '+541123961619'  # Podés cambiarlo dinámicamente si querés


def activar_whatsapp():
    global whatsapp_activado
    whatsapp_activado = True


def desactivar_whatsapp():
    global whatsapp_activado
    whatsapp_activado = False


def enviar_mensaje(mensaje):
    if not whatsapp_activado:
        return

    ahora = datetime.datetime.now()
    hora = ahora.hour
    minuto = ahora.minute + 1 if ahora.second > 50 else ahora.minute + 2
    if minuto >= 60:
        hora += 1
        minuto = 0

    try:
        kit.sendwhatmsg(numero_destino, mensaje, hora, minuto, wait_time=10, tab_close=True)
    except Exception as e:
        print(f"[WhatsApp] Error al enviar mensaje: {e}")
