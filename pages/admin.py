# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components

# =======================
# HANDSHAKE (JS -> URL PARAMS -> SESSION)
# =======================
try:
    qp = st.query_params
except Exception:
    qp = {}

if (qp.get("auth") == "1") or (qp.get("ok") == "1"):
    usuario = qp.get("usuario", "") or qp.get("user", "") or ""
    rol = qp.get("rol", "") or qp.get("role", "") or ""

    st.session_state["auth"] = True
    st.session_state["usuario"] = usuario
    st.session_state["rol"] = rol
    st.session_state["user"] = usuario
    st.session_state["role"] = rol

    try:
        st.query_params.clear()
    except Exception:
        pass

    st.switch_page("app.py")

# ==============================================================================
# PLANO RESPONSIVO — LOGIN (MISMAS DIMENSIONES / RESPONSIVE) + NUEVO DISEÑO ROJO
# ==============================================================================

# ================== AJUSTES (NO CAMBIAR RESPONSIVE / DIMENSIONES) ==================

# 1) CUADRO / MARCO (px)
PAD_X_PX = 10          # px
PAD_TOP_PX = 10        # px

# 2) BORDES / FONDO
BORDER_PX = 2
BORDER_COLOR = "rgba(255,255,255,0.18)"   # (solo color; dimensiones igual)
BG_COLOR = "#2a0000"                      # (solo color; dimensiones igual)

# 3) CONTENEDOR INTERNO — % del CUADRO
CARD_LEFT = 6
CARD_RIGHT = 6
CARD_TOP = 6
CARD_BOTTOM = 6

# 4) POSICIONES VERTICALES — % del CUADRO
TITLE_Y = 14
USER_LABEL_Y = 32
USER_INPUT_Y = 38
PASS_LABEL_Y = 52
PASS_INPUT_Y = 58
BTN_Y = 72
LINKS_Y = 84

# 5) ANCHOS Y ALTOS — % del CUADRO
INPUT_LEFT = 18
INPUT_RIGHT = 18
INPUT_H = 10

BTN_LEFT = 18
BTN_RIGHT = 18
BTN_H = 9

# 6) LINKS — % del CUADRO
LINK_LEFT_X = 18
LINK_RIGHT_X = 70

# 7) RADIOS (px)
INPUT_RADIUS_PX = 12
BTN_RADIUS_PX = 999

# 8) TIPOS (px)
TITLE_SIZE_PX = 26
LABEL_SIZE_PX = 12
LINK_SIZE_PX = 11
BTN_TEXT_SIZE_PX = 13

# 9) API
AUTH_API_URL = "https://camilo27.pythonanywhere.com/api/auth"

# ===============================================================

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}

      /* Ocultar sidebar/nav de multipage */
      [data-testid="stSidebar"]{display:none !important;}
      [data-testid="collapsedControl"]{display:none !important;}
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
    #stage{position:fixed;inset:0;width:100vw;height:100vh;background:
      radial-gradient(900px 600px at 70% 35%, rgba(255,60,60,0.22), transparent 60%),
      radial-gradient(900px 600px at 25% 70%, rgba(255,0,0,0.20), transparent 62%),
      linear-gradient(135deg, #6a0000 0%, #2a0000 55%, #110000 100%);
    }

    /* Marco (mismas dimensiones) */
    #frame{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      border-left:var(--b) solid rgba(255,255,255,0.08);
      border-right:var(--b) solid rgba(255,255,255,0.08);
      border-top:var(--b) solid rgba(255,255,255,0.08);
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
      z-index:1;
    }

    /* Card (mismas dimensiones) */
    #card{
      position:absolute;
      left: __CARD_L__%;
      right: __CARD_R__%;
      top: __CARD_T__%;
      bottom: __CARD_B__%;

      display:flex;
      align-items:center;
      justify-content:center;
    }

    /* Modal */
    #modal{
      position:relative;
      width:min(420px, 92vw);
      padding: 18px 18px 14px;
      border-radius: 16px;
      background: rgba(0,0,0,0.18);
      border: 1px solid rgba(255,255,255,0.14);
      box-shadow: 0 18px 50px rgba(0,0,0,0.45);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }

    #close{
      position:absolute;
      right: 10px;
      top: 10px;
      width: 28px;
      height: 28px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.10);
      color: rgba(255,255,255,0.9);
      font: 700 14px Arial, sans-serif;
      display:flex;
      align-items:center;
      justify-content:center;
      cursor:pointer;
      user-select:none;
    }

    #icon{
      width: 38px;
      height: 38px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.12);
      display:flex;
      align-items:center;
      justify-content:center;
      margin: 0 auto 10px;
    }
    #icon svg{width:18px;height:18px;fill: rgba(255,255,255,0.9);}

    #title{
      text-align:center;
      color:#fff;
      font: 800 __TITLE_SZ__px Arial, sans-serif;
      margin: 0 0 14px;
      letter-spacing: 0.2px;
    }

    .lbl{
      color: rgba(255,255,255,0.9);
      font: 700 __LBL_SZ__px Arial, sans-serif;
      margin: 10px 0 6px;
    }

    .inp-wrap{position:relative;}
    .inp{
      width: 100%;
      height: 42px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.14);
      background: rgba(255,255,255,0.95);
      outline: none;
      padding: 0 12px;
      font: 700 13px Arial, sans-serif;
      color:#111;
      box-sizing:border-box;
    }

    #eye{
      position:absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 28px;
      height: 28px;
      border-radius: 10px;
      border: 1px solid rgba(0,0,0,0.10);
      background: rgba(255,255,255,0.85);
      display:flex;
      align-items:center;
      justify-content:center;
      cursor:pointer;
      user-select:none;
    }
    #eye svg{width:16px;height:16px;fill:#333;}

    #btn{
      width: 100%;
      height: 42px;
      margin-top: 14px;
      border: none;
      border-radius: var(--r_btn);
      background: linear-gradient(180deg, #ff4b4b 0%, #d60000 100%);
      color:#fff;
      font: 800 __BTN_TXT__px Arial, sans-serif;
      cursor:pointer;
      box-shadow: 0 10px 22px rgba(255,0,0,0.25);
    }
    #btn:active{transform: translateY(1px);}

    #row-links{
      display:flex;
      justify-content:space-between;
      margin-top: 10px;
      color: rgba(255,255,255,0.75);
      font: 700 __LINK_SZ__px Arial, sans-serif;
    }

    #err{
      display:none;
      margin-top: 10px;
      padding: 10px 12px;
      border-radius: 10px;
      background: rgba(255,255,255,0.10);
      border: 1px solid rgba(255,255,255,0.12);
      color: #ffd1d1;
      font: 700 12px Arial, sans-serif;
    }

    /* HUD */
    #hud{
      position:absolute; top:8px; left:8px;
      font: 12px Arial, sans-serif;
      background: rgba(255,255,255,0.92);
      border: 1px solid rgba(0,0,0,0.20);
      border-radius: 6px;
      padding: 6px 10px;
      white-space: nowrap;
      pointer-events:none;
      z-index:3;
      display:none;
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="plan">
      <div id="card">
        <div id="modal">
          <div id="close" title="Cerrar">×</div>

          <div id="icon" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M12 3l9 7v11a1 1 0 0 1-1 1h-6v-7H10v7H4a1 1 0 0 1-1-1V10l9-7z"/></svg>
          </div>

          <div id="title">Welcome</div>

          <div class="lbl">Correo</div>
          <input id="correo" class="inp" type="email" autocomplete="username" />

          <div class="lbl">DNI</div>
          <div class="inp-wrap">
            <input id="dni" class="inp" type="password" autocomplete="current-password" />
            <div id="eye" title="Ver/ocultar">
              <svg viewBox="0 0 24 24"><path d="M12 5c5 0 9 7 9 7s-4 7-9 7-9-7-9-7 4-7 9-7zm0 3.5A3.5 3.5 0 1 0 12 19a3.5 3.5 0 0 0 0-7z"/></svg>
            </div>
          </div>

          <button id="btn" type="button">Login to my account</button>

          <div id="row-links">
            <div>Forgot password?</div>
            <div>Create account</div>
          </div>

          <div id="err">Error conectando con el servidor</div>
        </div>
      </div>

      <div id="hud">Cargando.</div>
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

      var apiUrl = "__API__";
      var correo = document.getElementById("correo");
      var dni = document.getElementById("dni");
      var btn = document.getElementById("btn");
      var err = document.getElementById("err");
      var eye = document.getElementById("eye");
      var close = document.getElementById("close");

      function showErr(msg){
        err.style.display = "block";
        err.textContent = msg || "Error conectando con el servidor";
      }
      function hideErr(){
        err.style.display = "none";
        err.textContent = "";
      }

      eye.addEventListener("click", function(){
        dni.type = (dni.type === "password") ? "text" : "password";
      });

      close.addEventListener("click", function(){
        // No hace nada: evitar volver al login gris
        hideErr();
      });

      async function doLogin(){
        hideErr();

        var c = (correo.value || "").trim();
        var d = (dni.value || "").trim();

        if (!c || !d){
          showErr("Completa Correo y DNI");
          return;
        }

        btn.disabled = true;
        btn.textContent = "Validando...";

        try{
          var r = await fetch(apiUrl, {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({correo: c, dni: d})
          });

          var data = null;
          try{ data = await r.json(); }catch(e){}

          if (!r.ok || !data){
            showErr("Error conectando con el servidor");
            return;
          }

          if (!data.ok){
            showErr(data.error || "Credenciales inválidas");
            return;
          }

          var usuario = encodeURIComponent(data.usuario || c);
          var rol = encodeURIComponent(data.rol || data.role || "");
          var target = window.location.origin + "/?auth=1&usuario=" + usuario + "&rol=" + rol;
          window.location.href = target;
        }catch(e){
          showErr("Error conectando con el servidor");
        }finally{
          btn.disabled = false;
          btn.textContent = "Login to my account";
        }
      }

      btn.addEventListener("click", doLogin);

      dni.addEventListener("keydown", function(ev){
        if (ev.key === "Enter") doLogin();
      });
      correo.addEventListener("keydown", function(ev){
        if (ev.key === "Enter") doLogin();
      });
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
        .replace("__TITLE_SZ__", str(TITLE_SIZE_PX))
        .replace("__LBL_SZ__", str(LABEL_SIZE_PX))
        .replace("__LINK_SZ__", str(LINK_SIZE_PX))
        .replace("__BTN_TXT__", str(BTN_TEXT_SIZE_PX))
        .replace("__API__", AUTH_API_URL)
)

components.html(html, height=10, scrolling=False)
