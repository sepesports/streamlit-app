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
  /* ===== PALETA AZUL (basada en el logo) ===== */
  --bgTop: #0f3f8f;
  --bgMid: #0b2e6d;
  --bgDeep:#05173f;

  --overlay1: rgba(10, 40, 110, .42);
  --overlay2: rgba(0, 10, 40, .60);

  --ink: rgba(255,255,255,.92);

  --pill: rgba(238, 245, 255, .92);
  --pill2: rgba(255,255,255,.86);

  --btn1:#2f7de1;
  --btn2:#1e5fc4;

  --shadow1: 0 22px 55px rgba(0,0,0,.55);
  --blur: 14px;
}

*{box-sizing:border-box}
html, body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  overflow:hidden;
  background:#020614;
}

#stage{
  position:fixed;
  inset:0;
  width:100vw;
  height:100vh;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.18), transparent 60%),
    radial-gradient(900px 700px at 20% 120%, rgba(30,90,200,.18), transparent 60%),
    linear-gradient(180deg, #050a1c 0%, #020614 100%);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* ===== PANEL PRINCIPAL ===== */
#plan{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  overflow:hidden;

  border-radius: 34px;
  box-shadow: var(--shadow1);
  background:
    linear-gradient(180deg, rgba(255,255,255,.18) 0%, transparent 22%),
    linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #07306f 58%, var(--bgDeep) 100%);
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

/* viñeta */
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

/* marco */
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

/* contenedor */
#card{
  position:absolute;
  left:6%;
  right:6%;
  top:6%;
  bottom:6%;
}

/* ===== LOGO ===== */
/* 👉 CAMBIA width para modificar tamaño del logo */
.logo{
  position:absolute;
  top:4%;
  left:50%;
  transform:translateX(-50%);
  width:90px; /* ← TAMAÑO DEL LOGO */
}

/* ===== TÍTULO ===== */
/* 👉 CAMBIA font-size para modificar tamaño del título */
.title{
  position:absolute;
  left:0; right:0;
  top:16%;
  text-align:center;
  font:800 20px Arial, sans-serif; /* ← TAMAÑO DEL TÍTULO */
  color: var(--ink);
  text-shadow: 0 8px 18px rgba(0,0,0,.35);
}

/* ===== LABELS ===== */
/* 👉 CAMBIA font-size para modificar tamaño de labels */
.label{
  position:absolute;
  left:18%;
  right:18%;
  font:700 14px Arial, sans-serif; /* ← TAMAÑO LABEL */
  color: rgba(255,255,255,.82);
}

/* inputs */
input.field{
  position:absolute;
  left:18%;
  right:18%;
  height:10%;
  border: 1px solid rgba(255,255,255,.55);
  border-radius: 999px;
  background: linear-gradient(180deg, var(--pill) 0%, var(--pill2) 100%);
  padding: 0 14px;

  /* 👉 CAMBIA font-size para tamaño texto input */
  font:700 14px Arial, sans-serif; /* ← TAMAÑO INPUT */

  color: rgba(30,40,55,.92);
  box-shadow: 0 10px 18px rgba(0,0,0,.22),
              inset 0 1px 0 rgba(255,255,255,.55);
  backdrop-filter: blur(var(--blur));
  outline:none;
}

/* botón */
/* 👉 CAMBIA font-size para tamaño texto botón */
.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:9%;
  border-radius:999px;
  border:1px solid rgba(255,255,255,.18);
  background:
    radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.26), transparent 60%),
    linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
  display:flex;
  align-items:center;
  justify-content:center;
  font:700 14px Arial, sans-serif; /* ← TAMAÑO BOTÓN */
  color:white;
  cursor:pointer;
  box-shadow:0 18px 26px rgba(0,0,0,.28),
             inset 0 1px 0 rgba(255,255,255,.22);
}

/* links */
/* 👉 CAMBIA font-size para tamaño links */
.link{
  position:absolute;
  font:700 13px Arial, sans-serif; /* ← TAMAÑO LINKS */
  color: rgba(255,255,255,.70);
}

#hud{
  position:absolute;
  top:8px;
  left:8px;
  font:12px Arial;
  background: rgba(255,255,255,.10);
  border-radius:10px;
  padding:6px 10px;
  color: rgba(255,255,255,.70);
}
</style>
</head>

<body>
<div id="stage">
  <div id="frame"></div>

  <div id="plan">
    <div id="card">

      <img class="logo" src="https://files.catbox.moe/q2os5j.jpeg"/>

      <div class="title">¡BIENVENIDO!</div>

      <div class="label" style="top:28%;">Usuario:</div>
      <input id="user" class="field" style="top:34%;" autocomplete="username"/>

      <div class="label" style="top:48%;">Contraseña:</div>
      <input id="pass" class="field" style="top:54%;" type="password"/>

      <div class="btn" style="top:72%;" onclick="doLogin()">Login</div>

      <div class="link" style="top:82%; left:20%;">Politicas</div>
      <div class="link" style="top:82%; left:68%;">Registrarse</div>

    </div>

    <div id="hud">Cargando...</div>
  </div>
</div>

<script>
async function doLogin(){
  const u=document.getElementById("user").value.trim();
  const p=document.getElementById("pass").value.trim();
  try{
    const r=await fetch("https://camilo27.pythonanywhere.com/api/auth",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({usuario:u,password:p})
    });
    const j=await r.json();
    if(j && j.ok===true){
      window.location.href="/?auth=ok";
    }else{
      alert("Credenciales inválidas");
    }
  }catch(e){
    alert("Error de conexión");
  }
}

(function(){
  var hud=document.getElementById("hud");
  function update(){
    hud.textContent="Viewport: "+window.innerWidth+" x "+window.innerHeight;
  }
  window.addEventListener("resize",update);
  update();
})();
</script>

</body>
</html>
"""

components.html(html, height=10, scrolling=False)
