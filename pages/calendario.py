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
  :root{
    --padx: __PADX__px;
    --padtop: __PADTOP__px;

    --b: __B__px;
    --bc: __BC__;

    --bg: __BG__;
    --panel: __PANEL__;
    --card: __CARD__;
    --txt: __TXT__;
    --muted: __MUTED__;

    --fbase: __FBASE__px;
    --title: __TITLE__px;
    --h2: __H2__px;
    --small: __SMALL__px;

    --innerL: __INNERL__%;
    --innerR: __INNERR__%;
    --gapY: __GAPY__%;

    --topbarH: __TOPBARH__%;
    --monthbarH: __MONTHBARH__%;
    --calgridH: __CALGRIDH__%;
    --filtersH: __FILTERSH__%;
    --agendaH: __AGENDAH__%;
    --bottombarH: __BOTTOMH__%;

    --cellGap: __CELLGAP__px;

    --bg0:#06132c;
    --bg1:#081a3a;
    --bg2:#0c2248;

    --shadow0: 0 18px 40px rgba(0,0,0,.55);
    --shadow1: 0 12px 26px rgba(0,0,0,.45);
    --shadow2: 0 10px 18px rgba(0,0,0,.38);

    --accent: #ff7c2c;
    --accentGlow: 0 0 18px rgba(255,124,44,.35);

    --okBg: rgba(40,200,120,.12);
    --okLine: rgba(40,200,120,.28);

    --badBg: rgba(255,80,80,.12);
    --badLine: rgba(255,80,80,.28);
  }

  html, body{
    margin:0; padding:0;
    width:100%; height:100%;
    overflow:hidden;
    font-family: "Segoe UI", Arial, sans-serif;
    color: var(--txt);
    background:
      radial-gradient(1200px 700px at 50% 12%, rgba(60,140,255,.35) 0%, rgba(60,140,255,.12) 35%, rgba(6,19,44,0) 72%),
      radial-gradient(900px 520px at 20% 55%, rgba(255,124,44,.12) 0%, rgba(255,124,44,0) 65%),
      linear-gradient(180deg, var(--bg2) 0%, var(--bg1) 55%, var(--bg0) 100%);
  }

  #stage{
    position:fixed;
    inset:0;
    background:
      radial-gradient(1200px 700px at 50% 12%, rgba(60,140,255,.35) 0%, rgba(60,140,255,.12) 35%, rgba(6,19,44,0) 72%),
      radial-gradient(900px 520px at 20% 55%, rgba(255,124,44,.12) 0%, rgba(255,124,44,0) 65%),
      linear-gradient(180deg, var(--bg2) 0%, var(--bg1) 55%, var(--bg0) 100%);
  }

  #frame{
    position:absolute;
    left:var(--padx); right:var(--padx);
    top:var(--padtop); bottom:0;
    border-left:var(--b) solid var(--bc);
    border-right:var(--b) solid var(--bc);
    border-top:var(--b) solid var(--bc);
    box-sizing:border-box;
    pointer-events:none;
    box-shadow: inset 0 0 0 1px rgba(0,0,0,.35);
  }

  #plan{
    position:absolute;
    left:var(--padx); right:var(--padx);
    top:var(--padtop); bottom:0;
    overflow:hidden;
    background: transparent;
  }

  #wrap{
    position:absolute;
    left: var(--innerL);
    right: var(--innerR);
    top: 1.4%;
    bottom: 1.2%;
    display:flex;
    flex-direction:column;
  }

  .panel{
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 55%, rgba(255,255,255,.04) 100%);
    border: var(--b) solid var(--bc);
    border-radius: 14px;
    box-sizing:border-box;
    box-shadow: var(--shadow1);
    backdrop-filter: blur(10px);
  }

  .btn{
    background:
      radial-gradient(220px 80px at 24% 50%, rgba(120,210,255,.18) 0%, rgba(120,210,255,0) 68%),
      linear-gradient(180deg, rgba(18,78,185,.30) 0%, rgba(8,42,110,.42) 55%, rgba(4,24,66,.62) 100%);
    border: var(--b) solid rgba(255,255,255,.14);
    border-radius: 10px;
    box-sizing:border-box;
    padding: 10px 14px;
    font-weight: 700;
    font-size: var(--fbase);
    color: var(--txt);
    display:flex;
    align-items:center;
    justify-content:center;
    min-width: 92px;
    white-space:nowrap;
    box-shadow: var(--shadow2);
    user-select:none;
  }
  .btn.primary{
    background: linear-gradient(180deg, rgba(255,124,44,.95) 0%, rgba(255,106,0,.92) 100%);
    border-color: rgba(255,124,44,.55);
    color:#fff;
    box-shadow: var(--accentGlow), var(--shadow2);
  }

  .chip{
    border: var(--b) solid rgba(255,255,255,.14);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: var(--small);
    font-weight: 800;
    background: rgba(255,255,255,.06);
    color: var(--txt);
    display:inline-flex;
    align-items:center;
    gap:8px;
    white-space:nowrap;
    box-shadow: var(--shadow2);
  }

  .iconbtn{
    width:36px;height:36px;
    border: var(--b) solid rgba(255,255,255,.14);
    border-radius: 10px;
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
    display:flex;align-items:center;justify-content:center;
    font-weight: 900;
    color: var(--txt);
    user-select:none;
    box-shadow: var(--shadow2);
  }

  .muted{color: var(--muted);}

  #topbar{
    height: var(--topbarH);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
    background:
      radial-gradient(900px 240px at 35% 25%, rgba(120,210,255,.18) 0%, rgba(120,210,255,0) 70%),
      linear-gradient(180deg, rgba(30,70,150,.86) 0%, rgba(10,30,80,.92) 70%, rgba(6,19,44,.94) 100%);
  }
  #topbar .center{
    flex: 1;
    text-align:center;
    font-weight: 900;
    font-size: var(--h2);
    text-shadow: 0 2px 12px rgba(0,0,0,.35);
  }
  #topbar .right{
    display:flex;
    align-items:center;
    gap:10px;
    font-weight:800;
  }

  #monthbar{
    height: var(--monthbarH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 10px;
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  }
  #monthbar .month{
    font-weight: 900;
    font-size: var(--title);
    letter-spacing: 1px;
    flex:1;
    text-align:left;
    text-shadow: 0 2px 12px rgba(0,0,0,.28);
  }
  #monthbar .nav{display:flex; gap:10px; align-items:center;}

  #calgrid{
    height: var(--calgridH);
    margin-top: var(--gapY);
    padding: 8px 12px;
    display:flex;
    flex-direction:column;
    gap: 6px;
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  }
  #calgrid .head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
  }
  #calgrid .head .label{
    font-weight: 900;
    font-size: var(--fbase);
    letter-spacing:.6px;
    display:flex;
    align-items:center;
    gap:10px;
  }
  #syncBadge{
    font-size: 11px;
    font-weight: 900;
    padding: 4px 10px;
    border-radius: 999px;
    border: var(--b) solid rgba(255,255,255,.14);
    background: rgba(255,255,255,.06);
    color: rgba(234,242,255,.85);
    white-space:nowrap;
  }
  #syncBadge.ok{border-color: rgba(40,200,120,.35); background: rgba(40,200,120,.10); color: rgba(210,255,235,.95);}
  #syncBadge.err{border-color: rgba(255,80,80,.35); background: rgba(255,80,80,.10); color: rgba(255,220,220,.95);}

  #calgrid .weekheads{
    display:grid;
    grid-template-columns: repeat(__CALCOLS__, 1fr);
    gap: var(--cellGap);
    align-items:center;
    justify-items:center;
    font-size: var(--small);
    font-weight: 900;
    letter-spacing:.6px;
    color: rgba(234,242,255,.82);
    margin-top: -2px;
    user-select:none;
  }
  #calgrid .weekheads .w{width:100%;text-align:center;opacity:.92;}

  #calgrid .days{
    display:grid;
    grid-template-columns: repeat(__CALCOLS__, 1fr);
    grid-template-rows: repeat(__CALROWS__, 1fr);
    gap: var(--cellGap);
    flex:1;
    min-height: 0;
  }

  .day{
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
    border: var(--b) solid rgba(255,255,255,.14);
    border-radius: 10px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight: 900;
    font-size: var(--small);
    user-select:none;
    position:relative;
    color: var(--txt);
    box-shadow: var(--shadow2);
    cursor:pointer;
  }
  .day.dim{opacity:.35;}
  .day.sel{
    outline: 2px solid var(--accent);
    outline-offset: -2px;
    box-shadow: var(--accentGlow), var(--shadow2);
  }

  /* indicador "hay datos" */
  .day.hasdata::after{
    content:"";
    position:absolute;
    width:7px;height:7px;
    border-radius:50%;
    right:7px; bottom:7px;
    background: rgba(40,200,120,.70);
    box-shadow: 0 0 10px rgba(40,200,120,.35);
  }

  /* bloquear días antes de hoy (socorrista = desde hoy en adelante) */
  .day.past{
    opacity:.22;
    cursor:default;
    pointer-events:none;
    filter: grayscale(35%);
  }

  #legend{
    display:flex;
    align-items:center;
    gap:14px;
    font-size: 11px;
    font-weight: 900;
    color: var(--muted);
    margin-top: 0px;
  }
  .dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.35);display:inline-block;margin-right:6px;opacity:.35;}
  .dot.on{opacity:1; background: rgba(40,200,120,.65);}
  .dot.mid{opacity:1; background: rgba(255,80,80,.65);}

  #filters{
    height: var(--filtersH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:flex-end;
    gap: 12px;
    overflow:hidden;
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  }
  .select{
    min-width: 160px;
    padding: 10px 12px;
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
    border: var(--b) solid rgba(255,255,255,.14);
    border-radius: 10px;
    font-weight: 800;
    color: var(--txt);
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 10px;
    box-sizing:border-box;
    white-space:nowrap;
    box-shadow: var(--shadow2);
    position:relative;
  }
  .select select{
    background: transparent;
    border: none;
    color: inherit;
    font: inherit;
    outline: none;
    width: 100%;
    appearance: none;
    -webkit-appearance: none;
    cursor: pointer;
  }
  .select select option {background:#0c2248;color:#eaf2ff;}
  .caret{font-weight:900; pointer-events:none;}

  #agenda{
    height: var(--agendaH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    flex-direction:column;
    gap: 10px;
    min-height: 0;
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  }
  #agenda h3{margin:0;font-size: var(--h2);font-weight: 900;text-shadow: 0 2px 12px rgba(0,0,0,.28);}

  #table{
    flex:1;
    background: linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
    border: var(--b) solid rgba(255,255,255,.14);
    border-radius: 12px;
    overflow:hidden;
    display:flex;
    flex-direction:column;
    min-height: 0;
    box-shadow: var(--shadow2);
  }

  #thead, .trow{
    display:grid;
    grid-template-columns: 1fr 110px 110px 110px 110px;
    gap: 10px;
    align-items:center;
    padding: 10px 10px;
    box-sizing:border-box;
  }
  #thead{
    background: linear-gradient(180deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,.06) 100%);
    font-weight: 900;
    font-size: var(--small);
    color: rgba(234,242,255,.85);
    border-bottom: 1px solid rgba(255,255,255,.10);
  }
  .trow{
    border-top: 1px solid rgba(255,255,255,.08);
    font-weight: 800;
    font-size: var(--small);
    color: var(--txt);
  }

  .chk{
    width:18px;height:18px;
    border: var(--b) solid rgba(255,255,255,.18);
    border-radius: 4px;
    background: rgba(255,255,255,.06);
    display:inline-block;
    margin-right:8px;
    vertical-align:middle;
  }

  .status{
    justify-self:end;
    padding: 5px 10px;
    border-radius: 999px;
    border: var(--b) solid rgba(255,255,255,.14);
    font-weight: 900;
    font-size: 11px;
    background: rgba(255,255,255,.06);
    white-space:nowrap;
    color: var(--txt);
  }
  .status.free{border-color: var(--okLine);background: var(--okBg);color: rgba(210,255,235,.95);}
  .status.busy{border-color: var(--badLine);background: var(--badBg);color: rgba(255,220,220,.95);}
  .status.other{border-color: rgba(255,255,255,.18);background: rgba(255,255,255,.06);color: rgba(234,242,255,.85);}

  #bottom{
    height: var(--bottombarH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 12px;
    background:
      radial-gradient(900px 240px at 30% 10%, rgba(120,210,255,.12) 0%, rgba(120,210,255,0) 70%),
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 55%, rgba(255,255,255,.04) 100%);
    box-shadow: var(--shadow0);
  }
  #bottom .leftinfo{
    display:flex;
    align-items:center;
    gap: 12px;
    font-size: var(--small);
    font-weight: 900;
    color: var(--muted);
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
    min-width: 0;
  }
  #bottom .actions{display:flex;gap:10px;align-items:center;flex-shrink:0;}

  /* ===== MOBILE ===== */
  @media (max-width: 520px){
    html, body{overflow:hidden;}

    #filters{
      height: auto;
      display:grid;
      grid-template-columns: 1fr 1fr;
      grid-auto-rows: min-content;
      gap: 10px;
      justify-content: stretch;
      align-items: stretch;
    }
    #filters .select{min-width:0;width:100%;}
    #filters .btn{grid-column:1/-1;width:100%;min-width:0;}

    #thead{display:none;}
    .trow{
      grid-template-columns: 26px 1fr;
      grid-auto-rows: min-content;
      gap: 10px;
      align-items:start;
    }

    #bottom{
      height:auto;
      flex-direction:column;
      align-items:stretch;
      gap: 10px;
    }
    #bottom .actions{width:100%;justify-content:space-between;}
    #bottom .actions .btn{flex:1;min-width:0;}

    #monthbar .month{font-size:16px;}
  }
</style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="plan">
      <div id="wrap">

        <div id="topbar" class="panel">
          <div class="iconbtn">□</div>
          <div class="center">Calendario</div>
          <div class="right">
            <div id="userDisplay">Usuario</div>
            <div class="iconbtn">⌁</div>
            <div class="iconbtn">⋮</div>
          </div>
        </div>

        <div id="monthbar" class="panel">
          <div class="nav"><div class="iconbtn" id="prevMonth">‹</div></div>
          <div class="month" id="monthDisplay">—</div>
          <div class="nav"><div class="iconbtn" id="nextMonth">›</div></div>
        </div>

        <div id="calgrid" class="panel">
          <div class="head">
            <div class="label">
              <span>CALENDARIO</span>
              <span id="syncBadge">SYNC…</span>
            </div>
          </div>

          <div class="weekheads" aria-hidden="true">
            <div class="w">L</div>
            <div class="w">M</div>
            <div class="w">X</div>
            <div class="w">J</div>
            <div class="w">V</div>
            <div class="w">S</div>
            <div class="w">D</div>
          </div>

          <div class="days" id="days"></div>

          <div id="legend">
            <span><i class="dot on"></i>HAY DATOS</span>
            <span><i class="dot"></i>SIN DATOS</span>
          </div>
        </div>

        <div id="filters" class="panel">
          <div class="select">
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

          <div class="select">
            <select id="yearSelect"></select>
            <span class="caret">▾</span>
          </div>

          <div class="select">
            <select id="socorristaSelect">
              <option value="">Todos los socorristas</option>
            </select>
            <span class="caret">▾</span>
          </div>

          <div class="select">
            <select id="modeSelect">
              <option value="dia">Por día</option>
              <option value="todo">Ver todo (desde hoy)</option>
            </select>
            <span class="caret">▾</span>
          </div>

          <div class="btn primary" id="applyFilters">Aplicar</div>
        </div>

        <div id="agenda" class="panel">
          <h3>Agenda del día</h3>
          <div class="meta" id="agendaMeta">
            <div><b>Fecha:</b> <span id="fechaDisplay">—</span></div>
          </div>

          <div id="table">
            <div id="thead">
              <div>Instalación</div><div>Inicio</div><div>Finaliza</div><div>Horas</div><div>Estado</div>
            </div>
            <div id="tbody"></div>
          </div>
        </div>

        <div id="bottom" class="panel">
          <div class="leftinfo">
            <span class="chip" id="bottomFecha">—</span>
            <span class="status other" id="bottomEstado">—</span>
          </div>
          <div class="actions">
            <div class="btn">Aplicar</div>
            <div class="btn">Modificar</div>
            <div class="btn primary">Enviar</div>
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
