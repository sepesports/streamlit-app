# syntra_core.py
# Utilidades comunes de SYNTRA: sesion persistente entre paginas,
# redireccion del lado servidor y ajuste de la pagina contenedora.
import streamlit as st

_AUTH_KEY = "syntra_auth"

# Logo oficial de SYNTRA incrustado (no depende de servidores externos)
LOGO_DATA_URI = "data:image/png;base64,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"


def sync_auth():
    """Guarda la sesion (auth/usuario/rol/dni) al llegar por URL y la
    restaura en la URL cuando se navega entre paginas sin recargar."""
    qp = st.query_params
    usuario = qp.get("usuario") or qp.get("user") or ""
    rol = qp.get("rol") or qp.get("role") or ""
    dni = qp.get("dni") or ""

    if qp.get("auth") == "ok" and (usuario or rol or dni):
        st.session_state[_AUTH_KEY] = {"usuario": usuario, "rol": rol, "dni": dni}
        return

    saved = st.session_state.get(_AUTH_KEY)
    if saved:
        st.query_params.update({
            "auth": "ok",
            "usuario": saved.get("usuario", ""),
            "rol": saved.get("rol", ""),
            "dni": saved.get("dni", ""),
        })


def go(page_path):
    """Redireccion real del lado servidor (reemplaza <script> que no se ejecuta)."""
    st.switch_page(page_path)


def shell_css(bg="#1B2A4A"):
    """Contenedor a pantalla completa: sin barra lateral de Streamlit,
    sin huecos, fondo sin destellos blancos e iframe a la altura visible."""
    st.markdown(
        """
        <style>
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"]{background:radial-gradient(1100px 520px at 10% -10%, rgba(64,132,255,.30) 0%, rgba(64,132,255,0) 60%), radial-gradient(900px 460px at 108% 4%, rgba(31,79,216,.26) 0%, rgba(31,79,216,0) 55%), linear-gradient(165deg,#17274f 0%,#101d3d 48%,#0a142b 100%)  !important;}
        html, body{overflow:hidden !important;}
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"],
        [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stHeader"]{display:none !important;}
        [data-testid="stMainBlockContainer"], .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
        [data-testid="stVerticalBlock"]{gap:0 !important;}
        [data-testid="stElementContainer"]:has(> [data-testid="stMarkdown"] style){display:none !important;}
        iframe{display:block;width:100% !important;height:100vh !important;height:100dvh !important;border:0 !important;background:__BG__;}
        </style>
        """.replace("__BG__", bg),
        unsafe_allow_html=True,
    )


NAV_JS = r"""
/* Ajusta el alto real de la pantalla del movil (barra del navegador que aparece y desaparece) */
(function(){
var fe = window.frameElement;
if (!fe) return;
function fit(){
try{
var vv = window.parent.visualViewport;
var h = (vv && vv.height) || window.parent.innerHeight || window.innerHeight;
fe.style.position = "fixed";
fe.style.left = "0";
fe.style.top = "0";
fe.style.width = "100%";
fe.style.height = h + "px";
fe.style.border = "0";
fe.style.margin = "0";
}catch(e){}
}
fit();
setTimeout(fit, 300);
try{
var vv = window.parent.visualViewport;
if (vv){ vv.addEventListener("resize", fit); vv.addEventListener("scroll", fit); }
window.parent.addEventListener("resize", fit);
window.parent.addEventListener("orientationchange", function(){ setTimeout(fit, 250); });
}catch(e){}
})();
function syntraTopNav(url){
/* Navega la pagina COMPLETA (no solo el marco interno) para que la barra de direccion quede correcta */
try{
var w = window;
while (w !== w.parent){
try{ if (w.parent.document) { w = w.parent; } else { break; } }catch(e){ break; }
}
var pd = w.document;
var abs = url;
try{ abs = new URL(url, w.location.origin).href; }catch(e){}
var a = pd.createElement("a");
a.href = abs;
a.target = "_top";
a.rel = "noopener";
a.style.display = "none";
pd.body.appendChild(a);
a.click();
return;
}catch(e){}
try{ window.top.location.href = url; return; }catch(e){}
window.location.href = url;
}
/* Barra inferior fija, igual en todas las pantallas (movil) */
function syntraBottomNav(){
if (document.getElementById("bottomnav") || document.getElementById("syntraBn")) return;
if (document.getElementById("btnLogin")) return;  /* pantalla de login: sin barra */
var path = "";
try{ path = window.parent.location.pathname; }catch(e){ path = location.pathname; }
var segs = path.split("/").filter(function(s){ return s && s !== "~" && s !== "+"; });
var here = segs.length ? segs[segs.length - 1] : "";

var items = [
{k:"", go:"/", ic:"&#8962;", lab:"Inicio"},
{k:"calendario", go:"/calendario", ic:"&#128197;", lab:"Horarios"},
{k:"chat_interfaz", go:"/chat_interfaz", ic:"&#128172;", lab:"Chat"},
{k:"mas", go:"", ic:"&#8942;", lab:"M\u00e1s"}
];

var st = document.createElement("style");
st.textContent = "#syntraBn{display:none;}" +
"@media (max-width:900px){" +
"#syntraBn{display:flex;position:fixed;left:0;right:0;bottom:0;height:62px;background:#fff;border-top:1px solid #e5e7eb;z-index:9998;padding-bottom:env(safe-area-inset-bottom);}" +
"#syntraBn .sbn{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:10.5px;font-weight:600;color:#6B7280;cursor:pointer;font-family:inherit;background:none;border:0;}" +
"#syntraBn .sbn.on{color:#1F4FD8;}" +
"#syntraBn .sbn .ic{font-size:18px;line-height:1;}" +
"body{padding-bottom:62px !important;}" +
"#app{padding-left:5px !important;padding-right:5px !important;}" +
"#content{padding-left:7px !important;padding-right:7px !important;}" +
"#app, #pagewrap{zoom:1.1;}" +
"html,body{background:radial-gradient(1100px 520px at 10% -10%, rgba(64,132,255,.30) 0%, rgba(64,132,255,0) 60%), radial-gradient(900px 460px at 108% 4%, rgba(31,79,216,.26) 0%, rgba(31,79,216,0) 55%), linear-gradient(165deg,#17274f 0%,#101d3d 48%,#0a142b 100%) !important;background-attachment:fixed !important;}" +
"#topbar{position:fixed !important;top:0 !important;left:0 !important;right:0 !important;z-index:60 !important;height:60px !important;min-height:60px !important;padding:0 14px !important;border-radius:0 !important;display:flex !important;align-items:center !important;justify-content:flex-start !important;background:linear-gradient(135deg,#182a54 0%,#0d1a37 100%) !important;border:0 !important;border-bottom:1px solid rgba(255,255,255,.12) !important;box-shadow:0 10px 26px rgba(0,0,0,.30) !important;}" +
"#topbar .mobile-logo{position:absolute !important;left:50% !important;transform:translateX(-50%) !important;display:flex !important;align-items:center !important;}" +
"#topbar h1{display:none !important;}" +
"#app{padding-top:70px !important;}" +
"#topbar h1, .mobile-logo{color:#eaf2ff !important;}" +
".hamburger{color:#eaf2ff !important;}" +
"#syntraBn{background:linear-gradient(180deg,#16264d 0%,#0b162f 100%) !important;border-top:1px solid rgba(255,255,255,.12) !important;box-shadow:0 -8px 22px rgba(0,0,0,.28) !important;}" +
"#syntraBn .sbn{color:rgba(234,242,255,.70) !important;}" +
"#syntraBn .sbn.on{color:#8ab4ff !important;}" +
"#topbar{overflow:hidden;}" +
"#topbar::after{content:\'\';position:absolute;top:0;left:-40%;width:35%;height:100%;background:linear-gradient(105deg, rgba(255,255,255,0) 0%, rgba(160,200,255,.16) 45%, rgba(255,255,255,0) 100%);transform:skewX(-18deg);animation:syntraSheen 7s ease-in-out infinite;pointer-events:none;}" +
"@keyframes syntraSheen{0%{left:-40%;}55%{left:115%;}100%{left:115%;}}" +
"#topbar::before{content:\'\';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg, rgba(255,255,255,0), rgba(170,205,255,.55), rgba(255,255,255,0));pointer-events:none;}" +
"#syntraBn::before{content:\'\';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg, rgba(255,255,255,0), rgba(170,205,255,.45), rgba(255,255,255,0));}" +
"#syntraBn .sbn.on{position:relative;}" +
"#syntraBn .sbn.on::after{content:\'\';position:absolute;top:0;left:22%;right:22%;height:2px;border-radius:0 0 3px 3px;background:linear-gradient(90deg, rgba(138,180,255,0), #8ab4ff, rgba(138,180,255,0));box-shadow:0 0 10px rgba(138,180,255,.8);}" +
"#content, #chatBody, .card, .mobile-day-card, .shift, .grid-wrap{box-shadow:0 10px 30px rgba(3,10,28,.28), 0 1px 0 rgba(255,255,255,.55) inset !important;}" +
"@media (prefers-reduced-motion: reduce){#topbar::after{animation:none;} .day-tab.active::after, .new-btn::after, .send-btn::after, .save-btn::after{animation:none;}}" +
".day-tab.active, .new-btn, .send-btn, .save-btn{position:relative;overflow:hidden;}" +
".day-tab.active::after, .new-btn::after, .send-btn::after, .save-btn::after{content:\'\';position:absolute;top:0;left:-45%;width:40%;height:100%;background:linear-gradient(105deg, rgba(255,255,255,0) 0%, rgba(235,244,255,.38) 45%, rgba(255,255,255,0) 100%);transform:skewX(-18deg);animation:syntraSheen 7s ease-in-out infinite;pointer-events:none;}" +
".day-tab.active{box-shadow:0 6px 16px rgba(47,111,224,.35);}" +
".thread-item.active{box-shadow:inset 3px 0 0 #2f6fe0, 0 4px 12px rgba(47,111,224,.14);}" +
".day-tab:active, .new-btn:active, .send-btn:active, .save-btn:active, .thread-item:active, .inst-item:active, .qa-btn:active{transform:translateY(1px);}" +
"}";
if (document.getElementById("chatBody")){
st.textContent += "@media (max-width:900px){#app{height:calc((100dvh - 62px) / 1.1) !important;min-height:0 !important;max-height:calc((100dvh - 62px) / 1.1) !important;}#main{height:100% !important;min-height:0 !important;}body{padding-bottom:0 !important;}#iaFab{bottom:calc(150px / 1.1) !important;right:calc(14px / 1.1) !important;}#iaPanel{bottom:calc(216px / 1.1) !important;height:calc((100dvh - 306px) / 1.1) !important;}}";
}
document.head.appendChild(st);

var bar = document.createElement("div");
bar.id = "syntraBn";
bar.innerHTML = items.map(function(it){
var on = (it.k === here) || (it.k === "" && here === "");
return '<button class="sbn' + (on ? " on" : "") + '" data-k="' + it.k + '"><span class="ic">' + it.ic + '</span>' + it.lab + '</button>';
}).join("");
document.body.appendChild(bar);

bar.querySelectorAll(".sbn").forEach(function(btn){
btn.addEventListener("click", function(){
var k = btn.getAttribute("data-k");
if (k === "mas"){
var dr = document.getElementById("drawer");
if (dr){ dr.classList.add("open"); return; }
}
var it = items.filter(function(x){ return x.k === k; })[0];
if (!it || !it.go) return;
syntraGoTo(it.go, function(){
try{ window.parent.location.href = it.go + window.parent.location.search; }
catch(e){ window.location.href = it.go; }
});
});
});
}

if (document.readyState === "loading"){
document.addEventListener("DOMContentLoaded", function(){ setTimeout(syntraBottomNav, 0); });
} else {
setTimeout(syntraBottomNav, 0);
}

function syntraGoTo(path, fallback){
try{
var want = String(path || "/").split("?")[0].replace(/^\/+|\/+$/g, "");
var links = window.parent.document.querySelectorAll('a[data-testid="stSidebarNavLink"]');
for (var i = 0; i < links.length; i++){
var segs = new URL(links[i].href).pathname.split("/").filter(function(s){ return s && s !== "~" && s !== "+"; });
var name = segs.length ? segs[segs.length - 1] : "";
if (name === want){ links[i].click(); return; }
}
}catch(e){}
fallback();
}
"""
