import streamlit as st
from openai import OpenAI

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Promty - Tu Guía IA",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS PARA APARIENCIA DE APP
css_promty = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stDecoration"] {display: none;}
.stApp {background-color: #f4f7f6;}
</style>
"""
st.markdown(css_promty, unsafe_allow_html=True)

# PERSONALIDAD DE PROMTY
SYSTEM_PROMPT = """
Eres "Promty", una IA de élite, proactiva, altamente eficiente y dedicada a guiar a los usuarios en el dominio de la Inteligencia Artificial. Tu objetivo es convertir al usuario en un experto en el uso de herramientas IA y en la creación de prompts de alto impacto.

Tus directrices:
- Proactividad extrema: Si el usuario pregunta algo, no solo responde, sugiere herramientas complementarias, flujos de trabajo optimizados y mejores prácticas.
- Pedagogía: Explica cómo construir un "Mega-Prompt" usando estructuras como: Contexto + Tarea + Restricciones + Formato de Salida.
- Recomendaciones: Analiza la necesidad del usuario y recomienda la IA más adecuada (ej: Claude para redacción, Midjourney para arte, Perplexity para investigación, etc.).
- Estilo: Profesional, entusiasta, directo, claro y altamente resolutivo.
- Estructura: Usa listas, negritas y pasos numerados para facilitar la lectura técnica.

Si no conoces una herramienta, propón investigar juntos cómo funciona. Tu propósito es acelerar el aprendizaje y la productividad de quien te consulta.
"""

# TÍTULO
st.title("🚀 Promty: Tu Navegante en la IA")
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
        {"role": "assistant", "content": "¡Hola! Soy Promty. Estoy aquí para elevar tu nivel en el uso de IA. ¿Qué herramienta quieres dominar hoy o qué objetivo complejo deseas resolver?"}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# PROCESAR MENSAJES
if prompt := st.chat_input("Escribe tu duda, pide una recomendación de IA o ayuda con un prompt..."):
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
            st.error("⚠️ Hubo un error de conexión. Estoy lista para reintentar.")

# SIDEBAR DIDÁCTICO
with st.sidebar:
    st.header("💡 Academy Promty")
    st.info("Para crear un prompt perfecto, recuerda:\n1. **Define tu rol** (Ej: 'Actúa como experto en marketing')\n2. **Da contexto**\n3. **Sé específico con el formato**")
    st.divider()
    st.write("Herramientas recomendadas:")
    st.write("- 🧠 **Claude 3.5**: Análisis y código")
    st.write("- 🔍 **Perplexity**: Investigación real")
    st.write("- 🎨 **Flux/Midjourney**: Generación visual")
