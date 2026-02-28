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
      iframe{display:block !important;}
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

      --outerPad:10px;

      --radiusDesk:52px;
      --radiusMob:44px;

      --hdrHDesk:54px;
      --hdrHMob:62px;

      --shellBorder:4px solid #7a7a7a;

      --fieldBorder:2px solid #6f7680;

      --labelMin:140px;
      --labelMinSmall:110px;
      --rowGap:14px;
      --colGap:26px;

      --inputHDesk:40px;
      --inputHMob:56px;
    }

    html, body{
      margin:0; padding:0;
      width:100%; height:100%;
      background:var(--bg);
      overflow:hidden;
      font-family: Arial, Helvetica, sans-serif;
      color:#111;
    }

    #stage{
      position:fixed; inset:0;
      width:100vw; height:100vh;
      background:var(--bg);
    }

    #outer{
      position:absolute;
      left:var(--outerPad); right:var(--outerPad);
      top:var(--outerPad); bottom:var(--outerPad);
      border:var(--border) solid var(--borderColor);
      box-sizing:border-box;
      background:transparent;
    }

    #wrap{
      position:absolute;
      left:var(--outerPad); right:var(--outerPad);
      top:var(--outerPad); bottom:var(--outerPad);
      box-sizing:border-box;
      padding:10px;
      display:flex;
      justify-content:center;
      align-items:stretch;
    }

    #app{
      width:100%;
      height:100%;
      max-width:1280px;
      display:flex;
      gap:22px;
      box-sizing:border-box;
    }

    /* ===== DESKTOP LAYOUT ===== */
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
      min-height:260px;
      display:flex;
      align-items:center;
      justify-content:center;
    }

    .hdr{
      height:var(--hdrHDesk);
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

    .form-shell{
      flex:1;
      border:var(--shellBorder);
      border-radius:var(--radiusDesk);
      box-sizing:border-box;
      padding:18px;
      position:relative;
      overflow:hidden;
      background:#fff;
    }

    .form-scroll{
      position:absolute;
      left:18px; right:18px; top:18px; bottom:18px;
      overflow:auto;
      padding-right:8px;
      box-sizing:border-box;
    }

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

    /* row label + input (desktop: lado a lado) */
    .qrow{
      display:grid;
      grid-template-columns: auto 1fr;
      column-gap:0;
      align-items:stretch;
    }

    .label{
      height:var(--inputHDesk);
      min-width:var(--labelMin);
      padding:0 12px;
      background:var(--yellow);
      border:var(--border) solid var(--borderColor);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:800;
      box-sizing:border-box;
      font-size:16px;
      white-space:nowrap;
    }

    .label.small{ min-width:var(--labelMinSmall); }

    .input{
      height:var(--inputHDesk);
      border:var(--fieldBorder);
      background:#fff;
      box-sizing:border-box;
      border-left:none;
      padding:0 10px;
      font-size:15px;
      outline:none;
      width:100%;
    }

    /* BLOQUES ROSAS (desktop columna derecha) */
    .pink-block{
      border:var(--fieldBorder);
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
      border:var(--fieldBorder);
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
      border:var(--fieldBorder);
      background:#efefef;
      display:flex;
      align-items:center;
      justify-content:center;
      box-sizing:border-box;
      border-radius:3px;
      font-size:18px;
      user-select:none;
    }

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

    .mobile-next{
      display:none;
    }

    /* ===== MOBILE LAYOUT =====
       - Mantiene "plano" (sin romper tamaños base)
       - Si no cabe input al lado: input debajo (por fila)
    */
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
        min-width:0;
      }

      .hdr{
        margin:0 10px;
        height:var(--hdrHMob);
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
        border-radius:var(--radiusMob);
        padding:16px;
      }

      .form-scroll{
        left:16px; right:16px; top:16px; bottom:16px;
      }

      .pill{
        width:100%;
        max-width:520px;
        height:46px;
        font-size:26px;
      }

      /* En móvil: una sola columna (solo 8 preguntas como en imagen) */
      .grid-2{ display:block; }
      .stack-right{ display:none; }

      .stack{ gap:18px; }

      /* Fila: intenta lado a lado; si no cabe, cae a 1 columna (label arriba, input abajo) */
      .qrow{
        grid-template-columns: minmax(140px, 42%) 1fr;
      }

      .label{
        height:var(--inputHMob);
        min-width:0;
        font-size:26px;
        justify-content:flex-start;
        padding-left:18px;
      }

      .input{
        height:var(--inputHMob);
        font-size:20px;
      }

      /* BREAKPOINT interno por ancho útil: input debajo */
      @media (max-width: 520px){
        .qrow{
          grid-template-columns: 1fr;
          row-gap:0;
        }
        .label{
          justify-content:flex-start;
          padding-left:18px;
        }
        .input{
          border-left:var(--fieldBorder);
          border-top:none;
        }
      }

      .terms-inside{
        margin-top:18px;
        padding-top:14px;
        font-size:18px;
      }

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

        <!-- IZQUIERDA (DESKTOP) -->
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

                <!-- IZQUIERDA / MÓVIL -->
                <div class="stack">

                  <div class="qrow">
                    <div class="label">NOMBRE:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">DNI:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">NACION:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">NAFF:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">CALLE:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">POBL:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">COMARCA:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">C.P:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="terms-inside">
                    <span class="chk"></span>
                    <span>Acepta terminos y condiciones</span>
                  </div>
                </div>

                <!-- DERECHA (SOLO DESKTOP) -->
                <div class="stack-right">

                  <div class="qrow">
                    <div class="label small">TLF:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label small">CORREO:</div>
                    <input class="input" type="email" />
                  </div>

                  <div class="qrow">
                    <div class="label">NACIMIENTO:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
                    <div class="label">ESTADO CIV:</div>
                    <input class="input" type="text" />
                  </div>

                  <div class="qrow">
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

                  <!-- HORAS ELIMINADO -->
                </div>

              </div>
            </div>
          </div>

          <div class="mobile-next">Siguiente</div>
        </div>

      </div>
    </div>
  </div>

  <script>
    (function(){
      // Full-screen real del iframe en Streamlit
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
    })();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
