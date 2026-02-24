# calendario.py
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# PLANTILLA "CALENDARIO" — (MISMA ESTRUCTURA / MISMAS MEDIDAS) + TEMA HUD NARANJA
# FIX: NO forzar el iframe a position:fixed en móvil (rompía el alto y “montaba” bloques)
# + DATA REAL: /api/mallas (PythonAnywhere) -> Calendario + Agenda del día + Filtro Socorrista
# ==============================================================================

PAD_X_PX = 10
PAD_TOP_PX = 10

BORDER_PX = 2
BORDER_COLOR = "rgba(255,255,255,.12)"
BG_COLOR = "#081a3a"
PANEL_BG = "rgba(255,255,255,.06)"
CARD_BG = "rgba(255,255,255,.07)"
TEXT_COLOR = "#eaf2ff"
MUTED_TEXT = "rgba(234,242,255,.75)"

FONT_BASE_PX = 14
TITLE_PX = 18
H2_PX = 16
SMALL_PX = 12

TOPBAR_H = 8
MONTHBAR_H = 10
CAL_GRID_H = 24
FILTERS_H = 9
AGENDA_H = 34
BOTTOMBAR_H = 10

INNER_L = 4
INNER_R = 4
INNER_TOP_GAP = 0.7

CAL_COLS = 7
CAL_ROWS = 6
DAY_CELL_GAP_PX = 6

AGENDA_ROWS = 5

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0!important;margin:0!important;max-width:100%!important;}
      section.main > div{padding:0!important;margin:0!important;}
      header, footer{display:none!important;}
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
  :root {
    /* Fondo */
    --bg-0:#070b12;       /* base */
    --bg-1:#0b1320;       /* capas */
    --bg-2:#0f1c2a;       /* panel */

    /* Glass */
    --glass: rgba(255,255,255,.06);
    --glass-2: rgba(255,255,255,.08);
    --stroke: rgba(255,255,255,.10);
    --stroke-2: rgba(255,255,255,.14);

    /* Glow */
    --glow-blue: rgba(96, 196, 255, .45);
    --glow-blue-2: rgba(96, 196, 255, .22);
    --glow-orange: rgba(255, 142, 64, .50);
    --glow-orange-2: rgba(255, 142, 64, .22);

    /* Texto */
    --txt-0: rgba(255,255,255,.95);
    --txt-1: rgba(255,255,255,.78);
    --txt-2: rgba(255,255,255,.55);
    --txt-3: rgba(255,255,255,.35);

    /* Estados */
    --free:#4fe38c;
    --busy:#ff4b4b;
    --other:#ff7c2c;

    /* Layout */
    --radius-outer: 26px;
    --radius-card: 18px;
    --radius-pill: 999px;
    --radius-cell: 12px;

    /* Sombras */
    --shadow-soft: 0 18px 40px rgba(0,0,0,.45);
    --shadow-inner: inset 0 1px 0 rgba(255,255,255,.08);

    /* Blur */
    --blur: 18px;

    /* Tamaños sugeridos (móvil) */
    --fs-top: 14px;      /* header */
    --fs-title: 28px;    /* FEBRERO 2026 */
    --fs-sub: 12px;      /* labels */
    --fs-day: 11px;      /* MO..FRI */
    --fs-cell: 14px;     /* números calendario */
    --fs-h3: 18px;       /* "Agenda del día" */
    --fs-table: 13px;    /* tabla */
    --fs-btn: 14px;      /* botones */

    /* Espaciados */
    --pad-outer: 16px;
    --pad-block: 14px;
  }

  /* ---------- 1) RESET BÁSICO ---------- */
  *{box-sizing:border-box;}
  html,body{height:100%;margin:0;padding:0;}
  body{
    font-family: "Inter", system-ui, -apple-system, "SF Pro Display", Segoe UI, Roboto, Arial, sans-serif;
    color:var(--txt-0);
    background: none; /* background handled by #stage */
  }
  #stage{
    position:fixed;
    inset:0;
    background:
      radial-gradient(1100px 700px at 10% 10%, rgba(255,124,44,.22), transparent 55%),
      radial-gradient(900px 650px at 90% 18%, rgba(96,196,255,.22), transparent 55%),
      radial-gradient(900px 750px at 50% 95%, rgba(96,196,255,.12), transparent 60%),
      linear-gradient(180deg, var(--bg-2), var(--bg-0));
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #frame{display:none;}

  #wrap{
    position: relative;
    width: min(420px, 92vw);
    margin: 0 auto;
    padding: var(--pad-outer);
    border-radius: var(--radius-outer);
    background: rgba(10, 16, 26, .58);
    border:1px solid var(--stroke);
    box-shadow:var(--shadow-soft);
    backdrop-filter:blur(var(--blur));
    -webkit-backdrop-filter:blur(var(--blur));
    overflow:hidden;
    display:flex;
    flex-direction:column;
    max-height: 95vh;
  }
  #wrap::before{
    content:"";
    position:absolute; inset:0;
    border-radius:inherit;
    pointer-events:none;
    background:
      linear-gradient(180deg, rgba(255,255,255,.10), transparent 30%),
      radial-gradient(800px 500px at 85% 20%, rgba(96,196,255,.18), transparent 60%),
      radial-gradient(700px 500px at 20% 20%, rgba(255,124,44,.12), transparent 65%);
    mix-blend-mode: screen;
  }

  /* Para pantallas grandes: ancho mayor pero con límite */
  @media (min-width: 1400px) {
    #wrap {
      width: min(1200px, 80vw);
      max-width: 1400px;
    }
  }

  /* Topbar */
  .topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    padding:10px 12px;
    border-radius:18px;
    background:var(--glass);
    border:1px solid var(--stroke);
    box-shadow:var(--shadow-inner);
    backdrop-filter:blur(calc(var(--blur) - 6px));
  }
  .topbar__iconBtn{
    width:34px; height:34px;
    border-radius:12px;
    display:grid;
    place-items:center;
    background:rgba(255,255,255,.05);
    border:1px solid var(--stroke);
    box-shadow:0 0 18px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.08);
  }
  .topbar__title{
    font-size:var(--fs-top);
    font-weight:600;
    color:var(--txt-0);
    letter-spacing:.2px;
  }
  .topbar__user{
    font-size:var(--fs-top);
    font-weight:600;
    color:var(--txt-1);
  }
  .topbar__right{
    display:flex;
    align-items:center;
    gap:10px;
  }

  /* Month block */
  .monthBlock{
    margin-top:14px;
    padding:12px 8px 6px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
  }
  .monthBlock .nav{
    display:flex;
    align-items:center;
    gap:10px;
  }
  .monthNav__btn{
    width:38px; height:38px;
    border-radius:14px;
    background:rgba(255,255,255,.05);
    border:1px solid var(--stroke);
    box-shadow:0 0 18px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.08);
    display:grid;
    place-items:center;
  }
  .monthNav__title{
    font-size:var(--fs-title);
    font-weight:800;
    letter-spacing:1px;
    text-transform:uppercase;
    color:rgba(255,255,255,.92);
    text-shadow:0 0 18px var(--glow-blue-2);
    line-height:1.05;
    text-align:center;
    flex:1;
  }

  /* Calendar card */
  .calendarCard{
    margin-top:8px;
    padding:var(--pad-block);
    border-radius:var(--radius-card);
    background:var(--glass-2);
    border:1px solid var(--stroke);
    box-shadow:0 0 34px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.08);
    backdrop-filter:blur(calc(var(--blur) - 6px));
  }
  .calendarCard__labelRow{
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:10px;
  }
  .calendarCard__label{
    font-size:var(--fs-sub);
    font-weight:700;
    letter-spacing:.8px;
    color:var(--txt-1);
  }
  .weekdays{
    display:grid;
    grid-template-columns:repeat(7,1fr);
    gap:8px;
    margin:10px 0 10px;
  }
  .weekdays span{
    font-size:var(--fs-day);
    color:var(--txt-3);
    text-align:center;
    letter-spacing:.6px;
  }
  .calendarGrid{
    display:grid;
    grid-template-columns:repeat(7,1fr);
    gap:10px;
  }
  .day{
    height:38px;
    border-radius:var(--radius-cell);
    background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.09);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.06);
    display:grid;
    place-items:center;
    font-size:var(--fs-cell);
    font-weight:700;
    color:var(--txt-1);
    position:relative;
  }
  .day.dim{
    color:var(--txt-3);
    background:rgba(255,255,255,.03);
    border-color:rgba(255,255,255,.07);
  }
  .day.sel{
    border:2px solid var(--glow-orange);
    box-shadow:0 0 0 2px rgba(255,124,44,.10), 0 0 18px var(--glow-orange-2), inset 0 1px 0 rgba(255,255,255,.08);
    color:var(--txt-0);
  }
  .day.past{
    opacity:.22;
    cursor:default;
    pointer-events:none;
    filter:grayscale(35%);
  }
  .day.hasdata::after{
    content:"";
    position:absolute;
    width:7px; height:7px;
    border-radius:50%;
    right:7px; bottom:7px;
    background:var(--free);
    box-shadow:0 0 10px var(--free);
  }

  /* Legend */
  .legend{
    display:flex;
    align-items:center;
    gap:14px;
    margin-top:12px;
    padding-top:8px;
  }
  .legend__item{
    display:flex;
    align-items:center;
    gap:8px;
    color:var(--txt-2);
    font-size:11px;
    letter-spacing:.2px;
  }
  .legend__dot{
    width:8px; height:8px;
    border-radius:99px;
    background:rgba(255,255,255,.30);
    box-shadow:0 0 14px rgba(255,255,255,.10);
  }
  .legend__dot.on{
    background:var(--free);
    box-shadow:0 0 14px var(--free);
  }

  /* Controls row */
  .controlsRow{
    display:grid;
    grid-template-columns:1fr 1fr auto;
    gap:10px;
    margin-top:14px;
    align-items:center;
  }
  .selectPill{
    height:40px;
    border-radius:var(--radius-pill);
    padding:0 14px;
    background:var(--glass);
    border:1px solid var(--stroke);
    color:var(--txt-1);
    font-size:13px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
    backdrop-filter:blur(calc(var(--blur) - 6px));
  }
  .selectPill select{
    background:transparent;
    border:none;
    color:inherit;
    font:inherit;
    outline:none;
    width:100%;
    appearance:none;
    -webkit-appearance:none;
    cursor:pointer;
  }
  .selectPill select option {
    background: var(--bg-1);
    color: var(--txt-0);
  }
  .selectPill .caret{
    font-weight:900;
    pointer-events:none;
  }
  .applyBtn{
    height:40px;
    min-width:92px;
    border-radius:14px;
    padding:0 16px;
    background:rgba(255,124,44,.06);
    border:1px solid rgba(255,124,44,.75);
    color:rgba(255,124,44,.95);
    font-weight:800;
    font-size:var(--fs-btn);
    letter-spacing:.3px;
    box-shadow:0 0 18px var(--glow-orange-2), inset 0 1px 0 rgba(255,255,255,.10);
  }

  /* Agenda block */
  .agendaBlock{
    margin-top:16px;
    flex:1;
    display:flex;
    flex-direction:column;
    min-height:0;
  }
  .agendaTitle{
    font-size:var(--fs-h3);
    font-weight:800;
    color:var(--txt-0);
    margin:0 0 10px 0;
    text-shadow:0 0 18px var(--glow-blue-2);
  }
  .agendaMeta{
    display:flex;
    justify-content:space-between;
    gap:10px;
    color:var(--txt-2);
    font-size:12px;
    margin-bottom:10px;
  }
  .tableCard{
    border-radius:var(--radius-card);
    background:var(--glass-2);
    border:1px solid var(--stroke);
    box-shadow:0 0 34px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.08);
    overflow:hidden;
    flex:1;
    display:flex;
    flex-direction:column;
    min-height:0;
  }
  .tableHeader{
    display:grid;
    grid-template-columns:26px 1fr 92px 92px 86px;
    gap:10px;
    padding:12px 14px;
    font-size:12px;
    font-weight:700;
    color:var(--txt-2);
    background:rgba(255,255,255,.03);
    border-bottom:1px solid rgba(255,255,255,.08);
  }
  .trow{
    display:grid;
    grid-template-columns:26px 1fr 92px 92px 86px;
    gap:10px;
    padding:11px 14px;
    align-items:center;
    border-bottom:1px solid rgba(255,255,255,.06);
  }
  .trow:last-child{border-bottom:none;}
  .trow div:nth-child(1){
    font-size:var(--fs-table);
    color:var(--txt-0);
    font-weight:650;
    display:flex;
    align-items:center;
    gap:8px;
  }
  .trow div:nth-child(2),
  .trow div:nth-child(3),
  .trow div:nth-child(4){
    font-size:12.5px;
    color:var(--txt-1);
    font-variant-numeric:tabular-nums;
  }
  .trow div:nth-child(5){
    display:flex;
    justify-content:flex-end;
  }
  .chk{
    width:16px; height:16px;
    border-radius:4px;
    border:1px solid rgba(255,255,255,.22);
    background:rgba(255,255,255,.04);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.06);
    display:inline-block;
  }
  .status{
    height:22px;
    padding:0 10px;
    border-radius:var(--radius-pill);
    display:inline-flex;
    align-items:center;
    justify-content:center;
    font-size:11px;
    font-weight:800;
    letter-spacing:.3px;
    color:rgba(0,0,0,.78);
  }
  .status.free{
    background:linear-gradient(180deg, rgba(79,227,140,1), rgba(46,196,118,1));
    box-shadow:0 0 14px rgba(79,227,140,.22);
  }
  .status.busy{
    background:linear-gradient(180deg, rgba(255,90,90,1), rgba(230,55,55,1));
    box-shadow:0 0 14px rgba(255,75,75,.22);
    color:rgba(255,255,255,.92);
  }
  .status.other{
    background:rgba(255,255,255,.1);
    border:1px solid rgba(255,255,255,.2);
    color:var(--txt-1);
  }
  #tbody{
    flex:1;
    overflow-y:auto;
  }

  /* Footer block */
  .footerBlock{
    margin-top:14px;
    padding-top:12px;
    border-top:1px solid rgba(255,255,255,.08);
  }
  .summaryRow{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
    color:var(--txt-2);
    font-size:12.5px;
    font-variant-numeric:tabular-nums;
    padding:8px 2px;
  }
  .chip{
    border:1px solid var(--stroke);
    border-radius:var(--radius-pill);
    padding:6px 10px;
    font-size:12px;
    font-weight:800;
    background:var(--glass);
    color:var(--txt-1);
    display:inline-flex;
    align-items:center;
    gap:8px;
    white-space:nowrap;
    box-shadow:0 10px 18px rgba(0,0,0,.38);
  }
  .footerActions{
    margin-top:12px;
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:10px;
  }
  .btn{
    height:42px;
    border-radius:14px;
    border:1px solid var(--stroke);
    background:var(--glass);
    color:var(--txt-1);
    font-weight:750;
    font-size:var(--fs-btn);
    letter-spacing:.2px;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.07);
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
  }
  .btn--primary, .btn.primary{
    border-color:rgba(255,124,44,.75);
    background:rgba(255,124,44,.06);
    color:rgba(255,124,44,.95);
    box-shadow:0 0 18px var(--glow-orange-2), inset 0 1px 0 rgba(255,255,255,.10);
  }

  /* Responsive */
  @media (max-width:380px){
    :root{
      --fs-title:24px;
    }
    .calendarGrid{gap:8px;}
    .day{height:34px;}
    .tableHeader, .trow{
      grid-template-columns:24px 1fr 84px 84px 78px;
    }
  }
  @media (max-width:520px){
    .controlsRow{
      grid-template-columns:1fr 1fr;
      grid-auto-rows:min-content;
    }
    .controlsRow .applyBtn{
      grid-column:1/-1;
    }
    .tableHeader{
      display:none;
    }
    .trow{
      grid-template-columns:1fr;
      gap:5px;
      padding:10px;
    }
    .trow div{
      display:flex;
      align-items:center;
    }
    .trow div:nth-child(1){
      font-weight:bold;
    }
    .footerActions{
      grid-template-columns:1fr 1fr;
    }
    .footerActions .btn:last-child{
      grid-column:span 2;
    }
  }

  /* Ajuste adicional para pantallas muy grandes */
  @media (min-width: 1400px) {
    .controlsRow {
      grid-template-columns: repeat(4, 1fr) auto;
    }
    .tableHeader {
      grid-template-columns: 26px 2fr 1fr 1fr 1fr 1fr;
    }
    .trow {
      grid-template-columns: 26px 2fr 1fr 1fr 1fr 1fr;
    }
  }
</style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="plan">
      <div id="wrap">

        <div id="topbar" class="panel topbar">
          <div class="iconbtn topbar__iconBtn">□</div>
          <div class="center topbar__title">Calendario</div>
          <div class="right topbar__right">
            <div id="userDisplay" class="topbar__user">Usuario</div>
            <div class="iconbtn topbar__iconBtn">⌁</div>
            <div class="iconbtn topbar__iconBtn">⋮</div>
          </div>
        </div>

        <div id="monthbar" class="panel monthBlock">
          <div class="nav"><div class="iconbtn monthNav__btn" id="prevMonth">‹</div></div>
          <div class="month monthNav__title" id="monthDisplay">—</div>
          <div class="nav"><div class="iconbtn monthNav__btn" id="nextMonth">›</div></div>
        </div>

        <div id="calgrid" class="panel calendarCard">
          <div class="head calendarCard__labelRow">
            <div class="label calendarCard__label">
              <span>CALENDARIO</span>
              <span id="syncBadge">SYNC…</span>
            </div>
          </div>

          <div class="weekheads weekdays" aria-hidden="true">
            <div class="w">L</div>
            <div class="w">M</div>
            <div class="w">X</div>
            <div class="w">J</div>
            <div class="w">V</div>
            <div class="w">S</div>
            <div class="w">D</div>
          </div>

          <div class="days calendarGrid" id="days"></div>

          <div id="legend" class="legend">
            <span class="legend__item"><i class="dot on legend__dot"></i>HAY DATOS</span>
            <span class="legend__item"><i class="dot legend__dot"></i>SIN DATOS</span>
          </div>
        </div>

        <div id="filters" class="panel controlsRow">
          <div class="select selectPill">
            <select id="monthSelect">
              <option value="0">Enero</option>
              <option value="1">Febrero</option>
              <option value="2">Marzo</option>
              <option value="3">Abril</option>
              <option value="4">Mayo</option>
              <option value="5">Junio</option>
              <option value="6">Julio</option>
              <option value="7">Agosto</option>
              <option value="8">Septiembre</option>
              <option value="9">Octubre</option>
              <option value="10">Noviembre</option>
              <option value="11">Diciembre</option>
            </select>
            <span class="caret">▾</span>
          </div>

          <div class="select selectPill">
            <select id="yearSelect"></select>
            <span class="caret">▾</span>
          </div>

          <div class="select selectPill">
            <select id="socorristaSelect">
              <option value="">Todos los socorristas</option>
            </select>
            <span class="caret">▾</span>
          </div>

          <div class="select selectPill">
            <select id="modeSelect">
              <option value="dia">Por día</option>
              <option value="todo">Ver todo (desde hoy)</option>
            </select>
            <span class="caret">▾</span>
          </div>

          <div class="btn primary applyBtn" id="applyFilters">Aplicar</div>
        </div>

        <div id="agenda" class="panel agendaBlock">
          <h3 class="agendaTitle">Agenda del día</h3>
          <div class="meta agendaMeta" id="agendaMeta">
            <div><b>Fecha:</b> <span id="fechaDisplay">—</span></div>
          </div>

          <div id="table" class="tableCard">
            <div id="thead" class="tableHeader">
              <div>Instalación</div><div>Inicio</div><div>Finaliza</div><div>Horas</div><div>Estado</div>
            </div>
            <div id="tbody"></div>
          </div>
        </div>

        <div id="bottom" class="panel footerBlock">
          <div class="leftinfo summaryRow">
            <span class="chip" id="bottomFecha">—</span>
            <span class="status other" id="bottomEstado">—</span>
          </div>
          <div class="actions footerActions">
            <div class="btn">Aplicar</div>
            <div class="btn">Modificar</div>
            <div class="btn primary btn--primary">Enviar</div>
          </div>
        </div>

      </div>
    </div>
  </div>

<script>
(function(){
  const API_BASE = "https://camilo27.pythonanywhere.com";
  const ENDPOINT_MALLAS = API_BASE + "/api/mallas";

  function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
  }
  const userName = getQueryParam('usuario') || 'Usuario';
  document.getElementById('userDisplay').textContent = userName;

  let currentDate = new Date();
  currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());

  let selectedDate = new Date(currentDate);
  let currentMonth = selectedDate.getMonth();
  let currentYear = selectedDate.getFullYear();

  // Data real
  let ALL_ROWS = [];
  let AVAILABLE_DATES = new Set(); // yyyy-mm-dd
  let SOCORRISTAS = []; // unique sorted

  let FILTER_SOCORRISTA = "";
  let FILTER_MODE = "dia"; // dia | todo

  function pad2(n){ return String(n).padStart(2,'0'); }

  function toKeyYMD(y,m,d){
    return `${y}-${pad2(m)}-${pad2(d)}`;
  }

  function formatDateKey(date) {
    return toKeyYMD(date.getFullYear(), date.getMonth()+1, date.getDate());
  }

  function formatDisplayDate(date) {
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function parseSheetDateToKey(fechaStr){
    // soporta: dd/mm/yyyy o yyyy-mm-dd
    const s = (fechaStr || "").trim();
    if(!s) return "";
    if(/^\d{2}\/\d{2}\/\d{4}$/.test(s)){
      const [dd,mm,yyyy] = s.split("/");
      return `${yyyy}-${mm}-${dd}`;
    }
    if(/^\d{4}-\d{2}-\d{2}$/.test(s)){
      return s;
    }
    return "";
  }

  function getField(row, keys){
    for(const k of keys){
      if(row && Object.prototype.hasOwnProperty.call(row, k)) return row[k];
    }
    return "";
  }

  function normalizeEstado(s){
    const v = String(s || "").trim().toLowerCase();
    if(!v) return {label:"OTRO", cls:"other"};
    if(v.includes("libre")) return {label:"LIBRE", cls:"free"};
    if(v.includes("ocup")) return {label:"OCUPADO", cls:"busy"};
    return {label:String(s).toUpperCase(), cls:"other"};
  }

  function setSyncBadge(ok, text){
    const el = document.getElementById("syncBadge");
    el.textContent = text;
    el.className = ok ? "ok" : "err";
  }

  function daysInMonth(year, month) {
    return new Date(year, month + 1, 0).getDate();
  }

  function getFirstDayOfMonth(year, month) {
    let day = new Date(year, month, 1).getDay();
    return day === 0 ? 7 : day;
  }

  function getMonthDays(year, month) {
    const firstDay = getFirstDayOfMonth(year, month);
    const totalDays = daysInMonth(year, month);

    const days = [];
    const prevMonthDays = firstDay - 1;

    if (prevMonthDays > 0) {
      const prevMonth = month === 0 ? 11 : month - 1;
      const prevYear = month === 0 ? year - 1 : year;
      const daysPrev = daysInMonth(prevYear, prevMonth);
      for (let i = prevMonthDays; i > 0; i--) {
        days.push({ date: new Date(prevYear, prevMonth, daysPrev - i + 1), currentMonth: false });
      }
    }

    for (let d = 1; d <= totalDays; d++) {
      days.push({ date: new Date(year, month, d), currentMonth: true });
    }

    const remaining = 7 - (days.length % 7);
    if (remaining < 7) {
      const nextMonth = month === 11 ? 0 : month + 1;
      const nextYear = month === 11 ? year + 1 : year;
      for (let i = 1; i <= remaining; i++) {
        days.push({ date: new Date(nextYear, nextMonth, i), currentMonth: false });
      }
    }

    while (days.length < 42) {
      const last = days[days.length - 1].date;
      const nd = new Date(last.getFullYear(), last.getMonth(), last.getDate() + 1);
      days.push({ date: nd, currentMonth: false });
    }
    if (days.length > 42) days.length = 42;

    return days;
  }

  function updateMonthYearDisplay(year, month) {
    document.getElementById('monthSelect').value = month;
    document.getElementById('yearSelect').value = year;
  }

  function renderCalendar(year, month) {
    const daysEl = document.getElementById('days');
    daysEl.innerHTML = '';

    const days = getMonthDays(year, month);

    days.forEach(dayInfo => {
      const date = dayInfo.date;
      const cell = document.createElement('div');
      cell.className = 'day';
      cell.textContent = date.getDate();

      if (!dayInfo.currentMonth) cell.classList.add('dim');

      const isPast = date < currentDate;
      if(isPast) cell.classList.add('past');

      const key = formatDateKey(date);
      if(AVAILABLE_DATES.has(key)) cell.classList.add('hasdata');

      if (date.getFullYear() === selectedDate.getFullYear() &&
          date.getMonth() === selectedDate.getMonth() &&
          date.getDate() === selectedDate.getDate()) {
        cell.classList.add('sel');
      }

      cell.addEventListener('click', function() {
        if(date < currentDate) return;

        selectedDate = new Date(date);
        if (date.getMonth() !== month || date.getFullYear() !== year) {
          currentMonth = date.getMonth();
          currentYear = date.getFullYear();
          renderCalendar(currentYear, currentMonth);
          updateMonthYearDisplay(currentYear, currentMonth);
        } else {
          renderCalendar(year, month);
        }
        updateAgenda();
        updateBottomBar();
      });

      daysEl.appendChild(cell);
    });

    document.getElementById('monthDisplay').textContent =
      new Date(year, month, 1).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' }).toUpperCase();
  }

  function getFilteredRows(){
    const soc = (FILTER_SOCORRISTA || "").trim().toLowerCase();
    const keySel = formatDateKey(selectedDate);

    const rows = ALL_ROWS.filter(r => {
      const fechaKey = parseSheetDateToKey(getField(r, ["Fecha","fecha"]));
      if(!fechaKey) return false;

      // desde hoy
      if(fechaKey < formatDateKey(currentDate)) return false;

      // filtro socorrista
      if(soc){
        const rs = String(getField(r, ["Socorrista","socorrista"])).trim().toLowerCase();
        if(rs !== soc) return false;
      }

      // modo por día / todo
      if(FILTER_MODE === "dia"){
        return fechaKey === keySel;
      }
      return true;
    });

    return rows;
  }

  function buildRowUI(r){
    const inst = getField(r, ["Instalacion","Instalación","instalacion"]);
    const ini  = getField(r, ["Ingreso","Inicio","ingreso","inicio"]);
    const fin  = getField(r, ["Salida","Finaliza","finaliza","salida"]);
    const hrs  = getField(r, ["Intensidad_horaria","Intensidad_ho","Horas","horas"]);
    const est0 = getField(r, ["estado","Estado","estado "]);

    const est = normalizeEstado(est0);

    const row = document.createElement('div');
    row.className = 'trow';

    const col0 = document.createElement('div');
    const chk = document.createElement('span');
    chk.className = 'chk';
    col0.appendChild(chk);
    col0.appendChild(document.createTextNode(' ' + (inst || '-')));

    const col1 = document.createElement('div'); col1.textContent = (ini || '-');
    const col2 = document.createElement('div'); col2.textContent = (fin || '-');
    const col3 = document.createElement('div'); col3.textContent = (hrs || '-');

    const col4 = document.createElement('div');
    const statusSpan = document.createElement('span');
    statusSpan.className = 'status ' + est.cls;
    statusSpan.textContent = est.label;
    col4.appendChild(statusSpan);

    row.appendChild(col0);
    row.appendChild(col1);
    row.appendChild(col2);
    row.appendChild(col3);
    row.appendChild(col4);

    return {row, est};
  }

  function updateAgenda(){
    const tbody = document.getElementById('tbody');
    tbody.innerHTML = '';

    // fecha label
    if(FILTER_MODE === "dia"){
      document.getElementById('fechaDisplay').textContent = formatDisplayDate(selectedDate);
    }else{
      document.getElementById('fechaDisplay').textContent = "Desde hoy";
    }

    const rows = getFilteredRows();

    if(rows.length === 0){
      const empty = document.createElement('div');
      empty.className = 'trow';
      empty.style.gridTemplateColumns = '1fr';
      empty.innerHTML = '<div class="muted">Sin registros para el filtro actual</div>';
      tbody.appendChild(empty);
      return;
    }

    rows.forEach(r => {
      const built = buildRowUI(r);
      tbody.appendChild(built.row);
    });
  }

  function updateBottomBar(){
    const rows = getFilteredRows();
    if(rows.length === 0){
      document.getElementById('bottomFecha').textContent = '—';
      const be = document.getElementById('bottomEstado');
      be.textContent = '—';
      be.className = 'status other';
      return;
    }

    const r0 = rows[0];
    const fechaKey = parseSheetDateToKey(getField(r0, ["Fecha","fecha"])) || formatDateKey(selectedDate);
    const inst = getField(r0, ["Instalacion","Instalación","instalacion"]) || "-";
    const ini  = getField(r0, ["Ingreso","Inicio","ingreso","inicio"]) || "-";
    const fin  = getField(r0, ["Salida","Finaliza","finaliza","salida"]) || "-";
    const est0 = getField(r0, ["estado","Estado","estado "]);

    document.getElementById('bottomFecha').textContent = `${fechaKey} · ${inst} · ${ini} → ${fin}`;

    const est = normalizeEstado(est0);
    const be = document.getElementById('bottomEstado');
    be.textContent = est.label;
    be.className = 'status ' + est.cls;
  }

  function changeMonth(delta) {
    let newMonth = currentMonth + delta;
    let newYear = currentYear;
    if (newMonth < 0) { newMonth = 11; newYear--; }
    else if (newMonth > 11) { newMonth = 0; newYear++; }

    currentMonth = newMonth;
    currentYear = newYear;

    let newSelectedDay = selectedDate.getDate();
    const dim = daysInMonth(newYear, newMonth);
    if (newSelectedDay > dim) newSelectedDay = dim;

    selectedDate = new Date(newYear, newMonth, newSelectedDay);

    renderCalendar(currentYear, currentMonth);
    updateAgenda();
    updateBottomBar();
    updateMonthYearDisplay(currentYear, currentMonth);
  }

  function fillSocorristaSelect(){
    const sel = document.getElementById("socorristaSelect");
    // reset dejando "Todos"
    sel.innerHTML = '<option value="">Todos los socorristas</option>';

    SOCORRISTAS.forEach(name => {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      sel.appendChild(opt);
    });

    sel.value = FILTER_SOCORRISTA || "";
  }

  function rebuildAvailability(){
    AVAILABLE_DATES = new Set();
    const soc = (FILTER_SOCORRISTA || "").trim().toLowerCase();

    ALL_ROWS.forEach(r => {
      const fechaKey = parseSheetDateToKey(getField(r, ["Fecha","fecha"]));
      if(!fechaKey) return;

      // desde hoy
      if(fechaKey < formatDateKey(currentDate)) return;

      if(soc){
        const rs = String(getField(r, ["Socorrista","socorrista"])).trim().toLowerCase();
        if(rs !== soc) return;
      }
      AVAILABLE_DATES.add(fechaKey);
    });
  }

  async function loadMallas(){
    setSyncBadge(false, "SYNC…");
    try{
      const res = await fetch(ENDPOINT_MALLAS, {method:"GET"});
      if(!res.ok) throw new Error("HTTP " + res.status);
      const data = await res.json();
      if(!data || data.ok !== true || !Array.isArray(data.rows)) throw new Error("JSON inválido");

      ALL_ROWS = data.rows;

      // SOCORRISTAS únicos
      const setS = new Set();
      ALL_ROWS.forEach(r => {
        const s = String(getField(r, ["Socorrista","socorrista"])).trim();
        if(s) setS.add(s);
      });
      SOCORRISTAS = Array.from(setS).sort((a,b)=>a.localeCompare(b, 'es', {sensitivity:'base'}));

      fillSocorristaSelect();

      rebuildAvailability();
      setSyncBadge(true, "SYNC OK");

      // pintar calendar y agenda
      renderCalendar(currentYear, currentMonth);
      updateAgenda();
      updateBottomBar();
    }catch(e){
      ALL_ROWS = [];
      SOCORRISTAS = [];
      AVAILABLE_DATES = new Set();
      setSyncBadge(false, "SYNC ERROR");
      renderCalendar(currentYear, currentMonth);
      updateAgenda();
      updateBottomBar();
    }
  }

  function init() {
    const yearSelect = document.getElementById('yearSelect');
    const y0 = new Date().getFullYear();
    for (let y = y0 - 5; y <= y0 + 5; y++) {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      yearSelect.appendChild(opt);
    }

    updateMonthYearDisplay(currentYear, currentMonth);

    document.getElementById('prevMonth').addEventListener('click', () => changeMonth(-1));
    document.getElementById('nextMonth').addEventListener('click', () => changeMonth(1));

    document.getElementById('applyFilters').addEventListener('click', () => {
      const newMonth = parseInt(document.getElementById('monthSelect').value);
      const newYear = parseInt(document.getElementById('yearSelect').value);
      FILTER_SOCORRISTA = document.getElementById('socorristaSelect').value || "";
      FILTER_MODE = document.getElementById('modeSelect').value || "dia";

      currentMonth = newMonth;
      currentYear = newYear;

      // mantener día válido
      let newSelectedDay = selectedDate.getDate();
      const dim = daysInMonth(newYear, newMonth);
      if (newSelectedDay > dim) newSelectedDay = dim;

      selectedDate = new Date(newYear, newMonth, newSelectedDay);

      rebuildAvailability();
      renderCalendar(currentYear, currentMonth);
      updateAgenda();
      updateBottomBar();
      updateMonthYearDisplay(currentYear, currentMonth);
    });

    // inicial UI sin datos (hasta cargar)
    renderCalendar(currentYear, currentMonth);
    updateAgenda();
    updateBottomBar();

    // cargar datos reales
    loadMallas();
  }

  init();
})();
</script>

</body>
</html>
"""

html = (
    html.replace("__PADX__", str(PAD_X_PX))
        .replace("__PADTOP__", str(PAD_TOP_PX))
        .replace("__B__", str(BORDER_PX))
        .replace("__BC__", BORDER_COLOR)
        .replace("__BG__", BG_COLOR)
        .replace("__PANEL__", PANEL_BG)
        .replace("__CARD__", CARD_BG)
        .replace("__TXT__", TEXT_COLOR)
        .replace("__MUTED__", MUTED_TEXT)
        .replace("__FBASE__", str(FONT_BASE_PX))
        .replace("__TITLE__", str(TITLE_PX))
        .replace("__H2__", str(H2_PX))
        .replace("__SMALL__", str(SMALL_PX))
        .replace("__INNERL__", str(INNER_L))
        .replace("__INNERR__", str(INNER_R))
        .replace("__GAPY__", str(INNER_TOP_GAP))
        .replace("__TOPBARH__", str(TOPBAR_H))
        .replace("__MONTHBARH__", str(MONTHBAR_H))
        .replace("__CALGRIDH__", str(CAL_GRID_H))
        .replace("__FILTERSH__", str(FILTERS_H))
        .replace("__AGENDAH__", str(AGENDA_H))
        .replace("__BOTTOMH__", str(BOTTOMBAR_H))
        .replace("__CELLGAP__", str(DAY_CELL_GAP_PX))
        .replace("__CALCOLS__", str(CAL_COLS))
        .replace("__CALROWS__", str(CAL_ROWS))
        .replace("__AGENDAROWS__", str(AGENDA_ROWS))
)

components.html(html, height=1100, scrolling=False)
