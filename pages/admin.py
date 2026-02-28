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
      --hdrHMob:42px;          /* reducido para 7 filas */

      --shellBorder:4px solid #7a7a7a;

      --fieldBorder:2px solid #6f7680;

      --labelMin:140px;
      --labelMinSmall:110px;
      --rowGap:4px;            /* mínimo gap entre filas */
      --colGap:26px;

      --inputHDesk:40px;
      --inputHMob:38px;         /* altura más compacta */

      /* nuevos colores oscuros (tipo calendario) */
      --bg-0:#070b12;
      --bg-1:#0b1320;
      --bg-2:#0f1c2a;
      --glass: rgba(255,255,255,.06);
      --glass-2: rgba(255,255,255,.08);
      --stroke: rgba(255,255,255,.10);
      --stroke-2: rgba(255,255,255,.14);
      --glow-blue: rgba(96, 196, 255, .45);
      --glow-blue-2: rgba(96, 196, 255, .22);
      --glow-orange: rgba(255, 142, 64, .50);
      --glow-orange-2: rgba(255, 142, 64, .22);
      --txt-0: rgba(255,255,255,.95);
      --txt-1: rgba(255,255,255,.78);
      --txt-2: rgba(255,255,255,.55);
      --txt-3: rgba(255,255,255,.35);
      --free:#4fe38c;
      --busy:#ff4b4b;
      --other:#ff7c2c;
      --radius-outer: 26px;
      --radius-card: 18px;
      --radius-pill: 999px;
      --radius-cell: 12px;
      --shadow-soft: 0 18px 40px rgba(0,0,0,.45);
      --shadow-inner: inset 0 1px 0 rgba(255,255,255,.08);
      --blur: 18px;
      --fs-top: 14px;
      --fs-title: 28px;
      --fs-sub: 12px;
      --fs-day: 11px;
      --fs-cell: 14px;
      --fs-h3: 18px;
      --fs-table: 13px;
      --fs-btn: 14px;
    }

    html, body{
      margin:0; padding:0;
      width:100%; height:100%;
      background:var(--bg-0);
      overflow:hidden;
      font-family: "Inter", system-ui, -apple-system, "SF Pro Display", Segoe UI, Roboto, Arial, sans-serif;
      color:var(--txt-0);
    }

    #stage{
      position:fixed; inset:0;
      width:100vw; height:100vh;
      background:
        radial-gradient(1100px 700px at 10% 10%, rgba(255,124,44,.22), transparent 55%),
        radial-gradient(900px 650px at 90% 18%, rgba(96,196,255,.22), transparent 55%),
        radial-gradient(900px 750px at 50% 95%, rgba(96,196,255,.12), transparent 60%),
        linear-gradient(180deg, var(--bg-2), var(--bg-0));
    }

    #outer{
      position:absolute;
      left:var(--outerPad); right:var(--outerPad);
      top:var(--outerPad); bottom:var(--outerPad);
      border:1px solid var(--stroke);
      box-sizing:border-box;
      background:transparent;
      border-radius:var(--radius-outer);
      backdrop-filter:blur(var(--blur));
      -webkit-backdrop-filter:blur(var(--blur));
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
      border:1px solid var(--stroke);
      box-sizing:border-box;
      background:var(--glass);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      border-radius:var(--radius-card);
      box-shadow:var(--shadow-soft), var(--shadow-inner);
      color:var(--txt-0);
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
      background:var(--glass-2);
      border:1px solid var(--stroke);
      border-radius:var(--radius-card);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      color:var(--txt-0);
    }

    .hdr::after{
      content:"";
      position:absolute;
      left:14px; right:14px;
      bottom:10px;
      height:2px;
      background:linear-gradient(90deg, transparent, var(--glow-orange), transparent);
    }

    .form-shell{
      flex:1;
      border:1px solid var(--stroke);
      border-radius:var(--radiusDesk);
      box-sizing:border-box;
      padding:18px;
      position:relative;
      overflow:hidden;
      background:var(--glass-2);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      box-shadow:var(--shadow-soft), var(--shadow-inner);
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
      background:linear-gradient(180deg, rgba(255,124,44,.3), rgba(255,124,44,.1));
      border:1px solid var(--glow-orange);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:800;
      letter-spacing:0.5px;
      box-sizing:border-box;
      border-radius:var(--radius-pill);
      color:var(--txt-0);
      text-shadow:0 0 8px var(--glow-orange);
      box-shadow:0 0 18px var(--glow-orange-2), var(--shadow-inner);
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
      background:rgba(255,124,44,.15);
      border:1px solid var(--glow-orange);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:800;
      box-sizing:border-box;
      font-size:16px;
      white-space:nowrap;
      color:var(--txt-0);
      text-shadow:0 0 5px var(--glow-orange);
      border-right:none;
    }

    .label.small{ min-width:var(--labelMinSmall); }

    .input{
      height:var(--inputHDesk);
      border:1px solid var(--stroke);
      background:rgba(0,0,0,.3);
      box-sizing:border-box;
      border-left:none;
      padding:0 10px;
      font-size:15px;
      outline:none;
      width:100%;
      color:var(--txt-0);
      transition:border 0.2s;
    }

    .input:focus{
      border-color:var(--glow-orange);
      box-shadow:0 0 10px var(--glow-orange-2);
    }

    /* BLOQUES AZULES (antes rosas) */
    .pink-block{
      border:1px solid var(--glow-blue);
      background:rgba(96,196,255,.08);
      padding:10px 12px 12px 12px;
      box-sizing:border-box;
      border-radius:var(--radius-card);
      backdrop-filter:blur(calc(var(--blur) - 10px));
    }

    .pink-title{
      font-weight:800;
      text-align:center;
      margin:0 0 10px 0;
      font-size:16px;
      letter-spacing:0.5px;
      color:var(--txt-0);
      text-shadow:0 0 8px var(--glow-blue);
    }

    .pink-input{
      width:100%;
      height:40px;
      border:1px solid var(--stroke);
      background:rgba(0,0,0,.4);
      box-sizing:border-box;
      padding:0 10px;
      font-size:15px;
      outline:none;
      border-radius:3px;
      color:var(--txt-0);
    }

    .pink-input:focus{
      border-color:var(--glow-blue);
      box-shadow:0 0 10px var(--glow-blue-2);
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
      border:1px solid var(--stroke);
      background:var(--glass);
      display:flex;
      align-items:center;
      justify-content:center;
      box-sizing:border-box;
      border-radius:3px;
      font-size:18px;
      user-select:none;
      color:var(--txt-1);
    }

    .terms-inside{
      margin-top:16px;
      padding-top:12px;
      border-top:1px solid var(--stroke);
      display:flex;
      align-items:center;
      gap:10px;
      font-size:18px;
      color:var(--txt-1);
    }

    .chk{
      width:18px; height:18px;
      border:2px solid var(--stroke);
      border-radius:3px;
      display:inline-block;
      box-sizing:border-box;
      background:rgba(0,0,0,.3);
    }

    .mobile-next{
      display:none;
    }

    /* ===== MOBILE LAYOUT =====
       - Ajustado para mostrar 7 filas visibles
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
        gap:6px;                /* reducido */
        min-width:0;
      }

      .hdr{
        margin:0 10px;
        height:var(--hdrHMob);
        font-size:20px;          /* más pequeño */
        border:none;
      }

      .hdr::after{
        left:18px; right:18px;
        bottom:6px;
        height:2px;
      }

      .form-shell{
        margin:0 10px;
        border-radius:var(--radiusMob);
        padding:8px;             /* reducido de 12px a 8px */
      }

      .form-scroll{
        left:8px; right:8px; top:8px; bottom:8px;
      }

      .pill{
        width:100%;
        max-width:480px;
        height:34px;             /* más compacto */
        font-size:18px;          /* reducido */
      }

      .grid-2{ display:block; }
      .stack-right{ display:none; }

      .stack{ gap:4px; }         /* mínimo gap */

      /* Fila: lado a lado con columna más estrecha */
      .qrow{
        grid-template-columns: minmax(100px, 35%) 1fr;
      }

      .label{
        height:var(--inputHMob);
        min-width:0;
        font-size:15px;           /* más pequeño */
        justify-content:flex-start;
        padding-left:8px;         /* reducido */
        border-right:1px solid var(--glow-orange);
      }

      .input{
        height:var(--inputHMob);
        font-size:14px;           /* más pequeño */
      }

      /* BREAKPOINT interno por ancho útil: input debajo */
      @media (max-width: 520px){
        .qrow{
          grid-template-columns: 1fr;
          row-gap:0;
        }
        .label{
          justify-content:flex-start;
          padding-left:8px;
          border-right:1px solid var(--glow-orange);
          border-bottom:none;
        }
        .input{
          border-left:1px solid var(--stroke);
          border-top:none;
        }
      }

      .terms-inside{
        margin-top:8px;
        padding-top:6px;
        font-size:14px;
      }

      .chk{
        width:14px; height:14px;
      }

      .mobile-next{
        margin:6px 10px 8px 10px;
        height:42px;              /* reducido */
        border:1px solid var(--stroke);
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:800;
        background:var(--glass);
        box-sizing:border-box;
        font-size:18px;           /* reducido */
        border-radius:var(--radius-pill);
        backdrop-filter:blur(calc(var(--blur) - 6px));
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
