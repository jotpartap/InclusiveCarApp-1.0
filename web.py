import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

@st.cache_resource
def modelo():
    data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine='python')
    data.columns = data.columns.str.strip()
    
    X = data["texto"]
    
    vista = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
    ]).fit(X, data["vista"])

    oido = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
    ]).fit(X, data["oido"])

    movilidad = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
    ]).fit(X, data["movilidad"])

    return vista, oido, movilidad

vista, oido, movilidad = modelo()

st.title("Selecciona tus propiedades")

tab1, tab2 = st.tabs(["Modo Deslizador", "Modo Text"])

with tab1:
    st.subheader("Ajusta tus valores manualmente")
    
    v = st.slider("Vista", min_value=0, max_value=2, value=1)
    o = st.slider("Oído", min_value=0, max_value=2, value=1)
    m = st.slider("Movilidad", min_value=0, max_value=2, value=1)
    
    if st.button("Submit ", key="btn_slider"):
        output_slider = pd.DataFrame([{
            "vista": v,
            "oido": o,
            "movilidad": m
        }])
        st.table(output_slider)
        st.write("De momento bien, ¿no?")

with tab2:
    st.subheader("Describe tu situación")
    
    texto = st.text_area("Descríbete:")

    VISTA = [
        "ciego", "ceguera", "veo", "vista", "ojo", "ojos", "gafas", "lentes", 
        "lentillas", "mirar", "agudeza", "borroso", "luz", "luces", "sombras", "baston",
        "fotofobia", "deslumbra", "brillos", "hipersensibilidad", "dolor", "duelen", "molestan",
        "izquierdo", "derecho", "perdido", "perdi", "tuerto", "ocular", "inflamados"
    ]

    OIDO = [
        "sordo", "sordera", "oigo", "oido", "oidos", "escucho", "escuchar", 
        "audicion", "audifono", "audifonos", "susurro", "susurros", "hipoacusia", "ruido", "ruidos",
        "hiperacusia", "sensible", "molestan", "hipersensibilidad", "tapon", "sordomudo"
    ]

    MOVILIDAD = [
        "silla", "ruedas", "caminar", "andar", "mover", "moverme", "movilidad", 
        "paralitico", "paraplejico", "agil", "muletas", "piernas", "pie", "pies",
        "correr", "lento", "despacio", "tortuga", "postrado", "paso", "pasos",
        "hiperactividad", "hiperactivo", "inquietud", "quieto", "tics", "cojo", "inmovilizado"
    ]

    def predecir(pipeline, texto_usuario, palabras_clave):
        txt = texto_usuario.lower()
        if not any(palabra in txt for palabra in palabras_clave):
            return 1
        return pipeline.predict([texto_usuario])[0]

    if st.button("Submit", key="btn_texto"):
        if not texto.strip():
            st.warning("No lo dejes vacio")
        else:
            v_res = predecir(vista, texto, VISTA)
            o_res = predecir(oido, texto, OIDO)
            m_res = predecir(movilidad, texto, MOVILIDAD)

            output_texto = pd.DataFrame([{
                "vista": v_res,
                "oido": o_res,
                "movilidad": m_res
            }])
            
            st.table(output_texto)
            st.write("De momento bien, ¿no?")
