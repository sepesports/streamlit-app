# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES (EDITA SOLO ESTO) =====
PAD_X_PX = 10
PAD_TOP_PX = 10
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

TOP_ROW = {
    "count": 4,
    "left": 5,      # prueba 3 vs 5 aquí
    "right": 5,     # prueba 3 vs 5 aquí
    "top": 10,
    "height": 10,
    "gap": 2,
    "prefix": "BTN"
}

MIN_BOX_W_PX = 64
MOBILE_MAX_W_PX = 520
MOBILE_MIN_LR = 3
MOBILE_MIN_GAP = 2
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

    #overlay{position:absolute;inset:0;pointer-events:none;}

    .grid{
      position:absolute;inset:0;
      background-image:
        linear-gradient(to right, rgba(0,0,0,0.08) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0,0,0,0.08) 1px, transparent 1px);
      background-size: 10% 10%;
    }

    /* Bandas de LEFT/RIGHT para ver el % real */
    #band-left{
      position:absolute; top:0; bottom:0; left:0;
      background: rgba(0,0,0,0.05);
    }
    #band-right{
      position:absolute; top:0; bottom:0; right:0;
      background: rgba(0,0,0,0.05);
    }

    #hud{
      position:absolute; top:8px; left:8px;
      font: 14px Arial, sans-serif;
      background: rgba(255,255,255,.95);
      border: 1px solid rgba(0,0,0,.25);
      border-radius: 6px;
      padding: 8px 12px;
      pointer-events:none;
    }

    .blk{
      position:absolute;
      border: 2px dashed rgba(0,0,0,.55);
      box-sizing:border-box;
      background: rgba(0,0,0,.02);
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

      <div id="band-left"></div>
      <div id="band-right"></div>

      <div id="top-row"></div>
      <div id="hud">Cargando...</div>
    </div>
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

      var cfg = __TOP_ROW__;
      var MIN_BOX_W_PX = __MIN_BOX_W_PX__;
      var MOBILE_MAX_W_PX = __MOBILE_MAX_W_PX__;
      var MOBILE_MIN_LR = __MOBILE_MIN_LR__;
      var MOBILE_MIN_GAP = __MOBILE_MIN_GAP__;

      var container = document.getElementById("top-row");
      var hud = document.getElementById("hud");
      var bandL = document.getElementById("band-left");
      var bandR = document.getElementById("band-right");

      function build(){
        container.innerHTML = "";

        var vw = window.innerWidth;
        var vh = window.innerHeight;

        var n0 = Math.max(1, Number(cfg.count || 1));
        var left = Number(cfg.left || 0);
        var right = Number(cfg.right || 0);
        var top = Number(cfg.top || 0);
        var h = Number(cfg.height || 10);
        var gap = Number(cfg.gap || 0);
        var prefix = String(cfg.prefix || "BTN");

        // Clamp solo para móvil si vienen más bajos que el mínimo
        if (vw <= MOBILE_MAX_W_PX){
          if (left < MOBILE_MIN_LR) left = MOBILE_MIN_LR;
          if (right < MOBILE_MIN_LR) right = MOBILE_MIN_LR;
          if (gap < MOBILE_MIN_GAP) gap = MOBILE_MIN_GAP;
        }

        // Bandas visuales de left/right
        bandL.style.width = left + "%";
        bandR.style.width = right + "%";

        var usable = 100 - left - right;
        if (usable < 1) usable = 1;

        // Auto-reduce columnas si no cabe por px
        var n = n0;
        while (n > 1){
          var wPctTry = (usable - (gap * (n - 1))) / n;
          var wPxTry = (wPctTry / 100) * vw;
          if (wPctTry > 0 && wPxTry >= MIN_BOX_W_PX) break;
          n -= 1;
        }

        var w = (usable - (gap * (n - 1))) / n;
        if (w < 0) w = 0;

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
          lab.textContent = prefix + (i+1) + " | x=" + x.toFixed(2) + " w=" + w.toFixed(2);
          d.appendChild(lab);

          container.appendChild(d);
        }

        hud.textContent =
          "VW×VH=" + Math.round(vw) + "×" + Math.round(vh) +
          " | cfg(L,R,gap)=(" + cfg.left + "," + cfg.right + "," + cfg.gap + ")" +
          " | usado(L,R,gap)=(" + left + "," + right + "," + gap + ")" +
          " | cajas=" + n + "/" + n0;
      }

      window.addEventListener("resize", build);
      build();
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
        .replace("__MIN_BOX_W_PX__", str(MIN_BOX_W_PX))
        .replace("__MOBILE_MAX_W_PX__", str(MOBILE_MAX_W_PX))
        .replace("__MOBILE_MIN_LR__", str(MOBILE_MIN_LR))
        .replace("__MOBILE_MIN_GAP__", str(MOBILE_MIN_GAP))
)

components.html(html, height=10, scrolling=False)
