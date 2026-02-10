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
html, body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#fff;}
#stage{position:fixed;inset:0;width:100vw;height:100vh;background:#fff;}

#frame{
  position:absolute;
  left:10px; right:10px;
  top:10px; bottom:0;
  border-left:2px solid #111;
  border-right:2px solid #111;
  border-top:2px solid #111;
  box-sizing:border-box;
  pointer-events:none;
}

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

.title{
  position:absolute;
  left:0; right:0;
  top:12%;
  text-align:center;
  font:18px Arial, sans-serif;
  font-weight:800;
  color:#000;
}

.label{
  position:absolute;
  left:18%;
  right:18%;
  font:14px Arial, sans-serif;
  font-weight:700;
  color:#000;
}

input.field{
  position:absolute;
  left:18%;
  right:18%;
  height:10%;
  border:2px solid #000;
  border-radius:10px;
  box-sizing:border-box;
  background:#fff;
  padding: 0 12px;
  font:14px Arial, sans-serif;
  font-weight:700;
  color:#000;
  outline:none;
}

.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:9%;
  border:2px solid #000;
  border-radius:10px;
  box-sizing:border-box;
  background:#fff;
  display:flex;
  align-items:center;
  justify-content:center;
  font:14px Arial, sans-serif;
  font-weight:700;
  color:#000;
  cursor:pointer;
  user-select:none;
}

.link{
  position:absolute;
  font:13px Arial, sans-serif;
  font-weight:700;
  color:#000;
  white-space:nowrap;
}

#hud{
  position:absolute; top:8px; left:8px;
  font:12px Arial, sans-serif;
  background: rgba(255,255,255,.92);
  border:1px solid rgba(0,0,0,.2);
  border-radius:6px;
  padding:6px 10px;
  white-space:nowrap;
  pointer-events:none;
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
