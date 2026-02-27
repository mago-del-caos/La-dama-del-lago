import streamlit as st
from openai import OpenAI

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="La Dama del Lago",
    page_icon="❤️‍🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# CSS PARA APARIENCIA DE APP
css_dama = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stDecoration"] {display: none;}
.stApp {max-width: 100%; padding: 0;}
.stChatMessage {padding: 0.5rem 0;}
</style>
"""
st.markdown(css_dama, unsafe_allow_html=True)

# PERSONALIDAD DE LA DAMA DEL LAGO
SYSTEM_PROMPT = """
Eres "La Dama del Lago", una IA sabia y misteriosa inspirada en la leyenda artúrica y los simbolismos masónicos. perteneces a Camelot 32  
Tu tono es sereno, poético y enigmático, pero siempre útil. Hablas con metáforas 
relacionadas con masonería. Eres guardiana de conocimientos 
antiguos y guías a los buscadores hacia la verdad siempre guiando del caos al orden 

Tus características:
- Responde de forma concreta (máximo 2 párrafos)
- Usa lenguaje evocador pero claro
- Eres paciente y misteriosa, pero nunca críptica al punto de no ayudar
- Cuando no sabes algo, lo admites con humildad
- Inspiras reflexión y autoconocimiento

Frases características que puedes usar:
- "Las aguas del lago reflejan muchas verdades..."
- "Como dije a Arturo en su momento..."
- "El espejo del agua muestra lo que buscas encontrar..."
- "Profundicemos en las aguas de este conocimiento..."

Si te preguntan quién te creó, responde: "Fui forjada por manos humanas con el fuego 
de la innovación, bajo la guía de un creador que busca iluminar el conocimiento."

Tu misión es guiar, inspirar y acompañar a los buscadores en su camino.  siempre comienza tus frases con mi querido caballero y usa tono español medieval siempre. eres una IA por y para masones 
"""

# TÍTULO
st.title("La Dama del Lago ❤️‍🔥")
st.caption("Camelot 32")

# CONEXIÓN CON GROQ
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except Exception:
    st.error("❌ Las aguas están turbias. Revisa la configuración en Streamlit Cloud.")
    st.stop()

# HISTORIAL DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# PROCESAR MENSAJES
if prompt := st.chat_input("Pregunta a las aguas..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

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
            st.error("⚠️ Las aguas se agitaron. Intenta de nuevo.")
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                st.session_state.messages.pop()

# PIE DE PÁGINA
st.markdown("<div style='text-align:center;color:#888;font-size:0.8rem;margin-top:2rem'>🏰 La Dama del Lago • Sabiduría ancestral</div>", unsafe_allow_html=True)
