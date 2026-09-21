import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from streamlit_mic_recorder import speech_to_text

CANALES = {
    (0, 0, 0): {"auditivo": "OFF (Ahorro)", "visual": "OFF (Ahorro)", "haptico": "MÁXIMO: Vibraciones codificadas, Braille al alcance de la silla.", "gestual": "Rampa ON. Reconocimiento de pequeños gestos manuales."},
    (0, 0, 1): {"auditivo": "OFF (Ahorro)", "visual": "MÁXIMO: Lengua de signos, pictogramas grandes.", "haptico": "ALTO: Vibración para dirigir la mirada a la pantalla.", "gestual": "Rampa ON. Lee gestos de cabeza y manos."},
    (0, 0, 2): {"auditivo": "OFF (Ahorro)", "visual": "OSCURO: Pictogramas muy claros sobre fondo negro mate.", "haptico": "ALTO: Suple la visión atenuada y la sordera.", "gestual": "Rampa ON. Reconocimiento de gestos."},
    (0, 1, 0): {"auditivo": "OFF (Ahorro)", "visual": "MÁXIMO: Asistente de voz descriptivo total.", "haptico": "ALTO: Vibración de confirmación de acciones.", "gestual": "Rampa ON. Micrófonos a la altura de la silla."},
    (0, 1, 1): {"auditivo": "NORMAL", "visual": "NORMAL: Pantallas bajas (al alcance de la silla).", "haptico": "NORMAL: Alertas de emergencia.", "gestual": "Rampa ON. Botones al alcance o gestos manuales."},
    (0, 1, 2): {"auditivo": "NORMAL", "visual": "OSCURO: Pantallas atenuadas a la altura de la silla.", "haptico": "NORMAL: Asistente de voz cobra relevancia.", "gestual": "Rampa ON."},
    (0, 2, 0): {"auditivo": "OFF (Ahorro)", "visual": "SUAVE: Voz susurrada + cancelación de ruido.", "haptico": "ALTO: Pasa a ser el canal principal.", "gestual": "Rampa ON."},
    (0, 2, 1): {"auditivo": "NORMAL", "visual": "SUAVE: Cancelación activa de ruido ambiental.", "haptico": "NORMAL: Pantallas adaptadas en altura.", "gestual": "Rampa ON."},
    (0, 2, 2): {"auditivo": "NORMAL", "visual": "SUAVE: Cancelación activa de ruido.", "haptico": "OSCURO: Ambiente de baja carga cognitiva.", "gestual": "Rampa ON. Conducción ultrasuave automática."},

    (1, 0, 0): {"auditivo": "OFF (Ahorro)", "visual": "OFF (Ahorro)", "haptico": "MÁXIMO: Guía táctil integral por todo el habitáculo.", "gestual": "Estándar."},
    (1, 0, 1): {"auditivo": "OFF (Ahorro)", "visual": "MÁXIMO: Lengua de signos y alertas luminosas.", "haptico": "ALTO: Vibración de llamada de atención.", "gestual": "Estándar."},
    (1, 0, 2): {"auditivo": "OFF (Ahorro)", "visual": "OSCURO: Pictogramas claros de alto contraste.", "haptico": "ALTO", "gestual": "Estándar."},
    (1, 1, 0): {"auditivo": "OFF (Ahorro)", "visual": "MÁXIMO: Asistente de voz descriptivo.", "haptico": "ALTO: Pulsera/asiento vibra al llegar.", "gestual": "Estándar."},
    (1, 1, 1): {"auditivo": "NORMAL", "visual": "NORMAL", "haptico": "NORMAL", "gestual": "Estándar."},
    (1, 1, 2): {"auditivo": "NORMAL", "visual": "OSCURO: Cristales opacos por defecto.", "haptico": "NORMAL", "gestual": "Estándar."},
    (1, 2, 0): {"auditivo": "OFF (Ahorro)", "visual": "SUAVE: Voz susurrada + cancelación de ruido.", "haptico": "ALTO: Pasa a ser el canal principal.", "gestual": "Estándar."},
    (1, 2, 1): {"auditivo": "NORMAL", "visual": "SUAVE: Cancelación de ruido.", "haptico": "NORMAL", "gestual": "Estándar."},
    (1, 2, 2): {"auditivo": "OSCURO", "visual": "OFF", "haptico": "SUAVE: Cancelación de ruido.", "gestual": "Estándar."},

    (2, 0, 0): {"auditivo": "OFF (Ahorro)", "visual": "OFF (Ahorro)", "haptico": "MODERADO: Vibraciones suaves para no sobreestimular.", "gestual": "Espacio amplio, cinturones adaptativos."},
    (2, 0, 1): {"auditivo": "OFF (Ahorro)", "visual": "MINIMIZADO", "haptico": "MODERADO: Pictogramas grandes sin destellos estridentes.", "gestual": "Espacio libre para moverse con seguridad."},
    (2, 0, 2): {"auditivo": "OFF (Ahorro)", "visual": "MINIMIZADO", "haptico": "OSCURO EXTREMO: Iluminación prácticamente nula.", "gestual": "Espacio adaptativo."},
    (2, 1, 0): {"auditivo": "OFF (Ahorro)", "visual": "MODERADO: Voz calmada y clara.", "haptico": "MINIMIZADO: Solo alertas críticas.", "gestual": "Espacio libre, bloqueo seguro de puertas."},
    (2, 1, 1): {"auditivo": "NORMAL", "visual": "MINIMIZADO", "haptico": "NORMAL: Juegos/distracciones en pantalla para relajar.", "gestual": "Máxima libertad de movimiento segura."},
    (2, 1, 2): {"auditivo": "NORMAL", "visual": "OSCURO", "haptico": "OFF", "gestual": "Espacio amplio."},
    (2, 2, 0): {"auditivo": "OFF (Ahorro)", "visual": "MUY SUAVE: Solo alertas vitales.", "haptico": "MINIMIZADO: Evitar sobrecarga sensorial.", "gestual": "Espacio libre, máximo aislamiento exterior."},
    (2, 2, 1): {"auditivo": "OFF / SUAVE: Aislamiento total del ruido exterior (TEA).", "visual": "RELAX: Colores pastel, rutas suaves.", "haptico": "OFF: Cero vibraciones innecesarias.", "gestual": "Ambiente zen, sin bloqueos físicos restrictivos."},
    (2, 2, 2): {"auditivo": "AISLAMIENTO: Silencio absoluto (ANC al máximo).", "visual": "OSCURO TOTAL: Cápsula de aislamiento visual.", "haptico": "OFF: Cero estímulos.", "gestual": "Máximo confort, cinturón envolvente relajante."}
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
    
    v = int(vista.predict(emb)[0])
    o = int(oido.predict(emb)[0])
    m = int(mov.predict(emb)[0])
    
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


st.title("InclusiveCarApp")

tab1, tab2, tab3 = st.tabs(["Modo Deslizador", "Modo IA", "Modo Voz"])

with tab1:
    v_slider = st.slider("Vista", 0, 2, 1)
    o_slider = st.slider("Oído", 0, 2, 1)
    m_slider = st.slider("Movilidad", 0, 2, 1)
    
    if st.button("Submit", key="btn_slider"):
        mostrar_canales(m_slider, o_slider, v_slider)

with tab2:
    texto = st.text_area("Descríbete:")
    
    if st.button("Submit", key="btn_texto"):
        if not texto.strip():
            st.warning("No lo dejes vació.")
        else:
            m_res, o_res, v_res = predecir_texto(texto_input)
            mostrar_canales(m_res, o_res, v_res)

with tab3:
    st.subheader("Habla para describirte")
    
    texto_transcrito = speech_to_text(
        language='es',
        start_prompt='Grabar audio',
        stop_prompt='Detener y procesar',
        just_once=True,
        use_container_width=True,
        key='STT_REC'
    )
    
    if texto_transcrito:
        m_res, o_res, v_res = predecir_texto(texto_transcrito)
        mostrar_canales(m_res, o_res, v_res)
