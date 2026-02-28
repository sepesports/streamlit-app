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
      [data-testid="stSidebar"], [data-testid="collapsedControl"]{display:none !important;}
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
      /* =========================================================
         PALETA HEREDADA DEL ADMINISTRADOR (azul base #040e31)
         ========================================================= */
      --baseBlue: #040e31;
      --bgTop:  #0a1a55;
      --bgMid:  #061240;
      --bgDeep: #02071c;

      --overlay1: rgba(40, 120, 255, .16);
      --overlay2: rgba(0,  10,  40, .62);

      --ink: rgba(255,255,255,.92);
      --muted: rgba(255,255,255,.62);

      --pill: rgba(238, 245, 255, .92);
      --pill2: rgba(255,255,255,.86);

      --btn1:#2f7de1;
      --btn2:#1e5fc4;

      --shadow1: 0 22px 55px rgba(0,0,0,.55);
      --shadow2: 0 10px 22px rgba(0,0,0,.40);
      --blur: 14px;

      /* Variables originales de estructura (se mantienen) */
      --border:2px;
      --borderColor:#111;
      --outerPad:10px;
      --radiusDesk:52px;
      --radiusMob:44px;
      --hdrHDesk:54px;
      --hdrHMob:42px;
      --labelMin:140px;
      --labelMinSmall:110px;
      --rowGap:4px;
      --colGap:26px;
      --inputHDesk:40px;
      --inputHMob:38px;
    }

    html, body{
      margin:0; padding:0;
      width:100%; height:100%;
      background:var(--baseBlue);
      overflow:hidden;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color:var(--ink);
    }

    #stage{
      position:fixed; inset:0;
      width:100vw; height:100vh;
      background:
        radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
        linear-gradient(180deg, #020614 0%, var(--baseBlue) 100%);
    }

    /* PANEL PRINCIPAL (similar al #plan del admin) */
    #plan{
      position:absolute;
      left:10px; right:10px;
      top:10px; bottom:0;
      overflow:hidden;
      border-radius: 34px;
      box-shadow: var(--shadow1);
      background:
        linear-gradient(180deg, rgba(255,255,255,.16) 0%, transparent 22%),
        linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #05164d 58%, var(--bgDeep) 100%);
    }

    /* CORTE DIAGONAL */
    #plan::before{
      content:"";
      position:absolute;
      inset:-10%;
      background:
        linear-gradient(135deg,
          transparent 0%,
          transparent 32%,
          var(--overlay1) 32%,
          var(--overlay2) 66%,
          transparent 66%);
      transform: rotate(-10deg);
      opacity:.95;
      pointer-events:none;
    }

    /* VIÑETA */
    #plan::after{
      content:"";
      position:absolute;
      inset:0;
      background:
        radial-gradient(50% 60% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
        radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
        linear-gradient(180deg, transparent 55%, rgba(0,0,0,.65) 100%);
      pointer-events:none;
    }

    /* MARCO */
    #frame{
      position:absolute;
      left:9px; right:9px;
      top:10px; bottom:0;
      border-left: 2px solid rgba(255,255,255,.14);
      border-right:2px solid rgba(255,255,255,.14);
      border-top:  2px solid rgba(255,255,255,.14);
      box-sizing:border-box;
      pointer-events:none;
      border-radius: 34px;
      box-shadow: inset 0 0 0 1px rgba(0,0,0,.55);
      z-index:5;
    }

    #outer{
      position:absolute;
      left:var(--outerPad); right:var(--outerPad);
      top:var(--outerPad); bottom:var(--outerPad);
      border:1px solid rgba(255,255,255,.10);
      box-sizing:border-box;
      background:transparent;
      border-radius:34px;
      backdrop-filter:blur(var(--blur));
      -webkit-backdrop-filter:blur(var(--blur));
      z-index:10;
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
      z-index:20;
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

    /* Logo sin marco (ambas versiones) */
    .logo, .mobile-logo {
      border: none !important;
      background: transparent !important;
      box-shadow: none !important;
      backdrop-filter: none !important;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    .logo {
      height: 180px; /* DUPLICADO respecto a 90px anterior */
    }

    .logo img, .mobile-logo img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 10px 18px rgba(0,0,0,.35));
      border-radius: 10px;
    }

    /* Logo móvil más grande (ya estaba) */
    .mobile-logo {
      display: none;
      height: 140px;
      margin: 5px 10px 0 10px;
      padding: 5px;
      box-sizing: border-box;
    }

    .blk{
      border:1px solid rgba(255,255,255,.10);
      box-sizing:border-box;
      background:rgba(255,255,255,.04);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      border-radius:24px;
      box-shadow:var(--shadow2), inset 0 1px 0 rgba(255,255,255,.08);
      color:var(--ink);
    }

    .desc{
      flex:1;
      min-height:260px;
      display:flex;
      align-items:center;
      justify-content:center;
      color:var(--muted);
    }

    .hdr{
      height:var(--hdrHDesk);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
      font-size:18px;
      position:relative;
      background:rgba(255,255,255,.04);
      border:1px solid rgba(255,255,255,.10);
      border-radius:24px;
      backdrop-filter:blur(calc(var(--blur) - 6px));
      color:var(--ink);
      text-shadow: 0 8px 18px rgba(0,0,0,.35);
    }

    .hdr::after{
      content:"";
      position:absolute;
      left:14px; right:14px;
      bottom:10px;
      height:2px;
      background:linear-gradient(90deg, transparent, rgba(255,255,255,.4), transparent);
    }

    .form-shell{
      flex:1;
      border:1px solid rgba(255,255,255,.10);
      border-radius:var(--radiusDesk);
      box-sizing:border-box;
      padding:18px;
      position:relative;
      overflow:hidden;
      background:rgba(255,255,255,.02);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      box-shadow:var(--shadow2), inset 0 1px 0 rgba(255,255,255,.08);
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

    /* Campo FOMUL - estilo pill */
    .pill-input {
      width: 210px;
      height: 34px;
      background: linear-gradient(180deg, var(--pill) 0%, var(--pill2) 100%);
      border: 1px solid rgba(255,255,255,.55);
      border-radius: 999px;
      color: rgba(30,40,55,.92);
      font-weight: 800;
      letter-spacing: 0.5px;
      box-sizing: border-box;
      text-align: center;
      font-size: 16px;
      outline: none;
      cursor: default;
      box-shadow: 0 15px 18px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.55);
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

    /* row label + input */
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
      background:rgba(255,255,255,.08);
      border:1px solid rgba(255,255,255,.15);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
      box-sizing:border-box;
      font-size:16px;
      white-space:nowrap;
      color:var(--ink);
      text-shadow: 0 6px 14px rgba(0,0,0,.30);
      border-right:none;
      border-radius: 8px 0 0 8px;
    }

    .label.small{ min-width:var(--labelMinSmall); }

    .input{
      height:var(--inputHDesk);
      border:1px solid rgba(255,255,255,.15);
      background:rgba(0,0,0,.2);
      box-sizing:border-box;
      border-left:none;
      padding:0 10px;
      font-size:15px;
      outline:none;
      width:100%;
      color:var(--ink);
      transition:border 0.2s;
      border-radius: 0 8px 8px 0;
    }

    .input:focus{
      border-color:rgba(255,255,255,.4);
      box-shadow:0 0 10px rgba(255,255,255,.1);
    }

    /* BLOQUES AZULES (antes rosas) */
    .pink-block{
      border:1px solid rgba(255,255,255,.15);
      background:rgba(255,255,255,.04);
      padding:10px 12px 12px 12px;
      box-sizing:border-box;
      border-radius:18px;
      backdrop-filter:blur(calc(var(--blur) - 10px));
    }

    .pink-title{
      font-weight:800;
      text-align:center;
      margin:0 0 10px 0;
      font-size:16px;
      letter-spacing:0.5px;
      color:var(--ink);
      text-shadow:0 0 8px rgba(255,255,255,.2);
    }

    .pink-input{
      width:100%;
      height:40px;
      border:1px solid rgba(255,255,255,.15);
      background:rgba(0,0,0,.3);
      box-sizing:border-box;
      padding:0 10px;
      font-size:15px;
      outline:none;
      border-radius:8px;
      color:var(--ink);
    }

    .pink-input:focus{
      border-color:rgba(255,255,255,.4);
      box-shadow:0 0 10px rgba(255,255,255,.1);
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
      border:1px solid rgba(255,255,255,.15);
      background:rgba(255,255,255,.04);
      display:flex;
      align-items:center;
      justify-content:center;
      box-sizing:border-box;
      border-radius:8px;
      font-size:18px;
      user-select:none;
      color:var(--muted);
    }

    .terms-inside{
      margin-top:16px;
      padding-top:12px;
      border-top:1px solid rgba(255,255,255,.1);
      display:flex;
      align-items:center;
      gap:10px;
      font-size:18px;
      color:var(--muted);
      background: rgba(0,0,0,0.2);
      border-radius: 8px;
      padding: 8px 12px;
    }

    .chk{
      width:18px; height:18px;
      border:2px solid rgba(255,255,255,.3);
      border-radius:4px;
      display:inline-block;
      box-sizing:border-box;
      background:rgba(0,0,0,.3);
    }

    /* Botón de registro en escritorio */
    .desktop-register {
      margin-top: 24px;
      display: flex;
      justify-content: center;
    }

    .register-btn {
      background: linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      border: 1px solid rgba(255,255,255,.1);
      color: var(--ink);
      font-weight: 800;
      font-size: 18px;
      padding: 12px 40px;
      border-radius: 999px;
      box-shadow: 0 22px 26px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.22);
      cursor: pointer;
      transition: transform .12s ease, filter .12s ease;
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .register-btn:hover {
      filter: brightness(1.05);
    }
    .register-btn:active {
      transform: scale(.985);
    }

    .mobile-next{
      display:none;
    }

    /* ===== MOBILE LAYOUT ===== */
    @media (max-width: 768px){
      #wrap{ padding:0; }
      #app{
        max-width:none;
        gap:0;
        flex-direction:column;
      }

      .col-left{ display:none; }

      .mobile-logo {
        display: flex;
      }

      .col-right{
        width:100%;
        flex:1;
        gap:6px;
        min-width:0;
      }

      .hdr{
        margin:0 10px;
        height:var(--hdrHMob);
        font-size:20px;
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
        padding:8px;
      }

      .form-scroll{
        left:8px; right:8px; top:8px; bottom:8px;
      }

      .row-top {
        margin-bottom: 12px;
      }

      .pill-input {
        width: 100%;
        max-width: 480px;
        height: 38px;
        font-size: 18px;
      }

      .grid-2{ display:block; }
      .stack-right{ display:none; }

      .stack{ gap:4px; }

      .qrow{
        grid-template-columns: minmax(100px, 35%) 1fr;
      }

      .label{
        height:var(--inputHMob);
        min-width:0;
        font-size:15px;
        justify-content:flex-start;
        padding-left:8px;
        border-right:1px solid rgba(255,255,255,.15);
      }

      .input{
        height:var(--inputHMob);
        font-size:14px;
      }

      @media (max-width: 520px){
        .qrow{
          grid-template-columns: 1fr;
          row-gap:0;
        }
        .label{
          justify-content:flex-start;
          padding-left:8px;
          border-right:1px solid rgba(255,255,255,.15);
          border-bottom:none;
        }
        .input{
          border-left:1px solid rgba(255,255,255,.15);
          border-top:none;
        }
      }

      .terms-inside{
        margin-top:8px;
        padding-top:6px;
        font-size:14px;
        background: rgba(0,0,0,0.3);
      }

      .chk{
        width:14px; height:14px;
      }

      .mobile-next{
        margin:6px 10px 8px 10px;
        height:42px;
        border:1px solid rgba(255,255,255,.15);
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:800;
        background:rgba(255,255,255,.04);
        box-sizing:border-box;
        font-size:18px;
        border-radius:999px;
        backdrop-filter:blur(calc(var(--blur) - 6px));
        color: var(--ink);
        text-transform: uppercase;
      }

      .desktop-register {
        display: none;
      }
    }

    @media (min-width: 769px) {
      .mobile-next {
        display: none;
      }
    }
  </style>
</head>

<body>
  <div id="stage">
    <div id="frame"></div>
    <div id="plan">
      <div id="outer"></div>

      <div id="wrap">
        <div id="app">

          <!-- IZQUIERDA (DESKTOP) -->
          <div class="col-left">
            <div class="logo">
              <img src="https://files.catbox.moe/056m6v.jpg" alt="Logo">
            </div>
            <div class="blk desc">Descripcion</div>
          </div>

          <!-- DERECHA -->
          <div class="col-right">
            <!-- Logo para móvil -->
            <div class="mobile-logo">
              <img src="https://files.catbox.moe/056m6v.jpg" alt="Logo">
            </div>

            <div class="blk hdr">Formulario</div>

            <div class="form-shell">
              <div class="form-scroll">

                <div class="row-top">
                  <!-- Campo FOMUL con fecha actual -->
                  <input type="text" id="fechaActual" class="pill-input" readonly>
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

                <!-- Botón de registro en escritorio -->
                <div class="desktop-register">
                  <button class="register-btn">Registro</button>
                </div>

              </div>
            </div>

            <!-- Botón móvil -->
            <div class="mobile-next">Registro</div>
          </div>

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

      function actualizarFecha() {
        const hoy = new Date();
        const dia = String(hoy.getDate()).padStart(2, '0');
        const mes = String(hoy.getMonth() + 1).padStart(2, '0');
        const año = hoy.getFullYear();
        const fechaFormateada = `${dia}/${mes}/${año}`;
        const campoFecha = document.getElementById('fechaActual');
        if (campoFecha) {
          campoFecha.value = fechaFormateada;
        }
      }

      actualizarFecha();
    })();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
