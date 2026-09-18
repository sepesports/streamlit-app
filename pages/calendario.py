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
<div id="sidebar"><div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="width:32px;height:32px;flex:0 0 auto;display:block;border-radius:8px;object-fit:cover;"/><span>SYNTRA</span></div><div id="navList"></div></div>
<div class="mobile-drawer" id="drawer">
<div class="overlay" id="drawerOverlay"></div>
<div class="panel"><div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="width:32px;height:32px;flex:0 0 auto;display:block;border-radius:8px;object-fit:cover;"/><span>SYNTRA</span></div><div id="navListMobile"></div></div>
</div>
<div id="main">
<div id="topbar">
<button class="hamburger" id="hamburgerBtn">&#9776;</button>
<h1>Horarios</h1>
<div class="mobile-logo"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="width:32px;height:32px;flex:0 0 auto;display:block;border-radius:8px;object-fit:cover;"/>SYNTRA</div>
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
