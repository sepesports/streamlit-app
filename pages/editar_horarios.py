# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Asignacion Horarios Socorristas", layout="wide")

# =========================
# HTML UI (RESPONSIVE) con diseño aplicado
# =========================
html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {
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
      --btn-red1:#d43d3d;
      --btn-red2:#a92a2a;
      --btn-green1:#2f7d32;
      --btn-green2:#256528;

      --shadow1: 0 22px 55px rgba(0,0,0,.55);
      --shadow2: 0 10px 22px rgba(0,0,0,.40);
      --blur: 14px;

      --outerPad:10px;
      --radiusDesk:34px;
      --radiusMob:26px;

      --lineSoft: rgba(255,255,255,.12);
      --lineSoft2: rgba(255,255,255,.08);
      --panelBg: rgba(255,255,255,.04);
      --panelBg2: rgba(255,255,255,.03);
      --inputBg: rgba(0,0,0,.24);
      --modalOverlay: rgba(0,0,0,.58);

      --font: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif;
    }

    html, body {
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      background:var(--baseBlue);
      overflow:hidden;
      font-family:var(--font);
      color:var(--ink);
    }

    * { box-sizing:border-box; }

    #stage{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      background:
        radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
        linear-gradient(180deg, #020614 0%, var(--baseBlue) 100%);
    }

    #plan{
      position:absolute;
      left:10px;
      right:10px;
      top:10px;
      bottom:10px;
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
        radial-gradient(50% 60% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
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
      left:var(--outerPad);
      right:var(--outerPad);
      top:var(--outerPad);
      bottom:var(--outerPad);
      border:1px solid rgba(255,255,255,.10);
      background:transparent;
      border-radius:34px;
      backdrop-filter:blur(var(--blur));
      -webkit-backdrop-filter:blur(var(--blur));
      z-index:10;
    }

    #wrap{
      position:absolute;
      left:var(--outerPad);
      right:var(--outerPad);
      top:var(--outerPad);
      bottom:var(--outerPad);
      padding:12px;
      z-index:20;
      overflow:auto;
    }

    .app{
      width:100%;
      max-width:1320px;
      min-height:100%;
      margin:0 auto;
    }

    .blk{
      border:1px solid rgba(255,255,255,.10);
      background:rgba(255,255,255,.04);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      -webkit-backdrop-filter:blur(calc(var(--blur) - 6px));
      border-radius:24px;
      box-shadow:var(--shadow2), inset 0 1px 0 rgba(255,255,255,.08);
      color:var(--ink);
    }

    .title{
      min-height:56px;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:12px 18px;
      text-align:center;
      font-weight:800;
      font-size:20px;
      letter-spacing:.2px;
      position:relative;
      background:rgba(255,255,255,.04);
      border:1px solid rgba(255,255,255,.10);
      border-radius:24px;
      backdrop-filter:blur(calc(var(--blur) - 6px));
      color:var(--ink);
      text-shadow:0 8px 18px rgba(0,0,0,.35);
      margin-bottom:14px;
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

    .top-actions{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:12px;
      margin-bottom:14px;
    }

    .btn{
      min-height:52px;
      border:1px solid rgba(255,255,255,.10);
      color:var(--ink);
      font-weight:800;
      font-size:16px;
      border-radius:999px;
      cursor:pointer;
      display:flex;
      align-items:center;
      justify-content:center;
      gap:10px;
      width:100%;
      box-shadow:0 22px 26px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.22);
      transition:transform .12s ease, filter .12s ease;
      text-transform:uppercase;
      letter-spacing:.6px;
      padding:12px 20px;
    }

    .btn:hover{ filter:brightness(1.05); }
    .btn:active{ transform:scale(.985); }

    .btn.green{
      background:linear-gradient(180deg, var(--btn-green1) 0%, var(--btn-green2) 100%);
    }

    .btn.red{
      background:linear-gradient(180deg, var(--btn-red1) 0%, var(--btn-red2) 100%);
    }

    .btn .ico{
      width:18px;
      height:18px;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      filter:drop-shadow(0 2px 2px rgba(0,0,0,.15));
    }

    .panel{
      border:1px solid rgba(255,255,255,.10);
      border-radius:28px;
      padding:16px;
      position:relative;
      overflow:hidden;
      background:rgba(255,255,255,.03);
      backdrop-filter:blur(calc(var(--blur) - 6px));
      -webkit-backdrop-filter:blur(calc(var(--blur) - 6px));
      box-shadow:var(--shadow2), inset 0 1px 0 rgba(255,255,255,.08);
      margin-bottom:14px;
    }

    .agregar-title,
    .subtitle,
    .table-title{
      font-weight:800;
      color:var(--ink);
      text-shadow:0 6px 14px rgba(0,0,0,.30);
    }

    .agregar-title{
      font-size:18px;
      margin-bottom:12px;
    }

    .agregar-row{
      display:flex;
      gap:12px;
      align-items:flex-end;
      flex-wrap:wrap;
    }

    .agregar-field{
      flex:1 1 180px;
      min-width:160px;
    }

    .agregar-field label,
    .field label,
    .modal-field label{
      display:block;
      font-size:12px;
      font-weight:800;
      color:var(--ink);
      margin:0 0 6px;
      letter-spacing:.3px;
    }

    .agregar-field input,
    select,
    .searchbtn,
    .modal-field input{
      width:100%;
      min-height:42px;
      border:1px solid rgba(255,255,255,.15);
      background:rgba(0,0,0,.24);
      box-sizing:border-box;
      padding:0 12px;
      font-size:14px;
      outline:none;
      color:var(--ink);
      border-radius:10px;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.04);
    }

    .agregar-field input::placeholder,
    .modal-field input::placeholder{
      color:rgba(255,255,255,.42);
    }

    .agregar-field input:focus,
    select:focus,
    .modal-field input:focus{
      border-color:rgba(255,255,255,.4);
      box-shadow:0 0 10px rgba(255,255,255,.08);
    }

    select{
      appearance:none;
      -webkit-appearance:none;
      -moz-appearance:none;
      font-weight:700;
      background-image:
        linear-gradient(45deg, transparent 50%, rgba(255,255,255,.7) 50%),
        linear-gradient(135deg, rgba(255,255,255,.7) 50%, transparent 50%);
      background-position:
        calc(100% - 18px) calc(50% - 3px),
        calc(100% - 12px) calc(50% - 3px);
      background-size:6px 6px, 6px 6px;
      background-repeat:no-repeat;
      padding-right:34px;
    }

    .agregar-btn,
    .searchbtn,
    .modal-actions button{
      border:1px solid rgba(255,255,255,.10);
      color:var(--ink);
      font-weight:800;
      border-radius:999px;
      cursor:pointer;
      transition:transform .12s ease, filter .12s ease, opacity .12s ease;
      box-shadow:0 16px 20px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.18);
    }

    .agregar-btn:hover,
    .searchbtn:hover,
    .modal-actions button:hover{
      filter:brightness(1.05);
    }

    .agregar-btn:active,
    .searchbtn:active,
    .modal-actions button:active{
      transform:scale(.985);
    }

    .agregar-btn{
      min-width:150px;
      min-height:42px;
      padding:10px 22px;
      background:linear-gradient(180deg, var(--btn-green1) 0%, var(--btn-green2) 100%);
    }

    .rango-opciones{
      display:flex;
      gap:10px;
      margin-top:12px;
      flex-wrap:wrap;
    }

    .rango-btn{
      min-height:38px;
      padding:8px 14px;
      font-weight:700;
      cursor:pointer;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.10);
      background:rgba(255,255,255,.06);
      color:var(--ink);
      box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
      transition:transform .12s ease, filter .12s ease, background .12s ease;
    }

    .rango-btn:hover{ filter:brightness(1.05); }
    .rango-btn:active{ transform:scale(.985); }

    .rango-btn.activo{
      background:linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      color:#fff;
    }

    .rangohint{
      display:block;
      margin-top:10px;
      color:var(--muted);
      font-size:12px;
    }

    .section-head{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      margin-bottom:12px;
    }

    .subtitle{
      font-size:20px;
      min-width:0;
    }

    .filters{
      display:grid;
      grid-template-columns:260px 1fr 1fr 170px;
      gap:12px;
      align-items:end;
      margin-bottom:14px;
    }

    .searchbtn{
      min-height:42px;
      background:linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      text-transform:uppercase;
      letter-spacing:.5px;
    }

    .tablewrap{
      border:1px solid rgba(255,255,255,.10);
      padding:12px;
      margin-top:10px;
      width:100%;
      overflow-x:auto;
      background:rgba(255,255,255,.03);
      border-radius:22px;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.06);
    }

    .table-title{
      font-size:15px;
      margin-bottom:10px;
    }

    table{
      width:100%;
      border-collapse:collapse;
      font-size:13px;
      min-width:760px;
    }

    thead th{
      text-align:left;
      padding:10px 8px;
      border-bottom:1px solid rgba(255,255,255,.12);
      font-weight:900;
      white-space:nowrap;
      color:var(--ink);
      background:rgba(255,255,255,.04);
    }

    tbody tr{
      transition:background .12s ease;
    }

    tbody tr:hover{
      background:rgba(255,255,255,.03);
    }

    tbody td{
      padding:11px 8px;
      border-bottom:1px solid rgba(255,255,255,.08);
      vertical-align:middle;
      font-weight:600;
      white-space:nowrap;
      color:rgba(255,255,255,.88);
    }

    .actions{
      display:flex;
      gap:10px;
      align-items:center;
      justify-content:flex-start;
    }

    .iconbtn{
      width:32px;
      height:32px;
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.05);
      border-radius:10px;
      cursor:pointer;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      flex:0 0 auto;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.06);
      transition:transform .12s ease, filter .12s ease, background .12s ease;
    }

    .iconbtn:hover{
      filter:brightness(1.08);
      background:rgba(255,255,255,.08);
    }

    .iconbtn:active{
      transform:scale(.97);
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
      gap:12px;
      margin-top:12px;
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
      gap:8px;
      flex:0 0 auto;
      max-width:45%;
    }

    .pgbtn{
      height:32px;
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.05);
      color:var(--ink);
      border-radius:10px;
      cursor:pointer;
      font-weight:900;
      padding:0 12px;
      white-space:nowrap;
      min-width:38px;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.06);
      transition:transform .12s ease, filter .12s ease, opacity .12s ease;
    }

    .pgbtn:hover{ filter:brightness(1.08); }
    .pgbtn:active{ transform:scale(.985); }
    .pgbtn:disabled{
      opacity:.45;
      cursor:not-allowed;
    }

    .pgbtn.prev{
      padding:0;
      width:32px;
      display:inline-flex;
      align-items:center;
      justify-content:center;
    }

    .pgcur{
      width:32px;
      height:32px;
      border-radius:10px;
      background:linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      color:#fff;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      font-size:12px;
      flex:0 0 auto;
      box-shadow:0 12px 18px rgba(0,0,0,.22);
    }

    .modal-overlay{
      display:none;
      position:fixed;
      inset:0;
      background:var(--modalOverlay);
      align-items:center;
      justify-content:center;
      z-index:1000;
      padding:18px;
      backdrop-filter:blur(4px);
      -webkit-backdrop-filter:blur(4px);
    }

    .modal{
      width:min(440px, 100%);
      border:1px solid rgba(255,255,255,.12);
      border-radius:26px;
      padding:22px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.04) 100%);
      box-shadow:var(--shadow1), inset 0 1px 0 rgba(255,255,255,.10);
      color:var(--ink);
    }

    .modal h3{
      margin:0 0 18px 0;
      font-weight:800;
      font-size:22px;
      text-align:center;
      text-shadow:0 8px 18px rgba(0,0,0,.35);
    }

    .modal-field{
      margin-bottom:14px;
    }

    .modal-actions{
      display:flex;
      justify-content:flex-end;
      gap:12px;
      margin-top:20px;
      flex-wrap:wrap;
    }

    .modal-actions .cancel{
      background:rgba(255,255,255,.10);
    }

    .modal-actions .save{
      background:linear-gradient(180deg, var(--btn-green1) 0%, var(--btn-green2) 100%);
    }

    /* ===== AJUSTES MÓVIL ===== */
    @media (max-width: 900px){
      #wrap{ padding:8px; }
      .filters{ grid-template-columns:1fr 1fr; }
    }

    @media (max-width: 768px){
      #plan, #frame, #outer{
        border-radius:24px;
      }

      #wrap{
        padding:8px;
      }

      .app{
        max-width:none;
      }

      .title{
        min-height:48px;
        font-size:18px;
        margin-bottom:10px;
      }

      .top-actions{
        grid-template-columns:1fr;
        gap:10px;
      }

      .btn{
        min-height:46px;
        font-size:14px;
        padding:10px 16px;
      }

      .panel{
        padding:10px;
        border-radius:20px;
        margin-bottom:10px;
      }

      .agregar-title{
        font-size:16px;
        margin-bottom:8px;
      }

      .agregar-row{
        display:block;
      }

      .agregar-field{
        margin-bottom:8px;
        min-width:0;
      }

      .agregar-field input,
      select,
      .searchbtn,
      .modal-field input{
        min-height:40px;
        font-size:14px;
      }

      .agregar-btn{
        width:100%;
        margin-top:4px;
      }

      .rango-opciones{
        gap:6px;
        margin-top:8px;
      }

      .rango-btn{
        min-height:34px;
        padding:6px 10px;
        font-size:12px;
      }

      .filters{
        grid-template-columns:1fr;
        gap:10px;
      }

      .subtitle{
        font-size:18px;
      }

      .col-instalacion, .col-socorrista, .col-horas{
        display:none;
      }

      .col-dia, .col-inicio, .col-finaliza, .col-estado{
        display:table-cell;
      }

      table{
        table-layout:fixed;
        min-width:0;
      }

      .col-dia{ width:30%; }
      .col-inicio{ width:23%; }
      .col-finaliza{ width:23%; }
      .col-estado{ width:24%; }

      td.col-estado .actions{
        justify-content:flex-start;
        gap:4px;
      }

      .iconbtn{
        width:24px;
        height:24px;
      }

      .iconbtn .icon{
        width:12px;
        height:12px;
      }

      .table-title{
        display:none;
      }

      .pagerbar{
        gap:8px;
      }

      .showing{
        max-width:60%;
      }

      .pager{
        max-width:40%;
      }

      .modal{
        padding:18px;
        border-radius:20px;
      }

      .modal h3{
        font-size:18px;
      }

      .modal-actions{
        justify-content:stretch;
      }

      .modal-actions button{
        flex:1 1 100%;
        min-height:42px;
      }
    }

    /* ========== FULLSCREEN TOGGLE STYLES (solo móvil) ========== */
    .fullscreen-toggle {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 48px;
      height: 48px;
      background: rgba(0,0,0,0.6);
      backdrop-filter: blur(12px);
      border-radius: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      color: white;
      cursor: pointer;
      z-index: 10000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: all 0.2s ease;
      border: 1px solid rgba(255,255,255,0.2);
      font-weight: bold;
      user-select: none;
      touch-action: manipulation;
    }
    .fullscreen-toggle:active {
      transform: scale(0.92);
      background: rgba(0,0,0,0.8);
    }
    @media (min-width: 769px) {
      .fullscreen-toggle {
        display: none;
      }
    }
    @media (max-width: 768px) {
      .fullscreen-toggle {
        display: flex;
      }
    }
    html:fullscreen #stage.fullscreen-mode #plan,
    html:-webkit-full-screen #stage.fullscreen-mode #plan,
    html:-moz-full-screen #stage.fullscreen-mode #plan {
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      border-radius: 0;
      box-shadow: none;
    }
    html:fullscreen #stage.fullscreen-mode #frame,
    html:-webkit-full-screen #stage.fullscreen-mode #frame,
    html:-moz-full-screen #stage.fullscreen-mode #frame {
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      border-radius: 0;
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>
    <div id="plan">
      <div id="outer"></div>

      <div id="wrap">
        <div class="app">

          <div class="title blk">Asignacion Horarios Socorristas</div>

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

          <div class="panel">
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
              <button class="agregar-btn" id="btnAgregarRango">Agregar rango</button>
            </div>

            <div class="rango-opciones">
              <button class="rango-btn" data-rango="dia">Día</button>
              <button class="rango-btn" data-rango="semana">Semana</button>
              <button class="rango-btn" data-rango="mes">Mes</button>
            </div>

            <small class="rangohint">Seleccione un rango o ingrese las fechas manualmente.</small>
          </div>

          <div class="panel">
            <div class="section-head">
              <div class="subtitle">Horarios de Socorristas</div>
            </div>

            <div class="filters">
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

            <div class="tablewrap">
              <div class="table-title">Tabla Horarios</div>

              <table id="data-table">
                <thead>
                  <tr>
                    <th class="col-instalacion">Instalacion</th>
                    <th class="col-socorrista">Socorrista</th>
                    <th class="col-dia">Día</th>
                    <th class="col-inicio">Inicio</th>
                    <th class="col-finaliza">Finaliza</th>
                    <th class="col-horas">Horas</th>
                    <th class="col-estado">Estado</th>
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
        <button class="cancel" id="modalCancel">Cancelar</button>
        <button class="save" id="modalSave">Guardar</button>
      </div>
    </div>
  </div>

  <!-- Botón de pantalla completa (solo móvil) -->
  <div id="fullscreenToggleBtn" class="fullscreen-toggle">⤢</div>

  <script>
    const API_BASE = "https://camilo27.pythonanywhere.com";
    const ENDPOINT_MALLAS = API_BASE + "/api/mallas";
    const ENDPOINT_AGREGAR = API_BASE + "/api/horarios/agregar";
    const ENDPOINT_EDITAR = API_BASE + "/api/horarios/editar";
    const ENDPOINT_ELIMINAR = API_BASE + "/api/horarios/eliminar";

    (function() {
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

    function getField(row, key) {
      if (!row) return "";
      if (row[key] !== undefined && row[key] !== null) return row[key];
      const lowerKey = key.toLowerCase();
      for (let k in row) {
        if (k.toLowerCase() === lowerKey) return row[k];
      }
      return "";
    }

    function formatTime(timeStr) {
      if (!timeStr) return "";
      const str = String(timeStr);
      const parts = str.split(':');
      if (parts.length >= 2) {
        return parts[0] + ':' + parts[1];
      }
      return str;
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
      return `<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M12 20h9" stroke="rgba(255,255,255,.9)" stroke-width="2" stroke-linecap="round"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4 11.5-11.5Z" stroke="rgba(255,255,255,.9)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    }

    function svgTrash() {
      return `<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M3 6h18" stroke="rgba(255,255,255,.9)" stroke-width="2" stroke-linecap="round"/><path d="M8 6V4h8v2" stroke="rgba(255,255,255,.9)" stroke-width="2" stroke-linecap="round"/><path d="M19 6l-1 14H6L5 6" stroke="rgba(255,255,255,.9)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11v6" stroke="rgba(255,255,255,.9)" stroke-width="2" stroke-linecap="round"/><path d="M14 11v6" stroke="rgba(255,255,255,.9)" stroke-width="2" stroke-linecap="round"/></svg>`;
    }

    function parseFechaDDMMYYYY(fechaStr) {
      if (!/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(fechaStr)) return null;
      const [dd, mm, yyyy] = fechaStr.split('/').map(Number);
      return new Date(yyyy, mm - 1, dd);
    }

    function formatDateToDDMMYYYY(date) {
      const d = date.getDate().toString().padStart(2,'0');
      const m = (date.getMonth() + 1).toString().padStart(2,'0');
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

    function resetRangoActivo() {
      rangoBtns.forEach(btn => btn.classList.remove("activo"));
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
          const inst = getField(r, "Instalacion") || getField(r, "instalacion");
          if (inst) instalacionesSet.add(inst);

          const soc = getField(r, "Socorrista") || getField(r, "socorrista");
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
        const rInst = getField(r, "Instalacion") || getField(r, "instalacion");
        const rSoc = getField(r, "Socorrista") || getField(r, "socorrista");
        const okInst = (inst === "Todas") || (rInst === inst);
        const okSoc = (soc === "Todos") || (rSoc === soc);
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

        const instalacion = r.Instalacion || r.instalacion || "";
        const socorrista = r.Socorrista || r.socorrista || "";
        const dia = r.Dia || r.dia || "";
        const inicioRaw = r.Ingreso || r.ingreso || r.Inicio || r.inicio || "";
        const salidaRaw = r.Salida || r.salida || r.Finaliza || r.finaliza || "";
        const horas = r.Intensidad_horaria || r.intensidad_horaria || r.Horas || r.horas || "";

        const inicio = formatTime(inicioRaw);
        const salida = formatTime(salidaRaw);

        const tdInst = document.createElement("td");
        tdInst.className = "col-instalacion";
        tdInst.textContent = instalacion;

        const tdSoc = document.createElement("td");
        tdSoc.className = "col-socorrista";
        tdSoc.textContent = socorrista;

        const tdDia = document.createElement("td");
        tdDia.className = "col-dia";
        tdDia.textContent = dia;

        const tdInicio = document.createElement("td");
        tdInicio.className = "col-inicio";
        tdInicio.textContent = inicio;

        const tdFinaliza = document.createElement("td");
        tdFinaliza.className = "col-finaliza";
        tdFinaliza.textContent = salida;

        const tdHoras = document.createElement("td");
        tdHoras.className = "col-horas";
        tdHoras.textContent = horas;

        const tdEstado = document.createElement("td");
        tdEstado.className = "col-estado";

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
      editSocorrista.value = row.Socorrista || row.socorrista || "";
      editInstalacion.value = row.Instalacion || row.instalacion || "";
      editIngreso.value = row.Ingreso || row.ingreso || row.Inicio || row.inicio || "";
      editSalida.value = row.Salida || row.salida || row.Finaliza || row.finaliza || "";
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

      let exitos = 0;
      let errores = 0;

      for (let i = 0; i < fechas.length; i++) {
        const fecha = fechas[i];
        try {
          const res = await fetch(ENDPOINT_AGREGAR, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fecha: fecha, bloque: bloque })
          });

          const data = await res.json();
          if (data.ok) exitos++;
          else errores++;
        } catch (e) {
          errores++;
        }

        await new Promise(r => setTimeout(r, 200));
      }

      alert(`Proceso completado: ${exitos} exitosos, ${errores} errores.`);

      if (exitos > 0) {
        fechaInicio.value = "";
        fechaFin.value = "";
        bloqueInput.value = "";
        resetRangoActivo();
        loadMallas();
      }
    }

    function setRango(tipo) {
      const hoy = new Date();
      let inicio, fin;

      if (tipo === 'dia') {
        inicio = fin = formatDateToDDMMYYYY(hoy);
      } else if (tipo === 'semana') {
        const diaSem = hoy.getDay();
        const diffLunes = (diaSem === 0 ? 6 : diaSem - 1);
        const lunes = new Date(hoy);
        lunes.setDate(hoy.getDate() - diffLunes);
        const domingo = new Date(lunes);
        domingo.setDate(lunes.getDate() + 6);
        inicio = formatDateToDDMMYYYY(lunes);
        fin = formatDateToDDMMYYYY(domingo);
      } else if (tipo === 'mes') {
        const primerDia = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
        const ultimoDia = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0);
        inicio = formatDateToDDMMYYYY(primerDia);
        fin = formatDateToDDMMYYYY(ultimoDia);
      }

      fechaInicio.value = inicio;
      fechaFin.value = fin;

      resetRangoActivo();
      const activeBtn = document.querySelector(`.rango-btn[data-rango="${tipo}"]`);
      if (activeBtn) activeBtn.classList.add("activo");
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
      btn.addEventListener("click", () => setRango(btn.dataset.rango));
    });

    modalCancel.addEventListener("click", closeModal);
    modalSave.addEventListener("click", guardarEdicion);
    editModal.addEventListener("click", (e) => {
      if (e.target === editModal) closeModal();
    });

    document.getElementById("btnPlantillas").addEventListener("click", () => alert("Descargar Plantilla (pendiente integrar)"));
    document.getElementById("btnSubir").addEventListener("click", () => alert("Subir Horarios Masivos (pendiente integrar)"));

    loadMallas();

    // ==================== FULLSCREEN PERSISTENCE (solo móvil) ====================
    (function() {
      const stageEl = document.getElementById("stage");
      const toggleBtn = document.getElementById("fullscreenToggleBtn");
      const isMobile = window.innerWidth <= 768;

      function setFullscreenFlag(active) {
        if (active) {
          localStorage.setItem("fullscreenActive", "true");
        } else {
          localStorage.removeItem("fullscreenActive");
        }
      }

      function enterFullscreen() {
        const elem = document.documentElement;
        const requestMethod = elem.requestFullscreen || elem.webkitRequestFullscreen || elem.mozRequestFullScreen || elem.msRequestFullscreen;
        if (requestMethod) {
          requestMethod.call(elem).then(() => {
            if (stageEl) stageEl.classList.add("fullscreen-mode");
            if (toggleBtn) {
              toggleBtn.textContent = "✕";
              toggleBtn.style.fontSize = "26px";
            }
            setFullscreenFlag(true);
          }).catch(err => {
            console.log("Error al entrar en fullscreen:", err);
          });
        }
      }

      function exitFullscreen() {
        const exitMethod = document.exitFullscreen || document.webkitExitFullscreen || document.mozCancelFullScreen || document.msExitFullscreen;
        if (exitMethod) {
          exitMethod.call(document).then(() => {
            if (stageEl) stageEl.classList.remove("fullscreen-mode");
            if (toggleBtn) {
              toggleBtn.textContent = "⤢";
              toggleBtn.style.fontSize = "28px";
            }
            setFullscreenFlag(false);
          }).catch(err => {
            console.log("Error al salir de fullscreen:", err);
          });
        }
      }

      function toggleFullscreen() {
        const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
        if (isFull) {
          exitFullscreen();
        } else {
          enterFullscreen();
        }
      }

      function onFullscreenChange() {
        const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
        if (isFull) {
          if (stageEl) stageEl.classList.add("fullscreen-mode");
          if (toggleBtn) {
            toggleBtn.textContent = "✕";
            toggleBtn.style.fontSize = "26px";
          }
          setFullscreenFlag(true);
        } else {
          if (stageEl) stageEl.classList.remove("fullscreen-mode");
          if (toggleBtn) {
            toggleBtn.textContent = "⤢";
            toggleBtn.style.fontSize = "28px";
          }
          setFullscreenFlag(false);
        }
      }

      // Restaurar fullscreen si estaba activo (solo móvil)
      if (isMobile) {
        const savedFlag = localStorage.getItem("fullscreenActive");
        if (savedFlag === "true") {
          const isCurrentlyFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
          if (!isCurrentlyFull) {
            enterFullscreen();
          } else {
            // Asegurar UI
            if (stageEl) stageEl.classList.add("fullscreen-mode");
            if (toggleBtn) {
              toggleBtn.textContent = "✕";
              toggleBtn.style.fontSize = "26px";
            }
          }
        }
      }

      if (toggleBtn) {
        toggleBtn.addEventListener("click", function(e) {
          e.preventDefault();
          toggleFullscreen();
        });
      }

      document.addEventListener("fullscreenchange", onFullscreenChange);
      document.addEventListener("webkitfullscreenchange", onFullscreenChange);
      document.addEventListener("mozfullscreenchange", onFullscreenChange);
      document.addEventListener("MSFullscreenChange", onFullscreenChange);
    })();
    // ==================== FIN FULLSCREEN PERSISTENCE ====================
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
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
      iframe{
        display:block !important;
        border:0 !important;
      }
      [data-testid="stSidebar"], [data-testid="collapsedControl"]{display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(html, height=1200, scrolling=True)
