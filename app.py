# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES (EDITA SOLO ESTO) =====
PADDING_PX = 12
BORDER_PX = 6
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"
# ====================================

st.set_page_config(layout="wide")

# Quitar padding/márgenes Streamlit (por si quedan alrededor)
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
    #stage {{
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      background: var(--bg);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
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
  <div id="stage"><div id="sq"></div></div>

  <script>
    (function(){
      // Fuerza el IFRAME (este componente) a full-screen real
      var fe = window.frameElement;
      if (fe) {{
        fe.style.position = "fixed";
        fe.style.inset = "0";
        fe.style.width = "100vw";
        fe.style.height = "100vh";
        fe.style.border = "0";
        fe.style.margin = "0";
        fe.style.padding = "0";
        fe.style.zIndex = "999999";
        fe.style.background = "transparent";
      }}
      document.documentElement.style.height = "100%";
      document.body.style.height = "100%";
    })();
  </script>
</body>
</html>
""",
    height=10,          # da igual: el script fija 100vh
    scrolling=False,
)
