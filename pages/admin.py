# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# LOGIN (RESPONSIVE) — NO CAMBIAR DIMENSIONES DEL PLANO
# Ajusta SOLO colores/textos desde la sección "AJUSTES".
# ==============================================================================

# ================== AJUSTES (SOLO COLORES/TEXTOS) ==================

# Fondo (rojo tipo mockup)
BG_GRAD_A = "#8c1010"
BG_GRAD_B = "#220404"
BG_HILIGHT = "rgba(255,255,255,0.10)"

# Card (glass)
CARD_BG = "rgba(0,0,0,0.22)"
CARD_BORDER = "rgba(255,255,255,0.18)"
TXT_WHITE = "#ffffff"
TXT_MUTED = "rgba(255,255,255,0.78)"
FIELD_BG = "rgba(255,255,255,0.92)"
FIELD_TXT = "#111111"

# Botón
BTN_GRAD_A = "#ff3a3a"
BTN_GRAD_B = "#b50b0b"
BTN_TXT_COLOR = "#ffffff"

# Error
ERROR_BG = "rgba(255,60,60,0.18)"
ERROR_TXT = "#ffd7d7"

# Textos
TITLE_TEXT = "Welcome"
BTN_TEXT = "Login to my account"
LABEL_CORREO = "Correo"
LABEL_DNI = "DNI"
LINK_LEFT = "Forgot password?"
LINK_RIGHT = "Create account"

# API
AUTH_URL = "https://camilo27.pythonanywhere.com/api/auth"

# ================== STREAMLIT BASE ==================
st.set_page_config(layout="wide")

# Ocultar UI de Streamlit (para que no aparezca el login gris)
st.markdown(
    """
    <style>
      header, footer {display:none !important;}
      [data-testid="stSidebar"], [data-testid="stSidebarNav"] {display:none !important;}
      .block-container{padding:0 !important; margin:0 !important; max-width:100% !important;}
      section.main > div{padding:0 !important; margin:0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# PLANO (DIMENSIONES) — PEGADO DEL ARCHIVO "Administrador" (NO MODIFICAR)
# ==============================================================================
PAD_X_PX = 10
PAD_TOP_PX = 10
BORDER_PX = 2
BORDER_COLOR = "#111111"

CARD_W = 38
CARD_H = 62
CARD_X = 62
CARD_Y = 55

TITLE_Y = 16
USER_LABEL_Y = 30
USER_INPUT_Y = 36
PASS_LABEL_Y = 50
PASS_INPUT_Y = 56
BTN_Y = 70
LINKS_Y = 82

TITLE_SZ = 34
LABEL_SZ = 12
INPUT_TXT = 14
BTN_TXT = 14
LINK_SZ = 10

INPUT_H_PX = 44
INPUT_RADIUS_PX = 12
BTN_H_PX = 44
BTN_RADIUS_PX = 16

HTML = r"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  html,body{height:100%; margin:0; font-family: Arial, sans-serif; background:transparent;}
  body{overflow:hidden;}

  #stage{
    position:fixed; inset:0;
    background:
      linear-gradient(135deg, __BG_HILIGHT__ 0%, rgba(255,255,255,0) 40%),
      radial-gradient(1200px 700px at 70% 30%, rgba(255,120,120,0.22), rgba(0,0,0,0) 60%),
      linear-gradient(180deg, __BG_A__, __BG_B__);
  }

  #frame{
    position:absolute;
    left: __PADX__px; right: __PADX__px; top: __PADTOP__px; bottom: __PADTOP__px;
    border: __B__px solid __BC__;
    box-sizing:border-box;
    pointer-events:none;
    opacity:0; /* no mostrar */
  }

  #plan{
    position:absolute;
    left: __PADX__px; right: __PADX__px; top: __PADTOP__px; bottom: __PADTOP__px;
  }

  #card{
    position:absolute;
    width: __CARD_W__%;
    height: __CARD_H__%;
    left: calc(__CARD_X__% - (__CARD_W__/2)*1%);
    top:  calc(__CARD_Y__% - (__CARD_H__/2)*1%);
    background: __CARD_BG__;
    border: 1px solid __CARD_BORDER__;
    border-radius: 18px;
    box-shadow: 0 18px 50px rgba(0,0,0,.35);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    overflow:hidden;
  }

  #miniIcon{
    position:absolute; top:14px; left:16px;
    width:34px; height:34px;
    border-radius: 10px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.18);
    display:flex; align-items:center; justify-content:center;
    color: __TXT_WHITE__;
    font-weight:700;
    user-select:none;
  }
  #closeBtn{
    position:absolute; top:14px; right:14px;
    width:28px; height:28px;
    border-radius: 8px;
    background: rgba(0,0,0,0.20);
    border: 1px solid rgba(255,255,255,0.14);
    color: __TXT_WHITE__;
    display:flex; align-items:center; justify-content:center;
    cursor:pointer;
    user-select:none;
  }

  .title{
    position:absolute;
    left: 0; right:0;
    top: __TITLE_Y__%;
    transform: translateY(-50%);
    text-align:center;
    font-size: __TITLE_SZ__px;
    font-weight: 800;
    color: __TXT_WHITE__;
    letter-spacing: .2px;
  }

  .label{
    position:absolute;
    left: 12%;
    right: 12%;
    font-size: __LABEL_SZ__px;
    font-weight: 700;
    color: __TXT_MUTED__;
    user-select:none;
  }

  .inputWrap{
    position:absolute;
    left: 12%;
    right: 12%;
    height: __INPUT_H__px;
  }
  .input{
    width:100%;
    height:100%;
    border-radius: __INPUT_RAD__px;
    border: 0;
    outline: none;
    padding: 0 14px;
    background: __FIELD_BG__;
    color: __FIELD_TXT__;
    font-size: __INPUT_TXT__px;
    box-sizing:border-box;
  }
  .input::placeholder{color: rgba(0,0,0,0.38);}

  .btn{
    position:absolute;
    left: 12%;
    right: 12%;
    height: __BTN_H__px;
    border-radius: __BTN_RAD__px;
    background: linear-gradient(180deg, __BTN_A__, __BTN_B__);
    color: __BTN_TXT__;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size: __BTN_TXT_SZ__px;
    font-weight: 800;
    cursor:pointer;
    user-select:none;
    box-shadow: 0 10px 26px rgba(0,0,0,.30);
  }
  .btn:active{transform: translateY(1px);}

  .rowLinks{
    position:absolute;
    left: 12%;
    right: 12%;
    display:flex;
    justify-content:space-between;
    font-size: __LINK_SZ__px;
    font-weight: 700;
    color: __TXT_MUTED__;
    user-select:none;
  }

  #err{
    position:absolute;
    left: 12%;
    right: 12%;
    top: calc(__BTN_Y__% + 10%);
    padding: 10px 12px;
    border-radius: 12px;
    background: __ERR_BG__;
    color: __ERR_TXT__;
    font-size: 12px;
    font-weight: 700;
    display:none;
    box-sizing:border-box;
  }
</style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>
    <div id="plan">
      <div id="card">
        <div id="miniIcon">⌂</div>
        <div id="closeBtn">×</div>

        <div class="title">__TITLE_TEXT__</div>

        <div class="label" style="top: __USER_L_Y__%;">__LABEL_CORREO__</div>
        <div class="inputWrap" style="top: __USER_I_Y__%;">
          <input id="correo" class="input" type="email" autocomplete="username" placeholder="correo@ejemplo.com"/>
        </div>

        <div class="label" style="top: __PASS_L_Y__%;">__LABEL_DNI__</div>
        <div class="inputWrap" style="top: __PASS_I_Y__%;">
          <input id="dni" class="input" type="password" autocomplete="current-password" placeholder="••••"/>
        </div>

        <div id="btnLogin" class="btn" style="top: __BTN_Y__%;">__BTN_TEXT__</div>

        <div id="err"></div>

        <div class="rowLinks" style="top: __LINKS_Y__%;">
          <div>__LINK_LEFT__</div>
          <div>__LINK_RIGHT__</div>
        </div>
      </div>
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

  var closeBtn = document.getElementById("closeBtn");
  closeBtn.addEventListener("click", function(){
    window.location.href = window.location.origin + "/";
  });

  function showErr(msg){
    var e = document.getElementById("err");
    e.style.display = "block";
    e.textContent = msg || "Error conectando con el servidor";
  }
  function hideErr(){
    var e = document.getElementById("err");
    e.style.display = "none";
    e.textContent = "";
  }

  async function doLogin(){
    hideErr();
    var correo = (document.getElementById("correo").value || "").trim();
    var dni = (document.getElementById("dni").value || "").trim();

    if(!correo || !dni){
      showErr("Completa correo y DNI");
      return;
    }

    try{
      var r = await fetch("__AUTH_URL__", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({correo: correo, dni: dni})
      });

      var dataText = await r.text();
      var data = {};
      try{ data = JSON.parse(dataText); }catch(e){}

      if(r.ok && data && data.ok === true){
        var usuario = encodeURIComponent(data.usuario || correo);
        var rol = encodeURIComponent(data.rol || data.role || "");
        window.location.href = window.location.origin + "/?auth=1&usuario=" + usuario + "&rol=" + rol;
        return;
      }

      showErr((data && (data.error || data.msg)) ? (data.error || data.msg) : "Credenciales inválidas");
    }catch(e){
      showErr("Error conectando con el servidor");
    }
  }

  document.getElementById("btnLogin").addEventListener("click", doLogin);
  document.getElementById("dni").addEventListener("keydown", function(ev){
    if(ev.key === "Enter") doLogin();
  });
})();
</script>
</body>
</html>
"""

html = (
    HTML
    .replace("__PADX__", str(PAD_X_PX))
    .replace("__PADTOP__", str(PAD_TOP_PX))
    .replace("__B__", str(BORDER_PX))
    .replace("__BC__", str(BORDER_COLOR))
    .replace("__BG_A__", str(BG_GRAD_A))
    .replace("__BG_B__", str(BG_GRAD_B))
    .replace("__BG_HILIGHT__", str(BG_HILIGHT))
    .replace("__CARD_W__", str(CARD_W))
    .replace("__CARD_H__", str(CARD_H))
    .replace("__CARD_X__", str(CARD_X))
    .replace("__CARD_Y__", str(CARD_Y))
    .replace("__TITLE_Y__", str(TITLE_Y))
    .replace("__USER_L_Y__", str(USER_LABEL_Y))
    .replace("__USER_I_Y__", str(USER_INPUT_Y))
    .replace("__PASS_L_Y__", str(PASS_LABEL_Y))
    .replace("__PASS_I_Y__", str(PASS_INPUT_Y))
    .replace("__BTN_Y__", str(BTN_Y))
    .replace("__LINKS_Y__", str(LINKS_Y))
    .replace("__TITLE_SZ__", str(TITLE_SZ))
    .replace("__LABEL_SZ__", str(LABEL_SZ))
    .replace("__INPUT_TXT__", str(INPUT_TXT))
    .replace("__BTN_TXT_SZ__", str(BTN_TXT))
    .replace("__LINK_SZ__", str(LINK_SZ))
    .replace("__INPUT_H__", str(INPUT_H_PX))
    .replace("__INPUT_RAD__", str(INPUT_RADIUS_PX))
    .replace("__BTN_H__", str(BTN_H_PX))
    .replace("__BTN_RAD__", str(BTN_RADIUS_PX))
    .replace("__CARD_BG__", str(CARD_BG))
    .replace("__CARD_BORDER__", str(CARD_BORDER))
    .replace("__TXT_WHITE__", str(TXT_WHITE))
    .replace("__TXT_MUTED__", str(TXT_MUTED))
    .replace("__FIELD_BG__", str(FIELD_BG))
    .replace("__FIELD_TXT__", str(FIELD_TXT))
    .replace("__BTN_A__", str(BTN_GRAD_A))
    .replace("__BTN_B__", str(BTN_GRAD_B))
    .replace("__BTN_TXT__", str(BTN_TXT_COLOR))
    .replace("__ERR_BG__", str(ERROR_BG))
    .replace("__ERR_TXT__", str(ERROR_TXT))
    .replace("__AUTH_URL__", AUTH_URL)
    .replace("__TITLE_TEXT__", TITLE_TEXT)
    .replace("__BTN_TEXT__", BTN_TEXT)
    .replace("__LABEL_CORREO__", LABEL_CORREO)
    .replace("__LABEL_DNI__", LABEL_DNI)
    .replace("__LINK_LEFT__", LINK_LEFT)
    .replace("__LINK_RIGHT__", LINK_RIGHT)
)

components.html(html, height=10, scrolling=False)
