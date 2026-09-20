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
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ]).fit(X, data["vista"])

    oido = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ]).fit(X, data["oido"])

    movilidad = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ]).fit(X, data["movilidad"])

    return vista, oido, movilidad

vista, oido, movilidad = modelo()

st.title("Selecciona tus propiedades")

texto = st.text_area("Describete:")

VISTA = [
    "ciego", "ceguera", "veo", "vista", "ojo", "ojos", "gafas", "lentes", 
    "lentillas", "mirar", "agudeza", "borroso", "luz", "luces", "sombras", "baston"
]

OIDO = [
    "sordo", "sordera", "oigo", "oido", "oidos", "escucho", "escuchar", 
    "audicion", "audifono", "audifonos", "susurro", "susurros", "hipoacusia", "fino", "ruido", "ruidos"
]

MOVILIDAD = [
    "silla", "ruedas", "caminar", "andar", "mover", "moverme", "movilidad", 
    "paralitico", "paraplejico", "agil", "atleta", "muletas", "piernas", "pie", 
    "correr", "lento", "despacio", "tortuga", "postrado", "paso", "pasos"
]

def predecir(pipeline, texto_usuario, palabras_clave):
    txt = texto_usuario.lower()
    
    if not any(palabra in txt for palabra in palabras_clave):
        return 1
    
    return pipeline.predict([texto_usuario])[0]

if st.button("Submit"):
    if not texto.strip():
        st.warning("No lo dejes vacio")
    else:
        v_res = predecir(vista, texto, PALABRAS_VISTA)
        o_res = predecir(oido, texto, PALABRAS_OIDO)
        m_res = predecir(movilidad, texto, PALABRAS_MOVILIDAD)

        output = pd.DataFrame([{
            "vista": v_res,
            "oido": o_res,
            "movilidad": m_res
        }])
        
        st.table(output)
        st.write("De momento bien, ¿no?")
