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
    "count": 4,       # cantidad de cajas
    "left": 3,        # inicio X (%) Distancia desde la Izquierda (relativo al cuadro)
    "right": 3,       # fin X (%) Distancia desde la Derecha (relativo al cuadro)
    "top": 10,        # Y (%) que tan abajo (relativo al cuadro)
    "height": 10,     # alto (%) (relativo al cuadro)
    "gap": 2,         # separación entre cajas (%) (relativo al cuadro)
    "prefix": "BTN"   # etiqueta
}

# Texto de prueba (13 caracteres)
BTN_TEXT = "Configuracion"

# Reglas anti-ruptura (móvil/tablet)
MIN_BOX_W_PX = 140     # asegura lectura de "Configuracion" (auto-reduce columnas si no cabe)
MOBILE_MAX_W_PX = 520  # <= esto se considera móvil
MOBILE_MIN_LR = 3      # left/right mínimo en móvil (%)
MOBILE_MIN_GAP = 2     # gap mínimo en móvil (%)

# Tipografía texto dentro de caja (ajuste automático)
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

    /* Overlay general */
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

    /* Contenedor del "plano" dentro del cuadro (para que NO se salga del marco) */
    #plan{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      overflow:hidden; /* clave: recorta cualquier cosa fuera del cuadro */
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

    /* Texto grande dentro (sin salirse del cuadro) */
    .blk-text{
      font-family: Arial, sans-serif;
      font-weight: 700;
      font-size: clamp(var(--fmin), 3.2vw, var(--fmax));
      line-height: 1;
      color: rgba(0,0,0,.85);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis; /* fallback si alguien reduce demasiado */
      max-width: 100%;
    }

    /* Etiqueta técnica pequeña (esquina) */
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
        <div id="top-row"></div>
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

      var cfg = __TOP_ROW__;
      var BTN_TEXT = "__BTN_TEXT__";
      var MIN_BOX_W_PX = __MIN_BOX_W_PX__;
      var MOBILE_MAX_W_PX = __MOBILE_MAX_W_PX__;
      var MOBILE_MIN_LR = __MOBILE_MIN_LR__;
      var MOBILE_MIN_GAP = __MOBILE_MIN_GAP__;

      var container = document.getElementById("top-row");
      var plan = document.getElementById("plan");
      var hud = document.getElementById("hud");

      function buildTopRow(){
        container.innerHTML = "";

        var vw = window.innerWidth;

        // Dimensiones reales del "cuadro" interior (plan)
        var r = plan.getBoundingClientRect();
        var planW = r.width;

        var n = Math.max(1, Number(cfg.count || 1));
        var left = Number(cfg.left || 0);
        var right = Number(cfg.right || 0);
        var top = Number(cfg.top || 0);
        var h = Number(cfg.height || 10);
        var gap = Number(cfg.gap || 0);
        var prefix = String(cfg.prefix || "BTN");

        // En móvil: mínimos para no romper
        if (vw <= MOBILE_MAX_W_PX){
          left = Math.max(left, MOBILE_MIN_LR);
          right = Math.max(right, MOBILE_MIN_LR);
          gap = Math.max(gap, MOBILE_MIN_GAP);
        }

        // usable% dentro del cuadro (plan)
        var usable = 100 - left - right;
        if (usable < 1) usable = 1;

        // Auto-reduce columnas hasta que el ancho en px sea >= MIN_BOX_W_PX
        while (n > 1){
          var wPct = (usable - (gap * (n - 1))) / n;
          var wPx = (wPct / 100) * planW;
          if (wPct > 0 && wPx >= MIN_BOX_W_PX) break;
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

          var text = document.createElement("div");
          text.className = "blk-text";
          text.textContent = BTN_TEXT;
          d.appendChild(text);

          var lab = document.createElement("span");
          lab.className = "blk-label";
          lab.textContent = prefix + (i+1) + " | n=" + n + " | w=" + w.toFixed(2) + "%";
          d.appendChild(lab);

          container.appendChild(d);
        }

        hud.textContent =
          "Viewport(px): " + Math.round(window.innerWidth) + " x " + Math.round(window.innerHeight) +
          " | Plan(px): " + Math.round(planW) +
          " | LR=" + left + "/" + right + " gap=" + gap +
          " | cajas=" + n + " | w=" + w.toFixed(2) + "% (" + Math.round((w/100)*planW) + "px)";
      }

      window.addEventListener("resize", buildTopRow);
      buildTopRow();
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
        .replace("__TOP_ROW__", str(TOP_ROW).replace("'", '"'))
        .replace("__MIN_BOX_W_PX__", str(MIN_BOX_W_PX))
        .replace("__MOBILE_MAX_W_PX__", str(MOBILE_MAX_W_PX))
        .replace("__MOBILE_MIN_LR__", str(MOBILE_MIN_LR))
        .replace("__MOBILE_MIN_GAP__", str(MOBILE_MIN_GAP))
)

components.html(html, height=10, scrolling=False)
