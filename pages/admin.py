# pages/admin.py
import os
import json
import urllib.parse
import urllib.request
import streamlit as st
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
AUTH_URL = os.environ.get("AUTH_URL", "https://camilo27.pythonanywhere.com/api/auth")
TIMEOUT_SEC = float(os.environ.get("AUTH_TIMEOUT", "12"))

# =========================
# HELPERS
# =========================
def _safe_get_query_params():
    try:
        qp = st.query_params  # streamlit >=1.30
        return dict(qp)
    except Exception:
        return st.experimental_get_query_params()

def _safe_set_query_params(**kwargs):
    try:
        st.query_params.clear()
        for k, v in kwargs.items():
            if v is None:
                continue
            st.query_params[k] = v
    except Exception:
        st.experimental_set_query_params(**kwargs)

def _call_auth(correo: str, dni: str):
    payload = json.dumps({"correo": correo, "dni": dni}).encode("utf-8")
    req = urllib.request.Request(
        AUTH_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        code = getattr(resp, "status", 200)
    try:
        data = json.loads(body)
    except Exception:
        data = {"ok": False, "raw": body}
    return code, data

# =========================
# PAGE CONFIG (FULLSCREEN)
# =========================
st.set_page_config(page_title="Admin - Login", layout="wide")

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
# LOGOUT (optional query)
# =========================
qp = _safe_get_query_params()
if str(qp.get("logout", ["0"])[0]).strip() == "1":
    st.session_state.pop("auth", None)
    st.session_state.pop("usuario", None)
    st.session_state.pop("rol", None)
    _safe_set_query_params()
    st.rerun()

# =========================
# IF ALREADY AUTH -> GO MAIN
# =========================
if st.session_state.get("auth"):
    st.switch_page("app.py")

# =========================
# LOGIN SUBMIT VIA QUERY PARAMS (FROM HTML)
# =========================
correo_q = (qp.get("correo", [""])[0] if isinstance(qp.get("correo"), list) else qp.get("correo", "")) or ""
dni_q = (qp.get("dni", [""])[0] if isinstance(qp.get("dni"), list) else qp.get("dni", "")) or ""
do_q = (qp.get("do", [""])[0] if isinstance(qp.get("do"), list) else qp.get("do", "")) or ""
err_q = (qp.get("err", [""])[0] if isinstance(qp.get("err"), list) else qp.get("err", "")) or ""

if do_q == "1":
    correo = str(correo_q).strip()
    dni = str(dni_q).strip()

    if not correo or not dni:
        _safe_set_query_params(err="Completa Correo y DNI")
        st.rerun()

    try:
        status, data = _call_auth(correo, dni)
    except Exception as e:
        _safe_set_query_params(err=f"Error de conexión ({type(e).__name__})")
        st.rerun()

    ok = bool(data.get("ok")) if isinstance(data, dict) else False
    if status == 200 and ok:
        st.session_state["auth"] = True
        st.session_state["usuario"] = data.get("usuario", correo)
        st.session_state["rol"] = data.get("rol", data.get("role", ""))
        _safe_set_query_params()  # limpia URL
        st.switch_page("app.py")
    else:
        _safe_set_query_params(err="Credenciales inválidas")
        st.rerun()

# =========================
# HTML (DISEÑO ROJO, RESPONSIVE) + FORM FUNCIONAL
# =========================
# Nota: no toca tus dimensiones del plano principal (eso está en app.py).
# Aquí solo login pantalla completa.
err_html = (
    f"<div class='err'>{urllib.parse.quote(str(err_q)).replace('%20',' ')}</div>"
    if err_q else ""
)

html = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    :root{{
      --bg1:#7b0b0b;
      --bg2:#b51717;
      --glass: rgba(255,255,255,.08);
      --glass2: rgba(255,255,255,.10);
      --border: rgba(255,255,255,.14);
      --txt: #ffffff;
      --muted: rgba(255,255,255,.78);
      --field: rgba(255,255,255,.92);
      --fieldTxt: #2b2b2b;
      --btn1:#ff3a3a;
      --btn2:#c90f0f;
      --shadow: 0 18px 60px rgba(0,0,0,.40);
    }}

    html,body{{height:100%;margin:0;}}
    body{{
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: radial-gradient(1200px 600px at 30% 20%, rgba(255,255,255,.10), rgba(0,0,0,0) 60%),
                  radial-gradient(900px 500px at 70% 75%, rgba(0,0,0,.18), rgba(0,0,0,0) 55%),
                  linear-gradient(135deg, var(--bg2), var(--bg1));
      overflow:hidden;
    }}

    /* Fondo con “corte” diagonal suave como tu referencia */
    .bg-cut{{
      position:fixed; inset:-20%;
      background: linear-gradient(135deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,0) 45%);
      transform: rotate(-8deg);
      pointer-events:none;
    }}

    .wrap{{
      position:fixed; inset:0;
      display:flex;
      align-items:center;
      justify-content:center;
      padding: 22px;
      box-sizing:border-box;
    }}

    .card{{
      width: min(520px, 92vw);
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(0,0,0,.22), rgba(0,0,0,.12));
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      padding: 22px 22px 18px 22px;
      position:relative;
    }}

    .toprow{{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      margin-bottom: 8px;
    }}

    .iconbtn{{
      width: 28px; height: 28px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,.18);
      background: rgba(0,0,0,.18);
      display:flex; align-items:center; justify-content:center;
      color: var(--txt);
      font-weight:700;
      user-select:none;
    }}

    .closebtn{{
      width: 28px; height: 28px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,.18);
      background: rgba(0,0,0,.18);
      display:flex; align-items:center; justify-content:center;
      color: var(--txt);
      cursor:pointer;
    }}

    h1{{
      margin: 8px 0 18px 0;
      text-align:center;
      color: var(--txt);
      font-size: 34px;
      letter-spacing: .2px;
    }}

    label{{
      display:block;
      color: var(--muted);
      font-size: 12px;
      margin: 10px 0 8px 2px;
      font-weight: 600;
    }}

    input{{
      width:100%;
      height: 42px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,.14);
      outline:none;
      background: var(--field);
      color: var(--fieldTxt);
      padding: 0 12px;
      box-sizing:border-box;
      font-size: 13px;
    }}

    input::placeholder{{ color: rgba(0,0,0,.45); }}

    .btn{{
      width:100%;
      height: 44px;
      border-radius: 12px;
      border: 0;
      margin-top: 16px;
      color: #fff;
      font-weight: 800;
      letter-spacing: .2px;
      cursor:pointer;
      background: linear-gradient(180deg, var(--btn1), var(--btn2));
      box-shadow: 0 10px 26px rgba(0,0,0,.35);
    }}

    .rowlinks{{
      display:flex;
      justify-content:space-between;
      margin-top: 10px;
      font-size: 11px;
      color: rgba(255,255,255,.70);
      user-select:none;
    }}

    .rowlinks span{{
      opacity:.85;
    }}

    .err{{
      margin: 10px 0 0 0;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,.18);
      background: rgba(0,0,0,.20);
      color: #fff;
      font-size: 12px;
    }}

    /* Mobile scaling */
    @media (max-width: 420px){{
      .card{{ padding: 18px; border-radius: 16px; }}
      h1{{ font-size: 30px; }}
    }}
  </style>
</head>
<body>
  <div class="bg-cut"></div>
  <div class="wrap">
    <div class="card" role="dialog" aria-label="Login">
      <div class="toprow">
        <div class="iconbtn" title="Home">⌂</div>
        <div class="closebtn" title="Cerrar" onclick="window.location.href='/?logout=1'">×</div>
      </div>

      <h1>Welcome</h1>

      <form id="loginForm" onsubmit="return goLogin();">
        <label for="correo">Correo</label>
        <input id="correo" name="correo" type="email" placeholder="correo@ejemplo.com" autocomplete="username" value="{correo_q.replace('"','&quot;')}"/>

        <label for="dni">DNI</label>
        <input id="dni" name="dni" type="password" placeholder="••••" autocomplete="current-password"/>

        <button class="btn" type="submit">Login to my account</button>
      </form>

      {err_html}

      <div class="rowlinks">
        <span>Forgot password?</span>
        <span>Create account</span>
      </div>
    </div>
  </div>

  <script>
    function goLogin(){{
      var correo = (document.getElementById('correo').value || '').trim();
      var dni = (document.getElementById('dni').value || '').trim();

      var p = new URLSearchParams(window.location.search);
      p.set('correo', correo);
      p.set('dni', dni);
      p.set('do', '1');
      p.delete('err');

      // IMPORTANTE: no navegamos a /admin (eso causa Page not found). Nos quedamos en la misma page de Streamlit.
      window.location.search = p.toString();
      return false;
    }}
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
