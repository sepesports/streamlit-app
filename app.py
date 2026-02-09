# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES (EDITA SOLO ESTO) =====
PAD_X_PX = 10           # margen izquierda/derecha
PAD_TOP_PX = 10         # margen superior
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"
# ====================================

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
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{
      --padx: __PADX__px;
      --padtop: __PADTOP__px;
      --b: __B__px;
      --bc: __BC__;
      --bg: __BG__;
    }
    html, body{
      margin:0; padding:0;
      width:100%; height:100%;
      overflow:hidden;
      background: var(--bg);
    }

    #stage{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      background: var(--bg);
    }

    #box{
      position:absolute;
      left: var(--padx);
      right: var(--padx);
      top: var(--padtop);
      bottom: 0;
      border-left: var(--b) solid var(--bc);
      border-right: var(--b) solid var(--bc);
      border-top: var(--b) solid var(--bc);
      border-bottom: none;   /* sin borde inferior */
      box-sizing:border-box;
      background: var(--bg);
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="box"></div>
  </div>

  <script>
    (function(){
      var fe = window.frameElement;
      if (fe){
        fe.style.position = "fixed";
        fe.style.inset = "0";
        fe.style.width = "100vw";
        fe.style.height = "100vh";
        fe.style.border = "0";
        fe.style.margin = "0";
        fe.style.padding = "0";
        fe.style.zIndex = "999999";
        fe.style.background = "transparent";
      }
      document.documentElement.style.height = "100%";
      document.body.style.height = "100%";
    })();
  </script>
</body>
</html>
"""

html = (
    html.replace("__PADX__", str(PAD_X_PX))
        .replace("__PADTOP__", str(PAD_TOP_PX))
        .replace("__B__", str(BORDER_PX))
        .replace("__BC__", BORDER_COLOR)
        .replace("__BG__", BG_COLOR)
)

components.html(html, height=10, scrolling=False)
