# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components
import requests

# =========================
# CONFIG / API
# =========================
API_URL = "https://camilo27.pythonanywhere.com/api/auth"

# Estado de sesión
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# =========================
# ESTILO FULLSCREEN (no sidebar/header)
# =========================
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
      [data-testid="stSidebar"]{display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# LOGIN (admin.py = PRIMERA VISTA)
# =========================
def _auth_api(correo: str, dni: str):
    r = requests.post(API_URL, data={"correo": correo, "dni": dni}, timeout=15)
    return r.status_code, r.json()

# Flags UI
if "login_error" not in st.session_state:
    st.session_state.login_error = ""

# Si ya está logueado, manda directo a app.py
if st.session_state.auth:
    st.switch_page("app.py")

# =========================
# UI HTML (diseño rojo estilo mockup)
# =========================
html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    html, body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;font-family:Arial, sans-serif;}
    #stage{
      position:fixed;inset:0;width:100vw;height:100vh;
      background:
        linear-gradient(135deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.00) 42%),
        linear-gradient(180deg, #b21a1a 0%, #7a0f0f 40%, #1b0a0a 100%);
      display:flex;align-items:center;justify-content:center;
    }
    #card{
      width:min(420px, 92vw);
      border-radius:22px;
      padding:26px 22px 18px 22px;
      box-sizing:border-box;
      background: rgba(0,0,0,0.08);
      border: 1px solid rgba(255,255,255,0.16);
      box-shadow: 0 18px 50px rgba(0,0,0,0.35);
      position:relative;
    }
    #icon{
      width:54px;height:54px;border-radius:16px;
      background: rgba(255,255,255,0.14);
      border: 1px solid rgba(255,255,255,0.20);
      display:flex;align-items:center;justify-content:center;
      color:#fff;font-weight:900;
      margin: 2px auto 10px auto;
      font-size:22px;
    }
    #title{
      text-align:center;
      color:#fff;
      font-weight:900;
      font-size:34px;
      letter-spacing:0.2px;
      margin: 6px 0 18px 0;
      text-shadow: 0 1px 10px rgba(0,0,0,0.18);
    }
    .lbl{
      color: rgba(255,255,255,0.92);
      font-size:13px;
      font-weight:700;
      margin: 0 0 6px 4px;
    }
    .in{
      width:100%;
      height:46px;
      border-radius:14px;
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.92);
      padding: 0 14px;
      box-sizing:border-box;
      font-size:14px;
      font-weight:700;
      color: rgba(0,0,0,0.74);
      outline:none;
    }
    .row{margin-bottom:14px;}
    #btn{
      width:100%;
      height:44px;
      border-radius:18px;
      border: 1px solid rgba(255,255,255,0.20);
      background: linear-gradient(180deg, #ff4a4a 0%, #d61f1f 100%);
      color:#fff;
      font-weight:900;
      letter-spacing:0.2px;
      cursor:pointer;
      box-shadow: 0 10px 22px rgba(0,0,0,0.22);
      margin-top: 6px;
    }
    #btn:active{transform:translateY(1px);}
    #err{
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: 14px;
      background: rgba(255,255,255,0.92);
      border: 1px solid rgba(255,0,0,0.20);
      color: #b10000;
      font-weight:800;
      display: __ERR_DISP__;
    }
    #links{
      margin-top: 14px;
      display:flex;
      justify-content:space-between;
      color: rgba(255,255,255,0.82);
      font-weight:700;
      font-size:12.5px;
    }
    #links span{opacity:0.9;}
    #x{
      position:absolute; right:14px; top:12px;
      width:34px;height:34px;border-radius:12px;
      border:1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.08);
      color:#fff;
      display:flex;align-items:center;justify-content:center;
      font-weight:900;
      user-select:none;
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="card">
      <div id="x">×</div>
      <div id="icon">⌂</div>
      <div id="title">Welcome</div>

      <form method="GET">
        <div class="row">
          <div class="lbl">Correo</div>
          <input class="in" name="correo" value="__CORREO__" autocomplete="username" />
        </div>

        <div class="row">
          <div class="lbl">DNI</div>
          <input class="in" name="dni" value="__DNI__" type="password" autocomplete="current-password" />
        </div>

        <button id="btn" type="submit">Login to my account</button>
      </form>

      <div id="err">__ERR_TXT__</div>

      <div id="links">
        <span>Forgot password?</span>
        <span>Create account</span>
      </div>
    </div>
  </div>

  <script>
    // Fullscreen real del iframe (Streamlit Cloud)
    var fe = window.frameElement;
    if (fe){
      fe.style.position="fixed";
      fe.style.inset="0";
      fe.style.width="100vw";
      fe.style.height="100vh";
      fe.style.border="0";
      fe.style.margin="0";
      fe.style.padding="0";
      fe.style.zIndex="999999";
      fe.style.background="transparent";
    }
  </script>
</body>
</html>
"""

# =========================
# CAPTURA DE INPUTS (GET) SIN query_params EXPERIMENTAL
# =========================
correo_val = st.query_params.get("correo", "")
dni_val = st.query_params.get("dni", "")

# Si el form envió datos, autenticar
if correo_val and dni_val:
    try:
        status, data = _auth_api(correo_val, dni_val)
        if status == 200 and data.get("ok") is True:
            st.session_state.auth = True
            st.session_state.user = data.get("usuario", correo_val) or correo_val
            st.session_state.role = data.get("rol", "") or ""
            st.session_state.login_error = ""
            st.switch_page("app.py")
        else:
            st.session_state.login_error = data.get("error", "Credenciales inválidas")
    except Exception:
        st.session_state.login_error = "Error conectando con el servidor"

# Render HTML con valores + error
err_txt = st.session_state.login_error or ""
html = (
    html.replace("__CORREO__", str(correo_val).replace('"', "&quot;"))
        .replace("__DNI__", str(dni_val).replace('"', "&quot;"))
        .replace("__ERR_TXT__", err_txt.replace("<", "").replace(">", ""))
        .replace("__ERR_DISP__", "block" if err_txt else "none")
)

components.html(html, height=10, scrolling=False)
