# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components
import requests

# ==============================================================================
# PLANO RESPONSIVO — LOGIN (según mockup)
# Ajustas TODO desde esta sección (sin tocar HTML/JS).
# ==============================================================================

PAD_X_PX = 10
PAD_TOP_PX = 10

BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

CARD_LEFT = 6
CARD_RIGHT = 6
CARD_TOP = 6
CARD_BOTTOM = 6

TITLE_Y = 12
USER_LABEL_Y = 22
USER_INPUT_Y = 28
PASS_LABEL_Y = 42
PASS_INPUT_Y = 48
BTN_Y = 67
LINKS_Y = 78

INPUT_LEFT = 18
INPUT_RIGHT = 18
INPUT_H = 10

BTN_LEFT = 32
BTN_RIGHT = 32
BTN_H = 9

LINK_LEFT_X = 20
LINK_RIGHT_X = 68

INPUT_RADIUS_PX = 10
BTN_RADIUS_PX = 10

TITLE_SIZE_PX = 18
LABEL_SIZE_PX = 14
LINK_SIZE_PX = 13
BTN_TEXT_SIZE_PX = 14

AUTH_URL = "https://camilo27.pythonanywhere.com/api/auth"

st.set_page_config(layout="wide")

# Oculta chrome de Streamlit (sidebar incl.)
st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
      [data-testid="stSidebar"], [data-testid="collapsedControl"]{display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================
# UI REAL (CAPTURA + BOTÓN)
# ==========================
# Se renderiza ARRIBA del HTML con z-index alto, pero visualmente queda alineado con el mockup.
st.markdown(
    """
    <style>
      /* Contenedor flotante para inputs reales (encima del mockup) */
      .auth-overlay{
        position:fixed;
        left:0; top:0;
        width:100vw; height:100vh;
        pointer-events:none;
        z-index:1000000;
      }
      .auth-overlay .inner{
        position:absolute;
        left:10px; right:10px;
        top:10px; bottom:0;
      }
      /* Hacemos que los widgets sí reciban click */
      .auth-overlay *{ pointer-events:auto; }

      /* Quita márgenes internos de widgets */
      .auth-overlay [data-testid="stTextInput"]{ margin:0 !important; padding:0 !important; }
      .auth-overlay [data-testid="stTextInput"] label{ display:none !important; }
      .auth-overlay [data-testid="stTextInput"] input{
        border:2px solid #000 !important;
        border-radius:10px !important;
        height:54px !important;
        font-weight:700 !important;
      }
      .auth-overlay [data-testid="stButton"] button{
        border:2px solid #000 !important;
        border-radius:10px !important;
        background:#fff !important;
        height:48px !important;
        font-weight:700 !important;
        width:100% !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Overlay: colocación aproximada sobre el mockup (misma lógica porcentual del CUADRO)
# Para no romper tu diseño, mantenemos el mockup como fondo y ponemos inputs reales encima.
overlay = st.container()
with overlay:
    st.markdown('<div class="auth-overlay"><div class="inner">', unsafe_allow_html=True)

    # Spacers para bajar hasta donde están los campos del mockup
    # (No tocamos el mockup; solo superponemos inputs)
    top_pad = int((PAD_TOP_PX + 60))
    st.markdown(f"<div style='height:{top_pad}px'></div>", unsafe_allow_html=True)

    # Inputs reales
    usuario = st.text_input("", key="auth_user")
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    password = st.text_input("", type="password", key="auth_pass")

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # Botón real
    login_clicked = st.button("Login", key="auth_btn")

    st.markdown("</div></div>", unsafe_allow_html=True)

# Acción server-side
if login_clicked:
    try:
        r = requests.post(
            AUTH_URL,
            json={"usuario": usuario, "password": password},
            timeout=20,
        )
        data = r.json() if r.headers.get("content-type", "").lower().startswith("application/json") else {}
        if data.get("ok") is True:
            st.session_state["auth_ok"] = True
            try:
                st.switch_page("app.py")
            except Exception:
                st.experimental_set_query_params(auth="ok")
                st.markdown(
                    "<script>window.location.href='/?auth=ok';</script>",
                    unsafe_allow_html=True,
                )
            st.stop()
        else:
            st.error("Credenciales inválidas")
    except Exception:
        st.error("Error de conexión")

# ==========================
# MOCKUP ORIGINAL (FONDO)
# ==========================
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

    #plan{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      overflow:hidden;
      background: var(--bg);
      z-index:1;
    }

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
