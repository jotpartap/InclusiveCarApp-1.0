import random
import pandas as pd

expresiones = {
    "vista": {
        0: [
            "soy ciego", "no veo nada", "tengo ceguera total", "veo muy mal",
            "tengo muy poca vision", "no veo casi nada", "tengo vision nula",
            "veo todo muy borroso", "uso baston para ciegos", "no veo en absoluto"
        ],
        1: [
            "veo bien", "mi vista es normal", "uso gafas para leer", "tengo vision normal",
            "veo perfectamente", "sin problemas de vista", "llevo lentillas y veo bien"
        ],
        2: [
            "tengo fotofobia", "me molesta mucho la luz", "tengo hipersensibilidad visual",
            "la luz me deslumbra demasiado", "tengo hipersensibilidad a la luz",
            "veo destellos constantemente", "los brillos me hacen daño en los ojos",
            "tengo sensibilidad extrema a la luz", "no soporto las luces brillantes"
        ]
    },
    "oido": {
        0: [
            "soy sordo", "no oigo nada", "tengo sordera profunda", "oigo muy mal",
            "tengo muy poca audicion", "no escucho nada", "tengo audicion nula",
            "escucho todo muy apagado", "uso lenguaje de senas", "no escucho en absoluto"
        ],
        1: [
            "oigo bien", "mi oido es normal", "escucho perfectamente", "tengo audicion normal",
            "sin problemas de oido", "escucho las conversaciones sin problema", "oigo lo normal"
        ],
        2: [
            "tengo hiperacusia", "me molestan mucho los ruidos", "tengo hipersensibilidad auditiva",
            "escucho los ruidos demasiado fuertes", "los sonidos agudos me dan dolor de cabeza",
            "tengo hipersensibilidad al ruido", "no soporto el volumen alto",
            "tengo un oido demasiado sensible", "los ruidos fuertes me aturden"
        ]
    },
    "movilidad": {
        0: [
            "ando en silla de ruedas", "soy paralitico", "soy paraplejico", "no puedo caminar",
            "tengo movilidad muy reducida", "ando con muletas", "no puedo mover las piernas",
            "estoy inmovilizado", "me cuesta mucho caminar", "tengo problemas al caminar",
            "tengo dificultad para andar", "camino muy lento", "soy muy lento caminando"
        ],
        1: [
            "camino bien", "mi movilidad es normal", "puedo andar sin problemas", "camino perfectamente",
            "sin problemas de movilidad", "puedo caminar y correr", "me muevo con normalidad"
        ],
        2: [
            "tengo hiperactividad", "soy hiperactivo", "no me puedo quedar quieto",
            "tengo necesidad constante de moverme", "tengo tics motores",
            "me muevo compulsivamente", "tengo inquietud motora extrema",
            "tengo exceso de movimiento", "no puedo estar sentado mucho tiempo"
        ]
    }
}

conectores = [", ", " y ", " pero ", " aunque ", ". ", " ademas ", ", por otro lado "]

filas = []

for _ in range(6767):
    v = random.choice([0, 1, 2])
    o = random.choice([0, 1, 2])
    m = random.choice([0, 1, 2])
    
    txt_v = random.choice(expresiones["vista"][v])
    txt_o = random.choice(expresiones["oido"][o])
    txt_m = random.choice(expresiones["movilidad"][m])
    
    tipo = random.choices(["corta", "combinada"], weights=[0.40, 0.60])[0]
    
    if tipo == "corta":
        cat = random.choice(["vista", "oido", "movilidad"])
        if cat == "vista":
            filas.append({"texto": txt_v, "vista": v, "oido": 1, "movilidad": 1})
        elif cat == "oido":
            filas.append({"texto": txt_o, "vista": 1, "oido": o, "movilidad": 1})
        else:
            filas.append({"texto": txt_m, "vista": 1, "oido": 1, "movilidad": m})
    else:
        c1 = random.choice(conectores)
        c2 = random.choice(conectores)
        frase = f"{txt_v}{c1}{txt_o}{c2}{txt_m}."
        filas.append({"texto": frase, "vista": v, "oido": o, "movilidad": m})
    
df = pd.DataFrame(filas).sample(frac=1).reset_index(drop=True)
df.to_csv("dataset.csv", index=False, encoding="utf-8")
