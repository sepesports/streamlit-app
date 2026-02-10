# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components

# ================== PROTECCIÓN (NO ENTRA SIN LOGIN) ==================
if not st.session_state.get("auth"):
    st.switch_page("app.py")

# ================== DATOS DE USUARIO (GARANTIZADO) ==================
USER_EMAIL = st.session_state.get("user", "") or st.session_state.get("usuario", "") or ""
USER_ROLE = st.session_state.get("role", "") or st.session_state.get("rol", "") or ""

# ================== UI STREAMLIT (SIN CAMBIAR RESPONSIVE DEL HTML) ==================
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

# Botón real de cerrar sesión (sin tocar el HTML/JS responsive)
logout_col = st.columns([1, 6, 1])[2]
with logout_col:
    if st.button("Cerrar sesión"):
        st.session_state.auth = False
        st.session_state.user = ""
        st.session_state.role = ""
        st.switch_page("app.py")

# ==============================================================================
# PLANO RESPONSIVO — ADMIN (MISMA ESTRUCTURA / MISMAS DIMENSIONES)
# NO MODIFICAR LA SECCIÓN DE DIMENSIONES / RESPONSIVE.
# SOLO SE AJUSTAN COLORES/ESTILO PARA PARECERSE A LA IMAGEN.
# ==============================================================================

# ================== AJUSTES (EDITA SOLO ESTO) ==================

# 1) CUADRO / MARCO (px)
PAD_X_PX = 10          # px: margen externo lateral del CUADRO
PAD_TOP_PX = 10        # px: margen externo superior del CUADRO

# 2) BORDES / FONDO
BORDER_PX = 2          # px: grosor de borde del marco y componentes
BORDER_COLOR = "rgba(255,255,255,0.14)"

# Fondo general (se mantiene, pero el gradiente lo da el CSS)
BG_COLOR = "#0b0b0b"

# 3) CONTENEDOR INTERNO (opcional) — % del CUADRO
CARD_LEFT = 6          # %: margen interno izquierdo del área
CARD_RIGHT = 6         # %: margen interno derecho
CARD_TOP = 6           # %: margen interno superior
CARD_BOTTOM = 6        # %: margen interno inferior

# 4) POSICIONES VERTICALES — % del CUADRO
TITLE_Y = 12           # %: posición vertical del título
USER_LABEL_Y = 22      # %: label "Correo"
USER_INPUT_Y = 28      # %: campo correo
PASS_LABEL_Y = 42      # %: label "Rol"
PASS_INPUT_Y = 48      # %: campo rol
BTN_Y = 67             # %: botón
LINKS_Y = 78           # %: links inferiores

# 5) ANCHOS Y ALTOS — % del CUADRO
INPUT_LEFT = 18        # %: margen izquierdo de inputs/labels
INPUT_RIGHT = 18       # %: margen derecho
INPUT_H = 10           # %: alto de cada input

BTN_LEFT = 18          # %: margen izquierdo del botón
BTN_RIGHT = 18         # %: margen derecho del botón
BTN_H = 9              # %: alto del botón

# 6) LINKS — % del CUADRO (posición horizontal por X)
LINK_LEFT_X = 20       # %: link izq
LINK_RIGHT_X = 62      # %: link der

# 7) RADIOS (px)
INPUT_RADIUS_PX = 14
BTN_RADIUS_PX = 18

# 8) TIPOS (px)
TITLE_SIZE_PX = 26
LABEL_SIZE_PX = 14
LINK_SIZE_PX = 13
BTN_TEXT_SIZE_PX = 14

# ===============================================================

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

    html, body{
      margin:0;padding:0;width:100%;height:100%;
      overflow:hidden;background:var(--bg);
      font-family: Arial, sans-serif;
    }

    /* Fondo tipo mockup (rojo con diagonal) */
    #stage{
      position:fixed;inset:0;width:100vw;height:100vh;
      background:
        linear-gradient(135deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.00) 42%),
        linear-gradient(180deg, #b21a1a 0%, #7a0f0f 40%, #1b0a0a 100%);
    }

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
      background: transparent;
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

    /* Icono superior (cuadrito) */
    #icon{
      position:absolute;
      left:50%;
      transform:translateX(-50%);
      top: 3%;
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: rgba(255,255,255,0.12);
      border: 1px solid rgba(255,255,255,0.18);
      display:flex;
      align-items:center;
      justify-content:center;
      color:#fff;
      font-weight:800;
      letter-spacing:0.5px;
    }

    .title{
      position:absolute;
      left:0; right:0;
      top: __TITLE_Y__%;
      text-align:center;
      font-size: __TITLE_SZ__px;
      font-weight: 900;
      color:#ffffff;
      letter-spacing: 0.5px;
      text-shadow: 0 1px 10px rgba(0,0,0,0.20);
    }

    .label{
      position:absolute;
      left: __IN_L__%;
      right: __IN_R__%;
      font-size: __LBL_SZ__px;
      font-weight: 700;
      color: rgba(255,255,255,0.92);
    }

    .field{
      position:absolute;
      left: __IN_L__%;
      right: __IN_R__%;
      height: __IN_H__%;
      border: 1px solid rgba(255,255,255,0.18);
      border-radius: var(--r_in);
      box-sizing:border-box;
      background: rgba(255,255,255,0.92);
      display:flex;
      align-items:center;
      padding: 0 14px;
      font-size: 14px;
      font-weight: 700;
      color: rgba(0,0,0,0.72);
      overflow:hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    .btn{
      position:absolute;
      left: __BTN_L__%;
      right: __BTN_R__%;
      height: __BTN_H__%;
      border: 1px solid rgba(255,255,255,0.20);
      border-radius: var(--r_btn);
      box-sizing:border-box;
      background: linear-gradient(180deg, #ff4a4a 0%, #d61f1f 100%);
      display:flex;
      align-items:center;
      justify-content:center;
      font-size: __BTN_TXT__px;
      font-weight: 900;
      color:#fff;
      letter-spacing: 0.2px;
      box-shadow: 0 10px 22px rgba(0,0,0,0.22);
      user-select:none;
    }

    .link{
      position:absolute;
      font-size: __LINK_SZ__px;
      font-weight: 700;
      color: rgba(255,255,255,0.85);
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
        <div id="icon">🏠</div>
        <div class="title">Welcome</div>

        <div class="label" style="top: __USER_L_Y__%;">Correo</div>
        <div class="field" style="top: __USER_I_Y__%;">__USER_EMAIL__</div>

        <div class="label" style="top: __PASS_L_Y__%;">Rol</div>
        <div class="field" style="top: __PASS_I_Y__%;">__USER_ROLE__</div>

        <div class="btn" style="top: __BTN_Y__%;">Acceso concedido</div>

        <div class="link" style="top: __LINKS_Y__%; left: __LINK_L_X__%;">Soporte</div>
        <div class="link" style="top: __LINKS_Y__%; left: __LINK_R_X__%;">Panel</div>
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
        .replace("__USER_EMAIL__", (USER_EMAIL or "-").replace("<", "").replace(">", ""))
        .replace("__USER_ROLE__", (USER_ROLE or "-").replace("<", "").replace(">", ""))
)

components.html(html, height=10, scrolling=False)
