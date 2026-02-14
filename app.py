# app.py
import streamlit as st
import streamlit.components.v1 as components

# 🔒 GATE: solo entra con ?auth=ok
if st.query_params.get("auth") != "ok":
    st.markdown(
        """
        <script>
          window.location.href="/admin";
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ===================== BASE (NO CAMBIAR ESTRUCTURA) =====================

PAD_X_PX = 8
PAD_TOP_PX = 8

BORDER_PX = 1
BORDER_COLOR = "rgba(255,255,255,.12)"

BG_COLOR = "#020a1a"
HEADER_BG = "transparent"
IMG_BG = "transparent"
BTN_BG = "transparent"
FOOTER_BG = "transparent"

IMG_LEFT = 0
IMG_RIGHT = 0
IMG_TOP = 10
IMG_HEIGHT = 44

HEADER_TOP = 0
HEADER_HEIGHT = 10

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

# ===================== CONTENIDO =====================

LOGO_URL = "https://files.catbox.moe/056m6v.jpg"
FOOTER_TEXT = "2026 Socorrista ProVersión 1.0. Todos los derechos reservados"

HERO_BG_IMAGE_URL = "https://files.catbox.moe/16109j.jpeg"
HERO_BG_IMAGE_FIT = "cover"
HERO_BG_IMAGE_POS = "center"

USER_NAME = st.query_params.get("usuario") or st.query_params.get("user") or "Login"

HERO_FONT_SIZE_DESKTOP_PX = 44
HERO_FONT_SIZE_MOBILE_PX = 13

HEADER_FONT_SIZE_DESKTOP_PX = 40
HEADER_FONT_SIZE_MOBILE_PX = 23

BTN_FONT_SIZE_DESKTOP_PX = 17
BTN_FONT_SIZE_MOBILE_PX = 17

FOOTER_FONT_SIZE_DESKTOP_PX = 13
FOOTER_FONT_SIZE_MOBILE_PX = 13

BTN_FONT_OVERRIDES_DESKTOP_PX = {}
BTN_FONT_OVERRIDES_MOBILE_PX = {}

LOGO_PADDING_PX_DESKTOP = 0
LOGO_PADDING_PX_MOBILE = 0
LOGO_BORDER_RADIUS_PX = 0
LOGO_OBJECT_FIT = "cover"
LOGO_BORDER = "0px solid rgba(255,255,255,.0)"

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

html = """ """ + open("/mnt/data/app.py.txt").read().split('html = """',1)[1]
