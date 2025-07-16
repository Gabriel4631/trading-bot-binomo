import time
import random
from utils.config import guardar_saldo, obtener_saldo_actual
from historial import guardar_operacion
from voz import hablar

try:
    from whatsapp import enviar_mensaje
except:
    def enviar_mensaje(msg): pass  # fallback si no hay WhatsApp

bot_activo = True

def detener_bot():
    global bot_activo
    bot_activo = False

def ciclo_de_operaciones(inversion_inicial, meta_final, tiempo_op, capital_total, voz_activa=True, whatsapp_activo=True):
    global bot_activo
    bot_activo = True

    saldo_actual = obtener_saldo_actual()

    if capital_total > 0 and saldo_actual == 0:
        saldo_actual = capital_total
        guardar_saldo(saldo_actual)

    print(f"\n🔄 Nuevo ciclo: capital disponible ${saldo_actual}, objetivo ${meta_final}")
    if voz_activa:
        hablar(f"Nuevo ciclo iniciado. Capital disponible: {saldo_actual} pesos. Objetivo: {meta_final} pesos.")
    if whatsapp_activo:
        enviar_mensaje(f"📊 Nuevo ciclo iniciado. Capital: ${saldo_actual}. Meta: ${meta_final}.")

    ronda = 1
    inversion = inversion_inicial
    acumulado = 0

    while bot_activo:
        if saldo_actual < inversion:
            print("⚠️ Saldo insuficiente para continuar operando.")
            if voz_activa:
                hablar("Saldo insuficiente para continuar operando.")
            break

        resultado = random.choice(["ganancia"] * 3 + ["perdida"])

        if resultado == "ganancia":
            ganancia = int(inversion * 0.8)
            saldo_actual += ganancia
            acumulado += inversion + ganancia
            print(f"✅ Ronda {ronda}: +${ganancia} (Saldo: ${saldo_actual})")
            if voz_activa:
                hablar(f"Ronda {ronda}: ganancia de {ganancia} pesos.")
            guardar_operacion("USD/ARS", "ganancia", inversion)
            ronda += 1
            inversion += ganancia
        else:
            print(f"❌ Ronda {ronda}: -${inversion} (Saldo: ${saldo_actual - inversion})")
            if voz_activa:
                hablar(f"Ronda {ronda}: pérdida de {inversion} pesos.")
            saldo_actual -= inversion
            guardar_operacion("USD/ARS", "perdida", inversion)
            ronda = 1
            inversion = inversion_inicial
            acumulado = 0

        guardar_saldo(saldo_actual)

        if acumulado >= meta_final:
            print(f"🎯 Meta alcanzada: ${acumulado}. Reiniciando ciclo.")
            if voz_activa:
                hablar(f"Meta de ciclo alcanzada: {acumulado} pesos.")
            if whatsapp_activo:
                enviar_mensaje(f"🎯 Meta alcanzada: ${acumulado}. Reiniciando ciclo.")
            ronda = 1
            acumulado = 0
            inversion = inversion_inicial

        if saldo_actual >= 1_000_000:
            print("🎉 ¡Meta total alcanzada: $1.000.000! Deteniendo bot.")
            if voz_activa:
                hablar("Meta total alcanzada: un millón de pesos.")
            if whatsapp_activo:
                enviar_mensaje("🎉 ¡Meta total alcanzada: $1.000.000! El bot se detiene.")
            bot_activo = False

        if not bot_activo:
            print("⏹ Bot detenido por el usuario.")
            if voz_activa:
                hablar("Bot detenido por el usuario.")
            if whatsapp_activo:
                enviar_mensaje("⏹ Bot detenido manualmente.")
            break

        time.sleep(1 if tiempo_op == "30s" else 2 if tiempo_op == "1min" else 3)
