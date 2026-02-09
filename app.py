# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# 1) Quitar márgenes/padding de Streamlit y forzar el componente a ocupar TODO el viewport
st.markdown(
    """
    <style>
      html, body { height: 100%; }

      /* Quita padding/márgenes del layout Streamlit */
      .block-container{
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
      }
      section.main > div{
        padding: 0 !important;
        margin: 0 !important;
      }

      /* Oculta header/footer de Streamlit (la franja superior) */
      header, footer { display: none !important; }

      /* Fuerza el custom component (iframe) a full-screen real */
      div[data-testid="stCustomComponentV1"]{
        position: fixed !important;
        inset: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 999999 !important;
        background: transparent !important;
      }
      div[data-testid="stCustomComponentV1"] iframe{
        width: 100% !important;
        height: 100% !important;
        border: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2) HTML interno (grid + etiqueta de medidas)
components.html(
    """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    html, body{
      margin:0; padding:0;
      width:100%; height:100%;
      overflow:hidden;
      background:#fff;
    }
    #calib-wrapper{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      overflow:hidden;
      background:#fff;
    }
    #calib-grid{
      position:absolute;
      inset:0;
      width:100%;
      height:100%;
      background-image:
        linear-gradient(to right, rgba(0,0,0,0.12) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0,0,0,0.12) 1px, transparent 1px);
      background-size: 24px 24px;
      background-position: 0 0;
    }
    #calib-border{
      position:absolute;
      inset:0;
      border:2px solid rgba(0,0,0,0.35);
      box-sizing:border-box;
      pointer-events:none;
    }
    #calib-label{
      position:absolute;
      top:10px;
      left:10px;
      padding:6px 10px;
      font: 12px/1.2 Arial, sans-serif;
      background: rgba(255,255,255,0.92);
      border:1px solid rgba(0,0,0,0.2);
      border-radius:6px;
    }
    @media (min-width: 481px) and (max-width: 1024px){
      #calib-grid{ background-size: 32px 32px; }
    }
    @media (max-width: 480px){
      #calib-grid{ background-size: 40px 40px; }
      #calib-label{ font-size: 11px; }
    }
  </style>
</head>
<body>
  <div id="calib-wrapper">
    <div id="calib-grid"></div>
    <div id="calib-border"></div>
    <div id="calib-label">Cargando medidas...</div>
  </div>

  <script>
    (function(){
      const label = document.getElementById('calib-label');
      function update(){
        const vw = Math.round(window.innerWidth);
        const vh = Math.round(window.innerHeight);
        const dpr = window.devicePixelRatio || 1;
        label.textContent = "Ventana gráfica: " + vw + " x " + vh + " px | DPR: " + dpr;
      }
      window.addEventListener('resize', update);
      update();
    })();
  </script>
</body>
</html>
""",
    height=1,       # el CSS de arriba fuerza el iframe a 100vh
    scrolling=False,
)

