import pyttsx3

voz_activada = True

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)


def hablar(texto):
    if voz_activada:
        engine.say(texto)
        engine.runAndWait()


def activar_voz():
    global voz_activada
    voz_activada = True


def desactivar_voz():
    global voz_activada
    voz_activada = False
