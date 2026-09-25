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
  width: 230px;
  height: 168px;
  margin: 0 auto 14px;
  background: transparent;
  border: 0;
  border-radius: 0;
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulseSoft 1.8s infinite alternate;
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
    width: 190px;
    height: 140px;
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

/* ===== Login fluido: logo, campos y boton se apilan centrados y nunca se montan ===== */
#card{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:clamp(8px,2vh,20px);top:3% !important;bottom:3% !important;}
#card .logo{position:static !important;transform:none !important;width:auto !important;height:clamp(96px,27vh,220px) !important;max-width:72%;object-fit:contain;flex:0 0 auto;margin:0 auto clamp(6px,2.2vh,20px);}
#card form{height:auto !important;width:100%;display:flex;flex-direction:column;align-items:center;gap:clamp(12px,2.8vh,26px);}
#card input.field{position:static !important;top:auto !important;left:auto !important;right:auto !important;width:min(620px,100%);height:clamp(46px,8vh,62px) !important;flex:0 0 auto;}
#card .btn{position:static !important;top:auto !important;left:auto !important;right:auto !important;width:min(380px,72%);height:clamp(46px,8vh,62px) !important;flex:0 0 auto;margin-top:clamp(2px,1vh,10px);}
#card .login-links{display:flex;justify-content:space-between;align-items:center;width:min(620px,100%);padding:0 22px;box-sizing:border-box;}
#card .link{position:static !important;top:auto !important;left:auto !important;}
@media (max-width:768px){
  #card{left:7% !important;right:7% !important;}
  #card .logo{height:clamp(90px,22vh,170px) !important;}
  #card .login-links{padding:0 10px;}
}
/* Politicas: oculto hasta tener el contenido */
#linkPol{display:none !important;}
#card .login-links{justify-content:center !important;}
#linkReg a{cursor:pointer;}

/* ===== Solicitud de alta (publico) ===== */
#solBack{display:none;position:fixed;inset:0;z-index:15000;background:rgba(2,8,28,.62);align-items:center;justify-content:center;padding:16px;box-sizing:border-box;}
#solBack.open{display:flex;}
#solCard{background:#fff;border-radius:18px;width:100%;max-width:440px;max-height:92vh;overflow-y:auto;padding:20px 20px 16px;box-shadow:0 24px 60px rgba(0,0,0,.45);font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#0f1b3d;box-sizing:border-box;}
#solCard h3{margin:0 0 4px;font-size:18px;font-weight:800;}
#solCard .sol-sub{font-size:13px;color:#6b7688;margin:0 0 14px;line-height:1.4;}
#solCard label{display:block;font-size:12px;font-weight:700;color:#6b7688;margin:10px 0 5px;}
#solCard input, #solCard textarea{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #dfe4ee;border-radius:10px;font-size:16px;font-family:inherit;color:#0f1b3d;background:#fbfcfe;}
#solCard textarea{min-height:64px;resize:vertical;}
#solCard input:focus, #solCard textarea:focus{outline:none;border-color:#2f6fe0;}
#solMsg{font-size:13px;margin-top:12px;min-height:18px;line-height:1.4;}
#solMsg.err{color:#b02a2a;} #solMsg.ok{color:#1a7f4f;}
.sol-foot{display:flex;justify-content:flex-end;gap:10px;margin-top:14px;}
.sol-foot button{border:0;border-radius:10px;padding:10px 16px;font-size:14px;font-weight:700;cursor:pointer;}
.sol-foot .ghost{background:#eef0f4;color:#0f1b3d;}
.sol-foot .ok{background:#2f6fe0;color:#fff;}
.sol-foot .ok[disabled]{opacity:.6;cursor:not-allowed;}
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

        <div class="login-links">
        <div id="linkPol" class="link" style="top:78%; left:20%;">Politicas:</div>
        <div id="linkReg" class="link" style="top:78%; left:68%;"><a href="#" onclick="event.preventDefault(); abrirSolicitud();" style="color:inherit; text-decoration:none;">Registrarse</a></div>
        </div>
      </form>
    </div>

    <div id="hud"></div>
  </div>
</div>

<!-- SOLICITUD DE ALTA -->
<div id="solBack"><div id="solCard">
  <h3>Solicitud de alta</h3>
  <p class="sol-sub">D&eacute;janos tus datos. Un administrador revisar&aacute; tu solicitud y te entregar&aacute; tu usuario y contrase&ntilde;a.</p>
  <label>Nombre completo *</label><input id="sol_nombre" autocomplete="off"/>
  <label>DNI *</label><input id="sol_dni" autocomplete="off"/>
  <label>Correo electr&oacute;nico *</label><input id="sol_correo" type="email" autocomplete="off"/>
  <label>Tel&eacute;fono</label><input id="sol_tel" type="tel" autocomplete="off"/>
  <label>Mensaje (opcional)</label><textarea id="sol_msg" placeholder="Ej. instalaci&oacute;n donde trabajar&aacute;s"></textarea>
  <div id="solMsg"></div>
  <div class="sol-foot">
    <button class="ghost" type="button" onclick="cerrarSolicitud()">Cancelar</button>
    <button class="ok" type="button" id="solEnviar" onclick="enviarSolicitud()">Enviar solicitud</button>
  </div>
</div></div>

<!-- SPLASH PROFESIONAL -->
<div id="splash">
  <div class="waves-bg"></div>
  <div class="splash-content">
    <div class="lifeguard-symbol">
      <img src="__LOGO_URL__" alt="SYNTRA" style="width:100%;height:100%;object-fit:contain;display:block;filter:drop-shadow(0 6px 22px rgba(120,170,255,.45));"/>
    </div>
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

// ---------- SOLICITUD DE ALTA (queda pendiente hasta que un Administrador la gestione) ----------
function abrirSolicitud(){
  ["sol_nombre","sol_dni","sol_correo","sol_tel","sol_msg"].forEach(function(id){ document.getElementById(id).value = ""; });
  var m = document.getElementById("solMsg"); m.className = ""; m.textContent = "";
  var b = document.getElementById("solEnviar"); b.disabled = false; b.textContent = "Enviar solicitud"; b.style.display = "";
  document.getElementById("solBack").classList.add("open");
}
function cerrarSolicitud(){ document.getElementById("solBack").classList.remove("open"); }
document.getElementById("solBack").addEventListener("click", function(e){ if (e.target.id === "solBack") cerrarSolicitud(); });
async function enviarSolicitud(){
  var m = document.getElementById("solMsg");
  var b = document.getElementById("solEnviar");
  var body = {
    nombre: document.getElementById("sol_nombre").value.trim(),
    dni: document.getElementById("sol_dni").value.trim(),
    correo: document.getElementById("sol_correo").value.trim(),
    telefono: document.getElementById("sol_tel").value.trim(),
    mensaje: document.getElementById("sol_msg").value.trim()
  };
  if (!body.nombre || !body.dni || !body.correo || body.correo.indexOf("@") === -1){
    m.className = "err"; m.textContent = "Nombre, DNI y un correo válido son obligatorios."; return;
  }
  b.disabled = true; b.textContent = "Enviando..."; m.className = ""; m.textContent = "";
  try{
    const r = await fetch("https://camilo27.pythonanywhere.com/api/solicitudes", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
    const j = await r.json();
    if (j && j.ok){
      m.className = "ok"; m.textContent = "Solicitud enviada. Un administrador la revisará y te entregará tus datos de acceso.";
      b.style.display = "none";
      setTimeout(cerrarSolicitud, 4000);
    } else {
      b.disabled = false; b.textContent = "Enviar solicitud";
      m.className = "err"; m.textContent = (j && j.error) || "No se pudo enviar la solicitud.";
    }
  }catch(e){
    b.disabled = false; b.textContent = "Enviar solicitud";
    m.className = "err"; m.textContent = "Error de conexión.";
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
