# app.py
import streamlit as st
import streamlit.components.v1 as components

# 🔒 CONTROL DE ACCESO (NO TOCAR)
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

# ======================================================================
# TU APP ORIGINAL (PEGADA COMPLETA)
# ======================================================================

# app.py
import streamlit as st
import streamlit.components.v1 as components

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

html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
</head>
<body style="margin:0;background:white;">
<script>
document.body.innerHTML = "<h2 style='font-family:Arial;text-align:center;margin-top:40vh'>App cargada</h2>";
</script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
