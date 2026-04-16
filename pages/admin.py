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
      <img class="logo" src="https://files.catbox.moe/056m6v.jpg" alt="Logo"/>
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
        <div id="linkReg" class="link" style="top:78%; left:68%;"><a href="/altas_registro" style="color:inherit; text-decoration:none;">Registrarse:</a></div>
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
      window.location.href = "/?auth=ok&usuario=" + encodeURIComponent(u) + "&rol=" + encodeURIComponent(rol) + "&dni=" + encodeURIComponent(dni);
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

components.html(html, height=1000, scrolling=False)
