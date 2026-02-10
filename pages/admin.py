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
/* ====== BASE ====== */
html, body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  overflow:hidden;
  background:#070606;
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}

/* =========================================================
   AJUSTE RÁPIDO DE TAMAÑOS (EDITA SOLO ESTO)
   - title: “Welcome” / “¡BIENVENIDO!”
   - label: “Usuario / Contraseña”
   - input: texto dentro de inputs
   - btn: texto del botón
   - link: “Politicas / Registrarse”
   ========================================================= */
:root{
  --fs-title: 28px;   /* (móvil/tablet) */
  --fs-label: 12px;
  --fs-input: 14px;
  --fs-btn:   14px;
  --fs-link:  12px;

  /* SOLO PANTALLA COMPUTADOR (>=1024px) */
  --fs-title-desktop: 44px;
  --fs-label-desktop: 16px;
  --fs-input-desktop: 18px;
  --fs-btn-desktop:   18px;
  --fs-link-desktop:  14px;
}

/* ====== LUX RED / VINOTINTO BACKGROUND ====== */
#stage{
  position:fixed;
  inset:0;
  width:100vw;
  height:100vh;
  overflow:hidden;

  /* base rojo/vinotinto + profundidad */
  background:
    radial-gradient(1200px 700px at 50% 10%,
      rgba(255,255,255,0.16) 0%,
      rgba(255,255,255,0.05) 34%,
      rgba(0,0,0,0.00) 62%),
    linear-gradient(180deg,
      #ff8a80 0%,
      #d12b2b 30%,
      #7b0a10 66%,
      #240005 100%);
}

/* ====== EFECTO “LUJO”: BRILLO GRIS/PLATA ENTRE MATICES ======
   La imagen tiene un reflejo diagonal tipo vidrio + brillo “plata”
   que cae sobre el rojo (no es blanco puro, es gris cálido).
*/
#stage::before{
  content:"";
  position:absolute;
  inset:-45%;
  transform: rotate(-12deg);
  pointer-events:none;

  /* Capa 1: reflejo diagonal “glass” */
  background:
    linear-gradient(135deg,
      rgba(235,235,235,0.48) 0%,
      rgba(235,235,235,0.26) 18%,
      rgba(235,235,235,0.12) 34%,
      rgba(235,235,235,0.04) 48%,
      rgba(0,0,0,0.10) 100%);
  filter: blur(1.35px);
  mix-blend-mode: screen;
  opacity: 0.92;
}

/* Capa 2: highlight “specular” gris suave + viñeta para lujo */
#stage::after{
  content:"";
  position:absolute;
  inset:-12%;
  pointer-events:none;

  background:
    /* brillo gris/plata central (aire lujo) */
    radial-gradient(520px 300px at 50% 14%,
      rgba(230,230,230,0.22) 0%,
      rgba(230,230,230,0.10) 26%,
      rgba(230,230,230,0.00) 60%),
    /* micro-reflejo lateral (similar a “glass edge”) */
    radial-gradient(420px 240px at 82% 26%,
      rgba(235,235,235,0.10) 0%,
      rgba(235,235,235,0.00) 62%),
    /* viñeta (profundidad) */
    radial-gradient(circle at 50% 10%,
      rgba(255,255,255,0.06) 0%,
      rgba(0,0,0,0.22) 56%,
      rgba(0,0,0,0.58) 100%);
}

/* ====== FRAME (solo visual) ====== */
#frame{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  box-sizing:border-box;
  pointer-events:none;
}

/* ====== LAYOUT (MISMA ESTRUCTURA / POSICIONES) ====== */
#plan{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  overflow:hidden;
}

#card{
  position:absolute;
  left:6%;
  right:6%;
  top:6%;
  bottom:6%;
}

/* ====== TITLE ====== */
.title{
  position:absolute;
  left:0; right:0;
  top:12%;
  text-align:center;

  font-size: var(--fs-title);
  line-height:1.05;
  font-weight:900;
  letter-spacing:0.4px;

  color: rgba(255,255,255,0.97);
  text-shadow:
    0 10px 26px rgba(0,0,0,0.35),
    0 2px 8px rgba(0,0,0,0.25);
}

/* ====== LABELS ====== */
.label{
  position:absolute;
  left:18%;
  right:18%;
  font-size: var(--fs-label);
  font-weight:800;
  letter-spacing:0.2px;
  color: rgba(255,255,255,0.72);
  text-shadow: 0 8px 18px rgba(0,0,0,0.28);
}

/* ====== INPUTS ====== */
input.field{
  position:absolute;
  left:18%;
  right:18%;
  height:10%;

  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 999px;
  box-sizing:border-box;

  background: rgba(255,255,255,0.86);
  box-shadow:
    0 14px 28px rgba(0,0,0,0.20),
    inset 0 1px 0 rgba(255,255,255,0.55);

  padding: 0 16px;

  font-size: var(--fs-input);
  font-weight:800;
  color:#2b0b0b;
  outline:none;
}

input.field::placeholder{
  color: rgba(43,11,11,0.45);
}

input.field:focus{
  box-shadow:
    0 16px 34px rgba(0,0,0,0.22),
    0 0 0 3px rgba(230,230,230,0.18),
    inset 0 1px 0 rgba(255,255,255,0.62);
}

/* ====== BUTTON ====== */
.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:9%;

  border: 1px solid rgba(255,255,255,0.16);
  border-radius: 999px;
  box-sizing:border-box;

  background:
    radial-gradient(140px 90px at 50% 25%,
      rgba(235,235,235,0.18) 0%,
      rgba(235,235,235,0.00) 60%),
    linear-gradient(180deg,
      #ff5a4a 0%,
      #e12822 48%,
      #b30c10 100%);

  box-shadow:
    0 18px 34px rgba(0,0,0,0.26),
    inset 0 1px 0 rgba(255,255,255,0.24);

  display:flex;
  align-items:center;
  justify-content:center;

  font-size: var(--fs-btn);
  font-weight:900;
  letter-spacing:0.25px;

  color: rgba(255,255,255,0.97);
  cursor:pointer;
  user-select:none;
  text-shadow: 0 10px 22px rgba(0,0,0,0.35);
}

.btn:hover{ filter: brightness(1.03); }
.btn:active{ transform: translateY(1px); filter: brightness(0.99); }

/* ====== LINKS ====== */
.link{
  position:absolute;
  font-size: var(--fs-link);
  font-weight:800;
  color: rgba(255,255,255,0.78);
  white-space:nowrap;
  text-shadow: 0 10px 22px rgba(0,0,0,0.30);
  opacity:0.92;
}

/* HUD discreto */
#hud{
  position:absolute; top:8px; left:8px;
  font:12px Arial, sans-serif;
  background: rgba(0,0,0,0.16);
  border:1px solid rgba(255,255,255,0.14);
  border-radius:10px;
  padding:6px 10px;
  white-space:nowrap;
  pointer-events:none;
  color: rgba(255,255,255,0.78);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* ====== SOLO PANTALLA COMPUTADOR ====== */
@media (min-width: 1024px){
  .title{font-size: var(--fs-title-desktop);}
  .label{font-size: var(--fs-label-desktop);}
  input.field{font-size: var(--fs-input-desktop);}
  .btn{font-size: var(--fs-btn-desktop);}
  .link{font-size: var(--fs-link-desktop);}
}

/* móviles */
@media (max-width: 420px){
  .title{font-size: var(--fs-title);}
  input.field{font-size: var(--fs-input);}
  .btn{font-size: var(--fs-btn);}
}
</style>
</head>

<body>
<div id="stage">
  <div id="frame"></div>

  <div id="plan">
    <div id="card">
      <div class="title">¡BIENVENIDO!</div>

      <div class="label" style="top:22%;">Usuario:</div>
      <input id="user" class="field" style="top:28%;" autocomplete="username"/>

      <div class="label" style="top:42%;">Contraseña:</div>
      <input id="pass" class="field" style="top:48%;" type="password" autocomplete="current-password"/>

      <div class="btn" style="top:67%;" onclick="doLogin()">Login</div>

      <div class="link" style="top:78%; left:20%;">Politicas:</div>
      <div class="link" style="top:78%; left:68%;">Registrarse:</div>
    </div>

    <div id="hud">Cargando...</div>
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

  var hud=document.getElementById("hud");
  var plan=document.getElementById("plan");
  function update(){
    var r=plan.getBoundingClientRect();
    hud.textContent="Viewport(px): "+Math.round(window.innerWidth)+" x "+Math.round(window.innerHeight)+
                    " | Plan(px): "+Math.round(r.width)+" x "+Math.round(r.height);
  }
  window.addEventListener("resize", update);
  update();
})();
</script>

</body>
</html>
"""

components.html(html, height=10, scrolling=False)
