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

/* ====== LUX RED BACKGROUND ====== */
#stage{
  position:fixed;
  inset:0;
  width:100vw;
  height:100vh;
  background:
    radial-gradient(1200px 700px at 50% 10%, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.06) 32%, rgba(0,0,0,0) 60%),
    linear-gradient(180deg, #ff8a80 0%, #d12b2b 32%, #7b0a10 70%, #2a0004 100%);
  overflow:hidden;
}

/* brillo diagonal tipo “glass” (más notorio) */
#stage::before{
  content:"";
  position:absolute;
  inset:-40%;
  background:
    linear-gradient(135deg,
      rgba(255,255,255,0.42) 0%,
      rgba(255,255,255,0.24) 22%,
      rgba(255,255,255,0.10) 38%,
      rgba(255,255,255,0.02) 52%,
      rgba(0,0,0,0.10) 100%);
  transform: rotate(-12deg);
  filter: blur(1.4px);
  pointer-events:none;
}

/* “specular highlight” adicional (aire lujo) */
#stage::after{
  content:"";
  position:absolute;
  inset:-10%;
  background:
    radial-gradient(520px 300px at 50% 14%, rgba(255,255,255,0.20) 0%, rgba(255,255,255,0.08) 28%, rgba(255,255,255,0.00) 58%),
    radial-gradient(circle at 50% 8%,
      rgba(255,255,255,0.08) 0%,
      rgba(0,0,0,0.22) 55%,
      rgba(0,0,0,0.55) 100%);
  pointer-events:none;
}

/* ====== FRAME (solo visual) ====== */
#frame{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  border-left:0;
  border-right:0;
  border-top:0;
  box-sizing:border-box;
  pointer-events:none;
}

/* ====== LAYOUT (NO CAMBIAR POSICIONES) ====== */
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
  font-size:28px;
  line-height:1.05;
  font-weight:900;
  letter-spacing:0.4px;
  color: rgba(255,255,255,0.97);
  text-shadow:
    0 10px 26px rgba(0,0,0,0.35),
    0 2px 8px rgba(0,0,0,0.25);
}

/* Labels discretos */
.label{
  position:absolute;
  left:18%;
  right:18%;
  font-size:12px;
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
  font-size:14px;
  font-weight:800;
  color:#2b0b0b;
  outline:none;
}

input.field::placeholder{ color: rgba(43,11,11,0.45); }

input.field:focus{
  box-shadow:
    0 16px 34px rgba(0,0,0,0.22),
    0 0 0 3px rgba(255,255,255,0.18),
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
    radial-gradient(140px 90px at 50% 25%, rgba(255,255,255,0.22) 0%, rgba(255,255,255,0) 60%),
    linear-gradient(180deg, #ff5a4a 0%, #e12822 48%, #b30c10 100%);
  box-shadow:
    0 18px 34px rgba(0,0,0,0.26),
    inset 0 1px 0 rgba(255,255,255,0.24);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:14px;
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
  font-size:12px;
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

/* ====== SOLO PANTALLA COMPUTADOR: SUBIR TAMAÑOS ====== */
@media (min-width: 1024px){
  .title{font-size:44px;}
  .label{font-size:16px;}
  input.field{font-size:18px;}
  .btn{font-size:18px;}
  .link{font-size:14px;}
}

/* móviles: se mantiene como estaba (no tocar layout) */
@media (max-width: 420px){
  .title{font-size:26px;}
  input.field{font-size:14px;}
  .btn{font-size:14px;}
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
