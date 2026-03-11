# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Asignacion Horarios Socorristas", layout="wide")

# =========================
# HTML UI (RESPONSIVE) con integración real a Mallas
# =========================
html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{
      --baseBlue:#040e31;
      --bgTop:#0a1a55;
      --bgMid:#061240;
      --bgDeep:#02071c;

      --overlay1:rgba(40,120,255,.16);
      --overlay2:rgba(0,10,40,.62);

      --ink:rgba(255,255,255,.92);
      --muted:rgba(255,255,255,.68);

      --btn1:#2f7de1;
      --btn2:#1e5fc4;
      --btnGreen1:#2f9b62;
      --btnGreen2:#1f7d4d;
      --btnRed1:#d44b56;
      --btnRed2:#af2431;

      --shadow1:0 22px 55px rgba(0,0,0,.55);
      --shadow2:0 10px 22px rgba(0,0,0,.40);
      --shadow3:0 18px 30px rgba(0,0,0,.28);
      --blur:14px;

      --softBorder:1px solid rgba(255,255,255,.12);
      --softBorder2:1px solid rgba(255,255,255,.16);
      --panel:rgba(255,255,255,.04);

      --radiusDesk:34px;
      --radiusMob:24px;
      --hdrHDesk:54px;
      --hdrHMob:44px;
      --font:ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif;
      --modal-overlay:rgba(0,0,0,.58);
    }

    *{ box-sizing:border-box; }

    html, body{
      margin:0;
      padding:0;
      width:100%;
      min-height:100%;
      background:var(--baseBlue);
      font-family:var(--font);
      color:var(--ink);
      overflow-x:hidden;
      overflow-y:auto;
      -webkit-font-smoothing:antialiased;
      -moz-osx-font-smoothing:grayscale;
    }

    body{
      position:relative;
    }

    #stage{
      position:relative;
      width:100%;
      min-height:100vh;
      background:
        radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
        linear-gradient(180deg, #020614 0%, var(--baseBlue) 100%);
      padding:10px;
    }

    #plan{
      position:relative;
      width:100%;
      min-height:calc(100vh - 20px);
      overflow:hidden;
      border-radius:34px;
      box-shadow:var(--shadow1);
      background:
        linear-gradient(180deg, rgba(255,255,255,.16) 0%, transparent 22%),
        linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #05164d 58%, var(--bgDeep) 100%);
    }

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
      transform:rotate(-10deg);
      opacity:.95;
      pointer-events:none;
    }

    #plan::after{
      content:"";
      position:absolute;
      inset:0;
      background:
        radial-gradient(50% 60% at 50% 20%, rgba(255,255,255,.06), transparent 55%),
        radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
        linear-gradient(180deg, transparent 55%, rgba(0,0,0,.65) 100%);
      pointer-events:none;
    }

    #frame{
      position:absolute;
      left:9px;
      right:9px;
      top:10px;
      bottom:10px;
      border-left:2px solid rgba(255,255,255,.14);
      border-right:2px solid rgba(255,255,255,.14);
      border-top:2px solid rgba(255,255,255,.14);
      box-sizing:border-box;
      pointer-events:none;
      border-radius:34px;
      box-shadow:inset 0 0 0 1px rgba(0,0,0,.55);
      z-index:5;
    }

    #outer{
      position:absolute;
      left:10px;
      right:10px;
      top:10px;
      bottom:10px;
      border:1px solid rgba(255,255,255,.10);
      box-sizing:border-box;
      background:transparent;
      border-radius:34px;
      backdrop-filter:blur(var(--blur));
      -webkit-backdrop-filter:blur(var(--blur));
      z-index:10;
      pointer-events:none;
    }

    #wrap{
      position:relative;
      z-index:20;
      width:100%;
      min-height:calc(100vh - 20px);
      padding:20px;
    }

    .shell{
      width:100%;
      max-width:1320px;
      margin:0 auto;
      display:flex;
      flex-direction:column;
      gap:12px;
    }

    .title{
      min-height:var(--hdrHDesk);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:800;
      font-size:18px;
      letter-spacing:.3px;
      position:relative;
      background:rgba(255,255,255,.04);
      border:var(--softBorder);
      border-radius:24px;
      backdrop-filter:blur(calc(var(--blur) - 6px));
      color:var(--ink);
      text-shadow:0 8px 18px rgba(0,0,0,.35);
      padding:14px 18px;
    }

    .title::after{
      content:"";
      position:absolute;
      left:14px;
      right:14px;
      bottom:10px;
      height:2px;
      background:linear-gradient(90deg, transparent, rgba(255,255,255,.4), transparent);
    }

    .content{
      display:flex;
      flex-direction:column;
      gap:12px;
    }

    .panel{
      border:var(--softBorder);
      background:var(--panel);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      -webkit-backdrop-filter:blur(calc(var(--blur) - 6px));
      border-radius:24px;
      box-shadow:var(--shadow2), inset 0 1px 0 rgba(255,255,255,.08);
    }

    .top-actions{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:12px;
    }

    .btn{
      border:var(--softBorder);
      border-radius:18px;
      padding:14px 16px;
      color:var(--ink);
      font-weight:800;
      cursor:pointer;
      display:flex;
      align-items:center;
      justify-content:center;
      gap:10px;
      box-shadow:var(--shadow3), inset 0 1px 0 rgba(255,255,255,.18);
      user-select:none;
      width:100%;
      min-width:0;
      text-transform:uppercase;
      letter-spacing:.5px;
      transition:transform .12s ease, filter .12s ease, opacity .12s ease;
    }

    .btn:hover{ filter:brightness(1.06); }
    .btn:active{ transform:scale(.985); }

    .btn .ico{
      width:18px;
      height:18px;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      filter:drop-shadow(0 2px 2px rgba(0,0,0,.18));
    }

    .btn.green{
      background:linear-gradient(180deg, var(--btnGreen1) 0%, var(--btnGreen2) 100%);
    }

    .btn.red{
      background:linear-gradient(180deg, var(--btnRed1) 0%, var(--btnRed2) 100%);
    }

    .agregar-section{
      padding:14px;
      background:rgba(255,255,255,.04);
    }

    .agregar-title{
      font-weight:900;
      font-size:16px;
      margin-bottom:10px;
      color:var(--ink);
      text-shadow:0 6px 14px rgba(0,0,0,.30);
    }

    .agregar-row{
      display:flex;
      gap:10px;
      align-items:flex-end;
      flex-wrap:wrap;
    }

    .agregar-field{
      flex:1 1 160px;
      min-width:145px;
    }

    .agregar-field label,
    .field label{
      display:block;
      font-size:12px;
      font-weight:800;
      color:var(--ink);
      margin:0 0 6px;
      letter-spacing:.2px;
    }

    .agregar-field input,
    select,
    .searchbtn,
    .modal-field input{
      width:100%;
      border:1px solid rgba(255,255,255,.15);
      background:rgba(0,0,0,.22);
      color:var(--ink);
      border-radius:12px;
      padding:11px 12px;
      font-size:14px;
      outline:none;
      min-width:0;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.04);
    }

    .agregar-field input::placeholder,
    .modal-field input::placeholder{
      color:rgba(255,255,255,.45);
    }

    .agregar-field input:focus,
    select:focus,
    .searchbtn:focus,
    .modal-field input:focus{
      border-color:rgba(255,255,255,.35);
      box-shadow:0 0 0 3px rgba(47,125,225,.14);
    }

    select{
      appearance:none;
      -webkit-appearance:none;
      -moz-appearance:none;
      font-weight:700;
      background-image:
        linear-gradient(45deg, transparent 50%, rgba(255,255,255,.85) 50%),
        linear-gradient(135deg, rgba(255,255,255,.85) 50%, transparent 50%);
      background-position:
        calc(100% - 18px) calc(50% - 3px),
        calc(100% - 12px) calc(50% - 3px);
      background-size:6px 6px, 6px 6px;
      background-repeat:no-repeat;
      padding-right:32px;
    }

    option{
      color:#111;
    }

    .agregar-btn,
    .searchbtn{
      border:var(--softBorder);
      background:linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      color:var(--ink);
      font-weight:800;
      cursor:pointer;
      border-radius:14px;
      box-shadow:var(--shadow3), inset 0 1px 0 rgba(255,255,255,.18);
      transition:transform .12s ease, filter .12s ease;
    }

    .agregar-btn{
      padding:11px 20px;
      min-width:150px;
      height:44px;
    }

    .searchbtn{
      height:44px;
    }

    .agregar-btn:hover,
    .searchbtn:hover{
      filter:brightness(1.06);
    }

    .agregar-btn:active,
    .searchbtn:active{
      transform:scale(.985);
    }

    .rango-opciones{
      display:flex;
      gap:8px;
      margin-top:10px;
      flex-wrap:wrap;
    }

    .rango-btn{
      background:rgba(255,255,255,.06);
      border:1px solid rgba(255,255,255,.14);
      color:var(--ink);
      padding:8px 12px;
      font-weight:700;
      cursor:pointer;
      border-radius:999px;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
      transition:transform .12s ease, filter .12s ease, background .12s ease;
    }

    .rango-btn:hover{ filter:brightness(1.08); }
    .rango-btn:active{ transform:scale(.985); }

    .rango-btn.activo{
      background:linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      color:var(--ink);
      border-color:rgba(255,255,255,.20);
    }

    .help-text{
      color:var(--muted);
      font-size:12px;
      margin-top:8px;
      display:block;
    }

    .section{
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    .section-head{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      min-width:0;
    }

    .subtitle{
      font-weight:900;
      font-size:18px;
      color:var(--ink);
      min-width:0;
      text-shadow:0 8px 18px rgba(0,0,0,.35);
    }

    .filters{
      display:grid;
      grid-template-columns:260px 1fr 1fr 160px;
      gap:10px;
      align-items:end;
      min-width:0;
      padding:14px;
    }

    .table-card{
      padding:12px;
      display:flex;
      flex-direction:column;
      overflow:visible;
    }

    .table-title{
      font-weight:900;
      margin-bottom:8px;
      color:var(--ink);
    }

    .tablewrap{
      width:100%;
      overflow:auto;
      border:1px solid rgba(255,255,255,.10);
      border-radius:18px;
      background:rgba(0,0,0,.14);
      box-shadow:inset 0 1px 0 rgba(255,255,255,.05);
    }

    table{
      width:100%;
      border-collapse:separate;
      border-spacing:0;
      font-size:13px;
      min-width:700px;
    }

    thead th{
      text-align:left;
      padding:12px 10px;
      border-bottom:1px solid rgba(255,255,255,.12);
      font-weight:900;
      white-space:nowrap;
      color:rgba(255,255,255,.92);
      background:rgba(255,255,255,.05);
      position:sticky;
      top:0;
      z-index:2;
      backdrop-filter:blur(8px);
    }

    thead th:first-child{ border-top-left-radius:14px; }
    thead th:last-child{ border-top-right-radius:14px; }

    tbody td{
      padding:12px 10px;
      border-bottom:1px solid rgba(255,255,255,.08);
      vertical-align:middle;
      font-weight:600;
      white-space:nowrap;
      color:rgba(255,255,255,.88);
    }

    tbody tr:hover td{
      background:rgba(255,255,255,.04);
    }

    .actions{
      display:flex;
      gap:8px;
      align-items:center;
      justify-content:flex-start;
    }

    .iconbtn{
      width:30px;
      height:30px;
      border:1px solid rgba(255,255,255,.14);
      background:rgba(255,255,255,.06);
      border-radius:10px;
      cursor:pointer;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      flex:0 0 auto;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
      transition:transform .12s ease, filter .12s ease, background .12s ease;
    }

    .iconbtn:hover{
      background:rgba(255,255,255,.12);
      filter:brightness(1.05);
    }

    .iconbtn:active{
      transform:scale(.96);
    }

    .icon{
      width:16px;
      height:16px;
      display:block;
    }

    .pagerbar{
      width:100%;
      display:flex;
      align-items:center;
      justify-content:flex-end;
      gap:10px;
      margin-top:10px;
      padding-right:2px;
      overflow:hidden;
    }

    .showing{
      font-size:12px;
      color:var(--muted);
      font-weight:800;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
      max-width:55%;
    }

    .pager{
      display:inline-flex;
      align-items:center;
      gap:6px;
      flex:0 0 auto;
      max-width:45%;
    }

    .pgbtn{
      height:30px;
      border:1px solid rgba(255,255,255,.14);
      background:rgba(255,255,255,.06);
      color:var(--ink);
      border-radius:10px;
      cursor:pointer;
      font-weight:900;
      padding:0 12px;
      white-space:nowrap;
      min-width:36px;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
    }

    .pgbtn:hover:not(:disabled){
      background:rgba(255,255,255,.12);
    }

    .pgbtn:disabled{
      opacity:.45;
      cursor:not-allowed;
    }

    .pgbtn.prev{
      padding:0;
      width:30px;
      display:inline-flex;
      align-items:center;
      justify-content:center;
    }

    .pgcur{
      width:30px;
      height:30px;
      border-radius:10px;
      background:linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      color:#fff;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      font-size:12px;
      flex:0 0 auto;
      box-shadow:var(--shadow3), inset 0 1px 0 rgba(255,255,255,.18);
    }

    .modal-overlay{
      display:none;
      position:fixed;
      top:0;
      left:0;
      width:100%;
      height:100%;
      background:var(--modal-overlay);
      align-items:center;
      justify-content:center;
      z-index:1000;
      padding:16px;
    }

    .modal{
      background:
        linear-gradient(180deg, rgba(255,255,255,.12) 0%, rgba(255,255,255,.03) 100%),
        linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 44%, var(--bgDeep) 100%);
      border:1px solid rgba(255,255,255,.14);
      padding:22px;
      max-width:420px;
      width:100%;
      box-shadow:var(--shadow1);
      border-radius:24px;
      backdrop-filter:blur(var(--blur));
      -webkit-backdrop-filter:blur(var(--blur));
      color:var(--ink);
    }

    .modal h3{
      margin:0 0 16px 0;
      font-weight:900;
      font-size:20px;
      text-shadow:0 8px 18px rgba(0,0,0,.35);
    }

    .modal-field{
      margin-bottom:14px;
    }

    .modal-field label{
      display:block;
      font-weight:800;
      font-size:12px;
      margin-bottom:6px;
      color:var(--ink);
    }

    .modal-actions{
      display:flex;
      justify-content:flex-end;
      gap:10px;
      margin-top:20px;
    }

    .modal-actions button{
      padding:10px 16px;
      border:1px solid rgba(255,255,255,.14);
      font-weight:800;
      cursor:pointer;
      border-radius:12px;
      color:var(--ink);
      transition:transform .12s ease, filter .12s ease;
      box-shadow:var(--shadow3), inset 0 1px 0 rgba(255,255,255,.18);
    }

    .modal-actions button:hover{ filter:brightness(1.06); }
    .modal-actions button:active{ transform:scale(.985); }

    .modal-actions .cancel{
      background:rgba(255,255,255,.10);
    }

    .modal-actions .save{
      background:linear-gradient(180deg, var(--btnGreen1) 0%, var(--btnGreen2) 100%);
    }

    .col-finaliza{
      display:none;
    }

    @media (max-width: 900px){
      #stage{
        padding:6px;
      }

      #plan{
        min-height:calc(100vh - 12px);
        border-radius:24px;
      }

      #frame{
        left:6px;
        right:6px;
        top:6px;
        bottom:6px;
        border-radius:24px;
      }

      #outer{
        left:6px;
        right:6px;
        top:6px;
        bottom:6px;
        border-radius:24px;
      }

      #wrap{
        min-height:calc(100vh - 12px);
        padding:12px;
      }

      .top-actions{
        grid-template-columns:1fr;
      }

      .filters{
        grid-template-columns:1fr 1fr;
      }
    }

    @media (max-width: 768px){
      #stage{
        padding:6px;
      }

      #plan{
        min-height:calc(100vh - 12px);
        border-radius:22px;
      }

      #frame{
        left:6px;
        right:6px;
        top:6px;
        bottom:6px;
        border-radius:22px;
      }

      #outer{
        left:6px;
        right:6px;
        top:6px;
        bottom:6px;
        border-radius:22px;
      }

      #wrap{
        min-height:calc(100vh - 12px);
        padding:8px;
      }

      .shell{
        gap:8px;
      }

      .title{
        min-height:var(--hdrHMob);
        font-size:16px;
        border-radius:18px;
        padding:12px 14px;
      }

      .title::after{
        left:18px;
        right:18px;
        bottom:7px;
      }

      .agregar-section{
        padding:10px 10px 9px 10px;
        border-radius:18px;
      }

      .agregar-title{
        font-size:15px;
        margin-bottom:6px;
      }

      .agregar-row{
        display:block;
      }

      .agregar-field{
        margin-bottom:4px;
        min-width:0;
      }

      .agregar-field label{
        font-size:12px;
        margin-bottom:2px;
      }

      .agregar-field input{
        padding:8px 10px;
        font-size:14px;
        height:38px;
      }

      .agregar-btn{
        width:100%;
        margin-top:4px;
        height:40px;
        padding:8px 12px;
        font-size:14px;
      }

      .rango-opciones{
        gap:5px;
        margin-top:6px;
      }

      .rango-btn{
        padding:5px 10px;
        font-size:12px;
      }

      .filters{
        grid-template-columns:1fr;
        padding:10px;
        gap:8px;
      }

      .searchbtn{
        height:40px;
      }

      .table-card{
        padding:8px;
        border-radius:18px;
      }

      table{
        min-width:0;
        width:100%;
        font-size:12px;
      }

      .col-instalacion,
      .col-socorrista,
      .col-horas{
        display:none;
      }

      thead th.col-instalacion,
      thead th.col-socorrista,
      thead th.col-horas{
        display:none;
      }

      .col-finaliza{
        display:table-cell;
      }

      thead th.col-finaliza{
        display:table-cell;
      }

      th:nth-child(5),
      td:nth-child(5){
        min-width:60px;
        text-align:left;
        padding-left:4px;
        padding-right:4px;
      }

      th:nth-child(7),
      td:nth-child(7){
        min-width:80px;
        text-align:left;
        padding-left:8px;
        vertical-align:middle;
      }

      td:nth-child(7) .actions{
        justify-content:flex-start;
        gap:6px;
        align-items:center;
      }

      .iconbtn{
        width:24px;
        height:24px;
        border-radius:8px;
      }

      .iconbtn .icon{
        width:14px;
        height:14px;
      }

      .table-title{
        display:none;
      }

      .pagerbar{
        gap:8px;
        flex-wrap:wrap;
        justify-content:space-between;
      }

      .showing{
        max-width:100%;
      }

      .pager{
        max-width:100%;
      }
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="plan">
      <div id="frame"></div>
      <div id="outer"></div>

      <div id="wrap">
        <div class="shell">

          <div class="title">Asignacion Horarios Socorristas</div>

          <div class="content">

            <div class="top-actions">
              <button class="btn green" id="btnPlantillas" type="button">
                <span class="ico">⬇️</span>
                <span>Descargar Plantilla</span>
              </button>

              <button class="btn red" id="btnSubir" type="button">
                <span class="ico">⬆️</span>
                <span>Subir Horarios Masivos</span>
              </button>
            </div>

            <div class="panel agregar-section">
              <div class="agregar-title">➕ Agregar desde bloque</div>

              <div class="agregar-row">
                <div class="agregar-field">
                  <label for="fechaInicio">Fecha inicio (dd/mm/aaaa)</label>
                  <input type="text" id="fechaInicio" placeholder="ej. 17/01/2025" value="">
                </div>

                <div class="agregar-field">
                  <label for="fechaFin">Fecha fin (dd/mm/aaaa)</label>
                  <input type="text" id="fechaFin" placeholder="ej. 23/01/2025" value="">
                </div>

                <div class="agregar-field">
                  <label for="bloqueInput">Número de bloque</label>
                  <input type="number" id="bloqueInput" placeholder="ej. 1" min="1" value="">
                </div>

                <button class="agregar-btn" id="btnAgregarRango" type="button">Agregar rango</button>
              </div>

              <div class="rango-opciones">
                <button class="rango-btn" data-rango="dia" type="button">Día</button>
                <button class="rango-btn" data-rango="semana" type="button">Semana</button>
                <button class="rango-btn" data-rango="mes" type="button">Mes</button>
              </div>

              <small class="help-text">Seleccione un rango o ingrese las fechas manualmente.</small>
            </div>

            <div class="section">
              <div class="section-head">
                <div class="subtitle">Horarios de Socorristas</div>
              </div>

              <div class="panel filters">
                <div class="field">
                  <label for="modeSel">Modo</label>
                  <select id="modeSel">
                    <option value="Individual">Individual</option>
                    <option value="Cargar Plantilla">Cargar Plantilla</option>
                  </select>
                </div>

                <div class="field">
                  <label for="instSel">Instalación</label>
                  <select id="instSel"></select>
                </div>

                <div class="field">
                  <label for="socSel">Socorrista</label>
                  <select id="socSel"></select>
                </div>

                <div class="field">
                  <label>&nbsp;</label>
                  <button class="searchbtn" id="btnBuscar" type="button">Buscar</button>
                </div>
              </div>

              <div class="panel table-card">
                <div class="table-title">Tabla Horarios</div>

                <div class="tablewrap">
                  <table>
                    <thead>
                      <tr>
                        <th class="col-instalacion">Instalacion</th>
                        <th class="col-socorrista">Socorrista</th>
                        <th>Día</th>
                        <th>Inicio</th>
                        <th class="col-finaliza">Finaliza</th>
                        <th class="col-horas">Horas</th>
                        <th>Estado</th>
                        <th style="display:none;">llave</th>
                      </tr>
                    </thead>
                    <tbody id="tbody"></tbody>
                  </table>
                </div>

                <div class="pagerbar">
                  <span class="showing" id="showingTxt">Mostrando 0 a 0 de 0</span>
                  <div class="pager">
                    <button class="pgbtn prev" id="pgPrev" type="button">‹</button>
                    <span class="pgcur" id="pgCur">1</span>
                    <button class="pgbtn" id="pgNext" type="button">Siguiente</button>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal-overlay" id="editModal">
    <div class="modal">
      <h3>Editar turno</h3>

      <div class="modal-field">
        <label for="editSocorrista">Socorrista</label>
        <input type="text" id="editSocorrista">
      </div>

      <div class="modal-field">
        <label for="editInstalacion">Instalacion</label>
        <input type="text" id="editInstalacion">
      </div>

      <div class="modal-field">
        <label for="editIngreso">Ingreso</label>
        <input type="text" id="editIngreso" placeholder="HH:MM">
      </div>

      <div class="modal-field">
        <label for="editSalida">Salida</label>
        <input type="text" id="editSalida" placeholder="HH:MM">
      </div>

      <div class="modal-actions">
        <button class="cancel" id="modalCancel" type="button">Cancelar</button>
        <button class="save" id="modalSave" type="button">Guardar</button>
      </div>
    </div>
  </div>

  <script>
    (function() {
      const API_BASE = "https://camilo27.pythonanywhere.com";
      const ENDPOINT_MALLAS = API_BASE + "/api/mallas";
      const ENDPOINT_AGREGAR = API_BASE + "/api/horarios/agregar";
      const ENDPOINT_EDITAR = API_BASE + "/api/horarios/editar";
      const ENDPOINT_ELIMINAR = API_BASE + "/api/horarios/eliminar";

      function getField(row, keys) {
        if (!row) return "";
        for (const k of keys) {
          if (Object.prototype.hasOwnProperty.call(row, k)) {
            const val = row[k];
            if (val !== undefined && val !== null) return val;
          }
        }
        return "";
      }

      let allRows = [];
      let filtered = [];
      let page = 1;
      const pageSize = 14;

      const instSel = document.getElementById("instSel");
      const socSel = document.getElementById("socSel");
      const tbody = document.getElementById("tbody");
      const showingTxt = document.getElementById("showingTxt");
      const pgCur = document.getElementById("pgCur");
      const pgPrev = document.getElementById("pgPrev");
      const pgNext = document.getElementById("pgNext");
      const btnBuscar = document.getElementById("btnBuscar");

      const fechaInicio = document.getElementById("fechaInicio");
      const fechaFin = document.getElementById("fechaFin");
      const bloqueInput = document.getElementById("bloqueInput");
      const btnAgregarRango = document.getElementById("btnAgregarRango");
      const rangoBtns = document.querySelectorAll(".rango-btn");

      const editModal = document.getElementById("editModal");
      const editSocorrista = document.getElementById("editSocorrista");
      const editInstalacion = document.getElementById("editInstalacion");
      const editIngreso = document.getElementById("editIngreso");
      const editSalida = document.getElementById("editSalida");
      const modalCancel = document.getElementById("modalCancel");
      const modalSave = document.getElementById("modalSave");

      let currentEditLlave = null;

      function svgEdit() {
        return '<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M12 20h9" stroke="rgba(255,255,255,.92)" stroke-width="2" stroke-linecap="round"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4 11.5-11.5Z" stroke="rgba(255,255,255,.92)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      }

      function svgTrash() {
        return '<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M3 6h18" stroke="rgba(255,255,255,.92)" stroke-width="2" stroke-linecap="round"/><path d="M8 6V4h8v2" stroke="rgba(255,255,255,.92)" stroke-width="2" stroke-linecap="round"/><path d="M19 6l-1 14H6L5 6" stroke="rgba(255,255,255,.92)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11v6" stroke="rgba(255,255,255,.92)" stroke-width="2" stroke-linecap="round"/><path d="M14 11v6" stroke="rgba(255,255,255,.92)" stroke-width="2" stroke-linecap="round"/></svg>';
      }

      function parseFechaDDMMYYYY(fechaStr) {
        if (!/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(fechaStr)) return null;
        const [dd, mm, yyyy] = fechaStr.split('/').map(Number);
        return new Date(yyyy, mm - 1, dd);
      }

      function formatDateToDDMMYYYY(date) {
        const d = date.getDate().toString().padStart(2, '0');
        const m = (date.getMonth() + 1).toString().padStart(2, '0');
        const y = date.getFullYear();
        return `${d}/${m}/${y}`;
      }

      function getDatesInRange(startStr, endStr) {
        const start = parseFechaDDMMYYYY(startStr);
        const end = parseFechaDDMMYYYY(endStr);
        if (!start || !end) return [];
        const dates = [];
        let current = new Date(start);
        while (current <= end) {
          dates.push(formatDateToDDMMYYYY(current));
          current.setDate(current.getDate() + 1);
        }
        return dates;
      }

      async function loadMallas() {
        try {
          const res = await fetch(ENDPOINT_MALLAS);
          if (!res.ok) throw new Error("Error HTTP " + res.status);
          const data = await res.json();
          if (!data.ok) throw new Error("Respuesta no ok");

          allRows = data.rows || [];

          const instalacionesSet = new Set();
          const socorristasSet = new Set();

          allRows.forEach(r => {
            const inst = getField(r, ["Instalacion", "Instalación", "instalacion"]);
            if (inst) instalacionesSet.add(inst);

            const soc = getField(r, ["Socorrista", "socorrista"]);
            if (soc) socorristasSet.add(soc);
          });

          const instalaciones = Array.from(instalacionesSet).sort();
          const socorristas = Array.from(socorristasSet).sort();

          fillSelect(instSel, ["Todas", ...instalaciones]);
          fillSelect(socSel, ["Todos", ...socorristas]);
          applyFilters();
        } catch (e) {
          console.error("Error cargando mallas:", e);
          allRows = [];
          fillSelect(instSel, ["Todas"]);
          fillSelect(socSel, ["Todos"]);
          applyFilters();
        }
      }

      function fillSelect(sel, items) {
        sel.innerHTML = "";
        items.forEach(v => {
          const opt = document.createElement("option");
          opt.value = v;
          opt.textContent = v;
          sel.appendChild(opt);
        });
      }

      function applyFilters() {
        const inst = instSel.value || "Todas";
        const soc = socSel.value || "Todos";

        filtered = allRows.filter(r => {
          const okInst = (inst === "Todas") || (getField(r, ["Instalacion", "Instalación", "instalacion"]) === inst);
          const okSoc = (soc === "Todos") || (getField(r, ["Socorrista", "socorrista"]) === soc);
          return okInst && okSoc;
        });

        page = 1;
        render();
      }

      function render() {
        const total = filtered.length;
        const pages = Math.max(1, Math.ceil(total / pageSize));
        page = Math.min(page, pages);

        const startIdx = (page - 1) * pageSize;
        const endIdx = Math.min(startIdx + pageSize, total);

        tbody.innerHTML = "";
        const slice = filtered.slice(startIdx, endIdx);

        slice.forEach((r) => {
          const tr = document.createElement("tr");
          tr.dataset.llave = r.llave || "";

          const tdInst = document.createElement("td");
          tdInst.className = "col-instalacion";
          tdInst.textContent = getField(r, ["Instalacion", "Instalación", "instalacion"]) || "";

          const tdSoc = document.createElement("td");
          tdSoc.className = "col-socorrista";
          tdSoc.textContent = getField(r, ["Socorrista", "socorrista"]) || "";

          const tdDia = document.createElement("td");
          tdDia.textContent = getField(r, ["Dia", "día", "dia"]) || "";

          const tdInicio = document.createElement("td");
          tdInicio.textContent = getField(r, ["Ingreso", "Inicio", "ingreso", "inicio"]) || "";

          const tdFinaliza = document.createElement("td");
          tdFinaliza.className = "col-finaliza";
          const salida = getField(r, ["Salida", "salida", "SALIDA", "Finaliza", "finaliza", "FINALIZA"]);
          tdFinaliza.textContent = salida || "";

          const tdHoras = document.createElement("td");
          tdHoras.className = "col-horas";
          tdHoras.textContent = getField(r, ["Intensidad_horaria", "Intensidad_ho", "Horas", "horas"]) || "";

          const tdEstado = document.createElement("td");
          const wrap = document.createElement("div");
          wrap.className = "actions";

          const b1 = document.createElement("button");
          b1.className = "iconbtn";
          b1.type = "button";
          b1.innerHTML = svgEdit();
          b1.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!r.llave) {
              alert("Este turno no tiene una llave válida. No se puede editar.");
              return;
            }
            openEditModal(r);
          });

          const b2 = document.createElement("button");
          b2.className = "iconbtn";
          b2.type = "button";
          b2.innerHTML = svgTrash();
          b2.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!r.llave) {
              alert("Este turno no tiene una llave válida. No se puede eliminar.");
              return;
            }
            if (confirm("¿Está seguro de eliminar este turno?")) {
              eliminarTurno(r.llave);
            }
          });

          wrap.appendChild(b1);
          wrap.appendChild(b2);
          tdEstado.appendChild(wrap);

          const tdLlave = document.createElement("td");
          tdLlave.style.display = "none";
          tdLlave.textContent = r.llave || "";

          tr.appendChild(tdInst);
          tr.appendChild(tdSoc);
          tr.appendChild(tdDia);
          tr.appendChild(tdInicio);
          tr.appendChild(tdFinaliza);
          tr.appendChild(tdHoras);
          tr.appendChild(tdEstado);
          tr.appendChild(tdLlave);

          tbody.appendChild(tr);
        });

        const showingA = total === 0 ? 0 : (startIdx + 1);
        const showingB = endIdx;
        showingTxt.textContent = `Mostrando ${showingA} a ${showingB} de ${total}`;
        pgCur.textContent = String(page);
        pgPrev.disabled = page <= 1;
        pgNext.disabled = page >= pages;
      }

      function openEditModal(row) {
        currentEditLlave = row.llave;
        editSocorrista.value = getField(row, ["Socorrista", "socorrista"]) || "";
        editInstalacion.value = getField(row, ["Instalacion", "Instalación", "instalacion"]) || "";
        editIngreso.value = getField(row, ["Ingreso", "Inicio", "ingreso", "inicio"]) || "";
        editSalida.value = getField(row, ["Salida", "salida", "Finaliza", "finaliza"]) || "";
        editModal.style.display = "flex";
      }

      function closeModal() {
        editModal.style.display = "none";
        currentEditLlave = null;
      }

      async function guardarEdicion() {
        if (!currentEditLlave) return;

        const payload = {
          llave: currentEditLlave,
          Socorrista: editSocorrista.value.trim(),
          Instalacion: editInstalacion.value.trim(),
          Ingreso: editIngreso.value.trim(),
          Salida: editSalida.value.trim()
        };

        try {
          const res = await fetch(ENDPOINT_EDITAR, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });

          const data = await res.json();

          if (data.ok) {
            closeModal();
            loadMallas();
          } else {
            alert("Error al editar: " + (data.error || "desconocido"));
          }
        } catch (e) {
          alert("Error de red al editar");
        }
      }

      async function eliminarTurno(llave) {
        try {
          const res = await fetch(ENDPOINT_ELIMINAR, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ llave: llave })
          });

          const data = await res.json();

          if (data.ok) {
            loadMallas();
          } else {
            alert("Error al eliminar: " + (data.error || "desconocido"));
          }
        } catch (e) {
          alert("Error de red al eliminar");
        }
      }

      async function agregarRango() {
        const inicio = fechaInicio.value.trim();
        const fin = fechaFin.value.trim();
        const bloque = bloqueInput.value.trim();

        if (!inicio || !fin || !bloque) {
          alert("Debe ingresar fecha inicio, fecha fin y bloque");
          return;
        }

        if (!/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(inicio) || !/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(fin)) {
          alert("Las fechas deben tener formato dd/mm/aaaa");
          return;
        }

        const fechas = getDatesInRange(inicio, fin);
        if (fechas.length === 0) {
          alert("Rango de fechas inválido");
          return;
        }

        const total = fechas.length;
        let exitos = 0;
        let errores = 0;

        for (let i = 0; i < total; i++) {
          const fecha = fechas[i];
          try {
            const res = await fetch(ENDPOINT_AGREGAR, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ fecha: fecha, bloque: bloque })
            });

            const data = await res.json();

            if (data.ok) {
              exitos++;
            } else {
              errores++;
              console.error("Error en fecha", fecha, data.error);
            }
          } catch (e) {
            errores++;
            console.error("Error de red en fecha", fecha, e);
          }

          await new Promise(r => setTimeout(r, 200));
        }

        alert(`Proceso completado: ${exitos} exitosos, ${errores} errores.`);

        if (exitos > 0) {
          fechaInicio.value = "";
          fechaFin.value = "";
          bloqueInput.value = "";
          rangoBtns.forEach(b => b.classList.remove("activo"));
          loadMallas();
        }
      }

      function setRango(tipo) {
        const hoy = new Date();
        let inicio = "";
        let fin = "";

        if (tipo === "dia") {
          inicio = formatDateToDDMMYYYY(hoy);
          fin = formatDateToDDMMYYYY(hoy);
        } else if (tipo === "semana") {
          const diaSem = hoy.getDay();
          const diffLunes = (diaSem === 0 ? 6 : diaSem - 1);
          const lunes = new Date(hoy);
          lunes.setDate(hoy.getDate() - diffLunes);
          const domingo = new Date(lunes);
          domingo.setDate(lunes.getDate() + 6);
          inicio = formatDateToDDMMYYYY(lunes);
          fin = formatDateToDDMMYYYY(domingo);
        } else if (tipo === "mes") {
          const primerDia = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
          const ultimoDia = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0);
          inicio = formatDateToDDMMYYYY(primerDia);
          fin = formatDateToDDMMYYYY(ultimoDia);
        }

        fechaInicio.value = inicio;
        fechaFin.value = fin;

        rangoBtns.forEach(btn => {
          btn.classList.toggle("activo", btn.dataset.rango === tipo);
        });
      }

      btnBuscar.addEventListener("click", applyFilters);

      pgPrev.addEventListener("click", () => {
        if (page > 1) {
          page--;
          render();
        }
      });

      pgNext.addEventListener("click", () => {
        if (!pgNext.disabled) {
          page++;
          render();
        }
      });

      btnAgregarRango.addEventListener("click", agregarRango);

      rangoBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          setRango(btn.dataset.rango);
        });
      });

      modalCancel.addEventListener("click", closeModal);
      modalSave.addEventListener("click", guardarEdicion);

      editModal.addEventListener("click", (e) => {
        if (e.target === editModal) closeModal();
      });

      document.getElementById("btnPlantillas").addEventListener("click", () => {
        alert("Descargar Plantilla (pendiente integrar)");
      });

      document.getElementById("btnSubir").addEventListener("click", () => {
        alert("Subir Horarios Masivos (pendiente integrar)");
      });

      loadMallas();
    })();
  </script>
</body>
</html>
"""

# =========================
# STREAMLIT SHELL
# =========================
st.markdown(
    """
    <style>
      .block-container{
        padding:0 !important;
        margin:0 !important;
        max-width:100% !important;
      }
      section.main > div{
        padding:0 !important;
        margin:0 !important;
      }
      header, footer{
        display:none !important;
      }
      iframe{
        display:block !important;
        border:0 !important;
        width:100% !important;
        min-height:100vh !important;
      }
      [data-testid="stSidebar"],
      [data-testid="collapsedControl"]{
        display:none !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(html, height=2200, scrolling=True)
