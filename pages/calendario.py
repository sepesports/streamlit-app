# calendario.py
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# PLANTILLA "CALENDARIO" — (MISMA ESTRUCTURA / MISMAS MEDIDAS) + TEMA HUD NARANJA
# ==============================================================================

# ================== AJUSTES (NO TOCAR MEDIDAS) ==================

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
CAL_ROWS = 3
DAY_CELL_GAP_PX = 8

AGENDA_ROWS = 5

# ===============================================================

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

    /* TEMA HUD */
    --bg0:#06132c;
    --bg1:#081a3a;
    --bg2:#0c2248;

    --line: rgba(255,255,255,.12);
    --line2: rgba(255,255,255,.10);

    --shadow0: 0 18px 40px rgba(0,0,0,.55);
    --shadow1: 0 12px 26px rgba(0,0,0,.45);
    --shadow2: 0 10px 18px rgba(0,0,0,.38);

    --accent: #ff7c2c;
    --accentGlow: 0 0 18px rgba(255,124,44,.35);

    --ok: rgba(40,200,120,.95);
    --okBg: rgba(40,200,120,.12);
    --okLine: rgba(40,200,120,.28);

    --bad: rgba(255,80,80,.95);
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
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 55%, rgba(255,255,255,.04) 100%);
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
    transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, filter .12s ease;
    user-select:none;
  }
  .btn:hover{
    transform: translateY(-2px);
    box-shadow: 0 16px 34px rgba(0,0,0,.52);
    border-color: rgba(255,124,44,.35);
    filter: saturate(1.06);
  }
  .btn:active{ transform: translateY(0px); }

  .btn.primary{
    background: linear-gradient(180deg, rgba(255,124,44,.95) 0%, rgba(255,106,0,.92) 100%);
    border-color: rgba(255,124,44,.55);
    color: #ffffff;
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
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
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
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
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
    padding: 10px 12px;
    display:flex;
    flex-direction:column;
    gap: 10px;
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
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
  }
  #calgrid .days{
    display:grid;
    grid-template-columns: repeat(__CALCOLS__, 1fr);
    grid-template-rows: repeat(__CALROWS__, 1fr);
    gap: var(--cellGap);
    flex:1;
    min-height: 0;
  }
  .day{
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
    border: var(--b) solid rgba(255,255,255,.14);
    border-radius: 10px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight: 900;
    user-select:none;
    position:relative;
    min-height: 34px;
    color: var(--txt);
    box-shadow: var(--shadow2);
  }
  .day.dim{opacity:.35;}

  .day.sel{
    outline: 2px solid var(--accent);
    outline-offset: -2px;
    box-shadow: var(--accentGlow), var(--shadow2);
  }

  .day.mark::after{
    content:"";
    position:absolute;
    bottom:6px;
    width:7px;height:7px;
    border-radius:50%;
    background: var(--accent);
    opacity:.95;
    box-shadow: 0 0 10px rgba(255,124,44,.35);
  }

  #legend{
    display:flex;
    align-items:center;
    gap:14px;
    font-size: var(--small);
    font-weight: 800;
    color: var(--muted);
    margin-top: 2px;
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
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  }
  .select{
    min-width: 160px;
    padding: 10px 12px;
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
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
  .caret{font-weight:900; pointer-events:none;}

  #agenda{
    height: var(--agendaH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    flex-direction:column;
    gap: 10px;
    min-height: 0;
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  }
  #agenda h3{
    margin:0;
    font-size: var(--h2);
    font-weight: 900;
    text-shadow: 0 2px 12px rgba(0,0,0,.28);
  }
  #agenda .meta{
    display:flex;
    gap: 18px;
    font-size: var(--small);
    font-weight: 800;
    color: var(--muted);
    flex-wrap:wrap;
  }

  #table{
    flex:1;
    background:
      linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
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
    background:
      linear-gradient(180deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,.06) 100%);
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

  .status.free{
    border-color: var(--okLine);
    background: var(--okBg);
    color: rgba(210,255,235,.95);
  }
  .status.busy{
    border-color: var(--badLine);
    background: var(--badBg);
    color: rgba(255,220,220,.95);
  }

  .rowmeta{
    display:none;
    margin-top: 4px;
    font-size: 11px;
    color: var(--muted);
    font-weight: 800;
    gap: 10px;
  }

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
  #bottom .actions{
    display:flex;
    gap: 10px;
    align-items:center;
    flex-shrink:0;
  }

  /* ===== MOBILE ===== */
  @media (max-width: 520px){

    #filters{
      height: auto;
      display:grid;
      grid-template-columns: 1fr 1fr;
      grid-auto-rows: min-content;
      gap: 10px;
      justify-content: stretch;
      align-items: stretch;
    }
    #filters .select{
      min-width: 0;
      width: 100%;
    }
    #filters .btn{
      grid-column: 1 / -1;
      width: 100%;
      min-width: 0;
    }

    #thead{ display:none; }

    .trow{
      grid-template-columns: 26px 1fr;
      grid-auto-rows: min-content;
      gap: 10px;
      align-items:start;
    }
    .trow > .col_time,
    .trow > .col_time2,
    .trow > .col_status{
      display:none;
    }

    .rowmeta{
      display:flex;
      flex-wrap:wrap;
      align-items:center;
    }
    .rowmeta .pill{
      border: 1px solid rgba(255,255,255,.16);
      border-radius: 999px;
      padding: 3px 8px;
      background: rgba(255,255,255,.08);
      font-weight: 900;
      color: var(--txt);
      white-space:nowrap;
    }

    #bottom{
      height:auto;
      flex-direction:column;
      align-items:stretch;
      gap: 10px;
    }
    #bottom .leftinfo{
      justify-content:space-between;
    }
    #bottom .actions{
      width:100%;
      justify-content:space-between;
    }
    #bottom .actions .btn{
      flex:1;
      min-width: 0;
    }

    #monthbar .month{font-size: 16px;}
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
            <div id="userDisplay">Jefe</div>
            <div class="iconbtn">⌁</div>
            <div class="iconbtn">⋮</div>
          </div>
        </div>

        <div id="monthbar" class="panel">
          <div class="nav"><div class="iconbtn" id="prevMonth">‹</div></div>
          <div class="month" id="monthDisplay">FEBRERO 2026</div>
          <div class="nav"><div class="iconbtn" id="nextMonth">›</div></div>
        </div>

        <div id="calgrid" class="panel">
          <div class="head">
            <div class="label">CALENDARIO</div>
            <div class="muted" style="font-weight:900;font-size:var(--small);">LU MA MI JU VI SA DO</div>
          </div>

          <div class="days" id="days"></div>

          <div id="legend">
            <span><i class="dot on"></i>LIBRE</span>
            <span><i class="dot mid"></i>OCUPADO</span>
            <span><i class="dot"></i>OTRO</span>
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
          <div class="btn primary" id="applyFilters">Aplicar</div>
        </div>

        <div id="agenda" class="panel">
          <h3>Agenda del día</h3>
          <div class="meta" id="agendaMeta">
            <div><b>Fecha:</b> <span id="fechaDisplay">15 febrero 2026</span></div>
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
            <span class="chip" id="bottomFecha">2026-02-15 · Rocafort · 09:00:00 → 15:00:00</span>
            <span class="status free" id="bottomEstado">LIBRE</span>
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
  // ==================== OBTENER USUARIO ====================
  function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
  }
  const userName = getQueryParam('usuario') || 'Usuario';
  document.getElementById('userDisplay').textContent = userName;

  // ==================== VARIABLES GLOBALES ====================
  let currentDate = new Date(); // hoy
  let selectedDate = new Date(currentDate); // copia
  // Ajustar a medianoche para evitar problemas de zona horaria
  currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
  selectedDate = new Date(currentDate);

  // ==================== UTILIDADES ====================
  function formatDate(date) {
    const d = date.getDate().toString().padStart(2,'0');
    const m = (date.getMonth()+1).toString().padStart(2,'0');
    const y = date.getFullYear();
    return `${y}-${m}-${d}`;
  }

  function formatDisplayDate(date) {
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function getMonday(date) {
    const d = new Date(date);
    const day = d.getDay(); // 0 domingo, 1 lunes, ...
    const diff = (day === 0 ? 6 : day - 1); // si domingo, restar 6 para ir al lunes anterior
    d.setDate(d.getDate() - diff);
    return d;
  }

  // Obtiene 21 días (3 semanas) centrados en la semana que contiene centerDate
  function getThreeWeeks(centerDate) {
    const mondayCenter = getMonday(centerDate);
    const prevMonday = new Date(mondayCenter);
    prevMonday.setDate(mondayCenter.getDate() - 7);
    const nextMonday = new Date(mondayCenter);
    nextMonday.setDate(mondayCenter.getDate() + 7);

    const weeks = [prevMonday, mondayCenter, nextMonday];
    const days = [];
    for (let w = 0; w < 3; w++) {
      for (let d = 0; d < 7; d++) {
        const day = new Date(weeks[w]);
        day.setDate(weeks[w].getDate() + d);
        days.push(day);
      }
    }
    return days;
  }

  // ==================== RENDERIZAR CALENDARIO ====================
  function renderCalendar(centerDate) {
    const daysEl = document.getElementById('days');
    daysEl.innerHTML = '';

    const days = getThreeWeeks(centerDate);
    const currentYear = centerDate.getFullYear();
    const currentMonth = centerDate.getMonth();

    days.forEach(date => {
      const cell = document.createElement('div');
      cell.className = 'day';
      cell.textContent = date.getDate();

      // Si el día no es del mes actual, atenuar
      if (date.getMonth() !== currentMonth) {
        cell.classList.add('dim');
      }

      // Marcar si es el día seleccionado
      if (date.toDateString() === selectedDate.toDateString()) {
        cell.classList.add('sel');
      }

      // Añadir evento de selección
      cell.addEventListener('click', function() {
        selectedDate = new Date(date);
        renderCalendar(centerDate); // re-renderiza con el mismo centro (puede no estar visible si cambia mes)
        // Pero para asegurar que el día seleccionado esté visible, deberíamos recentrar
        // Para simplificar, recentramos en el día seleccionado
        renderCalendar(selectedDate);
        updateAgenda(selectedDate);
        updateBottomBar(selectedDate);
        updateMonthYearDisplay(selectedDate);
      });

      daysEl.appendChild(cell);
    });

    // Actualizar título del mes
    document.getElementById('monthDisplay').textContent = 
      centerDate.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' }).toUpperCase();
  }

  // ==================== ACTUALIZAR SELECTORES MES/AÑO ====================
  function updateMonthYearDisplay(date) {
    const monthSelect = document.getElementById('monthSelect');
    const yearSelect = document.getElementById('yearSelect');
    monthSelect.value = date.getMonth();
    yearSelect.value = date.getFullYear();
  }

  // ==================== RENDERIZAR AGENDA ====================
  function updateAgenda(date) {
    const fechaSpan = document.getElementById('fechaDisplay');
    fechaSpan.textContent = formatDisplayDate(date);

    const tbody = document.getElementById('tbody');
    tbody.innerHTML = '';

    // Datos de ejemplo (pueden ser reemplazados por fetch a Google Sheets)
    const instalaciones = ['Cn Fabra', 'Arsenal', 'Guissona', 'Descanso', 'St. Jordi'];
    // Generar eventos aleatorios pero coherentes con el día
    const numEventos = 5; // para llenar la tabla
    for (let i = 0; i < numEventos; i++) {
      const inst = instalaciones[i % instalaciones.length];
      const inicio = `${8 + i}:00:00`;
      const fin = `${12 + i}:00:00`;
      const estado = i % 2 === 0 ? 'LIBRE' : 'OCUPADO';
      const estadoClass = estado === 'LIBRE' ? 'free' : 'busy';
      // Calcular horas (ejemplo simple)
      const horas = (parseInt(fin) - parseInt(inicio)) + 'h';

      const row = document.createElement('div');
      row.className = 'trow';

      // Columna Instalación (con checkbox)
      const col0 = document.createElement('div');
      const chk = document.createElement('span');
      chk.className = 'chk';
      if (i === 0) chk.style.background = 'rgba(255,124,44,.95)'; // ejemplo marcado
      col0.appendChild(chk);
      col0.appendChild(document.createTextNode(' ' + inst));

      // Columnas de tiempo y estado
      const col1 = document.createElement('div');
      col1.textContent = inicio;
      const col2 = document.createElement('div');
      col2.textContent = fin;
      const col3 = document.createElement('div');
      col3.textContent = horas;
      const col4 = document.createElement('div');
      const statusSpan = document.createElement('span');
      statusSpan.className = 'status ' + estadoClass;
      statusSpan.textContent = estado;
      col4.appendChild(statusSpan);

      row.appendChild(col0);
      row.appendChild(col1);
      row.appendChild(col2);
      row.appendChild(col3);
      row.appendChild(col4);

      // Para móvil, añadir meta (ya lo maneja el CSS)
      tbody.appendChild(row);
    }
  }

  // ==================== ACTUALIZAR BARRA INFERIOR ====================
  function updateBottomBar(date) {
    // Ejemplo con datos fijos, se puede adaptar
    document.getElementById('bottomFecha').textContent = formatDate(date) + ' · Rocafort · 09:00:00 → 15:00:00';
    // Podríamos cambiar el estado según el día
    document.getElementById('bottomEstado').textContent = 'LIBRE';
    document.getElementById('bottomEstado').className = 'status free';
  }

  // ==================== CAMBIO DE MES ====================
  function changeMonth(delta) {
    let newDate = new Date(selectedDate);
    newDate.setMonth(selectedDate.getMonth() + delta);
    selectedDate = newDate;
    renderCalendar(selectedDate);
    updateAgenda(selectedDate);
    updateBottomBar(selectedDate);
    updateMonthYearDisplay(selectedDate);
  }

  // ==================== INICIALIZACIÓN ====================
  function init() {
    // Llenar selector de años (desde 2020 hasta 2030)
    const yearSelect = document.getElementById('yearSelect');
    const currentYear = new Date().getFullYear();
    for (let y = currentYear - 5; y <= currentYear + 5; y++) {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      yearSelect.appendChild(opt);
    }

    // Eventos de navegación
    document.getElementById('prevMonth').addEventListener('click', () => changeMonth(-1));
    document.getElementById('nextMonth').addEventListener('click', () => changeMonth(1));

    // Evento de aplicar filtros (mes/año)
    document.getElementById('applyFilters').addEventListener('click', () => {
      const newMonth = parseInt(document.getElementById('monthSelect').value);
      const newYear = parseInt(document.getElementById('yearSelect').value);
      // Crear nueva fecha con el primer día del mes seleccionado
      const newDate = new Date(newYear, newMonth, 1);
      selectedDate = newDate;
      renderCalendar(selectedDate);
      updateAgenda(selectedDate);
      updateBottomBar(selectedDate);
      updateMonthYearDisplay(selectedDate);
    });

    // Render inicial con hoy
    renderCalendar(selectedDate);
    updateAgenda(selectedDate);
    updateBottomBar(selectedDate);
    updateMonthYearDisplay(selectedDate);
  }

  init();

  // Ajustar frame
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
  })();
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
