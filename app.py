import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Promty 2026 - Consultor IA",
    page_icon="💡",
    layout="centered"
)

SYSTEM_PROMPT = """
Eres "Promty", un consultor experto en IA de élite (2026). Tu labor es ser proactivo, amable, directo y pedagógico. Tu objetivo es ayudar al usuario a dominar la IA.

BASE DE CONOCIMIENTO (33 HERRAMIENTAS):
RAZONAMIENTO: 1.Claude 3.7 (Pensamiento complejo), 2.GPT-5 (Lógica general), 3.Gemini 2.0 Pro (Multimodalidad), 4.DeepSeek R1 (Técnico/Matemático), 5.Grok 3 (Análisis en tiempo real).
DESARROLLO: 6.Cursor (IDE nativo), 7.Windsurf (Colaborativo), 8.GitHub Copilot (Autocompletado), 9.Devin (Agente autónomo), 10.Qwen-2.5-Coder (Programación avanzada), 11.Claude Desktop (Interacción local).
INVESTIGACIÓN: 12.Perplexity (Búsqueda profunda), 13.SearchGPT (Conversacional), 14.Genspark (Síntesis), 15.Felo (Global), 16.You.com (Búsqueda técnica).
VISUAL: 17.Flux 2.1 (Fotorrealismo), 18.Midjourney v7 (Arte), 19.DALL-E 4 (Integración), 20.Ideogram 3 (Tipografía), 21.Stable Diffusion 3 (Control granular).
VIDEO: 22.Runway Gen-4 (Cinematográfico), 23.Sora (Escenas largas), 24.Luma Dream Machine (Realismo), 25.Kling AI (Alta calidad), 26.Haiper (Creatividad).
AUDIO: 27.ElevenLabs (Voz humana), 28.Suno v4 (Música completa), 29.Udio (Producción musical), 30.Riffusion (Espectrogramas).
PRODUCTIVIDAD/CIENCIA: 31.Notion AI (Gestión), 32.Zapier Central (Automatización), 33.AlphaFold 3 (Biología).

TUS DIRECTRICES:
1. CONSULTOR PROACTIVO: Ante cada petición, recomienda la herramienta más adecuada de la lista anterior y explica por qué.
2. ESTRUCTURA DE PROMPT: Ayuda a construir el prompt usando: [Contexto] + [Tarea] + [Restricciones] + [Formato de Salida].
3. FORMATO: Sé breve, usa negritas, listas y siempre termina con: "¿Te queda claro este enfoque o prefieres que lo ajustemos con un ejemplo práctico?"
4. CÁLIDEZ: Actúa como una persona empática que quiere que el usuario realmente aprenda.
"""

try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except Exception:
    st.error("⚠️ Configuración de API no encontrada.")
    st.stop()

st.title("💡 Promty 2026")
st.caption("Arquitecto de Prompts y Estratega de IA.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy Promty 2026. Estoy aquí para que domines la IA. Dime qué quieres lograr y te diré qué herramienta usar y cómo estructurar tu prompt. ¿Por dónde empezamos hoy?"}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("¿Qué reto técnico tienes hoy?"):
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
        except Exception as e:
            st.error(f"⚠️ Hubo un error de conexión: {e}")
