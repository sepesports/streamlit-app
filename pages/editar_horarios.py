# pages/editar_horarios.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gestion de Horarios", layout="wide")

query_params = st.query_params
AUTH_USER = query_params.get("usuario") or query_params.get("user") or ""
AUTH_ROLE = query_params.get("rol") or query_params.get("role") or ""
AUTH_DNI = query_params.get("dni") or ""
NORMALIZED_ROLE = AUTH_ROLE.strip().lower()

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

if NORMALIZED_ROLE != "administrador":
          st.markdown(
                        """
                                <script>
                                          window.location.href="/?auth=ok";
                                                  </script>
                                                          """,
                        unsafe_allow_html=True,
          )
          st.stop()

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
.loading-row td{text-align:center;color:var(--muted);padding:24px;}

@media (max-width:768px){
#sidebar{display:none;}
.hamburger{display:block;}
.mobile-logo{display:flex;}
#topbar h1{display:none;}
#topbar{padding:14px 16px;}
#content{padding:14px 12px 90px 12px;}
table{font-size:12px;}
thead th, tbody td{padding:9px 10px;}
}

.mobile-drawer{display:none;position:fixed;inset:0;z-index:100;}
.mobile-drawer.open{display:block;}
.mobile-drawer .overlay{position:absolute;inset:0;background:rgba(0,0,0,.4);}
.mobile-drawer .panel{
position:absolute;left:0;top:0;bottom:0;width:250px;
background:linear-gradient(180deg,var(--navy1) 0%,var(--navy2) 60%,var(--navy3) 100%);
padding:26px 18px;color:#eaf2ff;overflow-y:auto;
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
<h1>Gesti&oacute;n de Horarios</h1>
<div class="mobile-logo"><img src="__LOGO_URL__"/>SYNTRA</div>
<button class="primary-btn" id="addBtn">+ Nueva Asignaci&oacute;n</button>
</div>
<div id="content">
<div class="tabbar">
<button class="tabbtn active" data-tab="bloques">Bloques</button>
<button class="tabbtn" data-tab="asignaciones">Asignaciones</button>
<button class="tabbtn" data-tab="historial">Historial</button>
</div>

<div class="card" id="panel-bloques">
<table>
<thead><tr><th>Instalaci&oacute;n</th><th>Bloque</th><th>D&iacute;a</th><th>Horario</th><th>Socorristas</th></tr></thead>
<tbody id="bloquesBody"><tr class="loading-row"><td colspan="5">Cargando...</td></tr></tbody>
</table>
<div class="info-bar">Datos reales de la hoja Bloques, agrupados por instalaci&oacute;n + bloque + d&iacute;a. Solo lectura.</div>
</div>

<div class="card" id="panel-asignaciones" style="display:none;">
<table>
<thead><tr><th>Fecha</th><th>Instalaci&oacute;n</th><th>Socorrista</th><th>Ingreso</th><th>Salida</th><th>Estado</th><th></th></tr></thead>
<tbody id="asigBody"><tr class="loading-row"><td colspan="7">Cargando...</td></tr></tbody>
</table>
<div class="info-bar">Turnos desde hoy en adelante. Edita o elimina cada asignaci&oacute;n.</div>
</div>

<div class="card" id="panel-historial" style="display:none;">
<table>
<thead><tr><th>Fecha</th><th>Instalaci&oacute;n</th><th>Socorrista</th><th>Ingreso</th><th>Salida</th><th>Estado</th></tr></thead>
<tbody id="histBody"><tr class="loading-row"><td colspan="6">Cargando...</td></tr></tbody>
</table>
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

<div class="modal-overlay" id="addModal">
<div class="modal">
<h3>Nueva asignaci&oacute;n desde bloque</h3>
<div class="field"><label>Fecha</label><input id="add_fecha" type="date"/></div>
<div class="field"><label>Bloque</label>
<select id="add_bloque"><option value="">Selecciona...</option></select>
</div>
<div class="msg" id="addMsg"></div>
<div class="actions">
<button class="btn-cancel" id="addCancelBtn">Cancelar</button>
<button class="primary-btn" id="addSaveBtn">Agregar</button>
</div>
</div>
</div>

<script>
(function(){
var API_BASE = __API_BASE__;
var AUTH_USER = __AUTH_USER__;
var AUTH_ROLE = __AUTH_ROLE__;
var AUTH_DNI = __AUTH_DNI__;

function qs(){
var p = new URLSearchParams();
p.set("usuario", AUTH_USER);
p.set("rol", AUTH_ROLE);
p.set("dni", AUTH_DNI);
return "?" + p.toString();
}
function goToPage(path){ window.top.location.href = path + qs(); }

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
if (lo) lo.addEventListener("click", function(){ window.top.location.href = "/admin"; });
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

fetch(API_BASE + "/api/bloques")
.then(function(r){ return r.json(); })
.then(function(d){
var tbody = document.getElementById("bloquesBody");
if (!d || !d.ok || !d.rows || !d.rows.length){
tbody.innerHTML = '<tr class="empty-row"><td colspan="5">Sin datos de bloques.</td></tr>';
return;
}
var groups = {};
d.rows.forEach(function(r){
var inst = (r["Instalacion"] || "").trim();
var bloque = (r["bloque"] || "").trim();
var dia = (r["Dia"] || "").trim();
var ingreso = (r["Ingreso"] || "").trim();
var key = inst + "|" + bloque + "|" + dia;
if (!groups[key]) groups[key] = {inst:inst, bloque:bloque, dia:dia, horas:[], count:0};
if (ingreso) groups[key].horas.push(ingreso);
groups[key].count += 1;
});
var rows = Object.keys(groups).map(function(k){ return groups[k]; });
rows.sort(function(a,b){
if (a.inst !== b.inst) return a.inst.localeCompare(b.inst);
return a.bloque.localeCompare(b.bloque);
});
tbody.innerHTML = rows.map(function(g){
var horas = g.horas.slice().sort();
var rango = horas.length ? (horas[0] + " - " + horas[horas.length-1]) : "-";
return "<tr><td>" + g.inst + "</td><td>Bloque " + g.bloque + "</td><td>" + g.dia + "</td><td>" + rango + "</td><td>" + g.count + "</td></tr>";
}).join("");

var sel = document.getElementById("add_bloque");
var bloqueSet = {};
d.rows.forEach(function(r){ bloqueSet[(r["bloque"]||"").trim()] = true; });
Object.keys(bloqueSet).sort().forEach(function(b){
if (!b) return;
var opt = document.createElement("option");
opt.value = b;
opt.textContent = "Bloque " + b;
sel.appendChild(opt);
});
})
.catch(function(){
document.getElementById("bloquesBody").innerHTML = '<tr class="empty-row"><td colspan="5">Error al cargar bloques.</td></tr>';
});

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
addModal.classList.add("open");
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
setTimeout(function(){ addModal.classList.remove("open"); loadMallas(); }, 800);
} else {
msgEl.className = "msg err"; msgEl.textContent = (d && d.error) || "Error al agregar.";
}
})
.catch(function(){ msgEl.className = "msg err"; msgEl.textContent = "Error de conexi&oacute;n."; });
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

components.html(html, height=1000, scrolling=True)
