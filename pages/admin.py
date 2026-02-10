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
  --bgTop: #e06b6a;
  --bgMid: #b53a33;
  --bgDeep:#3b0707;

  --overlay1: rgba(120, 0, 0, .42);
  --overlay2: rgba(20, 0, 0, .55);

  --ink: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.62);

  --pill: rgba(238, 245, 255, .92);
  --pill2: rgba(255,255,255,.86);

  --btn1:#ff4f4a;
  --btn2:#ff3a33;

  --shadow1: 0 22px 55px rgba(0,0,0,.55);
  --shadow2: 0 10px 22px rgba(0,0,0,.40);

  --blur: 14px;
}

*{box-sizing:border-box}
html, body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  overflow:hidden;
  background:#07070b;
}

#stage{
  position:fixed;
  inset:0;
  width:100vw;
  height:100vh;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.18), transparent 60%),
    radial-gradient(900px 700px at 20% 120%, rgba(255,0,0,.12), transparent 60%),
    linear-gradient(180deg, #101018 0%, #07070b 100%);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* Fondo rojo + corte diagonal + viñeta (sin cambiar layout) */
#plan{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  overflow:hidden;

  border-radius: 34px;
  box-shadow: var(--shadow1);
  background:
    linear-gradient(180deg, rgba(255,255,255,.22) 0%, transparent 22%),
    linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #7b1b19 58%, var(--bgDeep) 100%);
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

/* textos: solo visual */
.title{
  position:absolute;
  left:0; right:0;
  top:12%;
  text-align:center;
  font:18px Arial, sans-serif;
  font-weight:800;
  color: var(--ink);
  text-shadow: 0 8px 18px rgba(0,0,0,.35);
  letter-spacing: .2px;
}

.label{
  position:absolute;
  left:18%;
  right:18%;
  font:14px Arial, sans-serif;
  font-weight:700;
  color: rgba(255,255,255,.82);
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}

/* inputs: pill + blur (misma posición/alto por inline style) */
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
  font:14px Arial, sans-serif;
  font-weight:700;
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

/* botón: pill rojo (misma posición/alto por inline style) */
.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:9%;

  border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px;

  box-sizing:border-box;

  background:
    radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.26), transparent 60%),
    linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);

  box-shadow:
    0 18px 26px rgba(0,0,0,.28),
    inset 0 1px 0 rgba(255,255,255,.22);

  display:flex;
  align-items:center;
  justify-content:center;

  font:14px Arial, sans-serif;
  font-weight:700;
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
.link{
  position:absolute;
  font:13px Arial, sans-serif;
  font-weight:700;
  color: rgba(255,255,255,.70);
  white-space:nowrap;
  text-shadow: 0 6px 14px rgba(0,0,0,.30);
}

.link:hover{
  color: rgba(255,255,255,.85);
}

/* HUD: mantener, solo estética */
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
