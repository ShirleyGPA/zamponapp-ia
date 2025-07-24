import streamlit as st
import librosa
import numpy as np
import soundfile as sf
import io

st.set_page_config(page_title="ZampoñAPP", layout="centered")
st.title("?? ZampoñAPP: Retroalimentación musical automática")
st.markdown("Sube tu grabación de zampoña para recibir retroalimentación inmediata.")

# Cargar el audio modelo
modelo_audio, modelo_sr = librosa.load("modelo.wav", sr=None)
modelo_mfcc = librosa.feature.mfcc(y=modelo_audio, sr=modelo_sr, n_mfcc=13)
modelo_promedio = np.mean(modelo_mfcc, axis=1)

# Subir audio del estudiante
archivo = st.file_uploader("?? Sube tu audio en formato .wav", type=["wav"])
if archivo is not None:
    y, sr = sf.read(io.BytesIO(archivo.read()))
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    promedio = np.mean(mfcc, axis=1)

    distancia = np.linalg.norm(promedio - modelo_promedio)

    st.audio(archivo, format="audio/wav")

    if distancia < 50:
        st.success("?? ¡Muy bien! Tu ejecución está muy cercana al modelo.")
    elif distancia < 100:
        st.warning("?? Aceptable. Puedes mejorar ritmo o afinación.")
    else:
        st.error("? Requiere mejora. Practica un poco más con ayuda del docente.")
