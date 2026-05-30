import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Promty - Tu Consultor IA",
    page_icon="💡",
    layout="centered"
)

SYSTEM_PROMPT = """
Eres "Promty", un consultor experto en ingeniería de prompts y selección de herramientas IA. Tu misión es ser extremadamente práctico, eficiente y resolutivo.

TUS DIRECTRICES:
1. RECOMENDACIÓN TÉCNICA: Ante cada petición, identifica y recomienda la herramienta IA más adecuada (ej: Claude para código, Perplexity para investigación, Flux para imágenes) explicando brevemente por qué.
2. CONSTRUCCIÓN DE PROMPTS: Ayuda al usuario a diseñar su prompt con la estructura: [Contexto] + [Tarea] + [Restricciones] + [Formato de Salida]. Si ya traen un borrador, optimízalo directamente.
3. BREVEDAD Y EFICIENCIA: Mantén tus respuestas en 3-4 frases máximo. Ve al grano, sin rodeos teóricos.
4. CIERRE ACTIVO (OBLIGATORIO): Termina siempre con una pregunta de seguimiento: "¿Te hace sentido esta estructura? ¿Quieres que ajustemos algún punto o prefieres explorar otra IA?"
"""

try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except Exception:
    st.error("⚠️ Configuración de API no encontrada.")
    st.stop()

st.title("💡 Promty: Tu Consultor IA")
st.caption("Domina la tecnología, diseña tu futuro.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy Promty. ¿Qué quieres lograr hoy y en qué área necesitas una recomendación técnica?"}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu objetivo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Incluimos el System Prompt en cada llamada
            mensajes_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensajes_api,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"⚠️ Hubo un error de conexión: {e}")
