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
body{margin:0;background:#fff;font-family:Arial;}
.wrap{
position:fixed;inset:0;
display:flex;flex-direction:column;
align-items:center;justify-content:center;
gap:12px;
}
input{
width:260px;padding:10px;
border:2px solid #000;border-radius:8px;
font-size:14px;
}
button{
width:200px;padding:10px;
border:2px solid #000;border-radius:8px;
background:#fff;font-weight:bold;
cursor:pointer;
}
#msg{font-size:13px;color:red;height:18px;}
</style>
</head>

<body>
<div class="wrap">
<h2>¡BIENVENIDO!</h2>

<input id="user" placeholder="Usuario"/>
<input id="pass" type="password" placeholder="Contraseña"/>

<button onclick="login()">Login</button>
<div id="msg"></div>
</div>

<script>
async function login(){
const u=document.getElementById("user").value;
const p=document.getElementById("pass").value;
const msg=document.getElementById("msg");
msg.textContent="Validando...";

try{
const r=await fetch("https://camilo27.pythonanywhere.com/api/auth",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({usuario:u,password:p})
});

const j=await r.json();

if(j.ok===true){
window.location.href="/?auth=ok";
}else{
msg.textContent="Credenciales inválidas";
}

}catch(e){
msg.textContent="Error de conexión";
}
}
</script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
