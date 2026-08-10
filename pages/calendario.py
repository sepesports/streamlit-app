# pages/calendario.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Horarios", layout="wide")

query_params = st.query_params
AUTH_USER = query_params.get("usuario") or query_params.get("user") or ""
AUTH_ROLE = query_params.get("rol") or query_params.get("role") or ""
AUTH_DNI = query_params.get("dni") or ""

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

NORMALIZED_ROLE = AUTH_ROLE.strip().lower()
CAN_MANAGE_SCHEDULES = NORMALIZED_ROLE == "administrador"
CAN_REGISTER_USERS = NORMALIZED_ROLE == "administrador"
IS_SOCORRISTA = NORMALIZED_ROLE == "socorrista"

API_BASE = "https://camilo27.pythonanywhere.com"
LOGO_URL = "https://files.catbox.moe/056m6v.jpg"

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
.dot.manana{background:#3fbf76;}
.dot.tarde{background:#3f7fd6;}
.dot.noche{background:#d64f4f;}
.dot.libre{background:#9aa3b5;}

.mobile-list{display:none;}
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
#content{padding:14px 12px 90px 12px;}
.filters-row{gap:10px;}
.filter-field select{min-width:0;flex:1;}
.date-nav{width:100%;margin-left:0;justify-content:space-between;}
.day-tabs{display:flex;gap:6px;overflow-x:auto;margin-bottom:14px;}
.day-tab{flex:0 0 auto;padding:8px 14px;border-radius:10px;background:#fff;border:1px solid var(--border);font-size:12.5px;font-weight:700;cursor:pointer;color:var(--muted);}
.day-tab.active{background:var(--blue);color:#fff;border-color:var(--blue);}
.grid-wrap{display:none;}
.mobile-list{display:block;}
}
</style>
</head>
<body>
<div id="app">
<div id="sidebar"><div class="logo-row"><img src="__LOGO_URL__"/><span>SYNTRA</span></div><div id="navList"></div></div>
<div class="mobile-drawer" id="drawer">
<div class="overlay" id="drawerOverlay"></div>
<div class="panel"><div class="logo-row"><img src="__LOGO_URL__"/><span>SYNTRA</span></div><div id="navListMobile"></div></div>
</div>
<div id="main">
<div id="topbar">
<button class="hamburger" id="hamburgerBtn">&#9776;</button>
<h1>Horarios</h1>
<div class="mobile-logo"><img src="__LOGO_URL__"/>SYNTRA</div>
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
p.set("usuario", AUTH_USER);
p.set("rol", AUTH_ROLE);
p.set("dni", AUTH_DNI);
return "?" + p.toString();
}
function goToPage(path){ window.parent.location.href = path + qs(); }

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
if (lo) lo.addEventListener("click", function(){ window.parent.location.href = "/admin"; });
}
renderNav("navList");
renderNav("navListMobile");

var drawer = document.getElementById("drawer");
document.getElementById("hamburgerBtn").addEventListener("click", function(){ drawer.classList.add("open"); });
document.getElementById("drawerOverlay").addEventListener("click", function(){ drawer.classList.remove("open"); });

var DIAS_ES = ["Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado"];
var DIAS_CORTO = ["Dom","Lun","Mar","Mie","Jue","Vie","Sab"];

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
if (!instNames.length){
wrap.innerHTML = "<div class='empty-note'>Sin turnos para este d&iacute;a.</div>";
return;
}
wrap.innerHTML = instNames.map(function(inst){
var turnos = grouped[inst].map(function(r){
var cls = turnoClass(r["Ingreso"]);
var bg = cls === "manana" ? "var(--manana)" : cls === "tarde" ? "var(--tarde)" : "var(--noche)";
return "<div class='mobile-turno' style='background:" + bg + ";'><div class='t'>" + (r["Ingreso"]||"") + " - " + (r["Salida"]||"") + "</div><div class='n'>" + (r["Socorrista"]||"") + "</div></div>";
}).join("");
return "<div class='mobile-day-card'><div class='inst-name'>" + inst + "</div>" + turnos + "</div>";
}).join("");
}

function renderDayTabs(){
var days = getWeekDays();
var tabsEl = document.getElementById("dayTabs");
tabsEl.innerHTML = days.map(function(d, i){
var cls = "day-tab" + (i === activeDayIndex ? " active" : "");
return "<div class='" + cls + "' data-idx='" + i + "'>" + DIAS_CORTO[d.getDay()] + " " + d.getDate() + "</div>";
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

components.html(html, height=900, scrolling=True)
