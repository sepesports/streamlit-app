# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES (EDITA SOLO ESTO) =====
PAD_X_PX = 10
PAD_TOP_PX = 10
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

# Layout superior en grilla (todo automático)
TOP_ROW = {
    "count": 4,       # cantidad de cajas
    "left": 2,       # inicio X (%) Distancia desde la Izquierda 
    "right": 2,      # fin X (%)
    "top": 10,        # Y (%) que tan abajo
    "height": 10,     # alto (%)
    "gap": 2,         # separación entre cajas (%)
    "prefix": "BTN"   # etiqueta
}
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
    html, body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:var(--bg);}
    #stage{position:fixed;inset:0;width:100vw;height:100vh;background:var(--bg);}

    /* Marco (izq/der/sup) */
    #frame{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      border-left:var(--b) solid var(--bc);
      border-right:var(--b) solid var(--bc);
      border-top:var(--b) solid var(--bc);
      box-sizing:border-box;
      pointer-events:none;
    }

    /* Plano */
    #overlay{position:absolute;inset:0;pointer-events:none;}
    .grid{
      position:absolute;inset:0;
      background-image:
        linear-gradient(to right, rgba(0,0,0,0.10) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0,0,0,0.10) 1px, transparent 1px);
      background-size: 10% 10%;
    }
    .mid-v{position:absolute;left:50%;top:0;bottom:0;width:1px;background:rgba(0,0,0,.25);}
    .mid-h{position:absolute;top:50%;left:0;right:0;height:1px;background:rgba(0,0,0,.25);}

    #hud{
      position:absolute; top:8px; left:8px;
      font: 12px Arial, sans-serif;
      background: rgba(255,255,255,.92);
      border: 1px solid rgba(0,0,0,.2);
      border-radius: 6px;
      padding: 6px 10px;
      pointer-events:none;
    }

    .blk{
      position:absolute;
      border: 2px dashed rgba(0,0,0,.55);
      box-sizing:border-box;
      background: rgba(0,0,0,.03);
    }
    .blk-label{
      position:absolute; top:2px; left:2px;
      font: 11px Arial, sans-serif;
      background: rgba(255,255,255,.9);
      border: 1px solid rgba(0,0,0,.15);
      border-radius: 4px;
      padding: 2px 6px;
      white-space: nowrap;
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="overlay">
      <div class="grid"></div>
      <div class="mid-v"></div>
      <div class="mid-h"></div>

      <div id="top-row"></div>

      <div id="hud">Cargando...</div>
    </div>
  </div>

  <script>
    (function(){
      // Full-screen real del iframe
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

      var cfg = __TOP_ROW__;
      var container = document.getElementById("top-row");

      function buildTopRow(){
        container.innerHTML = "";

        var n = Math.max(1, Number(cfg.count || 1));
        var left = Number(cfg.left || 0);
        var right = Number(cfg.right || 0);
        var top = Number(cfg.top || 0);
        var h = Number(cfg.height || 10);
        var gap = Number(cfg.gap || 0);
        var prefix = String(cfg.prefix || "BTN");

        // ancho util disponible en %
        var usable = 100 - left - right;

        // ancho por caja (todas iguales)
        var w = (usable - (gap * (n - 1))) / n;

        for (var i = 0; i < n; i++){
          var x = left + i * (w + gap);

          var d = document.createElement("div");
          d.className = "blk";
          d.style.left = x + "%";
          d.style.top = top + "%";
          d.style.width = w + "%";
          d.style.height = h + "%";

          var lab = document.createElement("span");
          lab.className = "blk-label";
          lab.textContent = prefix + (i+1) + " x=" + x.toFixed(2) + " w=" + w.toFixed(2);
          d.appendChild(lab);

          container.appendChild(d);
        }
      }

      var hud = document.getElementById("hud");
      function updateHud(){
        var vw = Math.round(window.innerWidth);
        var vh = Math.round(window.innerHeight);
        hud.textContent =
          "Viewport(px): " + vw + " x " + vh +
          " | Mitad: " + Math.round(vw/2) + " x " + Math.round(vh/2) +
          " | 10%=" + Math.round(vw*0.10) + "px";
      }

      window.addEventListener("resize", function(){
        buildTopRow();
        updateHud();
      });

      buildTopRow();
      updateHud();
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
        .replace("__TOP_ROW__", str(TOP_ROW).replace("'", '"'))
)

components.html(html, height=10, scrolling=False)
