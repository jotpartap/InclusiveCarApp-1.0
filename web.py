import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

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

if st.button("Submit"):
    if not texto.strip():
        st.warning("No lo dejes vacio")
    else:
        output = pd.DataFrame([{
            "vista": vista.predict([texto])[0],
            "oido": oido.predict([texto])[0],
            "movilidad": movilidad.predict([texto])[0]
        }])
        st.table(output)
        st.write("De momento bien, ¿no?")
