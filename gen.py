import random
import pandas as pd

expresiones = {
    "vista": {
        0: [
            "soy ciego parcialmente", "no veo nada", "tengo ceguera total", "veo muy mal",
            "tengo muy poca vision", "no veo casi nada", "tengo vision nula",
            "veo todo muy borroso", "uso baston para ciegos", "no veo en absoluto",
            "me duelen los ojos", "tengo dolor ocular", "me duele el ojo",
            "he perdido la vista", "perdi el ojo", "soy tuerto", "dolor de ojos",
            "no tengo ojos", "no me funcionan los ojos", "ciego de nacimiento",
            "toy ciego", "no distingo formas ni colores", "casi no tengo vista"
        ],
        1: [
            "veo bien", "mi vista es normal", "uso gafas para leer", "tengo vision normal",
            "veo perfectamente", "sin problemas de vista", "llevo lentillas y veo bien",
            "mi agudeza visual es correcta", "veo lo estandar", "de la vista ando bien",
            "no tengo problemas en los ojos", "todo ok con la vista"
        ],
        2: [
            "tengo fotofobia", "me molesta mucho la luz", "tengo hipersensibilidad visual",
            "la luz me deslumbra demasiado", "hipersensibilidad a la luz",
            "veo destellos constantemente", "los brillos me hacen daño en los ojos",
            "no soporto las luces brillantes", "vista de aguila", "hipervision",
            "luz solar me ciega", "pantallas muy brillantes me duelen", "necesito ambiente oscuro", 
            "ojos sensibles"
        ]
    },
    "oido": {
        0: [
            "soy sordo", "no oigo nada", "tengo sordera profunda", "oigo muy mal",
            "tengo muy poca audicion", "no escucho nada", "tengo audicion nula",
            "escucho todo muy apagado", "uso lenguaje de senas", "tapon en el oido",
            "no tengo orejas", "sin sentido del oido", "no me funcionan los oidos",
            "toy sordo", "sordo total", "escucho cero", "no oigo ni papa"
        ],
        1: [
            "oigo bien", "mi oido es normal", "escucho perfectamente", "tengo audicion normal",
            "sin problemas de oido", "escucho las conversaciones sin problema",
            "de oido ando perfecto", "audicion sin problemas", "oigo genial"
        ],
        2: [
            "tengo hiperacusia", "me molestan mucho los ruidos", "tengo hipersensibilidad auditiva",
            "escucho los ruidos demasiado fuertes", "los sonidos agudos me dan dolor de cabeza",
            "no soporto el volumen alto", "oido demasiado sensible", "hiperaudicion",
            "el ruido fuerte me daña", "sensible a pitidos", "ruido ambiental me agobia", "orejas sensibles"
        ]
    },
    "movilidad": {
        0: [
            "ando en silla de ruedas", "soy paralitico", "soy paraplejico", "no puedo caminar",
            "tengo movilidad muy reducida", "ando con muletas", "no puedo mover las piernas",
            "estoy inmovilizado", "me cuesta mucho caminar", "camino muy lento", "estoy postrado",
            "no tengo piernas", "voy en silla", "no puedo andar", "invalido", "ando cojo",
            "me fallan las piernas", "dificultad severa para moverme", "no tengo piernas", "camino con baston",
            "no puedo subir escaleras", "camino con mueletas"
        ],
        1: [
            "camino bien", "mi movilidad es normal", "puedo andar sin problemas", "camino perfectamente",
            "sin problemas de movilidad", "me muevo con normalidad", "ando bien de las piernas",
            "movilidad estandar", "ningun problema para caminar"
        ],
        2: [
            "tengo hiperactividad", "soy hiperactivo", "no me puedo quedar quieto",
            "tengo necesidad constante de moverme", "tengo tics motores",
            "me muevo compulsivamente", "inquietud motora extrema", "hipermovilidad",
            "necesito espacio amplio", "no soporto estar atrapado", "necesidad de moverme siempre", 
            "tengo tdah", "diagnosticado de tdah", "sufro tdah"
        ]
    }
}

conectores = [", ", " y ", " pero ", " aunque ", ". ", " ademas ", ", por otro lado ", " "]

filas = []

for _ in range(5000):
    v = random.choice([0, 1, 2])
    o = random.choice([0, 1, 2])
    m = random.choice([0, 1, 2])
    
    txt_v = random.choice(expresiones["vista"][v])
    txt_o = random.choice(expresiones["oido"][o])
    txt_m = random.choice(expresiones["movilidad"][m])
    
    tipo = random.choices(["corta", "doble", "triple"], weights=[0.35, 0.35, 0.30])[0]
    
    if tipo == "corta":
        cat = random.choice(["vista", "oido", "movilidad"])
        if cat == "vista":
            filas.append({"texto": txt_v, "vista": v, "oido": 1, "movilidad": 1})
        elif cat == "oido":
            filas.append({"texto": txt_o, "vista": 1, "oido": o, "movilidad": 1})
        else:
            filas.append({"texto": txt_m, "vista": 1, "oido": 1, "movilidad": m})
            
    elif tipo == "doble":
        cats = random.sample([
            ("vista", txt_v, v), 
            ("oido", txt_o, o), 
            ("movilidad", txt_m, m)
        ], 2)
        c = random.choice(conectores)
        frase = f"{cats[0][1]}{c}{cats[1][1]}"
        
        vals = {"vista": 1, "oido": 1, "movilidad": 1}
        vals[cats[0][0]] = cats[0][2]
        vals[cats[1][0]] = cats[1][2]
        
        filas.append({"texto": frase, "vista": vals["vista"], "oido": vals["oido"], "movilidad": vals["movilidad"]})
        
    else:
        elementos = [(txt_v, v), (txt_o, o), (txt_m, m)]
        random.shuffle(elementos)
        c1 = random.choice(conectores)
        c2 = random.choice(conectores)
        frase = f"{elementos[0][0]}{c1}{elementos[1][0]}{c2}{elementos[2][0]}."
        filas.append({"texto": frase, "vista": v, "oido": o, "movilidad": m})

df = pd.DataFrame(filas).sample(frac=1).reset_index(drop=True)
df.to_csv("dataset.csv", index=False, encoding="utf-8")
