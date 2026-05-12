# pages/chat_interfaz.py
import json
from urllib.parse import urlencode

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ==========================================================
# GATE DE AUTENTICACIÓN
# ==========================================================
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

# ==========================================================
# CSS BASE + REDIRECCIÓN MÓVIL TEMPRANA
# ==========================================================
st.markdown(
    f"""
    <style>
      .block-container{{padding:0 !important;margin:0 !important;max-width:100% !important;}}
      section.main > div{{padding:0 !important;margin:0 !important;}}
      header, footer{{display:none !important;}}
      [data-testid="stSidebar"], [data-testid="collapsedControl"]{{display:none !important;}}
      iframe{{border:0 !important;}}

      @media (max-width: 900px){{
        .stApp{{
          opacity:0 !important;
          pointer-events:none !important;
          background:#020614 !important;
        }}
        html, body{{
          background:#020614 !important;
          overflow:hidden !important;
        }}
      }}
    </style>

    <script>
      (function(){{
        var target = {json.dumps(WORDPRESS_CHAT_TARGET, ensure_ascii=False)};
        var ua = navigator.userAgent || "";
        var isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile/i.test(ua);
        var isMobileWidth = window.innerWidth <= 900;
        var isTouchMobile = (navigator.maxTouchPoints || 0) > 1 && window.innerWidth <= 1024;

        if (isMobileUA || isMobileWidth || isTouchMobile) {{
          try {{
            window.location.replace(target);
          }} catch(e) {{
            window.location.href = target;
          }}

          setTimeout(function(){{
            try {{
              window.top.location.replace(target);
            }} catch(e) {{
              window.location.href = target;
            }}
          }}, 250);
        }}
      }})();
    </script>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# CHAT DE ESCRITORIO STREAMLIT
# ==========================================================
html = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
  <title>Chat</title>

  <style>
    :root{
      --baseBlue:#040e31;
      --bgTop:#0a1a55;
      --bgMid:#061240;
      --bgDeep:#02071c;
      --overlay1:rgba(40,120,255,.16);
      --overlay2:rgba(0,10,40,.62);
      --ink:rgba(255,255,255,.92);
      --muted:rgba(255,255,255,.62);
      --line:rgba(255,255,255,.12);
      --green:#008069;
      --shadow1:0 22px 55px rgba(0,0,0,.55);
      --font-main:15px;
      --font-title:16px;
      --font-body:14px;
    }

    *{
      box-sizing:border-box;
      margin:0;
      padding:0;
    }

    html,
    body{
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--baseBlue);
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    }

    #stage{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      background:
        radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
        linear-gradient(180deg,#020614 0%,var(--baseBlue) 100%);
    }

    #plan{
      position:absolute;
      left:10px;
      right:10px;
      top:10px;
      bottom:0;
      overflow:hidden;
      border-radius:34px;
      box-shadow:var(--shadow1);
      background:
        linear-gradient(180deg,rgba(255,255,255,.16) 0%,transparent 22%),
        linear-gradient(180deg,var(--bgTop) 0%,var(--bgMid) 34%,#05164d 58%,var(--bgDeep) 100%);
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
      transform:rotate(-10deg);
      opacity:.95;
      pointer-events:none;
    }

    #plan::after{
      content:"";
      position:absolute;
      inset:0;
      background:
        radial-gradient(50% 60% at 50% 25%,rgba(255,255,255,.06),transparent 55%),
        radial-gradient(120% 90% at 50% 95%,rgba(0,0,0,.55),transparent 55%),
        linear-gradient(180deg,transparent 55%,rgba(0,0,0,.65) 100%);
      pointer-events:none;
    }

    #frame{
      position:absolute;
      left:9px;
      right:9px;
      top:10px;
      bottom:0;
      border-left:2px solid rgba(255,255,255,.14);
      border-right:2px solid rgba(255,255,255,.14);
      border-top:2px solid rgba(255,255,255,.14);
      pointer-events:none;
      border-radius:34px;
      box-shadow:inset 0 0 0 1px rgba(0,0,0,.55);
      z-index:2;
    }

    #card{
      position:absolute;
      left:6%;
      right:6%;
      top:2%;
      bottom:6%;
      z-index:5;
    }

    #hud{
      position:absolute;
      inset:0;
      pointer-events:none;
      background:
        radial-gradient(60% 45% at 50% 18%,rgba(255,255,255,.12),transparent 60%),
        linear-gradient(180deg,transparent 62%,rgba(0,0,0,.30) 100%);
      z-index:4;
    }

    .inner{
      width:100%;
      height:100%;
      display:flex;
      flex-direction:column;
      justify-content:flex-start;
      align-items:center;
      gap:16px;
      padding-top:16px;
      position:relative;
      z-index:7;
    }

    .top-buttons{
      display:flex;
      gap:8px;
      background:rgba(0,0,0,.2);
      backdrop-filter:blur(8px);
      -webkit-backdrop-filter:blur(8px);
      border-radius:40px;
      padding:4px;
      flex-shrink:0;
    }

    .top-btn{
      background:transparent;
      border:none;
      padding:8px 20px;
      border-radius:32px;
      font-size:var(--font-main);
      font-weight:500;
      color:rgba(255,255,255,.85);
      cursor:pointer;
      transition:all .2s;
      display:flex;
      align-items:center;
      justify-content:center;
    }

    .top-btn.active{
      background:var(--green);
      color:white;
      box-shadow:0 2px 6px rgba(0,0,0,.2);
    }

    .btn-stack{
      display:flex;
      flex-direction:column;
      align-items:center;
      gap:2px;
    }

    .btn-topline{
      font-size:10px;
      opacity:.7;
    }

    .btn-mainline{
      font-size:14px;
      font-weight:600;
    }

    .chat-shell{
      width:min(900px,90%);
      height:70vh;
      background:#efeae2;
      background-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.03"><path fill="none" d="M0 0h100v100H0z"/><path fill="%23000" d="M10 10h80v80H10z"/></svg>');
      background-repeat:repeat;
      border-radius:28px;
      overflow:hidden;
      display:flex;
      flex-direction:column;
      box-shadow:0 8px 20px rgba(0,0,0,.2);
      backdrop-filter:blur(2px);
    }

    .chat-header{
      background:#f0f2f5;
      padding:12px 20px;
      font-size:var(--font-title);
      font-weight:500;
      color:#111b21;
      border-bottom:1px solid #e9edef;
      flex-shrink:0;
    }

    .messages-area{
      flex:1;
      overflow-y:auto;
      padding:16px;
      display:flex;
      flex-direction:column;
      gap:8px;
    }

    .message{
      max-width:70%;
      padding:8px 12px;
      border-radius:18px;
      font-size:var(--font-body);
      line-height:1.4;
      background:#fff;
      color:#111b21;
      box-shadow:0 1px .5px rgba(0,0,0,.13);
      align-self:flex-start;
      overflow-wrap:anywhere;
    }

    .message.out{
      background:#d9f0c3;
      align-self:flex-end;
    }

    .message.pending{
      opacity:.65;
    }

    .message strong{
      display:block;
      font-size:11px;
      font-weight:500;
      margin-bottom:4px;
      color:#54656f;
    }

    .input-area{
      background:#f0f2f5;
      padding:8px 16px;
      display:flex;
      gap:12px;
      align-items:center;
      border-top:1px solid #e9edef;
      flex-shrink:0;
    }

    #chatInput{
      flex:1;
      border:none;
      border-radius:24px;
      padding:10px 16px;
      font-size:var(--font-body);
      background:white;
      outline:none;
      min-width:0;
    }

    #chatInput::placeholder{
      color:#8696a0;
    }

    #sendBtn{
      background:var(--green);
      border:none;
      color:white;
      font-weight:600;
      padding:8px 20px;
      border-radius:24px;
      cursor:pointer;
      transition:background .2s;
    }

    #sendBtn:active{
      background:#006b56;
    }

    #sendBtn:disabled{
      opacity:.55;
      cursor:not-allowed;
    }

    #functionalLayer{
      display:none !important;
    }

    .selector-modal{
      position:fixed;
      inset:0;
      background:rgba(0,0,0,.5);
      display:none;
      align-items:center;
      justify-content:center;
      z-index:2000;
    }

    .selector-modal.show{
      display:flex;
    }

    .selector-card{
      width:min(500px,90%);
      max-height:80vh;
      background:#fff;
      border-radius:28px;
      overflow:hidden;
      display:flex;
      flex-direction:column;
      box-shadow:0 12px 28px rgba(0,0,0,.2);
    }

    .selector-head{
      display:flex;
      justify-content:space-between;
      align-items:center;
      padding:16px;
      border-bottom:1px solid #e9edef;
    }

    .selector-title{
      font-size:18px;
      font-weight:600;
      color:#111b21;
    }

    .selector-close{
      background:transparent;
      border:none;
      font-size:24px;
      cursor:pointer;
      color:#54656f;
    }

    .selector-search-wrap{
      padding:12px 16px;
      border-bottom:1px solid #e9edef;
    }

    .selector-search{
      width:100%;
      padding:10px 12px;
      border-radius:24px;
      border:none;
      background:#f0f2f5;
      font-size:14px;
      outline:none;
    }

    .selector-list{
      flex:1;
      overflow-y:auto;
    }

    .selector-item,
    .selector-action{
      display:block;
      width:100%;
      text-align:left;
      padding:12px 16px;
      border:none;
      background:transparent;
      cursor:pointer;
      font-size:15px;
      border-bottom:1px solid #f0f2f5;
    }

    .selector-item:hover,
    .selector-action:hover{
      background:#f5f6f6;
    }

    .selector-item.active{
      background:#e9f0e8;
    }

    .selector-item-title{
      font-weight:500;
      color:#111b21;
    }

    .selector-item-sub{
      font-size:13px;
      color:#667781;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .section-label{
      padding:12px 16px 4px;
      font-size:12px;
      font-weight:500;
      color:#667781;
      text-transform:uppercase;
    }

    .selector-empty{
      padding:14px 16px;
      color:#667781;
      font-size:14px;
    }

    .user-search-modal{
      position:fixed;
      inset:0;
      background:rgba(0,0,0,.5);
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
      color:#111b21;
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

    .loading,
    .error{
      padding:14px;
      color:#667781;
      font-size:14px;
      text-align:center;
    }

    .fullscreen-toggle{
      position:fixed;
      bottom:20px;
      right:20px;
      width:48px;
      height:48px;
      background:rgba(0,0,0,.6);
      backdrop-filter:blur(12px);
      border-radius:40px;
      display:none;
      align-items:center;
      justify-content:center;
      font-size:28px;
      color:white;
      cursor:pointer;
      z-index:10000;
      box-shadow:0 4px 12px rgba(0,0,0,.3);
      transition:all .2s ease;
      border:1px solid rgba(255,255,255,.2);
      font-weight:bold;
      user-select:none;
      touch-action:manipulation;
    }

    .fullscreen-toggle:active{
      transform:scale(.92);
      background:rgba(0,0,0,.8);
    }

    @media (max-width:768px){
      .fullscreen-toggle{
        display:flex;
      }

      .chat-shell{
        width:96%;
        height:62vh;
      }

      .top-btn{
        padding:4px 12px;
      }

      .message{
        max-width:85%;
      }

      .inner{
        padding-top:8px;
        gap:12px;
      }
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
              <button id="sendBtn" type="button">Enviar</button>
            </div>
          </div>

          <div id="functionalLayer">
            <div class="threads-panel">
              <div class="threads-header">
                <span>Conversaciones</span>
                <button class="new-chat-btn" id="newChatBtn" type="button">+ Nuevo</button>
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

  <div id="fullscreenToggleBtn" class="fullscreen-toggle">⤢</div>

  <script>
    const API_BASE = "https://camilo27.pythonanywhere.com/api/chat";
    const currentUserId = __CURRENT_USER_ID__;

    let currentThreadId = null;
    let threads = [];
    let pollingInterval = null;
    let threadsPollingInterval = null;
    let lastRenderedMessageId = null;
    let selectorMode = null;
    let isSending = false;

    function escapeHtml(text){
      return String(text ?? "")
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;")
        .replaceAll('"',"&quot;")
        .replaceAll("'","&#039;");
    }

    async function fetchJSON(url, options = {}){
      const response = await fetch(url, Object.assign({ cache:"no-store" }, options));
      const data = await response.json().catch(function(){ return {}; });

      if(!response.ok){
        throw new Error(data.error || data.detail || ("HTTP " + response.status));
      }

      return data;
    }

    async function loadThreads(){
      const listDiv = document.getElementById("threadList");

      try{
        const data = await fetchJSON(API_BASE + "/threads?user_id=" + encodeURIComponent(currentUserId) + "&_=" + Date.now());
        threads = Array.isArray(data.threads) ? data.threads : [];

        renderThreadList();

        if(threads.length > 0 && !currentThreadId){
          setActiveThread(threads[0].id);
        }

        syncTopButtonsFromThread();

        if(selectorMode){
          renderSelector();
        }
      }catch(error){
        console.error("Error loading threads:", error);
        listDiv.innerHTML = '<div class="error">Error al cargar conversaciones.<br>' + escapeHtml(error.message) + '</div>';

        const messagesArea = document.getElementById("messagesArea");
        if(!currentThreadId){
          messagesArea.innerHTML = '<div class="error">Error al cargar conversaciones.<br>' + escapeHtml(error.message) + '</div>';
        }
      }
    }

    function renderThreadList(){
      const container = document.getElementById("threadList");

      if(!threads.length){
        container.innerHTML = '<div style="padding:12px;text-align:center;">No hay conversaciones</div>';
        return;
      }

      container.innerHTML = threads.map(function(t){
        return '' +
          '<div class="thread-item' + (String(currentThreadId) === String(t.id) ? ' active' : '') + '" data-id="' + escapeHtml(t.id) + '">' +
            '<div class="thread-title">' + escapeHtml(t.title || (t.type === "private" ? "Privado" : "Grupo")) + '</div>' +
            '<div class="thread-preview">' + escapeHtml(t.last_message || '') + '</div>' +
          '</div>';
      }).join("");

      document.querySelectorAll(".thread-item").forEach(function(el){
        el.addEventListener("click", function(){
          setActiveThread(el.getAttribute("data-id"));
        });
      });
    }

    async function loadMessages(threadId, poll = false){
      const limit = poll ? 40 : 500;
      const url = API_BASE + "/threads/" + encodeURIComponent(threadId) + "/messages?user_id=" + encodeURIComponent(currentUserId) + "&limit=" + limit + "&_=" + Date.now();

      try{
        const data = await fetchJSON(url);
        let messages = Array.isArray(data.messages) ? data.messages : [];

        if(poll && lastRenderedMessageId !== null){
          messages = messages.filter(function(m){
            return Number(m.id || 0) > Number(lastRenderedMessageId || 0);
          });
        }

        const container = document.getElementById("messagesArea");

        if(!poll){
          container.innerHTML = "";
          lastRenderedMessageId = null;
        }

        if(!messages.length && !poll){
          container.innerHTML = '<div style="text-align:center;margin-top:20px;color:#667781;">No hay mensajes</div>';
          lastRenderedMessageId = null;
          return;
        }

        messages.forEach(function(msg){
          const id = String(msg.id || "");
          const div = document.createElement("div");
          const mine = String(msg.sender_id) === String(currentUserId);

          div.className = "message" + (mine ? " out" : "");
          div.setAttribute("data-id", id);
          div.innerHTML =
            '<strong>' + escapeHtml(mine ? "Tú" : (msg.sender_alias || "Usuario")) + '</strong>' +
            escapeHtml(msg.body || "");

          container.appendChild(div);

          if(id){
            lastRenderedMessageId = Number(id) || lastRenderedMessageId;
          }
        });

        container.scrollTop = container.scrollHeight;
        await markThreadRead(threadId);
      }catch(error){
        console.error("Error loading messages:", error);

        if(!poll){
          document.getElementById("messagesArea").innerHTML =
            '<div class="error">Error al cargar mensajes<br>' + escapeHtml(error.message) + '</div>';
        }
      }
    }

    async function markThreadRead(threadId){
      const messagesDiv = document.getElementById("messagesArea");
      const lastMsg = messagesDiv.querySelector(".message:last-child");

      if(!lastMsg) return;

      const lastId = lastMsg.getAttribute("data-id");

      if(!lastId) return;

      try{
        await fetch(API_BASE + "/threads/" + encodeURIComponent(threadId) + "/read", {
          method:"POST",
          headers:{ "Content-Type":"application/json" },
          body:JSON.stringify({
            user_id:currentUserId,
            last_read_message_id:lastId
          })
        });
      }catch(error){
        console.error("Error marking read:", error);
      }
    }

    async function sendMessage(){
      if(isSending) return;
      if(!currentThreadId) return;

      const input = document.getElementById("chatInput");
      const text = input.value.trim();

      if(!text) return;

      isSending = true;

      const sendBtn = document.getElementById("sendBtn");
      sendBtn.disabled = true;
      sendBtn.textContent = "Enviando";

      input.value = "";

      const container = document.getElementById("messagesArea");
      const pending = document.createElement("div");
      pending.className = "message out pending";
      pending.innerHTML = '<strong>Tú</strong>' + escapeHtml(text);
      container.appendChild(pending);
      container.scrollTop = container.scrollHeight;

      try{
        const data = await fetchJSON(API_BASE + "/threads/" + encodeURIComponent(currentThreadId) + "/messages", {
          method:"POST",
          headers:{ "Content-Type":"application/json" },
          body:JSON.stringify({
            sender_id:currentUserId,
            body:text
          })
        });

        await loadMessages(currentThreadId, false);
        await loadThreads();
      }catch(error){
        console.error("Error sending message:", error);
        alert("Error al enviar mensaje: " + error.message);
        await loadMessages(currentThreadId, false);
      }finally{
        isSending = false;
        sendBtn.disabled = false;
        sendBtn.textContent = "Enviar";
      }
    }

    function setActiveThread(threadId){
      currentThreadId = String(threadId || "");

      const thread = threads.find(function(t){
        return String(t.id) === String(currentThreadId);
      });

      document.getElementById("chatHeader").innerText = thread
        ? (thread.title || (thread.type === "private" ? "Privado" : "Grupo"))
        : "Conversación";

      document.getElementById("inputArea").style.display = "flex";

      lastRenderedMessageId = null;
      loadMessages(currentThreadId, false);
      renderThreadList();
      syncTopButtonsFromThread();

      if(selectorMode){
        renderSelector();
      }

      if(pollingInterval){
        clearInterval(pollingInterval);
      }

      pollingInterval = setInterval(function(){
        if(currentThreadId){
          loadMessages(currentThreadId, true);
        }
      }, 10000);
    }

    function setTopActive(mode){
      document.getElementById("btnSocorristas").classList.remove("active");
      document.getElementById("btnInstalacion").classList.remove("active");
      document.getElementById("btnNotificaciones").classList.remove("active");

      if(mode === "socorristas"){
        document.getElementById("btnSocorristas").classList.add("active");
      }

      if(mode === "instalacion"){
        document.getElementById("btnInstalacion").classList.add("active");
      }

      if(mode === "notificaciones"){
        document.getElementById("btnNotificaciones").classList.add("active");
      }
    }

    function syncTopButtonsFromThread(){
      const thread = threads.find(function(t){
        return String(t.id) === String(currentThreadId);
      });

      if(!thread){
        setTopActive(null);
        return;
      }

      if(thread.type === "private"){
        setTopActive("socorristas");
      }else{
        setTopActive("instalacion");
      }
    }

    function openSelector(mode){
      selectorMode = mode;
      document.getElementById("selectorModal").classList.add("show");
      renderSelector();

      setTimeout(function(){
        const input = document.getElementById("selectorSearch");
        if(input) input.focus();
      }, 10);
    }

    function closeSelector(){
      document.getElementById("selectorModal").classList.remove("show");
      document.getElementById("selectorSearch").value = "";
      selectorMode = null;
      syncTopButtonsFromThread();
    }

    function getFilteredThreads(){
      const query = document.getElementById("selectorSearch").value.trim().toLowerCase();
      let list = threads.slice();

      if(selectorMode === "socorristas"){
        list = list.filter(function(t){
          return t.type === "private";
        });
      }else if(selectorMode === "instalacion"){
        list = list.filter(function(t){
          return t.type !== "private";
        });
      }

      if(!query) return list;

      return list.filter(function(t){
        const title = String(t.title || (t.type === "private" ? "Privado" : "Grupo")).toLowerCase();
        const preview = String(t.last_message || "").toLowerCase();
        return title.includes(query) || preview.includes(query);
      });
    }

    function renderSelector(){
      if(!selectorMode) return;

      const selectorTitle = document.getElementById("selectorTitle");
      const selectorSearch = document.getElementById("selectorSearch");
      const selectorList = document.getElementById("selectorList");

      if(selectorMode === "socorristas"){
        selectorTitle.innerText = "Socorristas";
        selectorSearch.placeholder = "Buscar conversación";
        setTopActive("socorristas");
      }else if(selectorMode === "instalacion"){
        selectorTitle.innerText = "Instalación";
        selectorSearch.placeholder = "Buscar conversación";
        setTopActive("instalacion");
      }else{
        selectorTitle.innerText = "Notificaciones";
        selectorSearch.placeholder = "Buscar conversación";
        setTopActive("notificaciones");
      }

      let html = "";

      if(selectorMode === "socorristas"){
        html += '<button class="selector-action" id="selectorNewChat">+ Nuevo chat</button>';
      }

      const list = getFilteredThreads();

      html += '<div class="section-label">Conversaciones</div>';

      if(!list.length){
        html += '<div class="selector-empty">No hay conversaciones</div>';
      }else{
        html += list.map(function(t){
          return '' +
            '<button class="selector-item selector-thread' + (String(currentThreadId) === String(t.id) ? ' active' : '') + '" data-id="' + escapeHtml(t.id) + '">' +
              '<div class="selector-item-title">' + escapeHtml(t.title || (t.type === "private" ? "Privado" : "Grupo")) + '</div>' +
              '<div class="selector-item-sub">' + escapeHtml(t.last_message || "") + '</div>' +
            '</button>';
        }).join("");
      }

      selectorList.innerHTML = html;

      const selectorNewChat = document.getElementById("selectorNewChat");

      if(selectorNewChat){
        selectorNewChat.addEventListener("click", function(){
          closeSelector();
          showNewChatModal();
        });
      }

      document.querySelectorAll(".selector-thread").forEach(function(el){
        el.addEventListener("click", function(){
          setActiveThread(el.getAttribute("data-id"));
          closeSelector();
        });
      });
    }

    function showNewChatModal(){
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
      closeBtn.onclick = function(){
        modal.remove();
      };

      const searchInput = modal.querySelector("#userSearch");
      const resultsDiv = modal.querySelector("#userSearchResults");

      async function searchUsers(){
        const query = searchInput.value.trim().toLowerCase();

        if(query.length < 2){
          resultsDiv.innerHTML = '<div>Escribe al menos 2 caracteres</div>';
          return;
        }

        try{
          const users = await fetchJSON(API_BASE + "/users?_=" + Date.now());

          const filtered = users.filter(function(u){
            return String(u.alias || "").toLowerCase().includes(query) ||
                   String(u.dni || "").toLowerCase().includes(query);
          });

          if(!filtered.length){
            resultsDiv.innerHTML = '<div>No se encontraron usuarios</div>';
            return;
          }

          resultsDiv.innerHTML = filtered.map(function(u){
            return '<div class="user-item" data-dni="' + escapeHtml(u.dni) + '">@' + escapeHtml(u.alias || "socorrista") + ' (' + escapeHtml(u.dni) + ')</div>';
          }).join("");

          resultsDiv.querySelectorAll(".user-item").forEach(function(el){
            el.addEventListener("click", async function(){
              const otherDni = el.getAttribute("data-dni");

              if(String(otherDni) === String(currentUserId)){
                alert("No puedes chatear contigo mismo");
                return;
              }

              try{
                const data = await fetchJSON(
                  API_BASE + "/private/" + encodeURIComponent(otherDni) +
                  "?user_id=" + encodeURIComponent(currentUserId) +
                  "&_=" + Date.now()
                );

                if(data.thread_id){
                  modal.remove();
                  await loadThreads();
                  setActiveThread(data.thread_id);
                }
              }catch(error){
                alert("Error al crear el chat: " + error.message);
              }
            });
          });
        }catch(error){
          resultsDiv.innerHTML = '<div class="error">Error al cargar usuarios<br>' + escapeHtml(error.message) + '</div>';
        }
      }

      searchInput.addEventListener("input", searchUsers);
      searchUsers();
    }

    document.getElementById("sendBtn").addEventListener("click", sendMessage);

    document.getElementById("chatInput").addEventListener("keydown", function(e){
      if(e.key === "Enter"){
        e.preventDefault();
        sendMessage();
      }
    });

    document.getElementById("btnSocorristas").addEventListener("click", function(){
      openSelector("socorristas");
    });

    document.getElementById("btnInstalacion").addEventListener("click", function(){
      openSelector("instalacion");
    });

    document.getElementById("btnNotificaciones").addEventListener("click", function(){
      openSelector("notificaciones");
    });

    document.getElementById("selectorClose").addEventListener("click", closeSelector);

    document.getElementById("selectorModal").addEventListener("click", function(e){
      if(e.target === document.getElementById("selectorModal")){
        closeSelector();
      }
    });

    document.getElementById("selectorSearch").addEventListener("input", renderSelector);

    loadThreads();

    threadsPollingInterval = setInterval(loadThreads, 15000);

    (function(){
      const stageEl = document.getElementById("stage");
      const toggleBtn = document.getElementById("fullscreenToggleBtn");

      function setFullscreenFlag(active){
        if(active){
          localStorage.setItem("fullscreenActive","true");
        }else{
          localStorage.removeItem("fullscreenActive");
        }
      }

      function enterFullscreen(){
        const elem = document.documentElement;
        const requestMethod =
          elem.requestFullscreen ||
          elem.webkitRequestFullscreen ||
          elem.mozRequestFullScreen ||
          elem.msRequestFullscreen;

        if(requestMethod){
          requestMethod.call(elem).then(function(){
            if(stageEl) stageEl.classList.add("fullscreen-mode");

            if(toggleBtn){
              toggleBtn.textContent = "✕";
              toggleBtn.style.fontSize = "26px";
            }

            setFullscreenFlag(true);
          }).catch(function(err){
            console.log("Error al entrar en fullscreen:", err);
          });
        }
      }

      function exitFullscreen(){
        const exitMethod =
          document.exitFullscreen ||
          document.webkitExitFullscreen ||
          document.mozCancelFullScreen ||
          document.msExitFullscreen;

        if(exitMethod){
          exitMethod.call(document).then(function(){
            if(stageEl) stageEl.classList.remove("fullscreen-mode");

            if(toggleBtn){
              toggleBtn.textContent = "⤢";
              toggleBtn.style.fontSize = "28px";
            }

            setFullscreenFlag(false);
          }).catch(function(err){
            console.log("Error al salir de fullscreen:", err);
          });
        }
      }

      function toggleFullscreen(){
        const isFull = !!(
          document.fullscreenElement ||
          document.webkitFullscreenElement ||
          document.mozFullScreenElement ||
          document.msFullscreenElement
        );

        if(isFull){
          exitFullscreen();
        }else{
          enterFullscreen();
        }
      }

      function onFullscreenChange(){
        const isFull = !!(
          document.fullscreenElement ||
          document.webkitFullscreenElement ||
          document.mozFullScreenElement ||
          document.msFullscreenElement
        );

        if(isFull){
          if(stageEl) stageEl.classList.add("fullscreen-mode");

          if(toggleBtn){
            toggleBtn.textContent = "✕";
            toggleBtn.style.fontSize = "26px";
          }

          setFullscreenFlag(true);
        }else{
          if(stageEl) stageEl.classList.remove("fullscreen-mode");

          if(toggleBtn){
            toggleBtn.textContent = "⤢";
            toggleBtn.style.fontSize = "28px";
          }

          setFullscreenFlag(false);
        }
      }

      if(toggleBtn){
        toggleBtn.addEventListener("click", function(e){
          e.preventDefault();
          toggleFullscreen();
        });
      }

      document.addEventListener("fullscreenchange", onFullscreenChange);
      document.addEventListener("webkitfullscreenchange", onFullscreenChange);
      document.addEventListener("mozfullscreenchange", onFullscreenChange);
      document.addEventListener("MSFullscreenChange", onFullscreenChange);
    })();
  </script>
</body>
</html>
"""

html = html.replace("__CURRENT_USER_ID__", json.dumps(str(USER_DNI)))

components.html(html, height=800, scrolling=False)
