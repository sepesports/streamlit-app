# app.py
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

html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{
      --border:2px;
      --borderColor:#111;
      --bg:#fff;

      --yellow:#f2b400;
      --pink:#f3a3a3;

      --radius:48px;
      --gap:18px;
      --pad:18px;
      --text:#111;

      --fieldH:40px;
      --headerH:44px;
      --termsH:34px;

      --maxW:1200px;
    }

    html, body{
      margin:0; padding:0;
      width:100%; height:100%;
      background:var(--bg);
      overflow:hidden;
      font-family: Arial, Helvetica, sans-serif;
      color:var(--text);
    }

    /* Forzar iframe a full screen dentro de Streamlit */
    #stage{
      position:fixed; inset:0;
      width:100vw; height:100vh;
      background:var(--bg);
    }

    /* Marco exterior */
    #outer{
      position:absolute;
      left:10px; right:10px; top:10px; bottom:10px;
      border:var(--border) solid var(--borderColor);
      box-sizing:border-box;
      background:transparent;
    }

    /* Layout general */
    #wrap{
      position:absolute;
      left:10px; right:10px; top:10px; bottom:10px;
      display:flex;
      justify-content:center;
      align-items:stretch;
      box-sizing:border-box;
      padding:10px;
    }

    #app{
      width:100%;
      max-width:var(--maxW);
      height:100%;
      display:flex;
      gap:22px;
      box-sizing:border-box;
    }

    /* Desktop: 2 columnas */
    .col-left{
      flex:0 0 32%;
      display:flex;
      flex-direction:column;
      gap:18px;
      min-width:260px;
    }

    .col-right{
      flex:1;
      display:flex;
      flex-direction:column;
      gap:16px;
      min-width:320px;
    }

    /* Bloques */
    .blk{
      border:var(--border) solid var(--borderColor);
      box-sizing:border-box;
      background:#fff;
    }

    .logo{
      height:88px;
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
    }

    .desc{
      flex:1;
      display:flex;
      align-items:center;
      justify-content:center;
      min-height:220px;
    }

    .terms{
      height:var(--termsH);
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:13px;
      padding:0 10px;
      box-sizing:border-box;
      white-space:nowrap;
    }

    .hdr{
      height:var(--headerH);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
    }

    /* Contenedor formulario (borde redondeado grande) */
    .form-shell{
      flex:1;
      border:3px solid #777;
      border-radius:var(--radius);
      box-sizing:border-box;
      padding:18px 18px 18px 18px;
      position:relative;
      overflow:hidden;
      background:#fff;
    }

    /* Area scroll para que quepan 17 preguntas sin romper bloques */
    .form-scroll{
      position:absolute;
      left:18px; right:18px; top:18px; bottom:18px;
      overflow:auto;
      padding-right:6px;
      box-sizing:border-box;
    }

    /* Top "FOMUL" centrado */
    .row-top{
      width:100%;
      display:flex;
      justify-content:center;
      margin-bottom:16px;
    }

    .pill{
      width:140px;
      height:30px;
      background:var(--yellow);
      border:var(--border) solid var(--borderColor);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
      box-sizing:border-box;
    }

    /* Grilla 2 columnas (desktop) */
    .grid-2{
      display:grid;
      grid-template-columns: 1fr 0.75fr;
      gap:18px 28px;
      align-items:start;
    }

    /* Columna izquierda con 8 campos */
    .stack{
      display:flex;
      flex-direction:column;
      gap:14px;
    }

    /* Columna derecha con 8 campos */
    .stack-right{
      display:flex;
      flex-direction:column;
      gap:14px;
      padding-top:0px;
    }

    /* Campo */
    .field{
      height:var(--fieldH);
      border:var(--border) solid var(--borderColor);
      background:var(--yellow);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
      box-sizing:border-box;
    }

    .field.small{ height:34px; font-size:13px; font-style:italic; font-weight:700; }
    .field.tall{ height:52px; }
    .field.pink{ background:var(--pink); font-style:italic; }

    /* Ajustes tipo imagen (algunos más altos) */
    .field.nacion, .field.naff, .field.pobl{ height:54px; }
    .field.nacimiento{ height:54px; }
    .field.instalacion{ height:50px; }
    .field.fecha_fin{ height:38px; }
    .field.horas{ height:34px; }

    /* ---- MÓVIL ---- */
    @media (max-width: 768px){
      #wrap{ padding:0; }
      #app{
        max-width:none;
        gap:0;
        flex-direction:column;
      }

      .col-left{ display:none; }

      .col-right{
        width:100%;
        flex:1;
        gap:10px;
      }

      .hdr{
        margin:0 10px;
      }

      .form-shell{
        margin:0 10px;
        border-radius:36px;
        padding:14px;
      }

      .form-scroll{
        left:14px; right:14px; top:14px; bottom:14px;
      }

      /* En móvil: lista 1 columna (17 preguntas) */
      .grid-2{ display:block; }
      .stack, .stack-right{ padding:0; }
      .stack-right{ margin-top:14px; }

      .row-top{ margin-bottom:12px; }

      .pill{ width:78%; max-width:260px; }

      /* Botón siguiente bloque aparte */
      .mobile-next{
        margin:10px 10px 12px 10px;
        height:48px;
        border:var(--border) solid var(--borderColor);
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:700;
        background:#fff;
        box-sizing:border-box;
      }

      /* En móvil ocultamos la columna derecha “pareada” y lo convertimos a 17 campos apilados */
      .stack-right{ display:none; }
      .mobile-fields{ display:flex; flex-direction:column; gap:12px; }
      .mobile-fields .field{ height:44px; font-size:14px; }
      .mobile-fields .field.pink{ height:44px; }
    }
  </style>
</head>

<body>
  <div id="stage">
    <div id="outer"></div>

    <div id="wrap">
      <div id="app">

        <!-- IZQUIERDA (DESKTOP): Logo / Descripción / Términos -->
        <div class="col-left">
          <div class="blk logo">Logo</div>
          <div class="blk desc">Descripcion</div>
          <div class="blk terms">Acepta terminos y condiciones</div>
        </div>

        <!-- DERECHA: Header Formulario + Área preguntas -->
        <div class="col-right">
          <div class="blk hdr">Formulario</div>

          <div class="form-shell">
            <div class="form-scroll">

              <div class="row-top">
                <div class="pill">FOMUL</div>
              </div>

              <!-- DESKTOP: 2 columnas (como imagen 1) -->
              <div class="grid-2">
                <div class="stack">
                  <div class="field">NOMBRE</div>
                  <div class="field">DNI</div>
                  <div class="field nacion">NACION</div>
                  <div class="field naff">NAFF</div>
                  <div class="field">CALLE</div>
                  <div class="field pobl">POBL</div>
                  <div class="field">COMARCA</div>
                  <div class="field">C.P</div>
                </div>

                <div class="stack-right">
                  <div class="field small">TLF</div>
                  <div class="field small">CORREO</div>
                  <div class="field small nacimiento">NACIMIENTO</div>
                  <div class="field small">ESTADO CIV</div>
                  <div class="field small">IBAN</div>

                  <div class="field pink instalacion">INSTALACION</div>
                  <div class="field pink fecha_fin">FECHA FIN</div>
                  <div class="field pink horas">HORAS</div>
                </div>

                <!-- MÓVIL: 17 preguntas apiladas -->
                <div class="mobile-fields" style="display:none;">
                  <div class="field">FOMUL</div>
                  <div class="field">NOMBRE</div>
                  <div class="field">DNI</div>
                  <div class="field">NACION</div>
                  <div class="field">NAFF</div>
                  <div class="field">CALLE</div>
                  <div class="field">POBL</div>
                  <div class="field">COMARCA</div>
                  <div class="field">C.P</div>
                  <div class="field">TLF</div>
                  <div class="field">CORREO</div>
                  <div class="field">NACIMIENTO</div>
                  <div class="field">ESTADO CIV</div>
                  <div class="field">IBAN</div>
                  <div class="field pink">INSTALACION</div>
                  <div class="field pink">FECHA FIN</div>
                  <div class="field pink">HORAS</div>
                </div>

              </div>
            </div>
          </div>

          <!-- Botón siguiente (solo móvil) -->
          <div class="mobile-next" style="display:none;">Siguiente</div>
        </div>

      </div>
    </div>
  </div>

  <script>
    (function(){
      var fe = window.frameElement;
      if (fe){
        fe.style.position = "fixed";
        fe.style.inset = "0";
        fe.style.width = "100vw";
        fe.style.height = "100vh";
        fe.style.border = "0";
        fe.style.margin = "0";
        fe.style.padding = "0";
        fe.style.zIndex = "999999";
        fe.style.background = "transparent";
      }

      function syncMobile(){
        var isMobile = window.matchMedia("(max-width: 768px)").matches;

        var mobileNext = document.querySelector(".mobile-next");
        var mobileFields = document.querySelector(".mobile-fields");
        var stackRight = document.querySelector(".stack-right");
        var rowTop = document.querySelector(".row-top");

        if (isMobile){
          if (mobileNext) mobileNext.style.display = "flex";
          if (mobileFields) mobileFields.style.display = "flex";
          if (stackRight) stackRight.style.display = "none";
          if (rowTop) rowTop.style.display = "none"; // en móvil FOMUL va dentro de las 17 preguntas
        } else {
          if (mobileNext) mobileNext.style.display = "none";
          if (mobileFields) mobileFields.style.display = "none";
          if (stackRight) stackRight.style.display = "flex";
          if (rowTop) rowTop.style.display = "flex";
        }
      }

      window.addEventListener("resize", syncMobile);
      syncMobile();
    })();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
