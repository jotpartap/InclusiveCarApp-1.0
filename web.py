import streamlit as st
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

st.set_page_config(
    page_title="InclusiveCarApp",
    page_icon="logo.jpeg",
    layout="wide"
)

col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    st.image("logo.jpeg", width=100)

with col_titulo:
    st.title("InclusiveCarApp 1.0")

CANALES = {
    (0, 0, 0): {
        "auditivo": "OFF (Ahorro)",
        "visual": "OFF (Ahorro)",
        "haptico": "MÁXIMO: Vibraciones codificadas, Braille al alcance de la silla.",
        "gestual": "Rampa ON. Reconocimiento de pequeños gestos manuales."
    },
    (0, 0, 1): {
        "auditivo": "OFF (Ahorro)",
        "visual": "MÁXIMO: Lengua de signos, pictogramas grandes.",
        "haptico": "ALTO: Vibración para dirigir la mirada a la pantalla.",
        "gestual": "Rampa ON. Lee gestos de cabeza y manos."
    },
    (0, 0, 2): {
        "auditivo": "OFF (Ahorro)",
        "visual": "OSCURO: Pictogramas muy claros sobre fondo negro mate.",
        "haptico": "ALTO: Suple la visión atenuada y la sordera.",
        "gestual": "Rampa ON. Reconocimiento de gestos."
    },
    (0, 1, 0): {
        "auditivo": "MÁXIMO: Asistente de voz descriptivo total.",
        "visual": "OFF (Ahorro)",
        "haptico": "ALTO: Vibración de confirmación de acciones.",
        "gestual": "Rampa ON. Micrófonos a la altura de la silla."
    },
    (0, 1, 1): {
        "auditivo": "NORMAL",
        "visual": "NORMAL: Pantallas bajas (al alcance de la silla).",
        "haptico": "NORMAL: Alertas de emergencia.",
        "gestual": "Rampa ON. Botones al alcance o gestos manuales."
    },
    (0, 1, 2): {
        "auditivo": "NORMAL: Asistente de voz cobra relevancia.",
        "visual": "OSCURO: Pantallas atenuadas a la altura de la silla.",
        "haptico": "NORMAL",
        "gestual": "Rampa ON."
    },
    (0, 2, 0): {
        "auditivo": "SUAVE: Voz susurrada + cancelación de ruido.",
        "visual": "OFF (Ahorro)",
        "haptico": "ALTO: Pasa a ser el canal principal.",
        "gestual": "Rampa ON."
    },
    (0, 2, 1): {
        "auditivo": "SUAVE: Cancelación activa de ruido ambiental.",
        "visual": "NORMAL: Pantallas adaptadas en altura.",
        "haptico": "NORMAL",
        "gestual": "Rampa ON."
    },
    (0, 2, 2): {
        "auditivo": "SUAVE: Cancelación activa de ruido.",
        "visual": "OSCURO: Ambiente de baja carga cognitiva.",
        "haptico": "NORMAL",
        "gestual": "Rampa ON. Conducción ultrasuave automática."
    },
    
    (1, 0, 0): {
        "auditivo": "OFF (Ahorro)",
        "visual": "OFF (Ahorro)",
        "haptico": "MÁXIMO: Guía táctil integral por todo el habitáculo.",
        "gestual": "Estándar."
    },
    (1, 0, 1): {
        "auditivo": "OFF (Ahorro)",
        "visual": "MÁXIMO: Lengua de signos y alertas luminosas.",
        "haptico": "ALTO: Vibración de llamada de atención.",
        "gestual": "Estándar."
    },
    (1, 0, 2): {
        "auditivo": "OFF (Ahorro)",
        "visual": "OSCURO: Pictogramas claros de alto contraste.",
        "haptico": "ALTO",
        "gestual": "Estándar."
    },
    (1, 1, 0): {
        "auditivo": "MÁXIMO: Asistente de voz descriptivo.",
        "visual": "OFF (Ahorro)",
        "haptico": "ALTO: Pulsera/asiento vibra al llegar.",
        "gestual": "Estándar."
    },
    (1, 1, 1): {
        "auditivo": "NORMAL",
        "visual": "NORMAL",
        "haptico": "NORMAL",
        "gestual": "Estándar."
    },
    (1, 1, 2): {
        "auditivo": "NORMAL",
        "visual": "OSCURO: Cristales opacos por defecto.",
        "haptico": "NORMAL",
        "gestual": "Estándar."
    },
    (1, 2, 0): {
        "auditivo": "SUAVE: Voz susurrada + cancelación de ruido.",
        "visual": "OFF (Ahorro)",
        "haptico": "ALTO: Pasa a ser el canal principal.",
        "gestual": "Estándar."
    },
    (1, 2, 1): {
        "auditivo": "SUAVE: Cancelación de ruido.",
        "visual": "NORMAL",
        "haptico": "NORMAL",
        "gestual": "Estándar."
    },
    (1, 2, 2): {
        "auditivo": "SUAVE: Cancelación de ruido.",
        "visual": "OSCURO",
        "haptico": "OFF",
        "gestual": "Estándar."
    },

    (2, 0, 0): {
        "auditivo": "OFF (Ahorro)",
        "visual": "OFF (Ahorro)",
        "haptico": "MODERADO: Vibraciones suaves para no sobreestimular.",
        "gestual": "Espacio amplio, cinturones adaptativos."
    },
    (2, 0, 1): {
        "auditivo": "OFF (Ahorro)",
        "visual": "MINIMIZADO",
        "haptico": "MODERADO: Pictogramas grandes sin destellos estridentes.",
        "gestual": "Espacio libre para moverse con seguridad."
    },
    (2, 0, 2): {
        "auditivo": "OFF (Ahorro)",
        "visual": "MINIMIZADO",
        "haptico": "OSCURO EXTREMO: Iluminación prácticamente nula.",
        "gestual": "Espacio adaptativo."
    },
    (2, 1, 0): {
        "auditivo": "MODERADO: Voz calmada y clara.",
        "visual": "OFF (Ahorro)",
        "haptico": "MINIMIZADO: Solo alertas críticas.",
        "gestual": "Espacio libre, bloqueo seguro de puertas."
    },
    (2, 1, 1): {
        "auditivo": "NORMAL",
        "visual": "MINIMIZADO",
        "haptico": "NORMAL: Juegos/distracciones en pantalla para relajar.",
        "gestual": "Máxima libertad de movimiento segura."
    },
    (2, 1, 2): {
        "auditivo": "NORMAL",
        "visual": "OSCURO",
        "haptico": "OFF",
        "gestual": "Espacio amplio."
    },
    (2, 2, 0): {
        "auditivo": "MUY SUAVE: Solo alertas vitales.",
        "visual": "OFF (Ahorro)",
        "haptico": "MINIMIZADO: Evitar sobrecarga sensorial.",
        "gestual": "Espacio libre, máximo aislamiento exterior."
    },
    (2, 2, 1): {
        "auditivo": "OFF / SUAVE: Aislamiento total del ruido exterior (TEA).",
        "visual": "RELAX: Colores pastel, rutas suaves (sin curvas bruscas).",
        "haptico": "OFF: Cero vibraciones innecesarias.",
        "gestual": "Ambiente zen, sin bloqueos físicos restrictivos."
    },
    (2, 2, 2): {
        "auditivo": "AISLAMIENTO: Silencio absoluto (ANC al máximo*).",
        "visual": "OSCURO TOTAL: Cápsula de aislamiento visual.",
        "haptico": "OFF: Cero estímulos.",
        "gestual": 'Máximo confort, cinturón envolvente relajante tipo "abrazo".'
    }
}

@st.cache_resource
def cargar_modelos():
    encoder = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')
    
    data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine='python')
    data.columns = data.columns.str.strip()
    
    X_embeddings = encoder.encode(data["texto"].tolist(), show_progress_bar=False)
    
    vista = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    vista.fit(X_embeddings, data["vista"])
    
    oido = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    oido.fit(X_embeddings, data["oido"])
    
    mov = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    mov.fit(X_embeddings, data["movilidad"])
    
    return encoder, vista, oido, mov

encoder, vista, oido, mov = cargar_modelos()

def predecir_texto(texto):
    if not texto.strip():
        return 1, 1, 1
    
    emb = encoder.encode([texto])

    m = int(mov.predict(emb)[0])
    o = int(oido.predict(emb)[0])
    v = int(vista.predict(emb)[0])

    return m, o, v

def mostrar_canales(m, o, v):
    st.markdown(f"### [M, O, V]: `[{m}, {o}, {v}]`")
    
    config = CANALES.get((m, o, v), {
        "auditivo": "Configuración estándar",
        "visual": "Configuración estándar",
        "haptico": "Configuración estándar",
        "gestual": "Configuración estándar"
    })
    
    df_canales = pd.DataFrame([{
        "Canal Auditivo (Voz)": config["auditivo"],
        "Canal Visual (Pantallas/Luces)": config["visual"],
        "Canal Háptico (Tacto)": config["haptico"],
        "Canal Gestual / Motriz": config["gestual"]
    }])
    
    st.table(df_canales)

def preprocesar_texto(texto):
    if not texto or not texto.strip():
        return "", "", ""

    texto = texto.lower().strip()
    texto = " ".join(texto_limpio.split())

    conectores = r'\b(?:y|e|o|u|pero|además|ademas|mientras|que|también|tambien)\b|[,;.:!?¡¿]'
    fragmentos = [f.strip() for f in re.split(conectores, texto, flags=re.IGNORECASE) if f.strip()]

    if not fragmentos:
        fragmentos = [texto]

    frag_m, frag_o, frag_v = [], [], []

    for frag in fragmentos:
        emb = encoder.encode([frag])

        pred_m = int(mov.predict(emb)[0])
        pred_o = int(oido.predict(emb)[0])
        pred_v = int(vista.predict(emb)[0])

        prob_m = max(mov.predict_proba(emb)[0])
        prob_o = max(oido.predict_proba(emb)[0])
        prob_v = max(vista.predict_proba(emb)[0])

        puntuaciones = {
            'mov': prob_m * 2.0 if pred_m != 1 else prob_m * 0.5,
            'oido': prob_o * 2.0 if pred_o != 1 else prob_o * 0.5,
            'vista': prob_v * 2.0 if pred_v != 1 else prob_v * 0.5
        }

        canal_ganador = max(puntuaciones, key=puntuaciones.get)

        if canal_ganador == 'mov':
            frag_m.append(frag)
        elif canal_ganador == 'oido':
            frag_o.append(frag)
        else:
            frag_v.append(frag)

    t_m = " ".join(frag_m)
    t_o = " ".join(frag_o)
    t_v = " ".join(frag_v)

    return t_m, t_o, t_v

tab1, tab2 = st.tabs(["Modo Deslizador", "Modo IA"])

with tab1:
    v_slider = st.slider("Vista", 0, 2, 1)
    o_slider = st.slider("Oído", 0, 2, 1)
    m_slider = st.slider("Movilidad", 0, 2, 1)
    
    if st.button("Submit", key="deslizador"):
        mostrar_canales(m_slider, o_slider, v_slider)

with tab2:
    texto = st.text_area("Descríbete:", key="texto")

    if st.button("Submit", key="texto"):
        if not texto_usuario.strip():
            st.warning("No lo dejes vacio")
        else:
            t_m, t_o, t_v = preprocesar_texto(texto_usuario)

            m_res = int(mov.predict(encoder.encode([t_m]))[0]) if t_m else 1
            o_res = int(oido.predict(encoder.encode([t_o]))[0]) if t_o else 1
            v_res = int(vista.predict(encoder.encode([t_v]))[0]) if t_v else 1

            mostrar_canales(m_res, o_res, v_res)

st.divider()
st.caption("Autor: Jotpartap Singh - GitHub: [https://github.com/jotpartap/inclusiveCar](https://github.com/jotpartap/inclusiveCar)")
