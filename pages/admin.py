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

.label{
  position:absolute;
  left:18%;
  right:18%;
  font:700 var(--labelSizeDesktop) Arial, sans-serif !important;
  color: rgba(255,255,255,.82);
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}

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

/* ========== SPLASH MEJORADO con ajuste de posición vertical ========== */
#splash {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, #030b1f 0%, #000000 100%);
  display: flex;
  align-items: center;      /* centrado vertical */
  justify-content: center;  /* centrado horizontal */
  z-index: 20000;
  transition: opacity 0.8s cubic-bezier(0.23, 1, 0.32, 1), visibility 0s linear 0.8s;
  backdrop-filter: blur(2px);
  font-family: 'Segoe UI', 'Arial Black', 'Impact', sans-serif;
  overflow: hidden;
}

/* Contenedor del texto: lo subimos un 8% respecto al centro */
.splash-content {
  text-align: center;
  z-index: 10;
  animation: fadeInScale 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  position: relative;
  top: -8%;  /* Ajuste hacia arriba */
}

/* Grid de neón */
.splash-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(74,126,255,0.15) 1px, transparent 1px),
    linear-gradient(90deg, rgba(74,126,255,0.15) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
  opacity: 0.5;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(40px, 40px); }
}

/* Líneas de escaneo */
.scan-line {
  position: absolute;
  width: 100%;
  height: 8px;
  background: rgba(74,126,255,0.4);
  filter: blur(2px);
  animation: scan 4s linear infinite;
  top: -10%;
}

@keyframes scan {
  0% { top: -10%; }
  100% { top: 110%; }
}

@keyframes fadeInScale {
  0% { opacity: 0; transform: scale(0.8); filter: blur(10px); }
  100% { opacity: 1; transform: scale(1); filter: blur(0); }
}

/* Texto con glitch */
.glitch-text {
  font-size: 6rem;
  font-weight: 900;
  letter-spacing: 12px;
  position: relative;
  display: inline-block;
  color: white;
  text-shadow: 
    0 0 10px #4a7eff,
    0 0 20px #4a7eff,
    0 0 40px #2f5fcf;
  animation: glitchSkew 3s infinite alternate;
}

.glitch-text::before,
.glitch-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent;
}

.glitch-text::before {
  color: #ff00cc;
  z-index: -1;
  animation: glitchOffset 0.2s infinite linear alternate-reverse;
}

.glitch-text::after {
  color: #00ffff;
  z-index: -2;
  animation: glitchOffset2 0.18s infinite linear alternate-reverse;
}

@keyframes glitchOffset {
  0% { transform: translate(0); opacity: 0.8; }
  100% { transform: translate(-4px, 2px); opacity: 0.4; }
}

@keyframes glitchOffset2 {
  0% { transform: translate(0); opacity: 0.8; }
  100% { transform: translate(4px, -2px); opacity: 0.4; }
}

@keyframes glitchSkew {
  0% { transform: skew(0deg); }
  95% { transform: skew(0deg); }
  96% { transform: skew(2deg); }
  97% { transform: skew(-2deg); }
  98% { transform: skew(1deg); }
  100% { transform: skew(0deg); }
}

/* Halo de luz pulsante */
.halo-ring {
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(74,126,255,0.8) 0%, rgba(74,126,255,0) 70%);
  animation: haloPulse 1.2s infinite alternate;
  filter: blur(12px);
}

@keyframes haloPulse {
  0% { transform: scale(0.6); opacity: 0.5; }
  100% { transform: scale(1.2); opacity: 0.2; }
}

/* Partículas (canvas) */
#particles-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5;
}

/* Destello de lente */
.lens-flare {
  position: absolute;
  width: 150%;
  height: 150%;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 60%);
  top: -25%;
  left: -25%;
  animation: flareRotate 8s linear infinite;
  pointer-events: none;
  mix-blend-mode: overlay;
}

@keyframes flareRotate {
  0% { transform: rotate(0deg) translate(10%, 10%); }
  100% { transform: rotate(360deg) translate(10%, 10%); }
}

/* Ocultar splash */
.splash-hidden {
  opacity: 0;
  visibility: hidden;
}

/* Responsive para móvil */
@media (max-width: 768px) {
  .glitch-text {
    font-size: 2.5rem;
    letter-spacing: 6px;
  }
  .halo-ring {
    width: 120px;
    height: 120px;
  }
  .splash-grid {
    background-size: 20px 20px;
  }
  .splash-content {
    top: -5%;  /* menos desplazamiento en móvil para no cortar */
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

  .label{
    left:12%;
    right:12%;
    font:700 var(--labelSizeMobile) Arial, sans-serif !important;
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

  #lblUser{ top: var(--lblUserTopMobile) !important; }
  #inUser { top: var(--inUserTopMobile) !important; }
  #lblPass{ top: var(--lblPassTopMobile) !important; }
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

  /* Ocultar título y etiquetas en móvil */
  .title,
  #lblUser,
  #lblPass {
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
        <div id="lblUser" class="label" style="top:22%;">Usuario:</div>
        <input id="inUser" class="field" style="top:28%;" 
               autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" 
               placeholder="Usuario"/>

        <div id="lblPass" class="label" style="top:42%;">Contraseña:</div>
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

<!-- SPLASH MEJORADO -->
<div id="splash">
  <canvas id="particles-canvas"></canvas>
  <div class="splash-grid"></div>
  <div class="scan-line"></div>
  <div class="lens-flare"></div>
  <div class="splash-content">
    <div class="halo-ring"></div>
    <div class="glitch-text" data-text="SYNTRA">SYNTRA</div>
  </div>
</div>

<div id="fullscreenToggleBtn" class="fullscreen-toggle">⤢</div>

<script>
// ---------- PARTÍCULAS ----------
const canvas = document.getElementById('particles-canvas');
let ctx = null;
let particles = [];
let animationId = null;

function initParticles() {
  if (!canvas) return;
  ctx = canvas.getContext('2d');
  resizeCanvas();
  const particleCount = 120;
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 3 + 1,
      speedX: (Math.random() - 0.5) * 0.8,
      speedY: (Math.random() - 0.5) * 0.5,
      alpha: Math.random() * 0.6 + 0.2,
      color: `rgba(74, 126, 255, ${Math.random() * 0.5 + 0.2})`
    });
  }
  drawParticles();
}

function resizeCanvas() {
  if (!canvas) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

function drawParticles() {
  if (!ctx || !canvas) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let p of particles) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.fill();
    // actualizar posición
    p.x += p.speedX;
    p.y += p.speedY;
    if (p.x < 0) p.x = canvas.width;
    if (p.x > canvas.width) p.x = 0;
    if (p.y < 0) p.y = canvas.height;
    if (p.y > canvas.height) p.y = 0;
  }
  animationId = requestAnimationFrame(drawParticles);
}

window.addEventListener('resize', () => {
  if (canvas) {
    resizeCanvas();
    // Reajustar partículas al nuevo tamaño
    if (particles.length) {
      for (let p of particles) {
        p.x = Math.random() * canvas.width;
        p.y = Math.random() * canvas.height;
      }
    }
  }
});

// Iniciar partículas solo si el splash existe
if (document.getElementById('splash')) {
  initParticles();
}

// ---------- SPLASH TIMER ----------
window.addEventListener('load', function() {
  setTimeout(function() {
    var splash = document.getElementById('splash');
    if (splash) {
      splash.classList.add('splash-hidden');
      // Detener animación de partículas para ahorrar recursos
      if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
      }
      setTimeout(function() {
        if (splash && splash.parentNode) splash.parentNode.removeChild(splash);
      }, 800);
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
