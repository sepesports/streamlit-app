# admin.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
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
html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#fff;}
#stage{position:fixed;inset:0;width:100vw;height:100vh;background:#fff;}

.wrap{
position:absolute;
left:18%; right:18%;
top:20%;
font-family:Arial;
}

.title{
text-align:center;
font-size:20px;
font-weight:800;
margin-bottom:20px;
}

.field{
width:100%;
padding:12px;
border:2px solid #000;
border-radius:10px;
box-sizing:border-box;
font-size:14px;
margin-bottom:18px;
}

.btn{
width:36%;
margin:0 auto;
padding:12px;
border:2px solid #000;
border-radius:10px;
background:#fff;
font-weight:700;
cursor:pointer;
text-align:center;
}

.msg{
text-align:center;
margin-top:12px;
font-size:13px;
color:red;
}
</style>
</head>

<body>
<div id="stage">

<div class="wrap">

<div class="title">¡BIENVENIDO!</div>

<input id="user" class="field" placeholder="Usuario">
<input id="pass" class="field" type="password" placeholder="Contraseña">

<div class="btn" onclick="login()">Login</div>

<div id="msg" class="msg"></div>

</div>

</div>

<script>
async function login(){

const u = document.getElementById("user").value.trim();
const p = document.getElementById("pass").value.trim();
const msg = document.getElementById("msg");

msg.textContent = "Validando...";

try{

const r = await fetch("https://camilo27.pythonanywhere.com/api/auth",{
method:"POST",
headers:{"Content-Type":"application/json"},
body: JSON.stringify({
usuario: u,
password: p
})
});

const j = await r.json();

if(j.ok === true){
window.location.href = "/?auth=ok";
}else{
msg.textContent = "Credenciales inválidas";
}

}catch(e){
msg.textContent = "Error de conexión";
}

}
</script>

</body>
</html>
"""

components.html(html, height=10, scrolling=False)
