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
    /* ========== ESTILOS BASE DEL LOGIN (fondo, panel, efectos) ========== */
    :root{
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
    }

    *{ box-sizing:border-box; }
    html, body{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background: var(--baseBlue);
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }

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
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow: auto;
    }

    #hud{
      position:absolute; inset:0;
      pointer-events:none;
      background:
        radial-gradient(60% 45% at 50% 18%, rgba(255,255,255,.12), transparent 60%),
        linear-gradient(180deg, transparent 62%, rgba(0,0,0,.30) 100%);
    }

    /* ========== ESTILOS DEL CHAT (adaptados para encajar dentro del panel) ========== */
    .chat-container {
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.3);
      backdrop-filter: blur(12px);
      border-radius: 28px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      overflow: auto;
    }

    /* Reutilizamos los estilos originales del chat pero ajustamos colores para que se vean sobre fondo oscuro */
    :root {
      --chat-bg: rgba(255,255,255,0.1);
      --chat-text: #fff;
      --chat-border: rgba(255,255,255,0.3);
      --chat-soft: rgba(255,255,255,0.15);
      --chat-soft2: rgba(255,255,255,0.25);
      --chat-muted: rgba(255,255,255,0.7);
      --chat-danger: #ff6b6b;
    }

    .top-buttons {
      display: grid;
      grid-template-columns: 1fr 1fr 1.15fr;
      gap: 12px;
    }

    .top-btn, #sendBtn, .new-chat-btn, .selector-close, .selector-item, .selector-action {
      border: 1px solid rgba(255,255,255,.20) !important;
      border-radius: 999px !important;
      background:
        radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.22), transparent 60%),
        linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%) !important;
      box-shadow:
        0 8px 18px rgba(0,0,0,.3),
        inset 0 1px 0 rgba(255,255,255,.25) !important;
      color: rgba(255,255,255,.95) !important;
      cursor: pointer;
      transition: transform .12s ease, filter .12s ease;
      font-weight: 700 !important;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    .top-btn {
      padding: 12px 16px !important;
      font-size: 18px !important;
    }
    .top-btn .btn-stack, .top-btn .btn-center {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .btn-topline {
      font-size: 12px;
      opacity: 0.9;
    }
    .btn-mainline, .btn-center {
      font-size: 20px;
      font-weight: 700;
    }

    #sendBtn {
      width: 120px;
      font-size: 16px !important;
    }

    .new-chat-btn {
      padding: 6px 12px !important;
      font-size: 12px !important;
    }

    .selector-close {
      width: 48px;
      font-size: 24px;
    }

    .selector-item, .selector-action {
      width: 100%;
      padding: 12px !important;
      margin-bottom: 8px;
      justify-content: flex-start;
    }

    .top-btn:hover, #sendBtn:hover, .new-chat-btn:hover, .selector-close:hover, .selector-item:hover, .selector-action:hover {
      filter: brightness(0.98);
    }
    .top-btn:active, #sendBtn:active, .new-chat-btn:active, .selector-close:active, .selector-item:active, .selector-action:active {
      transform: scale(0.985);
      filter: brightness(0.96);
    }

    .chat-shell {
      background: rgba(0,0,0,0.4);
      border-radius: 24px;
      border: 1px solid rgba(255,255,255,0.2);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      flex: 1;
      min-height: 0;
    }

    .chat-header {
      padding: 12px 20px;
      background: rgba(0,0,0,0.3);
      border-bottom: 1px solid rgba(255,255,255,0.2);
      font-size: 18px;
      font-weight: bold;
      color: white;
    }

    .messages-area {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .message {
      max-width: 70%;
      padding: 8px 12px;
      border-radius: 18px;
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(8px);
      color: white;
      align-self: flex-start;
      border: 1px solid rgba(255,255,255,0.2);
    }
    .message.out {
      background: rgba(0,0,0,0.5);
      align-self: flex-end;
    }
    .message strong {
      font-size: 12px;
      display: block;
      margin-bottom: 4px;
      color: #ccc;
    }

    .input-area {
      display: none;
      border-top: 1px solid rgba(255,255,255,0.2);
      padding: 12px;
      gap: 12px;
      background: rgba(0,0,0,0.3);
    }
    #chatInput {
      flex: 1;
      padding: 12px 16px;
      border-radius: 30px;
      border: none;
      background: rgba(255,255,255,0.2);
      color: white;
      font-size: 14px;
      outline: none;
    }
    #chatInput::placeholder {
      color: rgba(255,255,255,0.6);
    }

    /* modal y selector mantienen su estructura pero con estilos oscuros */
    .user-search-modal .modal-content,
    .selector-card {
      background: rgba(0,0,0,0.85);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255,255,255,0.3);
      border-radius: 24px;
      color: white;
    }
    .selector-search {
      background: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.3);
      color: white;
    }
    .selector-item, .selector-action {
      background: transparent !important;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      color: white !important;
    }
    .selector-item:hover, .selector-action:hover {
      background: rgba(255,255,255,0.1) !important;
    }
    .thread-item {
      background: transparent;
      color: white;
    }
    .thread-item:hover {
      background: rgba(255,255,255,0.1);
    }
    .thread-item.active {
      background: rgba(255,255,255,0.2);
    }

    /* Ajustes móviles */
    @media (max-width: 768px) {
      .top-btn { font-size: 14px !important; padding: 8px 12px !important; }
      .btn-mainline, .btn-center { font-size: 16px; }
      .chat-header { font-size: 16px; }
      .message { max-width: 85%; }
    }
  </style>
</head>
<body>
<div id="stage">
  <div id="plan">
    <div id="frame"></div>
    <div id="card">
      <div class="chat-container">
        <!-- Aquí va TODO el contenido del chat original -->
        <div class="top-buttons">
          <button class="top-btn" id="btnSocorristas" type="button">
            <div class="btn-stack">
              <span class="btn-topline">seleccióna</span>
              <span class="btn-mainline">Socorristas</span>
            </div>
          </button>
          <button class="top-btn" id="btnInstalacion" type="button">
            <div class="btn-stack">
              <span class="btn-topline">seleccióna</span>
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
            <input type="text" id="chatInput" placeholder="Dialogo para enviar Mensaje" autocomplete="off">
            <button id="sendBtn">SEND</button>
          </div>
        </div>

        <div id="functionalLayer" style="display: none;">
          <div class="threads-panel">
            <div class="threads-header">
              <span>Conversaciones</span>
              <button class="new-chat-btn" id="newChatBtn">+ Nuevo</button>
            </div>
            <div class="thread-list" id="threadList"></div>
          </div>
        </div>
      </div>
    </div>
    <div id="hud"></div>
  </div>
</div>

<!-- Modales igual que antes, pero con clases adaptadas -->
<div class="selector-modal" id="selectorModal">
  <div class="selector-card">
    <div class="selector-head">
      <div class="selector-title" id="selectorTitle">Selección</div>
      <button class="selector-close" id="selectorClose" type="button">×</button>
    </div>
    <div class="selector-search-wrap">
      <input id="selectorSearch" class="selector-search" type="text" autocomplete="off" placeholder="Buscar">
    </div>
    <div class="selector-list" id="selectorList"></div>
  </div>
</div>

<script>
  // *************** TODO EL JAVASCRIPT ORIGINAL SIN MODIFICACIONES ***************
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
