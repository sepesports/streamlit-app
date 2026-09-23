# pages/directivo.py
import json
import streamlit as st
import streamlit.components.v1 as components
import importlib
import syntra_core
importlib.reload(syntra_core)
from syntra_core import sync_auth, go, shell_css, NAV_JS

st.set_page_config(page_title="Panel Directivo", layout="wide")
sync_auth()

qp = st.query_params
AUTH_USER = qp.get("usuario") or qp.get("user") or ""
AUTH_ROLE = qp.get("rol") or qp.get("role") or ""
AUTH_DNI = qp.get("dni") or ""
NORMALIZED_ROLE = AUTH_ROLE.strip().lower()

if not AUTH_USER or not AUTH_ROLE:
    go("pages/admin.py")

# El panel del Directivo es exclusivo del rol Directivo
if NORMALIZED_ROLE != "directivo":
    go("app.py")

API_BASE = "https://camilo27.pythonanywhere.com"
LOGO_DATA_URI = "data:image/png;base64,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"
LOGO_URL = LOGO_DATA_URI

shell_css()


def _js_str(value):
    return json.dumps(value)


HTML = r"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
:root{--blue:#2f6fe0;--red:#d64545;--border:#e5e9f2;--muted:#6b7688;--ink:#1b2740;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);}
#app{display:flex;min-height:100vh;}
#sidebar{width:230px;flex:0 0 230px;background:linear-gradient(180deg,#16264d,#0b162f);color:#eaf2ff;padding:16px 12px;}
.logo-row{display:flex;align-items:center;gap:10px;padding:6px 8px 16px;}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:10px;color:#cdd8ef;cursor:pointer;font-size:13.5px;font-weight:600;margin-bottom:2px;}
.nav-item:hover{background:rgba(255,255,255,.06);}
.nav-item.active{background:rgba(90,140,255,.22);color:#fff;}
.nav-item .nav-badge{margin-left:auto;font-size:9.5px;background:rgba(255,255,255,.14);padding:2px 6px;border-radius:20px;}
.nav-sep{height:1px;background:rgba(255,255,255,.12);margin:10px 6px;}
.nav-bottom{margin-top:18px;}
#main{flex:1;min-width:0;display:flex;flex-direction:column;background:transparent;}
#topbar{display:flex;align-items:center;gap:12px;padding:10px 14px;color:#eaf2ff;}
#topbar h1{font-size:17px;margin:0;font-weight:800;letter-spacing:.2px;}
.hamburger{display:none;background:none;border:0;color:#eaf2ff;font-size:22px;cursor:pointer;}
.mobile-logo{display:none;}
#content{margin:0 12px 18px;background:#f5f7fc;border-radius:16px;padding:14px;min-height:70vh;}

.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;margin-bottom:16px;}
.filters .fld{display:flex;flex-direction:column;gap:4px;}
.filters label{font-size:11px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.4px;}
.filters input,.filters select{padding:8px 10px;border:1px solid var(--border);border-radius:9px;font-size:13px;background:#fff;min-width:130px;}
.btn{border:none;cursor:pointer;font-weight:700;border-radius:9px;padding:9px 14px;font-size:12.5px;}
.btn.primary{background:var(--blue);color:#fff;}
.btn.ghost{background:#fff;border:1px solid var(--border);color:var(--ink);}
.chips{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;}
.chip{background:#eef3ff;color:#2f5bd0;border:1px solid #d9e4ff;border-radius:20px;padding:6px 12px;font-size:12px;font-weight:700;cursor:pointer;}
.chip:hover{background:#e2ecff;}

.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px;}
.kpi{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 16px;box-shadow:0 6px 18px rgba(20,40,80,.06);}
.kpi .k-lbl{font-size:11px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.4px;}
.kpi .k-val{font-size:24px;font-weight:800;margin-top:6px;color:var(--ink);}
.kpi .k-sub{font-size:11.5px;color:var(--muted);margin-top:2px;}
.kpi.accent .k-val{color:#1a7f4f;}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.grid2>.card{margin-bottom:0;}
.card{background:#fff;border:1px solid var(--border);border-radius:14px;padding:16px;margin-bottom:16px;box-shadow:0 6px 18px rgba(20,40,80,.06);min-width:0;}
.card h3{margin:0 0 12px;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:space-between;}
.tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;}
.tscroll table{min-width:100%;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th,td{text-align:left;padding:8px 8px;border-bottom:1px solid #eef1f7;}
th{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.3px;}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;}
.tar-input{width:110px;padding:6px 8px;border:1px solid var(--border);border-radius:8px;font-size:13px;text-align:right;}
.tar-input:disabled{background:#f3f5fa;color:#9aa4b6;}
.tar-editor{display:flex;flex-wrap:wrap;align-items:center;gap:10px;}
.tar-editor select{flex:1;min-width:160px;padding:8px 10px;border:1px solid var(--border);border-radius:9px;font-size:13px;background:#fff;}
.tar-editor .mini:disabled{background:#c7cbd6;cursor:not-allowed;}
.tar-hint{font-size:12px;color:var(--muted);margin-top:10px;}
.tar-hint.warn{color:#a3690a;}
.tar-hint.ok{color:#1a7f4f;}
.mini{border:none;cursor:pointer;font-size:11.5px;font-weight:700;padding:5px 10px;border-radius:8px;background:var(--blue);color:#fff;}
.mini:disabled{cursor:not-allowed;}
.pill{display:inline-block;padding:2px 8px;border-radius:20px;font-size:10.5px;font-weight:700;}
.pill.warn{background:#fff4e0;color:#a3690a;}
.pill.ok{background:#e6f7ee;color:#1a7f4f;}
.alerta{background:#fff4e0;color:#8a5808;border:1px solid #ffe4b3;border-radius:10px;padding:10px 12px;font-size:12.5px;margin-bottom:12px;}
.bar-row{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:12px;}
.bar-row .bl{width:34%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--ink);font-weight:600;}
.bar-row .bt{flex:1;background:#eef1f7;border-radius:6px;height:16px;position:relative;overflow:hidden;}
.bar-row .bf{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#3f7bff,#1f4fd8);border-radius:6px;}
.bar-row .bv{width:74px;text-align:right;font-variant-numeric:tabular-nums;color:var(--muted);}
.empty{color:var(--muted);font-size:13px;padding:14px 4px;}

.mobile-drawer{display:none;}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(10,20,50,.45);z-index:200;align-items:center;justify-content:center;}
.modal-overlay.open{display:flex;}
.modal{background:#fff;border-radius:14px;padding:20px;width:min(92vw,380px);}
.modal h3{margin:0 0 12px;font-size:15px;}
.modal .field{margin-bottom:12px;}
.modal .field label{display:block;font-size:12px;color:var(--muted);margin-bottom:5px;font-weight:600;}
.modal .field input{width:100%;padding:9px 11px;border:1px solid var(--border);border-radius:9px;font-size:13px;}
.modal .actions{display:flex;justify-content:flex-end;gap:8px;margin-top:8px;}
.btn-cancel{background:#fff;border:1px solid var(--border);border-radius:9px;padding:9px 14px;font-size:12.5px;font-weight:700;cursor:pointer;}
.msg{font-size:12.5px;margin-top:10px;padding:8px 12px;border-radius:9px;display:none;}
.msg.ok{background:#e6f7ee;color:#1a7f4f;display:block;}
.msg.err{background:#fde8e8;color:#b02a2a;display:block;}

@media (max-width:900px){
 #sidebar{display:none;}
 .hamburger{display:block;}
 .mobile-logo{display:flex;align-items:center;}
 .kpis{grid-template-columns:1fr 1fr;gap:10px;}
 .grid2{grid-template-columns:1fr;gap:12px;}
 #content{margin:0 0 16px;padding:12px 10px;border-radius:0;}
 #topbar{padding:10px 10px;}
 .card{padding:14px;}
 .mobile-drawer{display:block;}
 .mobile-drawer .overlay{position:fixed;inset:0;background:rgba(0,0,0,.4);opacity:0;pointer-events:none;transition:.2s;z-index:80;}
 .mobile-drawer.open .overlay{opacity:1;pointer-events:auto;}
 .mobile-drawer .panel{position:fixed;top:0;left:-260px;width:250px;height:100%;background:linear-gradient(180deg,#16264d,#0b162f);color:#eaf2ff;z-index:90;transition:.2s;padding:16px 12px;}
 .mobile-drawer.open .panel{left:0;}
}
</style>
</head>
<body>
<div id="app">
<div id="sidebar"><div class="logo-row"><img src="__LOGO_URL__" alt="SYNTRA" style="height:40px;"/></div><div id="navList"></div></div>
<div class="mobile-drawer" id="drawer">
<div class="overlay" id="drawerOverlay"></div>
<div class="panel"><div class="logo-row"><img src="__LOGO_URL__" alt="SYNTRA" style="height:40px;"/></div><div id="navListMobile"></div></div>
</div>
<div id="main">
<div id="topbar">
<button class="hamburger" id="hamburgerBtn">&#9776;</button>
<h1>Panel Directivo</h1>
<div class="mobile-logo"><img src="__LOGO_URL__" alt="SYNTRA" style="height:38px;"/></div>
</div>
<div id="content">

<div class="filters">
<div class="fld"><label>Desde</label><input type="date" id="f_desde"/></div>
<div class="fld"><label>Hasta</label><input type="date" id="f_hasta"/></div>
<div class="fld"><label>Instalaci&oacute;n</label><select id="f_inst"><option value="">Todas</option></select></div>
<div class="fld"><label>Socorrista</label><input id="f_soc" list="dlSoc" placeholder="Todos"/></div>
<button class="btn primary" id="aplicarBtn">Aplicar</button>
<button class="btn ghost" id="limpiarBtn">Limpiar</button>
</div>
<div class="chips">
<span class="chip" data-range="hoy">Hoy</span>
<span class="chip" data-range="semana">Esta semana</span>
<span class="chip" data-range="mes">Este mes</span>
<span class="chip" data-range="todo">Todo</span>
</div>

<div class="kpis">
<div class="kpi"><div class="k-lbl">Socorristas</div><div class="k-val" id="kpi_soc">-</div><div class="k-sub">con turnos en el rango</div></div>
<div class="kpi"><div class="k-lbl">Horas confirmadas</div><div class="k-val" id="kpi_horas">-</div><div class="k-sub" id="kpi_horas_sub">programadas: -</div></div>
<div class="kpi accent"><div class="k-lbl">N&oacute;mina confirmada</div><div class="k-val" id="kpi_imp">-</div><div class="k-sub">horas ON &times; tarifa</div></div>
<div class="kpi"><div class="k-lbl">Proyectado</div><div class="k-val" id="kpi_prog">-</div><div class="k-sub">todos los turnos del rango</div></div>
</div>

<div id="alertaTarifa" class="alerta" style="display:none;"></div>

<div class="grid2">
<div class="card">
<h3>N&oacute;mina por socorrista</h3>
<div class="tscroll"><table>
<thead><tr><th>Socorrista</th><th class="num">H. conf.</th><th class="num">Importe</th><th class="num">H. prog.</th><th class="num">Proyect.</th></tr></thead>
<tbody id="socBody"><tr><td colspan="5" class="empty">Cargando...</td></tr></tbody>
</table></div>
</div>
<div class="card">
<h3>Importe por socorrista (confirmado)</h3>
<div id="chartSoc"><div class="empty">Cargando...</div></div>
</div>
</div>

<div class="grid2">
<div class="card">
<h3>Tarifas por instalaci&oacute;n <button class="mini" id="addInstBtn">+ Instalaci&oacute;n</button></h3>
<div class="tar-editor">
<select id="tarSelect"><option value="">Cargando...</option></select>
<input id="tarValor" class="tar-input" type="number" step="0.01" min="0" placeholder="Valor/hora" disabled/>
<button class="mini" id="tarGuardar" disabled>Guardar</button>
</div>
<div id="tarHint" class="tar-hint">Elige una instalaci&oacute;n para ver o fijar su valor por hora.</div>
</div>
<div class="card">
<h3>Importe por instalaci&oacute;n (confirmado)</h3>
<div id="chartInst"><div class="empty">Cargando...</div></div>
</div>
</div>

<div class="card">
<h3>N&oacute;mina por instalaci&oacute;n</h3>
<div class="tscroll"><table>
<thead><tr><th>Instalaci&oacute;n</th><th class="num">Valor/h</th><th class="num">H. conf.</th><th class="num">Importe</th><th class="num">H. prog.</th><th class="num">Proyect.</th></tr></thead>
<tbody id="instBody"><tr><td colspan="6" class="empty">Cargando...</td></tr></tbody>
</table></div>
</div>

</div>
</div>
</div>

<div class="modal-overlay" id="instModal">
<div class="modal">
<h3>Nueva instalaci&oacute;n</h3>
<div class="field"><label>Nombre de la instalaci&oacute;n</label><input id="inst_nombre" placeholder="Ej. Piscina Central"/></div>
<div class="msg" id="instMsg"></div>
<div class="actions">
<button class="btn-cancel" id="instCancelBtn">Cancelar</button>
<button class="btn primary" id="instSaveBtn">Agregar</button>
</div>
</div>
</div>

<datalist id="dlSoc"></datalist>

<script>
__SYNTRA_NAV__
(function(){
var API_BASE = __API_BASE__;
var AUTH_USER = __AUTH_USER__;
var AUTH_ROLE = __AUTH_ROLE__;
var AUTH_DNI = __AUTH_DNI__;

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
{label:"Perfiles", icon:"&#11088;", go:"/perfiles", badge:"Solo admin"},
{label:"Panel Directivo", icon:"&#128202;", go:"/directivo", active:true, badge:"Directivo"}
];
/* Menu por rol: solo se muestran las opciones habilitadas para cada perfil */
(function(){
var _rolNav = String(AUTH_ROLE || "").trim().toLowerCase();
var _permNav = {"/altas_registro":["administrador"], "/editar_horarios":["administrador"], "/perfiles":["administrador","directivo"], "/directivo":["directivo"]};
NAV_ITEMS = NAV_ITEMS.filter(function(it){ return it.sep || !_permNav[it.go] || _permNav[it.go].indexOf(_rolNav) !== -1; });
if (NAV_ITEMS.length && NAV_ITEMS[NAV_ITEMS.length - 1].sep) NAV_ITEMS.pop();
NAV_ITEMS.forEach(function(it){ if (it.go === "/perfiles" && _rolNav === "directivo") it.badge = "Solo ver"; });
})();
function renderNav(id){
var el=document.getElementById(id); var parts=[];
NAV_ITEMS.forEach(function(it){
if(it.sep){ parts.push('<div class="nav-sep"></div>'); return; }
var cls="nav-item"+(it.active?" active":"");
var b=it.badge?'<span class="nav-badge">'+it.badge+'</span>':"";
parts.push('<div class="'+cls+'" data-go="'+it.go+'"><span>'+it.icon+'</span><span>'+it.label+'</span>'+b+'</div>');
});
parts.push('<div class="nav-bottom"><div class="nav-item" id="logout_'+id+'"><span>&#8630;</span><span>Cerrar sesi&oacute;n</span></div></div>');
el.innerHTML=parts.join("");
el.querySelectorAll(".nav-item[data-go]").forEach(function(n){ n.addEventListener("click", function(){ goToPage(n.getAttribute("data-go")); }); });
var lo=document.getElementById("logout_"+id); if(lo) lo.addEventListener("click", function(){ syntraTopNav("/admin"); });
}
renderNav("navList"); renderNav("navListMobile");
var drawer=document.getElementById("drawer");
document.getElementById("hamburgerBtn").addEventListener("click", function(){ drawer.classList.add("open"); });
document.getElementById("drawerOverlay").addEventListener("click", function(){ drawer.classList.remove("open"); });

function esc(t){ return String(t==null?"":t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;"); }
function fmtN(n, dec){ dec = (dec==null?2:dec); var v=Number(n||0); return v.toLocaleString("es-CO",{minimumFractionDigits:dec, maximumFractionDigits:dec}); }
function fmtMoney(n){ return fmtN(n,0); }

function isoToInput(d){ var m=String(d.getMonth()+1).padStart(2,"0"); var day=String(d.getDate()).padStart(2,"0"); return d.getFullYear()+"-"+m+"-"+day; }

document.querySelectorAll(".chip").forEach(function(ch){
ch.addEventListener("click", function(){
var r=ch.getAttribute("data-range"); var hoy=new Date(); var d1="", d2="";
if(r==="hoy"){ d1=isoToInput(hoy); d2=d1; }
else if(r==="semana"){ var wd=(hoy.getDay()+6)%7; var lun=new Date(hoy); lun.setDate(hoy.getDate()-wd); var dom=new Date(lun); dom.setDate(lun.getDate()+6); d1=isoToInput(lun); d2=isoToInput(dom); }
else if(r==="mes"){ var pri=new Date(hoy.getFullYear(),hoy.getMonth(),1); var ult=new Date(hoy.getFullYear(),hoy.getMonth()+1,0); d1=isoToInput(pri); d2=isoToInput(ult); }
else { d1=""; d2=""; }
document.getElementById("f_desde").value=d1; document.getElementById("f_hasta").value=d2;
cargarNomina();
});
});
document.getElementById("aplicarBtn").addEventListener("click", cargarNomina);
document.getElementById("limpiarBtn").addEventListener("click", function(){
document.getElementById("f_desde").value=""; document.getElementById("f_hasta").value="";
document.getElementById("f_inst").value=""; document.getElementById("f_soc").value=""; cargarNomina();
});

// ---- Socorristas para el datalist ----
fetch(API_BASE+"/api/chat/users").then(function(r){return r.json();}).then(function(d){
var us=Array.isArray(d)?d:((d&&d.users)||[]);
var dl=document.getElementById("dlSoc");
us.map(function(u){return (u.nombre||u.alias||"").trim();}).filter(Boolean).sort().forEach(function(n){ var o=document.createElement("option"); o.value=n; dl.appendChild(o); });
}).catch(function(){});

// ---- Tarifas ----
function cargarTarifas(){
fetch(API_BASE+"/api/tarifas").then(function(r){return r.json();}).then(function(d){
var items=(d&&d.items)||[];
var map={}; items.forEach(function(i){ map[i.instalacion]={valor:i.valor_hora, definida:!!i.definida}; });
window.__tarMap=map;
// llenar filtro de instalaciones (arriba)
var f=document.getElementById("f_inst"); var prevF=f.value;
f.innerHTML='<option value="">Todas</option>'+items.map(function(i){return '<option value="'+esc(i.instalacion)+'">'+esc(i.instalacion)+'</option>';}).join("");
f.value=prevF;
// selector de tarifas (editar una a la vez)
var sel=document.getElementById("tarSelect"); var prev=sel.value;
if(!items.length){
  sel.innerHTML='<option value="">Sin instalaciones</option>';
  var h=document.getElementById("tarHint"); h.className="tar-hint warn"; h.textContent="No hay instalaciones registradas. Usa “+ Instalación” para crear una.";
  return;
}
sel.innerHTML='<option value="">Selecciona instalación...</option>'+items.map(function(i){var s=i.definida?'':' (sin tarifa)'; return '<option value="'+esc(i.instalacion)+'">'+esc(i.instalacion)+s+'</option>';}).join("");
sel.value=(prev&&map[prev])?prev:"";
aplicarSeleccionTarifa();
if(!window.__tarWired){
  window.__tarWired=true;
  document.getElementById("tarSelect").addEventListener("change", aplicarSeleccionTarifa);
  document.getElementById("tarGuardar").addEventListener("click", guardarTarifa);
}
}).catch(function(){ var h=document.getElementById("tarHint"); h.className="tar-hint warn"; h.textContent="Error al cargar tarifas."; });
}
function aplicarSeleccionTarifa(){
var inst=document.getElementById("tarSelect").value;
var val=document.getElementById("tarValor");
var btn=document.getElementById("tarGuardar");
var hint=document.getElementById("tarHint");
var map=window.__tarMap||{};
if(!inst){ val.value=""; val.disabled=true; btn.disabled=true; hint.className="tar-hint"; hint.textContent="Elige una instalación para ver o fijar su valor por hora."; return; }
var info=map[inst]||{};
val.disabled=false; btn.disabled=false;
val.value=info.definida?info.valor:"";
if(info.definida){ hint.className="tar-hint ok"; hint.textContent="Valor actual: "+info.valor+" por hora. Edita y guarda para actualizar."; }
else { hint.className="tar-hint warn"; hint.textContent="Esta instalación aún no tiene tarifa. Fija su valor/hora y guarda."; }
}
function guardarTarifa(){
var inst=document.getElementById("tarSelect").value;
var val=(document.getElementById("tarValor").value||"").trim();
var btn=document.getElementById("tarGuardar");
if(!inst) return;
if(val===""){ alert("Indica un valor por hora."); return; }
btn.textContent="..."; btn.disabled=true;
fetch(API_BASE+"/api/tarifas",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({instalacion:inst, valor:val})})
.then(function(r){return r.json();}).then(function(d){
btn.disabled=false; btn.textContent="Guardar";
if(d&&d.ok){ btn.textContent="✓"; setTimeout(function(){btn.textContent="Guardar";},900); cargarTarifas(); cargarNomina(); }
else alert((d&&d.error)||"Error al guardar.");
}).catch(function(){ btn.disabled=false; btn.textContent="Guardar"; alert("Error de conexión."); });
}

// ---- Nomina ----
function barras(cont, filas, valKey, labKey){
var el=document.getElementById(cont);
var arr=filas.filter(function(x){return Number(x[valKey])>0;});
if(!arr.length){ el.innerHTML='<div class="empty">Sin importes en el rango.</div>'; return; }
var max=Math.max.apply(null, arr.map(function(x){return Number(x[valKey]);}));
el.innerHTML=arr.slice(0,10).map(function(x){
var w=max>0?(Number(x[valKey])/max*100):0;
return '<div class="bar-row"><div class="bl" title="'+esc(x[labKey])+'">'+esc(x[labKey])+'</div>'+
'<div class="bt"><div class="bf" style="width:'+w.toFixed(1)+'%"></div></div>'+
'<div class="bv">'+fmtMoney(x[valKey])+'</div></div>';
}).join("");
}

function cargarNomina(){
var p=new URLSearchParams();
var d1=document.getElementById("f_desde").value; var d2=document.getElementById("f_hasta").value;
var inst=document.getElementById("f_inst").value; var soc=document.getElementById("f_soc").value.trim();
if(d1) p.set("desde",d1); if(d2) p.set("hasta",d2); if(inst) p.set("instalacion",inst); if(soc) p.set("socorrista",soc);
fetch(API_BASE+"/api/nomina?"+p.toString()).then(function(r){return r.json();}).then(function(d){
if(!d||!d.ok){ return; }
var t=d.totales||{};
document.getElementById("kpi_soc").textContent=t.socorristas||0;
document.getElementById("kpi_horas").textContent=fmtN(t.horas_conf,1);
document.getElementById("kpi_horas_sub").textContent="programadas: "+fmtN(t.horas_prog,1);
document.getElementById("kpi_imp").textContent=fmtMoney(t.importe_conf);
document.getElementById("kpi_prog").textContent=fmtMoney(t.importe_prog);

var sinT=(d.sin_tarifa||[]);
var al=document.getElementById("alertaTarifa");
if(sinT.length){ al.style.display="block"; al.innerHTML="&#9888; Instalaciones sin tarifa (no suman importe): <b>"+sinT.map(esc).join(", ")+"</b>. Fija su valor/hora abajo."; }
else { al.style.display="none"; }

var socArr=(d.por_socorrista||[]);
var sb=document.getElementById("socBody");
sb.innerHTML=socArr.length?socArr.map(function(s){
return '<tr><td>'+esc(s.socorrista)+'</td><td class="num">'+fmtN(s.horas_conf,1)+'</td><td class="num">'+fmtMoney(s.importe_conf)+'</td><td class="num">'+fmtN(s.horas_prog,1)+'</td><td class="num">'+fmtMoney(s.importe_prog)+'</td></tr>';
}).join(""):'<tr><td colspan="5" class="empty">Sin turnos en el rango.</td></tr>';

var instArr=(d.por_instalacion||[]);
var ib=document.getElementById("instBody");
ib.innerHTML=instArr.length?instArr.map(function(i){
return '<tr><td>'+esc(i.instalacion)+'</td><td class="num">'+fmtN(i.valor_hora,0)+'</td><td class="num">'+fmtN(i.horas_conf,1)+'</td><td class="num">'+fmtMoney(i.importe_conf)+'</td><td class="num">'+fmtN(i.horas_prog,1)+'</td><td class="num">'+fmtMoney(i.importe_prog)+'</td></tr>';
}).join(""):'<tr><td colspan="6" class="empty">Sin turnos en el rango.</td></tr>';

barras("chartSoc", socArr, "importe_conf", "socorrista");
barras("chartInst", instArr, "importe_conf", "instalacion");
}).catch(function(){});
}

// ---- Modal + Instalacion ----
var instModal=document.getElementById("instModal");
document.getElementById("addInstBtn").addEventListener("click", function(){
document.getElementById("inst_nombre").value=""; var m=document.getElementById("instMsg"); m.className="msg"; m.textContent=""; instModal.classList.add("open");
});
document.getElementById("instCancelBtn").addEventListener("click", function(){ instModal.classList.remove("open"); });
document.getElementById("instSaveBtn").addEventListener("click", function(){
var nombre=document.getElementById("inst_nombre").value.trim(); var m=document.getElementById("instMsg");
if(!nombre){ m.className="msg err"; m.textContent="Escribe un nombre."; return; }
fetch(API_BASE+"/api/instalaciones",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({nombre:nombre})})
.then(function(r){return r.json();}).then(function(d){
if(d&&d.ok){ m.className="msg ok"; m.textContent="Instalación agregada."; setTimeout(function(){ instModal.classList.remove("open"); cargarTarifas(); },700); }
else { m.className="msg err"; m.textContent=(d&&d.error)||"Error al agregar."; }
}).catch(function(){ m.className="msg err"; m.textContent="Error de conexión."; });
});

cargarTarifas();
cargarNomina();
})();
</script>
</body>
</html>
"""

html = (HTML
        .replace("__LOGO_URL__", LOGO_URL)
        .replace("__API_BASE__", _js_str(API_BASE))
        .replace("__AUTH_USER__", _js_str(AUTH_USER))
        .replace("__AUTH_ROLE__", _js_str(AUTH_ROLE))
        .replace("__AUTH_DNI__", _js_str(AUTH_DNI)))
html = html.replace("__SYNTRA_NAV__", NAV_JS)

components.html(html, height=1000, scrolling=True)
