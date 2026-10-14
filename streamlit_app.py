import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

# -------- Configuración de página --------
st.set_page_config(page_title="App con Pizarra", layout="wide")
st.title("🎨 Mi App con Pizarra")

# -------- Inicializar clave única del canvas --------
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0

# -------- Sección: Saludo --------
nombre = st.text_input("Escribe tu nombre:")
if st.button("Saludar"):
    if nombre:
        st.success(f"¡Hola, {nombre}!")
    else:
        st.warning("Por favor, escribe un nombre.")

st.divider()

# -------- Sección: Pizarra --------
st.subheader("Pizarra interactiva")

col1, col2 = st.columns([1, 3])

with col1:
    stroke_width = st.slider("Grosor del trazo", 1, 25, 3)
    stroke_color = st.color_picker("Color del trazo", "#000000")
    bg_color = st.color_picker("Color de fondo", "#FFFFFF")
    drawing_mode = st.selectbox(
        "Modo de dibujo",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )
    realtime_update = st.checkbox("Actualización en tiempo real", True)

    # Botón para limpiar la pizarra: cambia la key para forzar un canvas nuevo
    if st.button("🧹 Limpiar pizarra"):
        st.session_state.canvas_key += 1
        st.rerun()

with col2:
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=700,
        drawing_mode=drawing_mode,
        key=f"canvas_{st.session_state.canvas_key}",   # 👈 key dinámica
        update_streamlit=realtime_update,
        return_image_data=True,
    )

# -------- Guardar / Descargar imagen --------
if canvas_result.image_data is not None:
    img_array = canvas_result.image_data.astype("uint8")
    img = Image.fromarray(img_array, "RGBA")

    buf = io.BytesIO()
    img.save(buf, format="PNG")

    st.download_button(
        "⬇️ Descargar dibujo (PNG)",
        data=buf.getvalue(),
        file_name="pizarra.png",
        mime="image/png",
    )
    st.image(img, caption="Vista previa", use_column_width=True)
