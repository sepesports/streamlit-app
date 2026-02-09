# app.py
import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      /* Quita padding de Streamlit para que el contenedor ocupe TODA la pantalla */
      .block-container{
        padding:0 !important;
        margin:0 !important;
        max-width:100% !important;
      }
      header, footer{ display:none !important; }

      /* Canvas full-viewport */
      #calib-wrapper{
        position:fixed;
        inset:0;
        width:100vw;
        height:100vh;
        overflow:hidden;
        background:#fff;
      }

      /* Cuadrícula (sin efectos) */
      #calib-grid{
        position:absolute;
        inset:0;
        width:100%;
        height:100%;
        background-image:
          linear-gradient(to right, rgba(0,0,0,0.12) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(0,0,0,0.12) 1px, transparent 1px);
        background-size: 24px 24px; /* base desktop */
        background-position: 0 0;
      }

      /* Marco para ver bordes exactos */
      #calib-border{
        position:absolute;
        inset:0;
        border:2px solid rgba(0,0,0,0.35);
        box-sizing:border-box;
        pointer-events:none;
      }

      /* Etiqueta */
      #calib-label{
        position:absolute;
        top:10px;
        left:10px;
        padding:6px 10px;
        font: 12px/1.2 Arial, sans-serif;
        background: rgba(255,255,255,0.9);
        border:1px solid rgba(0,0,0,0.2);
      }

      /* Tablet: grid más grande */
      @media (min-width: 481px) and (max-width: 1024px){
        #calib-grid{ background-size: 32px 32px; }
      }

      /* Móvil: grid más grande */
      @media (max-width: 480px){
        #calib-grid{ background-size: 40px 40px; }
        #calib-label{ font-size: 11px; }
      }
    </style>

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
          label.textContent = `Viewport: ${vw} x ${vh} px | DPR: ${dpr}`;
        }
        window.addEventListener('resize', update);
        update();
      })();
    </script>
    """,
    unsafe_allow_html=True,
)
