# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components
import importlib
import syntra_core

# Recarga el modulo comun: el servidor puede quedarse con una version vieja en memoria
importlib.reload(syntra_core)
from syntra_core import sync_auth, go, shell_css, NAV_JS

# Logo oficial de SYNTRA incrustado (no depende de servidores externos)
LOGO_DATA_URI = "data:image/png;base64,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"

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
shell_css("#040e31")

html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no"/>
<style>
:root{
  --baseBlue: #040e31;
  --bgTop:  #0a1a55;
  --bgMid:  #061240;
  --bgDeep: #02071c;

  --overlay1: rgba(40, 120, 255, .16);
  --overlay2: rgba(0,  10,  40, .62);

  --ink: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.62);

  --pill: rgba(238, 245, 255, .92);
  --pill2: rgba(255,255,255,.86);

  --btn1:#2f7de1;
  --btn2:#1e5fc4;

  --shadow1: 0 22px 55px rgba(0,0,0,.55);
  --shadow2: 0 10px 22px rgba(0,0,0,.40);
  --blur: 14px;

  --logoWDesktop: 250px;
  --logoTopDesktop: 0.0%;
  --logoXDesktop: 0px;

  --titleTopDesktop: 20%;
  --titleSizeDesktop: 22px;
  --titleXDesktop: 0px;

  --lblUserTopDesktop: 22%;
  --inUserTopDesktop: 28%;
  --lblPassTopDesktop: 42%;
  --inPassTopDesktop: 48%;
  --btnTopDesktop: 67%;

  --linkPolTopDesktop: 78%;
  --linkPolLeftDesktop: 20%;
  --linkRegTopDesktop: 78%;
  --linkRegLeftDesktop: 68%;

  --labelSizeDesktop: 22px;
  --inputSizeDesktop: 22px;
  --btnTextSizeDesktop: 22px;
  --linkSizeDesktop: 22px;

  --logoWMobile: 150px;
  --logoTopMobile: 6%;
  --logoXMobile: 0px;

  --titleTopMobile: 20%;
  --titleSizeMobile: 18px;
  --titleXMobile: 0px;

  --lblUserTopMobile: 22%;
  --inUserTopMobile: 28%;
  --lblPassTopMobile: 42%;
  --inPassTopMobile: 48%;
  --btnTopMobile: 65%;

  --linkPolTopMobile: 78%;
  --linkPolLeftMobile: 20%;
  --linkRegTopMobile: 78%;
  --linkRegLeftMobile: 68%;

  --labelSizeMobile: 16px;
  --inputSizeMobile: 16px;
  --btnTextSizeMobile: 18px;
  --linkSizeMobile: 15px;
}

*{box-sizing:border-box}
html, body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  overflow:hidden;
  background: var(--baseBlue);
}

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
  transition: all 0.2s ease;
}

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
  transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
}

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
  transition: all 0.3s ease;
}

#card{
  position:absolute;
  left:6%;
  right:6%;
  top:6%;
  bottom:6%;
}

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

.title{
  display:none;
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

/* Las etiquetas ya no se usan, se eliminan del HTML */
input.field{
  position:absolute;
  left:22%;
  right:22%;
  height:10%;
  border: 1px solid rgba(255,255,255,.55);
  border-radius: 999px;
  box-sizing:border-box;
  background: linear-gradient(180deg, var(--pill) 0%, var(--pill2) 100%);
  padding: 0 16px;
  font:700 var(--inputSizeDesktop) Arial, sans-serif !important;
  color: rgba(30,40,55,.92);
  outline:none;
  box-shadow:
    0 15px 18px rgba(0,0,0,.22),
    inset 0 1px 0 rgba(255,255,255,.55);
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
}
input.field::placeholder{ color: rgba(60,70,85,.55); }

.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:10%;  
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 999px;
  box-sizing:border-box;
  background:
    radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.22), transparent 60%),
    linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
  box-shadow:
    0 22px 26px rgba(0,0,0,.28),
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

.link{
  position:absolute;
  font:700 var(--linkSizeDesktop) Arial, sans-serif !important;
  color: rgba(255,255,255,.70);
  white-space:nowrap;
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}
.link:hover{ color: rgba(255,255,255,.85); }

#hud{
  position:absolute; inset:0;
  pointer-events:none;
  background:
    radial-gradient(60% 45% at 50% 18%, rgba(255,255,255,.12), transparent 60%),
    linear-gradient(180deg, transparent 62%, rgba(0,0,0,.30) 100%);
}

.fullscreen-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 48px;
  height: 48px;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(12px);
  border-radius: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
  cursor: pointer;
  z-index: 10000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
  border: 1px solid rgba(255,255,255,0.2);
  font-weight: bold;
  user-select: none;
  touch-action: manipulation;
}
.fullscreen-toggle:active {
  transform: scale(0.92);
  background: rgba(0,0,0,0.8);
}
@media (min-width: 769px) {
  .fullscreen-toggle {
    display: none;
  }
}
@media (max-width: 768px) {
  .fullscreen-toggle {
    display: flex;
  }
}

html:fullscreen #stage.fullscreen-mode #plan,
html:-webkit-full-screen #stage.fullscreen-mode #plan,
html:-moz-full-screen #stage.fullscreen-mode #plan {
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  border-radius: 0;
  box-shadow: none;
}
html:fullscreen #stage.fullscreen-mode #frame,
html:-webkit-full-screen #stage.fullscreen-mode #frame,
html:-moz-full-screen #stage.fullscreen-mode #frame {
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  border-radius: 0;
}

/* ========== SPLASH PROFESIONAL TEMÁTICO (SALVAMENTO ACUÁTICO) ========== */
#splash {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(145deg, #021c3a 0%, #00122a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20000;
  transition: opacity 1s ease-out, visibility 0s linear 1s;
  font-family: 'Segoe UI', 'Roboto', 'Poppins', sans-serif;
  overflow: hidden;
}

/* Fondo de ondas sutiles */
.waves-bg {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(transparent 0px, transparent 98px, rgba(74, 126, 255, 0.08) 98px, rgba(74, 126, 255, 0.12) 100px);
  pointer-events: none;
  animation: waveMove 6s linear infinite;
}

@keyframes waveMove {
  0% { background-position: 0 0; }
  100% { background-position: 0 100px; }
}

/* Contenedor principal del splash */
.splash-content {
  text-align: center;
  z-index: 10;
  animation: fadeInUp 0.8s cubic-bezier(0.2, 0.9, 0.4, 1.1) forwards;
  position: relative;
  top: -5%; /* centrado visual */
}

@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(30px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* Símbolo de salvavidas (cruz de rescate) */
.lifeguard-symbol {
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
  border: 2px solid rgba(74, 126, 255, 0.6);
  box-shadow: 0 0 20px rgba(74, 126, 255, 0.3);
  animation: pulseSoft 1.5s infinite alternate;
}

.lifeguard-symbol svg {
  width: 60px;
  height: 60px;
  filter: drop-shadow(0 0 6px #4a7eff);
}

@keyframes pulseSoft {
  0% { transform: scale(0.95); opacity: 0.7; box-shadow: 0 0 10px rgba(74,126,255,0.3); }
  100% { transform: scale(1.05); opacity: 1; box-shadow: 0 0 30px rgba(74,126,255,0.6); }
}

/* Texto SYNTRA limpio y elegante */
.syntra-text {
  font-size: 3.8rem;
  font-weight: 700;
  letter-spacing: 6px;
  color: white;
  text-shadow: 0 0 15px rgba(74,126,255,0.8);
  margin-top: 10px;
  font-family: 'Poppins', 'Segoe UI', sans-serif;
}

.sub {
  font-size: 1rem;
  letter-spacing: 2px;
  color: rgba(255,255,255,0.6);
  margin-top: 12px;
  font-weight: 400;
}

/* Ocultar splash */
.splash-hidden {
  opacity: 0;
  visibility: hidden;
}

/* Responsive */
@media (max-width: 768px) {
  .lifeguard-symbol {
    width: 70px;
    height: 70px;
  }
  .lifeguard-symbol svg {
    width: 42px;
    height: 42px;
  }
  .syntra-text {
    font-size: 2.2rem;
    letter-spacing: 3px;
  }
  .sub {
    font-size: 0.8rem;
  }
  .splash-content {
    top: -3%;
  }
}

@media (max-width: 768px){
  #card{ left:8%; right:8%; top:6%; bottom:8%; }

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

  input.field{
    left:12%;
    right:12%;
    font:700 var(--inputSizeMobile) Arial, sans-serif !important;
  }

  .btn{
    left:24%;
    right:24%;
    font:700 var(--btnTextSizeMobile) Arial, sans-serif !important;
  }

  .link{
    font:700 var(--linkSizeMobile) Arial, sans-serif !important;
  }

  #inUser { top: var(--inUserTopMobile) !important; }
  #txtPwd { top: var(--inPassTopMobile) !important; }
  #btnLogin{ top: var(--btnTopMobile) !important; }

  #linkPol{
    top: var(--linkPolTopMobile) !important;
    left: var(--linkPolLeftMobile) !important;
  }
  #linkReg{
    top: var(--linkRegTopMobile) !important;
    left: var(--linkRegLeftMobile) !important;
  }

  /* Ocultar título en móvil (opcional, se mantiene) */
  .title {
    display: none;
  }
}
</style>
</head>
<body>
<div id="stage">
  <div id="plan">
    <div id="frame"></div>

    <div id="card">
      <img class="logo" src="__LOGO_URL__" alt="Logo"/>
      <div class="title">¡BIENVENIDO!</div>

      <form autocomplete="off" style="margin:0; padding:0; position:relative; height:100%; width:100%;">
        <!-- Las etiquetas "Usuario:" y "Contraseña:" han sido eliminadas -->
        <input id="inUser" class="field" style="top:28%;" 
               autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" 
               placeholder="Usuario"/>

        <input id="txtPwd" class="field" style="top:48%; -webkit-text-security: disc; text-security: disc;" 
               type="text" 
               autocomplete="new-password" 
               autocapitalize="off" 
               autocorrect="off" 
               spellcheck="false" 
               inputmode="text"
               placeholder="Contraseña"/>

        <div id="btnLogin" class="btn" style="top:67%;" onclick="doLogin()">Login</div>

        <div id="linkPol" class="link" style="top:78%; left:20%;">Politicas:</div>
        <div id="linkReg" class="link" style="top:78%; left:68%;"><a href="/altas_registro" onclick="event.preventDefault(); syntraTopNav('/altas_registro');" style="color:inherit; text-decoration:none;">Registrarse:</a></div>
      </form>
    </div>

    <div id="hud"></div>
  </div>
</div>

<!-- SPLASH PROFESIONAL -->
<div id="splash">
  <div class="waves-bg"></div>
  <div class="splash-content">
    <div class="lifeguard-symbol">
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="42" stroke="#4a7eff" stroke-width="3" fill="none"/>
        <path d="M50 20 L50 80 M20 50 L80 50" stroke="#4a7eff" stroke-width="4" stroke-linecap="round"/>
        <circle cx="50" cy="50" r="8" fill="#4a7eff"/>
        <path d="M50 8 L50 20 M50 80 L50 92 M8 50 L20 50 M80 50 L92 50" stroke="#4a7eff" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>
    <div class="syntra-text">SYNTRA</div>
    <div class="sub">Lifeguard Management</div>
  </div>
</div>

<div id="fullscreenToggleBtn" class="fullscreen-toggle">⤢</div>

<script>
__SYNTRA_NAV__
// ---------- SPLASH TIMER (2 segundos) ----------
window.addEventListener('load', function() {
  setTimeout(function() {
    var splash = document.getElementById('splash');
    if (splash) {
      splash.classList.add('splash-hidden');
      setTimeout(function() {
        if (splash && splash.parentNode) splash.parentNode.removeChild(splash);
      }, 1000);
    }
  }, 2000);
});

// ---------- LOGIN Y FULLSCREEN (sin cambios) ----------
async function doLogin(){
  const u = (document.getElementById("inUser").value || "").trim();
  const p = (document.getElementById("txtPwd").value || "").trim();

  try{
    const r = await fetch("https://camilo27.pythonanywhere.com/api/auth", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({usuario:u, password:p})
    });

    const j = await r.json();

    if (j && j.ok === true){
      const rol = (j.rol || "").toString();
      const dni = (j.dni || "").toString();
      syntraTopNav("/?auth=ok&usuario=" + encodeURIComponent(u) + "&rol=" + encodeURIComponent(rol) + "&dni=" + encodeURIComponent(dni));
    } else {
      alert("Credenciales inválidas");
    }
  }catch(e){
    alert("Error de conexión");
  }
}

const stage = document.getElementById("stage");
const btn = document.getElementById("fullscreenToggleBtn");

function setFullscreenFlag(active) {
  if (active) localStorage.setItem("fullscreenActive", "true");
  else localStorage.removeItem("fullscreenActive");
}

function enterFullscreen() {
  const elem = document.documentElement;
  const requestMethod = elem.requestFullscreen || elem.webkitRequestFullscreen || elem.mozRequestFullScreen || elem.msRequestFullscreen;
  if (requestMethod) {
    requestMethod.call(elem).then(() => {
      if (stage) stage.classList.add("fullscreen-mode");
      if (btn) { btn.textContent = "✕"; btn.style.fontSize = "26px"; }
      setFullscreenFlag(true);
    }).catch(err => console.log(err));
  }
}

function exitFullscreen() {
  const exitMethod = document.exitFullscreen || document.webkitExitFullscreen || document.mozCancelFullScreen || document.msExitFullscreen;
  if (exitMethod) {
    exitMethod.call(document).then(() => {
      if (stage) stage.classList.remove("fullscreen-mode");
      if (btn) { btn.textContent = "⤢"; btn.style.fontSize = "28px"; }
      setFullscreenFlag(false);
    }).catch(err => console.log(err));
  }
}

function toggleFullscreen() {
  const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
  isFull ? exitFullscreen() : enterFullscreen();
}

function onFullscreenChange() {
  const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
  if (isFull) {
    if (stage) stage.classList.add("fullscreen-mode");
    if (btn) { btn.textContent = "✕"; btn.style.fontSize = "26px"; }
    setFullscreenFlag(true);
  } else {
    if (stage) stage.classList.remove("fullscreen-mode");
    if (btn) { btn.textContent = "⤢"; btn.style.fontSize = "28px"; }
    setFullscreenFlag(false);
  }
}

document.addEventListener("fullscreenchange", onFullscreenChange);
document.addEventListener("webkitfullscreenchange", onFullscreenChange);
document.addEventListener("mozfullscreenchange", onFullscreenChange);
document.addEventListener("MSFullscreenChange", onFullscreenChange);

if (btn) btn.addEventListener("click", (e) => { e.preventDefault(); toggleFullscreen(); });

if (window.innerWidth <= 768) {
  const savedFlag = localStorage.getItem("fullscreenActive");
  if (savedFlag === "true") {
    const isCurrentlyFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
    if (!isCurrentlyFull) enterFullscreen();
    else { if (stage) stage.classList.add("fullscreen-mode"); if (btn) { btn.textContent = "✕"; btn.style.fontSize = "26px"; } }
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
    fe.style.background="transparent";
  }
})();
</script>
</body>
</html>
"""

html = html.replace("__SYNTRA_NAV__", NAV_JS).replace("__LOGO_URL__", LOGO_DATA_URI)

components.html(html, height=1000, scrolling=False)
