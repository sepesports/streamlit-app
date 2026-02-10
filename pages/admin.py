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
/* =========================
   TAMAÑOS DE TEXTO (EDITA SOLO ESTO)
   ========================= */
:root{
  --fs-title: 34px;      /* título móvil/tablet */
  --fs-label: 12px;      /* labels móvil/tablet */
  --fs-input: 14px;      /* texto input móvil/tablet */
  --fs-btn:   14px;      /* texto botón móvil/tablet */
  --fs-link:  12px;      /* links móvil/tablet */

  --fs-title-desktop: 54px; /* título SOLO computador */
  --fs-label-desktop: 16px;
  --fs-input-desktop: 18px;
  --fs-btn-desktop:   18px;
  --fs-link-desktop:  14px;

  /* =========================
     PALETA / EFECTOS (TU CSS)
     ========================= */
  --bgTop: #e06b6a;
  --bgMid: #b53a33;
  --bgDeep:#3b0707;

  --overlay1: rgba(120, 0, 0, .42);
  --overlay2: rgba(20, 0, 0, .55);

  --white: #ffffff;
  --ink: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.62);

  --pill: rgba(238, 245, 255, .92);
  --pill2: rgba(255,255,255,.86);

  --btn1:#ff4f4a;
  --btn2:#ff3a33;

  --shadow1: 0 22px 55px rgba(0,0,0,.55);
  --shadow2: 0 10px 22px rgba(0,0,0,.40);
  --inner: inset 0 1px 0 rgba(255,255,255,.22);
  --blur: 14px;
  --radius: 34px;
}

*{ box-sizing:border-box; }
html,body{ height:100%; }

html, body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  overflow:hidden;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* =========================
   FONDO GENERAL (como tu body)
   ========================= */
#stage{
  position:fixed;
  inset:0;
  width:100vw;
  height:100vh;
  overflow:hidden;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.18), transparent 60%),
    radial-gradient(900px 700px at 20% 120%, rgba(255,0,0,.12), transparent 60%),
    linear-gradient(180deg, #101018 0%, #07070b 100%);
}

/* =========================
   “PHONE” (marco) usando #plan
   NO CAMBIA ESTRUCTURA, SOLO ESTILO
   ========================= */
#plan{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;

  /* centrado tipo phone sin alterar lógica */
  display:flex;
  align-items:center;
  justify-content:center;

  overflow:hidden;
}

/* el marco visible */
#frame{
  position:absolute;
  width:min(390px, 92vw);
  aspect-ratio: 9 / 19.5;
  border-radius: 42px;
  padding:14px;
  background: rgba(255,255,255,.06);
  box-shadow: 0 30px 90px rgba(0,0,0,.70);
  border: 1px solid rgba(255,255,255,.10);
  overflow:hidden;
  pointer-events:none;
}

/* brillo del marco */
#frame::before{
  content:"";
  position:absolute; inset:-2px;
  border-radius:44px;
  background:
    radial-gradient(220px 160px at 35% 0%, rgba(255,255,255,.18), transparent 60%),
    linear-gradient(135deg, rgba(255,255,255,.10), transparent 45%);
  mix-blend-mode: screen;
  pointer-events:none;
}

/* borde interno oscuro */
#frame::after{
  content:"";
  position:absolute; inset:0;
  border-radius:42px;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,.55);
  pointer-events:none;
}

/* =========================
   “SCREEN” (pantalla) usando #card
   ========================= */
#card{
  position:relative;
  width:min(390px, 92vw);
  aspect-ratio: 9 / 19.5;
  border-radius: var(--radius);
  overflow:hidden;
  box-shadow: var(--shadow1);

  /* tu gradiente de pantalla */
  background:
    linear-gradient(180deg, rgba(255,255,255,.22) 0%, transparent 22%),
    linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #7b1b19 58%, var(--bgDeep) 100%);
}

/* overlay diagonal (tu screen::before) */
#card::before{
  content:"";
  position:absolute; inset:-10%;
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

/* brillo/vineta (tu screen::after) */
#card::after{
  content:"";
  position:absolute; inset:0;
  background:
    radial-gradient(80% 70% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
    radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
    linear-gradient(180deg, transparent 55%, rgba(0,0,0,.65) 100%);
  pointer-events:none;
}

/* =========================
   TEXTO / CAMPOS (misma ubicación absoluta)
   ========================= */
.title{
  position:absolute;
  left:0; right:0;
  top:12%;
  text-align:center;
  margin:0;

  color: var(--ink);
  font-size: var(--fs-title);
  font-weight:800;
  text-shadow: 0 8px 18px rgba(0,0,0,.35);
}

.label{
  position:absolute;
  left:18%;
  right:18%;
  font-size: var(--fs-label);
  font-weight:800;
  color: rgba(255,255,255,.62);
  text-shadow: 0 6px 14px rgba(0,0,0,.28);
}

/* inputs (equivalente a .pill) */
input.field{
  position:absolute;
  left:18%;
  right:18%;
  height:44px;                 /* fijo como tu .pill */
  border-radius:999px;
  border:1px solid rgba(255,255,255,.55);
  background:
    linear-gradient(180deg, var(--pill) 0%, var(--pill2) 100%);
  box-shadow:
    0 10px 18px rgba(0,0,0,.22),
    inset 0 1px 0 rgba(255,255,255,.55);
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));

  padding:0 16px;
  outline:none;

  font-size: var(--fs-input);
  color: rgba(30,40,55,.92);
  font-weight:700;
}

input.field::placeholder{
  color: rgba(60,70,85,.55);
}

input.field:focus{
  box-shadow:
    0 12px 22px rgba(0,0,0,.26),
    inset 0 1px 0 rgba(255,255,255,.60);
}

/* botón (tu .btn) */
.btn{
  position:absolute;
  left:18%;
  right:18%;
  height:52px;                 /* como tu .btn */
  border-radius:999px;
  border:1px solid rgba(255,255,255,.18);
  background:
    radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.26), transparent 60%),
    linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
  box-shadow:
    0 18px 26px rgba(0,0,0,.28),
    inset 0 1px 0 rgba(255,255,255,.22);

  display:flex;
  align-items:center;
  justify-content:center;

  color:#fff;
  font-weight:700;
  font-size: var(--fs-btn);
  cursor:pointer;
  transition: transform .12s ease, filter .12s ease;
  user-select:none;
}

.btn:active{
  transform: scale(.985);
  filter: brightness(.98);
}

/* texto inferior (small) */
.link{
  position:absolute;
  font-size: var(--fs-link);
  color: rgba(255,255,255,.55);
  font-weight:700;
  text-shadow: 0 6px 14px rgba(0,0,0,.28);
}

.link.link-accent{
  color: rgba(255,80,70,.75);
  font-weight:800;
}

/* HUD (dejar igual, solo visual) */
#hud{
  position:absolute; top:10px; left:10px;
  font:11px Arial, sans-serif;
  background: rgba(0,0,0,.18);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 10px;
  padding: 6px 10px;
  color: rgba(255,255,255,.78);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  white-space:nowrap;
  pointer-events:none;
}

/* SOLO PANTALLA COMPUTADOR */
@media (min-width: 1024px){
  .title{ font-size: var(--fs-title-desktop); }
  .label{ font-size: var(--fs-label-desktop); }
  input.field{ font-size: var(--fs-input-desktop); }
  .btn{ font-size: var(--fs-btn-desktop); }
  .link{ font-size: var(--fs-link-desktop); }
}
</style>
</head>

<body>
<div id="stage">
  <div id="frame"></div>

  <div id="plan">
    <div id="card">
      <div class="title">Welcome</div>

      <div class="label" style="top:22%;">Usuario:</div>
      <input id="user" class="field" style="top:28%;" autocomplete="username" placeholder=""/>

      <div class="label" style="top:42%;">Contraseña:</div>
      <input id="pass" class="field" style="top:48%;" type="password" autocomplete="current-password" placeholder=""/>

      <div class="btn" style="top:67%;" onclick="doLogin()">Login</div>

      <div class="link" style="top:78%; left:20%;">Politicas:</div>
      <div class="link link-accent" style="top:78%; left:68%;">Registrarse:</div>

      <div id="hud">Cargando...</div>
    </div>
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
  var card=document.getElementById("card");
  function update(){
    var r=card.getBoundingClientRect();
    hud.textContent="Viewport(px): "+Math.round(window.innerWidth)+" x "+Math.round(window.innerHeight)+
                    " | Card(px): "+Math.round(r.width)+" x "+Math.round(r.height);
  }
  window.addEventListener("resize", update);
  update();
})();
</script>

</body>
</html>
"""

components.html(html, height=10, scrolling=False)
