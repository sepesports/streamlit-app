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
     OBJETIVO: Rojo -> AZUL base #040e31 con degradado
     ========================================================= */
  --baseBlue: #040e31;            /* <-- Color base */
  --bgTop:  #0a1a55;              /* <-- Degradado superior (más claro) */
  --bgMid:  #061240;              /* <-- Degradado medio */
  --bgDeep: #02071c;              /* <-- Degradado inferior (más oscuro) */

  --overlay1: rgba(20, 60, 170, .26); /* <-- Corte diagonal (claro) */
  --overlay2: rgba(0,  10,  40, .62); /* <-- Corte diagonal (oscuro) */

  --ink: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.62);

  --pill: rgba(238, 245, 255, .92);
  --pill2: rgba(255,255,255,.86);

  /* =========================================================
     BOTÓN (azules)
     ========================================================= */
  --btn1:#2f7de1;
  --btn2:#1e5fc4;

  --shadow1: 0 22px 55px rgba(0,0,0,.55);
  --shadow2: 0 10px 22px rgba(0,0,0,.40);

  --blur: 14px;

  /* =========================================================
     LOGO RESPONSIVE (AJUSTABLE)
     - Desktop: usa --logoWDesktop y --logoTopDesktop
     - Móvil:   usa --logoWMobile  y --logoTopMobile
     ========================================================= */
  --logoWDesktop: 270px;  /* <-- ANCHO LOGO EN PANTALLA (desktop) */
  --logoTopDesktop: 2.0%; /* <-- POSICIÓN VERTICAL LOGO EN PANTALLA */

  --logoWMobile: 110px;   /* <-- ANCHO LOGO EN MÓVIL */
  --logoTopMobile: 5%;    /* <-- POSICIÓN VERTICAL LOGO EN MÓVIL */

  /* =========================================================
     TAMAÑOS DE TEXTO (AJUSTABLES)
     ========================================================= */
  --titleSize: 18px;      /* <-- TAMAÑO "¡BIENVENIDO!" */
  --labelSize: 14px;      /* <-- TAMAÑO "Usuario / Contraseña" */
  --inputSize: 14px;      /* <-- TAMAÑO TEXTO INPUTS */
  --btnTextSize: 14px;    /* <-- TAMAÑO TEXTO BOTÓN */
  --linkSize: 13px;       /* <-- TAMAÑO LINKS */
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
}

/* Fondo azul + corte diagonal + viñeta (sin cambiar layout) */
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

/* corte diagonal */
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

/* viñeta + profundidad inferior */
#plan::after{
  content:"";
  position:absolute;
  inset:0;
  background:
    radial-gradient(80% 70% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
    radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
    linear-gradient(180deg, transparent 55%, rgba(0,0,0,.65) 100%);
  pointer-events:none;
}

/* marco existente: suavizado visual (sin moverlo) */
#frame{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  border-left: 2px solid rgba(255,255,255,.14);
  border-right:2px solid rgba(255,255,255,.14);
  border-top:  2px solid rgba(255,255,255,.14);
  box-sizing:border-box;
  pointer-events:none;
  border-radius: 34px;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,.55);
}

/* contenedor del card: se mantiene igual */
#card{
  position:absolute;
  left:6%;
  right:6%;
  top:6%;
  bottom:6%;
}

/* =========================================================
   LOGO (encima y centrado del título)
   - Desktop: controlado por variables --logoWDesktop / --logoTopDesktop
   - Móvil:   controlado por variables --logoWMobile  / --logoTopMobile
   ========================================================= */
.logo{
  position:absolute;
  left:50%;
  transform: translateX(-50%);
  top: var(--logoTopDesktop);    /* <-- SUBE/BAJA logo en desktop */
  width: var(--logoWDesktop);    /* <-- ANCHO logo en desktop */
  height:auto;
  display:block;
  border-radius: 10px;           /* quítalo si NO quieres bordes redondeados */
  filter: drop-shadow(0 10px 18px rgba(0,0,0,.35));
}

/* En móvil, usa las variables móviles */
@media (max-width: 640px){
  .logo{
    top: var(--logoTopMobile);   /* <-- SUBE/BAJA logo en móvil */
    width: var(--logoWMobile);   /* <-- ANCHO logo en móvil */
  }
}

/* textos: solo visual */
/* =========================================================
   TÍTULO
   - Tamaño: --titleSize
   - Movimiento: top (sube/baja) aquí
   ========================================================= */
.title{
  position:absolute;
  left:0; right:0;
  top:17%;                        /* <-- SUBE/BAJA "¡BIENVENIDO!" */
  text-align:center;
  font:800 var(--titleSize) Arial, sans-serif; /* <-- TAMAÑO TÍTULO */
  color: var(--ink);
  text-shadow: 0 8px 18px rgba(0,0,0,.35);
  letter-spacing: .2px;
}

/* =========================================================
   LABELS
   - Tamaño: --labelSize
   - Movimiento: se controla desde el HTML con style="top:.."
   ========================================================= */
.label{
  position:absolute;
  left:18%;
  right:18%;
  font:700 var(--labelSize) Arial, sans-serif; /* <-- TAMAÑO LABEL */
  color: rgba(255,255,255,.82);
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}

/* inputs: pill + blur (misma posición/alto por inline style) */
/* =========================================================
   INPUTS
   - Tamaño: --inputSize
   - Movimiento: se controla desde el HTML con style="top:.."
   ========================================================= */
input.field{
  position:absolute;
  left:18%;
  right:18%;
  height:10%;

  border: 1px solid rgba(255,255,255,.55);
  border-radius: 999px;

  box-sizing:border-box;
  background:
    linear-gradient(180deg, var(--pill) 0%, var(--pill2) 100%);

  padding: 0 14px;
  font:700 var(--inputSize) Arial, sans-serif; /* <-- TAMAÑO INPUT */
  color: rgba(30,40,55,.92);

  outline:none;

  box-shadow:
    0 10px 18px rgba(0,0,0,.22),
    inset 0 1px 0 rgba(255,255,255,.55);

  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
}

input.field::placeholder{
  color: rgba(60,70,85,.55);
}

/* botón: pill azul (misma posición/alto por inline style) */
/* =========================================================
   BOTÓN
   - Tamaño: --btnTextSize
   - Movimiento: se controla desde el HTML con style="top:.."
   ========================================================= */
.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:9%;

  border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px;

  box-sizing:border-box;

  background:
    radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.22), transparent 60%),
    linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);

  box-shadow:
    0 18px 26px rgba(0,0,0,.28),
    inset 0 1px 0 rgba(255,255,255,.22);

  display:flex;
  align-items:center;
  justify-content:center;

  font:700 var(--btnTextSize) Arial, sans-serif; /* <-- TAMAÑO TEXTO BOTÓN */
  color: rgba(255,255,255,.92);

  cursor:pointer;
  user-select:none;

  transition: transform .12s ease, filter .12s ease;
}

.btn:active{
  transform: scale(.985);
  filter: brightness(.98);
}

/* links inferiores: mismo layout (solo color) */
/* =========================================================
   LINKS
   - Tamaño: --linkSize
   - Movimiento: se controla desde el HTML con style="top/left"
   ========================================================= */
.link{
  position:absolute;
  font:700 var(--linkSize) Arial, sans-serif; /* <-- TAMAÑO LINKS */
  color: rgba(255,255,255,.70);
  white-space:nowrap;
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}

.link:hover{
  color: rgba(255,255,255,.85);
}

/* HUD: mantener, solo estética (sin imprimir medidas) */
#hud{
  position:absolute; top:8px; left:8px;
  font:12px Arial, sans-serif;
  background: rgba(255,255,255,.10);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 10px;
  padding: 6px 10px;
  white-space:nowrap;
  pointer-events:none;
  color: rgba(255,255,255,.70);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 10px 18px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.14);
}
</style>
</head>

<body>
<div id="stage">
  <div id="frame"></div>

  <div id="plan">
    <div id="card">
      <!-- LOGO: encima y centrado del título -->
      <img class="logo" src="https://files.catbox.moe/056m6v.jpg" alt="Logo"/>

      <div class="title">¡BIENVENIDO!</div>

      <div class="label" style="top:22%;">Usuario:</div>
      <input id="user" class="field" style="top:28%;" autocomplete="username"/>

      <div class="label" style="top:42%;">Contraseña:</div>
      <input id="pass" class="field" style="top:48%;" type="password" autocomplete="current-password"/>

      <div class="btn" style="top:67%;" onclick="doLogin()">Login</div>

      <div class="link" style="top:78%; left:20%;">Politicas:</div>
      <div class="link" style="top:78%; left:68%;">Registrarse:</div>
    </div>

    <!-- HUD ya NO imprime medidas -->
    <div id="hud"></div>
  </div>
</div>

<script>
async function doLogin(){
  const u = (document.getElementById("user").value || "").trim();
  const p = (document.getElementById("pass").value || "").trim();

  try{
    const r = await fetch("https://camilo27.pythonanywhere.com/api/auth", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({usuario:u, password:p})
    });

    const j = await r.json();

    if (j && j.ok === true){
      // IMPORTANTE: no usar window.top (sandbox lo bloquea)
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

  /* =========================================================
     Se eliminó la impresión de medidas:
     - Antes: hud.textContent = "Viewport... | Plan..."
     - Ahora: no imprime nada
     ========================================================= */
})();
</script>

</body>
</html>
"""

components.html(html, height=10, scrolling=False)
