# pages/chat_interfaz.py
import json
from urllib.parse import urlencode

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
      [data-testid="stSidebar"], [data-testid="collapsedControl"]{display:none !important;}
      iframe{border:0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

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

USER_NAME = st.query_params.get("usuario") or st.query_params.get("user") or ""
USER_ROLE = st.query_params.get("rol") or st.query_params.get("role") or ""
USER_DNI = st.query_params.get("dni") or ""

if not USER_DNI:
    st.error("No se pudo identificar al usuario. Por favor, vuelve a iniciar sesión.")
    st.stop()

WORDPRESS_CHAT_URL = "https://www.meditaciondelyosoy.com/chat/"
WORDPRESS_CHAT_TARGET = WORDPRESS_CHAT_URL + "?" + urlencode(
    {
        "auth": "ok",
        "usuario": USER_NAME,
        "rol": USER_ROLE,
        "dni": USER_DNI,
    }
)
WORDPRESS_CHAT_TARGET_JSON = json.dumps(WORDPRESS_CHAT_TARGET, ensure_ascii=False)

st.markdown(
    f"""
    <style>
      #mobile-chat-redirect-cover{{
        display:none;
      }}

      @media (max-width:768px), (pointer:coarse) and (max-width:1024px){{
        #mobile-chat-redirect-cover{{
          position:fixed !important;
          inset:0 !important;
          z-index:2147483647 !important;
          display:grid !important;
          place-items:center !important;
          padding:22px !important;
          background:
            radial-gradient(900px 520px at 50% -10%, rgba(255,255,255,.16), transparent 60%),
            linear-gradient(180deg,#020614,#040e31) !important;
          color:#fff !important;
          font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif !important;
        }}

        #mobile-chat-redirect-cover .box{{
          width:min(420px,94vw);
          border:1px solid rgba(255,255,255,.14);
          border-radius:26px;
          padding:22px;
          text-align:center;
          background:rgba(255,255,255,.07);
          box-shadow:0 22px 55px rgba(0,0,0,.52);
        }}

        #mobile-chat-redirect-cover .title{{
          font-size:18px;
          font-weight:900;
          margin-bottom:8px;
        }}

        #mobile-chat-redirect-cover .txt{{
          font-size:13px;
          color:rgba(255,255,255,.68);
          margin-bottom:16px;
        }}

        #mobile-chat-redirect-cover .btn{{
          display:flex;
          align-items:center;
          justify-content:center;
          width:100%;
          height:46px;
          border-radius:999px;
          background:#008069;
          color:#fff !important;
          text-decoration:none !important;
          font-weight:900;
        }}
      }}
    </style>

    <div id="mobile-chat-redirect-cover">
      <div class="box">
        <div class="title">Abriendo chat móvil</div>
        <div class="txt">Redirección segura a WordPress con la sesión actual.</div>
        <a class="btn" href="{WORDPRESS_CHAT_TARGET}" target="_top" rel="noopener">Abrir chat móvil</a>
      </div>
    </div>

    <script>
      (function(){{
        var target = {WORDPRESS_CHAT_TARGET_JSON};
        var ua = navigator.userAgent || "";
        var width = Math.min(window.innerWidth || 9999, screen.width || 9999);
        var coarse = false;

        try{{
          coarse = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
        }}catch(e){{}}

        var mobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile/i.test(ua);
        var mobileWidth = width <= 768;
        var touchMobile = coarse && width <= 1024;

        if(!(mobileUA || mobileWidth || touchMobile)) return;

        function go(){{
          try{{ window.top.location.href = target; return; }}catch(e){{}}
          try{{ window.parent.location.href = target; return; }}catch(e){{}}
          try{{ window.location.href = target; return; }}catch(e){{}}
        }}

        go();
        setTimeout(go, 80);
        setTimeout(go, 300);
        setTimeout(go, 900);
      }})();
    </script>
    """,
    unsafe_allow_html=True,
)

components.html(
    f"""
    <script>
      (function(){{
        var target = {WORDPRESS_CHAT_TARGET_JSON};
        var ua = navigator.userAgent || "";
        var width = Math.min(window.innerWidth || 9999, screen.width || 9999);
        var coarse = false;

        try{{
          coarse = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
        }}catch(e){{}}

        var mobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile/i.test(ua);
        var mobileWidth = width <= 768;
        var touchMobile = coarse && width <= 1024;

        if(!(mobileUA || mobileWidth || touchMobile)) return;

        function go(){{
          try{{ window.top.location.href = target; return; }}catch(e){{}}
          try{{ window.parent.location.href = target; return; }}catch(e){{}}
          try{{ window.location.href = target; return; }}catch(e){{}}
        }}

        go();
        setTimeout(go, 80);
        setTimeout(go, 300);
        setTimeout(go, 900);
      }})();
    </script>
    """,
    height=0,
    width=0,
)

html = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
  <title>Chat</title>
  <style>
    :root{
      /* ===== PALETA ADMIN ===== */
      --baseBlue: #040e31;
      --bgTop:  #0a1a55;
      --bgMid:  #061240;
      --bgDeep: #02071c;
      --overlay1: rgba(40, 120, 255, .16);
      --overlay2: rgba(0,  10,  40, .62);
      --ink: rgba(255,255,255,.92);
      --shadow1: 0 22px 55px rgba(0,0,0,.55);
      --blur: 14px;

      /* ===== AJUSTES DE ALTURA (conservados) ===== */
      --top-row-h: 48px;
      --title-row-h: 44px;
      --input-row-h: 52px;
      --chat-shell-h-desktop: 70vh;
      --chat-shell-h-mobile: 62vh;

      /* ===== TIPOGRAFÍA WHATSAPP ===== */
      --font-main: 15px;
      --font-small: 12px;
      --font-title: 16px;
      --font-body: 14px;
      --send-w: 88px;
    }

    *{ box-sizing:border-box; margin:0; padding:0; }

    html, body{
      width:100%;
      height:100%;
      overflow:hidden;
      background: var(--baseBlue);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* ===== ESTRUCTURA EXTERIOR (IDÉNTICA A ADMIN.PY) ===== */
    #stage{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      background:
        radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
        linear-gradient(180deg, #020614 0%, var(--baseBlue) 100%);
    }

    #plan{
      position:absolute;
      left:10px; right:10px;
      top:10px; bottom:0;
      overflow:hidden;
      border-radius: 34px;
      box-shadow: var(--shadow1);
      background:
        linear-gradient(180deg, rgba(255,255,255,.16) 0%, transparent 22%),
        linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #05164d 58%, var(--bgDeep) 100%);
    }

    #plan::before{
      content:"";
      position:absolute;
      inset:-10%;
      background:
        linear-gradient(135deg,
          transparent 0%,
          transparent 32%,
          var(--overlay1) 32%,
          var(--overlay2) 66%,
          transparent 66%);
      transform: rotate(-10deg);
      opacity:.95;
      pointer-events:none;
    }

    #plan::after{
      content:"";
      position:absolute;
      inset:0;
      background:
        radial-gradient(50% 60% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
        radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
        linear-gradient(180deg, transparent 55%, rgba(0,0,0,.65) 100%);
      pointer-events:none;
    }

    #frame{
      position:absolute;
      left:9px; right:9px;
      top:10px; bottom:0;
      border-left: 2px solid rgba(255,255,255,.14);
      border-right:2px solid rgba(255,255,255,.14);
      border-top:  2px solid rgba(255,255,255,.14);
      box-sizing:border-box;
      pointer-events:none;
      border-radius: 34px;
      box-shadow: inset 0 0 0 1px rgba(0,0,0,.55);
    }

    #card{
      position:absolute;
      left:6%;
      right:6%;
      top:2%;
      bottom:6%;
    }

    #hud{
      position:absolute; inset:0;
      pointer-events:none;
      background:
        radial-gradient(60% 45% at 50% 18%, rgba(255,255,255,.12), transparent 60%),
        linear-gradient(180deg, transparent 62%, rgba(0,0,0,.30) 100%);
    }

    /* ===== CONTENEDOR INTERIOR ===== */
    .inner{
      width:100%;
      height:100%;
      display:flex;
      flex-direction:column;
      justify-content:flex-start;
      align-items:center;
      gap:16px;
      padding-top:16px;
    }

    /* ===== BOTONES SUPERIORES (ESTILO WHATSAPP) ===== */
    .top-buttons{
      display:flex;
      gap:8px;
      background: rgba(0,0,0,0.2);
      backdrop-filter: blur(8px);
      border-radius: 40px;
      padding: 4px;
      flex-shrink:0;
    }

    .top-btn{
      background: transparent;
      border: none;
      padding: 8px 20px;
      border-radius: 32px;
      font-size: var(--font-main);
      font-weight: 500;
      color: rgba(255,255,255,0.85);
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .top-btn.active{
      background: #008069;
      color: white;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }

    .btn-stack{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
    }
    .btn-topline{
      font-size: 10px;
      opacity: 0.7;
    }
    .btn-mainline{
      font-size: 14px;
      font-weight: 600;
    }

    /* ===== BLOQUE DEL CHAT (ESTILO WHATSAPP) ===== */
    .chat-shell{
      width: min(900px, 90%);
      height: var(--chat-shell-h-desktop);
      background: #efeae2;
      background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.03"><path fill="none" d="M0 0h100v100H0z"/><path fill="%23000" d="M10 10h80v80H10z"/></svg>');
      background-repeat: repeat;
      border-radius: 28px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 8px 20px rgba(0,0,0,0.2);
      backdrop-filter: blur(2px);
    }

    .chat-header{
      background: #f0f2f5;
      padding: 12px 20px;
      font-size: var(--font-title);
      font-weight: 500;
      color: #111b21;
      border-bottom: 1px solid #e9edef;
      flex-shrink: 0;
    }

    .messages-area{
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .message{
      max-width: 70%;
      padding: 8px 12px;
      border-radius: 18px;
      font-size: var(--font-body);
      line-height: 1.4;
      background: #ffffff;
      color: #111b21;
      box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
      align-self: flex-start;
    }

    .message.out{
      background: #d9f0c3;
      align-self: flex-end;
    }

    .message strong{
      display: block;
      font-size: 11px;
      font-weight: 500;
      margin-bottom: 4px;
      color: #54656f;
    }

    .input-area{
      background: #f0f2f5;
      padding: 8px 16px;
      display: flex;
      gap: 12px;
      align-items: center;
      border-top: 1px solid #e9edef;
      flex-shrink: 0;
    }

    #chatInput{
      flex: 1;
      border: none;
      border-radius: 24px;
      padding: 10px 16px;
      font-size: var(--font-body);
      background: white;
      outline: none;
    }

    #chatInput::placeholder{
      color: #8696a0;
    }

    #sendBtn{
      background: #008069;
      border: none;
      color: white;
      font-weight: 600;
      padding: 8px 20px;
      border-radius: 24px;
      cursor: pointer;
      transition: background 0.2s;
    }

    #sendBtn:active{
      background: #006b56;
    }

    /* ===== MODALES (ESTILO WHATSAPP) ===== */
    .selector-modal{
      position:fixed;
      top:0; left:0; right:0; bottom:0;
      background:rgba(0,0,0,0.5);
      display:none;
      align-items:center;
      justify-content:center;
      z-index:2000;
    }
    .selector-modal.show{ display:flex; }

    .selector-card{
      width: min(500px, 90%);
      max-height: 80vh;
      background: #fff;
      border-radius: 28px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 12px 28px rgba(0,0,0,0.2);
    }

    .selector-head{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
      border-bottom: 1px solid #e9edef;
    }
    .selector-title{
      font-size: 18px;
      font-weight: 600;
      color: #111b21;
    }
    .selector-close{
      background: transparent;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: #54656f;
    }

    .selector-search-wrap{
      padding: 12px 16px;
      border-bottom: 1px solid #e9edef;
    }
    .selector-search{
      width: 100%;
      padding: 10px 12px;
      border-radius: 24px;
      border: none;
      background: #f0f2f5;
      font-size: 14px;
      outline: none;
    }

    .selector-list{
      flex: 1;
      overflow-y: auto;
    }

    .selector-item, .selector-action{
      display: block;
      width: 100%;
      text-align: left;
      padding: 12px 16px;
      border: none;
      background: transparent;
      cursor: pointer;
      font-size: 15px;
      border-bottom: 1px solid #f0f2f5;
    }
    .selector-item:hover, .selector-action:hover{
      background: #f5f6f6;
    }
    .selector-item.active{
      background: #e9f0e8;
    }
    .selector-item-title{
      font-weight: 500;
      color: #111b21;
    }
    .selector-item-sub{
      font-size: 13px;
      color: #667781;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .section-label{
      padding: 12px 16px 4px;
      font-size: 12px;
      font-weight: 500;
      color: #667781;
      text-transform: uppercase;
    }

    /* Nuevo chat modal */
    .user-search-modal{
      position:fixed;
      top:0; left:0; right:0; bottom:0;
      background:rgba(0,0,0,0.5);
      display:flex;
      align-items:center;
      justify-content:center;
      z-index:2100;
    }
    .modal-content{
      background:#fff;
      width:90%;
      max-width:400px;
      border-radius:28px;
      padding:20px;
    }
    .modal-content h3{
      margin-bottom:16px;
      font-size:18px;
    }
    .modal-content input{
      width:100%;
      padding:12px;
      border-radius:24px;
      border:1px solid #e9edef;
      margin-bottom:16px;
      font-size:15px;
    }
    .user-list{
      max-height:300px;
      overflow-y:auto;
    }
    .user-item{
      padding:12px;
      cursor:pointer;
      border-bottom:1px solid #f0f2f5;
    }
    .user-item:hover{
      background:#f5f6f6;
    }
    .close-modal{
      float:right;
      font-size:24px;
      cursor:pointer;
    }

    #functionalLayer{ display:none !important; }

    /* ===== MÓVIL ===== */
    @media (max-width: 768px){
      :root{
        --top-row-h: 44px;
        --title-row-h: 40px;
        --input-row-h: 48px;
        --chat-shell-h-desktop: var(--chat-shell-h-mobile);
        --font-main: 13px;
        --font-small: 10px;
        --font-title: 14px;
        --font-body: 13px;
        --send-w: 76px;
      }
      .chat-shell{
        width: 96%;
        height: var(--chat-shell-h-mobile);
      }
      .top-btn{
        padding: 4px 12px;
      }
      .message{
        max-width: 85%;
      }
      .inner{
        padding-top: 8px;
        gap: 12px;
      }
    }

    /* Scrollbar */
    .messages-area::-webkit-scrollbar{
      width: 6px;
    }
    .messages-area::-webkit-scrollbar-track{
      background: #f0f2f5;
    }
    .messages-area::-webkit-scrollbar-thumb{
      background: #c1c9d0;
      border-radius: 3px;
    }

    /* ========== FULLSCREEN TOGGLE STYLES (solo móvil) ========== */
    .fullscreen-toggle {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 48px;
      height: 48px;
      background: rgba(0,0,0,0.6);
      backdrop-filter: blur(12px);
      border-radius: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      color: white;
      cursor: pointer;
      z-index: 10000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: all 0.2s ease;
      border: 1px solid rgba(255,255,255,0.2);
      font-weight: bold;
      user-select: none;
      touch-action: manipulation;
    }
    .fullscreen-toggle:active {
      transform: scale(0.92);
      background: rgba(0,0,0,0.8);
    }
    @media (min-width: 769px) {
      .fullscreen-toggle {
        display: none;
      }
    }
    @media (max-width: 768px) {
      .fullscreen-toggle {
        display: flex;
      }
    }
    html:fullscreen #stage.fullscreen-mode #plan,
    html:-webkit-full-screen #stage.fullscreen-mode #plan,
    html:-moz-full-screen #stage.fullscreen-mode #plan {
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      border-radius: 0;
      box-shadow: none;
    }
    html:fullscreen #stage.fullscreen-mode #frame,
    html:-webkit-full-screen #stage.fullscreen-mode #frame,
    html:-moz-full-screen #stage.fullscreen-mode #frame {
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      border-radius: 0;
    }
  </style>
</head>
<body>
<div id="stage">
  <div id="plan">
    <div id="frame"></div>
    <div id="card">
      <div class="inner">

        <div class="top-buttons">
          <button class="top-btn" id="btnSocorristas" type="button">
            <div class="btn-stack">
              <span class="btn-topline">selecciona</span>
              <span class="btn-mainline">Socorristas</span>
            </div>
          </button>
          <button class="top-btn" id="btnInstalacion" type="button">
            <div class="btn-stack">
              <span class="btn-topline">selecciona</span>
              <span class="btn-mainline">Instalación</span>
            </div>
          </button>
          <button class="top-btn" id="btnNotificaciones" type="button">
            <div class="btn-center">Notificaciones</div>
          </button>
        </div>

        <div class="chat-shell">
          <div class="chat-header" id="chatHeader">Nombre del socorrista o Grupo de instalación</div>
          <div class="messages-area" id="messagesArea">
            <div class="loading">Cargando conversaciones...</div>
          </div>
          <div class="input-area" id="inputArea">
            <input type="text" id="chatInput" placeholder="Mensaje" autocomplete="off">
            <button id="sendBtn">Enviar</button>
          </div>
        </div>

        <div id="functionalLayer">
          <div class="threads-panel">
            <div class="threads-header">
              <span>Conversaciones</span>
              <button class="new-chat-btn" id="newChatBtn">+ Nuevo</button>
            </div>
            <div class="thread-list" id="threadList">
              <div class="loading">Cargando conversaciones...</div>
            </div>
          </div>
        </div>

      </div>
    </div>
    <div id="hud"></div>
  </div>
</div>

<div class="selector-modal" id="selectorModal">
  <div class="selector-card">
    <div class="selector-head">
      <div class="selector-title" id="selectorTitle">Selección</div>
      <button class="selector-close" id="selectorClose" type="button">×</button>
    </div>
    <div class="selector-search-wrap">
      <input id="selectorSearch" class="selector-search" type="text" autocomplete="off" placeholder="Buscar">
    </div>
    <div class="selector-list" id="selectorList">
      <div class="loading">Cargando...</div>
    </div>
  </div>
</div>

<!-- Botón de pantalla completa (solo móvil) -->
<div id="fullscreenToggleBtn" class="fullscreen-toggle">⤢</div>

<script>
  const API_BASE = "https://camilo27.pythonanywhere.com/api/chat";
  const currentUserId = "REEMPLAZAR_DNI";
  let currentThreadId = null;
  let threads = [];
  let pollingInterval = null;
  let threadsPollingInterval = null;
  let lastRenderedMessageId = null;

  function escapeHtml(text) {
    return String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
  }

  async function fetchJSON(url, options = {}) {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} - ${response.statusText}`);
    }
    return response.json();
  }

  async function loadThreads() {
    const listDiv = document.getElementById("threadList");
    try {
      const data = await fetchJSON(API_BASE + "/threads?user_id=" + encodeURIComponent(currentUserId));
      threads = data.threads || [];
      renderThreadList();
      if (threads.length > 0 && !currentThreadId) {
        setActiveThread(threads[0].id);
      }
    } catch (error) {
      console.error("Error loading threads:", error);
      listDiv.innerHTML = '<div class="error">Error al cargar conversaciones.<br>' + escapeHtml(error.message) + '</div>';
    }
  }

  function renderThreadList() {
    const container = document.getElementById("threadList");
    if (threads.length === 0) {
      container.innerHTML = '<div style="padding: 12px; text-align: center;">No hay conversaciones</div>';
      return;
    }
    container.innerHTML = threads.map(function(t) {
      return '<div class="thread-item' + (currentThreadId == t.id ? ' active' : '') + '" data-id="' + t.id + '">' +
               '<div class="thread-title">' + escapeHtml(t.title || (t.type === 'private' ? 'Privado' : 'Grupo')) + '</div>' +
               '<div class="thread-preview">' + escapeHtml(t.last_message || '') + '</div>' +
             '</div>';
    }).join('');
    document.querySelectorAll('.thread-item').forEach(function(el) {
      el.addEventListener('click', function() { setActiveThread(el.getAttribute('data-id')); });
    });
  }

  async function loadMessages(threadId, poll = false) {
    const limit = poll ? 30 : 500;
    let url = API_BASE + "/threads/" + threadId + "/messages?user_id=" + encodeURIComponent(currentUserId) + "&limit=" + limit;
    try {
      const data = await fetchJSON(url);
      let messages = data.messages || [];
      if (poll && lastRenderedMessageId !== null) {
        messages = messages.filter(function(m) { return parseInt(m.id) > lastRenderedMessageId; });
      }
      const container = document.getElementById("messagesArea");
      if (!poll) {
        container.innerHTML = '';
        lastRenderedMessageId = null;
      }
      if (messages.length === 0 && !poll) {
        container.innerHTML = '<div style="text-align: center; margin-top: 20px;">No hay mensajes</div>';
        lastRenderedMessageId = null;
        return;
      }
      messages.forEach(function(msg) {
        const div = document.createElement("div");
        div.className = "message" + (msg.sender_id == currentUserId ? " out" : "");
        div.innerHTML = '<strong>' + escapeHtml(msg.sender_alias || 'Usuario') + ':</strong> ' + escapeHtml(msg.body);
        container.appendChild(div);
        lastRenderedMessageId = parseInt(msg.id);
      });
      container.scrollTop = container.scrollHeight;
      await markThreadRead(threadId);
    } catch (error) {
      console.error("Error loading messages:", error);
      const container = document.getElementById("messagesArea");
      if (!poll) container.innerHTML = '<div class="error">Error al cargar mensajes<br>' + escapeHtml(error.message) + '</div>';
    }
  }

  async function markThreadRead(threadId) {
    const messagesDiv = document.getElementById("messagesArea");
    const lastMsg = messagesDiv.querySelector(".message:last-child");
    if (!lastMsg) return;
    const lastId = lastMsg.getAttribute("data-id");
    if (!lastId) return;
    try {
      await fetch(API_BASE + "/threads/" + threadId + "/read", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: currentUserId, last_read_message_id: lastId })
      });
    } catch (error) {
      console.error("Error marking read:", error);
    }
  }

  async function sendMessage() {
    if (!currentThreadId) return;
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    try {
      await fetch(API_BASE + "/threads/" + currentThreadId + "/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender_id: currentUserId, body: text })
      });
      await loadMessages(currentThreadId, false);
    } catch (error) {
      console.error("Error sending message:", error);
      alert("Error al enviar mensaje: " + error.message);
    }
  }

  function setActiveThread(threadId) {
    currentThreadId = threadId;
    loadMessages(threadId, false);
    const thread = threads.find(function(t) { return t.id == threadId; });
    document.getElementById("chatHeader").innerText = thread ? (thread.title || (thread.type === 'private' ? 'Privado' : 'Grupo')) : "Conversación";
    document.getElementById("inputArea").style.display = "flex";
    renderThreadList();
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(function() {
      if (currentThreadId) loadMessages(currentThreadId, true);
    }, 10000);
  }

  function showNewChatModal() {
    const modal = document.createElement("div");
    modal.className = "user-search-modal";
    modal.innerHTML = `
      <div class="modal-content">
        <span class="close-modal">&times;</span>
        <h3>Nuevo chat</h3>
        <input type="text" id="userSearch" placeholder="Buscar por alias o DNI">
        <div id="userSearchResults" class="user-list">Escribe al menos 2 caracteres</div>
      </div>
    `;
    document.body.appendChild(modal);
    const closeBtn = modal.querySelector(".close-modal");
    closeBtn.onclick = function() { modal.remove(); };
    const searchInput = modal.querySelector("#userSearch");
    const resultsDiv = modal.querySelector("#userSearchResults");

    async function searchUsers() {
      const query = searchInput.value.trim().toLowerCase();
      if (query.length < 2) {
        resultsDiv.innerHTML = '<div>Escribe al menos 2 caracteres</div>';
        return;
      }
      try {
        const users = await fetchJSON(API_BASE + "/users");
        const filtered = users.filter(function(u) { return u.alias.toLowerCase().includes(query) || u.dni.includes(query); });
        if (filtered.length === 0) {
          resultsDiv.innerHTML = '<div>No se encontraron usuarios</div>';
          return;
        }
        resultsDiv.innerHTML = filtered.map(function(u) {
          return '<div class="user-item" data-dni="' + u.dni + '">@' + escapeHtml(u.alias) + ' (' + u.dni + ')</div>';
        }).join('');
        resultsDiv.querySelectorAll(".user-item").forEach(function(el) {
          el.addEventListener("click", async function() {
            const otherDni = el.getAttribute("data-dni");
            if (otherDni == currentUserId) {
              alert("No puedes chatear contigo mismo");
              return;
            }
            try {
              const data = await fetchJSON(API_BASE + "/private/" + encodeURIComponent(otherDni) + "?user_id=" + encodeURIComponent(currentUserId));
              if (data.thread_id) {
                setActiveThread(data.thread_id);
                modal.remove();
                await loadThreads();
              }
            } catch (error) {
              alert("Error al crear el chat: " + error.message);
            }
          });
        });
      } catch (error) {
        resultsDiv.innerHTML = '<div class="error">Error al cargar usuarios<br>' + escapeHtml(error.message) + '</div>';
      }
    }
    searchInput.addEventListener("input", searchUsers);
    searchUsers();
  }

  document.getElementById("newChatBtn").addEventListener("click", showNewChatModal);
  document.getElementById("sendBtn").addEventListener("click", sendMessage);
  document.getElementById("chatInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
  });

  let selectorMode = null;

  function setTopActive(mode) {
    document.getElementById("btnSocorristas").classList.remove("active");
    document.getElementById("btnInstalacion").classList.remove("active");
    document.getElementById("btnNotificaciones").classList.remove("active");

    if (mode === "socorristas") document.getElementById("btnSocorristas").classList.add("active");
    if (mode === "instalacion") document.getElementById("btnInstalacion").classList.add("active");
    if (mode === "notificaciones") document.getElementById("btnNotificaciones").classList.add("active");
  }

  function syncTopButtonsFromThread() {
    const thread = threads.find(function(t) { return String(t.id) === String(currentThreadId); });
    if (!thread) {
      setTopActive(null);
      return;
    }
    if (thread.type === "private") setTopActive("socorristas");
    else setTopActive("instalacion");
  }

  function openSelector(mode) {
    selectorMode = mode;
    document.getElementById("selectorModal").classList.add("show");
    renderSelector();
    setTimeout(function() {
      document.getElementById("selectorSearch").focus();
    }, 10);
  }

  function closeSelector() {
    document.getElementById("selectorModal").classList.remove("show");
    document.getElementById("selectorSearch").value = "";
    selectorMode = null;
    syncTopButtonsFromThread();
  }

  function getFilteredThreads() {
    const query = document.getElementById("selectorSearch").value.trim().toLowerCase();

    let list = threads.slice();

    if (selectorMode === "socorristas") {
      list = list.filter(function(t) { return t.type === "private"; });
    } else if (selectorMode === "instalacion") {
      list = list.filter(function(t) { return t.type !== "private"; });
    }

    if (!query) return list;

    return list.filter(function(t) {
      const title = String(t.title || (t.type === 'private' ? 'Privado' : 'Grupo')).toLowerCase();
      const preview = String(t.last_message || "").toLowerCase();
      return title.includes(query) || preview.includes(query);
    });
  }

  function renderSelector() {
    if (!selectorMode) return;

    const selectorTitle = document.getElementById("selectorTitle");
    const selectorSearch = document.getElementById("selectorSearch");
    const selectorList = document.getElementById("selectorList");

    if (selectorMode === "socorristas") {
      selectorTitle.innerText = "Socorristas";
      selectorSearch.placeholder = "Buscar conversación";
      setTopActive("socorristas");
    } else if (selectorMode === "instalacion") {
      selectorTitle.innerText = "Instalación";
      selectorSearch.placeholder = "Buscar conversación";
      setTopActive("instalacion");
    } else {
      selectorTitle.innerText = "Notificaciones";
      selectorSearch.placeholder = "Buscar conversación";
      setTopActive("notificaciones");
    }

    let html = "";

    if (selectorMode === "socorristas") {
      html += '<button class="selector-action" id="selectorNewChat">+ Nuevo chat</button>';
    }

    const list = getFilteredThreads();

    html += '<div class="section-label">Conversaciones</div>';

    if (list.length === 0) {
      html += '<div class="selector-empty">No hay conversaciones</div>';
    } else {
      html += list.map(function(t) {
        return '<button class="selector-item selector-thread' + (currentThreadId == t.id ? ' active' : '') + '" data-id="' + t.id + '">' +
                 '<div class="selector-item-title">' + escapeHtml(t.title || (t.type === 'private' ? 'Privado' : 'Grupo')) + '</div>' +
                 '<div class="selector-item-sub">' + escapeHtml(t.last_message || '') + '</div>' +
               '</button>';
      }).join('');
    }

    selectorList.innerHTML = html;

    const selectorNewChat = document.getElementById("selectorNewChat");
    if (selectorNewChat) {
      selectorNewChat.addEventListener("click", function() {
        closeSelector();
        document.getElementById("newChatBtn").click();
      });
    }

    document.querySelectorAll(".selector-thread").forEach(function(el) {
      el.addEventListener("click", function() {
        setActiveThread(el.getAttribute("data-id"));
        closeSelector();
      });
    });
  }

  const __originalLoadThreads = loadThreads;
  loadThreads = async function() {
    await __originalLoadThreads();
    syncTopButtonsFromThread();
    if (selectorMode) renderSelector();
  };

  const __originalSetActiveThread = setActiveThread;
  setActiveThread = function(threadId) {
    __originalSetActiveThread(threadId);
    syncTopButtonsFromThread();
    if (selectorMode) renderSelector();
  };

  document.getElementById("btnSocorristas").addEventListener("click", function() {
    openSelector("socorristas");
  });

  document.getElementById("btnInstalacion").addEventListener("click", function() {
    openSelector("instalacion");
  });

  document.getElementById("btnNotificaciones").addEventListener("click", function() {
    openSelector("notificaciones");
  });

  document.getElementById("selectorClose").addEventListener("click", closeSelector);

  document.getElementById("selectorModal").addEventListener("click", function(e) {
    if (e.target === document.getElementById("selectorModal")) {
      closeSelector();
    }
  });

  document.getElementById("selectorSearch").addEventListener("input", function() {
    renderSelector();
  });

  loadThreads();
  threadsPollingInterval = setInterval(loadThreads, 15000);

  // ==================== FULLSCREEN PERSISTENCE (solo móvil) ====================
  (function() {
    const stageEl = document.getElementById("stage");
    const toggleBtn = document.getElementById("fullscreenToggleBtn");
    const isMobile = window.innerWidth <= 768;

    function setFullscreenFlag(active) {
      if (active) {
        localStorage.setItem("fullscreenActive", "true");
      } else {
        localStorage.removeItem("fullscreenActive");
      }
    }

    function enterFullscreen() {
      const elem = document.documentElement;
      const requestMethod = elem.requestFullscreen || elem.webkitRequestFullscreen || elem.mozRequestFullScreen || elem.msRequestFullscreen;
      if (requestMethod) {
        requestMethod.call(elem).then(() => {
          if (stageEl) stageEl.classList.add("fullscreen-mode");
          if (toggleBtn) {
            toggleBtn.textContent = "✕";
            toggleBtn.style.fontSize = "26px";
          }
          setFullscreenFlag(true);
        }).catch(err => {
          console.log("Error al entrar en fullscreen:", err);
        });
      }
    }

    function exitFullscreen() {
      const exitMethod = document.exitFullscreen || document.webkitExitFullscreen || document.mozCancelFullScreen || document.msExitFullscreen;
      if (exitMethod) {
        exitMethod.call(document).then(() => {
          if (stageEl) stageEl.classList.remove("fullscreen-mode");
          if (toggleBtn) {
            toggleBtn.textContent = "⤢";
            toggleBtn.style.fontSize = "28px";
          }
          setFullscreenFlag(false);
        }).catch(err => {
          console.log("Error al salir de fullscreen:", err);
        });
      }
    }

    function toggleFullscreen() {
      const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
      if (isFull) {
        exitFullscreen();
      } else {
        enterFullscreen();
      }
    }

    function onFullscreenChange() {
      const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
      if (isFull) {
        if (stageEl) stageEl.classList.add("fullscreen-mode");
        if (toggleBtn) {
          toggleBtn.textContent = "✕";
          toggleBtn.style.fontSize = "26px";
        }
        setFullscreenFlag(true);
      } else {
        if (stageEl) stageEl.classList.remove("fullscreen-mode");
        if (toggleBtn) {
          toggleBtn.textContent = "⤢";
          toggleBtn.style.fontSize = "28px";
        }
        setFullscreenFlag(false);
      }
    }

    // Restaurar fullscreen si estaba activo (solo móvil)
    if (isMobile) {
      const savedFlag = localStorage.getItem("fullscreenActive");
      if (savedFlag === "true") {
        const isCurrentlyFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
        if (!isCurrentlyFull) {
          enterFullscreen();
        } else {
          // Asegurar UI
          if (stageEl) stageEl.classList.add("fullscreen-mode");
          if (toggleBtn) {
            toggleBtn.textContent = "✕";
            toggleBtn.style.fontSize = "26px";
          }
        }
      }
    }

    if (toggleBtn) {
      toggleBtn.addEventListener("click", function(e) {
        e.preventDefault();
        toggleFullscreen();
      });
    }

    document.addEventListener("fullscreenchange", onFullscreenChange);
    document.addEventListener("webkitfullscreenchange", onFullscreenChange);
    document.addEventListener("mozfullscreenchange", onFullscreenChange);
    document.addEventListener("MSFullscreenChange", onFullscreenChange);
  })();
  // ==================== FIN FULLSCREEN PERSISTENCE ====================
</script>
</body>
</html>
""".replace("REEMPLAZAR_DNI", USER_DNI)

components.html(html, height=800, scrolling=False)
