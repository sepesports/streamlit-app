# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown("""
<style>
.block-container{padding:0!important;margin:0!important;max-width:100%!important;}
section.main > div{padding:0!important;margin:0!important;}
header, footer{display:none!important;}
</style>
""", unsafe_allow_html=True)

html = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
html,body{
  margin:0;
  padding:0;
  width:100%;
  height:100%;
  background:#fff;
  overflow:hidden;
}

#frame{
  position:fixed;
  inset:10px 10px 0 10px;
  border-left:2px solid #111;
  border-right:2px solid #111;
  border-top:2px solid #111;
  box-sizing:border-box;
}

#plan{
  position:absolute;
  inset:0;
  font-family:Arial,sans-serif;
}

/* Título */
.title{
  position:absolute;
  top:12%;
  left:0;
  right:0;
  text-align:center;
  font-weight:800;
  font-size:18px;
}

/* Labels */
.label{
  position:absolute;
  left:18%;
  right:18%;
  font-weight:700;
  font-size:14px;
}

/* Inputs */
.field{
  position:absolute;
  left:18%;
  right:18%;
  height:10%;
  border:2px solid #000;
  border-radius:10px;
  background:#fff;
  box-sizing:border-box;
}

/* Botón */
.btn{
  position:absolute;
  left:32%;
  right:32%;
  height:9%;
  border:2px solid #000;
  border-radius:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:700;
  font-size:14px;
}

/* Links */
.link{
  position:absolute;
  font-weight:700;
  font-size:13px;
}

/* Posiciones */
#u_label{top:22%;}
#u_input{top:28%;}

#p_label{top:42%;}
#p_input{top:48%;}

#login{top:67%;}

#pol{top:78%; left:20%;}
#reg{top:78%; left:68%;}
</style>
</head>

<body>
<div id="frame">
  <div id="plan">

    <div class="title">¡BIENVENIDO!</div>

    <div id="u_label" class="label">Usuario:</div>
    <div id="u_input" class="field"></div>

    <div id="p_label" class="label">Contraseña:</div>
    <div id="p_input" class="field"></div>

    <div id="login" class="btn">Login</div>

    <div id="pol" class="link">Politicas:</div>
    <div id="reg" class="link">Registrarse:</div>

  </div>
</div>
</body>
</html>
"""

components.html(html, height=1000, scrolling=False)
