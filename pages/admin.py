# app.py
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# PLANO RESPONSIVO — LOGIN (según mockup)
# Ajustas TODO desde esta sección (sin tocar HTML/JS).
#
# UNIDADES:
# - PAD_* y radios/bordes: px
# - Posiciones y tamaños del layout: % del CUADRO (plan)
#
# CUADRO (plan):
# - Es el área interior delimitada por el marco (izq/der/sup).
# - Todo el diseño vive dentro del CUADRO.
# ==============================================================================

# ================== AJUSTES (EDITA SOLO ESTO) ==================

# 1) CUADRO / MARCO (px)
PAD_X_PX = 10          # px: margen externo lateral del CUADRO
PAD_TOP_PX = 10        # px: margen externo superior del CUADRO

# 2) BORDES / FONDO
BORDER_PX = 2          # px: grosor de borde del marco y componentes
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

# 3) CONTENEDOR INTERNO (opcional) — % del CUADRO
#    Útil si quieres que todo el login quede “con margen” dentro del cuadro.
CARD_LEFT = 6          # %: margen interno izquierdo del área login
CARD_RIGHT = 6         # %: margen interno derecho
CARD_TOP = 6           # %: margen interno superior
CARD_BOTTOM = 6        # %: margen interno inferior

# 4) POSICIONES VERTICALES — % del CUADRO (referencia: 0 arriba, 100 abajo)
TITLE_Y = 12           # %: posición vertical del título
USER_LABEL_Y = 22      # %: label "Usuario:"
USER_INPUT_Y = 28      # %: input usuario
PASS_LABEL_Y = 42      # %: label "Contraseña:"
PASS_INPUT_Y = 48      # %: input contraseña
BTN_Y = 67             # %: botón Login
LINKS_Y = 78           # %: links inferiores

# 5) ANCHOS Y ALTOS — % del CUADRO
INPUT_LEFT = 18        # %: margen izquierdo de inputs/labels
INPUT_RIGHT = 18       # %: margen derecho de inputs/labels
INPUT_H = 10           # %: alto de cada input

BTN_LEFT = 32          # %: margen izquierdo del botón (más grande = botón más angosto)
BTN_RIGHT = 32         # %: margen derecho del botón
BTN_H = 9              # %: alto del botón

# 6) LINKS — % del CUADRO (posición horizontal por X)
LINK_LEFT_X = 20       # %: X del texto "Politicas:"
LINK_RIGHT_X = 68      # %: X del texto "Registrarse:"

# 7) RADIOS (px)
INPUT_RADIUS_PX = 10
BTN_RADIUS_PX = 10

# 8) TIPOS (px)
TITLE_SIZE_PX = 18
LABEL_SIZE_PX = 14
LINK_SIZE_PX = 13
BTN_TEXT_SIZE_PX = 14

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

      --r_in: __RIN__px;
      --r_btn: __RBTN__px;
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
      z-index:2;
    }

    /* CUADRO (plan) */
    #plan{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      overflow:hidden;
      background: var(--bg);
      z-index:1;
    }

    /* Área interna (card) */
    #card{
      position:absolute;
      left: __CARD_L__%;
      right: __CARD_R__%;
      top: __CARD_T__%;
      bottom: __CARD_B__%;
    }

    .title{
      position:absolute;
      left:0; right:0;
      top: __TITLE_Y__%;
      text-align:center;
      font: __TITLE_SZ__px Arial, sans-serif;
      font-weight: 800;
      color:#000;
    }

    .label{
      position:absolute;
      left: __IN_L__%;
      right: __IN_R__%;
      font: __LBL_SZ__px Arial, sans-serif;
      font-weight: 700;
      color:#000;
    }

    .field{
      position:absolute;
      left: __IN_L__%;
      right: __IN_R__%;
      height: __IN_H__%;
      border: var(--b) solid #000;
      border-radius: var(--r_in);
      box-sizing:border-box;
      background:#fff;
    }

    .btn{
      position:absolute;
      left: __BTN_L__%;
      right: __BTN_R__%;
      height: __BTN_H__%;
      border: var(--b) solid #000;
      border-radius: var(--r_btn);
      box-sizing:border-box;
      background:#fff;
      display:flex;
      align-items:center;
      justify-content:center;
      font: __BTN_TXT__px Arial, sans-serif;
      font-weight: 700;
      color:#000;
    }

    .link{
      position:absolute;
      font: __LINK_SZ__px Arial, sans-serif;
      font-weight: 700;
      color:#000;
      white-space:nowrap;
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
      z-index:3;
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="plan">
      <div id="card">
        <div class="title">¡BIENVENIDO!</div>

        <div class="label" style="top: __USER_L_Y__%;">Usuario:</div>
        <div class="field" style="top: __USER_I_Y__%;"></div>

        <div class="label" style="top: __PASS_L_Y__%;">Contraseña:</div>
        <div class="field" style="top: __PASS_I_Y__%;"></div>

        <div class="btn" style="top: __BTN_Y__%;">Login</div>

        <div class="link" style="top: __LINKS_Y__%; left: __LINK_L_X__%;">Politicas:</div>
        <div class="link" style="top: __LINKS_Y__%; left: __LINK_R_X__%;">Registrarse:</div>
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

      var hud = document.getElementById("hud");
      var plan = document.getElementById("plan");
      function update(){
        var r = plan.getBoundingClientRect();
        hud.textContent =
          "Viewport(px): " + Math.round(window.innerWidth) + " x " + Math.round(window.innerHeight) +
          " | Plan(px): " + Math.round(r.width) + " x " + Math.round(r.height);
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
        .replace("__RIN__", str(INPUT_RADIUS_PX))
        .replace("__RBTN__", str(BTN_RADIUS_PX))
        .replace("__CARD_L__", str(CARD_LEFT))
        .replace("__CARD_R__", str(CARD_RIGHT))
        .replace("__CARD_T__", str(CARD_TOP))
        .replace("__CARD_B__", str(CARD_BOTTOM))
        .replace("__TITLE_Y__", str(TITLE_Y))
        .replace("__USER_L_Y__", str(USER_LABEL_Y))
        .replace("__USER_I_Y__", str(USER_INPUT_Y))
        .replace("__PASS_L_Y__", str(PASS_LABEL_Y))
        .replace("__PASS_I_Y__", str(PASS_INPUT_Y))
        .replace("__BTN_Y__", str(BTN_Y))
        .replace("__LINKS_Y__", str(LINKS_Y))
        .replace("__IN_L__", str(INPUT_LEFT))
        .replace("__IN_R__", str(INPUT_RIGHT))
        .replace("__IN_H__", str(INPUT_H))
        .replace("__BTN_L__", str(BTN_LEFT))
        .replace("__BTN_R__", str(BTN_RIGHT))
        .replace("__BTN_H__", str(BTN_H))
        .replace("__LINK_L_X__", str(LINK_LEFT_X))
        .replace("__LINK_R_X__", str(LINK_RIGHT_X))
        .replace("__TITLE_SZ__", str(TITLE_SIZE_PX))
        .replace("__LBL_SZ__", str(LABEL_SIZE_PX))
        .replace("__LINK_SZ__", str(LINK_SIZE_PX))
        .replace("__BTN_TXT__", str(BTN_TEXT_SIZE_PX))
)

components.html(html, height=10, scrolling=False)
