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
/* ====== BASE / STAGE ====== */
html, body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  overflow:hidden;
  background:#0b0b0b;
  font-family: Arial, sans-serif;
}

#stage{
  position:fixed;
  inset:0;
  width:100vw;
  height:100vh;
  overflow:hidden;
  background: linear-gradient(180deg, #ff8b7a 0%, #d84a3a 28%, #7b0f10 100%);
}

/* difuminado diagonal como la referencia */
#stage::before{
  content:"";
  position:absolute;
  inset:-25% -25%;
  background:
    linear-gradient(135deg,
      rgba(255,255,255,0.22) 0%,
      rgba(255,255,255,0.14) 35%,
      rgba(255,255,255,0.00) 62%,
      rgba(0,0,0,0.10) 100%);
  transform: rotate(-12deg);
  filter: blur(1px);
  pointer-events:none;
}

/* viñeta suave */
#stage::after{
  content:"";
  position:absolute;
  inset:-10%;
  background: radial-gradient(circle at 50% 10%, rgba(255,255,255,0.10) 0%, rgba(0,0,0,0.40) 55%, rgba(0,0,0,0.65) 100%);
  pointer-events:none;
}

/* marco (solo visual) */
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

/* contenedor */
#plan{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  overflow:hidden;
}

/* card */
#card{
  position:absolute;
  left:6%;
  right:6%;
  top:6%;
  bottom:6%;
}

/* ====== TYPO ====== */
.title{
  position:absolute;
  left:0; right:0;
  top:12%;
  text-align:center;
  font: 22px Arial, sans-serif;
  font-weight:900;
  letter-spacing:0.3px;
  color: rgba(255,255,255,0.96);
  text-shadow: 0 6px 18px rgba(0,0,0,0.35);
}

.label{
  position:absolute;
  left:18%;
  right:18%;
  font:12px Arial, sans-serif;
  font-weight:700;
  color: rgba(255,255,255,0.86);
  text-shadow: 0 4px 14px rgba(0,0,0,0.28);
}

/* ====== FIELDS (píldoras claras) ====== */
input.field{
  position:absolute;
  left:18%;
  right:18%;
  height:10%;
  border: 0;
  border-radius: 999px;
  box-sizing:border-box;
  background: rgba(255,255,255,0.84);
  box-shadow:
    0 10px 22px rgba(0,0,0,0.18),
    inset 0 1px 0 rgba(255,255,255,0.55);
  padding: 0 16px;
  font:14px Arial, sans-serif;
  font-weight:800;
  color:#2a0c0c;
  outline:none;
}

input.field::placeholder{
  color: rgba(42,12,12,0.45);
}

input.field:focus{
  box-shadow:
    0 12px 26px rgba(0,0,0,0.20),
    0 0 0 3px rgba(255,255,255,0.25),
    inset 0 1px 0 rgba(255,255,255,0.60);
}

/* ====== BUTTON (rojo intenso) ====== */
.btn{
  position:absolute;
  left:24%;
  right:24%;
  height:9%;
  border: 0;
  border-radius: 999px;
  box-sizing:border-box;
  background: linear-gradient(180deg, #ff4a3a 0%, #e02b22 55%, #c81915 100%);
  box-shadow:
    0 14px 28px rgba(0,0,0,0.24),
    inset 0 1px 0 rgba(255,255,255,0.28);
  display:flex;
  align-items:center;
  justify-content:center;
  font:14px Arial, sans-serif;
  font-weight:900;
  letter-spacing:0.2px;
  color: rgba(255,255,255,0.96);
  cursor:pointer;
  user-select:none;
  text-shadow: 0 6px 16px rgba(0,0,0,0.35);
}

.btn:hover{
  filter: brightness(1.03);
}

.btn:active{
  transform: translateY(1px);
  filter: brightness(0.99);
}

/* ====== LINKS ====== */
.link{
  position:absolute;
  font:12px Arial, sans-serif;
  font-weight:800;
  color: rgba(255,255,255,0.86);
  white-space:nowrap;
  text-shadow: 0 6px 16px rgba(0,0,0,0.32);
  opacity:0.92;
}

/* HUD discreto */
#hud{
  position:absolute; top:10px; left:10px;
  font:11px Arial, sans-serif;
  background: rgba(0,0,0,0.18);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 10px;
  padding: 6px 10px;
  color: rgba(255,255,255,0.78);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  white-space:nowrap;
  pointer-events:none;
}

/* Responsivo fino (sin mover posiciones) */
@media (max-width: 420px){
  .title{font-size:20px;}
  input.field{font-size:14px;}
  .btn{font-size:14px;}
  .label,.link{font-size:12px;}
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
