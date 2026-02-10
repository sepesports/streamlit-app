import streamlit as st
import streamlit.components.v1 as components
import requests
import json

st.set_page_config(layout="wide")

st.markdown("""
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
    </style>
    """, unsafe_allow_html=True)

# Variables de configuración
PAD_X_PX = 10
PAD_TOP_PX = 10
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"
CARD_LEFT = 6
CARD_RIGHT = 6
CARD_TOP = 6
CARD_BOTTOM = 6
TITLE_Y = 12
USER_LABEL_Y = 22
USER_INPUT_Y = 28
PASS_LABEL_Y = 42
PASS_INPUT_Y = 48
BTN_Y = 67
LINKS_Y = 78
INPUT_LEFT = 18
INPUT_RIGHT = 18
INPUT_H = 10
BTN_LEFT = 32
BTN_RIGHT = 32
BTN_H = 9
LINK_LEFT_X = 20
LINK_RIGHT_X = 68
INPUT_RADIUS_PX = 10
BTN_RADIUS_PX = 10
TITLE_SIZE_PX = 18
LABEL_SIZE_PX = 14
LINK_SIZE_PX = 13
BTN_TEXT_SIZE_PX = 14

# Estado de autenticación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Crear HTML con diseño idéntico
    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <style>
        :root{{
          --padx: {PAD_X_PX}px;
          --padtop: {PAD_TOP_PX}px;
          --b: {BORDER_PX}px;
          --bc: {BORDER_COLOR};
          --bg: {BG_COLOR};
          --r_in: {INPUT_RADIUS_PX}px;
          --r_btn: {BTN_RADIUS_PX}px;
        }}
        html, body{{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:var(--bg);}}
        #stage{{position:fixed;inset:0;width:100vw;height:100vh;background:var(--bg);}}
        #frame{{
          position:absolute;
          left:var(--padx); right:var(--padx);
          top:var(--padtop); bottom:0;
          border-left:var(--b) solid var(--bc);
          border-right:var(--b) solid var(--bc);
          border-top:var(--b) solid var(--bc);
          box-sizing:border-box;
          pointer-events:none;
          z-index:2;
        }}
        #plan{{
          position:absolute;
          left:var(--padx); right:var(--padx);
          top:var(--padtop); bottom:0;
          overflow:hidden;
          background: var(--bg);
          z-index:1;
        }}
        #card{{
          position:absolute;
          left: {CARD_LEFT}%;
          right: {CARD_RIGHT}%;
          top: {CARD_TOP}%;
          bottom: {CARD_BOTTOM}%;
        }}
        .title{{
          position:absolute;
          left:0; right:0;
          top: {TITLE_Y}%;
          text-align:center;
          font: {TITLE_SIZE_PX}px Arial, sans-serif;
          font-weight: 800;
          color:#000;
        }}
        .label{{
          position:absolute;
          left: {INPUT_LEFT}%;
          right: {INPUT_RIGHT}%;
          font: {LABEL_SIZE_PX}px Arial, sans-serif;
          font-weight: 700;
          color:#000;
        }}
        .link{{
          position:absolute;
          font: {LINK_SIZE_PX}px Arial, sans-serif;
          font-weight: 700;
          color:#000;
          white-space:nowrap;
        }}
        #hud{{
          position:absolute; top:8px; left:8px;
          font: 12px Arial, sans-serif;
          background: rgba(255,255,255,.92);
          border: 1px solid rgba(0,0,0,.2);
          border-radius: 6px;
          padding: 6px 10px;
          white-space: nowrap;
          pointer-events:none;
          z-index:3;
        }}
      </style>
    </head>
    <body>
      <div id="stage">
        <div id="frame"></div>
        <div id="plan">
          <div id="card">
            <div class="title">¡BIENVENIDO!</div>
            <div class="label" style="top: {USER_LABEL_Y}%;">Usuario:</div>
            <div class="label" style="top: {PASS_LABEL_Y}%;">Contraseña:</div>
            <div class="link" style="top: {LINKS_Y}%; left: {LINK_LEFT_X}%;">Politicas:</div>
            <div class="link" style="top: {LINKS_Y}%; left: {LINK_RIGHT_X}%;">Registrarse:</div>
          </div>
          <div id="hud">Ingrese sus credenciales</div>
        </div>
      </div>
      <script>
        var fe = window.frameElement;
        if (fe){{
          fe.style.position = "fixed";
          fe.style.inset = "0";
          fe.style.width = "100vw";
          fe.style.height = "100vh";
          fe.style.border = "0";
          fe.style.margin = "0";
          fe.style.padding = "0";
          fe.style.zIndex = "999999";
          fe.style.background = "transparent";
        }}
      </script>
    </body>
    </html>
    """
    
    # Mostrar el diseño
    components.html(html, height=600, scrolling=False)
    
    # FORMULARIO STREAMLIT PARA CAPTURAR CREDENCIALES
    with st.form(key="login_form"):
        # Crear columnas para posicionar los inputs
        col1, col2, col3 = st.columns([INPUT_LEFT, 100-INPUT_LEFT-INPUT_RIGHT, INPUT_RIGHT])
        
        with col2:
            # Posicionar usuario
            st.markdown(f'<div style="height:{USER_LABEL_Y-15}px"></div>', unsafe_allow_html=True)
            usuario = st.text_input("", placeholder="warja@gmail.com", key="usuario")
            
            # Posicionar contraseña  
            st.markdown(f'<div style="height:{PASS_LABEL_Y-USER_INPUT_Y-5}px"></div>', unsafe_allow_html=True)
            password = st.text_input("", type="password", placeholder="••••••••", key="password")
            
            # Posicionar botón
            st.markdown(f'<div style="height:{BTN_Y-PASS_INPUT_Y-5}px"></div>', unsafe_allow_html=True)
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            # Mostrar error si existe
            if "login_error" in st.session_state:
                st.error(st.session_state.login_error)
    
    # PROCESAR LOGIN
    if login_button:
        if usuario and password:
            try:
                # Hacer POST a la API
                response = requests.post(
                    "https://camilo27.pythonanywhere.com/api/auth",
                    json={"username": usuario, "password": password},
                    headers={"Content-Type": "application/json"}
                )
                
                data = response.json()
                
                if data.get("ok") == True:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.session_state.login_error = data.get("error", "Credenciales incorrectas")
                    st.rerun()
                    
            except Exception as e:
                st.session_state.login_error = f"Error de conexión: {str(e)}"
                st.rerun()
        else:
            st.session_state.login_error = "Complete ambos campos"
            st.rerun()
else:
    # Redirigir a app principal
    st.switch_page("app.py")
