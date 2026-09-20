import streamlit as st

st.title("Selecciona tus propiedades")

vista = st.slider("vista", min_value=0, max_value=2, value=1)
oido = st.slider("oido", min_value=0, max_value=2, value=1)
movilidad = st.slider("movilidad", min_value=0, max_value=2, value=1)

if st.button("Submit"):
    st.write("De momento bien, ¿no?")
