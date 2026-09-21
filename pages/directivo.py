# pages/directivo.py
import json
import streamlit as st
import streamlit.components.v1 as components
import importlib
import syntra_core
importlib.reload(syntra_core)
from syntra_core import sync_auth, go, shell_css, NAV_JS, LOGO_DATA_URI

st.set_page_config(page_title="Panel Directivo", layout="wide")
sync_auth()

qp = st.query_params
AUTH_USER = qp.get("usuario") or qp.get("user") or ""
AUTH_ROLE = qp.get("rol") or qp.get("role") or ""
AUTH_DNI = qp.get("dni") or ""
NORMALIZED_ROLE = AUTH_ROLE.strip().lower()

if not AUTH_USER or not AUTH_ROLE:
    go("pages/admin.py")

# El panel del Directivo tambien es visible para el Administrador (rol superior)
if NORMALIZED_ROLE not in ("directivo", "administrador"):
    go("app.py")

API_BASE = "https://camilo27.pythonanywhere.com"
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
#topbar{display:flex;align-items:center;gap:12px;padding:14px 20px;color:#eaf2ff;}
#topbar h1{font-size:17px;margin:0;font-weight:800;letter-spacing:.2px;}
.hamburger{display:none;background:none;border:0;color:#eaf2ff;font-size:22px;cursor:pointer;}
.mobile-logo{display:none;}
#content{margin:0 18px 26px;background:#f5f7fc;border-radius:16px;padding:18px;min-height:70vh;}

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
.card{background:#fff;border:1px solid var(--border);border-radius:14px;padding:16px;margin-bottom:16px;box-shadow:0 6px 18px rgba(20,40,80,.06);}
.card h3{margin:0 0 12px;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:space-between;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th,td{text-align:left;padding:8px 8px;border-bottom:1px solid #eef1f7;}
th{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.3px;}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;}
.tar-input{width:110px;padding:6px 8px;border:1px solid var(--border);border-radius:8px;font-size:13px;text-align:right;}
.mini{border:none;cursor:pointer;font-size:11.5px;font-weight:700;padding:5px 10px;border-radius:8px;background:var(--blue);color:#fff;}
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
 .kpis{grid-template-columns:1fr 1fr;}
 .grid2{grid-template-columns:1fr;}
 #content{margin:0 10px 26px;}
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
<div class="tscroll"><table>
<thead><tr><th>Instalaci&oacute;n</th><th class="num">Valor/hora</th><th></th></tr></thead>
<tbody id="tarBody"><tr><td colspan="3" class="empty">Cargando...</td></tr></tbody>
</table></div>
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
{label:"Panel Directivo", icon:"&#128202;", go:"/directivo", active:true, badge:"Directivo"}
];
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
// llenar filtro de instalaciones
var sel=document.getElementById("f_inst"); var prev=sel.value;
sel.innerHTML='<option value="">Todas</option>'+items.map(function(i){return '<option value="'+esc(i.instalacion)+'">'+esc(i.instalacion)+'</option>';}).join("");
sel.value=prev;
var tb=document.getElementById("tarBody");
if(!items.length){ tb.innerHTML='<tr><td colspan="3" class="empty">Sin instalaciones.</td></tr>'; return; }
tb.innerHTML=items.map(function(i){
var badge=i.definida?'':' <span class="pill warn">sin tarifa</span>';
return '<tr><td>'+esc(i.instalacion)+badge+'</td>'+
'<td class="num"><input class="tar-input" type="number" step="0.01" min="0" value="'+(i.definida?i.valor_hora:"")+'" data-inst="'+esc(i.instalacion)+'" placeholder="0"/></td>'+
'<td class="num"><button class="mini" data-save="'+esc(i.instalacion)+'">Guardar</button></td></tr>';
}).join("");
tb.querySelectorAll("button[data-save]").forEach(function(b){
b.addEventListener("click", function(){
var inst=b.getAttribute("data-save");
var inp=tb.querySelector('input[data-inst="'+inst.replace(/"/g,'\\"')+'"]');
var val=(inp&&inp.value||"").trim();
if(val===""){ alert("Indica un valor por hora."); return; }
b.textContent="..."; b.disabled=true;
fetch(API_BASE+"/api/tarifas",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({instalacion:inst, valor:val})})
.then(function(r){return r.json();}).then(function(d){
b.disabled=false; b.textContent="Guardar";
if(d&&d.ok){ b.textContent="✓"; setTimeout(function(){b.textContent="Guardar";},900); cargarTarifas(); cargarNomina(); }
else alert((d&&d.error)||"Error al guardar.");
}).catch(function(){ b.disabled=false; b.textContent="Guardar"; alert("Error de conexión."); });
});
});
}).catch(function(){ document.getElementById("tarBody").innerHTML='<tr><td colspan="3" class="empty">Error al cargar tarifas.</td></tr>'; });
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
