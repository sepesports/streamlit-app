# pages/editar_horarios.py
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

st.set_page_config(page_title="Gestion de Horarios", layout="wide")
sync_auth()

query_params = st.query_params
AUTH_USER = query_params.get("usuario") or query_params.get("user") or ""
AUTH_ROLE = query_params.get("rol") or query_params.get("role") or ""
AUTH_DNI = query_params.get("dni") or ""
NORMALIZED_ROLE = AUTH_ROLE.strip().lower()

if not AUTH_USER or not AUTH_ROLE:
          go("pages/admin.py")

if NORMALIZED_ROLE != "administrador":
          go("app.py")

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
--red:#d43d3d;
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
#topbar{background:#fff;border-bottom:1px solid var(--border);padding:18px 30px;display:flex;align-items:center;justify-content:space-between;}
#topbar h1{font-size:20px;margin:0;font-weight:700;}
.hamburger{display:none;font-size:20px;background:none;border:none;cursor:pointer;color:var(--ink);}
.mobile-logo{display:none;align-items:center;gap:8px;font-weight:800;letter-spacing:1px;}
.mobile-logo img{width:26px;height:26px;border-radius:6px;object-fit:contain;}
.primary-btn{background:var(--blue);color:#fff;border:none;border-radius:10px;padding:9px 16px;font-size:13px;font-weight:700;cursor:pointer;}
.primary-btn:hover{background:#1e4fb8;}
.primary-btn .lbl-short{display:none;}
#content{padding:22px 30px 90px 30px;}
.tabbar{display:flex;gap:6px;border-bottom:1px solid var(--border);margin-bottom:18px;}
.tabbtn{padding:10px 4px;margin-right:22px;background:none;border:none;font-size:13.5px;font-weight:700;color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;}
.tabbtn.active{color:var(--blue);border-bottom-color:var(--blue);}
.card{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:0;overflow:hidden;}
.info-bar{background:#eef4ff;color:#2f5fc4;font-size:12.5px;padding:12px 20px;border-top:1px solid var(--border);}
table{width:100%;border-collapse:collapse;font-size:13px;}
thead th{text-align:left;padding:12px 18px;color:var(--muted);font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;border-bottom:1px solid var(--border);}
tbody td{padding:12px 18px;border-bottom:1px solid var(--border);vertical-align:middle;}
tbody tr:last-child td{border-bottom:none;}
.pill{display:inline-block;padding:3px 10px;border-radius:20px;font-size:11.5px;font-weight:700;}
.pill.ok{background:#e6f7ee;color:#1a7f4f;}
.pill.warn{background:#fff4e0;color:#a3690a;}
.pill.off{background:#f1f2f5;color:#6b7688;}
.icon-btn{background:none;border:none;cursor:pointer;font-size:15px;padding:4px 6px;border-radius:6px;}
.icon-btn.edit{color:var(--blue);}
.icon-btn.del{color:var(--red);}
.icon-btn:hover{background:#f1f4fb;}
.empty-row td{text-align:center;color:var(--muted);padding:30px;}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(10,20,50,.45);z-index:200;align-items:center;justify-content:center;}
.modal-overlay.open{display:flex;}
.modal{background:#fff;border-radius:16px;padding:24px;width:420px;max-width:92vw;}
.modal h3{margin:0 0 16px 0;font-size:16px;}
.modal .field{margin-bottom:12px;}
.modal .field label{display:block;font-size:12px;color:var(--muted);margin-bottom:5px;font-weight:600;}
.modal .field input, .modal .field select{width:100%;padding:9px 11px;border:1px solid var(--border);border-radius:9px;font-size:13px;}
.modal .actions{display:flex;justify-content:flex-end;gap:8px;margin-top:16px;}
.btn-cancel{background:#fff;border:1px solid var(--border);border-radius:9px;padding:9px 14px;font-size:12.5px;font-weight:700;cursor:pointer;}
.msg{font-size:12.5px;margin-top:10px;padding:8px 12px;border-radius:9px;display:none;}
.msg.ok{background:#e6f7ee;color:#1a7f4f;display:block;}
.msg.err{background:#fde8e8;color:#b02a2a;display:block;}
.modal-help{font-size:12.5px;color:#5a6b8c;background:#f3f7ff;border:1px solid #dbe6ff;border-radius:9px;padding:9px 11px;margin:0 0 14px 0;line-height:1.4;}
.bloque-prev{display:none;font-size:12.5px;color:#2f5fc4;background:#eef4ff;border-radius:9px;padding:10px 12px;margin-top:4px;}
.bloque-prev.show{display:block;}
.bloque-prev .bp-t{font-weight:800;margin-bottom:5px;color:#123a8a;}
.bloque-prev .bp-row{padding:2px 0;}
.loading-row td{text-align:center;color:var(--muted);padding:24px;}
.tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;}
.panel-tools{padding:12px 14px;border-bottom:1px solid var(--border);display:flex;justify-content:flex-end;align-items:center;gap:8px;flex-wrap:wrap;}
.primary-btn.sm{padding:7px 12px;font-size:12px;white-space:nowrap;}
.sd{position:relative;flex:1 1 170px;max-width:280px;min-width:150px;}
.sd-input{width:100%;padding:8px 11px;border:1px solid var(--border);border-radius:9px;font-size:12.5px;}
.sd-list{position:absolute;z-index:60;left:0;right:0;top:calc(100% + 4px);background:#fff;border:1px solid var(--border);border-radius:10px;box-shadow:0 10px 28px rgba(10,20,50,.20);max-height:240px;overflow-y:auto;display:none;}
.sd-list.open{display:block;}
.sd-item{padding:9px 12px;font-size:13px;cursor:pointer;border-bottom:1px solid #f0f2f7;}
.sd-item:last-child{border-bottom:none;}
.sd-item:hover,.sd-item.active{background:#eef4ff;}
.sd-empty{padding:9px 12px;font-size:12px;color:var(--muted);}
.chkcol{width:38px;text-align:center;}
tbody td.chkcol input{width:17px;height:17px;cursor:pointer;}
.brow{cursor:pointer;}
.brow:hover{background:#f5f8ff;}
.caret{color:#8a96ad;font-size:10px;margin-left:4px;}
.bdetail td{background:#f7f9fc;border-bottom:1px solid var(--border);}

.modal .field.two{display:flex;gap:10px;}
.modal .field.two > div{flex:1;}
.modal .field select{width:100%;padding:9px 11px;border:1px solid var(--border);border-radius:9px;font-size:13px;background:#fff;}

@media (max-width:768px){
#sidebar{display:none;}
.hamburger{display:block;}
.mobile-logo{display:flex;}
#topbar h1{display:none;}
#topbar{padding:14px 16px;}
#topbar .primary-btn{margin-left:auto;padding:7px 11px;font-size:11.5px;white-space:nowrap;}
.primary-btn .lbl-full{display:none;}
.primary-btn .lbl-short{display:inline;}
#content{padding:14px 12px 90px 12px;}
table{font-size:12px;min-width:600px;}
thead th, tbody td{padding:9px 10px;white-space:nowrap;}
}

.mobile-drawer{display:none;position:fixed;inset:0;z-index:100;}
.mobile-drawer.open{display:block;}
.mobile-drawer .overlay{position:absolute;inset:0;background:rgba(0,0,0,.4);}
.mobile-drawer .panel{
position:absolute;left:0;top:0;bottom:0;width:250px;
background:linear-gradient(180deg,var(--navy1) 0%,var(--navy2) 60%,var(--navy3) 100%);
padding:26px 18px;color:#eaf2ff;overflow-y:auto;
}

/* ===== SYNTRA reskin: hoja azul + cajas blancas (consistente con Inicio) ===== */
html,body{background:#1B2A4A !important;}
#app{min-height:100vh;gap:14px !important;padding:14px !important;box-sizing:border-box !important;align-items:stretch !important;}
#sidebar{background:#1B2A4A !important;border:1px solid rgba(255,255,255,.16) !important;border-radius:12px !important;min-height:0 !important;}
#main{gap:14px !important;}
#topbar{background:#fff !important;border-bottom:none !important;border-radius:12px !important;box-shadow:0 4px 12px rgba(27,42,74,.08) !important;flex:0 0 auto !important;}
#content{background:#fff !important;border-radius:12px !important;box-shadow:0 4px 12px rgba(27,42,74,.08) !important;padding-bottom:22px !important;}
#chatBody{background:#fff !important;border-radius:12px !important;box-shadow:0 4px 12px rgba(27,42,74,.08) !important;overflow:hidden !important;}
@media (max-width:900px){#app{padding:10px !important;gap:10px !important;}}
@media (max-width:768px){#content{overflow-x:hidden !important;}}
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
<h1>Gesti&oacute;n de Horarios</h1>
<div class="mobile-logo"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
<button class="primary-btn" id="addBtn"><span class="lbl-full">+ Nueva Asignaci&oacute;n</span><span class="lbl-short">+ Nueva</span></button>
</div>
<div id="content">
<div class="tabbar">
<button class="tabbtn active" data-tab="bloques">Bloques</button>
<button class="tabbtn" data-tab="asignaciones">Asignaciones</button>
<button class="tabbtn" data-tab="historial">Historial</button>
</div>

<div class="card" id="panel-bloques">
<div class="panel-tools">
<div class="sd" id="sdInst"><input class="sd-input" id="filtroInst" placeholder="Filtrar por instalaci&oacute;n..." autocomplete="off"/><div class="sd-list" id="filtroInstList"></div></div>
<button class="primary-btn sm" id="btnAsignarSel" style="display:none;">Asignar seleccionados</button>
<button class="primary-btn sm" id="btnCrearBloque">+ A&ntilde;adir a un bloque</button>
</div>
<div class="tscroll"><table>
<thead><tr><th class="chkcol"></th><th>Bloque</th><th>Contenido</th></tr></thead>
<tbody id="bloquesBody"><tr class="loading-row"><td colspan="3">Cargando...</td></tr></tbody>
</table></div>
<div class="info-bar">Elige una instalaci&oacute;n para ver sus bloques. Marca uno o varios y usa <b>Asignar seleccionados</b> para dar ese turno a un socorrista en una fecha.</div>
</div>

<div class="card" id="panel-asignaciones" style="display:none;">
<div class="panel-tools"><button class="primary-btn sm" id="btnAsignar">+ Asignar a socorrista</button></div>
<div class="tscroll"><table>
<thead><tr><th>Fecha</th><th>Instalaci&oacute;n</th><th>Socorrista</th><th>Ingreso</th><th>Salida</th><th>Estado</th><th></th></tr></thead>
<tbody id="asigBody"><tr class="loading-row"><td colspan="7">Cargando...</td></tr></tbody>
</table></div>
<div class="info-bar">Turnos desde hoy en adelante. Edita o elimina cada asignaci&oacute;n.</div>
</div>

<div class="card" id="panel-historial" style="display:none;">
<div class="tscroll"><table>
<thead><tr><th>Fecha</th><th>Instalaci&oacute;n</th><th>Socorrista</th><th>Ingreso</th><th>Salida</th><th>Estado</th></tr></thead>
<tbody id="histBody"><tr class="loading-row"><td colspan="6">Cargando...</td></tr></tbody>
</table></div>
<div class="info-bar">Turnos anteriores a hoy. Solo lectura.</div>
</div>
</div>
</div>
</div>

<div class="modal-overlay" id="editModal">
<div class="modal">
<h3>Editar asignaci&oacute;n</h3>
<div class="field"><label>Socorrista</label><input id="edit_socorrista"/></div>
<div class="field"><label>Instalaci&oacute;n</label><input id="edit_instalacion"/></div>
<div class="field"><label>Ingreso</label><input id="edit_ingreso" placeholder="08:00"/></div>
<div class="field"><label>Salida</label><input id="edit_salida" placeholder="16:00"/></div>
<div class="msg" id="editMsg"></div>
<div class="actions">
<button class="btn-cancel" id="editCancelBtn">Cancelar</button>
<button class="primary-btn" id="editSaveBtn">Guardar</button>
</div>
</div>
</div>

<div class="modal-overlay" id="asigModal">
<div class="modal">
<h3>Asignar turno a un socorrista</h3>
<p class="modal-help">Crea un turno para <b>una persona</b> en una fecha concreta (no usa plantilla de bloque).</p>
<div class="field"><label>Fecha</label><input id="as_fecha" type="date"/></div>
<div class="field"><label>Socorrista</label><input id="as_socorrista" list="dlSocorristas" placeholder="Nombre del socorrista"/></div>
<div class="field"><label>Instalaci&oacute;n</label><input id="as_instalacion" list="dlInstalaciones" placeholder="Instalaci&oacute;n"/></div>
<div class="field"><label>Ingreso</label><input id="as_ingreso" placeholder="08:00"/></div>
<div class="field"><label>Salida</label><input id="as_salida" placeholder="16:00"/></div>
<div class="msg" id="asMsg"></div>
<div class="actions">
<button class="btn-cancel" id="asCancelBtn">Cancelar</button>
<button class="primary-btn" id="asSaveBtn">Asignar</button>
</div>
</div>
</div>

<div class="modal-overlay" id="crearBloqueModal">
<div class="modal">
<h3>A&ntilde;adir a un bloque</h3>
<p class="modal-help">Un bloque es una plantilla que se repite un <b>d&iacute;a de la semana</b>. A&ntilde;ade una l&iacute;nea (instalaci&oacute;n, d&iacute;a, horario y un socorrista); repite para sumar m&aacute;s socorristas al mismo bloque.</p>
<div class="field"><label>Bloque</label><input id="cb_bloque" placeholder="N&uacute;mero o nombre del bloque"/></div>
<div class="field two"><div><label>Fecha</label><input id="cb_fecha" type="date"/></div><div><label>Hasta (opcional)</label><input id="cb_fecha_fin" type="date"/></div></div>
<div class="hint" style="margin:-6px 0 12px 2px;">Elige un d&iacute;a o un rango de fechas. Con rango, el bloque tendr&aacute; una l&iacute;nea por fecha.</div>
<div class="field"><label>Socorrista</label><div class="sd"><input class="sd-input" id="cb_socorrista" placeholder="Buscar socorrista..." autocomplete="off"/><div class="sd-list" id="cb_socorrista_list"></div></div></div>
<div class="field"><label>Instalaci&oacute;n</label><div class="sd"><input class="sd-input" id="cb_instalacion" placeholder="Buscar instalaci&oacute;n..." autocomplete="off"/><div class="sd-list" id="cb_instalacion_list"></div></div></div>
<div class="field two"><div><label>Ingreso</label><input id="cb_ingreso" placeholder="08:00"/></div><div><label>Salida</label><input id="cb_salida" placeholder="16:00"/></div></div>
<div class="msg" id="cbMsg"></div>
<div class="actions">
<button class="btn-cancel" id="cbCancelBtn">Cancelar</button>
<button class="primary-btn" id="cbSaveBtn">Guardar</button>
</div>
</div>
</div>

<div class="modal-overlay" id="asignarSelModal">
<div class="modal">
<h3>Asignar bloque(s) a un socorrista</h3>
<p class="modal-help">Se crear&aacute;n turnos para el socorrista elegido en la fecha indicada, copiando instalaci&oacute;n y horario de los bloques marcados.</p>
<div id="aselResumen" class="bloque-prev show"></div>
<div class="field"><label>Fecha</label><input id="asel_fecha" type="date"/></div>
<div class="field"><label>Socorrista</label><div class="sd"><input class="sd-input" id="asel_socorrista" placeholder="Buscar socorrista..." autocomplete="off"/><div class="sd-list" id="asel_socorrista_list"></div></div></div>
<div class="msg" id="aselMsg"></div>
<div class="actions">
<button class="btn-cancel" id="aselCancelBtn">Cancelar</button>
<button class="primary-btn" id="aselSaveBtn">Asignar</button>
</div>
</div>
</div>

<datalist id="dlSocorristas"></datalist>
<datalist id="dlInstalaciones"></datalist>
<datalist id="dlDias"><option value="lunes"></option><option value="martes"></option><option value="mi&eacute;rcoles"></option><option value="jueves"></option><option value="viernes"></option><option value="s&aacute;bado"></option><option value="domingo"></option></datalist>

<div class="modal-overlay" id="addModal">
<div class="modal">
<h3>Nueva asignaci&oacute;n desde bloque</h3>
<p class="modal-help">Un <b>bloque</b> es una plantilla de turnos ya creada en la hoja de horarios (instalaci&oacute;n, d&iacute;a, horario y socorristas). Elige una fecha y un bloque: se generar&aacute;n esos turnos para esa fecha.</p>
<div class="field"><label>Fecha</label><input id="add_fecha" type="date"/></div>
<div class="field"><label>Bloque</label>
<select id="add_bloque"><option value="">Selecciona...</option></select>
</div>
<div id="bloquePrev" class="bloque-prev"></div>
<div class="msg" id="addMsg"></div>
<div class="actions">
<button class="btn-cancel" id="addCancelBtn">Cancelar</button>
<button class="primary-btn" id="addSaveBtn">Agregar</button>
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
{label:"Horarios", icon:"&#128197;", go:"/calendario"},
{label:"Incidencias y Comunicados", icon:"&#128172;", go:"/chat_interfaz"},
{sep:true},
{label:"Registro", icon:"&#128100;+", go:"/altas_registro", badge:"Solo admin"},
{label:"Gesti&oacute;n de Horarios", icon:"&#9881;", go:"/editar_horarios", active:true, badge:"Solo admin"}
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

var tabbtns = document.querySelectorAll(".tabbtn");
tabbtns.forEach(function(btn){
btn.addEventListener("click", function(){
tabbtns.forEach(function(b){ b.classList.remove("active"); });
btn.classList.add("active");
["bloques","asignaciones","historial"].forEach(function(name){
document.getElementById("panel-" + name).style.display = (name === btn.getAttribute("data-tab")) ? "" : "none";
});
});
});

function todayStr(){
var d = new Date();
var m = String(d.getMonth()+1).padStart(2,"0");
var day = String(d.getDate()).padStart(2,"0");
return d.getFullYear() + "-" + m + "-" + day;
}

function parseFecha(str){
str = (str || "").trim();
if (!str) return null;
var parts = str.split("/");
if (parts.length === 3){
return parts[2] + "-" + parts[1].padStart(2,"0") + "-" + parts[0].padStart(2,"0");
}
return str;
}

function estadoPill(estado){
var e = (estado || "").trim().toLowerCase();
if (e === "programado") return '<span class="pill ok">Programado</span>';
if (e === "disponible") return '<span class="pill warn">Disponible</span>';
if (!e) return '<span class="pill off">-</span>';
return '<span class="pill off">' + estado + '</span>';
}

var bloqueDetalle = {};
function llenarDatalist(id, valores){
var dl=document.getElementById(id); if(!dl) return;
var existentes={}; [].slice.call(dl.querySelectorAll("option")).forEach(function(o){ existentes[o.value]=1; });
valores.forEach(function(v){ if(v && !existentes[v]){ var o=document.createElement("option"); o.value=v; dl.appendChild(o); existentes[v]=1; } });
}
fetch(API_BASE + "/api/chat/users").then(function(r){ return r.json(); }).then(function(d){
var us = Array.isArray(d) ? d : ((d && d.users) || []);
llenarDatalist("dlSocorristas", us.map(function(u){ return (u.nombre || u.alias || "").trim(); }).filter(Boolean).sort());
}).catch(function(){});
var gruposBloque = {};   // bloque -> {bloque, lineas:[{inst,dia,ingresos,salida,socorristas}], insts:{}}
var sugSocorristas = [];
var sugInstalaciones = [];
var filtroInstSel = "";
var bloquesAbiertos = {};

function esc(t){ return String(t==null?"":t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;"); }

function renderBloquesTabla(){
var tbody = document.getElementById("bloquesBody");
var keys = Object.keys(gruposBloque);
if (!keys.length){ tbody.innerHTML = '<tr class="empty-row"><td colspan="3">Sin datos de bloques.</td></tr>'; document.getElementById("btnAsignarSel").style.display="none"; return; }
var filtro = (filtroInstSel || "").toLowerCase();
var lista = keys.map(function(k){ return gruposBloque[k]; });
if (filtro){ lista = lista.filter(function(g){ return Object.keys(g.insts).some(function(i){ return i.toLowerCase().indexOf(filtro)!==-1; }); }); }
lista.sort(function(a,b){ return String(a.bloque).localeCompare(String(b.bloque), undefined, {numeric:true}); });
if (!lista.length){ tbody.innerHTML = '<tr class="empty-row"><td colspan="3">No hay bloques para esa instalaci&oacute;n.</td></tr>'; document.getElementById("btnAsignarSel").style.display="none"; return; }
var html = "";
lista.forEach(function(g){
var insts = Object.keys(g.insts);
var abierto = !!bloquesAbiertos[g.bloque];
var resumen = esc(insts.join(", ") || "-") + ' <span style="color:#6b7688;">&middot; ' + g.lineas.length + " turno" + (g.lineas.length!==1?"s":"") + '</span>';
html += '<tr class="brow" data-b="'+esc(g.bloque)+'">' +
'<td class="chkcol"><input type="checkbox" class="bchk" data-b="'+esc(g.bloque)+'"/></td>' +
'<td><b>Bloque '+esc(g.bloque)+'</b> <span class="caret">'+(abierto?"&#9650;":"&#9660;")+'</span></td>' +
'<td>'+resumen+'</td>' +
'</tr>';
if (abierto){
g.lineas.forEach(function(l){
var horas=l.ingresos.slice().sort();
var rango=horas.length ? (horas[0]+(l.salida?" - "+l.salida:"")) : (l.salida||"-");
html += '<tr class="bdetail"><td></td><td colspan="2" style="font-size:12px;color:#40506e;">&#8226; '+esc(l.inst)+' &middot; '+esc(l.dia)+' &middot; '+esc(rango)+(l.socorristas.length?(' &middot; '+esc(l.socorristas.join(", "))):"")+'</td></tr>';
});
}
});
tbody.innerHTML = html;
tbody.querySelectorAll(".brow").forEach(function(tr){
tr.addEventListener("click", function(e){ if(e.target.classList.contains("bchk")) return; var b=tr.getAttribute("data-b"); bloquesAbiertos[b]=!bloquesAbiertos[b]; renderBloquesTabla(); });
});
tbody.querySelectorAll(".bchk").forEach(function(c){ c.addEventListener("click", function(e){ e.stopPropagation(); }); c.addEventListener("change", actualizarSeleccion); });
actualizarSeleccion();
}

function actualizarSeleccion(){
var n = document.querySelectorAll("#bloquesBody .bchk:checked").length;
var b = document.getElementById("btnAsignarSel");
b.style.display = n ? "" : "none";
b.textContent = n>1 ? ("Asignar seleccionados ("+n+")") : "Asignar seleccionado";
}

function loadBloques(){
fetch(API_BASE + "/api/bloques")
.then(function(r){ return r.json(); })
.then(function(d){
var tbody = document.getElementById("bloquesBody");
if (!d || !d.ok || !d.rows || !d.rows.length){
tbody.innerHTML = '<tr class="empty-row"><td colspan="3">Sin datos de bloques.</td></tr>';
return;
}
gruposBloque = {};
d.rows.forEach(function(r){
var inst = (r["Instalacion"] || "").trim();
var bloque = (r["bloque"] || "").trim();
var dia = (r["Dia"] || "").trim();
var ingreso = (r["Ingreso"] || "").trim();
var salida = (r["Salida"] || "").trim();
var soc = (r["Socorrista"] || "").trim();
if (!bloque) return;
if (!gruposBloque[bloque]) gruposBloque[bloque] = {bloque:bloque, lineas:[], insts:{}, _idx:{}};
var g = gruposBloque[bloque];
if (inst) g.insts[inst]=1;
var lk = inst+"|"+dia+"|"+ingreso+"|"+salida;
if (!g._idx[lk]){ g._idx[lk]={inst:inst, dia:dia, ingresos:[], salida:salida, socorristas:[]}; g.lineas.push(g._idx[lk]); }
var l=g._idx[lk];
if (ingreso) l.ingresos.push(ingreso);
if (salida && !l.salida) l.salida=salida;
if (soc && l.socorristas.indexOf(soc)===-1) l.socorristas.push(soc);
});
// preview para "Nueva desde bloque"
bloqueDetalle = {};
Object.keys(gruposBloque).forEach(function(bn){
var g=gruposBloque[bn];
bloqueDetalle[bn]=g.lineas.map(function(l){ var h=l.ingresos.slice().sort(); return {inst:l.inst, dia:l.dia, rango:(h.length?(h[0]+" - "+(l.salida||h[h.length-1])):(l.salida||"-")), count:l.socorristas.length}; });
});
// sugerencias para buscadores
var setS={}, setI={};
d.rows.forEach(function(r){ var sc=(r["Socorrista"]||"").trim(); var ins=(r["Instalacion"]||"").trim(); if(sc) setS[sc]=1; if(ins) setI[ins]=1; });
Object.keys(setS).forEach(function(x){ if(sugSocorristas.indexOf(x)===-1) sugSocorristas.push(x); });
sugSocorristas.sort();
sugInstalaciones = Object.keys(setI).sort();
llenarDatalist("dlSocorristas", sugSocorristas);
llenarDatalist("dlInstalaciones", sugInstalaciones);
// selector "Nueva desde bloque"
var sel = document.getElementById("add_bloque");
if (sel){
sel.innerHTML = '<option value="">Selecciona...</option>';
var bset={};
d.rows.forEach(function(r){ bset[(r["bloque"]||"").trim()]=true; });
Object.keys(bset).sort().forEach(function(b){ if(!b) return; var o=document.createElement("option"); o.value=b; o.textContent="Bloque "+b; sel.appendChild(o); });
}
renderBloquesTabla();
})
.catch(function(){
document.getElementById("bloquesBody").innerHTML = '<tr class="empty-row"><td colspan="5">Error al cargar bloques.</td></tr>';
});
}
loadBloques();

function diaSemana(iso){
try{
var pr=(iso||"").split("-"); if(pr.length!==3) return "";
var d=new Date(parseInt(pr[0],10), parseInt(pr[1],10)-1, parseInt(pr[2],10));
var dias=["domingo","lunes","martes","mi\u00e9rcoles","jueves","viernes","s\u00e1bado"];
return dias[d.getDay()] || "";
}catch(e){ return ""; }
}

var mallasCache = [];

function renderMallas(){
var today = todayStr();
var futuras = [];
var pasadas = [];
mallasCache.forEach(function(r){
var fechaISO = parseFecha(r["Fecha"]);
var inst = (r["Instalacion"] || "").trim();
if (!inst || inst.toLowerCase() === "descanso") return;
if (fechaISO && fechaISO >= today) futuras.push(r);
else pasadas.push(r);
});
futuras.sort(function(a,b){ return (parseFecha(a["Fecha"])||"").localeCompare(parseFecha(b["Fecha"])||""); });
pasadas.sort(function(a,b){ return (parseFecha(b["Fecha"])||"").localeCompare(parseFecha(a["Fecha"])||""); });

var asigBody = document.getElementById("asigBody");
if (!futuras.length){
asigBody.innerHTML = '<tr class="empty-row"><td colspan="7">No hay asignaciones futuras.</td></tr>';
} else {
asigBody.innerHTML = futuras.map(function(r){
var llave = (r["llave"] || "").replace(/"/g, "&quot;");
return "<tr>" +
"<td>" + (r["Fecha"]||"") + "</td>" +
"<td>" + (r["Instalacion"]||"") + "</td>" +
"<td>" + (r["Socorrista"]||"") + "</td>" +
"<td>" + (r["Ingreso"]||"") + "</td>" +
"<td>" + (r["Salida"]||"") + "</td>" +
"<td>" + estadoPill(r["estado"]) + "</td>" +
'<td><button class="icon-btn edit" data-llave="' + llave + '" data-action="edit">&#9998;</button>' +
'<button class="icon-btn del" data-llave="' + llave + '" data-action="del">&#128465;</button></td>' +
"</tr>";
}).join("");
}

var histBody = document.getElementById("histBody");
if (!pasadas.length){
histBody.innerHTML = '<tr class="empty-row"><td colspan="6">Sin historial.</td></tr>';
} else {
histBody.innerHTML = pasadas.slice(0, 200).map(function(r){
return "<tr>" +
"<td>" + (r["Fecha"]||"") + "</td>" +
"<td>" + (r["Instalacion"]||"") + "</td>" +
"<td>" + (r["Socorrista"]||"") + "</td>" +
"<td>" + (r["Ingreso"]||"") + "</td>" +
"<td>" + (r["Salida"]||"") + "</td>" +
"<td>" + estadoPill(r["estado"]) + "</td>" +
"</tr>";
}).join("");
}

asigBody.querySelectorAll(".icon-btn").forEach(function(btn){
btn.addEventListener("click", function(){
var llave = btn.getAttribute("data-llave");
var action = btn.getAttribute("data-action");
if (action === "edit") openEditModal(llave);
else if (action === "del") deleteAsignacion(llave);
});
});
}

function loadMallas(){
fetch(API_BASE + "/api/mallas")
.then(function(r){ return r.json(); })
.then(function(d){
mallasCache = (d && d.ok && d.rows) ? d.rows : [];
renderMallas();
})
.catch(function(){
document.getElementById("asigBody").innerHTML = '<tr class="empty-row"><td colspan="7">Error al cargar.</td></tr>';
document.getElementById("histBody").innerHTML = '<tr class="empty-row"><td colspan="6">Error al cargar.</td></tr>';
});
}
loadMallas();

var editModal = document.getElementById("editModal");
var currentLlave = null;

function openEditModal(llave){
var row = mallasCache.find(function(r){ return r["llave"] === llave; });
if (!row) return;
currentLlave = llave;
document.getElementById("edit_socorrista").value = row["Socorrista"] || "";
document.getElementById("edit_instalacion").value = row["Instalacion"] || "";
document.getElementById("edit_ingreso").value = row["Ingreso"] || "";
document.getElementById("edit_salida").value = row["Salida"] || "";
document.getElementById("editMsg").className = "msg";
document.getElementById("editMsg").textContent = "";
editModal.classList.add("open");
}
document.getElementById("editCancelBtn").addEventListener("click", function(){ editModal.classList.remove("open"); });

document.getElementById("editSaveBtn").addEventListener("click", function(){
var payload = {
llave: currentLlave,
Socorrista: document.getElementById("edit_socorrista").value.trim(),
Instalacion: document.getElementById("edit_instalacion").value.trim(),
Ingreso: document.getElementById("edit_ingreso").value.trim(),
Salida: document.getElementById("edit_salida").value.trim()
};
var msgEl = document.getElementById("editMsg");
fetch(API_BASE + "/api/horarios/editar", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify(payload)
})
.then(function(r){ return r.json(); })
.then(function(d){
if (d && d.ok){
msgEl.className = "msg ok"; msgEl.textContent = "Actualizado.";
setTimeout(function(){ editModal.classList.remove("open"); loadMallas(); }, 700);
} else {
msgEl.className = "msg err"; msgEl.textContent = (d && d.error) || "Error al actualizar.";
}
})
.catch(function(){ msgEl.className = "msg err"; msgEl.textContent = "Error de conexi&oacute;n."; });
});

function deleteAsignacion(llave){
if (!window.confirm("&#191;Eliminar esta asignaci&oacute;n?")) return;
fetch(API_BASE + "/api/horarios/eliminar", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({llave: llave})
})
.then(function(r){ return r.json(); })
.then(function(d){ if (d && d.ok) loadMallas(); else alert((d && d.error) || "Error al eliminar."); })
.catch(function(){ alert("Error de conexi&oacute;n."); });
}

var addModal = document.getElementById("addModal");
document.getElementById("addBtn").addEventListener("click", function(){
document.getElementById("add_fecha").value = "";
document.getElementById("add_bloque").value = "";
document.getElementById("addMsg").className = "msg";
document.getElementById("addMsg").textContent = "";
var prev0 = document.getElementById("bloquePrev"); prev0.className = "bloque-prev"; prev0.innerHTML = "";
addModal.classList.add("open");
});
document.getElementById("add_bloque").addEventListener("change", function(){
var prev = document.getElementById("bloquePrev");
var det = bloqueDetalle[this.value] || [];
if (!this.value || !det.length){ prev.className = "bloque-prev"; prev.innerHTML = ""; return; }
var html = '<div class="bp-t">Este bloque genera:</div>';
det.forEach(function(x){
html += '<div class="bp-row">&#8226; ' + x.inst + ' &middot; ' + x.dia + ' &middot; ' + x.rango + ' &middot; ' + x.count + ' socorrista(s)</div>';
});
prev.innerHTML = html; prev.className = "bloque-prev show";
});
document.getElementById("addCancelBtn").addEventListener("click", function(){ addModal.classList.remove("open"); });

document.getElementById("addSaveBtn").addEventListener("click", function(){
var fechaVal = document.getElementById("add_fecha").value;
var bloqueVal = document.getElementById("add_bloque").value;
var msgEl = document.getElementById("addMsg");
if (!fechaVal || !bloqueVal){
msgEl.className = "msg err"; msgEl.textContent = "Selecciona fecha y bloque.";
return;
}
var parts = fechaVal.split("-");
var fechaDMY = parts[2] + "/" + parts[1] + "/" + parts[0];
fetch(API_BASE + "/api/horarios/agregar", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({fecha: fechaDMY, bloque: bloqueVal})
})
.then(function(r){ return r.json(); })
.then(function(d){
if (d && d.ok){
msgEl.className = "msg ok"; msgEl.textContent = d.mensaje || "Agregado.";
setTimeout(function(){ addModal.classList.remove("open"); loadMallas(); }, 1600);
} else {
msgEl.className = "msg err"; msgEl.textContent = (d && d.error) || "Error al agregar.";
}
})
.catch(function(){ msgEl.className = "msg err"; msgEl.textContent = "Error de conexi&oacute;n."; });
});

/* ---- Asignar turno a un socorrista ---- */
var asigModal = document.getElementById("asigModal");
var btnAsignar = document.getElementById("btnAsignar");
if (btnAsignar) btnAsignar.addEventListener("click", function(){
["as_fecha","as_socorrista","as_instalacion","as_ingreso","as_salida"].forEach(function(id){ document.getElementById(id).value=""; });
var mm=document.getElementById("asMsg"); mm.className="msg"; mm.textContent="";
asigModal.classList.add("open");
});
document.getElementById("asCancelBtn").addEventListener("click", function(){ asigModal.classList.remove("open"); });
document.getElementById("asSaveBtn").addEventListener("click", function(){
var msgEl=document.getElementById("asMsg");
var fechaVal=document.getElementById("as_fecha").value;
var soc=document.getElementById("as_socorrista").value.trim();
var ins=document.getElementById("as_instalacion").value.trim();
var ing=document.getElementById("as_ingreso").value.trim();
var sal=document.getElementById("as_salida").value.trim();
if(!fechaVal || !soc || !ins){ msgEl.className="msg err"; msgEl.textContent="Fecha, socorrista e instalaci\u00f3n son obligatorios."; return; }
var pr=fechaVal.split("-"); var fechaDMY=pr[2]+"/"+pr[1]+"/"+pr[0];
var dia=diaSemana(fechaVal);
var btn=this; btn.disabled=true; btn.textContent="Guardando...";
fetch(API_BASE + "/api/horarios/asignar", {
method:"POST", headers:{"Content-Type":"application/json"},
body: JSON.stringify({fecha:fechaDMY, dia:dia, socorrista:soc, instalacion:ins, ingreso:ing, salida:sal})
})
.then(function(r){ return r.json(); })
.then(function(d){
btn.disabled=false; btn.textContent="Asignar";
if(d && d.ok){ msgEl.className="msg ok"; msgEl.textContent=d.mensaje || "Turno asignado."; setTimeout(function(){ asigModal.classList.remove("open"); loadMallas(); }, 1600); }
else { msgEl.className="msg err"; msgEl.textContent=(d && d.error) || "Error al asignar."; }
})
.catch(function(){ btn.disabled=false; btn.textContent="Asignar"; msgEl.className="msg err"; msgEl.textContent="Error de conexi\u00f3n."; });
});

/* ---- A\u00f1adir a un bloque ---- */
var cbModal = document.getElementById("crearBloqueModal");
var btnCrearBloque = document.getElementById("btnCrearBloque");
if (btnCrearBloque) btnCrearBloque.addEventListener("click", function(){
["cb_bloque","cb_fecha","cb_fecha_fin","cb_socorrista","cb_instalacion","cb_ingreso","cb_salida"].forEach(function(id){ var e=document.getElementById(id); if(e) e.value=""; });
var mm=document.getElementById("cbMsg"); mm.className="msg"; mm.textContent="";
cbModal.classList.add("open");
});
document.getElementById("cbCancelBtn").addEventListener("click", function(){ cbModal.classList.remove("open"); });
function fechasRango(iso1, iso2){
if(!iso1) return [];
var a=iso1, b=iso2||iso1;
if(b<a){ var t=a; a=b; b=t; }
var out=[]; var d=new Date(a+"T00:00:00"); var fin=new Date(b+"T00:00:00"); var guard=0;
while(d<=fin && guard<400){ var y=d.getFullYear(), m=("0"+(d.getMonth()+1)).slice(-2), dd=("0"+d.getDate()).slice(-2); out.push(dd+"/"+m+"/"+y); d.setDate(d.getDate()+1); guard++; }
return out;
}
document.getElementById("cbSaveBtn").addEventListener("click", function(){
var msgEl=document.getElementById("cbMsg");
var bl=document.getElementById("cb_bloque").value.trim();
var f1=document.getElementById("cb_fecha").value;
var f2=document.getElementById("cb_fecha_fin").value;
var soc=document.getElementById("cb_socorrista").value.trim();
var ins=document.getElementById("cb_instalacion").value.trim();
var ing=document.getElementById("cb_ingreso").value.trim();
var sal=document.getElementById("cb_salida").value.trim();
if(!bl || !soc || !ins || !f1){ msgEl.className="msg err"; msgEl.textContent="Bloque, fecha, socorrista e instalaci\u00f3n son obligatorios."; return; }
var fechas=fechasRango(f1,f2);
var btn=this; btn.disabled=true; btn.textContent="Guardando...";
var pend=fechas.map(function(fe){
return fetch(API_BASE + "/api/bloques/crear", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({bloque:bl, dia:fe, socorrista:soc, instalacion:ins, ingreso:ing, salida:sal}) }).then(function(r){ return r.json(); });
});
Promise.all(pend).then(function(rs){
btn.disabled=false; btn.textContent="Guardar";
var ok=rs.filter(function(x){ return x && x.ok; }).length;
if(ok){ msgEl.className="msg ok"; msgEl.textContent="Bloque actualizado ("+ok+" fecha"+(ok!==1?"s":"")+")."; setTimeout(function(){ cbModal.classList.remove("open"); loadBloques(); }, 1600); }
else { msgEl.className="msg err"; msgEl.textContent=(rs[0] && rs[0].error) || "Error al guardar."; }
}).catch(function(){ btn.disabled=false; btn.textContent="Guardar"; msgEl.className="msg err"; msgEl.textContent="Error de conexi\u00f3n."; });
});

/* ---- Buscador desplegable reutilizable ---- */
function attachSearch(inputId, listId, getOptions, onPick){
var inp=document.getElementById(inputId), lst=document.getElementById(listId);
if(!inp || !lst) return;
function pintar(){
var q=(inp.value||"").toLowerCase();
var ops=getOptions().filter(function(v){ return v.toLowerCase().indexOf(q)!==-1; }).slice(0,50);
if(!ops.length){ lst.innerHTML='<div class="sd-empty">Sin coincidencias</div>'; }
else { lst.innerHTML=ops.map(function(v){ return '<div class="sd-item" data-v="'+esc(v)+'">'+esc(v)+'</div>'; }).join(""); }
lst.querySelectorAll(".sd-item").forEach(function(it){ it.addEventListener("mousedown", function(e){ e.preventDefault(); inp.value=it.getAttribute("data-v"); lst.classList.remove("open"); if(onPick) onPick(inp.value); }); });
lst.classList.add("open");
}
inp.addEventListener("focus", pintar);
inp.addEventListener("input", function(){ pintar(); if(onPick) onPick(inp.value); });
document.addEventListener("click", function(e){ if(e.target!==inp && !lst.contains(e.target)) lst.classList.remove("open"); });
}

attachSearch("cb_socorrista","cb_socorrista_list", function(){ return sugSocorristas; });
attachSearch("cb_instalacion","cb_instalacion_list", function(){ return sugInstalaciones; });
attachSearch("filtroInst","filtroInstList", function(){ return sugInstalaciones; }, function(v){ filtroInstSel=v; renderBloquesTabla(); });
attachSearch("asel_socorrista","asel_socorrista_list", function(){ return sugSocorristas; });

/* ---- Asignar bloque(s) seleccionados a un socorrista ---- */
var aselModal=document.getElementById("asignarSelModal");
var btnAsignarSel=document.getElementById("btnAsignarSel");
if(btnAsignarSel) btnAsignarSel.addEventListener("click", function(){
var marcados=[].slice.call(document.querySelectorAll("#bloquesBody .bchk:checked")).map(function(c){ return gruposBloque[c.getAttribute("data-b")]; }).filter(Boolean);
if(!marcados.length) return;
var res=document.getElementById("aselResumen");
var lineas=[]; marcados.forEach(function(g){ g.lineas.forEach(function(l){ var h=l.ingresos.slice().sort(); lineas.push('<div class="bp-row">&#8226; Bloque '+esc(g.bloque)+' &middot; '+esc(l.inst)+' &middot; '+(h[0]||"")+(l.salida?(" - "+esc(l.salida)):"")+'</div>'); }); });
res.innerHTML='<div class="bp-t">Se asignar&aacute;n '+lineas.length+' turno(s):</div>'+lineas.join("");
document.getElementById("asel_fecha").value="";
document.getElementById("asel_socorrista").value="";
var mm=document.getElementById("aselMsg"); mm.className="msg"; mm.textContent="";
aselModal.classList.add("open");
});
document.getElementById("aselCancelBtn").addEventListener("click", function(){ aselModal.classList.remove("open"); });
document.getElementById("aselSaveBtn").addEventListener("click", function(){
var msgEl=document.getElementById("aselMsg");
var fechaVal=document.getElementById("asel_fecha").value;
var soc=document.getElementById("asel_socorrista").value.trim();
if(!fechaVal || !soc){ msgEl.className="msg err"; msgEl.textContent="Elige fecha y socorrista."; return; }
var marcados=[].slice.call(document.querySelectorAll("#bloquesBody .bchk:checked")).map(function(c){ return gruposBloque[c.getAttribute("data-b")]; }).filter(Boolean);
if(!marcados.length){ msgEl.className="msg err"; msgEl.textContent="No hay bloques seleccionados."; return; }
var pr=fechaVal.split("-"); var fechaDMY=pr[2]+"/"+pr[1]+"/"+pr[0]; var dia=diaSemana(fechaVal);
var btn=this; btn.disabled=true; btn.textContent="Asignando...";
var pend=[];
marcados.forEach(function(g){ g.lineas.forEach(function(l){ var horas=l.ingresos.slice().sort(); var ing=horas[0]||"";
pend.push(fetch(API_BASE + "/api/horarios/asignar", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({fecha:fechaDMY, dia:dia, socorrista:soc, instalacion:l.inst, ingreso:ing, salida:l.salida||""}) }).then(function(r){ return r.json(); }));
}); });
Promise.all(pend).then(function(rs){
btn.disabled=false; btn.textContent="Asignar";
var ok=rs.filter(function(x){ return x && x.ok; }).length;
if(ok){ msgEl.className="msg ok"; msgEl.textContent="Se asignaron "+ok+" turno(s)."; setTimeout(function(){ aselModal.classList.remove("open"); }, 1200); }
else { msgEl.className="msg err"; msgEl.textContent="No se pudo asignar."; }
}).catch(function(){ btn.disabled=false; btn.textContent="Asignar"; msgEl.className="msg err"; msgEl.textContent="Error de conexi\u00f3n."; });
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
)

html = html.replace("__SYNTRA_NAV__", NAV_JS)

components.html(html, height=1000, scrolling=True)
