# pages/perfiles.py
import json
import streamlit as st
import streamlit.components.v1 as components
import importlib
import syntra_core

# Recarga el modulo comun: el servidor puede quedarse con una version vieja en memoria
importlib.reload(syntra_core)
from syntra_core import sync_auth, go, shell_css, NAV_JS

# Logo oficial de SYNTRA incrustado (no depende de servidores externos)
LOGO_DATA_URI = syntra_core.LOGO_DATA_URI

st.set_page_config(page_title="Perfiles", layout="wide")
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
.perf-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:14px;}
.perf-hint{font-size:12px;color:var(--muted);}
.perf-list{display:flex;flex-direction:column;gap:12px;}
.pcard{background:#fff;border:1px solid var(--border);border-radius:16px;box-shadow:0 4px 12px rgba(27,42,74,.06);overflow:hidden;}
.pcard-main{display:flex;align-items:center;gap:14px;padding:14px 16px;cursor:pointer;}
.pcard-photo{width:64px;height:64px;border-radius:14px;background:var(--navy2);color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;overflow:hidden;flex:0 0 64px;}
.pcard-photo img{width:100%;height:100%;object-fit:cover;display:block;cursor:zoom-in;}
.pcard-info{flex:1;min-width:0;}
.pcard-name{font-size:15.5px;font-weight:800;color:var(--ink);}
.pcard-sub{font-size:12.5px;color:var(--muted);margin-top:2px;}
.pcard-rate{flex:0 0 auto;text-align:center;}
.rate-badge{display:inline-block;font-size:18px;font-weight:800;padding:6px 12px;border-radius:12px;}
.rate-badge.hi{background:#e6f7ee;color:#1a7f4f;}
.rate-badge.mid{background:#fff4e0;color:#a3690a;}
.rate-badge.low{background:#fde8e8;color:#b02a2a;}
.rate-badge.none{background:#f1f2f5;color:#6b7688;font-size:11.5px;font-weight:700;padding:8px 10px;}
.pcard-det{display:none;padding:2px 16px 16px 16px;border-top:1px solid var(--border);}
.pcard.open .pcard-det{display:block;}
.det-row{font-size:13px;color:#40506e;padding:7px 0;border-bottom:1px solid #f2f4f8;}
.det-row b{color:var(--ink);}
.crit{display:flex;align-items:center;justify-content:space-between;padding:6px 0;font-size:12.5px;color:#40506e;}
.crit .bar{flex:1;height:8px;background:#eef1f6;border-radius:6px;margin:0 10px;overflow:hidden;}
.crit .bar > i{display:block;height:100%;background:var(--blue);}
.det-actions{margin-top:12px;display:flex;justify-content:flex-end;}
.stars{display:flex;gap:6px;}
.stars .st{font-size:24px;color:#d4d9e3;cursor:pointer;line-height:1;}
.stars .st.on{color:#f2b01e;}
.crit-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;gap:10px;}
.crit-row .cl{font-size:13px;font-weight:600;}
#imgViewer{position:fixed;inset:0;background:rgba(2,7,28,.85);z-index:10000;display:none;align-items:center;justify-content:center;padding:16px;}
#imgViewer.open{display:flex;}
#imgViewer img{width:min(80vw,360px);height:auto;border-radius:18px;box-shadow:0 20px 60px rgba(0,0,0,.5);}
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
<h1>Perfiles</h1>
<div class="mobile-logo"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
</div>
<div id="content">
<div class="perf-head">
<div class="sd" id="sdBuscar" style="max-width:320px;"><input class="sd-input" id="buscarPerf" placeholder="Buscar socorrista..." autocomplete="off"/></div>
<div class="perf-hint">Toca una tarjeta para ver detalles. Toca la foto para ampliarla.</div>
</div>
<div id="perfList" class="perf-list"><div class="empty-note" style="padding:24px;color:var(--muted);">Cargando...</div></div>
</div>
</div>
</div>

<div class="modal-overlay" id="calModal">
<div class="modal">
<h3 id="calTitle">Calificar</h3>
<p class="modal-help">Punt&uacute;a cada criterio de 0 a 5 estrellas. El porcentaje se calcula solo.</p>
<div id="calCrit"></div>
<div class="field"><label>Comentario</label><textarea id="cal_comentario" rows="3" style="width:100%;padding:9px 11px;border:1px solid var(--border);border-radius:9px;font-size:13px;resize:vertical;"></textarea></div>
<div class="msg" id="calMsg"></div>
<div class="actions"><button class="btn-cancel" id="calCancel">Cancelar</button><button class="primary-btn" id="calSave">Guardar</button></div>
</div>
</div>
<div id="imgViewer"><img id="imgViewerImg" alt=""/></div>

<script>
__SYNTRA_NAV__
(function(){
var API_BASE = __API_BASE__;
var AUTH_USER = __AUTH_USER__;
var AUTH_ROLE = __AUTH_ROLE__;
var AUTH_DNI = __AUTH_DNI__;
var ES_ADMIN = String(AUTH_ROLE||"").trim().toLowerCase() === "administrador";

function qs(){
var p = new URLSearchParams();
p.set("auth","ok"); p.set("usuario",AUTH_USER); p.set("rol",AUTH_ROLE); p.set("dni",AUTH_DNI);
return "?" + p.toString();
}
function goToPage(path){ syntraGoTo(path, function(){ window.open(path + qs(), "_blank"); }); }

var NAV_ITEMS = [
{label:"Inicio", icon:"&#8962;", go:"/"},
{label:"Horarios", icon:"&#128197;", go:"/calendario"},
{label:"Incidencias y Comunicados", icon:"&#128172;", go:"/chat_interfaz"},
{sep:true},
{label:"Registro", icon:"&#128100;+", go:"/altas_registro", badge:"Solo admin"},
{label:"Gesti&oacute;n de Horarios", icon:"&#9881;", go:"/editar_horarios", badge:"Solo admin"},
{label:"Perfiles", icon:"&#11088;", go:"/perfiles", active:true, badge:"Solo admin"}
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
var hb = document.getElementById("hamburgerBtn");
if (hb) hb.addEventListener("click", function(){ drawer.classList.add("open"); });
var dov = document.getElementById("drawerOverlay");
if (dov) dov.addEventListener("click", function(){ drawer.classList.remove("open"); });

function esc(t){ return String(t==null?"":t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;"); }
function initials(n){ n=(n||"").trim(); if(!n) return "?"; var p=n.split(/\s+/); return ((p[0]||"")[0]||"" ).toUpperCase() + ((p[1]||"")[0]||"").toUpperCase(); }

var CRITS = [["puntualidad","Puntualidad"],["confiabilidad","Confiabilidad"],["sin_incidencias","Sin incidencias"],["trato","Trato al p\u00fablico"],["iniciativa","Iniciativa"]];

function parseDate(str){
str=(str||"").trim(); if(!str) return null;
var m;
if (str.indexOf("/")>=0){ var p=str.split("/"); if(p.length===3){ var d=parseInt(p[0],10),mo=parseInt(p[1],10),y=parseInt(p[2],10); if(y<100)y+=2000; var dt=new Date(y,mo-1,d); return isNaN(dt.getTime())?null:dt; } }
if (str.indexOf("-")>=0){ var q=str.split("-"); if(q.length===3){ var dt2=new Date(parseInt(q[0],10),parseInt(q[1],10)-1,parseInt(q[2],10)); return isNaN(dt2.getTime())?null:dt2; } }
return null;
}
function edad(nac){
var d=parseDate(nac); if(!d) return null;
var h=new Date(); var a=h.getFullYear()-d.getFullYear();
var mm=h.getMonth()-d.getMonth(); if(mm<0 || (mm===0 && h.getDate()<d.getDate())) a--;
if(a<0 || a>120) return null;
return a;
}
function experiencia(fi){
var d=parseDate(fi); if(!d) return "";
var h=new Date(); var meses=(h.getFullYear()-d.getFullYear())*12 + (h.getMonth()-d.getMonth());
if(h.getDate()<d.getDate()) meses--;
if(meses<0) return "";
var an=Math.floor(meses/12), me=meses%12;
if(an<=0) return me + " mes" + (me!==1?"es":"");
if(me===0) return an + " a\u00f1o" + (an!==1?"s":"");
return an + " a\u00f1o" + (an!==1?"s":"") + " " + me + " mes" + (me!==1?"es":"");
}
function rateCls(c){ if(!c.calificado) return "none"; if(c.calificacion>=80) return "hi"; if(c.calificacion>=60) return "mid"; return "low"; }
function rateLabel(c){ return c.calificado ? (c.calificacion + "%") : "Sin calificar"; }

function avatarUrl(dni){ return API_BASE + "/api/chat/avatar/" + encodeURIComponent(dni||""); }

var lista = [];
var abiertos = {};

function render(filtro){
var cont = document.getElementById("perfList");
filtro = (filtro||"").toLowerCase();
var arr = lista.filter(function(s){ return !filtro || (s.nombre||"").toLowerCase().indexOf(filtro)!==-1 || (s.instalacion||"").toLowerCase().indexOf(filtro)!==-1; });
if(!arr.length){ cont.innerHTML='<div class="empty-note" style="padding:24px;color:var(--muted);">Sin socorristas.</div>'; return; }
cont.innerHTML = arr.map(function(s){
var ed = edad(s.nacimiento); var exp = experiencia(s.fecha_inicio);
var sub = [ (ed!=null? ed+" a\u00f1os":""), (s.instalacion||""), (s.rol||"") ].filter(Boolean).join(" \u00b7 ");
var cls = rateCls(s);
var abierto = !!abiertos[s.dni];
var crithtml = CRITS.map(function(c){ var v=(s.criterios&&s.criterios[c[0]])||0; return '<div class="crit"><span>'+c[1]+'</span><span class="bar"><i style="width:'+(v/5*100)+'%"></i></span><span>'+v+'/5</span></div>'; }).join("");
return '<div class="pcard'+(abierto?" open":"")+'" data-dni="'+esc(s.dni)+'">' +
'<div class="pcard-main">' +
'<div class="pcard-photo"><img src="'+avatarUrl(s.dni)+'" data-ini="'+esc(initials(s.nombre))+'" alt=""/></div>' +
'<div class="pcard-info"><div class="pcard-name">'+esc(s.nombre||s.dni)+'</div><div class="pcard-sub">'+esc(sub)+'</div></div>' +
'<div class="pcard-rate"><span class="rate-badge '+cls+'">'+rateLabel(s)+'</span></div>' +
'</div>' +
'<div class="pcard-det">' +
'<div class="det-row"><b>Experiencia:</b> '+(exp?esc(exp):"&mdash;")+'</div>' +
'<div class="det-row"><b>Contrato:</b> '+(s.contrato?esc(s.contrato):"&mdash;")+'</div>' +
'<div style="margin:10px 0 4px 0;font-size:12px;color:#6b7688;font-weight:700;">CALIFICACI\u00d3N</div>' +
crithtml +
(s.comentario ? '<div class="det-row" style="margin-top:6px;"><b>Comentario:</b> '+esc(s.comentario)+'</div>' : '') +
(ES_ADMIN ? '<div class="det-actions"><button class="primary-btn sm" data-cal="'+esc(s.dni)+'">'+(s.calificado?"Editar calificaci\u00f3n":"Calificar")+'</button></div>' : '') +
'</div>' +
'</div>';
}).join("");
// toggle abrir (no al tocar foto ni boton)
cont.querySelectorAll(".pcard-main").forEach(function(m){
m.addEventListener("click", function(e){
if(e.target.tagName==="IMG") return;
var card=m.closest(".pcard"); var dni=card.getAttribute("data-dni");
abiertos[dni]=!abiertos[dni]; render(document.getElementById("buscarPerf").value);
});
});
// foto ampliar
cont.querySelectorAll(".pcard-photo img").forEach(function(img){
img.addEventListener("click", function(e){ e.stopPropagation(); var v=document.getElementById("imgViewerImg"); v.src=img.src; document.getElementById("imgViewer").classList.add("open"); });
});
// calificar
cont.querySelectorAll("[data-cal]").forEach(function(bt){
bt.addEventListener("click", function(e){ e.stopPropagation(); abrirCal(bt.getAttribute("data-cal")); });
});
}

// avatar fallback -> iniciales
document.addEventListener("error", function(e){
var t=e.target;
if(t && t.tagName==="IMG" && t.closest && t.closest(".pcard-photo")){
var ini=t.getAttribute("data-ini")||"?"; var padre=t.parentNode; if(padre) padre.textContent=ini;
}
}, true);

var imgViewer=document.getElementById("imgViewer");
imgViewer.addEventListener("click", function(){ imgViewer.classList.remove("open"); });

function cargar(){
fetch(API_BASE + "/api/perfiles?user_id=" + encodeURIComponent(AUTH_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
if(!d || !d.ok){ document.getElementById("perfList").innerHTML='<div class="empty-note" style="padding:24px;color:var(--muted);">No se pudo cargar.</div>'; return; }
lista = d.socorristas || [];
render(document.getElementById("buscarPerf").value);
})
.catch(function(){ document.getElementById("perfList").innerHTML='<div class="empty-note" style="padding:24px;color:var(--muted);">Error de conexi\u00f3n.</div>'; });
}
document.getElementById("buscarPerf").addEventListener("input", function(e){ render(e.target.value); });

/* ---- Modal calificar ---- */
var calModal=document.getElementById("calModal");
var calDni=null; var calVals={};
function abrirCal(dni){
var s=lista.filter(function(x){return x.dni===dni;})[0]; if(!s) return;
calDni=dni; calVals={};
document.getElementById("calTitle").innerHTML="Calificar a "+esc(s.nombre||dni);
var html="";
CRITS.forEach(function(c){
var v=(s.criterios&&s.criterios[c[0]])||0; calVals[c[0]]=v;
var stars=""; for(var i=1;i<=5;i++){ stars+='<span class="st'+(i<=v?" on":"")+'" data-c="'+c[0]+'" data-v="'+i+'">&#9733;</span>'; }
html+='<div class="crit-row"><span class="cl">'+c[1]+'</span><span class="stars" data-cg="'+c[0]+'">'+stars+'</span></div>';
});
document.getElementById("calCrit").innerHTML=html;
document.getElementById("cal_comentario").value=s.comentario||"";
var mm=document.getElementById("calMsg"); mm.className="msg"; mm.textContent="";
document.getElementById("calCrit").querySelectorAll(".st").forEach(function(st){
st.addEventListener("click", function(){
var c=st.getAttribute("data-c"), v=parseInt(st.getAttribute("data-v"),10);
calVals[c]=v;
var grupo=st.parentNode;
grupo.querySelectorAll(".st").forEach(function(x){ x.classList.toggle("on", parseInt(x.getAttribute("data-v"),10)<=v); });
});
});
calModal.classList.add("open");
}
document.getElementById("calCancel").addEventListener("click", function(){ calModal.classList.remove("open"); });
document.getElementById("calSave").addEventListener("click", function(){
if(!calDni) return;
var msgEl=document.getElementById("calMsg");
var body={dni:calDni, comentario:document.getElementById("cal_comentario").value};
CRITS.forEach(function(c){ body[c[0]]=calVals[c[0]]||0; });
var btn=this; btn.disabled=true; btn.textContent="Guardando...";
fetch(API_BASE + "/api/perfiles/calificar", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body) })
.then(function(r){ return r.json(); })
.then(function(d){
btn.disabled=false; btn.textContent="Guardar";
if(d && d.ok){ msgEl.className="msg ok"; msgEl.textContent="Calificaci\u00f3n guardada ("+d.calificacion+"%)."; setTimeout(function(){ calModal.classList.remove("open"); cargar(); }, 900); }
else { msgEl.className="msg err"; msgEl.textContent=(d && d.error) || "Error al guardar."; }
})
.catch(function(){ btn.disabled=false; btn.textContent="Guardar"; msgEl.className="msg err"; msgEl.textContent="Error de conexi\u00f3n."; });
});

cargar();
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
