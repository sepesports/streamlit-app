# syntra_core.py
# Utilidades comunes de SYNTRA: sesion persistente entre paginas,
# redireccion del lado servidor y ajuste de la pagina contenedora.
import streamlit as st

_AUTH_KEY = "syntra_auth"


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
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"]{background:__BG__ !important;}
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
try{
var pd = window.parent.document;
var a = pd.createElement("a");
a.href = url;
a.style.display = "none";
pd.body.appendChild(a);
a.click();
return;
}catch(e){}
window.location.href = url;
}
/* Barra inferior fija, igual en todas las pantallas (movil) */
function syntraBottomNav(){
if (document.getElementById("bottomnav") || document.getElementById("syntraBn")) return;
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
"}";
if (document.getElementById("chatBody")){
st.textContent += "@media (max-width:900px){#app{height:calc(100dvh - 62px) !important;min-height:0 !important;max-height:calc(100dvh - 62px) !important;}#main{height:100% !important;min-height:0 !important;}body{padding-bottom:0 !important;}#iaFab{bottom:74px !important;}#iaPanel{bottom:140px !important;height:calc(100dvh - 215px) !important;}}";
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
