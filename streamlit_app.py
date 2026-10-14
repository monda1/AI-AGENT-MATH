import streamlit as st

st.title("Mi App Simple")

nombre = st.text_input("Escribe tu nombre:")

if st.button("Saludar"):
    if nombre:
        st.success(f"¡Hola, {nombre}!")
    else:
        st.warning("Por favor, escribe un nombre.")