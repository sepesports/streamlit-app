import streamlit as st
import requests

r = requests.post(
    "https://camilo27.pythonanywhere.com/api/auth",
    data={"correo": "warja@gmail.com", "dni": "Y044"},
    timeout=10
)

st.write(r.status_code, r.text)
st.stop()


# app.py
import streamlit as st
import streamlit.components.v1 as components
import requests

# ================= LOGIN / SESIÓN =================
API_URL = "https://camilo27.pythonanywhere.com/api/auth"

if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = ""

@st.dialog("Login")
def login_dialog():
    correo = st.text_input("Correo")
    dni = st.text_input("DNI", type="password")

    if st.button("Entrar"):
        try:
            r = requests.post(API_URL, data={"correo": correo, "dni": dni}, timeout=10)
            data = r.json()
            if data.get("ok"):
                st.session_state.auth = True
                st.session_state.user = correo
                st.success("Acceso concedido")
                st.switch_page("pages/admin.py")
            else:
                st.error("Credenciales inválidas")
        except Exception:
            st.error("Error conectando con el servidor")

# ======================================================================
# DESDE AQUÍ TU CÓDIGO ORIGINAL — SOLO SE AGREGA EL CLICK EN “Login”
# ======================================================================

# (todo tu bloque de constantes se mantiene igual)
PAD_X_PX = 8
PAD_TOP_PX = 8
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"
HEADER_BG = "#FFFFFF"
IMG_BG = "#FFFFFF"
BTN_BG = "#FFFFFF"
FOOTER_BG = "#FFFFFF"
IMG_LEFT = 0
IMG_RIGHT = 0
IMG_TOP = 10
IMG_HEIGHT = 44
HEADER_TOP = 0
HEADER_HEIGHT = 12
BTN_AREA_TOP = 55
BTN_H = 23
BTN_GAP_X = 2
BTN_GAP_Y = 2
BTN_LEFT = 5
BTN_RIGHT = 5
BTN_TEXTS = [
    "Horarios",
    "Control de\nAsistencia",
    "Nomina y\nPagos",
    "Incidencias",
    "Formación",
    "Comunicados",
]
FOOTER_H = 18
FOOTER_BOTTOM = 5
FOOTER_LEFT = 6
FOOTER_RIGHT = 6
MIN_BTN_W_PX = 130
MOBILE_MAX_W_PX = 500

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = """<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#fff;}
#stage{position:fixed;inset:0}
#login-btn{
position:absolute;
right:3%;
top:2%;
padding:8px 16px;
font-weight:bold;
cursor:pointer;
z-index:9999;
}
</style>
</head>
<body>
<div id="stage">
<button id="login-btn">Login</button>
<script>
document.getElementById("login-btn").onclick = function(){
    window.parent.postMessage({type:"login"}, "*");
};
</script>
</div>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)

# Escucha el evento del botón Login

if st.button("🔐 Abrir Login"):
    login_dialog()
