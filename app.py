# app.py
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

st.set_page_config(layout="wide", page_title="SYNTRA")
sync_auth()

# GATE: solo entra con ?auth=ok
if st.query_params.get("auth") != "ok":
    go("pages/admin.py")

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
shell_css()


def _js_str(value) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


LOGO_URL = LOGO_DATA_URI

html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
:root{
--navy:#1B2A4A;
--navy-dark:#16233F;
--blue:#1F4FD8;
--blue-soft:#E8F0FE;
--slate:#C7D2E0;
--bg:#F5F6F8;
--card-bg:#FFFFFF;
--ink:#1B2A4A;
--muted:#6B7280;
--border:#E5E7EB;
--red:#EF4444;
--manana:#12B39A;--tarde:#F5B642;--noche:#7C5CFF;--libre:#D1D5DB;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;height:100%;width:100%;font-family:"Inter","Segoe UI",Arial,Helvetica,sans-serif;background:radial-gradient(1100px 520px at 10% -10%, rgba(64,132,255,.30) 0%, rgba(64,132,255,0) 60%), radial-gradient(900px 460px at 108% 4%, rgba(31,79,216,.26) 0%, rgba(31,79,216,0) 55%), linear-gradient(165deg,#17274f 0%,#101d3d 48%,#0a142b 100%);background-attachment:fixed;color:var(--ink);}

#pagewrap{display:flex;flex-direction:column;height:100vh;padding:16px;gap:16px;overflow:hidden;}

/* ===== FRANJA A ===== */
#franjaA{
flex:55 1 0;min-height:0;
display:grid;grid-template-columns:230px 1fr;gap:16px;
}
/* Contenedor 2 = sidebar (fondo navy con borde externo) */
#sidebar{
min-height:0;display:flex;flex-direction:column;color:#eaf2ff;padding:18px 14px;
border:1px solid rgba(255,255,255,.16);border-radius:12px;
}
.logo-row{display:flex;align-items:center;gap:10px;margin-bottom:26px;padding:0 4px;}
.logo-row img{width:32px;height:32px;object-fit:contain;border-radius:6px;}
.logo-row span{font-weight:800;letter-spacing:2px;font-size:18px;color:#fff;}
.nav-item{
display:flex;align-items:center;gap:12px;
padding:10px 12px;border-radius:999px;margin-bottom:4px;
color:var(--slate);font-size:14px;font-weight:600;
cursor:pointer;text-decoration:none;transition:background .15s;position:relative;
}
.nav-item:hover{background:rgba(255,255,255,.08);color:#fff;}
.nav-item.active{background:var(--blue);color:#fff;}
.nav-item.disabled{opacity:.55;cursor:not-allowed;}
.nav-badge{
margin-left:auto;font-size:9.5px;font-weight:700;background:var(--blue);color:#fff;
padding:2px 8px;border-radius:999px;white-space:nowrap;
}
.nav-sep{height:1px;background:rgba(255,255,255,.12);margin:12px 6px;}
.nav-bottom{margin-top:auto;}

/* Contenedor 1 = panel principal (una sola caja blanca) */
#mainpanel{
min-width:0;min-height:0;background:linear-gradient(180deg,#ffffff 0%,#f7f9ff 100%);border-radius:14px;
box-shadow:0 14px 34px rgba(3,10,28,.30), 0 1px 0 rgba(255,255,255,.8) inset;
display:flex;flex-direction:column;padding:16px 20px;gap:12px;
box-shadow:0 4px 12px rgba(27,42,74,.08);overflow:hidden;
}
.mp-header{
padding-bottom:12px;border-bottom:1px solid var(--border);
display:flex;align-items:center;justify-content:space-between;gap:12px;flex:0 0 auto;
}
.mp-header .greet h1{font-size:20px;margin:0 0 3px 0;font-weight:800;color:var(--navy);}
.mp-header .greet p{margin:0;color:var(--muted);font-size:13px;}
.mp-right{display:flex;align-items:center;gap:16px;}
.desktop-brand{display:flex;align-items:center;gap:8px;font-weight:800;letter-spacing:1.5px;font-size:15px;color:var(--navy);}
.desktop-brand img{width:26px;height:26px;object-fit:contain;border-radius:6px;}
.bell{position:relative;font-size:19px;color:var(--navy);cursor:pointer;}
.bell .dot{position:absolute;top:-5px;right:-7px;background:var(--red);color:#fff;font-size:10px;font-weight:800;border-radius:999px;padding:1px 5px;}
.hamburger{display:none;font-size:20px;background:none;border:none;cursor:pointer;color:var(--navy);}

.mp-qa{flex:1;min-height:0;display:flex;flex-direction:column;}
.mp-qa h2{font-size:14px;margin:0 0 10px 0;font-weight:800;color:var(--navy);}
.cards-grid{flex:1;min-height:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}
.qa-card{
background:#fff;border:1px solid var(--border);border-radius:12px;
padding:14px 14px;display:flex;flex-direction:column;gap:8px;
box-shadow:0 4px 12px rgba(27,42,74,.06);min-height:0;
}
.qa-top{display:flex;align-items:flex-start;gap:12px;}
.qa-textcol{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px;}
.qa-icon{
width:60px;height:60px;border-radius:14px;background:var(--blue-soft);
display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--blue);flex:0 0 auto;
}
.qa-icon.qa-icon-chat{background:linear-gradient(140deg,#1faa52 0%,#128C7E 100%);box-shadow:0 6px 14px rgba(18,140,126,.25);}
.qa-card h3{margin:0;font-size:14px;font-weight:700;color:var(--navy);}
.qa-card p{margin:0;font-size:12px;color:var(--muted);line-height:1.35;}
.qa-pill{align-self:flex-start;background:var(--blue-soft);color:var(--blue);font-size:10px;font-weight:700;padding:3px 9px;border-radius:999px;}
.qa-btn{
margin-top:auto;background:var(--navy-dark);color:#fff;border:none;border-radius:10px;
padding:9px 12px;font-size:12.5px;font-weight:700;cursor:pointer;
display:flex;align-items:center;justify-content:center;gap:6px;
}
.qa-btn:hover{background:var(--navy);}
.qa-btn[disabled]{background:#c7cbd6;cursor:not-allowed;}

.kpi-row{
border-top:1px solid var(--border);
display:grid;grid-template-columns:repeat(4,1fr);padding:12px 4px 2px 4px;flex:0 0 auto;
}
.kpi-item{display:flex;align-items:center;gap:10px;padding:0 14px;}
.kpi-item + .kpi-item{border-left:1px solid var(--border);}
.kpi-icon{font-size:18px;color:var(--navy-dark);width:24px;text-align:center;}
.kpi-item .lab{font-size:11px;color:var(--muted);margin:0 0 2px 0;}
.kpi-item .val{font-size:19px;font-weight:800;color:var(--navy);margin:0;}

/* ===== FRANJA B ===== */
#franjaB{
flex:38 1 0;min-height:0;
display:grid;grid-template-columns:repeat(4,1fr);gap:16px;
}
.preview-card{
background:#fff;border:1px solid var(--border);border-radius:16px;
overflow:hidden;display:flex;flex-direction:column;min-height:0;
box-shadow:0 4px 12px rgba(27,42,74,.08);
}
.preview-head{
padding:12px 16px;background:var(--navy);
display:flex;align-items:center;justify-content:space-between;flex:0 0 auto;
}
.preview-head .t{font-size:13px;font-weight:700;color:#fff;display:flex;align-items:center;gap:8px;}
.preview-head .t .ph-ic{color:#fff;font-size:15px;line-height:1;}
.preview-head .more{font-size:11.5px;color:#dfe7f5;font-weight:700;cursor:pointer;background:none;border:none;}
.preview-body{padding:12px 16px;flex:1;min-height:0;overflow:auto;}

.mini-tabs{display:flex;gap:16px;padding:0 16px;border-bottom:1px solid var(--border);flex:0 0 auto;}
.mini-tab{padding:8px 0;font-size:11px;font-weight:700;color:var(--muted);border-bottom:2px solid transparent;}
.mini-tab.active{color:var(--blue);border-bottom-color:var(--blue);}

.mini-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);font-size:12px;}
.mini-row:last-child{border-bottom:none;}
.mini-row .inst{font-weight:700;}
.mini-chip{display:inline-block;border-radius:7px;padding:3px 8px;font-size:11px;margin-left:6px;color:#fff;}
.mini-chip.manana{background:var(--manana);}
.mini-chip.tarde{background:var(--tarde);color:var(--navy);}
.mini-chip.noche{background:var(--noche);}

.mini-thread{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);align-items:center;}
.mini-thread:last-child{border-bottom:none;}
.mini-avatar{width:30px;height:30px;border-radius:8px;background:var(--navy-dark);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;flex:0 0 30px;}
.mini-thread .info{flex:1;min-width:0;}
.mini-thread .title{font-size:12.5px;font-weight:700;}
.mini-thread .sub{font-size:11.5px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.mini-unread{background:var(--blue);color:#fff;font-size:10px;font-weight:700;border-radius:999px;padding:1px 6px;}

.mini-table{width:100%;border-collapse:collapse;font-size:12px;}
.mini-table th{text-align:left;padding:6px 4px;color:var(--muted);font-weight:600;border-bottom:1px solid var(--border);}
.mini-table td{padding:6px 4px;border-bottom:1px solid var(--border);}

.mini-cal{width:100%;border-collapse:collapse;font-size:10.5px;}
.mini-cal th{background:#fafbfd;padding:5px 4px;color:var(--muted);font-weight:600;border-bottom:1px solid var(--border);text-align:center;}
.mini-cal th:first-child{text-align:left;}
.mini-cal td{padding:4px;border-bottom:1px solid var(--border);vertical-align:top;}
.mini-cal td.inst{font-weight:700;font-size:11px;white-space:nowrap;}
.mini-cal-chip{border-radius:5px;padding:2px 4px;font-size:9px;margin-bottom:2px;line-height:1.2;color:#fff;}
.mini-cal-chip.manana{background:var(--manana);}
.mini-cal-chip.tarde{background:var(--tarde);color:var(--navy);}
.mini-cal-chip.noche{background:var(--noche);}

.locked-note{color:var(--muted);font-size:12.5px;text-align:center;padding:24px 10px;}
.empty-note{color:var(--muted);font-size:12.5px;text-align:center;padding:24px 10px;}

.mini-form .field{margin-bottom:9px;}
.mini-form label{display:block;font-size:11px;color:var(--muted);margin-bottom:4px;font-weight:600;}
.mini-form input, .mini-form select{width:100%;padding:7px 10px;border:1px solid var(--border);border-radius:10px;font-size:12.5px;}
.mini-form input:focus, .mini-form select:focus{outline:none;border-color:var(--blue);}
.mini-form-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 10px;}
.mini-save-btn{background:var(--navy-dark);color:#fff;border:none;border-radius:10px;padding:8px 14px;font-size:12.5px;font-weight:700;cursor:pointer;width:100%;margin-top:6px;}
.mini-msg{font-size:11.5px;margin-top:8px;padding:6px 10px;border-radius:8px;display:none;}
.mini-msg.ok{background:#e6f7ee;color:#1a7f4f;display:block;}
.mini-msg.err{background:#fde8e8;color:#b02a2a;display:block;}

/* ===== FRANJA C ===== */
/* Contenedor 7 = pie (caja blanca) */
#franjaC{
flex:7 1 0;min-height:0;
background:#fff;border-radius:12px;color:var(--muted);box-shadow:0 4px 12px rgba(27,42,74,.08);
padding:0 26px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;font-size:12px;
}
#franjaC .brand{display:flex;align-items:center;gap:9px;font-weight:800;letter-spacing:1.5px;color:var(--navy);font-size:14px;}
#franjaC .brand img{width:24px;height:24px;object-fit:contain;border-radius:5px;}

/* ===== Barra superior fija (movil) ===== */
#topbarMobile{display:none;}
@media (max-width:768px){
#topbarMobile{
display:flex;position:fixed;left:0;right:0;top:0;height:60px;z-index:60;
background:linear-gradient(135deg,#182a54 0%,#0d1a37 100%);
border-bottom:1px solid rgba(255,255,255,.12);
box-shadow:0 10px 26px rgba(0,0,0,.30);
align-items:center;padding:0 14px;gap:10px;padding-top:env(safe-area-inset-top);
overflow:hidden;
}
#topbarMobile::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg, rgba(255,255,255,0), rgba(170,205,255,.55), rgba(255,255,255,0));}
#topbarMobile::after{content:'';position:absolute;top:0;left:-40%;width:35%;height:100%;background:linear-gradient(105deg, rgba(255,255,255,0) 0%, rgba(160,200,255,.16) 45%, rgba(255,255,255,0) 100%);transform:skewX(-18deg);animation:syntraSheen 7s ease-in-out infinite;pointer-events:none;}
@keyframes syntraSheen{0%{left:-40%;}55%{left:115%;}100%{left:115%;}}
@media (prefers-reduced-motion: reduce){#topbarMobile::after{animation:none;}}
#topbarMobile .tb-burger{background:none;border:0;font-size:20px;color:#eaf2ff;cursor:pointer;line-height:1;padding:4px;}
#topbarMobile .tb-brand{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;font-weight:800;letter-spacing:2px;font-size:16px;color:#eaf2ff;}
#topbarMobile .tb-bell{position:relative;background:none;border:0;font-size:19px;cursor:pointer;padding:4px;}
#topbarMobile .tb-bell .dot{position:absolute;top:0;right:0;background:var(--red);color:#fff;font-size:9.5px;font-weight:700;border-radius:99px;padding:1px 5px;display:none;}
#pagewrap{padding-top:72px !important;}
.mp-header .hamburger, .mp-header .bell{display:none !important;}
.mp-header{padding-bottom:10px;}
}

/* ===== Inicio movil (por rol) ===== */
#homeMobile{display:none;}
.hm-hero{border-radius:16px;padding:16px 16px 14px 16px;color:#fff;background:linear-gradient(135deg,#1F4FD8 0%,#1B2A4A 100%);margin-bottom:12px;}
.hm-hero .lab{font-size:11.5px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;opacity:.75;}
.hm-hero .big{font-size:26px;font-weight:800;margin-top:6px;letter-spacing:.3px;line-height:1.15;}
.hm-hero .sub{font-size:13px;opacity:.9;margin-top:6px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;}
.hm-hero .chips{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}
.hm-chip{background:rgba(255,255,255,.16);border-radius:99px;padding:5px 11px;font-size:11.5px;font-weight:700;}
.hm-week{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin-bottom:14px;}
.hm-day{background:#fff;border:1px solid var(--border);border-radius:12px;padding:7px 0 6px 0;text-align:center;line-height:1.1;cursor:pointer;}
.hm-day .w{display:block;font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;}
.hm-day .n{display:block;font-size:15px;font-weight:800;margin-top:2px;}
.hm-day .d{display:block;width:5px;height:5px;border-radius:50%;background:var(--blue);margin:3px auto 0 auto;}
.hm-day .d.off{background:transparent;}
.hm-day.today{border-color:var(--blue);background:var(--blue-soft);}
.hm-tiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;}
.hm-tile{background:#fff;border:1px solid var(--border);border-radius:14px;padding:12px 13px;cursor:pointer;}
.hm-tile .v{font-size:22px;font-weight:800;color:var(--navy);line-height:1;}
.hm-tile .l{font-size:11.5px;color:var(--muted);margin-top:5px;font-weight:600;}
.hm-sec{font-size:13px;font-weight:800;color:var(--navy);margin:0 0 8px 2px;display:flex;align-items:center;justify-content:space-between;}
.hm-sec a{font-size:12px;color:var(--blue);font-weight:700;text-decoration:none;}
.hm-list{background:#fff;border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:14px;}
.hm-row{display:flex;align-items:center;gap:11px;padding:11px 13px;border-bottom:1px solid var(--border);cursor:pointer;}
.hm-row:last-child{border-bottom:none;}
.hm-av{width:34px;height:34px;border-radius:10px;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;flex:0 0 34px;}
.hm-row .info{flex:1;min-width:0;}
.hm-row .t{font-size:13.5px;font-weight:700;}
.hm-row .s{font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.hm-badge{background:var(--blue);color:#fff;border-radius:99px;font-size:11px;font-weight:700;padding:2px 8px;}
.hm-arrow{color:var(--muted);font-size:16px;}
.hm-empty{padding:18px 14px;text-align:center;color:var(--muted);font-size:13px;}

/* mobile drawer + bottomnav */
.mobile-drawer{display:none;position:fixed;inset:0;z-index:100;}
.mobile-drawer.open{display:block;}
.mobile-drawer .overlay{position:absolute;inset:0;background:rgba(0,0,0,.4);}
.mobile-drawer .panel{position:absolute;left:0;top:0;bottom:0;width:250px;background:var(--navy);padding:26px 18px;color:#eaf2ff;overflow-y:auto;}
#bottomnav{display:none;}

/* ===== MOBILE ===== */
@media (max-width: 768px){
#pagewrap{height:auto;min-height:100vh;overflow-x:hidden;padding:12px 6px 84px 6px;gap:12px;}
#franjaA{flex:none;grid-template-columns:1fr;padding:6px;}
#sidebar{display:none;}
#mainpanel{padding:14px 14px;}
.hamburger{display:block;}
.mp-header .desktop-brand{display:none;}
.mp-header .greet h1{font-size:17px;}
.mp-qa{flex:none;}
#homeMobile{display:none !important;}
#mainpanel{overflow:visible;}
.cards-grid{grid-template-columns:1fr;gap:10px;}
.qa-card p{min-height:0;}
.kpi-row{grid-template-columns:repeat(2,1fr);gap:12px;}
.kpi-item:nth-child(3){border-left:none;}
#franjaB{flex:none;grid-template-columns:1fr;}
.preview-body{max-height:320px;}
#franjaC{flex:none;padding:16px 18px;}
#bottomnav{
display:flex;position:fixed;left:0;right:0;bottom:0;height:60px;
background:linear-gradient(180deg,#16264d 0%,#0b162f 100%);
border-top:1px solid rgba(255,255,255,.12);box-shadow:0 -8px 22px rgba(0,0,0,.28);z-index:50;position:fixed;
}
#bottomnav::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg, rgba(255,255,255,0), rgba(170,205,255,.45), rgba(255,255,255,0));}
#bottomnav .bn-item.active{position:relative;}
#bottomnav .bn-item.active::after{content:'';position:absolute;top:0;left:22%;right:22%;height:2px;border-radius:0 0 3px 3px;background:linear-gradient(90deg, rgba(138,180,255,0), #8ab4ff, rgba(138,180,255,0));box-shadow:0 0 10px rgba(138,180,255,.8);}
#bottomnav .bn-item{
flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
gap:3px;font-size:10.5px;color:rgba(234,242,255,.70);cursor:pointer;font-weight:600;
}
#bottomnav .bn-item.active{color:#8ab4ff;}
#bottomnav .bn-item .ic{font-size:18px;}
}
</style>
</head>
<body>
<div id="topbarMobile">
<button class="tb-burger" id="tbBurger" aria-label="Men&uacute;">&#9776;</button>
<div class="tb-brand"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:48px;width:auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 10px rgba(120,170,255,.40));"/></div>
<button class="tb-bell" id="tbBell" aria-label="Avisos">&#128276;<span class="dot" id="tbBellDot"></span></button>
</div>

<div id="pagewrap">

<div id="franjaA">
<div id="sidebar">
<div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
<div id="navList"></div>
</div>
<div id="mainpanel">
<div class="mp-header">
<div class="greet">
<h1>&iexcl;Bienvenido, __USER_NAME__!</h1>
<p>Rol: __ROLE_DISPLAY__ &bull; DNI: __USER_DNI__</p>
</div>
<div class="mp-right">
<div class="desktop-brand"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
<div class="bell">&#128276;<span class="dot" id="bellDot" style="display:none;">0</span></div>
<button class="hamburger" id="hamburgerBtn">&#9776;</button>
</div>
</div>
<div id="homeMobile"></div>
<div class="mp-qa">
<h2>Accesos r&aacute;pidos</h2>
<div class="cards-grid" id="cardsGrid"></div>
</div>
<div class="kpi-row" id="kpiRow">
<div class="kpi-item"><div class="kpi-icon">&#128101;</div><div><p class="lab">Total Socorristas</p><p class="val" id="kpiSocorristas">&ndash;</p></div></div>
<div class="kpi-item"><div class="kpi-icon">&#128197;</div><div><p class="lab">Turnos esta semana</p><p class="val" id="kpiTurnos">&ndash;</p></div></div>
<div class="kpi-item"><div class="kpi-icon">&#127970;</div><div><p class="lab">Instalaciones activas</p><p class="val" id="kpiInstalaciones">&ndash;</p></div></div>
<div class="kpi-item"><div class="kpi-icon">&#128172;</div><div><p class="lab">Mensajes no le&iacute;dos</p><p class="val" id="kpiMensajes">&ndash;</p></div></div>
</div>
</div>
</div>

<div class="mobile-drawer" id="drawer">
<div class="overlay" id="drawerOverlay"></div>
<div class="panel">
<div class="logo-row"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
<div id="navListMobile"></div>
</div>
</div>

<div id="franjaB">
<div class="preview-card">
<div class="preview-head">
<div class="t"><span class="ph-ic">&#9776;</span> Calendario de Turnos</div>
<button class="more" data-go="/calendario">Ver m&aacute;s &rarr;</button>
</div>
<div class="preview-body" id="previewCalendario" style="padding:0;">
<div class="empty-note">Cargando...</div>
</div>
</div>

<div class="preview-card">
<div class="preview-head">
<div class="t"><span class="ph-ic">&#9776;</span> Incidencias y Comunicados</div>
<button class="more" data-go="/chat_interfaz">Ver m&aacute;s &rarr;</button>
</div>
<div class="preview-body" id="previewChat">
<div class="empty-note">Cargando...</div>
</div>
</div>

<div class="preview-card">
<div class="preview-head">
<div class="t"><span class="ph-ic">&#9776;</span> Gesti&oacute;n de Horarios</div>
<button class="more" data-go="/editar_horarios">Ver m&aacute;s &rarr;</button>
</div>
<div class="mini-tabs" id="horariosMiniTabs" style="display:none;">
<div class="mini-tab active">Bloques</div>
<div class="mini-tab">Asignaciones</div>
<div class="mini-tab">Historial</div>
</div>
<div class="preview-body" id="previewHorarios">
<div class="empty-note">Cargando...</div>
</div>
</div>

<div class="preview-card">
<div class="preview-head">
<div class="t"><span class="ph-ic">&#9776;</span> Registro de Personal</div>
<button class="more" data-go="/altas_registro">Ver m&aacute;s &rarr;</button>
</div>
<div class="preview-body" id="previewRegistro">
<div class="empty-note">Cargando...</div>
</div>
</div>
</div>

<div id="franjaC">
<div class="brand"><img class="brand-mark" src="__LOGO_URL__" alt="SYNTRA" style="height:46px;width:auto;flex:0 0 auto;display:block;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(120,170,255,.35));"/></div>
<div>Sistema de gesti&oacute;n de turnos y comunicaci&oacute;n interna para socorristas</div>
<div>&copy; 2025 SYNTRA</div>
</div>

<div id="bottomnav">
<div class="bn-item active"><span class="ic">&#8962;</span>Inicio</div>
<div class="bn-item" data-goto="/calendario"><span class="ic">&#128197;</span>Horarios</div>
<div class="bn-item" data-goto="/chat_interfaz"><span class="ic">&#128172;</span>Chat</div>
<div class="bn-item" id="masBtn"><span class="ic">&#8942;</span>M&aacute;s</div>
</div>

</div>
<script>
__SYNTRA_NAV__
(function(){
var API_BASE = __API_BASE__;
var USER_NAME = __USER_NAME_JS__;
var USER_ROLE = __USER_ROLE_JS__;
var USER_DNI = __USER_DNI_JS__;
var CAN_MANAGE_SCHEDULES = __CAN_MANAGE_SCHEDULES__;
var CAN_REGISTER_USERS = __CAN_REGISTER_USERS__;

function qs(){
var p = new URLSearchParams();
p.set("auth", "ok");
p.set("usuario", USER_NAME);
p.set("rol", USER_ROLE);
p.set("dni", USER_DNI);
return "?" + p.toString();
}

function goToPage(path){ syntraGoTo(path, function(){ window.open(path + qs(), "_blank"); }); }

var NAV_ITEMS = [
{label:"Inicio", icon:"&#8962;", go:"/", active:true},
{label:"Horarios", icon:"&#128197;", go:"/calendario"},
{label:"Incidencias y Comunicados", icon:"&#128172;", go:"/chat_interfaz"},
{sep:true},
{label:"Registro", icon:"&#128100;+", go:"/altas_registro", adminOnly:true, badge:"Solo admin"},
{label:"Gesti&oacute;n de Horarios", icon:"&#9881;", go:"/editar_horarios", adminOnly:true, badge:"Solo admin"},
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
if (lo) lo.addEventListener("click", function(){ syntraTopNav("/admin"); });
}

renderNav("navList");
renderNav("navListMobile");

var CARDS = [
{
icon:"&#128197;", title:"Horarios", desc:"Consulta tus turnos y horarios asignados.",
btn:"Ver horarios &rarr;", go:"/calendario", locked:false
},
{
icon:'<svg viewBox="0 0 48 48" width="34" height="34" aria-hidden="true"><path fill="#ffffff" d="M24 7c-9.4 0-17 7.2-17 16.1 0 3.1.9 6 2.6 8.5L7 41l9.8-2.5c2.2 1.1 4.7 1.7 7.2 1.7 9.4 0 17-7.2 17-16.1S33.4 7 24 7z"/><path fill="#25D366" d="M24 9.5c-8 0-14.5 6.1-14.5 13.6 0 2.9 1 5.6 2.6 7.8l-1.2 4.4 4.6-1.2c2.1 1.3 4.7 2.1 7.4 2.1 8 0 14.5-6.1 14.5-13.6S32 9.5 24 9.5z"/><path fill="#ffffff" d="M19.6 16.4c-.3-.7-.6-.7-.9-.7h-.8c-.3 0-.8.1-1.2.6-.4.5-1.6 1.5-1.6 3.6s1.6 4.2 1.9 4.5c.2.3 3.1 4.9 7.7 6.7 3.8 1.5 4.6 1.2 5.4 1.1.8-.1 2.6-1 3-2 .4-1 .4-1.8.3-2-.1-.2-.4-.3-.8-.5-.4-.2-2.6-1.3-3-1.4-.4-.1-.7-.2-1 .2-.3.5-1.1 1.4-1.4 1.7-.3.3-.5.3-.9.1-.4-.2-1.9-.7-3.6-2.2-1.3-1.2-2.2-2.6-2.5-3.1-.3-.5 0-.7.2-.9.2-.2.4-.5.6-.8.2-.3.3-.5.4-.8.1-.3.1-.6 0-.8-.1-.2-1-2.6-1.4-3.5z"/></svg>', iconCls:"qa-icon-chat", title:"Incidencias y Comunicados", desc:"Comun&iacute;cate con tu equipo o por instalaciones.",
btn:"Abrir chat &rarr;", go:"/chat_interfaz", locked:false
},
{
icon:"&#128100;+", title:"Registro de Personal", desc:"Registra nuevos socorristas y personal.",
btn:"Ir al registro &rarr;", go:"/altas_registro", locked:!CAN_REGISTER_USERS, pill:"Solo administradores"
},
{
icon:"&#9881;", title:"Gesti&oacute;n de Horarios", desc:"Crear, editar o eliminar bloques de turnos.",
btn:"Gestionar &rarr;", go:"/editar_horarios", locked:!CAN_MANAGE_SCHEDULES, pill:"Solo administradores"
},
];

var grid = document.getElementById("cardsGrid");
CARDS.forEach(function(c){
var div = document.createElement("div");
div.className = "qa-card";
div.innerHTML =
'<div class="qa-top"><div class="qa-icon' + (c.iconCls ? " " + c.iconCls : "") + '">' + c.icon + '</div>' +
'<div class="qa-textcol"><h3>' + c.title + '</h3>' +
'<p>' + c.desc + '</p></div></div>' +
(c.pill ? '<span class="qa-pill">' + c.pill + '</span>' : '') +
'<button class="qa-btn"' + (c.locked ? ' disabled' : '') + '>' + c.btn + '</button>';
if (!c.locked){
div.querySelector(".qa-btn").addEventListener("click", function(){ goToPage(c.go); });
}
grid.appendChild(div);
});

document.querySelectorAll(".preview-head .more[data-go]").forEach(function(btn){
btn.addEventListener("click", function(){ goToPage(btn.getAttribute("data-go")); });
});

var drawer = document.getElementById("drawer");
var hamburgerBtn = document.getElementById("hamburgerBtn");
var drawerOverlay = document.getElementById("drawerOverlay");
if (hamburgerBtn) hamburgerBtn.addEventListener("click", function(){ drawer.classList.add("open"); });
if (drawerOverlay) drawerOverlay.addEventListener("click", function(){ drawer.classList.remove("open"); });

var tbBurger = document.getElementById("tbBurger");
if (tbBurger) tbBurger.addEventListener("click", function(){ drawer.classList.add("open"); });
var tbBell = document.getElementById("tbBell");
if (tbBell) tbBell.addEventListener("click", function(){ goToPage("/chat_interfaz"); });

document.querySelectorAll("#bottomnav .bn-item[data-goto]").forEach(function(node){
node.addEventListener("click", function(){ goToPage(node.getAttribute("data-goto")); });
});
var masBtn = document.getElementById("masBtn");
if (masBtn) masBtn.addEventListener("click", function(){ drawer.classList.add("open"); });

var HOME = {dash:null, rows:null, threads:null};
var HM_DIAS = ["Dom","Lun","Mar","Mi\u00e9","Jue","Vie","S\u00e1b"];
var HM_DIAS_L = ["domingo","lunes","martes","mi\u00e9rcoles","jueves","viernes","s\u00e1bado"];

function hmNorm(v){ return String(v||"").trim().toLowerCase(); }

function hmTurno(ingreso){
var h = parseInt((ingreso || "0").split(":")[0], 10);
if (h < 13) return "Ma\u00f1ana";
if (h < 19) return "Tarde";
return "Noche";
}

function hmMisFilas(rows){
return rows.filter(function(r){
var inst = hmNorm(r["Instalacion"]);
if (!inst || inst === "descanso") return false;
var dni = hmNorm(r["DNI"] || r["dni"]);
if (dni && dni === hmNorm(USER_DNI)) return true;
return hmNorm(r["Socorrista"]) === hmNorm(USER_NAME);
});
}

function hmEsc(t){ return String(t||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

function renderHome(){
var box = document.getElementById("homeMobile");
if (!box) return;
var rows = HOME.rows || [];
var hoy = new Date(); hoy.setHours(0,0,0,0);
var mias = hmMisFilas(rows);
var esAdmin = CAN_MANAGE_SCHEDULES;
var base = esAdmin ? rows.filter(function(r){ var i = hmNorm(r["Instalacion"]); return i && i !== "descanso"; }) : mias;

var proximos = base.map(function(r){
var f = parseFecha(r["Fecha"]);
return f ? {f:f, r:r} : null;
}).filter(function(x){ return x && x.f >= hoy; }).sort(function(a,b){
if (a.f - b.f !== 0) return a.f - b.f;
return String(a.r["Ingreso"]||"").localeCompare(String(b.r["Ingreso"]||""));
});

var deHoy = proximos.filter(function(x){ return ymd(x.f) === ymd(hoy); });
var html = "";

if (!esAdmin){
if (proximos.length){
var p = proximos[0];
var esHoy = ymd(p.f) === ymd(hoy);
html += '<div class="hm-hero">' +
'<div class="lab">' + (esHoy ? "Tu turno de hoy" : "Tu pr\u00f3ximo turno") + '</div>' +
'<div class="big">' + hmEsc(p.r["Ingreso"]||"--:--") + " &ndash; " + hmEsc(p.r["Salida"]||"--:--") + '</div>' +
'<div class="sub">&#127958; ' + hmEsc(p.r["Instalacion"]||"") + '</div>' +
'<div class="chips"><span class="hm-chip">' + (esHoy ? "Hoy" : HM_DIAS_L[p.f.getDay()] + " " + p.f.getDate()) + '</span>' +
'<span class="hm-chip">' + hmTurno(p.r["Ingreso"]) + '</span></div>' +
'</div>';
} else {
html += '<div class="hm-hero"><div class="lab">Tus turnos</div><div class="big">Sin turnos asignados</div>' +
'<div class="sub">Cuando te asignen un turno aparecer\u00e1 aqu\u00ed.</div></div>';
}
} else {
var instHoy = {};
deHoy.forEach(function(x){ instHoy[x.r["Instalacion"]] = true; });
html += '<div class="hm-hero"><div class="lab">Cobertura de hoy</div>' +
'<div class="big">' + deHoy.length + (deHoy.length === 1 ? " turno" : " turnos") + '</div>' +
'<div class="sub">' + Object.keys(instHoy).length + (Object.keys(instHoy).length === 1 ? ' instalaci\u00f3n con personal hoy' : ' instalaciones con personal hoy') + '</div>' +
'<div class="chips"><span class="hm-chip">Semana: ' + ((HOME.dash && HOME.dash.turnos_semana) || base.length) + ' turnos</span>' +
'<span class="hm-chip">' + ((HOME.dash && HOME.dash.total_socorristas) || "-") + ' socorristas</span></div></div>';
}

// tira de la semana
var ws = startOfWeek(new Date());
var semana = "";
for (var i = 0; i < 7; i++){
var d = new Date(ws); d.setDate(ws.getDate() + i);
var key = ymd(d);
var tiene = base.some(function(r){ var f = parseFecha(r["Fecha"]); return f && ymd(f) === key; });
semana += '<div class="hm-day' + (key === ymd(hoy) ? " today" : "") + '" data-go="/calendario">' +
'<span class="w">' + HM_DIAS[d.getDay()] + '</span><span class="n">' + d.getDate() + '</span>' +
'<span class="d' + (tiene ? "" : " off") + '"></span></div>';
}
html += '<div class="hm-sec">' + (esAdmin ? "Semana del equipo" : "Tu semana") + '<a href="#" data-go="/calendario">Ver horarios &rarr;</a></div>';
html += '<div class="hm-week">' + semana + '</div>';

// tarjetas de cifras
var sinLeer = (HOME.dash && HOME.dash.mensajes_no_leidos) || (HOME.threads || []).reduce(function(a,t){ return a + (t.unread_count||0); }, 0);
if (esAdmin){
html += '<div class="hm-tiles">' +
'<div class="hm-tile" data-go="/altas_registro"><div class="v">' + ((HOME.dash && HOME.dash.total_socorristas) || "-") + '</div><div class="l">Socorristas</div></div>' +
'<div class="hm-tile" data-go="/calendario"><div class="v">' + ((HOME.dash && HOME.dash.instalaciones_activas) || Object.keys(instHoy).length) + '</div><div class="l">Instalaciones activas</div></div>' +
'</div>';
} else {
var miSemana = base.filter(function(r){
var f = parseFecha(r["Fecha"]);
if (!f) return false;
var fin = new Date(ws); fin.setDate(ws.getDate() + 6);
return f >= ws && f <= fin;
}).length;
html += '<div class="hm-tiles">' +
'<div class="hm-tile" data-go="/calendario"><div class="v">' + miSemana + '</div><div class="l">Tus turnos esta semana</div></div>' +
'<div class="hm-tile" data-go="/chat_interfaz"><div class="v">' + sinLeer + '</div><div class="l">Mensajes sin leer</div></div>' +
'</div>';
}

// mensajes recientes
html += '<div class="hm-sec">Mensajes<a href="#" data-go="/chat_interfaz">Abrir chat &rarr;</a></div>';
var th = (HOME.threads || []).slice(0, 3);
if (!th.length){
html += '<div class="hm-list"><div class="hm-empty">Sin conversaciones a\u00fan.</div></div>';
} else {
html += '<div class="hm-list">' + th.map(function(t){
var ini = (t.title || "?").charAt(0).toUpperCase();
var prev = String(t.last_message || "");
if (prev.indexOf("[[adj:image:") === 0) prev = "\u00a0Imagen adjunta";
else if (prev.indexOf("[[adj:audio:") === 0) prev = "\u00a0Nota de voz";
return '<div class="hm-row" data-go="/chat_interfaz">' +
'<div class="hm-av">' + (t.type === "installation" ? "&#127970;" : ini) + '</div>' +
'<div class="info"><div class="t">' + hmEsc(t.title) + '</div><div class="s">' + hmEsc(prev) + '</div></div>' +
(t.unread_count > 0 ? '<span class="hm-badge">' + t.unread_count + '</span>' : '<span class="hm-arrow">&rsaquo;</span>') +
'</div>';
}).join("") + '</div>';
}

if (esAdmin){
html += '<div class="hm-sec">Administraci\u00f3n</div><div class="hm-list">' +
'<div class="hm-row" data-go="/editar_horarios"><div class="hm-av">&#9881;</div><div class="info"><div class="t">Gesti\u00f3n de Horarios</div><div class="s">Crear, editar o eliminar bloques</div></div><span class="hm-arrow">&rsaquo;</span></div>' +
'<div class="hm-row" data-go="/altas_registro"><div class="hm-av">&#128100;</div><div class="info"><div class="t">Registro de Personal</div><div class="s">Registrar socorristas y personal</div></div><span class="hm-arrow">&rsaquo;</span></div>' +
'</div>';
}

box.innerHTML = html;
box.querySelectorAll("[data-go]").forEach(function(n){
n.addEventListener("click", function(e){ e.preventDefault(); goToPage(n.getAttribute("data-go")); });
});
}

fetch(API_BASE + "/api/dashboard?dni=" + encodeURIComponent(USER_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
if (!d || !d.ok) return;
HOME.dash = d;
renderHome();
document.getElementById("kpiSocorristas").textContent = d.total_socorristas;
document.getElementById("kpiTurnos").textContent = d.turnos_semana;
document.getElementById("kpiInstalaciones").textContent = d.instalaciones_activas;
document.getElementById("kpiMensajes").textContent = d.mensajes_no_leidos;
if (d.mensajes_no_leidos > 0){
var dot = document.getElementById("bellDot");
dot.style.display = "inline-block";
dot.textContent = d.mensajes_no_leidos;
var dot2 = document.getElementById("tbBellDot");
if (dot2){ dot2.style.display = "inline-block"; dot2.textContent = d.mensajes_no_leidos; }
}
})
.catch(function(){});

function turnoClass(ingreso){
var h = parseInt((ingreso || "0").split(":")[0], 10);
if (h < 13) return "manana";
if (h < 19) return "tarde";
return "noche";
}
function parseFecha(str){
str = (str || "").trim();
if (!str) return null;
var parts = str.split("/");
if (parts.length === 3){
return new Date(parseInt(parts[2],10), parseInt(parts[1],10)-1, parseInt(parts[0],10));
}
return null;
}
function ymd(d){
return d.getFullYear() + "-" + String(d.getMonth()+1).padStart(2,"0") + "-" + String(d.getDate()).padStart(2,"0");
}
function startOfWeek(d){
var day = d.getDay();
var diff = (day === 0 ? -6 : 1) - day;
var res = new Date(d);
res.setDate(d.getDate() + diff);
res.setHours(0,0,0,0);
return res;
}

var DIAS_CORTO = ["Dom","Lun","Mar","Mie","Jue","Vie","Sab"];

fetch(API_BASE + "/api/mallas")
.then(function(r){ return r.json(); })
.then(function(d){
var rows = (d && d.ok && d.rows) ? d.rows : [];
HOME.rows = rows;
renderHome();
var wStart = startOfWeek(new Date());
var days = [];
for (var i = 0; i < 7; i++){
var dd = new Date(wStart);
dd.setDate(wStart.getDate() + i);
days.push(dd);
}
var weekKeys = days.map(ymd);

var filtered = rows.filter(function(r){
var inst = (r["Instalacion"] || "").trim();
if (!inst || inst.toLowerCase() === "descanso") return false;
var fd = parseFecha(r["Fecha"]);
if (!fd) return false;
return weekKeys.indexOf(ymd(fd)) !== -1;
});

var instSet = {};
filtered.forEach(function(r){ instSet[r["Instalacion"]] = true; });
var instalaciones = Object.keys(instSet).sort().slice(0, 5);

var wrap = document.getElementById("previewCalendario");
if (!instalaciones.length){
wrap.innerHTML = '<div class="empty-note">Sin turnos programados esta semana.</div>';
return;
}

var headHtml = "<th>Instalaci&oacute;n</th>" + days.map(function(dd){
return "<th>" + DIAS_CORTO[dd.getDay()] + " " + dd.getDate() + "</th>";
}).join("");

var bodyHtml = instalaciones.map(function(inst){
var cells = days.map(function(dd){
var key = ymd(dd);
var matches = filtered.filter(function(r){
var rd = parseFecha(r["Fecha"]);
return r["Instalacion"] === inst && rd && ymd(rd) === key;
});
if (!matches.length) return "<td></td>";
var chips = matches.slice(0,2).map(function(r){
var cls = turnoClass(r["Ingreso"]);
return "<div class='mini-cal-chip " + cls + "'>" + (r["Ingreso"]||"") + "</div>";
}).join("");
return "<td>" + chips + "</td>";
}).join("");
return "<tr><td class='inst'>" + inst + "</td>" + cells + "</tr>";
}).join("");

wrap.innerHTML = "<table class='mini-cal'><thead><tr>" + headHtml + "</tr></thead><tbody>" + bodyHtml + "</tbody></table>";
})
.catch(function(){
document.getElementById("previewCalendario").innerHTML = '<div class="empty-note">Error al cargar.</div>';
});

fetch(API_BASE + "/api/chat/threads?user_id=" + encodeURIComponent(USER_DNI))
.then(function(r){ return r.json(); })
.then(function(d){
var threads = (d && d.ok && d.threads) ? d.threads : [];
HOME.threads = threads;
renderHome();
var wrap = document.getElementById("previewChat");
if (!threads.length){
wrap.innerHTML = '<div class="empty-note">Sin conversaciones a&uacute;n.</div>';
return;
}
wrap.innerHTML = threads.slice(0, 4).map(function(t){
var unread = t.unread_count > 0 ? '<span class="mini-unread">' + t.unread_count + '</span>' : "";
var init = (t.title || "?").charAt(0).toUpperCase();
var prev = String(t.last_message || "");
if (prev.indexOf("[[adj:image:") === 0) prev = "Imagen adjunta";
else if (prev.indexOf("[[adj:audio:") === 0) prev = "Nota de voz";
return '<div class="mini-thread"><div class="mini-avatar">' + (t.type === "installation" ? "&#127970;" : init) + '</div>' +
'<div class="info"><div class="title">' + (t.title||"") + '</div><div class="sub">' + prev + '</div></div>' + unread + '</div>';
}).join("");
})
.catch(function(){
document.getElementById("previewChat").innerHTML = '<div class="empty-note">Error al cargar.</div>';
});

if (CAN_MANAGE_SCHEDULES){
document.getElementById("horariosMiniTabs").style.display = "flex";
fetch(API_BASE + "/api/bloques")
.then(function(r){ return r.json(); })
.then(function(d){
var rows = (d && d.ok && d.rows) ? d.rows : [];
var groups = {};
rows.forEach(function(r){
var key = (r["Instalacion"]||"") + "|" + (r["bloque"]||"") + "|" + (r["Dia"]||"");
if (!groups[key]) groups[key] = {inst:r["Instalacion"], bloque:r["bloque"], dia:r["Dia"]};
});
var list = Object.keys(groups).map(function(k){ return groups[k]; });
var wrap = document.getElementById("previewHorarios");
if (!list.length){
wrap.innerHTML = '<div class="empty-note">Sin bloques configurados.</div>';
return;
}
wrap.innerHTML = '<table class="mini-table"><thead><tr><th>Instalaci&oacute;n</th><th>Bloque</th><th>D&iacute;a</th></tr></thead><tbody>' +
list.slice(0, 6).map(function(g){
return '<tr><td>' + g.inst + '</td><td>Bloque ' + g.bloque + '</td><td>' + g.dia + '</td></tr>';
}).join("") + '</tbody></table>';
})
.catch(function(){
document.getElementById("previewHorarios").innerHTML = '<div class="empty-note">Error al cargar.</div>';
});
} else {
document.getElementById("previewHorarios").innerHTML = '<div class="locked-note">&#128274; Solo administradores</div>';
}

if (CAN_REGISTER_USERS){
var wrap = document.getElementById("previewRegistro");
wrap.innerHTML =
'<div class="mini-form">' +
'<div class="field"><label>Nombre completo</label><input id="mf_nombre"/></div>' +
'<div class="mini-form-grid">' +
'<div class="field"><label>DNI</label><input id="mf_dni"/></div>' +
'<div class="field"><label>Correo electr&oacute;nico</label><input id="mf_correo"/></div>' +
'<div class="field"><label>Tel&eacute;fono</label><input id="mf_telefono"/></div>' +
'<div class="field"><label>Instalaci&oacute;n</label><input id="mf_instalacion"/></div>' +
'<div class="field"><label>Tipo de contrato</label><select id="mf_contrato"><option value="">Selecciona</option><option>Fijo</option><option>Temporal</option><option>Media jornada</option></select></div>' +
'<div class="field"><label>Fecha de inicio</label><input id="mf_fecha_inicio" type="date"/></div>' +
'</div>' +
'<div class="field"><label>Rol</label><select id="mf_rol"><option value="">Selecciona</option><option>Socorrista</option><option>Directivo</option><option>Administrador</option></select></div>' +
'<div class="mini-msg" id="mfMsg"></div>' +
'<button class="mini-save-btn" id="mfSaveBtn">Guardar</button>' +
'</div>';

document.getElementById("mfSaveBtn").addEventListener("click", function(){
var nombre = document.getElementById("mf_nombre").value.trim();
var dni = document.getElementById("mf_dni").value.trim();
var msgEl = document.getElementById("mfMsg");
if (!nombre || !dni){
msgEl.className = "mini-msg err"; msgEl.textContent = "Nombre y DNI son obligatorios.";
return;
}
var payload = {
nombre: nombre,
dni: dni,
correo: document.getElementById("mf_correo").value.trim(),
tlf: document.getElementById("mf_telefono").value.trim(),
instalacion: document.getElementById("mf_instalacion").value.trim(),
contrato: document.getElementById("mf_contrato").value,
fecha_inicio: document.getElementById("mf_fecha_inicio").value,
rol: document.getElementById("mf_rol").value
};
var btn = document.getElementById("mfSaveBtn");
btn.disabled = true; btn.textContent = "Guardando...";
fetch(API_BASE + "/api/altas/registro", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify(payload)
})
.then(function(r){ return r.json(); })
.then(function(d){
btn.disabled = false; btn.textContent = "Guardar";
if (d && d.ok){
msgEl.className = "mini-msg ok"; msgEl.textContent = "Registrado correctamente.";
["mf_nombre","mf_dni","mf_correo","mf_telefono","mf_instalacion","mf_fecha_inicio"].forEach(function(id){ document.getElementById(id).value = ""; });
document.getElementById("mf_rol").value = "";
document.getElementById("mf_contrato").value = "";
} else {
msgEl.className = "mini-msg err"; msgEl.textContent = (d && d.error) || "Error al guardar.";
}
})
.catch(function(){
btn.disabled = false; btn.textContent = "Guardar";
msgEl.className = "mini-msg err"; msgEl.textContent = "Error de conexion.";
});
});
} else {
document.getElementById("previewRegistro").innerHTML = '<div class="locked-note">&#128274; Solo administradores</div>';
}
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

html = html.replace("__SYNTRA_NAV__", NAV_JS)

components.html(html, height=860, scrolling=True)
