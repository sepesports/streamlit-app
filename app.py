# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES (EDITA SOLO ESTO) =====
PAD_X_PX = 10
PAD_TOP_PX = 10
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

TOP_AREA = {
    "count": 4,        # cantidad total de cajas
    "left": 3,         # inicio X (%) dentro del cuadro
    "right": 3,        # fin X (%) dentro del cuadro
    "top": 10,         # Y (%) dentro del cuadro
    "height": 10,      # alto (%) por fila
    "gap_x": 2,        # separación horizontal entre cajas (%) dentro del cuadro
    "gap_y": 2,        # separación vertical entre filas (%) dentro del cuadro
    "max_cols": 4,     # columnas máximas (desktop)
    "prefix": "BTN"
}

BTN_TEXT = "Configuracion"  # 13 caracteres

# Reglas anti-ruptura
MIN_BOX_W_PX = 140     # si no cabe, baja columnas y crea más filas
MOBILE_MAX_W_PX = 520
MOBILE_MIN_LR = 3
MOBILE_MIN_GAP_X = 2
MOBILE_MIN_GAP_Y = 2

FONT_MIN_PX = 12
FONT_MAX_PX = 16
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
      --fmin: __FMIN__px;
      --fmax: __FMAX__px;
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
      background: transparent;
    }

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
      white-space: nowrap;
    }

    /* Plano dentro del cuadro: nada se puede salir */
    #plan{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      overflow:hidden;
      pointer-events:none;
    }

    .blk{
      position:absolute;
      border: 2px dashed rgba(0,0,0,.55);
      box-sizing:border-box;
      background: rgba(0,0,0,.03);

      display:flex;
      align-items:center;
      justify-content:center;

      padding: 6px 8px;
      overflow:hidden;
    }

    .blk-text{
      font-family: Arial, sans-serif;
      font-weight: 700;
      font-size: clamp(var(--fmin), 3.2vw, var(--fmax));
      line-height: 1;
      color: rgba(0,0,0,.85);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }

    .blk-label{
      position:absolute; top:2px; left:2px;
      font: 10px Arial, sans-serif;
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

      <div id="plan">
        <div id="btn-area"></div>
      </div>

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

      var cfg = __TOP_AREA__;
      var BTN_TEXT = "__BTN_TEXT__";
      var MIN_BOX_W_PX = __MIN_BOX_W_PX__;
      var MOBILE_MAX_W_PX = __MOBILE_MAX_W_PX__;
      var MOBILE_MIN_LR = __MOBILE_MIN_LR__;
      var MOBILE_MIN_GAP_X = __MOBILE_MIN_GAP_X__;
      var MOBILE_MIN_GAP_Y = __MOBILE_MIN_GAP_Y__;

      var area = document.getElementById("btn-area");
      var plan = document.getElementById("plan");
      var hud = document.getElementById("hud");

      function ceilDiv(a,b){ return Math.floor((a + b - 1) / b); }

      function build(){
        area.innerHTML = "";

        var vw = window.innerWidth;
        var vh = window.innerHeight;

        var r = plan.getBoundingClientRect();
        var planW = r.width;

        var count = Math.max(1, Number(cfg.count || 1));
        var left = Number(cfg.left || 0);
        var right = Number(cfg.right || 0);
        var top = Number(cfg.top || 0);
        var h = Number(cfg.height || 10);
        var gapX = Number(cfg.gap_x || 0);
        var gapY = Number(cfg.gap_y || 0);
        var maxCols = Math.max(1, Number(cfg.max_cols || count));
        var prefix = String(cfg.prefix || "BTN");

        if (vw <= MOBILE_MAX_W_PX){
          left = Math.max(left, MOBILE_MIN_LR);
          right = Math.max(right, MOBILE_MIN_LR);
          gapX = Math.max(gapX, MOBILE_MIN_GAP_X);
          gapY = Math.max(gapY, MOBILE_MIN_GAP_Y);
        }

        var usable = 100 - left - right;
        if (usable < 1) usable = 1;

        // Elegir columnas (<=maxCols) que cumplan ancho mínimo en px.
        var cols = Math.min(maxCols, count);
        while (cols > 1){
          var wPctTry = (usable - (gapX * (cols - 1))) / cols;
          var wPxTry = (wPctTry / 100) * planW;
          if (wPctTry > 0 && wPxTry >= MIN_BOX_W_PX) break;
          cols -= 1;
        }

        // Filas resultantes
        var rows = ceilDiv(count, cols);

        // Ancho final por caja
        var w = (usable - (gapX * (cols - 1))) / cols;
        if (w < 0) w = 0;

        // Render en filas: 2x2, 3x1, 1x4, etc según columnas elegidas
        for (var i = 0; i < count; i++){
          var row = Math.floor(i / cols);
          var col = i % cols;

          var x = left + col * (w + gapX);
          var y = top + row * (h + gapY);

          var d = document.createElement("div");
          d.className = "blk";
          d.style.left = x + "%";
          d.style.top = y + "%";
          d.style.width = w + "%";
          d.style.height = h + "%";

          var text = document.createElement("div");
          text.className = "blk-text";
          text.textContent = BTN_TEXT;
          d.appendChild(text);

          var lab = document.createElement("span");
          lab.className = "blk-label";
          lab.textContent = prefix + (i+1) + " | " + (row+1) + "x" + (col+1);
          d.appendChild(lab);

          area.appendChild(d);
        }

        hud.textContent =
          "Viewport(px): " + Math.round(vw) + " x " + Math.round(vh) +
          " | Plan(px): " + Math.round(planW) +
          " | cols=" + cols + " rows=" + rows +
          " | w=" + w.toFixed(2) + "% (" + Math.round((w/100)*planW) + "px)";
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
        .replace("__FMIN__", str(FONT_MIN_PX))
        .replace("__FMAX__", str(FONT_MAX_PX))
        .replace("__BTN_TEXT__", BTN_TEXT)
        .replace("__TOP_AREA__", str(TOP_AREA).replace("'", '"'))
        .replace("__MIN_BOX_W_PX__", str(MIN_BOX_W_PX))
        .replace("__MOBILE_MAX_W_PX__", str(MOBILE_MAX_W_PX))
        .replace("__MOBILE_MIN_LR__", str(MOBILE_MIN_LR))
        .replace("__MOBILE_MIN_GAP_X__", str(MOBILE_MIN_GAP_X))
        .replace("__MOBILE_MIN_GAP_Y__", str(MOBILE_MIN_GAP_Y))
)

components.html(html, height=10, scrolling=False)
