# altas_registro.py
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

API_URL = "https://camilo27.pythonanywhere.com/api/altas/registro"

html = rf"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{{
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
    }}

    html, body{{
      margin:0; padding:0;
      width:100%; height:100%;
      background:var(--baseBlue);
      overflow:hidden;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color:var(--ink);
    }}

    #stage{{
      position:fixed; inset:0;
      width:100vw; height:100vh;
      background:
        radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
        linear-gradient(180deg, #020614 0%, var(--baseBlue) 100%);
    }}

    #plan{{
      position:absolute;
      left:10px; right:10px;
      top:10px; bottom:0;
      overflow:hidden;
      border-radius: 34px;
      box-shadow: var(--shadow1);
      background:
        linear-gradient(180deg, rgba(255,255,255,.16) 0%, transparent 22%),
        linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #05164d 58%, var(--bgDeep) 100%);
    }}

    #plan::before{{
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
    }}

    #plan::after{{
      content:"";
      position:absolute;
      inset:0;
      background:
        radial-gradient(50% 60% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
        radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
        linear-gradient(180deg, transparent 55%, rgba(0,0,0,.65) 100%);
      pointer-events:none;
    }}

    #frame{{
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
    }}

    #outer{{
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
    }}

    #wrap{{
      position:absolute;
      left:var(--outerPad); right:var(--outerPad);
      top:var(--outerPad); bottom:var(--outerPad);
      box-sizing:border-box;
      padding:10px;
      display:flex;
      justify-content:center;
      align-items:stretch;
      z-index:20;
    }}

    #app{{
      width:100%;
      height:100%;
      max-width:1280px;
      display:flex;
      gap:22px;
      box-sizing:border-box;
    }}

    .col-left{{
      flex:0 0 32%;
      display:flex;
      flex-direction:column;
      gap:18px;
      min-width:260px;
    }}

    .col-right{{
      flex:1;
      display:flex;
      flex-direction:column;
      gap:12px;
      min-width:420px;
    }}

    .logo, .mobile-logo {{
      border: none !important;
      background: transparent !important;
      box-shadow: none !important;
      backdrop-filter: none !important;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}

    .logo {{ height: 180px; }}

    .logo img, .mobile-logo img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 10px 18px rgba(0,0,0,.35));
      border-radius: 10px;
    }}

    .mobile-logo {{
      display: none;
      height: 140px;
      margin: 5px 10px 0 10px;
      padding: 5px;
      box-sizing: border-box;
    }}

    .blk{{
      border:1px solid rgba(255,255,255,.10);
      box-sizing:border-box;
      background:rgba(255,255,255,.04);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      border-radius:24px;
      box-shadow:var(--shadow2), inset 0 1px 0 rgba(255,255,255,.08);
      color:var(--ink);
    }}

    .desc {{
      flex:1;
      min-height:260px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 20px;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.5;
      gap: 12px;
    }}

    .desc p {{ margin: 0; max-width: 90%; }}
    .desc p:first-child {{ font-weight: 600; color: var(--ink); }}

    .hdr{{
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
    }}

    .hdr::after{{
      content:"";
      position:absolute;
      left:14px; right:14px;
      bottom:10px;
      height:2px;
      background:linear-gradient(90deg, transparent, rgba(255,255,255,.4), transparent);
    }}

    .form-shell{{
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
    }}

    .form-scroll{{
      position:absolute;
      left:18px; right:18px; top:18px; bottom:18px;
      overflow:auto;
      padding-right:8px;
      box-sizing:border-box;
    }}

    .row-top{{
      width:100%;
      display:flex;
      justify-content:center;
      margin-bottom:16px;
    }}

    .pill-input {{
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
    }}

    .grid-2{{
      display:grid;
      grid-template-columns: 1fr 0.95fr;
      gap:18px var(--colGap);
      align-items:start;
    }}

    .stack, .stack-right{{
      display:flex;
      flex-direction:column;
      gap:var(--rowGap);
    }}

    .qrow{{
      display:grid;
      grid-template-columns: auto 1fr;
      column-gap:0;
      align-items:stretch;
    }}

    .label{{
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
    }}

    .label.small{{ min-width:var(--labelMinSmall); }}

    .input{{
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
    }}

    .pink-block{{
      border:1px solid rgba(255,255,255,.15);
      background:rgba(255,255,255,.04);
      padding:10px 12px 12px 12px;
      box-sizing:border-box;
      border-radius:18px;
      backdrop-filter:blur(calc(var(--blur) - 10px));
    }}

    .pink-title{{
      font-weight:800;
      text-align:center;
      margin:0 0 10px 0;
      font-size:16px;
      letter-spacing:0.5px;
      color:var(--ink);
      text-shadow:0 0 8px rgba(255,255,255,.2);
    }}

    .pink-input{{
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
    }}

    .terms-inside{{
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
    }}

    .terms-inside input[type="checkbox"]{{
      width:18px; height:18px;
      accent-color: #2f7de1;
      cursor:pointer;
    }}

    .desktop-register {{
      margin-top: 24px;
      display: flex;
      justify-content: center;
    }}

    .register-btn {{
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
    }}

    .register-btn[disabled] {{ opacity:.55; cursor:not-allowed; }}

    .mobile-next{{ display:none; }}

    @media (max-width: 768px){{
      #wrap{{ padding:0; }}
      #app{{ max-width:none; gap:0; flex-direction:column; }}
      .col-left{{ display:none; }}
      .mobile-logo {{ display: flex; }}
      .col-right{{ width:100%; flex:1; gap:6px; min-width:0; }}
      .hdr{{ margin:0 10px; height:var(--hdrHMob); font-size:20px; border:none; }}
      .form-shell{{ margin:0 10px; border-radius:var(--radiusMob); padding:8px; }}
      .form-scroll{{ left:8px; right:8px; top:8px; bottom:8px; }}
      .pill-input {{ width: 100%; max-width: 480px; height: 38px; font-size: 18px; }}
      .grid-2{{ display:block; }}
      .desktop-register {{ display: none; }}

      .mobile-next{{
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
        cursor:pointer;
      }}
    }}

    @media (min-width: 769px) {{
      .mobile-next {{ display: none; }}
    }}
  </style>
</head>

<body>
  <div id="stage">
    <div id="frame"></div>
    <div id="plan">
      <div id="outer"></div>

      <div id="wrap">
        <div id="app">

          <div class="col-left">
            <div class="logo">
              <img src="https://files.catbox.moe/056m6v.jpg" alt="Logo">
            </div>
            <div class="blk desc">
              <p>Bienvenido al portal oficial de registro de SYNTRA.</p>
              <p>Aquí los socorristas podrán completar su inscripción de forma segura y acceder posteriormente a sus horarios e instalaciones asignadas de manera organizada.</p>
              <p>La información proporcionada será tratada con estricta confidencialidad y utilizada únicamente para fines administrativos y de coordinación interna relacionados con su participación en SYNTRA.</p>
              <p>Sus datos no serán compartidos con terceros sin su autorización, salvo obligación legal.</p>
            </div>
          </div>

          <div class="col-right">
            <div class="mobile-logo">
              <img src="https://files.catbox.moe/056m6v.jpg" alt="Logo">
            </div>

            <div class="blk hdr">Formulario</div>

            <div class="form-shell">
              <div class="form-scroll">

                <div class="row-top">
                  <input type="text" id="fomul" class="pill-input" readonly>
                </div>

                <div class="grid-2">

                  <div class="stack">
                    <div class="qrow"><div class="label">NOMBRE:</div><input id="nombre" class="input" type="text" autocomplete="name"/></div>
                    <div class="qrow"><div class="label">DNI:</div><input id="dni" class="input" type="text" /></div>
                    <div class="qrow"><div class="label">NACION:</div><input id="nacion" class="input" type="text" /></div>
                    <div class="qrow"><div class="label">NAFF:</div><input id="naff" class="input" type="text" /></div>
                    <div class="qrow"><div class="label">CALLE:</div><input id="calle" class="input" type="text" /></div>
                    <div class="qrow"><div class="label">POBL:</div><input id="pobl" class="input" type="text" /></div>
                    <div class="qrow"><div class="label">COMARCA:</div><input id="comarca" class="input" type="text" /></div>
                    <div class="qrow"><div class="label">C.P:</div><input id="cp" class="input" type="text" /></div>
                  </div>

                  <div class="stack-right">
                    <div class="qrow"><div class="label small">TLF:</div><input id="tlf" class="input" type="text" inputmode="tel" /></div>
                    <div class="qrow"><div class="label small">CORREO:</div><input id="correo" class="input" type="email" autocomplete="email"/></div>
                    <div class="qrow"><div class="label">NACIMIENTO:</div><input id="nacimiento" class="input" type="text" placeholder="dd/mm/aaaa"/></div>
                    <div class="qrow"><div class="label">ESTADO CIV:</div><input id="estado_civ" class="input" type="text" /></div>
                    <div class="qrow"><div class="label small">IBAN:</div><input id="iban" class="input" type="text" /></div>

                    <div class="pink-block">
                      <div class="pink-title">INSTALACION:</div>
                      <input id="instalacion" class="pink-input" type="text" />
                    </div>

                    <div class="pink-block">
                      <div class="pink-title">FECHA FIN:</div>
                      <input id="fecha_fin" class="pink-input" type="text" placeholder="dd/mm/aaaa" />
                    </div>

                    <div class="qrow"><div class="label">HORAS:</div><input id="horas" class="input" type="text" /></div>
                  </div>

                </div>

                <div class="terms-inside" style="margin-top: 20px;">
                  <input id="terms" type="checkbox" />
                  <span>Acepta términos y condiciones</span>
                </div>

                <div class="desktop-register">
                  <button id="btnDesktop" class="register-btn">Registro</button>
                </div>

              </div>
            </div>

            <div id="btnMobile" class="mobile-next">Registro</div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <script>
    (function() {{
      function ddmmyyyy(d) {{
        const dia = String(d.getDate()).padStart(2, '0');
        const mes = String(d.getMonth() + 1).padStart(2, '0');
        const ano = d.getFullYear();
        return `${{dia}}/${{mes}}/${{ano}}`;
      }}

      function setFomulHoy() {{
        const hoy = new Date();
        const el = document.getElementById('fomul');
        if (el) el.value = ddmmyyyy(hoy);
      }}

      function getVal(id) {{
        const el = document.getElementById(id);
        return el ? (el.value || '').trim() : '';
      }}

      function setDisabled(disabled) {{
        const bd = document.getElementById('btnDesktop');
        if (bd) bd.disabled = disabled;

        const bm = document.getElementById('btnMobile');
        if (bm) {{
          bm.style.pointerEvents = disabled ? 'none' : 'auto';
          bm.style.opacity = disabled ? '0.55' : '1';
        }}
      }}

      function validateAll() {{
        const requiredIds = [
          'fomul','nombre','dni','nacion','naff','calle','pobl','comarca','cp',
          'tlf','correo','nacimiento','estado_civ','iban','instalacion','fecha_fin','horas'
        ];

        for (const id of requiredIds) {{
          const v = getVal(id);
          if (!v) return {{ ok:false, msg:`Completa el campo: ${{id.toUpperCase()}}` }};
        }}

        const terms = document.getElementById('terms');
        if (!terms || !terms.checked) return {{ ok:false, msg:'Debes aceptar términos y condiciones' }};

        return {{ ok:true }};
      }}

      function goAdminPageViaSidebarLink() {{
        // Streamlit bloquea navegación "top" desde iframe sandbox.
        // Solución: encontrar el link real de la navegación multipage (aunque esté oculto) y disparar click.
        try {{
          const pdoc = window.parent.document;
          const links = Array.from(pdoc.querySelectorAll('a[href]'));

          // 1) prioriza href que contenga "admin"
          let target = links.find(a => (a.getAttribute('href') || '').toLowerCase().includes('admin'));

          // 2) fallback: por texto visible
          if (!target) {{
            target = links.find(a => (a.textContent || '').trim().toLowerCase() === 'admin');
          }}

          if (target) {{
            target.click();
            return true;
          }}
        }} catch (e) {{}}

        return false;
      }}

      async function enviarRegistro() {{
        const v = validateAll();
        if (!v.ok) {{
          alert(v.msg);
          return;
        }}

        setDisabled(true);

        const payload = {{
          "FOMUL": getVal('fomul'),
          "NOMBRE": getVal('nombre'),
          "DNI": getVal('dni'),
          "NACION": getVal('nacion'),
          "NAFF": getVal('naff'),
          "CALLE": getVal('calle'),
          "POBL": getVal('pobl'),
          "COMARCA": getVal('comarca'),
          "C.P": getVal('cp'),
          "TLF": getVal('tlf'),
          "CORREO": getVal('correo'),
          "NACIMIENTO": getVal('nacimiento'),
          "ESTADO CIV": getVal('estado_civ'),
          "IBAN": getVal('iban'),
          "INSTALACION": getVal('instalacion'),
          "FECHA FIN": getVal('fecha_fin'),
          "HORAS": getVal('horas')
        }};

        try {{
          const resp = await fetch("{API_URL}", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify(payload)
          }});

          const data = await resp.json().catch(() => ({{}}));

          if (data && data.ok) {{
            const okNav = goAdminPageViaSidebarLink();
            if (!okNav) {{
              alert("Guardado, pero no se pudo redirigir automáticamente. Abre ADMIN desde el menú.");
            }}
          }} else {{
            const err = (data && (data.error || data.detail)) ? (data.error || data.detail) : "Error al guardar";
            alert(err);
          }}
        }} catch (e) {{
          alert("Error de conexión");
        }} finally {{
          setDisabled(false);
        }}
      }}

      function bind() {{
        const bd = document.getElementById('btnDesktop');
        if (bd) bd.addEventListener('click', enviarRegistro);

        const bm = document.getElementById('btnMobile');
        if (bm) bm.addEventListener('click', enviarRegistro);
      }}

      setFomulHoy();
      bind();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
