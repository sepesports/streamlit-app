# pages/chat_interfaz.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Incidencias y Comunicados", layout="wide")

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
.list-tabs{display:flex;gap:18px;padding:14px 18px 0 18px;border-bottom:1px solid var(--border);}
.list-tab{padding:0 0 12px 0;font-size:13px;font-weight:700;color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;}
.list-tab.active{color:var(--blue);border-bottom-color:var(--blue);}
.new-btn{margin-left:auto;background:var(--blue);color:#fff;border:none;border-radius:8px;padding:5px 12px;font-size:12px;font-weight:700;cursor:pointer;align-self:flex-start;}
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
<h1>Incidencias y Comunicados</h1>
<div class="mobile-logo"><img src="__LOGO_URL__"/>SYNTRA</div>
<div></div>
</div>

<div id="chatBody">
<div id="listPanel">
<div class="list-tabs">
<div class="list-tab active" data-tab="conversaciones">Conversaciones</div>
<div class="list-tab" data-tab="instalaciones">Instalaciones</div>
<button class="new-btn" id="newBtn">+ Nueva</button>
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

<script>
(function(){
var API_BASE = __API_BASE__;
var AUTH_USER = __AUTH_USER__;
var AUTH_ROLE = __AUTH_ROLE__;
var AUTH_DNI = __AUTH_DNI__;
var CAN_MANAGE_SCHEDULES = __CAN_MANAGE_SCHEDULES__;
var CAN_REGISTER_USERS = __CAN_REGISTER_USERS__;

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
if (lo) lo.addEventListener("click", function(){ window.top.location.href = "/admin"; });
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

function timeAgo(iso){
if (!iso) return "";
try{
var d = new Date(iso);
var now = new Date();
var diffMs = now - d;
var mins = Math.floor(diffMs / 60000);
if (mins < 1) return "ahora";
if (mins < 60) return mins + "m";
var hrs = Math.floor(mins / 60);
if (hrs < 24) return hrs + "h";
var days = Math.floor(hrs / 24);
return days + "d";
}catch(e){ return ""; }
}

function initials(name){
name = (name || "?").trim();
return name.charAt(0).toUpperCase();
}

function renderThreadList(filter){
filter = (filter || "").toLowerCase();
var filtered = threadsCache.filter(function(t){
return !filter || (t.title || "").toLowerCase().indexOf(filter) !== -1;
});
if (!filtered.length){
threadListEl.innerHTML = '<div class="empty-note">No hay conversaciones.</div>';
return;
}
threadListEl.innerHTML = filtered.map(function(t){
var cls = "thread-item" + (t.id === currentThreadId ? " active" : "");
var unread = t.unread_count > 0 ? '<span class="unread-dot">' + t.unread_count + '</span>' : "";
var sub = t.last_message || (t.type === "installation" ? "Instalaci&oacute;n" : "Privado");
return '<div class="' + cls + '" data-id="' + t.id + '">' +
'<div class="thread-avatar">' + (t.type === "installation" ? "&#127970;" : initials(t.title)) + '</div>' +
'<div class="thread-info">' +
'<div class="thread-title"><span>' + t.title + '</span><span class="thread-time">' + timeAgo(t.last_message_at) + '</span></div>' +
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
if (name === "conversaciones"){
threadListEl.style.display = "";
instListEl.style.display = "none";
} else {
threadListEl.style.display = "none";
instListEl.style.display = "";
loadInstallations();
}
});
});

document.getElementById("searchBox").addEventListener("input", function(e){
renderThreadList(e.target.value);
});

document.getElementById("newBtn").addEventListener("click", function(){
fetch(API_BASE + "/api/chat/users")
.then(function(r){ return r.json(); })
.then(function(users){
var others = (users || []).filter(function(u){ return u.dni !== AUTH_DNI; });
if (!others.length){ alert("No hay usuarios disponibles."); return; }
var names = others.map(function(u, idx){ return (idx+1) + ". " + (u.alias || u.nombre || u.dni); }).join(String.fromCharCode(10));
var pick = window.prompt("Elige un numero para iniciar chat privado:" + String.fromCharCode(10) + names);
var idx = parseInt(pick, 10) - 1;
if (isNaN(idx) || !others[idx]) return;
var target = others[idx];
fetch(API_BASE + "/api/chat/private/" + encodeURIComponent(target.dni) + "?user_id=" + encodeURIComponent(AUTH_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
if (d && d.ok && d.thread_id){
loadThreads();
setTimeout(function(){ openThread(d.thread_id); }, 300);
}
});
})
.catch(function(){ alert("Error al cargar usuarios."); });
});

function openThread(threadId){
currentThreadId = threadId;
chatBody.classList.add("thread-open");
renderThreadList(document.getElementById("searchBox").value);
loadThreadPanel(threadId);
if (pollTimer) clearInterval(pollTimer);
pollTimer = setInterval(function(){ loadThreadPanel(threadId, true); }, 5000);
}

function esc(s){
return (s || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function loadThreadPanel(threadId, silent){
var meta = threadsCache.find(function(t){ return t.id === threadId; });
fetch(API_BASE + "/api/chat/threads/" + encodeURIComponent(threadId) + "/messages?user_id=" + encodeURIComponent(AUTH_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
var messages = (d && d.ok && d.messages) ? d.messages : [];
renderThreadPanel(meta, messages);
if (messages.length){
var lastId = messages[messages.length - 1].id;
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

function renderThreadPanel(meta, messages){
var title = meta ? meta.title : "Conversaci&oacute;n";
var sub = meta && meta.type === "installation" ? "Instalaci&oacute;n" : "Privado";
threadPanel.innerHTML =
'<div id="threadHeader">' +
'<button class="back-btn" id="backBtn">&#8592;</button>' +
'<div><div id="threadHeaderTitle">' + esc(title) + '</div><div id="threadHeaderSub">' + sub + '</div></div>' +
'</div>' +
'<div id="messagesWrap"></div>' +
'<div id="composer">' +
'<input id="msgInput" placeholder="Escribe un mensaje..." />' +
'<button class="send-btn" id="sendBtn">&#10148;</button>' +
'</div>';

var wrap = document.getElementById("messagesWrap");
if (!messages.length){
wrap.innerHTML = '<div class="empty-note">Aun no hay mensajes. Envia el primero.</div>';
} else {
wrap.innerHTML = messages.map(function(m){
var mine = m.sender_id === AUTH_DNI;
return '<div class="msg-row' + (mine ? ' mine' : '') + '">' +
(mine ? '' : '<div class="msg-sender">' + esc(m.sender_alias) + '</div>') +
'<div class="msg-bubble">' + esc(m.body) + '</div>' +
'<div class="msg-time">' + timeAgo(m.created_at) + '</div>' +
'</div>';
}).join("");
}
wrap.scrollTop = wrap.scrollHeight;

document.getElementById("backBtn").addEventListener("click", function(){
chatBody.classList.remove("thread-open");
if (pollTimer) clearInterval(pollTimer);
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
}
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

components.html(html, height=850, scrolling=False)
