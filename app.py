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
.desktop-brand{display:inline-flex;align-items:center;gap:8px;font-weight:800;letter-spacing:1.5px;font-size:15px;color:#eaf2ff;background:linear-gradient(135deg,#182a54 0%,#0d1a37 100%);padding:6px 12px;border-radius:10px;box-shadow:0 5px 14px rgba(3,10,28,.20);}
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
@keyframes syntraSheen{0%{left:-45%;}55%{left:115%;}100%{left:115%;}}
.qa-btn{position:relative;overflow:hidden;}
.qa-btn:not([disabled])::after{content:'';position:absolute;top:0;left:-45%;width:38%;height:100%;
background:linear-gradient(105deg, rgba(255,255,255,0) 0%, rgba(190,215,255,.30) 45%, rgba(255,255,255,0) 100%);
transform:skewX(-18deg);animation:syntraSheen 7s ease-in-out infinite;pointer-events:none;}
.qa-btn:not([disabled]):active{transform:translateY(1px);box-shadow:0 0 0 3px rgba(138,180,255,.25);}
@media (prefers-reduced-motion: reduce){.qa-btn::after{animation:none;}}
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
#franjaC .brand{display:inline-flex;align-items:center;gap:7px;font-weight:800;letter-spacing:1.2px;color:#eaf2ff;font-size:12px;background:linear-gradient(135deg,#182a54 0%,#0d1a37 100%);padding:5px 10px;border-radius:10px;box-shadow:0 6px 16px rgba(3,10,28,.22);max-height:100%;}
#franjaC .brand img{width:20px;height:20px;object-fit:contain;border-radius:5px;}

/* ===== Barra superior fija (movil) ===== */
#topbarMobile{display:none;}
@media (max-width:768px){
#topbarMobile{
display:flex;position:fixed;left:0;right:0;top:0;height:60px;z-index:60;zoom:1.1;
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
#topbarMobile .tb-brand{position:absolute;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:8px;font-weight:800;letter-spacing:2px;font-size:16px;color:#eaf2ff;pointer-events:none;}
#topbarMobile .tb-bell{position:relative;background:none;border:0;font-size:19px;cursor:pointer;padding:4px;margin-left:auto;}
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
<div>&copy; 2026 SYNTRA</div>
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
