# app.py
import streamlit as st
import streamlit.components.v1 as components
import json

# ================== AUTH DESDE QUERY PARAMS (Streamlit nuevo) ==================
# admin.py redirige a /?auth=1&usuario=...&rol=...; aquí se guarda en session_state.
try:
    qp = st.query_params
    if str(qp.get('auth', '')) == '1':
        st.session_state['auth'] = True
        st.session_state['usuario'] = str(qp.get('usuario', qp.get('correo', '')) or '')
        st.session_state['rol'] = str(qp.get('rol', qp.get('role', '')) or '')
        try:
            st.query_params.clear()
        except Exception:
            pass
except Exception:
    pass

# Texto de cabecera (Login o usuario | rol)
LOGIN_CELL_TEXT = 'Login'
if st.session_state.get('auth') and st.session_state.get('usuario'):
    _u = st.session_state.get('usuario','')
    _r = st.session_state.get('rol','')
    LOGIN_CELL_TEXT = (_u + (' | ' + _r if _r else '')).strip()

# ==============================================================================
# PLANO AJUSTADO (responsivo) - NO TOCAR HTML
# Ajusta SOLO la sección "AJUSTES" para mover/medir.
# ==============================================================================

# ================== AJUSTES ==================
# CUADRO / CONTENEDOR PRINCIPAL (px)
PAD_X_PX = 20          # margen lateral
PAD_TOP_PX = 20        # margen superior
BORDER_PX = 2          # borde del marco
BORDER_COLOR = "#111"  # color borde

# CABECERA (alto en % del CUADRO)
HEADER_H = 12          # % altura cabecera

# Celdas cabecera (ancho en % del CUADRO) => deben sumar 100
HEADER_COLS = [25, 50, 25]  # [Logo, Fondo1, Login/Usuario]

# IMAGEN CENTRAL (alto en % del CUADRO)
IMAGE_H = 46

# SECCIÓN BOTONES (alto en % del CUADRO)
BTNS_H = 32

# PIE (alto en % del CUADRO)
FOOTER_H = 10

# BOTONES: 2 filas x 3 columnas (en desktop)
BTN_ROWS = 2
BTN_COLS = 3

# Separación entre botones (px)
BTN_GAP_PX = 18

# Padding interno de la sección botones (px)
BTNS_PAD_PX = 24

# Fuentes (px)
FONT_MAIN = 14
FONT_BOLD = 14

# MOBILE: ancho máximo para cambiar a layout 2x? (px)
MOBILE_MAX_W_PX = 820

# ================== UI BASE ==================
st.set_page_config(layout="wide")

# ================== HTML PLANO ==================
HTML = r"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  html,body{height:100%; margin:0; font-family: Arial, sans-serif;}
  body{background:#fff;}

  #stage{
    position:fixed; inset:0;
    background:#fff;
  }

  #frame{
    position:absolute;
    left: __PADX__px; right: __PADX__px; top: __PADTOP__px; bottom: __PADTOP__px;
    border: __B__px solid __BC__;
    box-sizing:border-box;
    background:#fff;
  }

  #grid{
    position:absolute;
    left: __PADX__px; right: __PADX__px; top: __PADTOP__px; bottom: __PADTOP__px;
    display:flex;
    flex-direction:column;
  }

  /* ===== Cabecera ===== */
  #header{
    height: __HEADER_H__%;
    display:flex;
    border-bottom: __B__px solid __BC__;
  }
  .hcell{
    border-right: __B__px solid __BC__;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    font-size: __FMAIN__px;
    box-sizing:border-box;
  }
  .hcell:last-child{border-right:none;}
  #h1{width: __H1__%;}
  #h2{width: __H2__%;}
  #h3{width: __H3__%;}

  /* ===== Imagen ===== */
  #img{
    height: __IMG_H__%;
    border-bottom: __B__px solid __BC__;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    font-size: __FMAIN__px;
    box-sizing:border-box;
  }

  /* ===== Botones ===== */
  #btns{
    height: __BTNS_H__%;
    border-bottom: __B__px solid __BC__;
    box-sizing:border-box;
    padding: __BTNS_PAD__px;
    display:grid;
    grid-template-columns: repeat(__COLS__, 1fr);
    grid-template-rows: repeat(__ROWS__, 1fr);
    gap: __GAP__px;
  }

  .btn{
    border: __B__px solid __BC__;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    font-size: __FBOLD__px;
    box-sizing:border-box;
    background:#fff;
    cursor:pointer;
    user-select:none;
    text-align:center;
    padding: 12px;
  }

  /* ===== Footer ===== */
  #footer{
    height: __FOOT_H__%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    font-size: __FMAIN__px;
    box-sizing:border-box;
  }

  /* Mobile: 2 columnas y 3 filas */
  @media (max-width: __MOBILE_MAX_W_PX__px){
    #btns{
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(3, 1fr);
    }
  }
</style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="grid">
      <div id="header">
        <div id="h1" class="hcell">Logo</div>
        <div id="h2" class="hcell">Fondo 1</div>
        <div id="h3" class="hcell">__LOGIN_CELL_TEXT__</div>
      </div>

      <div id="img">Imagen</div>

      <div id="btns">
        <div class="btn" data-go="admin">Horarios</div>
        <div class="btn" data-go="admin">Control de<br/>Asistencia</div>
        <div class="btn" data-go="admin">Nómina y<br/>Pagos</div>
        <div class="btn" data-go="admin">Incidencias</div>
        <div class="btn" data-go="admin">Formación</div>
        <div class="btn" data-go="admin">Comunicados</div>
      </div>

      <div id="footer">Pie de pagina</div>
    </div>
  </div>

<script>
  // Si NO está autenticado, cualquier botón manda a /admin (login).
  // Si está autenticado, aquí puedes cambiar la navegación real más adelante.
  (function(){
    var authed = "__AUTH__" === "1";
    document.querySelectorAll(".btn").forEach(function(b){
      b.addEventListener("click", function(){
        if(!authed){
          window.location.href = window.location.origin + "/admin";
        }else{
          // TODO: aquí irán rutas reales cuando existan páginas.
          // Por ahora no hace nada para no inventar.
        }
      });
    });
  })();
</script>
</body>
</html>
"""

AUTH_FLAG = "1" if st.session_state.get("auth") else "0"

html = (
    HTML
    .replace("__PADX__", str(PAD_X_PX))
    .replace("__PADTOP__", str(PAD_TOP_PX))
    .replace("__B__", str(BORDER_PX))
    .replace("__BC__", str(BORDER_COLOR))
    .replace("__HEADER_H__", str(HEADER_H))
    .replace("__H1__", str(HEADER_COLS[0]))
    .replace("__H2__", str(HEADER_COLS[1]))
    .replace("__H3__", str(HEADER_COLS[2]))
    .replace("__IMG_H__", str(IMAGE_H))
    .replace("__BTNS_H__", str(BTNS_H))
    .replace("__FOOT_H__", str(FOOTER_H))
    .replace("__ROWS__", str(BTN_ROWS))
    .replace("__COLS__", str(BTN_COLS))
    .replace("__GAP__", str(BTN_GAP_PX))
    .replace("__BTNS_PAD__", str(BTNS_PAD_PX))
    .replace("__FMAIN__", str(FONT_MAIN))
    .replace("__FBOLD__", str(FONT_BOLD))
    .replace("__MOBILE_MAX_W_PX__", str(MOBILE_MAX_W_PX))
    .replace("__LOGIN_CELL_TEXT__", json.dumps(LOGIN_CELL_TEXT)[1:-1])
    .replace("__AUTH__", AUTH_FLAG)
)

components.html(html, height=10, scrolling=False)
