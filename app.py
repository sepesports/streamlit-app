# app.py
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# PLANO RESPONSIVO (BASE) — MISMA VERSIÓN QUE SUBISTE (SIN CAMBIAR LAYOUT)
# ==============================================================================
# REGLAS IMPORTANTES (para ajustar con precisión):
#
# A) UNIDADES
# 1) PAD_X_PX / PAD_TOP_PX están en PIXELES (px).
#    - Controlan el “cuadro” (plan) dentro del viewport.
#    - Si quieres que el marco quede más pegado a la pantalla: baja PAD_X_PX / PAD_TOP_PX.
#
# 2) La mayoría de medidas del layout están en PORCENTAJE (%) DEL CUADRO.
#    - Ej: IMG_LEFT = 6 significa “6% del ANCHO del cuadro”, no del viewport.
#    - Ej: IMG_TOP = 12 significa “12% del ALTO del cuadro desde arriba”.
#
# 3) MIN_BTN_W_PX está en PIXELES (px) y es la regla más importante del responsivo:
#    - Define el ANCHO MÍNIMO permitido por botón.
#    - Si en móvil no caben 3 columnas con ese mínimo, el layout baja automáticamente a 2 o 1.
#
# B) CÓMO MOVER/ESCALAR CADA SECCIÓN (sin romper nada)
# 1) HEADER:
#    - HEADER_TOP: normalmente 0.
#    - HEADER_HEIGHT: sube/baja el alto del header (8–12 suele ser rango sano).
#
# 2) IMAGEN:
#    - IMG_LEFT/IMG_RIGHT: “margen interno” lateral de la imagen.
#      (más grande = imagen más angosta, más aire a los lados)
#    - IMG_TOP: qué tan abajo arranca la imagen.
#    - IMG_HEIGHT: qué tan alta es la imagen.
#
# 3) ZONA BOTONES:
#    - BTN_AREA_TOP: desde qué % vertical empieza “Fondo 2” (zona verde inferior).
#      (más grande = zona botones arranca más abajo, menos espacio para botones)
#    - BTN_LEFT/BTN_RIGHT: márgenes laterales del grid de botones.
#    - BTN_H: alto de cada botón (por fila).
#    - BTN_GAP_X: separación horizontal entre botones.
#    - BTN_GAP_Y: separación vertical entre filas.
#
# 4) FOOTER:
#    - FOOTER_LEFT/FOOTER_RIGHT: márgenes laterales del footer.
#    - FOOTER_H: alto del footer.
#    - FOOTER_BOTTOM: separación desde abajo del cuadro.
#
# C) “FONDO 2”
# - El texto "Fondo 2" se posiciona con __F2_BOTTOM__ (por ahora fijo a "22").
#   Si quieres que sea editable como variable, lo dejo en comentarios listo.
#
# D) LECTURA / DEBUG (HUD)
# - El HUD muestra:
#   Viewport(px)  -> tamaño real de la pantalla
#   Plan(px)      -> ancho del cuadro (planW)
#   cols/rows     -> columnas/filas calculadas por el responsivo
#   btnW          -> ancho real de cada botón en % y en px
# ==============================================================================

# ================== AJUSTES (EDITA SOLO ESTO) ==================

# (1) CUADRO / MARCO (px) — Ajuste fino contra bordes de la pantalla
PAD_X_PX = 8   # px | margen externo izquierda/derecha del CUADRO
PAD_TOP_PX = 8 # px | margen externo superior del CUADRO

# (2) BORDES (px + color)
BORDER_PX = 2
BORDER_COLOR = "#111111"

# (3) COLORES (hex)
BG_COLOR = "#CFE3BF"        # Fondo general (verde)
HEADER_BG = "#FFF200"       # Fondo header (amarillo)
IMG_BG = "#FFFFFF"          # Fondo imagen (blanco)
BTN_BG = "#FFFFFF"          # Fondo botones (blanco)
FOOTER_BG = "#FFFFFF"       # Fondo footer (blanco)

# (4) IMAGEN (todo en % DEL CUADRO)
IMG_LEFT = 0     # % | margen interno izquierdo de la imagen (la hace más angosta si sube) 
IMG_RIGHT = 0    # % | margen interno derecho
IMG_TOP = 10     # % | distancia desde arriba del cuadro (baja la imagen si sube)
IMG_HEIGHT = 44  # % | alto del bloque de imagen

# (5) HEADER (todo en % DEL CUADRO)
HEADER_TOP = 0       # % | distancia desde arriba del cuadro
HEADER_HEIGHT = 12   # % | alto del header

# (6) BOTONES (todo en % DEL CUADRO)
BTN_AREA_TOP = 55    # % | desde aquí empieza la sección inferior (Fondo2 + botones + footer)
BTN_H = 23           # % | alto de cada botón
BTN_GAP_X = 2        # % | separación horizontal entre botones
BTN_GAP_Y = 2        # % | separación vertical entre filas  
BTN_LEFT = 5         # % | margen interno izquierdo del grid de botones
BTN_RIGHT = 5        # % | margen interno derecho del grid de botones

BTN_TEXTS = [
    "Horarios",
    "Control de\nAsistencia",
    "Nomina y\nPagos",
    "Incidencias",
    "Formación",
    "Comunicados",
]

# (7) FOOTER (todo en % DEL CUADRO)
FOOTER_H = 18         # % | alto del footer Estoy aqui
FOOTER_BOTTOM = 5    # % | separación desde abajo del cuadro (sube el footer si sube)
FOOTER_LEFT = 6      # % | margen lateral del footer
FOOTER_RIGHT = 6     # % | margen lateral del footer

# (8) RESPONSIVO (px)
MIN_BTN_W_PX = 130   # px | ancho mínimo por botón antes de bajar columnas (3 -> 2 -> 1)
MOBILE_MAX_W_PX = 500  # px | umbral para aplicar mínimos de gap en móvil

# (9) (Opcional) Si quieres controlar la posición del texto "Fondo 2" desde Python:
# FONDO2_BOTTOM = 30  # % | cuanto más grande, más arriba aparece el texto
# ===============================================================

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
      --headerbg: __HEADERBG__;
      --imgbg: __IMGBG__;
      --btnbg: __BTNBG__;
      --footerbg: __FOOTERBG__;
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
      background: transparent;
    }

    /* Plano dentro del cuadro: nada se sale */
    #plan{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      overflow:hidden;
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

    /* Fondo 2 (área botones) */
    #btn-area{
      position:absolute;
      left:0; right:0;
      top: __BTN_AREA_TOP__%;
      bottom: 0;
      background: var(--bg);
      box-sizing:border-box;
    }
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
      white-space: pre-line; /* respeta \\n */
    }

    /* Label Fondo 2 */
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

      var BTN_TEXTS = __BTN_TEXTS__;
      var MIN_BTN_W_PX = __MIN_BTN_W_PX__;
      var MOBILE_MAX_W_PX = __MOBILE_MAX_W_PX__;

      // Header cells (5 columnas como imagen: margen, Logo, Fondo1, Login, margen)
      var hdr = document.getElementById("hdr");
      hdr.innerHTML = "";
      var cells = [
        {w: 6,  t:"",        white:false},
        {w: 22, t:"Logo",    white:true},
        {w: 44, t:"Fondo 1", white:false},
        {w: 22, t:"Login",   white:true},
        {w: 6,  t:"",        white:false},
      ];
      cells.forEach(function(c){
        var d = document.createElement("div");
        d.className = "hdr-cell" + (c.white ? " white" : "");
        d.style.width = c.w + "%";
        d.textContent = c.t;
        hdr.appendChild(d);
      });

      var hud = document.getElementById("hud");
      var grid = document.getElementById("btn-grid");
      var plan = document.getElementById("plan");

      function ceilDiv(a,b){ return Math.floor((a + b - 1) / b); }

      function buildButtons(){
        grid.innerHTML = "";

        var vw = window.innerWidth;
        var r = plan.getBoundingClientRect();
        var planW = r.width;

        // Config grilla (en % del cuadro)
        var left = __BTN_L__;
        var right = __BTN_R__;
        var gapX = __BTN_GAP_X__;
        var gapY = __BTN_GAP_Y__;
        var btnH = __BTN_H__;

        // En móvil: asegura mínimos para que no se peguen demasiado
        if (vw <= MOBILE_MAX_W_PX){
          if (gapX < 2) gapX = 2;
          if (gapY < 3) gapY = 3;
        }

        var count = BTN_TEXTS.length;

        // Intentar 3 columnas (desktop) -> si no cumple MIN_BTN_W_PX baja a 2 -> si no a 1
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
          " | Plan(px): " + Math.round(planW) +
          " | cols=" + cols + " rows=" + rows +
          " | btnW=" + w.toFixed(2) + "% (" + Math.round((w/100)*planW) + "px)";
      }

      function update(){
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
        # Si quieres hacerlo variable desde Python: reemplaza "22" por str(FONDO2_BOTTOM)
        .replace("__F2_BOTTOM__", "22")  # % desde abajo del cuadro: sube/baja el texto "Fondo 2"
        .replace("__FOOT_L__", str(FOOTER_LEFT))
        .replace("__FOOT_R__", str(FOOTER_RIGHT))
        .replace("__FOOT_H__", str(FOOTER_H))
        .replace("__FOOT_BOTTOM__", str(FOOTER_BOTTOM))
        .replace("__BTN_TEXTS__", str(BTN_TEXTS).replace("'", '"'))
        .replace("__MIN_BTN_W_PX__", str(MIN_BTN_W_PX))
        .replace("__MOBILE_MAX_W_PX__", str(MOBILE_MAX_W_PX))
)

components.html(html, height=10, scrolling=False)
