# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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

html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>

<style>
:root{
  /* =========================================================
     PALETA (AZUL base #040e31) -> ajusta tonos globales aquí
     ========================================================= */
  --baseBlue: #040e31;            /* BASE requerida */
  --bgTop:  #0a1a55;              /* superior (más claro) */
  --bgMid:  #061240;              /* medio */
  --bgDeep: #02071c;              /* inferior (más oscuro) */

  --overlay1: rgba(40, 120, 255, .16); /* corte diagonal claro */
  --overlay2: rgba(0,  10,  40, .62);  /* corte diagonal oscuro */

  --ink: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.62);

  --pill: rgba(238, 245, 255, .92);
  --pill2: rgba(255,255,255,.86);

  --btn1:#2f7de1;
  --btn2:#1e5fc4;

  --shadow1: 0 22px 55px rgba(0,0,0,.55);
  --shadow2: 0 10px 22px rgba(0,0,0,.40);
  --blur: 14px;

  /* =========================================================
     CONTROLES DESKTOP (pantalla completa)
     Cambia AQUÍ posición/tamaño para desktop
     ========================================================= */
  --logoWDesktop: 310px;     /* tamaño logo desktop */
  --logoTopDesktop: 0.0%;    /* subir/bajar logo desktop */
  --logoXDesktop: 0px;       /* mover logo izq/der desktop (px) */

  --titleTopDesktop: 20%;    /* subir/bajar título desktop */
  --titleSizeDesktop: 22px;  /* tamaño título desktop */ 
  --titleXDesktop: 0px;      /* mover título izq/der desktop (px) */

  --lblUserTopDesktop: 22%;
  --inUserTopDesktop: 28%;
  --lblPassTopDesktop: 42%;
  --inPassTopDesktop: 48%;
  --btnTopDesktop: 67%;

  --linkPolTopDesktop: 78%;
  --linkPolLeftDesktop: 20%;
  --linkRegTopDesktop: 78%;
  --linkRegLeftDesktop: 68%;

  --labelSizeDesktop: 22px; /* 14px */
  --inputSizeDesktop: 22px; /* 14px */
  --btnTextSizeDesktop: 22px; /* 14px */
  --linkSizeDesktop: 22px; /* 13px estoy aqui */

  /* =========================================================
     CONTROLES MÓVIL
     Cambia AQUÍ posición/tamaño para móvil
     ========================================================= */
  --logoWMobile: 150px;      /* tamaño logo móvil */
  --logoTopMobile: 6%;       /* subir/bajar logo móvil */
  --logoXMobile: 0px;        /* mover logo izq/der móvil (px) *

  --titleTopMobile: 20%;     /* subir/bajar título móvil */
  --titleSizeMobile: 18px;   /* tamaño título móvil */
  --titleXMobile: 0px;       /* mover título izq/der móvil (px) */

  --lblUserTopMobile: 22%;
  --inUserTopMobile: 28%;     /* 28 */
  --lblPassTopMobile: 42%;  /* 42 */
  --inPassTopMobile: 48%;    /* 48 */
  --btnTopMobile: 65%;     /* 67%*/

  --linkPolTopMobile: 78%; /* 78 */
  --linkPolLeftMobile: 20%; /* 20 */
  --linkRegTopMobile: 78%;
  --linkRegLeftMobile: 68%; /* 68 */

  --labelSizeMobile: 16px;    /* 16 */
  --inputSizeMobile: 16px;    /* 16 */
  --btnTextSizeMobile: 18px; /* 14 */
  --linkSizeMobile: 15px;  /* 13*/
}

/* RESET */
*{box-sizing:border-box}
html, body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  overflow:hidden;
  background: var(--baseBlue);
}

/* FONDO EXTERIOR */
#stage{
  position:fixed;
  inset:0;
  width:100vw;
  height:100vh;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.14), transparent 60%),
    radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
    linear-gradient(180deg, #020614 0%, var(--baseBlue) 100%);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* PANEL PRINCIPAL */
#plan{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  overflow:hidden;
  border-radius: 34px;
  box-shadow: var(--shadow1);
  background:
    linear-gradient(180deg, rgba(255,255,255,.16) 0%, transparent 22%),
    linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #05164d 58%, var(--bgDeep) 100%);
}

/* CORTE DIAGONAL */
#plan::before{
  content:"";
  position:absolute;
  inset:-10%;
  background:
    linear-gradient(135deg,
      transparent 0%,
      transparent 32%,
      var(--overlay1) 32%,
      var(--overlay2) 66%,
      transparent 66%);
  transform: rotate(-10deg);
  opacity:.95;
  pointer-events:none;
}

/* VIÑETA */
#plan::after{
  content:"";
  position:absolute;
  inset:0;
  background:
    radial-gradient(50% 60% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
    radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
    linear-gradient(180deg, transparent 55%, rgba(0,0,0,.65) 100%);
  pointer-events:none;
}

/* MARCO */
#frame{
  position:absolute;
  left:9px; right:9px;
  top:10px; bottom:0;
  border-left: 2px solid rgba(255,255,255,.14);
  border-right:2px solid rgba(255,255,255,.14);
  border-top:  2px solid rgba(255,255,255,.14);
  box-sizing:border-box;
  pointer-events:none;
  border-radius: 34px;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,.55);
}

/* CONTENEDOR */
#card{
  position:absolute;
  left:6%;
  right:6%;
  top:6%;
  bottom:6%;
}

/* =========================================================
   LOGO (DESKTOP por defecto)
   - Tamaño: --logoWDesktop
   - Posición vertical: --logoTopDesktop
   - Movimiento X: --logoXDesktop (px)
   ========================================================= */
.logo{
  position:absolute;
  left:50%;
  top: var(--logoTopDesktop) !important;
  transform: translateX(-50%) translateX(var(--logoXDesktop)) !important;
  width: var(--logoWDesktop) !important;
  height:auto;
  display:block;
  border-radius: 10px;
  filter: drop-shadow(0 10px 18px rgba(0,0,0,.35));
}

/* =========================================================
   TÍTULO (DESKTOP por defecto)
   - Tamaño: --titleSizeDesktop
   - Posición vertical: --titleTopDesktop
   - Movimiento X: --titleXDesktop (px)
   ========================================================= */
.title{
  position:absolute;
  left:0; right:0;
  top: var(--titleTopDesktop) !important;
  text-align:center;
  font:800 var(--titleSizeDesktop) Arial, sans-serif !important;
  color: var(--ink);
  text-shadow: 0 8px 18px rgba(0,0,0,.35);
  letter-spacing: .2px;
  transform: translateX(var(--titleXDesktop)) !important;
}

/* LABELS */
.label{
  position:absolute;
  left:18%;
  right:18%;
  font:700 var(--labelSizeDesktop) Arial, sans-serif !important;
  color: rgba(255,255,255,.82);
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}

/* INPUTS */
input.field{
  position:absolute;
  left:22%; /* 16 */
  right:22%; /* 16 */
  height:10%; /* 16 */
  border: 1px solid rgba(255,255,255,.55);
  border-radius: 999px;
  box-sizing:border-box;
  background: linear-gradient(180deg, var(--pill) 0%, var(--pill2) 100%);
  padding: 0 16px; /* 14 */
  font:700 var(--inputSizeDesktop) Arial, sans-serif !important;
  color: rgba(30,40,55,.92);
  outline:none;
  box-shadow:
    0 15px 18px rgba(0,0,0,.22), /*0 10px */
    inset 0 1px 0 rgba(255,255,255,.55);
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
}
input.field::placeholder{ color: rgba(60,70,85,.55); }

/* BOTÓN */
.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:10%;  
  border: 1px solid rgba(255,255,255,.10);/* Estoy aqui 10*/
  border-radius: 999px;
  box-sizing:border-box;
  background:
    radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.22), transparent 60%), /* Estoy aqui transparent 80%*/
    linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
  box-shadow:
    0 22px 26px rgba(0,0,0,.28),/* Estoy aqui 0 18px */
    inset 0 1px 0 rgba(255,255,255,.22);
  display:flex;
  align-items:center;
  justify-content:center;
  font:700 var(--btnTextSizeDesktop) Arial, sans-serif !important;
  color: rgba(255,255,255,.92);
  cursor:pointer;
  user-select:none;
  transition: transform .12s ease, filter .12s ease;
}
.btn:active{ transform: scale(.985); filter: brightness(.98); }

/* LINKS */
.link{
  position:absolute;
  font:700 var(--linkSizeDesktop) Arial, sans-serif !important;
  color: rgba(255,255,255,.70);
  white-space:nowrap;
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}
.link:hover{ color: rgba(255,255,255,.85); }

/* HUD oculto */
#hud{ display:none !important; }

/* =========================================================
   POSICIONES DESKTOP (override a los inline style)
   Edita variables arriba, no toques el HTML si no quieres.
   ========================================================= */
#lblUser{ top: var(--lblUserTopDesktop) !important; }
#inUser{  top: var(--inUserTopDesktop) !important; }
#lblPass{ top: var(--lblPassTopDesktop) !important; }
#inPass{  top: var(--inPassTopDesktop) !important; }
#btnLogin{ top: var(--btnTopDesktop) !important; }

#linkPol{ top: var(--linkPolTopDesktop) !important; left: var(--linkPolLeftDesktop) !important; }
#linkReg{ top: var(--linkRegTopDesktop) !important; left: var(--linkRegLeftDesktop) !important; }

/* =========================================================
   MODO MÓVIL (posiciones/tamaños distintos)
   Edita variables Mobile arriba.
   ========================================================= */
@media (max-width: 640px){
  .logo{
    top: var(--logoTopMobile) !important;
    width: var(--logoWMobile) !important;
    transform: translateX(-50%) translateX(var(--logoXMobile)) !important;
  }
  .title{
    top: var(--titleTopMobile) !important;
    font:800 var(--titleSizeMobile) Arial, sans-serif !important;
    transform: translateX(var(--titleXMobile)) !important;
  }
  .label{ font:700 var(--labelSizeMobile) Arial, sans-serif !important; }
  input.field{ font:700 var(--inputSizeMobile) Arial, sans-serif !important; }
  .btn{ font:700 var(--btnTextSizeMobile) Arial, sans-serif !important; }
  .link{ font:700 var(--linkSizeMobile) Arial, sans-serif !important; }

  #lblUser{ top: var(--lblUserTopMobile) !important; }
  #inUser{  top: var(--inUserTopMobile) !important; }
  #lblPass{ top: var(--lblPassTopMobile) !important; }
  #inPass{  top: var(--inPassTopMobile) !important; }
  #btnLogin{ top: var(--btnTopMobile) !important; }

  #linkPol{ top: var(--linkPolTopMobile) !important; left: var(--linkPolLeftMobile) !important; }
  #linkReg{ top: var(--linkRegTopMobile) !important; left: var(--linkRegLeftMobile) !important; }
}
</style>
</head>

<body>
<div id="stage">
  <div id="frame"></div>

  <div id="plan">
    <div id="card">
      <!-- LOGO: cambia tamaño/posición con variables Desktop/Mobile en :root -->
      <img class="logo" src="https://files.catbox.moe/056m6v.jpg" alt="Logo"/>

      <!-- TÍTULO: cambia tamaño/posición con variables Desktop/Mobile en :root -->
      <div class="title">¡BIENVENIDO!</div>

      <!-- Estos inline style quedan como “fallback”.
           Las posiciones reales se controlan por variables (CSS) por modo. -->
      <div id="lblUser" class="label" style="top:22%;">Usuario:</div>
      <input id="inUser" class="field" style="top:28%;" autocomplete="username"/>

      <div id="lblPass" class="label" style="top:42%;">Contraseña:</div>
      <input id="inPass" class="field" style="top:48%;" type="password" autocomplete="current-password"/>

      <div id="btnLogin" class="btn" style="top:67%;" onclick="doLogin()">Login</div>

      <div id="linkPol" class="link" style="top:78%; left:20%;">Politicas:</div>
      <div id="linkReg" class="link" style="top:78%; left:68%;">Registrarse:</div>
    </div>

    <div id="hud"></div>
  </div>
</div>

<script>
async function doLogin(){
  const u = (document.getElementById("inUser").value || "").trim();
  const p = (document.getElementById("inPass").value || "").trim();

  try{
    const r = await fetch("https://camilo27.pythonanywhere.com/api/auth", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({usuario:u, password:p})
    });

    const j = await r.json();

    if (j && j.ok === true){
      window.location.href = "/?auth=ok";
    } else {
      alert("Credenciales inválidas");
    }
  }catch(e){
    alert("Error de conexión");
  }
}

(function(){
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
})();
</script>

</body>
</html>
"""

components.html(html, height=10, scrolling=False)
