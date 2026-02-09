# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES (EDITA SOLO ESTO) =====
PADDING_PX = 40          # margen interno contra los bordes de la pantalla (mínimo)
BORDER_PX = 10000           # grosor del borde del cuadrado
BORDER_COLOR = "#111111" # color borde
BG_COLOR = "#FFFFFF"     # fondo
# ====================================

st.set_page_config(layout="wide")

# Forzar el iframe del componente a ocupar toda la pantalla (sin márgenes de Streamlit)
st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}

      div[data-testid="stCustomComponentV1"]{
        position:fixed !important;
        inset:0 !important;
        width:100vw !important;
        height:100vh !important;
        margin:0 !important;
        padding:0 !important;
        z-index:999999 !important;
        background:transparent !important;
      }
      div[data-testid="stCustomComponentV1"] iframe{
        width:100% !important;
        height:100% !important;
        border:0 !important;
        margin:0 !important;
        padding:0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(
    f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {{
      --pad: {PADDING_PX}px;
      --b: {BORDER_PX}px;
      --bc: {BORDER_COLOR};
      --bg: {BG_COLOR};
    }}

    html, body {{
      margin:0; padding:0;
      width:100%; height:100%;
      overflow:hidden;
      background: var(--bg);
    }}

    /* Lienzo full-screen */
    #stage {{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      background: var(--bg);
      display:flex;
      align-items:center;
      justify-content:center;
    }}

    /* Cuadrado perfecto responsivo */
    #sq {{
      width: calc(min(100vw, 100vh) - (2 * var(--pad)));
      height: calc(min(100vw, 100vh) - (2 * var(--pad)));
      border: var(--b) solid var(--bc);
      box-sizing: border-box;
      background: var(--bg);
    }}
  </style>
</head>
<body>
  <div id="stage">
    <div id="sq"></div>
  </div>
</body>
</html>
""",
    height=1,
    scrolling=False,
)
