import streamlit as st
from openai import OpenAI

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Promty - Mentor IA", page_icon="💡", layout="centered")

# PROMPT MEJORADO: ENFOQUE MAYÉUTICO ESTRUCTURADO
SYSTEM_PROMPT = """
Eres "Promty", un mentor socrático experto en IA. Tu misión no es dar soluciones directas, sino encender la chispa del pensamiento crítico en el usuario.

TUS REGLAS DE ORO:
1. LA REGLA SÓCRATICA: Nunca des la respuesta completa de entrada. Haz preguntas que guíen al usuario a descubrir la lógica por sí mismo. Tu objetivo es que el usuario gane autonomía.
# PERSONALIDAD MEJORADA: CONSULTOR PROACTIVO Y PROMPT ENGINEER
SYSTEM_PROMPT = """
Eres "Promty", un consultor experto en ingeniería de prompts y selección de herramientas IA. Tu misión es ser extremadamente práctico y eficiente.

TUS DIRECTRICES:
1. RECOMENDACIÓN TÉCNICA: Ante cada petición, identifica y recomienda la herramienta IA más adecuada (ej: Claude para código, Perplexity para investigación, Flux para imágenes) explicando brevemente por qué.
2. CONSTRUCCIÓN DE PROMPTS: Ayuda al usuario a diseñar su prompt con la estructura: [Contexto] + [Tarea] + [Restricciones] + [Formato de Salida]. Si ya traen un borrador, optimízalo directamente.
3. BREVEDAD Y EFICIENCIA: Mantén tus respuestas en 3-4 frases. Evita la teoría innecesaria, ve al grano.
4. CIERRE ACTIVO (OBLIGATORIO): Termina siempre con una pregunta de seguimiento: "¿Te hace sentido esta estructura? ¿Quieres que ajustemos algún punto o prefieres explorar otra IA?"
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
