import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from streamlit_mic_recorder import speech_to_text

@st.cache_resource
def cargar_modelos():
    encoder = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')
    
    data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine='python')
    data.columns = data.columns.str.strip()
    
    X_embeddings = encoder.encode(data["texto"].tolist(), show_progress_bar=False)
    
    clf_vista = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    clf_vista.fit(X_embeddings, data["vista"])
    
    clf_oido = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    clf_oido.fit(X_embeddings, data["oido"])
    
    clf_mov = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    clf_mov.fit(X_embeddings, data["movilidad"])
    
    return encoder, clf_vista, clf_oido, clf_mov

encoder, clf_vista, clf_oido, clf_mov = cargar_modelos()

def predecir_texto(texto):
    if not texto.strip():
        return 1, 1, 1
    
    emb = encoder.encode([texto])
    
    v = clf_vista.predict(emb)[0]
    o = clf_oido.predict(emb)[0]
    m = clf_mov.predict(emb)[0]
    
    return v, o, m

st.title("Selecciona tus propiedades")

tab1, tab2, tab3 = st.tabs(["Modo Deslizador", "Modo Texto", "Modo Voz"])

with tab1:
    v_slider = st.slider("Vista", 0, 2, 1)
    o_slider = st.slider("Oído", 0, 2, 1)
    m_slider = st.slider("Movilidad", 0, 2, 1)
    
    if st.button("Submit", key="btn_slider"):
        out = pd.DataFrame([{"vista": v_slider, "oido": o_slider, "movilidad": m_slider}])
        st.table(out)

with tab2:
    texto_input = st.text_area("Descríbete:")
    
    if st.button("Submit", key="btn_texto"):
        if not texto_input.strip():
            st.warning("Escribe algo antes de enviar.")
        else:
            v_res, o_res, m_res = predecir_texto(texto_input)
            out = pd.DataFrame([{"vista": v_res, "oido": o_res, "movilidad": m_res}])
            st.table(out)

with tab3:
    from streamlit_mic_recorder import speech_to_text

with tab3:
    st.subheader("Habla para describir tu situación")
    
    texto_transcrito = speech_to_text(language='es', use_container_width=True, key='STT')
    
    if texto_transcrito:
        v_res, o_res, m_res = predecir_texto(texto_transcrito)
        st.table(pd.DataFrame([{"vista": v_res, "oido": o_res, "movilidad": m_res}]))
