# pages/calendario.py
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# CALENDARIO - TEMA HUD NARANJA (VERSIÓN CORREGIDA CON RUTEO SEGURO)
# ==============================================================================

query_params = st.query_params
AUTH_USER = query_params.get("usuario") or query_params.get("user") or ""
AUTH_ROLE = query_params.get("rol") or query_params.get("role") or ""
AUTH_DNI = query_params.get("dni") or ""

NORMALIZED_ROLE = AUTH_ROLE.strip().lower()
IS_SOCORRISTA = NORMALIZED_ROLE == "socorrista"
IS_ADMIN_OR_DIRECTIVO = NORMALIZED_ROLE in ["administrador", "directivo"]

if not AUTH_USER or not AUTH_ROLE:
    st.markdown(
        """
        <script>
          window.location.href="/admin";
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

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

def escape_js(s):
    return str(s).replace('"', '\\"').replace("'", "\\'")

# ===================== CÓDIGO HTML COMPLETO =====================
html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  :root {
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
    --pad-outer: 16px;
    --pad-block: 14px;
  }
  *{box-sizing:border-box;}
  html,body{height:100%;margin:0;padding:0;}
  body{
    font-family: "Inter", system-ui, -apple-system, "SF Pro Display", Segoe UI, Roboto, Arial, sans-serif;
    color:var(--txt-0);
    background: none;
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
    align-items: flex-start;
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
    overflow: hidden;
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
  @media (min-width: 1400px) {
    #wrap { width: min(1200px, 80vw); max-width: 1400px; }
  }
  .monthBlock{
    margin-top:0;
    padding:12px 8px 6px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
  }
  .monthBlock .nav{ display:flex; align-items:center; gap:10px; }
  .monthNav__btn{
    width:38px; height:38px;
    border-radius:14px;
    background:rgba(255,255,255,.05);
    border:1px solid var(--stroke);
    box-shadow:0 0 18px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.08);
    display:grid;
    place-items:center;
    cursor:pointer;
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
    cursor:pointer;
  }
  .day.dim{ color:var(--txt-3); background:rgba(255,255,255,.03); border-color:rgba(255,255,255,.07); }
  .day.sel{
    border:2px solid var(--glow-orange);
    box-shadow:0 0 0 2px rgba(255,124,44,.10), 0 0 18px var(--glow-orange-2), inset 0 1px 0 rgba(255,255,255,.08);
    color:var(--txt-0);
  }
  .day.past{ opacity:.22; cursor:default; pointer-events:none; filter:grayscale(35%); }
  .day.hasdata::after{
    content:"";
    position:absolute;
    width:7px; height:7px;
    border-radius:50%;
    right:7px; bottom:7px;
    background:var(--free);
    box-shadow:0 0 10px var(--free);
  }
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
  .legend__dot.on{ background:var(--free); box-shadow:0 0 14px var(--free); }
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
  .selectPill select option { background: var(--bg-1); color: var(--txt-0); }
  .selectPill .caret{ font-weight:900; pointer-events:none; }
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
    cursor:pointer;
  }
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
    overflow: hidden;
    flex:1;
    display:flex;
    flex-direction:column;
    min-height:0;
  }
  .tableHeader, .trow.desktop {
    display: grid;
    grid-template-columns: 26px 1fr 92px 92px 86px auto;
    gap: 10px;
    align-items: center;
  }
  .tableHeader{
    padding:12px 14px;
    font-size:12px;
    font-weight:700;
    color:var(--txt-2);
    background:rgba(255,255,255,.03);
    border-bottom:1px solid rgba(255,255,255,.08);
  }
  .trow.desktop{
    padding:11px 14px;
    border-bottom:1px solid rgba(255,255,255,.06);
  }
  .trow.desktop:last-child{border-bottom:none;}
  .trow.desktop div:nth-child(1){
    font-size:var(--fs-table);
    color:var(--txt-0);
    font-weight:650;
    display:flex;
    align-items:center;
    gap:8px;
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
  .status.free{ background:linear-gradient(180deg, rgba(79,227,140,1), rgba(46,196,118,1)); box-shadow:0 0 14px rgba(79,227,140,.22); }
  .status.busy{ background:linear-gradient(180deg, rgba(255,90,90,1), rgba(230,55,55,1)); box-shadow:0 0 14px rgba(255,75,75,.22); color:rgba(255,255,255,.92); }
  .status.other{ background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2); color:var(--txt-1); }
  .mobile-header { display: none; padding: 10px 12px; background: rgba(255,255,255,.03); border-bottom: 1px solid rgba(255,255,255,.08); font-weight: 700; color: var(--txt-2); font-size: 12px; }
  .mobile-header .horas { display: flex; gap: 8px; flex: 1; }
  .mobile-header .horas span:first-child { width: 70px; }
  .mobile-header .horas span:nth-child(2) { width: 70px; }
  .mobile-header .horas span:last-child { width: 60px; text-align: right; }
  .trow.mobile { display: block; border-bottom: 1px solid rgba(255,255,255,.06); padding: 0; }
  .row-main { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; cursor: pointer; background: rgba(255,255,255,.02); }
  .row-main .horas { display: flex; gap: 8px; flex: 1; font-size: 13px; }
  .row-main .horas span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .row-main .horas span:first-child { width: 70px; }
  .row-main .horas span:nth-child(2) { width: 70px; }
  .row-main .horas span:last-child { width: 60px; text-align: right; }
  .expand-icon { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; border-radius: 12px; background: var(--glass); border: 1px solid var(--stroke); font-size: 16px; font-weight: bold; color: var(--txt-1); transition: transform 0.2s; }
  .row-detail { display: none; padding: 8px 12px 12px; background: rgba(0,0,0,.2); border-top: 1px solid rgba(255,255,255,.05); font-size: 13px; grid-template-columns: 1fr auto; gap: 8px; }
  .row-detail .instalacion { color: var(--txt-0); font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .row-detail .estado { justify-self: end; }
  .trow.mobile.expanded .row-detail { display: grid; }
  .trow.mobile.expanded .expand-icon { transform: rotate(45deg); }
  .footerBlock{ margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,.08); }
  .footerActions{ margin-top:12px; display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; }
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
    transition: opacity 0.2s;
  }
  .btn:disabled, .btn.disabled { opacity: 0.4; pointer-events: none; }
  .btn--primary, .btn.primary{
    border-color:rgba(255,124,44,.75);
    background:rgba(255,124,44,.06);
    color:rgba(255,124,44,.95);
    box-shadow:0 0 18px var(--glow-orange-2), inset 0 1px 0 rgba(255,255,255,.10);
  }
  .modal-overlay {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.7);
    backdrop-filter: blur(5px);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  .modal {
    background: var(--bg-1);
    border: 1px solid var(--stroke);
    border-radius: var(--radius-card);
    padding: 24px;
    max-width: 400px;
    width: 90%;
    box-shadow: var(--shadow-soft);
    color: var(--txt-0);
  }
  .modal h3 { margin-top: 0; }
  .modal-option { margin: 12px 0; }
  .modal-option label { margin-left: 8px; }
  .modal-input { margin-top: 8px; margin-left: 24px; }
  .modal-input input { width: 100%; padding: 8px; border-radius: 8px; border: 1px solid var(--stroke); background: var(--glass); color: var(--txt-0); }
  .modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; }
  .modal-actions .btn { width: auto; padding: 0 20px; }
  @media (min-width: 1400px) {
    .controlsRow { grid-template-columns: repeat(4, 1fr) auto; }
    .tableHeader, .trow.desktop { grid-template-columns: 26px 2fr 1fr 1fr 1fr 1fr; }
  }
  @media (max-width:520px){
    #wrap { width: 98vw; padding: 12px; overflow-y: auto; display: block; max-height: 95vh; height: 95vh; }
    .controlsRow{ grid-template-columns:1fr 1fr; grid-auto-rows:min-content; }
    .controlsRow .applyBtn{ grid-column:1/-1; }
    .tableHeader { display: none; }
    .mobile-header { display: block; }
    .trow.desktop { display: none; }
    .trow.mobile { display: block; }
    .tableCard { max-height: none; height: auto; min-height: 0; }
    .agendaBlock { margin-top: 12px; }
    .agendaTitle { margin-bottom: 5px; }
    .agendaMeta { margin-bottom: 5px; }
  }
  @media (max-width:380px){
    :root{ --fs-title:24px; }
    .calendarGrid{gap:8px;}
    .day{height:34px;}
  }
</style>
</head>
<body>
<div id="stage">
  <div id="frame"></div>
  <div id="plan">
    <div id="wrap">
      <div id="monthbar" class="panel monthBlock">
        <div class="nav"><div class="iconbtn monthNav__btn" id="prevMonth">‹</div></div>
        <div class="month monthNav__title" id="monthDisplay">—</div>
        <div class="nav"><div class="iconbtn monthNav__btn" id="nextMonth">›</div></div>
      </div>
      <div id="calgrid" class="panel calendarCard">
        <div class="head calendarCard__labelRow">
          <div class="label calendarCard__label"><span>CALENDARIO</span><span id="syncBadge">SYNC…</span></div>
        </div>
        <div class="weekheads weekdays"><div class="w">L</div><div class="w">M</div><div class="w">X</div><div class="w">J</div><div class="w">V</div><div class="w">S</div><div class="w">D</div></div>
        <div class="days calendarGrid" id="days"></div>
        <div id="legend" class="legend">
          <span class="legend__item"><i class="dot on legend__dot"></i>HAY DATOS</span>
          <span class="legend__item"><i class="dot legend__dot"></i>SIN DATOS</span>
        </div>
      </div>
      <div id="filters" class="panel controlsRow">
        <div class="select selectPill"><select id="monthSelect"><option value="0">Enero</option><option value="1">Febrero</option><option value="2">Marzo</option><option value="3">Abril</option><option value="4">Mayo</option><option value="5">Junio</option><option value="6">Julio</option><option value="7">Agosto</option><option value="8">Septiembre</option><option value="9">Octubre</option><option value="10">Noviembre</option><option value="11">Diciembre</option></select><span class="caret">▾</span></div>
        <div class="select selectPill"><select id="yearSelect"></select><span class="caret">▾</span></div>
        <div class="select selectPill" id="socorristaSelectContainer"><select id="socorristaSelect"><option value="">Todos los socorristas</option></select><span class="caret">▾</span></div>
        <div class="select selectPill"><select id="modeSelect"><option value="dia">Por día</option><option value="todo">Ver todo (desde hoy)</option></select><span class="caret">▾</span></div>
        <div class="btn primary applyBtn" id="applyFilters">Aplicar</div>
      </div>
      <div id="agenda" class="panel agendaBlock">
        <h3 class="agendaTitle">Agenda del día</h3>
        <div class="meta agendaMeta" id="agendaMeta"><div><b>Fecha:</b> <span id="fechaDisplay">—</span></div><div><b>Usuario:</b> <span id="userDisplay">""" + escape_js(AUTH_USER) + """</span> (<span id="roleDisplay">""" + escape_js(AUTH_ROLE) + """</span>)</div></div>
        <div id="table" class="tableCard">
          <div class="mobile-header"><div style="width:26px;"></div><div class="horas"><span>Inicio</span><span>Finaliza</span><span>Horas</span></div><div style="width:24px;"></div></div>
          <div id="thead" class="tableHeader"><div></div><div>Instalación</div><div>Inicio</div><div>Finaliza</div><div>Horas</div><div>Estado</div></div>
          <div id="tbody"></div>
        </div>
      </div>
      <div id="bottom" class="panel footerBlock"><div class="actions footerActions"><button class="btn" id="btnAplicar">Aplicar</button><button class="btn" id="btnModificar">Modificar</button><button class="btn primary btn--primary" id="btnEnviar">Enviar</button></div></div>
    </div>
  </div>
</div>
<div class="modal-overlay" id="modalOverlay"><div class="modal" id="modal"><h3>Modificar turno</h3><div class="modal-option"><input type="radio" name="modalOption" id="optLiberar" value="liberar" checked><label for="optLiberar">Liberar Turno</label></div><div class="modal-option"><input type="radio" name="modalOption" id="optNovedad" value="novedad"><label for="optNovedad">Novedad</label><div class="modal-input" id="novedadInput" style="display:none;"><input type="text" placeholder="Escriba la novedad..."></div></div><div class="modal-option"><input type="radio" name="modalOption" id="optCalamidad" value="calamidad"><label for="optCalamidad">Calamidad</label></div><div class="modal-actions"><button class="btn" id="modalCancel">Cancelar</button><button class="btn primary" id="modalSend">Enviar</button></div></div></div>
<script>
(function(){
  const API_BASE = "https://camilo27.pythonanywhere.com";
  const ENDPOINT_MALLAS = API_BASE + "/api/mallas";
  const CURRENT_USER = \"""" + escape_js(AUTH_USER) + """\";
  const CURRENT_ROLE = \"""" + escape_js(AUTH_ROLE) + """\".toLowerCase();
  const CURRENT_DNI = \"""" + escape_js(AUTH_DNI) + """\";
  const IS_SOCORRISTA = CURRENT_ROLE === "socorrista";
  let currentDate = new Date();
  currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
  let selectedDate = new Date(currentDate);
  let currentMonth = selectedDate.getMonth();
  let currentYear = selectedDate.getFullYear();
  let ALL_ROWS = [];
  let AVAILABLE_DATES = new Set();
  let SOCORRISTAS = [];
  let FILTER_SOCORRISTA = "";
  let FILTER_MODE = "dia";
  let selectedRows = new Set();
  let currentFilteredRows = [];
  let DNI_COLUMN_NAME = null;

  if (IS_SOCORRISTA) {
    document.addEventListener('DOMContentLoaded', function() {
      const container = document.getElementById('socorristaSelectContainer');
      if (container) container.style.display = 'none';
    });
  }

  function pad2(n){ return String(n).padStart(2,'0'); }
  function toKeyYMD(y,m,d){ return `${y}-${pad2(m)}-${pad2(d)}`; }
  function formatDateKey(date) { return toKeyYMD(date.getFullYear(), date.getMonth()+1, date.getDate()); }
  function formatDisplayDate(date) { return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' }); }
  function parseSheetDateToKey(fechaStr) {
    const s = (fechaStr || "").trim();
    if (!s) return "";
    const parts = s.split('/');
    if (parts.length === 3) {
      let dd = parts[0].padStart(2, '0');
      let mm = parts[1].padStart(2, '0');
      let yyyy = parts[2];
      if (yyyy.length === 4 && mm >= 1 && mm <= 12 && dd >= 1 && dd <= 31) return `${yyyy}-${mm}-${dd}`;
    }
    if (/^\d{4}-\d{2}-\d{2}$/.test(s)) return s;
    const d = new Date(s);
    if (!isNaN(d.getTime())) return d.getFullYear() + '-' + pad2(d.getMonth()+1) + '-' + pad2(d.getDate());
    return "";
  }
  function getField(row, keys){ for(const k of keys){ if(row && Object.prototype.hasOwnProperty.call(row, k)) return row[k]; } return ""; }
  function detectDNIColumn(row) {
    const possibleNames = ["DNI","dni","Cédula","cedula","Documento","documento","Cedula de ciudadania","Numero documento","Número documento","Identificación","identificacion","ID","id"];
    for (let name of possibleNames) if (row.hasOwnProperty(name)) { console.log(`✅ Columna DNI detectada: "${name}"`); return name; }
    console.warn("⚠️ No se encontró columna DNI");
    return null;
  }
  function normalizeEstado(s){
    const v = String(s || "").trim().toLowerCase();
    if(!v) return {label:"OTRO", cls:"other"};
    if(v.includes("libre")) return {label:"LIBRE", cls:"free"};
    if(v.includes("ocup")) return {label:"OCUPADO", cls:"busy"};
    return {label:String(s).toUpperCase(), cls:"other"};
  }
  function getDisplayStatus(row) {
    const rawEstado = getField(row, ["estado","Estado","estado "]).toLowerCase().trim();
    const socorrista = getField(row, ["Socorrista","socorrista"]).trim();
    if (rawEstado.includes("disponible")) return { label: "Disponible", cls: "free" };
    if (rawEstado.includes("programado")) {
      if (socorrista.toLowerCase() === CURRENT_USER.toLowerCase()) return { label: "Programado", cls: "free" };
      else return { label: "Cerrado", cls: "busy" };
    }
    return normalizeEstado(rawEstado);
  }
  function formatTime(t) { if (!t) return '-'; const str = String(t); return str.replace(/(\d{1,2}:\d{2}):\d{2}$/, '$1'); }
  function setSyncBadge(ok, text){ const el = document.getElementById("syncBadge"); el.textContent = text; el.className = ok ? "ok" : "err"; }
  function daysInMonth(year, month) { return new Date(year, month + 1, 0).getDate(); }
  function getFirstDayOfMonth(year, month) { let day = new Date(year, month, 1).getDay(); return day === 0 ? 7 : day; }
  function getMonthDays(year, month) {
    const firstDay = getFirstDayOfMonth(year, month);
    const totalDays = daysInMonth(year, month);
    const days = [];
    const prevMonthDays = firstDay - 1;
    if (prevMonthDays > 0) {
      const prevMonth = month === 0 ? 11 : month - 1;
      const prevYear = month === 0 ? year - 1 : year;
      const daysPrev = daysInMonth(prevYear, prevMonth);
      for (let i = prevMonthDays; i > 0; i--) days.push({ date: new Date(prevYear, prevMonth, daysPrev - i + 1), currentMonth: false });
    }
    for (let d = 1; d <= totalDays; d++) days.push({ date: new Date(year, month, d), currentMonth: true });
    const remaining = 7 - (days.length % 7);
    if (remaining < 7) {
      const nextMonth = month === 11 ? 0 : month + 1;
      const nextYear = month === 11 ? year + 1 : year;
      for (let i = 1; i <= remaining; i++) days.push({ date: new Date(nextYear, nextMonth, i), currentMonth: false });
    }
    while (days.length < 42) { const last = days[days.length-1].date; const nd = new Date(last.getFullYear(), last.getMonth(), last.getDate()+1); days.push({ date: nd, currentMonth: false }); }
    if (days.length > 42) days.length = 42;
    return days;
  }
  function updateMonthYearDisplay(year, month) { document.getElementById('monthSelect').value = month; document.getElementById('yearSelect').value = year; }
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
      if (date < currentDate) cell.classList.add('past');
      const key = formatDateKey(date);
      if (AVAILABLE_DATES.has(key)) cell.classList.add('hasdata');
      if (date.getFullYear() === selectedDate.getFullYear() && date.getMonth() === selectedDate.getMonth() && date.getDate() === selectedDate.getDate()) cell.classList.add('sel');
      cell.addEventListener('click', function() {
        if(date < currentDate) return;
        selectedDate = new Date(date);
        if (date.getMonth() !== month || date.getFullYear() !== year) { currentMonth = date.getMonth(); currentYear = date.getFullYear(); renderCalendar(currentYear, currentMonth); updateMonthYearDisplay(currentYear, currentMonth); }
        else { renderCalendar(year, month); }
        updateAgenda();
      });
      daysEl.appendChild(cell);
    });
    document.getElementById('monthDisplay').textContent = new Date(year, month, 1).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' }).toUpperCase();
  }
  function getFilteredRows(){
    const soc = (FILTER_SOCORRISTA || "").trim().toLowerCase();
    const keySel = formatDateKey(selectedDate);
    return ALL_ROWS.filter(r => {
      const fechaKey = parseSheetDateToKey(getField(r, ["Fecha","fecha"]));
      if(!fechaKey) return false;
      if(fechaKey < formatDateKey(currentDate)) return false;
      if (IS_SOCORRISTA && CURRENT_DNI) {
        let rowDNI = "";
        if (DNI_COLUMN_NAME) rowDNI = String(r[DNI_COLUMN_NAME] || "").trim();
        else rowDNI = String(getField(r, ["DNI","dni","Cédula","cedula","Documento","documento","Cedula de ciudadania","Numero documento"])).trim();
        if (rowDNI.toLowerCase() !== CURRENT_DNI.toLowerCase()) return false;
      }
      if (!IS_SOCORRISTA && soc) {
        const rs = String(getField(r, ["Socorrista","socorrista"])).trim().toLowerCase();
        if(rs !== soc) return false;
      }
      if(FILTER_MODE === "dia") return fechaKey === keySel;
      return true;
    });
  }
  function isMobile() { return window.innerWidth <= 520; }
  function updateButtons() {
    const aplicarBtn = document.getElementById('btnAplicar');
    const modificarBtn = document.getElementById('btnModificar');
    if (!aplicarBtn || !modificarBtn) return;
    if (selectedRows.size === 0) { aplicarBtn.disabled = true; modificarBtn.disabled = true; return; }
    let allDisponible = true, allProgramado = true;
    for (let idx of selectedRows) {
      const row = currentFilteredRows[idx];
      if (!row) continue;
      const status = getDisplayStatus(row).label;
      if (status !== 'Disponible') allDisponible = false;
      if (status !== 'Programado') allProgramado = false;
    }
    aplicarBtn.disabled = !allDisponible;
    modificarBtn.disabled = !allProgramado;
  }
  function buildDesktopRow(r, idx) {
    const inst = getField(r, ["Instalacion","Instalación","instalacion"]);
    const ini = formatTime(getField(r, ["Ingreso","Inicio","ingreso","inicio"]));
    const fin = formatTime(getField(r, ["Salida","Finaliza","finaliza","salida"]));
    const hrs = formatTime(getField(r, ["Intensidad_horaria","Intensidad_ho","Horas","horas"]));
    const est = getDisplayStatus(r);
    const row = document.createElement('div'); row.className = 'trow desktop'; row.dataset.index = idx;
    const col0 = document.createElement('div');
    const chk = document.createElement('input'); chk.type = 'checkbox'; chk.className = 'row-checkbox'; chk.dataset.index = idx; chk.checked = selectedRows.has(idx);
    chk.addEventListener('click', (e) => e.stopPropagation());
    chk.addEventListener('change', (e) => { if(e.target.checked) selectedRows.add(idx); else selectedRows.delete(idx); updateButtons(); });
    col0.appendChild(chk);
    const col1 = document.createElement('div'); col1.textContent = inst || '-';
    const col2 = document.createElement('div'); col2.textContent = ini;
    const col3 = document.createElement('div'); col3.textContent = fin;
    const col4 = document.createElement('div'); col4.textContent = hrs;
    const col5 = document.createElement('div');
    const statusSpan = document.createElement('span'); statusSpan.className = 'status ' + est.cls; statusSpan.textContent = est.label;
    col5.appendChild(statusSpan);
    row.appendChild(col0); row.appendChild(col1); row.appendChild(col2); row.appendChild(col3); row.appendChild(col4); row.appendChild(col5);
    return row;
  }
  function buildMobileRow(r, idx) {
    const inst = getField(r, ["Instalacion","Instalación","instalacion"]) || '-';
    const ini = formatTime(getField(r, ["Ingreso","Inicio","ingreso","inicio"]));
    const fin = formatTime(getField(r, ["Salida","Finaliza","finaliza","salida"]));
    const hrs = formatTime(getField(r, ["Intensidad_horaria","Intensidad_ho","Horas","horas"]));
    const est = getDisplayStatus(r);
    const row = document.createElement('div'); row.className = 'trow mobile'; row.dataset.index = idx;
    const main = document.createElement('div'); main.className = 'row-main';
    const chk = document.createElement('input'); chk.type = 'checkbox'; chk.className = 'row-checkbox'; chk.dataset.index = idx; chk.checked = selectedRows.has(idx);
    chk.addEventListener('click', (e) => e.stopPropagation());
    chk.addEventListener('change', (e) => { if(e.target.checked) selectedRows.add(idx); else selectedRows.delete(idx); updateButtons(); });
    main.appendChild(chk);
    const horasDiv = document.createElement('div'); horasDiv.className = 'horas';
    const spanIni = document.createElement('span'); spanIni.textContent = ini;
    const spanFin = document.createElement('span'); spanFin.textContent = fin;
    const spanHrs = document.createElement('span'); spanHrs.textContent = hrs;
    horasDiv.appendChild(spanIni); horasDiv.appendChild(spanFin); horasDiv.appendChild(spanHrs);
    const expandIcon = document.createElement('div'); expandIcon.className = 'expand-icon'; expandIcon.textContent = '+';
    main.appendChild(horasDiv); main.appendChild(expandIcon);
    const detail = document.createElement('div'); detail.className = 'row-detail';
    const instDiv = document.createElement('div'); instDiv.className = 'instalacion'; instDiv.textContent = inst;
    const estadoDiv = document.createElement('div'); estadoDiv.className = 'estado';
    const statusSpan = document.createElement('span'); statusSpan.className = 'status ' + est.cls; statusSpan.textContent = est.label;
    estadoDiv.appendChild(statusSpan);
    detail.appendChild(instDiv); detail.appendChild(estadoDiv);
    row.appendChild(main); row.appendChild(detail);
    main.addEventListener('click', function(e) { if (e.target.type === 'checkbox') return; e.stopPropagation(); row.classList.toggle('expanded'); expandIcon.textContent = row.classList.contains('expanded') ? '−' : '+'; });
    return row;
  }
  function updateAgenda(){
    const tbody = document.getElementById('tbody');
    tbody.innerHTML = '';
    if(FILTER_MODE === "dia") document.getElementById('fechaDisplay').textContent = formatDisplayDate(selectedDate);
    else document.getElementById('fechaDisplay').textContent = "Desde hoy";
    const rows = getFilteredRows();
    currentFilteredRows = rows;
    selectedRows.clear();
    if(rows.length === 0){
      const empty = document.createElement('div');
      empty.className = isMobile() ? 'trow mobile' : 'trow desktop';
      empty.style.textAlign = 'center'; empty.style.padding = '20px';
      empty.innerHTML = '<div class="muted">Sin registros para el filtro actual</div>';
      tbody.appendChild(empty);
      updateButtons();
      return;
    }
    const mobile = isMobile();
    rows.forEach((r, idx) => { const row = mobile ? buildMobileRow(r, idx) : buildDesktopRow(r, idx); tbody.appendChild(row); });
    updateButtons();
  }
  function changeMonth(delta) {
    let newMonth = currentMonth + delta, newYear = currentYear;
    if (newMonth < 0) { newMonth = 11; newYear--; }
    else if (newMonth > 11) { newMonth = 0; newYear++; }
    currentMonth = newMonth; currentYear = newYear;
    let newSelectedDay = selectedDate.getDate();
    const dim = daysInMonth(newYear, newMonth);
    if (newSelectedDay > dim) newSelectedDay = dim;
    selectedDate = new Date(newYear, newMonth, newSelectedDay);
    renderCalendar(currentYear, currentMonth);
    updateAgenda();
    updateMonthYearDisplay(currentYear, currentMonth);
  }
  function fillSocorristaSelect(){
    const sel = document.getElementById("socorristaSelect");
    sel.innerHTML = '<option value="">Todos los socorristas</option>';
    SOCORRISTAS.forEach(name => { const opt = document.createElement("option"); opt.value = name; opt.textContent = name; sel.appendChild(opt); });
    sel.value = FILTER_SOCORRISTA || "";
  }
  function rebuildAvailability(){
    AVAILABLE_DATES = new Set();
    const soc = (FILTER_SOCORRISTA || "").trim().toLowerCase();
    ALL_ROWS.forEach(r => {
      const fechaKey = parseSheetDateToKey(getField(r, ["Fecha","fecha"]));
      if(!fechaKey) return;
      if(fechaKey < formatDateKey(currentDate)) return;
      if (IS_SOCORRISTA && CURRENT_DNI) {
        let rowDNI = "";
        if (DNI_COLUMN_NAME) rowDNI = String(r[DNI_COLUMN_NAME] || "").trim();
        else rowDNI = String(getField(r, ["DNI","dni","Cédula","cedula","Documento","documento","Cedula de ciudadania","Numero documento"])).trim();
        if (rowDNI.toLowerCase() !== CURRENT_DNI.toLowerCase()) return;
      } else if (!IS_SOCORRISTA && soc) {
        const rs = String(getField(r, ["Socorrista","socorrista"])).trim().toLowerCase();
        if(rs !== soc) return;
      }
      AVAILABLE_DATES.add(fechaKey);
    });
  }
  async function loadMallas(){
    setSyncBadge(false, "SYNC…");
    try{
      const res = await fetch(ENDPOINT_MALLAS);
      if(!res.ok) throw new Error("HTTP "+res.status);
      const data = await res.json();
      if(!data || data.ok !== true || !Array.isArray(data.rows)) throw new Error("JSON inválido");
      ALL_ROWS = data.rows;
      console.log("=== DEPURACIÓN ===");
      if(ALL_ROWS.length>0){
        console.log("Primera fila:", ALL_ROWS[0]);
        console.log("Columnas:", Object.keys(ALL_ROWS[0]));
        DNI_COLUMN_NAME = detectDNIColumn(ALL_ROWS[0]);
        if(DNI_COLUMN_NAME) console.log(`Usando columna DNI: "${DNI_COLUMN_NAME}"`);
      }
      console.log("CURRENT_DNI:", CURRENT_DNI);
      const setS = new Set();
      ALL_ROWS.forEach(r => {
        if(IS_SOCORRISTA && CURRENT_DNI){
          let rowDNI = "";
          if(DNI_COLUMN_NAME) rowDNI = String(r[DNI_COLUMN_NAME] || "").trim();
          else rowDNI = String(getField(r, ["DNI","dni","Cédula","cedula","Documento","documento","Cedula de ciudadania","Numero documento"])).trim();
          if(rowDNI.toLowerCase() === CURRENT_DNI.toLowerCase()){
            const s = String(getField(r, ["Socorrista","socorrista"])).trim();
            if(s) setS.add(s);
          }
        } else {
          const s = String(getField(r, ["Socorrista","socorrista"])).trim();
          if(s) setS.add(s);
        }
      });
      SOCORRISTAS = Array.from(setS).sort((a,b)=>a.localeCompare(b,'es',{sensitivity:'base'}));
      fillSocorristaSelect();
      rebuildAvailability();
      setSyncBadge(true, "SYNC OK");
      renderCalendar(currentYear, currentMonth);
      updateAgenda();
    }catch(e){
      console.error("Error loading mallas:", e);
      ALL_ROWS = []; SOCORRISTAS = []; AVAILABLE_DATES.clear();
      setSyncBadge(false, "SYNC ERROR");
      renderCalendar(currentYear, currentMonth);
      updateAgenda();
    }
  }
  const modalOverlay = document.getElementById('modalOverlay');
  const modalCancel = document.getElementById('modalCancel');
  const modalSend = document.getElementById('modalSend');
  const optNovedad = document.getElementById('optNovedad');
  const novedadInput = document.getElementById('novedadInput');
  function showModal() { modalOverlay.style.display = 'flex'; }
  function hideModal() { modalOverlay.style.display = 'none'; }
  if(optNovedad) optNovedad.addEventListener('change', function(e){ novedadInput.style.display = e.target.checked ? 'block' : 'none'; });
  if(modalCancel) modalCancel.addEventListener('click', hideModal);
  if(modalSend) modalSend.addEventListener('click', hideModal);
  if(modalOverlay) modalOverlay.addEventListener('click', function(e){ if(e.target === modalOverlay) hideModal(); });
  function init(){
    const yearSelect = document.getElementById('yearSelect');
    const y0 = new Date().getFullYear();
    for(let y=y0-5; y<=y0+5; y++){ const opt = document.createElement('option'); opt.value = y; opt.textContent = y; yearSelect.appendChild(opt); }
    updateMonthYearDisplay(currentYear, currentMonth);
    document.getElementById('prevMonth').addEventListener('click', ()=>changeMonth(-1));
    document.getElementById('nextMonth').addEventListener('click', ()=>changeMonth(1));
    document.getElementById('applyFilters').addEventListener('click', ()=>{
      const newMonth = parseInt(document.getElementById('monthSelect').value);
      const newYear = parseInt(document.getElementById('yearSelect').value);
      if(!IS_SOCORRISTA) FILTER_SOCORRISTA = document.getElementById('socorristaSelect').value || "";
      FILTER_MODE = document.getElementById('modeSelect').value || "dia";
      currentMonth = newMonth; currentYear = newYear;
      let newSelectedDay = selectedDate.getDate();
      const dim = daysInMonth(newYear, newMonth);
      if(newSelectedDay > dim) newSelectedDay = dim;
      selectedDate = new Date(newYear, newMonth, newSelectedDay);
      rebuildAvailability();
      renderCalendar(currentYear, currentMonth);
      updateAgenda();
      updateMonthYearDisplay(currentYear, currentMonth);
    });
    window.addEventListener('resize', ()=>updateAgenda());
    const btnModificar = document.getElementById('btnModificar');
    if(btnModificar) btnModificar.addEventListener('click', function(){ if(!this.disabled) showModal(); });
    const btnAplicar = document.getElementById('btnAplicar');
    const btnModificarEl = document.getElementById('btnModificar');
    if(btnAplicar) btnAplicar.disabled = true;
    if(btnModificarEl) btnModificarEl.disabled = true;
    renderCalendar(currentYear, currentMonth);
    updateAgenda();
    loadMallas();
  }
  init();
})();
</script>
</body>
</html>
"""

html = (html.replace("__PADX__", str(PAD_X_PX))
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
