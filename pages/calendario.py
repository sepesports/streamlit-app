# pages/calendario.py
import json
import streamlit as st
import streamlit.components.v1 as components
import importlib
import syntra_core

# Recarga el modulo comun: el servidor puede quedarse con una version vieja en memoria
importlib.reload(syntra_core)
from syntra_core import sync_auth, go, shell_css, NAV_JS

# Logo oficial de SYNTRA incrustado (no depende de servidores externos)
LOGO_DATA_URI = "data:image/png;base64,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"

st.set_page_config(page_title="Horarios", layout="wide")
sync_auth()

query_params = st.query_params
AUTH_USER = query_params.get("usuario") or query_params.get("user") or ""
AUTH_ROLE = query_params.get("rol") or query_params.get("role") or ""
AUTH_DNI = query_params.get("dni") or ""

if not AUTH_USER or not AUTH_ROLE:
        go("pages/admin.py")

NORMALIZED_ROLE = AUTH_ROLE.strip().lower()
CAN_MANAGE_SCHEDULES = NORMALIZED_ROLE == "administrador"
CAN_REGISTER_USERS = NORMALIZED_ROLE == "administrador"
IS_SOCORRISTA = NORMALIZED_ROLE == "socorrista"

API_BASE = "https://camilo27.pythonanywhere.com"
LOGO_URL = LOGO_DATA_URI

st.markdown(
        """
            <style>
                  .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
                        section.main > div{padding:0 !important;margin:0 !important;}
                              header, footer{display:none !important;}
                                    iframe{display:block;}
                                        </style>
                                            """,
        unsafe_allow_html=True,
)
shell_css()


def _js_str(value) -> str:
        return json.dumps("" if value is None else str(value), ensure_ascii=False)


html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
:root{
--navy1:#0a1a55;--navy2:#040e31;--navy3:#02071c;--blue:#2f6fe0;
--bg:#f3f5f9;--card-bg:#ffffff;--ink:#0f1b3d;--muted:#6b7688;--border:#e7eaf1;
--manana:#c9f0d8;--tarde:#cfe2ff;--noche:#ffd7d7;--libre:#e9ecf3;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;width:100%;font-family:"Segoe UI",Arial,Helvetica,sans-serif;background:var(--bg);color:var(--ink);}
#app{display:flex;min-height:100vh;width:100%;}
#sidebar{
width:250px;flex:0 0 250px;
background:linear-gradient(180deg,var(--navy1) 0%,var(--navy2) 60%,var(--navy3) 100%);
color:#eaf2ff;display:flex;flex-direction:column;padding:26px 18px;min-height:100vh;
}
.logo-row{display:flex;align-items:center;gap:10px;margin-bottom:34px;padding:0 4px;}
.logo-row img{width:34px;height:34px;object-fit:contain;border-radius:6px;}
.logo-row span{font-weight:800;letter-spacing:2px;font-size:19px;}
.nav-item{display:flex;align-items:center;gap:12px;padding:11px 12px;border-radius:10px;margin-bottom:4px;color:rgba(234,242,255,.82);font-size:14.5px;font-weight:600;cursor:pointer;}
.nav-item:hover{background:rgba(255,255,255,.06);}
.nav-item.active{background:var(--blue);color:#fff;}
.nav-badge{margin-left:auto;font-size:10px;font-weight:700;background:rgba(255,255,255,.14);padding:2px 7px;border-radius:20px;white-space:nowrap;}
.nav-sep{height:1px;background:rgba(255,255,255,.10);margin:14px 4px;}
.nav-bottom{margin-top:auto;}

#main{flex:1;min-width:0;display:flex;flex-direction:column;}
#topbar{background:#fff;border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;}
#topbar h1{font-size:18px;margin:0;font-weight:700;}
.hamburger{display:none;font-size:20px;background:none;border:none;cursor:pointer;color:var(--ink);}
.mobile-logo{display:none;align-items:center;gap:8px;font-weight:800;letter-spacing:1px;}
.mobile-logo img{width:26px;height:26px;border-radius:6px;object-fit:contain;}

#content{padding:20px 24px 90px 24px;}
.filters-row{display:flex;gap:18px;align-items:flex-end;margin-bottom:16px;flex-wrap:wrap;}
.filter-field label{display:block;font-size:11.5px;color:var(--muted);margin-bottom:5px;font-weight:600;}
.filter-field select{padding:8px 12px;border:1px solid var(--border);border-radius:9px;font-size:13px;min-width:160px;}
.date-nav{display:flex;align-items:center;gap:10px;margin-left:auto;}
.date-nav button{background:#fff;border:1px solid var(--border);border-radius:8px;width:30px;height:30px;cursor:pointer;font-size:14px;}
.date-nav .date-label{font-size:13.5px;font-weight:700;display:flex;align-items:center;gap:6px;}

.day-tabs{display:none;}

.grid-wrap{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;overflow:auto;}
table.cal{width:100%;border-collapse:collapse;min-width:760px;}
table.cal th{background:#fafbfd;padding:10px 12px;font-size:12px;color:var(--muted);text-align:center;border-bottom:1px solid var(--border);border-right:1px solid var(--border);position:sticky;top:0;}
table.cal th:first-child{text-align:left;position:sticky;left:0;z-index:2;background:#fafbfd;}
table.cal td{padding:8px;border-bottom:1px solid var(--border);border-right:1px solid var(--border);vertical-align:top;min-width:110px;}
table.cal td.inst-cell{font-weight:700;font-size:13px;background:#fafbfd;position:sticky;left:0;white-space:nowrap;}
.turno-chip{border-radius:8px;padding:5px 8px;font-size:11px;margin-bottom:4px;line-height:1.3;}
.turno-chip .t{font-weight:700;}
.turno-chip.manana{background:var(--manana);}
.turno-chip.tarde{background:var(--tarde);}
.turno-chip.noche{background:var(--noche);}

.legend{display:flex;gap:18px;margin-top:14px;font-size:12px;color:var(--muted);flex-wrap:wrap;}
.legend span{display:inline-flex;align-items:center;gap:6px;}
.legend .dot{width:9px;height:9px;border-radius:50%;display:inline-block;}
.dot.manana{background:#12B39A;}
.dot.tarde{background:#2f6fe0;}
.dot.noche{background:#7C5CFF;}
.dot.libre{background:#9aa3b5;}

.mobile-list{display:none;}
.day-heading{font-size:15px;font-weight:800;margin:0 0 4px 0;}
.day-sub{font-size:12px;color:var(--muted);margin-bottom:12px;}
.shift{display:flex;gap:12px;align-items:stretch;background:#fff;border:1px solid var(--border);border-radius:14px;padding:12px 14px;margin-bottom:10px;}
.shift .bar{width:5px;border-radius:99px;flex:0 0 5px;}
.shift .bar.manana{background:#12B39A;}
.shift .bar.tarde{background:#2f6fe0;}
.shift .bar.noche{background:#7C5CFF;}
.shift .body{flex:1;min-width:0;}
.shift .hours{font-size:15px;font-weight:800;letter-spacing:.2px;}
.shift .who{font-size:13.5px;margin-top:2px;}
.shift .place{font-size:12px;color:var(--muted);margin-top:3px;display:flex;align-items:center;gap:5px;}
.shift .tag{font-size:10.5px;font-weight:800;padding:3px 8px;border-radius:99px;align-self:flex-start;text-transform:uppercase;letter-spacing:.3px;}
.tag.manana{background:#e3f7f2;color:#0c7a69;}
.tag.tarde{background:#e6eeff;color:#1f4fd8;}
.tag.noche{background:#efeaff;color:#5b3fd6;}
.empty-day{background:#fff;border:1px dashed var(--border);border-radius:14px;padding:26px 16px;text-align:center;color:var(--muted);font-size:13.5px;}
.empty-day .big{font-size:26px;display:block;margin-bottom:6px;}
.mobile-day-card{background:var(--card-bg);border:1px solid var(--border);border-radius:14px;padding:14px 16px;margin-bottom:12px;}
.mobile-day-card .inst-name{font-size:13px;font-weight:700;margin-bottom:8px;color:var(--muted);text-transform:uppercase;letter-spacing:.3px;}
.mobile-turno{border-radius:10px;padding:9px 12px;margin-bottom:6px;}
.mobile-turno .t{font-weight:700;font-size:13px;}
.mobile-turno .n{font-size:13px;}

.empty-note{padding:30px;text-align:center;color:var(--muted);font-size:13px;}

.mobile-drawer{display:none;position:fixed;inset:0;z-index:100;}
.mobile-drawer.open{display:block;}
.mobile-drawer .overlay{position:absolute;inset:0;background:rgba(0,0,0,.4);}
.mobile-drawer .panel{
position:absolute;left:0;top:0;bottom:0;width:250px;
background:linear-gradient(180deg,var(--navy1) 0%,var(--navy2) 60%,var(--navy3) 100%);
padding:26px 18px;color:#eaf2ff;overflow-y:auto;
}

@media (max-width:900px){
#sidebar{display:none;}
.hamburger{display:block;}
.mobile-logo{display:flex;}
#topbar h1{display:none;}
#topbar{padding:12px 14px;}
#content{padding:14px 12px 90px 12px;display:flex;flex-direction:column;flex:1;min-height:0;}
.mobile-list{flex:1;}
.legend{margin-top:auto;padding-top:12px;}
.filters-row{gap:10px;}
.filter-field select{min-width:0;flex:1;}
.date-nav{width:100%;margin-left:0;justify-content:space-between;}
.day-tabs{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin:2px 0 16px 0;}
.day-tab{padding:7px 0 6px 0;border-radius:12px;background:#fff;border:1px solid var(--border);cursor:pointer;color:var(--ink);text-align:center;line-height:1.1;}
.day-tab .dw{display:block;font-size:10.5px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;}
.day-tab .dn{display:block;font-size:16px;font-weight:800;margin-top:2px;}
.day-tab .dd{display:block;width:5px;height:5px;border-radius:50%;background:var(--blue);margin:3px auto 0 auto;}
.day-tab .dd.off{background:transparent;}
.day-tab.today{border-color:var(--blue);}
.day-tab.active{background:var(--blue);border-color:var(--blue);}
.day-tab.active .dw,.day-tab.active .dn{color:#fff;}
.day-tab.active .dd{background:#fff;}
.grid-wrap{display:none;}
.mobile-list{display:block;}
}

/* ===== SYNTRA reskin: hoja azul + cajas blancas (consistente con Inicio) ===== */
html,body{background:#1B2A4A !important;}
#app{min-height:100vh;gap:14px !important;padding:14px !important;box-sizing:border-box !important;align-items:stretch !important;}
#sidebar{background:#1B2A4A !important;border:1px solid rgba(255,255,255,.16) !important;border-radius:12px !important;min-height:0 !important;}
#main{gap:14px !important;min-height:0 !important;}
@media (max-width:900px){#app{height:100vh;overflow:hidden;}#main{flex:1;min-height:0;}#content{overflow-y:auto;}}
#topbar{background:#fff !important;border-bottom:none !important;border-radius:12px !important;box-shadow:0 4px 12px rgba(27,42,74,.08) !important;flex:0 0 auto !important;}
#content{background:#fff !important;border-radius:12px !important;box-shadow:0 4px 12px rgba(27,42,74,.08) !important;padding-bottom:22px !important;}
#chatBody{background:#fff !important;border-radius:12px !important;box-shadow:0 4px 12px rgba(27,42,74,.08) !important;overflow:hidden !important;}
@media (max-width:900px){#app{padding:10px !important;gap:10px !important;}}
</style>
</head>
<body>
<div id="app">
<div id="sidebar"><div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div><div id="navList"></div></div>
<div class="mobile-drawer" id="drawer">
<div class="overlay" id="drawerOverlay"></div>
<div class="panel"><div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div><div id="navListMobile"></div></div>
</div>
<div id="main">
<div id="topbar">
<button class="hamburger" id="hamburgerBtn">&#9776;</button>
<h1>Horarios</h1>
<div class="mobile-logo"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
<div></div>
</div>
<div id="content">
<div class="filters-row">
<div class="filter-field"><label>Instalaci&oacute;n</label>
<select id="instFilter"><option value="">Todas</option></select>
</div>
<div class="date-nav">
<button id="prevWeek">&#8249;</button>
<span class="date-label" id="weekLabel">&#128197; Cargando...</span>
<button id="nextWeek">&#8250;</button>
</div>
</div>
<div class="day-tabs" id="dayTabs"></div>
<div class="grid-wrap"><table class="cal"><thead><tr id="calHeadRow"></tr></thead><tbody id="calBody"></tbody></table></div>
<div class="mobile-list" id="mobileList"></div>
<div class="legend">
<span><span class="dot manana"></span>Ma&ntilde;ana</span>
<span><span class="dot tarde"></span>Tarde</span>
<span><span class="dot noche"></span>Noche</span>
<span><span class="dot libre"></span>Libre</span>
</div>
</div>
</div>
</div>

<script>
__SYNTRA_NAV__
(function(){
var API_BASE = __API_BASE__;
var AUTH_USER = __AUTH_USER__;
var AUTH_ROLE = __AUTH_ROLE__;
var AUTH_DNI = __AUTH_DNI__;
var CAN_MANAGE_SCHEDULES = __CAN_MANAGE_SCHEDULES__;
var CAN_REGISTER_USERS = __CAN_REGISTER_USERS__;
var IS_SOCORRISTA = __IS_SOCORRISTA__;

function qs(){
var p = new URLSearchParams();
p.set("auth", "ok"); p.set("usuario", AUTH_USER);
p.set("rol", AUTH_ROLE);
p.set("dni", AUTH_DNI);
return "?" + p.toString();
}
function goToPage(path){ syntraGoTo(path, function(){ window.open(path + qs(), "_blank"); }); }

var NAV_ITEMS = [
{label:"Inicio", icon:"&#8962;", go:"/"},
{label:"Horarios", icon:"&#128197;", go:"/calendario", active:true},
{label:"Incidencias y Comunicados", icon:"&#128172;", go:"/chat_interfaz"},
{sep:true},
{label:"Registro", icon:"&#128100;+", go:"/altas_registro", badge:"Solo admin"},
{label:"Gesti&oacute;n de Horarios", icon:"&#9881;", go:"/editar_horarios", badge:"Solo admin"}
];

function renderNav(containerId){
var el = document.getElementById(containerId);
var parts = [];
NAV_ITEMS.forEach(function(item){
if (item.sep){ parts.push('<div class="nav-sep"></div>'); return; }
var cls = "nav-item" + (item.active ? " active" : "");
var badge = item.badge ? '<span class="nav-badge">' + item.badge + '</span>' : "";
parts.push('<div class="' + cls + '" data-go="' + item.go + '"><span>' + item.icon + '</span><span>' + item.label + '</span>' + badge + '</div>');
});
parts.push('<div class="nav-bottom"><div class="nav-item" id="logout_' + containerId + '"><span>&#8630;</span><span>Cerrar sesi&oacute;n</span></div></div>');
el.innerHTML = parts.join("");
el.querySelectorAll(".nav-item[data-go]").forEach(function(node){
node.addEventListener("click", function(){ goToPage(node.getAttribute("data-go")); });
});
var lo = document.getElementById("logout_" + containerId);
if (lo) lo.addEventListener("click", function(){ syntraTopNav("/admin"); });
}
renderNav("navList");
renderNav("navListMobile");

var drawer = document.getElementById("drawer");
document.getElementById("hamburgerBtn").addEventListener("click", function(){ drawer.classList.add("open"); });
document.getElementById("drawerOverlay").addEventListener("click", function(){ drawer.classList.remove("open"); });

var DIAS_ES = ["Domingo","Lunes","Martes","Mi\u00e9rcoles","Jueves","Viernes","S\u00e1bado"];
var DIAS_CORTO = ["Dom","Lun","Mar","Mi\u00e9","Jue","Vie","S\u00e1b"];

function pad2(n){ return String(n).padStart(2,"0"); }
function ymd(d){ return d.getFullYear() + "-" + pad2(d.getMonth()+1) + "-" + pad2(d.getDate()); }

function parseFecha(str){
str = (str || "").trim();
if (!str) return null;
var parts = str.split("/");
if (parts.length === 3){
var d = parseInt(parts[0],10), m = parseInt(parts[1],10)-1, y = parseInt(parts[2],10);
return new Date(y, m, d);
}
var dt = new Date(str);
return isNaN(dt.getTime()) ? null : dt;
}

function startOfWeek(d){
var day = d.getDay();
var diff = (day === 0 ? -6 : 1) - day;
var res = new Date(d);
res.setDate(d.getDate() + diff);
res.setHours(0,0,0,0);
return res;
}

var mallasCache = [];
var weekStart = startOfWeek(new Date());
var activeDayIndex = new Date().getDay() === 0 ? 6 : new Date().getDay() - 1;

function turnoClass(ingreso){
var h = parseInt((ingreso || "0").split(":")[0], 10);
if (h < 13) return "manana";
if (h < 19) return "tarde";
return "noche";
}

function getWeekDays(){
var days = [];
for (var i = 0; i < 7; i++){
var d = new Date(weekStart);
d.setDate(weekStart.getDate() + i);
days.push(d);
}
return days;
}

function updateWeekLabel(){
var days = getWeekDays();
var first = days[0], last = days[6];
var monthsEs = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
var label = "&#128197; " + first.getDate() + " - " + last.getDate() + " " + monthsEs[last.getMonth()] + " " + last.getFullYear();
document.getElementById("weekLabel").innerHTML = label;
}

function populateInstFilter(){
var sel = document.getElementById("instFilter");
var seen = {};
mallasCache.forEach(function(r){
var inst = (r["Instalacion"] || "").trim();
if (inst && inst.toLowerCase() !== "descanso") seen[inst] = true;
});
var names = Object.keys(seen).sort();
names.forEach(function(n){
var opt = document.createElement("option");
opt.value = n; opt.textContent = n;
sel.appendChild(opt);
});
}

function filteredRows(){
var instFilter = document.getElementById("instFilter").value;
return mallasCache.filter(function(r){
var inst = (r["Instalacion"] || "").trim();
if (!inst || inst.toLowerCase() === "descanso") return false;
if (instFilter && inst !== instFilter) return false;
return true;
});
}

function renderDesktopGrid(){
var days = getWeekDays();
var rows = filteredRows();

var instSet = {};
rows.forEach(function(r){
var d = parseFecha(r["Fecha"]);
if (!d) return;
var key = ymd(d);
var weekKeys = days.map(ymd);
if (weekKeys.indexOf(key) === -1) return;
instSet[r["Instalacion"]] = true;
});
var instalaciones = Object.keys(instSet).sort();

var headRow = document.getElementById("calHeadRow");
headRow.innerHTML = "<th>Instalaci&oacute;n</th>" + days.map(function(d,i){
return "<th>" + DIAS_CORTO[d.getDay()] + " " + d.getDate() + "</th>";
}).join("");

var body = document.getElementById("calBody");
if (!instalaciones.length){
body.innerHTML = "<tr><td colspan='8' class='empty-note'>Sin turnos para esta semana.</td></tr>";
return;
}
body.innerHTML = instalaciones.map(function(inst){
var cells = days.map(function(d){
var key = ymd(d);
var matches = rows.filter(function(r){
var rd = parseFecha(r["Fecha"]);
return r["Instalacion"] === inst && rd && ymd(rd) === key;
});
if (!matches.length) return "<td></td>";
var chips = matches.map(function(r){
var cls = turnoClass(r["Ingreso"]);
return "<div class='turno-chip " + cls + "'><div class='t'>" + (r["Ingreso"]||"") + " - " + (r["Salida"]||"") + "</div><div>" + (r["Socorrista"]||"") + "</div></div>";
}).join("");
return "<td>" + chips + "</td>";
}).join("");
return "<tr><td class='inst-cell'>" + inst + "</td>" + cells + "</tr>";
}).join("");
}

function renderMobileList(){
var days = getWeekDays();
var activeDay = days[activeDayIndex];
var key = ymd(activeDay);
var rows = filteredRows().filter(function(r){
var rd = parseFecha(r["Fecha"]);
return rd && ymd(rd) === key;
});

var grouped = {};
rows.forEach(function(r){
var inst = r["Instalacion"];
if (!grouped[inst]) grouped[inst] = [];
grouped[inst].push(r);
});

var instNames = Object.keys(grouped).sort();
var wrap = document.getElementById("mobileList");
var MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
var esHoy = ymd(new Date()) === key;
var cab = "<div class='day-heading'>" + DIAS_ES[activeDay.getDay()] + " " + activeDay.getDate() + " de " + MESES[activeDay.getMonth()] + "</div>" +
"<div class='day-sub'>" + (esHoy ? "Hoy &middot; " : "") + rows.length + (rows.length === 1 ? " turno programado" : " turnos programados") + "</div>";

if (!rows.length){
wrap.innerHTML = cab + "<div class='empty-day'><span class='big'>&#127958;</span>Sin turnos para este d&iacute;a.<br/>Toca otro d&iacute;a de la semana para ver sus turnos.</div>";
return;
}

var NOMBRE_TURNO = {manana:"Ma&ntilde;ana", tarde:"Tarde", noche:"Noche"};
var orden = {manana:0, tarde:1, noche:2};

var items = [];
instNames.forEach(function(inst){
grouped[inst].forEach(function(r){ items.push(r); });
});
items.sort(function(a,b){
var ca = turnoClass(a["Ingreso"]), cb = turnoClass(b["Ingreso"]);
if (orden[ca] !== orden[cb]) return orden[ca] - orden[cb];
return String(a["Ingreso"]||"").localeCompare(String(b["Ingreso"]||""));
});

wrap.innerHTML = cab + items.map(function(r){
var cls = turnoClass(r["Ingreso"]);
return "<div class='shift'>" +
"<div class='bar " + cls + "'></div>" +
"<div class='body'>" +
"<div class='hours'>" + (r["Ingreso"]||"--:--") + " &ndash; " + (r["Salida"]||"--:--") + "</div>" +
"<div class='who'>" + (r["Socorrista"]||"Sin asignar") + "</div>" +
"<div class='place'>&#127958; " + (r["Instalacion"]||"") + "</div>" +
"</div>" +
"<span class='tag " + cls + "'>" + NOMBRE_TURNO[cls] + "</span>" +
"</div>";
}).join("");
}

function renderDayTabs(){
var days = getWeekDays();
var tabsEl = document.getElementById("dayTabs");
var rowsWeek = filteredRows();
var hoy = ymd(new Date());
tabsEl.innerHTML = days.map(function(d, i){
var key = ymd(d);
var tiene = rowsWeek.some(function(r){ var rd = parseFecha(r["Fecha"]); return rd && ymd(rd) === key; });
var cls = "day-tab" + (i === activeDayIndex ? " active" : "") + (key === hoy ? " today" : "");
return "<div class='" + cls + "' data-idx='" + i + "'>" +
"<span class='dw'>" + DIAS_CORTO[d.getDay()] + "</span>" +
"<span class='dn'>" + d.getDate() + "</span>" +
"<span class='dd" + (tiene ? "" : " off") + "'></span>" +
"</div>";
}).join("");
tabsEl.querySelectorAll(".day-tab").forEach(function(node){
node.addEventListener("click", function(){
activeDayIndex = parseInt(node.getAttribute("data-idx"), 10);
renderDayTabs();
renderMobileList();
});
});
}

function renderAll(){
updateWeekLabel();
renderDesktopGrid();
renderDayTabs();
renderMobileList();
}

document.getElementById("prevWeek").addEventListener("click", function(){
weekStart.setDate(weekStart.getDate() - 7);
renderAll();
});
document.getElementById("nextWeek").addEventListener("click", function(){
weekStart.setDate(weekStart.getDate() + 7);
renderAll();
});
document.getElementById("instFilter").addEventListener("change", renderAll);

fetch(API_BASE + "/api/mallas")
.then(function(r){ return r.json(); })
.then(function(d){
mallasCache = (d && d.ok && d.rows) ? d.rows : [];
populateInstFilter();
renderAll();
})
.catch(function(){
document.getElementById("calBody").innerHTML = "<tr><td colspan='8' class='empty-note'>Error al cargar horarios.</td></tr>";
document.getElementById("mobileList").innerHTML = "<div class='empty-note'>Error al cargar horarios.</div>";
});
})();
</script>
</body>
</html>
"""

html = (
        html.replace("__LOGO_URL__", LOGO_URL)
            .replace("__API_BASE__", _js_str(API_BASE))
            .replace("__AUTH_USER__", _js_str(AUTH_USER))
            .replace("__AUTH_ROLE__", _js_str(AUTH_ROLE))
            .replace("__AUTH_DNI__", _js_str(AUTH_DNI))
            .replace("__CAN_MANAGE_SCHEDULES__", "true" if CAN_MANAGE_SCHEDULES else "false")
            .replace("__CAN_REGISTER_USERS__", "true" if CAN_REGISTER_USERS else "false")
            .replace("__IS_SOCORRISTA__", "true" if IS_SOCORRISTA else "false")
)

html = html.replace("__SYNTRA_NAV__", NAV_JS)

components.html(html, height=900, scrolling=True)
