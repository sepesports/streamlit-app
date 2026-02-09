# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

components.html(
    """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    html, body {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #fff;
    }

    /* Full viewport */
    #calib-wrapper{
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background: #fff;
    }

    /* Grid */
    #calib-grid{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      background-image:
        linear-gradient(to right, rgba(0,0,0,0.12) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0,0,0,0.12) 1px, transparent 1px);
      background-size: 24px 24px; /* desktop base */
      background-position: 0 0;
    }

    /* Border */
    #calib-border{
      position: absolute;
      inset: 0;
      border: 2px solid rgba(0,0,0,0.35);
      box-sizing: border-box;
      pointer-events: none;
    }

    /* Label */
    #calib-label{
      position: absolute;
      top: 10px;
      left: 10px;
      padding: 6px 10px;
      font: 12px/1.2 Arial, sans-serif;
      background: rgba(255,255,255,0.92);
      border: 1px solid rgba(0,0,0,0.2);
      border-radius: 6px;
    }

    /* Tablet */
    @media (min-width: 481px) and (max-width: 1024px){
      #calib-grid{ background-size: 32px 32px; }
    }

    /* Mobile */
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
        label.textContent = "Viewport: " + vw + " x " + vh + " px | DPR: " + dpr;
      }

      window.addEventListener('resize', update);
      update();
    })();
  </script>
</body>
</html>
""",
    height=1200,
    scrolling=False,
)
