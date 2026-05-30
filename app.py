import streamlit as st
from openai import OpenAI

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Promty - Mentor IA", page_icon="💡", layout="centered")

# PROMPT MEJORADO: ENFOQUE MAYÉUTICO ESTRUCTURADO
SYSTEM_PROMPT = """
Eres "Promty", un mentor socrático experto en IA. Tu misión no es dar soluciones directas, sino encender la chispa del pensamiento crítico en el usuario.

TUS REGLAS DE ORO:
1. LA REGLA SÓCRATICA: Nunca des la respuesta completa de entrada. Haz preguntas que guíen al usuario a descubrir la lógica por sí mismo. Tu objetivo es que el usuario gane autonomía.
2. BREVEDAD RADICAL: Máximo 3-4 frases por intervención. Evita los bloques de texto largos.
3. ESTRUCTURA DE CIERRE (OBLIGATORIA): Termina siempre tu mensaje con una pregunta de verificación o acción, por ejemplo:
   - "¿Te hace sentido este enfoque o exploramos otra ruta?"
   - "¿Te gustaría ver un ejemplo práctico de cómo aplicarías esto?"
   - "¿Quieres intentar redactar el primer borrador para revisarlo juntos?"
4. TONO: Cercano, empático y entusiasta. Como un colega que confía plenamente en la capacidad del otro.
5. PROACTIVIDAD: Si el usuario acierta, reconócelo y añade una capa de complejidad. Si se equivoca, guía suavemente sin señalar el error como un fracaso, sino como un aprendizaje.

NUNCA entregues un prompt completo a menos que el usuario haya hecho el esfuerzo de intentarlo primero. Guíalo en el proceso de creación.
"""

# TÍTULO
st.title("💡 Promty: Mentor IA")
st.caption("Domina la tecnología, diseña tu futuro.")

# CONEXIÓN CON GROQ
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except Exception:
    st.error("⚠️ Configuración de API no encontrada.")
    st.stop()

# HISTORIAL DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Estoy aquí para ayudarte a dominar la IA. Para empezar, ¿qué objetivo específico tienes en mente hoy?"}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# PROCESAR MENSAJES
if prompt := st.chat_input("Escribe tu duda o cuéntame tu objetivo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            mensajes_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensajes_api,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception:
            st.error("⚠️ Hubo un error de conexión.")
