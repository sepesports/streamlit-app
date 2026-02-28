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

      --radius:52px;
      --gap:18px;

      --maxW:1280px;

      --hdrH:54px;
      --termsH:34px;

      --labelH:40px;
      --inputH:40px;
      --rowGap:14px;
      --colGap:26px;

      --fieldBorder:#6f7680;
      --shellBorder:#7a7a7a;
    }

    html, body{
      margin:0; padding:0;
      width:100%; height:100%;
      background:var(--bg);
      overflow:hidden;
      font-family: Arial, Helvetica, sans-serif;
      color:#111;
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

    /* Layout */
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
      gap:12px;
      min-width:420px;
    }

    /* Bloques */
    .blk{
      border:var(--border) solid var(--borderColor);
      box-sizing:border-box;
      background:#fff;
    }

    .logo{
      height:90px;
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
      min-height:260px;
    }

    /* En la imagen nueva, "Acepta..." está dentro del formulario, NO como bloque izquierdo */
    .terms-left{ display:none; }

    .hdr{
      height:var(--hdrH);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
      font-size:18px;
      position:relative;
      background:#fff;
    }

    .hdr::after{
      content:"";
      position:absolute;
      left:14px; right:14px;
      bottom:10px;
      height:2px;
      background:#b7bcc3;
    }

    /* Contenedor formulario (borde redondeado grande) */
    .form-shell{
      flex:1;
      border:4px solid var(--shellBorder);
      border-radius:var(--radius);
      box-sizing:border-box;
      padding:18px;
      position:relative;
      overflow:hidden;
      background:#fff;
    }

    /* Scroll interno para no romper layout */
    .form-scroll{
      position:absolute;
      left:18px; right:18px; top:18px; bottom:18px;
      overflow:auto;
      padding-right:8px;
      box-sizing:border-box;
    }

    /* FOMUL */
    .row-top{
      width:100%;
      display:flex;
      justify-content:center;
      margin-bottom:16px;
    }

    .pill{
      width:210px;
      height:34px;
      background:var(--yellow);
      border:var(--border) solid var(--borderColor);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:800;
      letter-spacing:0.5px;
      box-sizing:border-box;
    }

    /* Desktop grid: 2 columnas */
    .grid-2{
      display:grid;
      grid-template-columns: 1fr 0.95fr;
      gap:18px var(--colGap);
      align-items:start;
    }

    .stack{
      display:flex;
      flex-direction:column;
      gap:var(--rowGap);
    }

    .stack-right{
      display:flex;
      flex-direction:column;
      gap:var(--rowGap);
    }

    /* Fila label+input */
    .row{
      display:flex;
      align-items:stretch;
      gap:0;
    }

    .label{
      height:var(--labelH);
      min-width:140px;
      padding:0 12px;
      background:var(--yellow);
      border:var(--border) solid var(--borderColor);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:800;
      box-sizing:border-box;
      font-size:16px;
    }

    .label.small{ min-width:110px; }

    .input{
      flex:1;
      height:var(--inputH);
      border:2px solid var(--fieldBorder);
      background:#fff;
      box-sizing:border-box;
      border-left:none;
      padding:0 10px;
      font-size:15px;
      outline:none;
    }

    /* Bloques rosas (INSTALACION / FECHA FIN / HORAS) */
    .pink-block{
      border:2px solid var(--fieldBorder);
      background:var(--pink);
      padding:10px 12px 12px 12px;
      box-sizing:border-box;
    }

    .pink-title{
      font-weight:800;
      text-align:center;
      margin:0 0 10px 0;
      font-size:16px;
      letter-spacing:0.5px;
    }

    .pink-input{
      width:100%;
      height:40px;
      border:2px solid var(--fieldBorder);
      background:#fff;
      box-sizing:border-box;
      padding:0 10px;
      font-size:15px;
      outline:none;
      border-radius:3px;
    }

    .date-row{
      display:flex;
      gap:8px;
      align-items:center;
    }

    .date-input{ flex:1; }

    .cal-ico{
      width:44px;
      height:40px;
      border:2px solid var(--fieldBorder);
      background:#efefef;
      display:flex;
      align-items:center;
      justify-content:center;
      box-sizing:border-box;
      border-radius:3px;
      font-size:18px;
      user-select:none;
    }

    /* Línea + checkbox dentro del formulario (desktop imagen nueva) */
    .terms-inside{
      margin-top:16px;
      padding-top:12px;
      border-top:2px solid #b7bcc3;
      display:flex;
      align-items:center;
      gap:10px;
      font-size:18px;
    }

    .chk{
      width:18px; height:18px;
      border:2px solid #666;
      border-radius:3px;
      display:inline-block;
      box-sizing:border-box;
      background:#fff;
    }

    /* Móvil */
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
        height:62px;
        font-size:34px;
        border:none;
      }

      .hdr::after{
        left:18px; right:18px;
        bottom:10px;
        height:2px;
      }

      .form-shell{
        margin:0 10px;
        border-radius:44px;
        padding:16px;
      }

      .form-scroll{
        left:16px; right:16px; top:16px; bottom:16px;
      }

      .row-top{ margin-bottom:14px; }
      .pill{
        width:100%;
        max-width:520px;
        height:46px;
        font-size:26px;
      }

      /* Móvil: 1 columna de filas */
      .grid-2{ display:block; }
      .stack-right{ display:none; }

      .stack{
        gap:18px;
      }

      .label{
        min-width:150px;
        height:56px;
        font-size:26px;
        justify-content:center;
      }

      .row{ gap:0; }
      .input{
        height:56px;
        font-size:20px;
      }

      .terms-inside{
        margin-top:18px;
        padding-top:14px;
        font-size:18px;
      }

      /* Botón Siguiente bloque (móvil) */
      .mobile-next{
        margin:12px 10px 14px 10px;
        height:64px;
        border:3px solid #111;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:800;
        background:#efefef;
        box-sizing:border-box;
        font-size:34px;
      }
    }
  </style>
</head>

<body>
  <div id="stage">
    <div id="outer"></div>

    <div id="wrap">
      <div id="app">

        <!-- IZQUIERDA (DESKTOP): Logo / Descripción -->
        <div class="col-left">
          <div class="blk logo">Logo</div>
          <div class="blk desc">Descripcion</div>
        </div>

        <!-- DERECHA -->
        <div class="col-right">
          <div class="blk hdr">Formulario</div>

          <div class="form-shell">
            <div class="form-scroll">

              <div class="row-top">
                <div class="pill">FOMUL</div>
              </div>

              <div class="grid-2">

                <!-- COLUMNA IZQUIERDA (desktop) / ÚNICA (móvil) -->
                <div class="stack">

                  <div class="row">
                    <div class="label">NOMBRE:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">DNI:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">NACION:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">NAFF:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">CALLE:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">POBL:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">COMARCA:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">C.P:</div>
                    <input class="input" type="text" />
                  </div>

                  <!-- En móvil solo mostramos estos 8 campos (como imagen) -->
                  <div class="terms-inside">
                    <span class="chk"></span>
                    <span>Acepta terminos y condiciones</span>
                  </div>
                </div>

                <!-- COLUMNA DERECHA (solo desktop) -->
                <div class="stack-right">

                  <div class="row">
                    <div class="label small">TLF:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label small">CORREO:</div>
                    <input class="input" type="email" />
                  </div>

                  <div class="row">
                    <div class="label">NACIMIENTO:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label">ESTADO CIV:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="row">
                    <div class="label small">IBAN:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="pink-block">
                    <div class="pink-title">INSTALACION:</div>
                    <input class="pink-input" type="text" />
                  </div>

                  <div class="pink-block">
                    <div class="pink-title">FECHA FIN:</div>
                    <div class="date-row">
                      <input class="pink-input date-input" type="text" />
                      <div class="cal-ico">🗓️</div>
                    </div>
                  </div>

                  <div class="pink-block">
                    <div class="pink-title">HORAS:</div>
                  </div>

                </div>
              </div>

            </div>
          </div>

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
        if (mobileNext){
          mobileNext.style.display = isMobile ? "flex" : "none";
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
