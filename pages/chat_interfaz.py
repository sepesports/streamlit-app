# pages/chat_interfaz.py
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

st.set_page_config(page_title="Incidencias y Comunicados", layout="wide")
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
html,body{margin:0;padding:0;width:100%;height:100%;font-family:"Segoe UI",Arial,Helvetica,sans-serif;background:var(--bg);color:var(--ink);}
#app{display:flex;height:100vh;width:100%;}
#sidebar{
width:250px;flex:0 0 250px;
background:linear-gradient(180deg,var(--navy1) 0%,var(--navy2) 60%,var(--navy3) 100%);
color:#eaf2ff;display:flex;flex-direction:column;padding:26px 18px;height:100vh;overflow-y:auto;
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

#main{flex:1;min-width:0;display:flex;flex-direction:column;height:100vh;}
#topbar{background:#fff;border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex:0 0 auto;}
#topbar h1{font-size:18px;margin:0;font-weight:700;}
.hamburger{display:none;font-size:20px;background:none;border:none;cursor:pointer;color:var(--ink);}
.mobile-logo{display:none;align-items:center;gap:8px;font-weight:800;letter-spacing:1px;}
.mobile-logo img{width:26px;height:26px;border-radius:6px;object-fit:contain;}

#chatBody{flex:1;min-height:0;display:flex;}

#listPanel{width:340px;flex:0 0 340px;border-right:1px solid var(--border);background:#fff;display:flex;flex-direction:column;}
.list-tabs{display:flex;align-items:flex-start;gap:13px;padding:14px 12px 0 12px;border-bottom:1px solid var(--border);}
.list-tab{padding:0 0 12px 0;font-size:12px;font-weight:700;color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap;flex:0 0 auto;}
.list-tab.active{color:var(--blue);border-bottom-color:var(--blue);}
.new-btn{margin-left:auto;background:var(--blue);color:#fff;border:none;border-radius:8px;padding:5px 10px;font-size:11.5px;font-weight:700;cursor:pointer;align-self:flex-start;white-space:nowrap;flex:0 0 auto;}
.search-box{margin:12px 16px;padding:8px 12px;border:1px solid var(--border);border-radius:10px;font-size:13px;width:calc(100% - 32px);}
#threadList, #instList{flex:1;overflow-y:auto;padding:0 8px 8px 8px;}
.thread-item{display:flex;gap:10px;align-items:flex-start;padding:12px 10px;border-radius:12px;cursor:pointer;}
.thread-item:hover{background:#f5f7fb;}
.thread-item.active{background:#eaf1ff;}
.thread-avatar{width:38px;height:38px;border-radius:10px;background:var(--navy2);color:#fff;display:flex;align-items:center;justify-content:center;font-size:16px;flex:0 0 38px;}
.thread-info{flex:1;min-width:0;}
.thread-title{font-size:13.5px;font-weight:700;display:flex;justify-content:space-between;gap:6px;}
.thread-sub{font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.thread-time{font-size:10.5px;color:var(--muted);white-space:nowrap;}
.unread-dot{background:var(--blue);color:#fff;border-radius:20px;font-size:10.5px;font-weight:700;padding:1px 7px;flex:0 0 auto;}
.inst-item{display:flex;align-items:center;gap:10px;padding:12px 12px;border-radius:12px;cursor:pointer;}
.inst-item:hover{background:#f5f7fb;}
.inst-icon{width:38px;height:38px;border-radius:10px;background:#eef4ff;color:var(--blue);display:flex;align-items:center;justify-content:center;font-size:17px;flex:0 0 38px;}
.inst-name{font-size:13.5px;font-weight:700;}
.inst-count{font-size:11.5px;color:var(--muted);}
.empty-note{padding:24px;color:var(--muted);font-size:13px;text-align:center;}

#threadPanel{flex:1;min-width:0;display:flex;flex-direction:column;background:#fbfcfe;}
#threadHeader{padding:14px 22px;border-bottom:1px solid var(--border);background:#fff;display:flex;align-items:center;gap:12px;flex:0 0 auto;}
.back-btn{display:none;background:none;border:none;font-size:18px;cursor:pointer;color:var(--ink);}
#threadHeaderTitle{font-size:15px;font-weight:700;}
#threadHeaderSub{font-size:11.5px;color:var(--muted);}
#messagesWrap{flex:1;min-height:0;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:12px;}
.msg-row{display:flex;flex-direction:column;max-width:70%;}
.msg-row.mine{align-self:flex-end;align-items:flex-end;}
.msg-sender{font-size:11px;color:var(--muted);margin-bottom:3px;padding:0 4px;}
.msg-bubble{background:#fff;border:1px solid var(--border);border-radius:14px 14px 14px 4px;padding:10px 14px;font-size:13.5px;line-height:1.4;}
.msg-row.mine .msg-bubble{background:var(--blue);color:#fff;border-color:var(--blue);border-radius:14px 14px 4px 14px;}
.msg-time{font-size:10px;color:var(--muted);margin-top:3px;padding:0 4px;}
#composer{padding:14px 22px;border-top:1px solid var(--border);background:#fff;display:flex;align-items:center;gap:10px;flex:0 0 auto;}
#msgInput{flex:1;padding:11px 14px;border:1px solid var(--border);border-radius:24px;font-size:13.5px;}
#msgInput:focus{outline:none;border-color:var(--blue);}
.send-btn{width:40px;height:40px;border-radius:50%;background:var(--blue);color:#fff;border:none;cursor:pointer;font-size:16px;flex:0 0 40px;}
.send-btn:disabled{opacity:.5;cursor:not-allowed;}
.placeholder-panel{flex:1;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:13.5px;}

.mobile-drawer{display:none;position:fixed;inset:0;z-index:100;}
.mobile-drawer.open{display:block;}
.mobile-drawer .overlay{position:absolute;inset:0;background:rgba(0,0,0,.4);}
.mobile-drawer .panel{
position:absolute;left:0;top:0;bottom:0;width:250px;
background:linear-gradient(180deg,var(--navy1) 0%,var(--navy2) 60%,var(--navy3) 100%);
padding:26px 18px;color:#eaf2ff;overflow-y:auto;
}

@media (max-width:768px){
#sidebar{display:none;}
.hamburger{display:block;}
.mobile-logo{display:flex;}
#topbar{padding:12px 14px;}
#topbar h1{display:none;}
#listPanel{width:100%;flex:1 1 auto;border-right:none;}
#threadPanel{display:none;}
#chatBody.thread-open #listPanel{display:none;}
#chatBody.thread-open #threadPanel{display:flex;}
.back-btn{display:block;}
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
/* ===== Grupos, integrantes y foto de perfil ===== */
.avatar-img{width:100%;height:100%;object-fit:cover;border-radius:inherit;display:block;}
.me-row{display:flex;align-items:center;gap:10px;padding:10px 16px 4px 16px;}
.me-av{width:38px;height:38px;border-radius:12px;background:var(--navy2);color:#fff;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;overflow:hidden;cursor:pointer;flex:0 0 38px;position:relative;}
.me-av .cam{position:absolute;right:-2px;bottom:-2px;background:#1F4FD8;color:#fff;border-radius:50%;width:16px;height:16px;font-size:9px;display:flex;align-items:center;justify-content:center;border:2px solid #fff;}
.me-name{font-size:13px;font-weight:700;}
.me-hint{font-size:11px;color:var(--muted);}
.thread-tag{font-size:9.5px;font-weight:800;letter-spacing:.3px;padding:2px 6px;border-radius:99px;background:#eaf1ff;color:#1F4FD8;text-transform:uppercase;margin-left:6px;}
#modalBack{position:fixed;inset:0;background:rgba(5,12,32,.55);z-index:10050;display:none;align-items:flex-end;justify-content:center;}
#modalBack.open{display:flex;}
#modalCard{background:#fff;width:100%;max-width:520px;border-radius:16px 16px 0 0;max-height:86vh;display:flex;flex-direction:column;overflow:hidden;}
#modalHead{padding:14px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
#modalHead b{font-size:15px;}
#modalClose{background:none;border:0;font-size:22px;line-height:1;cursor:pointer;color:var(--muted);}
#modalBody{padding:14px 16px;overflow-y:auto;flex:1;}
#modalFoot{padding:12px 16px;border-top:1px solid var(--border);display:flex;gap:10px;justify-content:flex-end;}
.modal-input{width:100%;padding:11px 13px;border:1px solid var(--border);border-radius:10px;font-size:14px;margin-bottom:12px;}
.modal-btn{background:var(--blue);color:#fff;border:0;border-radius:10px;padding:10px 18px;font-size:13.5px;font-weight:700;cursor:pointer;}
.modal-btn.ghost{background:#eef2fa;color:var(--ink);}
.modal-btn:disabled{opacity:.5;cursor:not-allowed;}
.pick{display:flex;align-items:center;gap:10px;padding:9px 6px;border-bottom:1px solid var(--border);cursor:pointer;}
.pick:last-child{border-bottom:none;}
.pick input{width:18px;height:18px;}
.pick .pav, .mem-row .pav{width:32px;height:32px;border-radius:10px;background:var(--navy2);color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;overflow:hidden;flex:0 0 32px;}
.pick .pname{font-size:13.5px;font-weight:600;}
.pick .prole{font-size:11px;color:var(--muted);}
.mem-row{display:flex;align-items:center;gap:10px;padding:9px 4px;border-bottom:1px solid var(--border);}
.mem-row:last-child{border-bottom:none;}
.mem-x{margin-left:auto;background:#ffeceb;color:#d33;border:0;border-radius:8px;padding:5px 10px;font-size:11.5px;font-weight:700;cursor:pointer;}
.mem-owner{margin-left:auto;font-size:10.5px;font-weight:800;color:var(--blue);background:#eaf1ff;padding:3px 8px;border-radius:99px;}
.head-btn{margin-left:auto;background:#eef2fa;border:0;border-radius:9px;padding:7px 11px;font-size:12px;font-weight:700;color:var(--ink);cursor:pointer;}
/* ===== Adjuntos y tiempo real ===== */
.att-btn{width:40px;height:40px;border-radius:50%;background:#eef2fa;color:#1B2A4A;border:none;cursor:pointer;font-size:17px;flex:0 0 40px;display:flex;align-items:center;justify-content:center;}
.att-btn:hover{background:#e0e7f5;}
.att-btn:disabled{opacity:.5;cursor:not-allowed;}
.att-btn.rec{background:#e5484d;color:#fff;animation:recPulse 1.2s infinite;}
@keyframes recPulse{0%{box-shadow:0 0 0 0 rgba(229,72,77,.5);}70%{box-shadow:0 0 0 10px rgba(229,72,77,0);}100%{box-shadow:0 0 0 0 rgba(229,72,77,0);}}
#recInfo{font-size:12px;color:#e5484d;font-weight:700;white-space:nowrap;}
.msg-img{display:block;width:240px;max-width:100%;height:auto;max-height:260px;border-radius:10px;cursor:pointer;object-fit:cover;background:#eef2fa;}
.msg-audio{display:block;width:240px;max-width:100%;height:40px;}
.msg-bubble.has-att{padding:6px;}
#imgViewer{position:fixed;inset:0;background:rgba(2,7,28,.85);z-index:10000;display:none;align-items:center;justify-content:center;padding:16px;}
#imgViewer.open{display:flex;}
#imgViewer img{max-width:100%;max-height:100%;border-radius:8px;}
@media (max-width:768px){.msg-row{max-width:85%;}.msg-img{width:200px;}.msg-audio{width:200px;}#composer{padding:10px 12px;gap:6px;}}
/* ===== Asistente IA (overlay aislado) ===== */
#iaFab{position:fixed;right:18px;bottom:96px;width:56px;height:56px;border-radius:50%;background:#1B2A4A;color:#fff;border:none;box-shadow:0 6px 18px rgba(27,42,74,.35);font-size:24px;cursor:pointer;z-index:9999;display:flex;align-items:center;justify-content:center;}
#iaFab:hover{background:#25366b;}
#iaPanel{position:fixed;right:18px;bottom:162px;width:340px;max-width:calc(100vw - 36px);height:460px;max-height:calc(100vh - 190px);background:#fff;border-radius:14px;box-shadow:0 12px 40px rgba(27,42,74,.28);z-index:9999;display:none;flex-direction:column;overflow:hidden;}
#iaPanel.open{display:flex;}
#iaHead{background:#1B2A4A;color:#fff;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;font-weight:600;font-size:15px;}
#iaClose{background:transparent;border:none;color:#fff;font-size:20px;cursor:pointer;line-height:1;}
#iaBody{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;background:#f4f6fb;}
.ia-msg{max-width:82%;padding:8px 11px;border-radius:12px;font-size:14px;line-height:1.35;white-space:pre-wrap;word-wrap:break-word;}
.ia-user{align-self:flex-end;background:#1B2A4A;color:#fff;border-bottom-right-radius:4px;}
.ia-bot{align-self:flex-start;background:#fff;color:#1B2A4A;border:1px solid #e2e7f2;border-bottom-left-radius:4px;}
.ia-typing{align-self:flex-start;color:#8a93a8;font-size:13px;font-style:italic;}
#iaFoot{display:flex;gap:6px;padding:10px;border-top:1px solid #e2e7f2;background:#fff;}
#iaInput{flex:1;border:1px solid #cfd6e4;border-radius:10px;padding:9px 11px;font-size:14px;outline:none;resize:none;font-family:inherit;}
#iaInput:focus{border-color:#1B2A4A;}
#iaSend{background:#1B2A4A;color:#fff;border:none;border-radius:10px;padding:0 14px;cursor:pointer;font-size:14px;}
#iaSend:disabled{opacity:.5;cursor:default;}
@media (max-width:900px){#iaPanel{right:10px;bottom:150px;width:calc(100vw - 20px);height:calc(100vh - 170px);}#iaFab{right:12px;bottom:84px;}}
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
<h1>Incidencias y Comunicados</h1>
<div class="mobile-logo"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
<div></div>
</div>

<div id="chatBody">
<div id="listPanel">
<div class="list-tabs">
<div class="list-tab active" data-tab="conversaciones">Conversaciones</div>
<div class="list-tab" data-tab="grupos">Grupos</div>
<div class="list-tab" data-tab="instalaciones">Instalaciones</div>
<button class="new-btn" id="newBtn">+ Grupo</button>
</div>
<div class="me-row">
<div class="me-av" id="meAvatar" title="Cambiar foto de perfil"><span id="meAvatarTxt">?</span><span class="cam">&#128247;</span></div>
<div><div class="me-name" id="meName">&nbsp;</div><div class="me-hint">Toca tu foto para cambiarla</div></div>
<input type="file" id="avatarInput" accept="image/*" style="display:none;" />
</div>
<input class="search-box" id="searchBox" placeholder="Buscar conversaciones..." />
<div id="threadList"></div>
<div id="instList" style="display:none;"></div>
</div>

<div id="threadPanel">
<div class="placeholder-panel" id="placeholderPanel">Selecciona una conversaci&oacute;n para empezar.</div>
</div>
</div>
</div>
</div>

<div id="imgViewer"><img id="imgViewerImg" alt=""/></div>

<div id="modalBack">
<div id="modalCard">
<div id="modalHead"><b id="modalTitle">Nuevo grupo</b><button id="modalClose" aria-label="Cerrar">&times;</button></div>
<div id="modalBody"></div>
<div id="modalFoot"></div>
</div>
</div>

<button id="iaFab" title="Asistente IA" aria-label="Asistente IA">&#129302;</button>
<div id="iaPanel" role="dialog" aria-label="Asistente IA">
<div id="iaHead"><span>&#129302; Asistente IA</span><button id="iaClose" aria-label="Cerrar">&times;</button></div>
<div id="iaBody"></div>
<div id="iaFoot">
<textarea id="iaInput" rows="1" placeholder="Escribe tu consulta..."></textarea>
<button id="iaSend">Enviar</button>
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
{label:"Incidencias y Comunicados", icon:"&#128172;", go:"/chat_interfaz", active:true},
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

var threadListEl = document.getElementById("threadList");
var instListEl = document.getElementById("instList");
var chatBody = document.getElementById("chatBody");
var threadPanel = document.getElementById("threadPanel");

var threadsCache = [];
var currentThreadId = null;
var pollTimer = null;
var lastMsgId = {};
var lastReadSent = {};
var renderedThreadId = null;
var mediaRecorder = null;
var recChunks = [];
var recTimer = null;
var recStart = 0;
var ATT_RE = /^\\[\\[adj:(image|audio):(\\/api\\/chat\\/files\\/[0-9]+\\/[a-f0-9]{32}\\.[a-z0-9]+)\\]\\]$/;

function attInfo(body){
var m = ATT_RE.exec((body || "").trim());
if (!m) return null;
return {kind: m[1], url: API_BASE + m[2] + "?user_id=" + encodeURIComponent(AUTH_DNI)};
}

var DIAS_SEM = ["domingo","lunes","martes","mi\u00e9rcoles","jueves","viernes","s\u00e1bado"];

function soloFecha(d){ return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }

function horaCorta(d){
try{
return d.toLocaleTimeString([], {hour:"numeric", minute:"2-digit", hour12:true}).toLowerCase();
}catch(e){
var h = d.getHours(), m = ("0"+d.getMinutes()).slice(-2);
var ap = h >= 12 ? "p. m." : "a. m.";
h = h % 12; if (h === 0) h = 12;
return h + ":" + m + " " + ap;
}
}

/* Fecha y hora claras, en la hora del propio celular */
function timeAgo(iso){
if (!iso) return "";
try{
var d = new Date(iso);
if (isNaN(d.getTime())) return "";
var hoy = soloFecha(new Date());
var dia = soloFecha(d);
var difDias = Math.round((hoy - dia) / 86400000);
if (difDias <= 0) return "Hoy " + horaCorta(d);
if (difDias === 1) return "Ayer " + horaCorta(d);
if (difDias < 7) return DIAS_SEM[d.getDay()] + " " + horaCorta(d);
if (difDias < 14) return "Hace 1 semana";
if (difDias < 31) return "Hace " + Math.floor(difDias / 7) + " semanas";
return ("0"+d.getDate()).slice(-2) + "/" + ("0"+(d.getMonth()+1)).slice(-2) + "/" + d.getFullYear();
}catch(e){ return ""; }
}

function avatarHtml(dni, texto){
var url = API_BASE + "/api/chat/avatar/" + encodeURIComponent(dni || "");
var alt = esc(texto || "?");
return '<img class="avatar-img" src="' + url + '" alt="' + alt + '" data-inicial="' + alt + '"/>';
}

/* si el usuario no tiene foto, se muestran sus iniciales */
document.addEventListener("error", function(e){
var t = e.target;
if (t && t.classList && t.classList.contains("avatar-img")){
var ini = t.getAttribute("data-inicial") || "?";
var padre = t.parentNode;
if (padre){ padre.textContent = ini; }
}
}, true);

function initials(name){
name = (name || "?").trim();
return name.charAt(0).toUpperCase();
}

var vistaLista = "conversaciones";

function renderThreadList(filter){
filter = (filter || "").toLowerCase();
var filtered = threadsCache.filter(function(t){
if (vistaLista === "grupos" && t.type !== "group") return false;
return !filter || (t.title || "").toLowerCase().indexOf(filter) !== -1;
});
if (!filtered.length){
threadListEl.innerHTML = '<div class="empty-note">' + (vistaLista === "grupos" ? 'Todav&iacute;a no tienes grupos. Crea uno con "+ Grupo".' : 'No hay conversaciones.') + '</div>';
return;
}
threadListEl.innerHTML = filtered.map(function(t){
var cls = "thread-item" + (t.id === currentThreadId ? " active" : "");
var unread = t.unread_count > 0 ? '<span class="unread-dot">' + t.unread_count + '</span>' : "";
var subAtt = attInfo(t.last_message);
var sub = subAtt ? (subAtt.kind === "image" ? "&#128247; Imagen" : "&#127908; Nota de voz") : (t.last_message || (t.type === "installation" ? "Instalaci&oacute;n" : "Privado"));
return '<div class="' + cls + '" data-id="' + t.id + '">' +
'<div class="thread-avatar">' + (t.type === "installation" ? "&#127970;" : (t.type === "group" ? "&#128101;" : avatarHtml(t.other_dni || "", initials(t.title)))) + '</div>' +
'<div class="thread-info">' +
'<div class="thread-title"><span>' + esc(t.title) + (t.type === "group" ? '<span class="thread-tag">Grupo</span>' : '') + '</span><span class="thread-time">' + timeAgo(t.last_message_at) + '</span></div>' +
'<div style="display:flex;justify-content:space-between;gap:6px;align-items:center;">' +
'<span class="thread-sub">' + sub + '</span>' + unread +
'</div>' +
'</div>' +
'</div>';
}).join("");
threadListEl.querySelectorAll(".thread-item").forEach(function(node){
node.addEventListener("click", function(){ openThread(node.getAttribute("data-id")); });
});
}

function loadThreads(){
fetch(API_BASE + "/api/chat/threads?user_id=" + encodeURIComponent(AUTH_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
threadsCache = (d && d.ok && d.threads) ? d.threads : [];
renderThreadList(document.getElementById("searchBox").value);
})
.catch(function(){
threadListEl.innerHTML = '<div class="empty-note">Error al cargar conversaciones.</div>';
});
}
loadThreads();

function loadInstallations(){
fetch(API_BASE + "/api/chat/installations?user_id=" + encodeURIComponent(AUTH_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
var list = (d && d.ok && d.installations) ? d.installations : [];
if (!list.length){
instListEl.innerHTML = '<div class="empty-note">Sin instalaciones.</div>';
return;
}
instListEl.innerHTML = list.map(function(i){
return '<div class="inst-item" data-name="' + i.instalacion.replace(/"/g,"&quot;") + '">' +
'<div class="inst-icon">&#127970;</div>' +
'<div><div class="inst-name">' + i.instalacion + '</div><div class="inst-count">' + i.total + ' socorristas</div></div>' +
'</div>';
}).join("");
instListEl.querySelectorAll(".inst-item").forEach(function(node){
node.addEventListener("click", function(){
var name = node.getAttribute("data-name");
fetch(API_BASE + "/api/chat/installation/" + encodeURIComponent(name) + "?user_id=" + encodeURIComponent(AUTH_DNI))
.then(function(r){ return r.json(); })
.then(function(d2){
if (d2 && d2.ok && d2.thread_id){
loadThreads();
setTimeout(function(){ openThread(d2.thread_id); }, 300);
} else {
threadPanel.innerHTML = '<div class="placeholder-panel">No tienes acceso al chat de esta instalaci&oacute;n.</div>';
chatBody.classList.add("thread-open");
}
});
});
});
})
.catch(function(){
instListEl.innerHTML = '<div class="empty-note">Error al cargar.</div>';
});
}

var tabs = document.querySelectorAll(".list-tab");
tabs.forEach(function(tab){
tab.addEventListener("click", function(){
tabs.forEach(function(t){ t.classList.remove("active"); });
tab.classList.add("active");
var name = tab.getAttribute("data-tab");
if (name === "instalaciones"){
threadListEl.style.display = "none";
instListEl.style.display = "";
loadInstallations();
} else {
vistaLista = name;
threadListEl.style.display = "";
instListEl.style.display = "none";
renderThreadList(document.getElementById("searchBox").value);
}
});
});

document.getElementById("searchBox").addEventListener("input", function(e){
renderThreadList(e.target.value);
});

var modalBack = document.getElementById("modalBack");
var modalBody = document.getElementById("modalBody");
var modalFoot = document.getElementById("modalFoot");
var modalTitle = document.getElementById("modalTitle");

function abrirModal(titulo, cuerpo, pie){
modalTitle.innerHTML = titulo;
modalBody.innerHTML = cuerpo;
modalFoot.innerHTML = pie || "";
modalBack.classList.add("open");
}
function cerrarModal(){ modalBack.classList.remove("open"); }
document.getElementById("modalClose").addEventListener("click", cerrarModal);
modalBack.addEventListener("click", function(e){ if (e.target === modalBack) cerrarModal(); });

function listaUsuarios(){
return fetch(API_BASE + "/api/chat/users").then(function(r){ return r.json(); }).then(function(d){ return Array.isArray(d) ? d : ((d && d.users) || []); });
}

function filaElegible(u, marcado){
return '<label class="pick">' +
'<input type="checkbox" value="' + esc(u.dni) + '"' + (marcado ? " checked" : "") + '/>' +
'<span class="pav">' + avatarHtml(u.dni, initials(u.alias || u.nombre || u.dni)) + '</span>' +
'<span><span class="pname">' + esc(u.alias || u.nombre || u.dni) + '</span><br/><span class="prole">' + esc(u.rol || "") + (u.instalacion ? " &middot; " + esc(u.instalacion) : "") + '</span></span>' +
'</label>';
}

/* ---- Crear grupo ---- */
function abrirNuevoGrupo(){
abrirModal("Nuevo grupo", '<div class="empty-note">Cargando...</div>', "");
listaUsuarios().then(function(users){
var otros = (users || []).filter(function(u){ return u.dni !== AUTH_DNI; });
var cuerpo = '<input class="modal-input" id="grpNombre" maxlength="60" placeholder="Nombre del grupo (ej. Turno noche)" />' +
'<input class="modal-input" id="grpBuscar" placeholder="Buscar socorrista..." />' +
'<div id="grpLista">' + otros.map(function(u){ return filaElegible(u, false); }).join("") + '</div>';
var pie = '<button class="modal-btn ghost" id="grpCancelar">Cancelar</button><button class="modal-btn" id="grpCrear">Crear grupo</button>';
abrirModal("Nuevo grupo", cuerpo, pie);
document.getElementById("grpBuscar").addEventListener("input", function(e){
var q = (e.target.value || "").toLowerCase();
document.querySelectorAll("#grpLista .pick").forEach(function(el){
el.style.display = el.textContent.toLowerCase().indexOf(q) === -1 ? "none" : "";
});
});
document.getElementById("grpCancelar").addEventListener("click", cerrarModal);
document.getElementById("grpCrear").addEventListener("click", function(){
var nombre = (document.getElementById("grpNombre").value || "").trim();
var elegidos = [].slice.call(document.querySelectorAll("#grpLista input:checked")).map(function(i){ return i.value; });
if (!nombre){ alert("Ponle un nombre al grupo."); return; }
if (elegidos.length < 2){ alert("Elige al menos 2 integrantes."); return; }
var btn = this; btn.disabled = true; btn.textContent = "Creando...";
fetch(API_BASE + "/api/chat/groups", {
method: "POST", headers: {"Content-Type": "application/json"},
body: JSON.stringify({user_id: AUTH_DNI, title: nombre, members: elegidos})
})
.then(function(r){ return r.json(); })
.then(function(d){
btn.disabled = false; btn.textContent = "Crear grupo";
if (d && d.ok && d.thread_id){
cerrarModal();
vistaLista = "grupos";
loadThreads();
setTimeout(function(){ openThread(d.thread_id); }, 600);
} else {
alert((d && d.error) || "No se pudo crear el grupo.");
}
})
.catch(function(){ btn.disabled = false; btn.textContent = "Crear grupo"; alert("Error de conexi\u00f3n."); });
});
}).catch(function(){ abrirModal("Nuevo grupo", '<div class="empty-note">Error al cargar la lista.</div>', ""); });
}

/* ---- Integrantes del grupo ---- */
function abrirIntegrantes(threadId){
abrirModal("Integrantes", '<div class="empty-note">Cargando...</div>', "");
Promise.all([
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(threadId) + "/members?user_id=" + encodeURIComponent(AUTH_DNI)).then(function(r){ return r.json(); }),
listaUsuarios()
]).then(function(res){
var info = res[0] || {}, users = res[1] || [];
var miembros = info.members || [];
var puedeEditar = (info.created_by || "").toLowerCase() === String(AUTH_DNI).toLowerCase() || String(AUTH_ROLE).toLowerCase() === "administrador";
var dentro = {};
miembros.forEach(function(m){ dentro[m.dni.toLowerCase()] = true; });
var fuera = users.filter(function(u){ return !dentro[String(u.dni).toLowerCase()]; });

var cuerpo = '<div style="font-size:12px;color:#6b7688;font-weight:700;margin-bottom:6px;">EN EL GRUPO (' + miembros.length + ')</div>' +
miembros.map(function(m){
return '<div class="mem-row"><span class="pav">' + avatarHtml(m.dni, initials(m.alias)) + '</span>' +
'<span><span class="pname">' + esc(m.alias) + '</span><br/><span class="prole">' + esc(m.rol || "") + '</span></span>' +
(m.es_creador ? '<span class="mem-owner">Creador</span>' : (puedeEditar ? '<button class="mem-x" data-quitar="' + esc(m.dni) + '">Quitar</button>' : '')) +
'</div>';
}).join("");

if (puedeEditar && fuera.length){
cuerpo += '<div style="font-size:12px;color:#6b7688;font-weight:700;margin:14px 0 6px 0;">AGREGAR</div>' +
'<input class="modal-input" id="memBuscar" placeholder="Buscar socorrista..." />' +
'<div id="memLista">' + fuera.map(function(u){ return filaElegible(u, false); }).join("") + '</div>';
}

var pie = puedeEditar
? '<button class="modal-btn ghost" id="memCerrar">Cerrar</button><button class="modal-btn" id="memGuardar">Guardar cambios</button>'
: '<button class="modal-btn ghost" id="memCerrar">Cerrar</button>';

abrirModal("Integrantes del grupo", cuerpo, pie);
document.getElementById("memCerrar").addEventListener("click", cerrarModal);

var buscar = document.getElementById("memBuscar");
if (buscar){
buscar.addEventListener("input", function(e){
var q = (e.target.value || "").toLowerCase();
document.querySelectorAll("#memLista .pick").forEach(function(el){
el.style.display = el.textContent.toLowerCase().indexOf(q) === -1 ? "none" : "";
});
});
}

var quitar = [];
document.querySelectorAll("[data-quitar]").forEach(function(btn){
btn.addEventListener("click", function(){
var dni = btn.getAttribute("data-quitar");
if (quitar.indexOf(dni) === -1){ quitar.push(dni); btn.textContent = "Se quitar\u00e1"; btn.style.opacity = ".6"; }
else { quitar.splice(quitar.indexOf(dni), 1); btn.textContent = "Quitar"; btn.style.opacity = "1"; }
});
});

var guardar = document.getElementById("memGuardar");
if (guardar){
guardar.addEventListener("click", function(){
var agregar = [].slice.call(document.querySelectorAll("#memLista input:checked")).map(function(i){ return i.value; });
if (!agregar.length && !quitar.length){ cerrarModal(); return; }
guardar.disabled = true; guardar.textContent = "Guardando...";
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(threadId) + "/members", {
method: "POST", headers: {"Content-Type": "application/json"},
body: JSON.stringify({user_id: AUTH_DNI, add: agregar, remove: quitar})
})
.then(function(r){ return r.json(); })
.then(function(d){
guardar.disabled = false; guardar.textContent = "Guardar cambios";
if (d && d.ok){ cerrarModal(); loadThreads(); loadThreadPanel(threadId, true); }
else { alert((d && d.error) || "No se pudo actualizar."); }
})
.catch(function(){ guardar.disabled = false; guardar.textContent = "Guardar cambios"; alert("Error de conexi\u00f3n."); });
});
}
}).catch(function(){ abrirModal("Integrantes", '<div class="empty-note">Error al cargar.</div>', ""); });
}

/* ---- Foto de perfil desde la galeria ---- */
(function(){
var meAv = document.getElementById("meAvatar");
var input = document.getElementById("avatarInput");
var txt = document.getElementById("meAvatarTxt");
var nombre = document.getElementById("meName");
if (nombre) nombre.textContent = AUTH_USER || AUTH_DNI || "";
function pintarMiFoto(){
if (!txt) return;
var img = new Image();
img.onload = function(){
meAv.innerHTML = '<img class="avatar-img" src="' + img.src + '"/><span class="cam">&#128247;</span>';
};
img.onerror = function(){
meAv.innerHTML = '<span id="meAvatarTxt">' + initials(AUTH_USER || AUTH_DNI) + '</span><span class="cam">&#128247;</span>';
};
img.src = API_BASE + "/api/chat/avatar/" + encodeURIComponent(AUTH_DNI) + "?t=" + Date.now();
}
pintarMiFoto();
if (meAv) meAv.addEventListener("click", function(){ input.click(); });
if (input) input.addEventListener("change", function(e){
var f = e.target.files && e.target.files[0];
e.target.value = "";
if (!f) return;
if (f.type.indexOf("image/") !== 0){ alert("Elige una imagen."); return; }
var reader = new FileReader();
reader.onload = function(){
var img = new Image();
img.onload = function(){
var lado = 320;
var c = document.createElement("canvas");
c.width = lado; c.height = lado;
var ctx = c.getContext("2d");
var min = Math.min(img.width, img.height);
ctx.drawImage(img, (img.width - min) / 2, (img.height - min) / 2, min, min, 0, 0, lado, lado);
var dataUrl = c.toDataURL("image/jpeg", 0.85);
fetch(API_BASE + "/api/chat/avatar", {
method: "POST", headers: {"Content-Type": "application/json"},
body: JSON.stringify({user_id: AUTH_DNI, mime: "image/jpeg", data: dataUrl})
})
.then(function(r){ return r.json(); })
.then(function(d){
if (d && d.ok){ pintarMiFoto(); loadThreads(); }
else { alert((d && d.error) || "No se pudo guardar la foto."); }
})
.catch(function(){ alert("Error de conexi\u00f3n al subir la foto."); });
};
img.src = reader.result;
};
reader.readAsDataURL(f);
});
})();

document.getElementById("newBtn").addEventListener("click", abrirNuevoGrupo);

function openThread(threadId){
currentThreadId = threadId;
chatBody.classList.add("thread-open");
renderThreadList(document.getElementById("searchBox").value);
loadThreadPanel(threadId);
if (pollTimer) clearInterval(pollTimer);
pollTimer = setInterval(function(){ checkUpdates(threadId); }, 3000);
}

function checkUpdates(threadId){
if (document.hidden || threadId !== currentThreadId) return;
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(threadId) + "/updates?user_id=" + encodeURIComponent(AUTH_DNI) + "&after=" + encodeURIComponent(lastMsgId[threadId] || "0"))
.then(function(r){ return r.json(); })
.then(function(d){
if (d && d.ok && d.has_new && threadId === currentThreadId){
loadThreadPanel(threadId, true);
loadThreads();
}
})
.catch(function(){});
}

setInterval(function(){ if (!document.hidden) loadThreads(); }, 10000);

document.addEventListener("visibilitychange", function(){
if (document.hidden) return;
loadThreads();
if (currentThreadId) checkUpdates(currentThreadId);
});
window.addEventListener("focus", function(){
if (currentThreadId) checkUpdates(currentThreadId);
});

var imgViewer = document.getElementById("imgViewer");
imgViewer.addEventListener("click", function(){ imgViewer.classList.remove("open"); });

function esc(s){
return (s || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function loadThreadPanel(threadId, silent){
var meta = threadsCache.find(function(t){ return t.id === threadId; });
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(threadId) + "/messages?user_id=" + encodeURIComponent(AUTH_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
var messages = (d && d.ok && d.messages) ? d.messages : [];
if (threadId !== currentThreadId) return;
renderThreadPanel(meta, messages, threadId);
if (messages.length){
var lastId = messages[messages.length - 1].id;
lastMsgId[threadId] = lastId;
if (lastReadSent[threadId] === lastId) return;
lastReadSent[threadId] = lastId;
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(threadId) + "/read", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({user_id: AUTH_DNI, last_read_message_id: lastId})
}).catch(function(){});
}
})
.catch(function(){
if (!silent) threadPanel.innerHTML = '<div class="placeholder-panel">Error al cargar mensajes.</div>';
});
}

function msgsHtml(messages){
return messages.map(function(m){
var mine = m.sender_id === AUTH_DNI;
var att = attInfo(m.body);
var inner = esc(m.body);
if (att && att.kind === "image"){ inner = '<img class="msg-img" src="' + att.url + '" loading="lazy" alt="Imagen"/>'; }
if (att && att.kind === "audio"){ inner = '<audio class="msg-audio" controls preload="metadata" src="' + att.url + '"></audio>'; }
return '<div class="msg-row' + (mine ? ' mine' : '') + '">' +
(mine ? '' : '<div class="msg-sender">' + esc(m.sender_alias) + '</div>') +
'<div class="msg-bubble' + (att ? ' has-att' : '') + '">' + inner + '</div>' +
'<div class="msg-time">' + timeAgo(m.created_at) + '</div>' +
'</div>';
}).join("");
}

function bindImgs(wrap){
wrap.querySelectorAll(".msg-img").forEach(function(img){
img.addEventListener("click", function(){
document.getElementById("imgViewerImg").src = img.src;
imgViewer.classList.add("open");
});
img.addEventListener("load", function(){ if (wrap.getAttribute("data-stick") === "1") wrap.scrollTop = wrap.scrollHeight; });
});
}

function subtituloHilo(meta){
if (!meta) return "Conversaci&oacute;n";
if (meta.type === "installation") return "Instalaci&oacute;n";
if (meta.type === "group") return "Grupo";
return "Privado";
}

function renderThreadPanel(meta, messages, threadId){
var existingWrap = document.getElementById("messagesWrap");
if (threadId && renderedThreadId === threadId && existingWrap && document.getElementById("msgInput")){
var sig = messages.length ? messages[messages.length - 1].id + ":" + messages.length : "0";
if (existingWrap.getAttribute("data-sig") === sig) return;
var nearBottom = (existingWrap.scrollHeight - existingWrap.scrollTop - existingWrap.clientHeight) < 80;
existingWrap.setAttribute("data-sig", sig);
existingWrap.innerHTML = messages.length ? msgsHtml(messages) : '<div class="empty-note">Aun no hay mensajes. Envia el primero.</div>';
existingWrap.setAttribute("data-stick", nearBottom ? "1" : "0");
bindImgs(existingWrap);
if (nearBottom) existingWrap.scrollTop = existingWrap.scrollHeight;
return;
}
renderedThreadId = threadId || null;
var title = meta ? meta.title : "Conversaci&oacute;n";
var sub = subtituloHilo(meta);
var esGrupo = meta && meta.type === "group";
threadPanel.innerHTML =
'<div id="threadHeader">' +
'<button class="back-btn" id="backBtn">&#8592;</button>' +
'<div><div id="threadHeaderTitle">' + esc(title) + '</div><div id="threadHeaderSub">' + sub + '</div></div>' +
(esGrupo ? '<button class="head-btn" id="membersBtn">&#128101; Integrantes</button>' : '') +
'</div>' +
'<div id="messagesWrap"></div>' +
'<div id="composer">' +
'<input type="file" id="fileInput" accept="image/*" style="display:none;" />' +
'<button class="att-btn" id="attachBtn" title="Enviar imagen">&#128206;</button>' +
'<button class="att-btn" id="micBtn" title="Nota de voz">&#127908;</button>' +
'<span id="recInfo" style="display:none;"></span>' +
'<input id="msgInput" placeholder="Escribe un mensaje..." />' +
'<button class="send-btn" id="sendBtn">&#10148;</button>' +
'</div>';

var wrap = document.getElementById("messagesWrap");
if (!messages.length){
wrap.innerHTML = '<div class="empty-note">Aun no hay mensajes. Envia el primero.</div>';
} else {
wrap.innerHTML = msgsHtml(messages);
}
wrap.setAttribute("data-sig", messages.length ? messages[messages.length - 1].id + ":" + messages.length : "0");
wrap.setAttribute("data-stick", "1");
bindImgs(wrap);
wrap.scrollTop = wrap.scrollHeight;

var mb = document.getElementById("membersBtn");
if (mb) mb.addEventListener("click", function(){ abrirIntegrantes(threadId || currentThreadId); });

document.getElementById("backBtn").addEventListener("click", function(){
chatBody.classList.remove("thread-open");
if (pollTimer) clearInterval(pollTimer);
currentThreadId = null;
renderedThreadId = null;
});

function doSend(){
var input = document.getElementById("msgInput");
var body = input.value.trim();
if (!body || !currentThreadId) return;
var btn = document.getElementById("sendBtn");
btn.disabled = true;
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(currentThreadId) + "/messages", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({sender_id: AUTH_DNI, body: body})
})
.then(function(r){ return r.json(); })
.then(function(d){
btn.disabled = false;
if (d && d.ok){
input.value = "";
loadThreadPanel(currentThreadId, true);
loadThreads();
}
})
.catch(function(){ btn.disabled = false; });
}
document.getElementById("sendBtn").addEventListener("click", doSend);
document.getElementById("msgInput").addEventListener("keydown", function(e){
if (e.key === "Enter") doSend();
});

function sendAttachment(mime, dataUrl){
var tid = currentThreadId;
if (!tid) return;
var attachBtn = document.getElementById("attachBtn");
var micBtn = document.getElementById("micBtn");
if (attachBtn) attachBtn.disabled = true;
if (micBtn && !mediaRecorder) micBtn.disabled = true;
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(tid) + "/attachments", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({sender_id: AUTH_DNI, mime: mime, data: dataUrl})
})
.then(function(r){ return r.json(); })
.then(function(d){
if (d && d.ok){
loadThreadPanel(tid, true);
loadThreads();
} else {
alert((d && d.error) ? d.error : "No se pudo enviar el archivo.");
}
})
.catch(function(){ alert("Error de conexion al enviar el archivo."); })
.then(function(){
var a = document.getElementById("attachBtn"); if (a) a.disabled = false;
var mb = document.getElementById("micBtn"); if (mb) mb.disabled = false;
});
}

function compressImage(file, cb){
var reader = new FileReader();
reader.onload = function(){
if (file.type === "image/gif"){ cb("image/gif", reader.result); return; }
var img = new Image();
img.onload = function(){
var max = 1280;
var w = img.width, h = img.height;
if (w > max || h > max){ var k = Math.min(max / w, max / h); w = Math.round(w * k); h = Math.round(h * k); }
var c = document.createElement("canvas");
c.width = w; c.height = h;
c.getContext("2d").drawImage(img, 0, 0, w, h);
cb("image/jpeg", c.toDataURL("image/jpeg", 0.82));
};
img.onerror = function(){ cb(file.type, reader.result); };
img.src = reader.result;
};
reader.readAsDataURL(file);
}

document.getElementById("attachBtn").addEventListener("click", function(){
document.getElementById("fileInput").click();
});
document.getElementById("fileInput").addEventListener("change", function(e){
var f = e.target.files && e.target.files[0];
e.target.value = "";
if (!f) return;
if (f.type.indexOf("image/") !== 0){ alert("Solo se permiten imagenes."); return; }
compressImage(f, function(mime, dataUrl){ sendAttachment(mime, dataUrl); });
});

function stopRecUi(){
var mb = document.getElementById("micBtn");
var ri = document.getElementById("recInfo");
if (mb){ mb.classList.remove("rec"); mb.innerHTML = "&#127908;"; }
if (ri){ ri.style.display = "none"; ri.textContent = ""; }
if (recTimer){ clearInterval(recTimer); recTimer = null; }
}

document.getElementById("micBtn").addEventListener("click", function(){
if (mediaRecorder && mediaRecorder.state === "recording"){ mediaRecorder.stop(); return; }
if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === "undefined"){
alert("Tu navegador no permite grabar audio aqui.");
return;
}
navigator.mediaDevices.getUserMedia({audio: true}).then(function(stream){
var opts = {};
["audio/webm;codecs=opus", "audio/webm", "audio/ogg;codecs=opus", "audio/mp4"].some(function(t){
if (MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(t)){ opts.mimeType = t; return true; }
return false;
});
recChunks = [];
mediaRecorder = new MediaRecorder(stream, opts);
mediaRecorder.ondataavailable = function(ev){ if (ev.data && ev.data.size) recChunks.push(ev.data); };
mediaRecorder.onstop = function(){
stream.getTracks().forEach(function(t){ t.stop(); });
stopRecUi();
var mime = ((mediaRecorder && mediaRecorder.mimeType) || opts.mimeType || "audio/webm").split(";")[0];
var blob = new Blob(recChunks, {type: mime});
mediaRecorder = null;
if (!blob.size || (Date.now() - recStart) < 800) return;
var fr = new FileReader();
fr.onload = function(){ sendAttachment(mime, fr.result); };
fr.readAsDataURL(blob);
};
mediaRecorder.start();
recStart = Date.now();
var mb = document.getElementById("micBtn");
var ri = document.getElementById("recInfo");
mb.classList.add("rec"); mb.innerHTML = "&#9632;";
ri.style.display = ""; ri.textContent = "0:00";
recTimer = setInterval(function(){
var sec = Math.floor((Date.now() - recStart) / 1000);
ri.textContent = Math.floor(sec / 60) + ":" + ("0" + (sec % 60)).slice(-2);
if (sec >= 120 && mediaRecorder && mediaRecorder.state === "recording") mediaRecorder.stop();
}, 500);
}).catch(function(){
alert("No se pudo acceder al microfono. Revisa los permisos del navegador.");
});
});
}
})();

/* ===== Asistente IA (IIFE independiente, no toca el chat) ===== */
(function(){
var IA_API = __API_BASE__;
var IA_DNI = __AUTH_DNI__;
var fab = document.getElementById("iaFab");
var panel = document.getElementById("iaPanel");
var closeBtn = document.getElementById("iaClose");
var body = document.getElementById("iaBody");
var input = document.getElementById("iaInput");
var sendBtn = document.getElementById("iaSend");
if(!fab || !panel){ return; }
var greeted = false;
function addMsg(text, who){
  var d = document.createElement("div");
  d.className = "ia-msg " + (who === "user" ? "ia-user" : "ia-bot");
  d.textContent = text;
  body.appendChild(d);
  body.scrollTop = body.scrollHeight;
  return d;
}
function openPanel(){
  panel.classList.add("open");
  if(!greeted){
    greeted = true;
    addMsg("Hola, soy tu asistente de SYNTRA. Pregúntame sobre turnos, incidencias, novedades o el uso de la plataforma.", "bot");
  }
  setTimeout(function(){ input.focus(); }, 50);
}
function closePanel(){ panel.classList.remove("open"); }
fab.addEventListener("click", function(){ panel.classList.contains("open") ? closePanel() : openPanel(); });
closeBtn.addEventListener("click", closePanel);
function doSend(){
  var q = (input.value || "").trim();
  if(!q){ return; }
  addMsg(q, "user");
  input.value = "";
  input.style.height = "auto";
  sendBtn.disabled = true;
  var typing = document.createElement("div");
  typing.className = "ia-typing";
  typing.textContent = "Escribiendo...";
  body.appendChild(typing);
  body.scrollTop = body.scrollHeight;
  fetch(IA_API + "/api/chat-ia", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ consulta: q, user_id: IA_DNI })
  })
  .then(function(r){ return r.json(); })
  .then(function(data){
    if(typing.parentNode){ typing.parentNode.removeChild(typing); }
    var reply = (data && (data.respuesta || data.reply || data.message)) || "";
    if(data && data.ok === false && data.error){ reply = "⚠️ " + data.error; }
    if(!reply){ reply = "No recibí respuesta. Intenta de nuevo."; }
    addMsg(reply, "bot");
  })
  .catch(function(){
    if(typing.parentNode){ typing.parentNode.removeChild(typing); }
    addMsg("⚠️ Error de conexión con el asistente.", "bot");
  })
  .then(function(){ sendBtn.disabled = false; input.focus(); });
}
sendBtn.addEventListener("click", doSend);
input.addEventListener("keydown", function(e){
  if(e.key === "Enter" && !e.shiftKey){ e.preventDefault(); doSend(); }
});
input.addEventListener("input", function(){
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 96) + "px";
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
)

html = html.replace("__SYNTRA_NAV__", NAV_JS)

components.html(html, height=850, scrolling=False)
