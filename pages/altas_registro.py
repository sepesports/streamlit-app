# pages/altas_registro.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Registro de Personal")

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
<h1>Registro de Personal</h1>
<div class="mobile-logo"><img src="__LOGO_URL__"/>SYNTRA</div>
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
function goToPage(path){ window.open(path + qs(), "syntra_main"); }

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
if (lo) lo.addEventListener("click", function(){ window.open("/admin", "syntra_main"); });
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

components.html(html, height=980, scrolling=True)
