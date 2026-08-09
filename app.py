# app.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="SYNTRA")

# GATE: solo entra con ?auth=ok
if st.query_params.get("auth") != "ok":
        st.markdown(
                    """
                            <script>
                                      window.location.href="/admin";
                                              </script>
                                                      """,
                    unsafe_allow_html=True,
        )
        st.stop()

USER_NAME = st.query_params.get("usuario") or st.query_params.get("user") or "Usuario"
USER_ROLE = st.query_params.get("rol") or st.query_params.get("role") or ""
USER_DNI = st.query_params.get("dni") or ""
NORMALIZED_ROLE = USER_ROLE.strip().lower()

CAN_MANAGE_SCHEDULES = NORMALIZED_ROLE == "administrador"
CAN_REGISTER_USERS = NORMALIZED_ROLE == "administrador"

ROLE_LABELS = {
        "administrador": "Administrador",
        "directivo": "Directivo",
        "socorrista": "Socorrista",
}
ROLE_DISPLAY = ROLE_LABELS.get(NORMALIZED_ROLE, USER_ROLE or "Usuario")

API_BASE = "https://camilo27.pythonanywhere.com"

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


LOGO_URL = "https://files.catbox.moe/056m6v.jpg"

html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
:root{
--navy1: #0a1a55;
--navy2: #040e31;
--navy3: #02071c;
--blue: #2f6fe0;
--blue-dark: #1e4fb8;
--bg: #f3f5f9;
--card-bg: #ffffff;
--ink: #0f1b3d;
--muted: #6b7688;
--border: #e7eaf1;
--pill-bg: #e8f0fe;
--pill-ink: #2f6fe0;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;width:100%;font-family:"Segoe UI",Arial,Helvetica,sans-serif;background:var(--bg);color:var(--ink);}
#app{display:flex;min-height:100vh;width:100%;}
#sidebar{
width:250px;flex:0 0 250px;
background:linear-gradient(180deg,var(--navy1) 0%,var(--navy2) 60%,var(--navy3) 100%);
color:#eaf2ff;display:flex;flex-direction:column;
padding:26px 18px;min-height:100vh;
}
.logo-row{display:flex;align-items:center;gap:10px;margin-bottom:34px;padding:0 4px;}
.logo-row img{width:34px;height:34px;object-fit:contain;border-radius:6px;}
.logo-row span{font-weight:800;letter-spacing:2px;font-size:19px;}
.nav-item{
display:flex;align-items:center;gap:12px;
padding:11px 12px;border-radius:10px;margin-bottom:4px;
color:rgba(234,242,255,.82);font-size:14.5px;font-weight:600;
cursor:pointer;text-decoration:none;transition:background .15s;
position:relative;
}
.nav-item:hover{background:rgba(255,255,255,.06);}
.nav-item.active{background:var(--blue);color:#fff;}
.nav-item.disabled{opacity:.5;cursor:not-allowed;}
.nav-badge{
margin-left:auto;font-size:10px;font-weight:700;background:rgba(255,255,255,.14);
padding:2px 7px;border-radius:20px;white-space:nowrap;
}
.nav-sep{height:1px;background:rgba(255,255,255,.10);margin:14px 4px;}
.nav-bottom{margin-top:auto;}
#main{flex:1;min-width:0;display:flex;flex-direction:column;}
#topbar{
background:#fff;border-bottom:1px solid var(--border);
padding:18px 30px;display:flex;align-items:center;justify-content:space-between;
}
#topbar .greet h1{font-size:22px;margin:0 0 4px 0;font-weight:700;}
#topbar .greet p{margin:0;color:var(--muted);font-size:13.5px;}
#topbar .right{display:flex;align-items:center;gap:14px;}
.bell{position:relative;font-size:20px;color:var(--ink);cursor:pointer;}
.bell .dot{
position:absolute;top:-4px;right:-6px;background:#e0433f;color:#fff;
font-size:10px;font-weight:800;border-radius:20px;padding:1px 5px;
}
.mobile-logo{display:none;align-items:center;gap:8px;font-weight:800;letter-spacing:1px;}
.mobile-logo img{width:26px;height:26px;border-radius:6px;object-fit:contain;}
.hamburger{display:none;font-size:20px;background:none;border:none;cursor:pointer;color:var(--ink);}
#content{padding:26px 30px 100px 30px;}
#content h2{font-size:16px;margin:0 0 16px 0;font-weight:700;color:var(--ink);}
.cards-grid{
display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:22px;
}
.qa-card{
background:var(--card-bg);border:1px solid var(--border);border-radius:16px;
padding:20px 18px;display:flex;flex-direction:column;gap:10px;
box-shadow:0 1px 3px rgba(20,30,60,.04);
}
.qa-icon{
width:44px;height:44px;border-radius:12px;background:var(--pill-bg);
display:flex;align-items:center;justify-content:center;font-size:20px;color:var(--blue);
}
.qa-card h3{margin:2px 0 0 0;font-size:15px;font-weight:700;color:var(--ink);}
.qa-card p{margin:0;font-size:12.5px;color:var(--muted);line-height:1.4;min-height:32px;}
.qa-pill{
align-self:flex-start;background:var(--pill-bg);color:var(--pill-ink);
font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:20px;
}
.qa-btn{
margin-top:auto;background:var(--navy2);color:#fff;border:none;border-radius:10px;
padding:10px 14px;font-size:13px;font-weight:700;cursor:pointer;
display:flex;align-items:center;justify-content:center;gap:6px;
}
.qa-btn:hover{background:var(--navy1);}
.qa-btn[disabled]{background:#c7cbd6;cursor:not-allowed;}
.kpi-row{
background:var(--card-bg);border:1px solid var(--border);border-radius:16px;
display:grid;grid-template-columns:repeat(4,1fr);padding:18px 10px;
}
.kpi-item{display:flex;align-items:center;gap:12px;padding:0 16px;}
.kpi-item + .kpi-item{border-left:1px solid var(--border);}
.kpi-icon{font-size:20px;color:var(--blue);width:26px;text-align:center;}
.kpi-item .lab{font-size:11.5px;color:var(--muted);margin:0 0 2px 0;}
.kpi-item .val{font-size:20px;font-weight:800;color:var(--ink);margin:0;}
#bottomnav{display:none;}
@media (max-width: 900px){
.cards-grid{grid-template-columns:repeat(2,1fr);}
.kpi-row{grid-template-columns:repeat(2,1fr);row-gap:14px;}
.kpi-item:nth-child(3){border-left:none;}
}
@media (max-width: 768px){
#sidebar{display:none;}
.hamburger{display:block;}
.mobile-logo{display:flex;}
#topbar .greet{display:none;}
#topbar{padding:14px 16px;}
#content{padding:16px 14px 90px 14px;}
.cards-grid{grid-template-columns:1fr 1fr;gap:10px;}
.qa-card{padding:14px 12px;}
.qa-card p{min-height:0;}
.kpi-row{grid-template-columns:repeat(2,1fr);gap:12px;padding:14px 10px;}
.kpi-item:nth-child(3){border-left:none;}
#bottomnav{
display:flex;position:fixed;left:0;right:0;bottom:0;height:60px;
background:#fff;border-top:1px solid var(--border);z-index:50;
}
#bottomnav .bn-item{
flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
gap:3px;font-size:10.5px;color:var(--muted);cursor:pointer;font-weight:600;
}
#bottomnav .bn-item.active{color:var(--blue);}
#bottomnav .bn-item .ic{font-size:18px;}
}
.mobile-drawer{
display:none;position:fixed;inset:0;z-index:100;
}
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
<div id="sidebar">
<div class="logo-row"><img src="__LOGO_URL__" alt="logo"/><span>SYNTRA</span></div>
<div id="navList"></div>
</div>
<div class="mobile-drawer" id="drawer">
<div class="overlay" id="drawerOverlay"></div>
<div class="panel">
<div class="logo-row"><img src="__LOGO_URL__" alt="logo"/><span>SYNTRA</span></div>
<div id="navListMobile"></div>
</div>
</div>
<div id="main">
<div id="topbar">
<button class="hamburger" id="hamburgerBtn">&#9776;</button>
<div class="greet">
<h1>&iexcl;Bienvenido, __USER_NAME__!</h1>
<p>Rol: __ROLE_DISPLAY__ &bull; DNI: __USER_DNI__</p>
</div>
<div class="mobile-logo"><img src="__LOGO_URL__" alt="logo"/>SYNTRA</div>
<div class="right">
<div class="bell">&#128276;<span class="dot" id="bellDot" style="display:none;">0</span></div>
</div>
</div>
<div id="content">
<h2>Accesos r&aacute;pidos</h2>
<div class="cards-grid" id="cardsGrid"></div>
<div class="kpi-row" id="kpiRow">
<div class="kpi-item"><div class="kpi-icon">&#128101;</div><div><p class="lab">Socorristas</p><p class="val" id="kpiSocorristas">&ndash;</p></div></div>
<div class="kpi-item"><div class="kpi-icon">&#128197;</div><div><p class="lab">Turnos esta semana</p><p class="val" id="kpiTurnos">&ndash;</p></div></div>
<div class="kpi-item"><div class="kpi-icon">&#127970;</div><div><p class="lab">Instalaciones activas</p><p class="val" id="kpiInstalaciones">&ndash;</p></div></div>
<div class="kpi-item"><div class="kpi-icon">&#128172;</div><div><p class="lab">Mensajes no le&iacute;dos</p><p class="val" id="kpiMensajes">&ndash;</p></div></div>
</div>
</div>
</div>
<div id="bottomnav">
<div class="bn-item active"><span class="ic">&#8962;</span>Inicio</div>
<div class="bn-item" data-goto="/calendario"><span class="ic">&#128197;</span>Horarios</div>
<div class="bn-item" data-goto="/chat_interfaz"><span class="ic">&#128172;</span>Chat</div>
<div class="bn-item" id="masBtn"><span class="ic">&#8942;</span>M&aacute;s</div>
</div>
</div>
<script>
(function(){
var API_BASE = __API_BASE__;
var USER_NAME = __USER_NAME_JS__;
var USER_ROLE = __USER_ROLE_JS__;
var USER_DNI = __USER_DNI_JS__;
var CAN_MANAGE_SCHEDULES = __CAN_MANAGE_SCHEDULES__;
var CAN_REGISTER_USERS = __CAN_REGISTER_USERS__;
function qs(params){
var p = new URLSearchParams();
p.set("usuario", USER_NAME);
p.set("rol", USER_ROLE);
p.set("dni", USER_DNI);
return "?" + p.toString();
}
function goToPage(path){
window.open(path + qs(), "_blank") + qs();
}
var NAV_ITEMS = [
{label:"Inicio", icon:"&#8962;", active:true},
{label:"Horarios", icon:"&#128197;", go:"/calendario"},
{label:"Incidencias y Comunicados", icon:"&#128172;", go:"/chat_interfaz"},
{sep:true},
{label:"Registro", icon:"&#128100;+", go:"/altas_registro", adminOnly:true, badge:"Solo admin"},
{label:"Gesti&oacute;n de Horarios", icon:"&#9881;", go:"/editar_horarios", adminOnly:true, badge:"Solo admin"}
];
function renderNav(containerId){
var el = document.getElementById(containerId);
var htmlParts = [];
NAV_ITEMS.forEach(function(item){
if (item.sep){ htmlParts.push('<div class="nav-sep"></div>'); return; }
var locked = item.adminOnly && !CAN_MANAGE_SCHEDULES && !(item.label === "Registro" && CAN_REGISTER_USERS);
var cls = "nav-item" + (item.active ? " active" : "") + (locked ? " disabled" : "");
var badge = item.badge ? '<span class="nav-badge">' + item.badge + '</span>' : "";
htmlParts.push(
'<div class="' + cls + '" data-go="' + (item.go || "") + '" data-locked="' + (locked ? "1":"0") + '">' +
'<span>' + item.icon + '</span><span>' + item.label + '</span>' + badge +
'</div>'
);
});
htmlParts.push('<div class="nav-bottom"><div class="nav-item" id="logoutBtn_' + containerId + '"><span>&#8630;</span><span>Cerrar sesi&oacute;n</span></div></div>');
el.innerHTML = htmlParts.join("");
el.querySelectorAll(".nav-item[data-go]").forEach(function(node){
node.addEventListener("click", function(){
if (node.getAttribute("data-locked") === "1") return;
var go = node.getAttribute("data-go");
if (go) goToPage(go);
});
});
var lo = document.getElementById("logoutBtn_" + containerId);
if (lo) lo.addEventListener("click", function(){ window.parent.location.href = "/admin"; });
}
renderNav("navList");
renderNav("navListMobile");
var CARDS = [
{
icon:"&#128197;", title:"Horarios", desc:"Consulta tus turnos y horarios asignados.",
btn:"Ver horarios &rarr;", go:"/calendario", locked:false
},
{
icon:"&#128172;", title:"Incidencias y Comunicados", desc:"Comun&iacute;cate con tu equipo o por instalaciones.",
btn:"Abrir chat &rarr;", go:"/chat_interfaz", locked:false
},
{
icon:"&#128100;+", title:"Registro de Personal", desc:"Registra nuevos socorristas y personal.",
btn:"Ir al registro &rarr;", go:"/altas_registro", locked:!CAN_REGISTER_USERS, pill:"Solo administradores"
},
{
icon:"&#9881;", title:"Gesti&oacute;n de Horarios", desc:"Crear, editar o eliminar bloques de turnos.",
btn:"Gestionar &rarr;", go:"/editar_horarios", locked:!CAN_MANAGE_SCHEDULES, pill:"Solo administradores"
}
];
var grid = document.getElementById("cardsGrid");
CARDS.forEach(function(c){
var div = document.createElement("div");
div.className = "qa-card";
div.innerHTML =
'<div class="qa-icon">' + c.icon + '</div>' +
'<h3>' + c.title + '</h3>' +
'<p>' + c.desc + '</p>' +
(c.pill ? '<span class="qa-pill">' + c.pill + '</span>' : '') +
'<button class="qa-btn"' + (c.locked ? ' disabled' : '') + '>' + c.btn + '</button>';
if (!c.locked){
div.querySelector(".qa-btn").addEventListener("click", function(){ goToPage(c.go); });
}
grid.appendChild(div);
});
var drawer = document.getElementById("drawer");
var hamburgerBtn = document.getElementById("hamburgerBtn");
var drawerOverlay = document.getElementById("drawerOverlay");
if (hamburgerBtn) hamburgerBtn.addEventListener("click", function(){ drawer.classList.add("open"); });
if (drawerOverlay) drawerOverlay.addEventListener("click", function(){ drawer.classList.remove("open"); });
document.querySelectorAll("#bottomnav .bn-item[data-goto]").forEach(function(node){
node.addEventListener("click", function(){ goToPage(node.getAttribute("data-goto")); });
});
var masBtn = document.getElementById("masBtn");
if (masBtn) masBtn.addEventListener("click", function(){ drawer.classList.add("open"); });
fetch(API_BASE + "/api/dashboard?dni=" + encodeURIComponent(USER_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
if (!d || !d.ok) return;
document.getElementById("kpiSocorristas").textContent = d.total_socorristas;
document.getElementById("kpiTurnos").textContent = d.turnos_semana;
document.getElementById("kpiInstalaciones").textContent = d.instalaciones_activas;
document.getElementById("kpiMensajes").textContent = d.mensajes_no_leidos;
if (d.mensajes_no_leidos > 0){
var dot = document.getElementById("bellDot");
dot.style.display = "inline-block";
dot.textContent = d.mensajes_no_leidos;
}
})
.catch(function(){});
})();
</script>
</body>
</html>
"""

html = (
        html.replace("__LOGO_URL__", LOGO_URL)
            .replace("__USER_NAME__", USER_NAME)
            .replace("__ROLE_DISPLAY__", ROLE_DISPLAY)
            .replace("__USER_DNI__", USER_DNI or "-")
            .replace("__API_BASE__", _js_str(API_BASE))
            .replace("__USER_NAME_JS__", _js_str(USER_NAME))
            .replace("__USER_ROLE_JS__", _js_str(USER_ROLE))
            .replace("__USER_DNI_JS__", _js_str(USER_DNI))
            .replace("__CAN_MANAGE_SCHEDULES__", "true" if CAN_MANAGE_SCHEDULES else "false")
            .replace("__CAN_REGISTER_USERS__", "true" if CAN_REGISTER_USERS else "false")
)

components.html(html, height=980, scrolling=True)
