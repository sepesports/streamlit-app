# pages/chat_interfaz.py
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

USER_DNI = st.query_params.get("dni") or ""
if not USER_DNI:
    st.error("No se pudo identificar al usuario. Por favor, vuelve a iniciar sesión.")
    st.stop()

html = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Chat</title>
  <style>
    :root{
      /* ===== PALETA DE ADMIN.PY ===== */
      --baseBlue: #040e31;
      --bgTop:  #0a1a55;
      --bgMid:  #061240;
      --bgDeep: #02071c;

      --overlay1: rgba(40, 120, 255, .16);
      --overlay2: rgba(0,  10,  40, .62);

      --ink: rgba(255,255,255,.92);
      --muted: rgba(255,255,255,.62);

      --pill: rgba(238, 245, 255, .92);
      --pill2: rgba(255,255,255,.86);

      --btn1:#2f7de1;
      --btn2:#1e5fc4;

      --shadow1: 0 22px 55px rgba(0,0,0,.55);
      --shadow2: 0 10px 22px rgba(0,0,0,.40);
      --blur: 14px;

      /* ===== AJUSTES DE ALTURA ===== */
      --top-row-h: 48px;        /* alto de los botones superiores */
      --title-row-h: 40px;      /* alto del header del chat */
      --input-row-h: 44px;      /* alto del área de input */

      --messages-h-desktop: calc(65vh - (var(--top-row-h) + var(--title-row-h) + var(--input-row-h))); /* se calcula automáticamente */
      --chat-shell-h-desktop: 65vh;    /* alto total del bloque del chat (desktop) */
      --chat-shell-h-mobile: 58vh;     /* alto total del bloque del chat (móvil) */

      /* ===== ESTILOS DE FUENTE ===== */
      --font-main: 16px;
      --font-small: 12px;
      --font-title: 15px;
      --font-body: 14px;
      --send-w: 120px;
    }

    *{ box-sizing:border-box; margin:0; padding:0; }

    html, body{
      width:100%;
      height:100%;
      overflow:hidden;
      background: var(--baseBlue);
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }

    /* ===== FONDO PRINCIPAL (idéntico a admin.py) ===== */
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
      top:6%;
      bottom:6%;
    }

    #hud{
      position:absolute; inset:0;
      pointer-events:none;
      background:
        radial-gradient(60% 45% at 50% 18%, rgba(255,255,255,.12), transparent 60%),
        linear-gradient(180deg, transparent 62%, rgba(0,0,0,.30) 100%);
    }

    /* ===== CONTENEDOR INTERIOR DEL CHAT ===== */
    .inner{
      width:100%;
      height:100%;
      display:flex;
      flex-direction:column;
      justify-content:center;   /* centrado vertical del bloque de chat */
      align-items:center;
      gap:20px;
    }

    /* ===== BOTONES SUPERIORES (estilo admin.py) ===== */
    .top-buttons{
      display:flex;
      gap:0;
      width:auto;
      min-height:var(--top-row-h);
      max-height:var(--top-row-h);
      background:transparent;
      border-radius: 48px;
      overflow:hidden;
      box-shadow: var(--shadow2);
    }

    .top-btn{
      border: 1px solid rgba(255,255,255,.20);
      background:
        radial-gradient(80px 30px at 30% 25%, rgba(255,255,255,.12), transparent 70%),
        linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      color: var(--ink);
      margin:0;
      padding:8px 24px;
      min-height:var(--top-row-h);
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      cursor:pointer;
      font-size:var(--font-main);
      font-weight:600;
      transition: transform .12s ease, filter .12s ease;
      backdrop-filter: blur(var(--blur));
      -webkit-backdrop-filter: blur(var(--blur));
    }

    .top-btn + .top-btn{ border-left:none; }
    .top-btn:active{ transform: scale(.98); filter: brightness(.96); }
    .top-btn.active{
      background:
        radial-gradient(80px 30px at 30% 25%, rgba(255,255,255,.22), transparent 70%),
        linear-gradient(180deg, #1e5fc4 0%, #0f4a9e 100%);
      box-shadow: inset 0 1px 2px rgba(0,0,0,.2), 0 1px 0 rgba(255,255,255,.2);
    }

    .btn-stack{
      display:flex;
      flex-direction:column;
      align-items:flex-start;
      justify-content:center;
      gap:2px;
    }
    .btn-topline{ font-size:var(--font-small); line-height:1.2; opacity:.8; }
    .btn-mainline{ font-size:calc(var(--font-main) + 2px); font-weight:700; }

    /* ===== BLOQUE DEL CHAT (contenedor principal) ===== */
    .chat-shell{
      width:min(820px, 90%);
      height:var(--chat-shell-h-desktop);
      display:flex;
      flex-direction:column;
      background: rgba(10,20,40,0.45);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: 28px;
      border: 1px solid rgba(255,255,255,.20);
      box-shadow: var(--shadow1), inset 0 1px 0 rgba(255,255,255,.08);
      overflow:hidden;
    }

    .chat-header{
      height:var(--title-row-h);
      min-height:var(--title-row-h);
      border-bottom: 1px solid rgba(255,255,255,.20);
      display:flex;
      align-items:center;
      padding:0 20px;
      font-size:var(--font-title);
      font-weight:600;
      color:var(--ink);
      text-shadow: 0 1px 2px rgba(0,0,0,.3);
      background: rgba(0,0,0,0.2);
    }

    .messages-area{
      flex:1;
      overflow-y:auto;
      padding:16px;
      display:flex;
      flex-direction:column;
      gap:12px;
      background: rgba(0,0,0,0.15);
    }

    .message{
      max-width:75%;
      padding:10px 16px;
      border-radius: 24px;
      background: rgba(255,255,255,0.18);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255,255,255,.20);
      color: var(--ink);
      font-size:var(--font-body);
      line-height:1.4;
      align-self:flex-start;
      box-shadow: 0 2px 6px rgba(0,0,0,.1);
    }

    .message.out{
      background: rgba(47,125,225,0.55);
      border-color: rgba(255,255,255,.30);
      align-self:flex-end;
    }

    .message strong{
      display:block;
      margin-bottom:4px;
      font-size:11px;
      opacity:.8;
      font-weight:500;
    }

    .input-area{
      height:var(--input-row-h);
      display:flex;
      border-top: 1px solid rgba(255,255,255,.20);
      background: rgba(0,0,0,0.25);
    }

    #chatInput{
      flex:1;
      background: rgba(255,255,255,0.92);
      border:none;
      padding:0 16px;
      font-size:var(--font-body);
      outline:none;
      color:#1a1a2e;
    }
    #chatInput::placeholder{ color:#6c6c8c; }

    #sendBtn{
      width:var(--send-w);
      background:
        radial-gradient(80px 30px at 30% 25%, rgba(255,255,255,.15), transparent 70%),
        linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      border:none;
      border-left:1px solid rgba(255,255,255,.20);
      color:var(--ink);
      font-weight:600;
      font-size:calc(var(--font-body) + 2px);
      cursor:pointer;
      transition: all .1s ease;
    }
    #sendBtn:active{ transform: scale(.98); filter: brightness(.96); }

    /* ===== MODAL SELECTOR (estilo admin.py) ===== */
    .selector-modal{
      position:fixed;
      top:0; left:0; right:0; bottom:0;
      background:rgba(0,0,0,0.75);
      display:none;
      align-items:center;
      justify-content:center;
      z-index:2000;
      backdrop-filter: blur(4px);
    }
    .selector-modal.show{ display:flex; }

    .selector-card{
      width:min(560px, 92%);
      max-height:80vh;
      background: rgba(10,20,40,0.9);
      backdrop-filter: blur(20px);
      border-radius: 28px;
      border: 1px solid rgba(255,255,255,.25);
      box-shadow: var(--shadow1);
      overflow:hidden;
      display:flex;
      flex-direction:column;
    }

    .selector-head{
      display:flex;
      justify-content:space-between;
      align-items:center;
      padding:0 16px;
      height:54px;
      border-bottom: 1px solid rgba(255,255,255,.20);
    }
    .selector-title{ font-size:18px; font-weight:600; color:var(--ink); }
    .selector-close{
      background:transparent;
      border:none;
      font-size:28px;
      color:var(--ink);
      cursor:pointer;
      width:48px;
      height:48px;
      transition:all .1s;
    }
    .selector-close:active{ transform:scale(.94); }

    .selector-search-wrap{ padding:12px; border-bottom:1px solid rgba(255,255,255,.15); }
    .selector-search{
      width:100%;
      padding:10px 14px;
      border-radius: 999px;
      border:1px solid rgba(255,255,255,.30);
      background: rgba(255,255,255,0.9);
      font-size:14px;
      outline:none;
    }

    .selector-list{
      flex:1;
      overflow-y:auto;
      padding:8px 0;
    }

    .selector-item, .selector-action{
      width:100%;
      text-align:left;
      padding:12px 20px;
      background:transparent;
      border:none;
      border-bottom:1px solid rgba(255,255,255,.10);
      color:var(--ink);
      cursor:pointer;
      transition:background .1s;
      font-size:14px;
    }
    .selector-item:hover, .selector-action:hover{ background:rgba(255,255,255,0.1); }
    .selector-item.active{ background:rgba(47,125,225,0.35); }
    .selector-item-title{ font-weight:500; margin-bottom:4px; }
    .selector-item-sub{ font-size:12px; opacity:.7; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .section-label{ padding:10px 20px 4px; font-size:11px; font-weight:600; opacity:.7; letter-spacing:1px; color:var(--ink); }

    /* ===== OCULTAR ELEMENTOS NO NECESARIOS ===== */
    #functionalLayer{ display:none !important; }

    /* ===== AJUSTES MÓVIL ===== */
    @media (max-width: 768px){
      :root{
        --top-row-h: 44px;
        --title-row-h: 36px;
        --input-row-h: 42px;
        --font-main: 14px;
        --font-small: 10px;
        --font-title: 13px;
        --font-body: 13px;
        --send-w: 88px;
      }
      .chat-shell{ height:var(--chat-shell-h-mobile); width:96%; }
      .top-btn{ padding:4px 16px; }
      .message{ max-width:88%; padding:8px 12px; }
      .selector-card{ max-height:70vh; }
    }

    /* ===== SCROLLBAR PERSONALIZADA ===== */
    .messages-area::-webkit-scrollbar,
    .selector-list::-webkit-scrollbar{
      width:6px;
    }
    .messages-area::-webkit-scrollbar-track,
    .selector-list::-webkit-scrollbar-track{
      background:rgba(0,0,0,0.2);
      border-radius:4px;
    }
    .messages-area::-webkit-scrollbar-thumb,
    .selector-list::-webkit-scrollbar-thumb{
      background:rgba(255,255,255,0.3);
      border-radius:4px;
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
            <input type="text" id="chatInput" placeholder="Diálogo para enviar mensaje" autocomplete="off">
            <button id="sendBtn">SEND</button>
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
</script>
</body>
</html>
""".replace("REEMPLAZAR_DNI", USER_DNI)

components.html(html, height=800, scrolling=False)
