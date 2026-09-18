# pages/altas_registro.py
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

st.set_page_config(layout="wide", page_title="Registro de Personal")
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
.nav-item{
display:flex;align-items:center;gap:12px;padding:11px 12px;border-radius:10px;margin-bottom:4px;
color:rgba(234,242,255,.82);font-size:14.5px;font-weight:600;cursor:pointer;position:relative;
}
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
.save-btn{background:var(--blue);color:#fff;border:none;border-radius:10px;padding:10px 18px;font-size:13.5px;font-weight:700;cursor:pointer;}
.save-btn:hover{background:#1e4fb8;}
.save-btn[disabled]{opacity:.6;cursor:not-allowed;}
#content{padding:26px 30px 90px 30px;max-width:900px;}
.card{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:26px 28px;}
.card h2{font-size:16px;margin:0 0 18px 0;font-weight:700;}
.field-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px 18px;margin-bottom:22px;}
.field-grid.full{grid-template-columns:1fr;}
.field label{display:block;font-size:12.5px;color:var(--muted);margin-bottom:6px;font-weight:600;}
.field input, .field select{
width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:10px;
font-size:13.5px;color:var(--ink);background:#fbfcfe;
}
.field input:focus, .field select:focus{outline:none;border-color:var(--blue);}
.section-title{font-size:12.5px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin:0 0 12px 0;}
.actions-row{display:flex;justify-content:flex-end;gap:10px;margin-top:6px;}
.cancel-btn{background:#fff;color:var(--ink);border:1px solid var(--border);border-radius:10px;padding:10px 18px;font-size:13.5px;font-weight:700;cursor:pointer;}
.msg{font-size:13px;margin-top:14px;padding:10px 14px;border-radius:10px;display:none;}
.msg.ok{background:#e6f7ee;color:#1a7f4f;display:block;}
.msg.err{background:#fde8e8;color:#b02a2a;display:block;}

@media (max-width:768px){
#sidebar{display:none;}
.hamburger{display:block;}
.mobile-logo{display:flex;}
#topbar h1{display:none;}
#topbar{padding:14px 16px;}
#content{padding:16px 14px 90px 14px;}
.field-grid{grid-template-columns:1fr;}
.card{padding:18px 16px;}
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
</style>
</head>
<body>
<div id="app">
<div id="sidebar"><div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:40px;width:auto;flex:0 0 auto;display:block;object-fit:contain;"/></div><div id="navList"></div></div>
<div class="mobile-drawer" id="drawer">
<div class="overlay" id="drawerOverlay"></div>
<div class="panel"><div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:40px;width:auto;flex:0 0 auto;display:block;object-fit:contain;"/></div><div id="navListMobile"></div></div>
</div>
<div id="main">
<div id="topbar">
<button class="hamburger" id="hamburgerBtn">&#9776;</button>
<h1>Registro de Personal</h1>
<div class="mobile-logo"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:40px;width:auto;flex:0 0 auto;display:block;object-fit:contain;"/></div>
<button class="save-btn" id="saveBtn">Guardar</button>
</div>
<div id="content">
<div class="card">
<p class="section-title">Datos personales</p>
<div class="field-grid">
<div class="field"><label>Nombre completo</label><input id="f_nombre" placeholder="Mar&iacute;a Fern&aacute;ndez L&oacute;pez"/></div>
<div class="field"><label>DNI</label><input id="f_dni" placeholder="12345678B"/></div>
<div class="field"><label>Correo electr&oacute;nico</label><input id="f_correo" placeholder="maria.fernandez@syntra.com"/></div>
<div class="field"><label>Tel&eacute;fono</label><input id="f_telefono" placeholder="600 123 456"/></div>
<div class="field"><label>Fecha de nacimiento</label><input id="f_nacimiento" type="date"/></div>
</div>
<p class="section-title">Informaci&oacute;n laboral</p>
<div class="field-grid">
<div class="field"><label>Instalaci&oacute;n</label>
<select id="f_instalacion">
<option value="">Selecciona...</option>
<option>Playa Norte</option>
<option>Playa Sur</option>
<option>Piscina Municipal</option>
<option>Centro Deportivo</option>
</select>
</div>
<div class="field"><label>Tipo de contrato</label>
<select id="f_contrato">
<option value="">Selecciona...</option>
<option>Fijo</option>
<option>Temporal</option>
<option>Media jornada</option>
</select>
</div>
<div class="field"><label>Fecha de inicio</label><input id="f_fecha_inicio" type="date"/></div>
<div class="field"><label>Rol</label>
<select id="f_rol">
<option value="">Selecciona...</option>
<option value="Socorrista">Socorrista</option>
<option value="Directivo">Directivo</option>
<option value="Administrador">Administrador</option>
</select>
</div>
</div>
<div class="msg" id="formMsg"></div>
<div class="actions-row">
<button class="cancel-btn" id="cancelBtn">Cancelar</button>
<button class="save-btn" id="saveBtn2">Guardar</button>
</div>
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
{label:"Registro", icon:"&#128100;+", go:"/altas_registro", active:true, badge:"Solo admin"},
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

document.getElementById("cancelBtn").addEventListener("click", function(){ goToPage("/"); });

function showMsg(text, ok){
var el = document.getElementById("formMsg");
el.textContent = text;
el.className = "msg " + (ok ? "ok" : "err");
}

function submitForm(){
var nombre = document.getElementById("f_nombre").value.trim();
var dni = document.getElementById("f_dni").value.trim();
var correo = document.getElementById("f_correo").value.trim();
var telefono = document.getElementById("f_telefono").value.trim();
var nacimiento = document.getElementById("f_nacimiento").value;
var instalacion = document.getElementById("f_instalacion").value;
var contrato = document.getElementById("f_contrato").value;
var fecha_inicio = document.getElementById("f_fecha_inicio").value;
var rol = document.getElementById("f_rol").value;

if (!nombre || !dni){
showMsg("Nombre y DNI son obligatorios.", false);
return;
}

var payload = {
nombre: nombre,
dni: dni,
correo: correo,
tlf: telefono,
nacimiento: nacimiento,
instalacion: instalacion,
contrato: contrato,
fecha_inicio: fecha_inicio,
rol: rol
};

var btns = document.querySelectorAll(".save-btn");
btns.forEach(function(b){ b.disabled = true; b.textContent = "Guardando..."; });

fetch(API_BASE + "/api/altas/registro", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify(payload)
})
.then(function(r){ return r.json(); })
.then(function(d){
btns.forEach(function(b){ b.disabled = false; b.textContent = "Guardar"; });
if (d && d.ok){
showMsg("Personal registrado correctamente.", true);
setTimeout(function(){ goToPage("/"); }, 1200);
} else {
showMsg((d && d.error) || "Error al guardar.", false);
}
})
.catch(function(){
btns.forEach(function(b){ b.disabled = false; b.textContent = "Guardar"; });
showMsg("Error de conexi&oacute;n con el servidor.", false);
});
}

document.getElementById("saveBtn").addEventListener("click", submitForm);
document.getElementById("saveBtn2").addEventListener("click", submitForm);
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

components.html(html, height=980, scrolling=True)
