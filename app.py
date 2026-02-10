# app.py
import streamlit as st
import streamlit.components.v1 as components

# =============================================================================
# PLANTILLA "PLANO" RESPONSIVO (STREAMLIT CLOUD)
# - Todas las medidas del layout (header/imagen/botones/footer) están en % DEL CUADRO.
# - El "CUADRO" es el área interior delimitada por el marco (izq/der/sup) que ya calibraste.
# - Regla: 0%..100% siempre se interpreta RELATIVO al ancho/alto del CUADRO, no del viewport.
#
# CÓMO AJUSTAR RÁPIDO (preciso):
# 1) Espacios externos del CUADRO (px):
#    - PAD_X_PX  : separa el cuadro de los bordes laterales del viewport (en px).
#    - PAD_TOP_PX: separa el cuadro de la parte superior del viewport (en px).
#
# 2) Bordes (px / color):
#    - BORDER_PX / BORDER_COLOR
#
# 3) HEADER (en % del CUADRO):
#    - HEADER_TOP      : 0 normalmente (arranca en el borde superior del cuadro)
#    - HEADER_HEIGHT   : alto del header (ej 8–12)
#    - HEADER_CELLS    : distribución horizontal en % (suma ideal ~100)
#
# 4) IMAGEN (en % del CUADRO):
#    - IMG_LEFT/IMG_RIGHT : margen lateral dentro del cuadro
#    - IMG_TOP            : distancia desde arriba del cuadro (debajo del header)
#    - IMG_HEIGHT         : alto del bloque imagen
#
# 5) ÁREA DE BOTONES (en % del CUADRO):
#    - BTN_AREA_TOP    : desde qué % vertical empieza la sección inferior (botones/fondo2/footer)
#    - BTN_LEFT/RIGHT  : márgenes laterales del grid de botones dentro del cuadro
#    - BTN_H           : alto de cada botón (por fila) en % del cuadro
#    - BTN_GAP_X/Y     : separación horizontal/vertical entre botones en % del cuadro
#    - MIN_BTN_W_PX    : ancho mínimo por botón en px -> si no caben 3, baja a 2 o 1 automáticamente
#
# 6) FOOTER (en % del CUADRO):
#    - FOOTER_LEFT/RIGHT : márgenes laterales del footer
#    - FOOTER_H          : alto del footer
#    - FOOTER_BOTTOM     : distancia desde abajo del cuadro hacia arriba
#
# 7) Colores:
#    - BG_COLOR   : fondo general (verde)
#    - HEADER_BG  : fondo header (amarillo)
#    - IMG_BG     : fondo imagen (blanco)
#    - BTN_BG     : fondo botones (blanco)
#    - FOOTER_BG  : fondo footer (blanco)
#
# HUD (arriba izquierda) muestra: viewport, ancho del cuadro (Plan), columnas calculadas y ancho px.
# =============================================================================

# ================== AJUSTES (EDITA SOLO ESTO) ==================
# 0) CUADRO (px) -> precisión fina
PAD_X_PX = 10          # px: margen exterior lateral del cuadro (viewport -> cuadro)
PAD_TOP_PX = 10        # px: margen exterior superior del cuadro (viewport -> cuadro)

# 1) Bordes
BORDER_PX = 2          # px: grosor bordes
BORDER_COLOR = "#111111"

# 2) Colores de secciones
BG_COLOR = "#CFE3BF"        # verde claro (fondo general)
HEADER_BG = "#FFF200"       # amarillo (Fondo 1)
IMG_BG = "#FFFFFF"          # blanco (Imagen)
BTN_BG = "#FFFFFF"          # blanco (botones)
FOOTER_BG = "#FFFFFF"       # blanco (pie)

# 3) HEADER (en % del CUADRO)
HEADER_TOP = 0              # %: distancia desde arriba del cuadro
HEADER_HEIGHT = 10          # %: alto del header

# Distribución horizontal del header (en % del ancho del CUADRO)
# Orden: [margen_izq, Logo, Fondo 1, Login, margen_der]
# Recomendación: que sumen 100 (o cercano).
HEADER_CELLS = [
    {"w": 6,  "t": "",        "white": False},
    {"w": 22, "t": "Logo",    "white": True},
    {"w": 44, "t": "Fondo 1", "white": False},
    {"w": 22, "t": "Login",   "white": True},
    {"w": 6,  "t": "",        "white": False},
]

# 4) IMAGEN (en % del CUADRO)
IMG_LEFT = 6          # %: margen lateral interno (cuadro -> bloque imagen)
IMG_RIGHT = 6         # %: margen lateral interno
IMG_TOP = 12          # %: distancia desde arriba del cuadro (debajo del header)
IMG_HEIGHT = 38       # %: alto del bloque imagen

# 5) BOTONES (en % del CUADRO)
BTN_AREA_TOP = 55     # %: desde aquí inicia la sección inferior (botones + "Fondo 2" + footer)

BTN_LEFT = 6          # %: margen izquierdo del grid de botones dentro del cuadro
BTN_RIGHT = 6         # %: margen derecho del grid de botones dentro del cuadro

BTN_H = 10            # %: alto de cada botón por fila (más alto = más aire)
BTN_GAP_X = 3         # %: separación horizontal entre botones
BTN_GAP_Y = 5         # %: separación vertical entre filas de botones

BTN_TEXTS = [
    "Horarios",
    "Control de\nAsistencia",
    "Nomina y\nPagos",
    "Incidencias",
    "Formación",
    "Comunicados",
]

# Texto "Fondo 2" (posición vertical dentro de la sección inferior, en % del CUADRO)
FONDO2_BOTTOM = 22    # %: sube/baja el texto "Fondo 2" (mayor = más arriba)

# 6) FOOTER (en % del CUADRO)
FOOTER_LEFT = 6       # %: margen lateral del footer
FOOTER_RIGHT = 6      # %: margen lateral del footer
FOOTER_H = 8          # %: alto del footer
FOOTER_BOTTOM = 3     # %: separación desde abajo del cuadro

# 7) Responsivo / reglas de ruptura (px)
MIN_BTN_W_PX = 150     # px: ancho mínimo por botón. Si no cabe 3, baja a 2; si no, a 1.
MOBILE_MAX_W_PX = 520  # px: umbral para tratar como móvil (aplica mínimos de gaps si quieres)
# ===============================================================

st.set_page_config(layout="wide")

# Quitar padding/márgenes de Streamlit
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
      --headerbg: __HEADERBG__;
      --imgbg: __IMGBG__;
      --btnbg: __BTNBG__;
      --footerbg: __FOOTERBG__;
    }

    html, body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:var(--bg);}
    #stage{position:fixed;inset:0;width:100vw;height:100vh;background:var(--bg);}

    /* Marco visible (izq/der/sup) */
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
      z-index: 2;
    }

    /* CUADRO/PLAN: todo el layout vive aquí dentro y NO puede salirse */
    #plan{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      overflow:hidden;
      z-index: 1;
    }

    /* Header */
    #hdr{
      position:absolute;
      left:0; right:0;
      top: __HDR_TOP__%;
      height: __HDR_H__%;
      background: var(--headerbg);
      border: var(--b) solid var(--bc);
      box-sizing:border-box;
      display:flex;
      gap:0;
    }

    .hdr-cell{
      border-right: var(--b) solid var(--bc);
      box-sizing:border-box;
      background: var(--headerbg);
      display:flex;
      align-items:center;
      justify-content:center;
      font: 14px Arial, sans-serif;
      font-weight: 700;
      color:#000;
      white-space: nowrap;
      overflow:hidden;
      text-overflow: ellipsis;
    }
    .hdr-cell.white{ background:#fff; }
    .hdr-cell:last-child{ border-right: none; }

    /* Imagen */
    #img{
      position:absolute;
      left: __IMG_L__%;
      right: __IMG_R__%;
      top: __IMG_T__%;
      height: __IMG_H__%;
      background: var(--imgbg);
      border: var(--b) solid var(--bc);
      box-sizing:border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      font: 16px Arial, sans-serif;
      font-weight: 700;
      color:#000;
    }

    /* Sección inferior (Fondo 2 + botones + footer) */
    #btn-area{
      position:absolute;
      left:0; right:0;
      top: __BTN_AREA_TOP__%;
      bottom: 0;
      background: var(--bg);
      box-sizing:border-box;
    }

    /* Grid de botones */
    #btn-grid{
      position:absolute;
      left: __BTN_L__%;
      right: __BTN_R__%;
      top: 0;
      bottom: 0;
    }

    .btn{
      position:absolute;
      background: var(--btnbg);
      border: var(--b) solid var(--bc);
      box-sizing:border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      padding: 8px 10px;
      font: 14px Arial, sans-serif;
      font-weight: 700;
      color:#000;
      overflow:hidden;
    }
    .btn span{
      display:block;
      line-height:1.05;
      white-space: pre-line; /* respeta \n */
    }

    /* Texto "Fondo 2" */
    #fondo2{
      position:absolute;
      left:0; right:0;
      bottom: __F2_BOTTOM__%;
      text-align:center;
      font: 13px Arial, sans-serif;
      font-weight: 700;
      color:#000;
      pointer-events:none;
    }

    /* Footer */
    #footer{
      position:absolute;
      left: __FOOT_L__%;
      right: __FOOT_R__%;
      height: __FOOT_H__%;
      bottom: __FOOT_BOTTOM__%;
      background: var(--footerbg);
      border: var(--b) solid var(--bc);
      box-sizing:border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      font: 13px Arial, sans-serif;
      font-weight: 700;
      color:#000;
    }

    /* HUD */
    #hud{
      position:absolute; top:8px; left:8px;
      font: 12px Arial, sans-serif;
      background: rgba(255,255,255,.92);
      border: 1px solid rgba(0,0,0,.2);
      border-radius: 6px;
      padding: 6px 10px;
      white-space: nowrap;
      pointer-events:none;
      z-index: 3;
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="plan">
      <div id="hdr"></div>
      <div id="img">Imagen</div>

      <div id="btn-area">
        <div id="btn-grid"></div>
        <div id="fondo2">Fondo 2</div>
        <div id="footer">Pie de pagina</div>
      </div>

      <div id="hud">Cargando...</div>
    </div>
  </div>

  <script>
    (function(){
      // Full-screen real del iframe (Streamlit Cloud)
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

      var HEADER_CELLS = __HEADER_CELLS__;
      var BTN_TEXTS = __BTN_TEXTS__;
      var MIN_BTN_W_PX = __MIN_BTN_W_PX__;
      var MOBILE_MAX_W_PX = __MOBILE_MAX_W_PX__;

      var hud = document.getElementById("hud");
      var hdr = document.getElementById("hdr");
      var grid = document.getElementById("btn-grid");
      var plan = document.getElementById("plan");

      function ceilDiv(a,b){ return Math.floor((a + b - 1) / b); }

      function buildHeader(){
        hdr.innerHTML = "";
        HEADER_CELLS.forEach(function(c){
          var d = document.createElement("div");
          d.className = "hdr-cell" + (c.white ? " white" : "");
          d.style.width = c.w + "%";
          d.textContent = c.t || "";
          hdr.appendChild(d);
        });
      }

      function buildButtons(){
        grid.innerHTML = "";

        var vw = window.innerWidth;
        var r = plan.getBoundingClientRect();
        var planW = r.width;

        // Config grilla (en % del CUADRO)
        var left = __BTN_L__;
        var right = __BTN_R__;
        var gapX = __BTN_GAP_X__;
        var gapY = __BTN_GAP_Y__;
        var btnH = __BTN_H__;

        // En móvil, evita gaps demasiado pequeños
        if (vw <= MOBILE_MAX_W_PX){
          if (gapX < 2) gapX = 2;
          if (gapY < 3) gapY = 3;
        }

        var count = BTN_TEXTS.length;

        // Intento: 3 columnas. Si el ancho en px cae por debajo del mínimo, baja a 2 o 1.
        var cols = 3;
        var usable = 100 - left - right;

        while (cols > 1){
          var wPctTry = (usable - (gapX * (cols - 1))) / cols;
          var wPxTry = (wPctTry / 100) * planW;
          if (wPctTry > 0 && wPxTry >= MIN_BTN_W_PX) break;
          cols -= 1;
        }

        var rows = ceilDiv(count, cols);
        var w = (usable - (gapX * (cols - 1))) / cols;
        if (w < 0) w = 0;

        for (var i=0;i<count;i++){
          var row = Math.floor(i/cols);
          var col = i%cols;

          var x = left + col*(w + gapX);
          var y = row*(btnH + gapY);

          var d = document.createElement("div");
          d.className = "btn";
          d.style.left = x + "%";
          d.style.top = y + "%";
          d.style.width = w + "%";
          d.style.height = btnH + "%";

          var sp = document.createElement("span");
          sp.textContent = BTN_TEXTS[i];
          d.appendChild(sp);

          grid.appendChild(d);
        }

        hud.textContent =
          "Viewport(px): " + Math.round(window.innerWidth) + " x " + Math.round(window.innerHeight) +
          " | PlanW(px): " + Math.round(planW) +
          " | cols=" + cols + " rows=" + rows +
          " | btnW(px)=" + Math.round((w/100)*planW);
      }

      function update(){
        buildHeader();
        buildButtons();
      }

      window.addEventListener("resize", update);
      update();
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
        .replace("__HEADERBG__", HEADER_BG)
        .replace("__IMGBG__", IMG_BG)
        .replace("__BTNBG__", BTN_BG)
        .replace("__FOOTERBG__", FOOTER_BG)
        .replace("__HDR_TOP__", str(HEADER_TOP))
        .replace("__HDR_H__", str(HEADER_HEIGHT))
        .replace("__HEADER_CELLS__", str(HEADER_CELLS).replace("'", '"'))
        .replace("__IMG_L__", str(IMG_LEFT))
        .replace("__IMG_R__", str(IMG_RIGHT))
        .replace("__IMG_T__", str(IMG_TOP))
        .replace("__IMG_H__", str(IMG_HEIGHT))
        .replace("__BTN_AREA_TOP__", str(BTN_AREA_TOP))
        .replace("__BTN_L__", str(BTN_LEFT))
        .replace("__BTN_R__", str(BTN_RIGHT))
        .replace("__BTN_H__", str(BTN_H))
        .replace("__BTN_GAP_X__", str(BTN_GAP_X))
        .replace("__BTN_GAP_Y__", str(BTN_GAP_Y))
        .replace("__F2_BOTTOM__", str(FONDO2_BOTTOM))
        .replace("__FOOT_L__", str(FOOTER_LEFT))
        .replace("__FOOT_R__", str(FOOTER_RIGHT))
        .replace("__FOOT_H__", str(FOOTER_H))
        .replace("__FOOT_BOTTOM__", str(FOOTER_BOTTOM))
        .replace("__BTN_TEXTS__", str(BTN_TEXTS).replace("'", '"'))
        .replace("__MIN_BTN_W_PX__", str(MIN_BTN_W_PX))
        .replace("__MOBILE_MAX_W_PX__", str(MOBILE_MAX_W_PX))
)

components.html(html, height=10, scrolling=False)
