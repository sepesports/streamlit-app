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
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
  <title>Chat</title>
  <style>
    /* ===== ESTILO WHATSAPP ===== */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: #f0f2f5;
    }

    /* Fondo y contenedor principal (similar a WhatsApp Web) */
    #stage {
      position: fixed;
      inset: 0;
      background: #f0f2f5;
    }

    #plan {
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      background: #f0f2f5;
      overflow: hidden;
    }

    /* Eliminar efectos decorativos de admin.py */
    #plan::before, #plan::after, #frame, #hud {
      display: none;
    }

    #card {
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      padding: 0;
    }

    .inner {
      display: flex;
      flex-direction: column;
      height: 100%;
      width: 100%;
      background: #f0f2f5;
    }

    /* Barra superior con pestañas (estilo WhatsApp) */
    .top-buttons {
      display: flex;
      background: #fff;
      border-bottom: 1px solid #e9edef;
      padding: 0 16px;
      height: 60px;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }

    .top-btn {
      background: transparent;
      border: none;
      padding: 8px 16px;
      font-size: 15px;
      font-weight: 500;
      color: #54656f;
      cursor: pointer;
      border-radius: 18px;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .top-btn.active {
      background: #e7f0e4;
      color: #008069;
    }

    .btn-stack {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .btn-topline {
      font-size: 11px;
      font-weight: normal;
      opacity: 0.7;
    }

    .btn-mainline {
      font-size: 14px;
      font-weight: 600;
    }

    .btn-center {
      font-size: 15px;
      font-weight: 500;
    }

    /* Contenedor del chat (similar a WhatsApp Web) */
    .chat-shell {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: #efeae2;
      background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.05"><path fill="none" d="M0 0h100v100H0z"/><path fill="%23000" d="M10 10h80v80H10z"/></svg>');
      background-repeat: repeat;
      overflow: hidden;
      position: relative;
    }

    /* Cabecera del chat */
    .chat-header {
      background: #f0f2f5;
      padding: 12px 16px;
      border-bottom: 1px solid #e9edef;
      font-size: 16px;
      font-weight: 500;
      color: #111b21;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }

    /* Área de mensajes */
    .messages-area {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    /* Burbujas de mensaje */
    .message {
      max-width: 65%;
      padding: 8px 12px;
      border-radius: 18px;
      font-size: 14px;
      line-height: 1.4;
      word-wrap: break-word;
      position: relative;
      background: #fff;
      color: #111b21;
      box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }

    .message.out {
      background: #d9f0c3;
      align-self: flex-end;
    }

    .message strong {
      display: block;
      font-size: 12px;
      font-weight: 500;
      margin-bottom: 4px;
      color: #54656f;
    }

    /* Área de entrada de texto */
    .input-area {
      display: flex;
      align-items: center;
      background: #f0f2f5;
      padding: 8px 12px;
      border-top: 1px solid #e9edef;
      gap: 8px;
      flex-shrink: 0;
    }

    #chatInput {
      flex: 1;
      border: none;
      border-radius: 24px;
      padding: 10px 16px;
      font-size: 15px;
      background: #fff;
      outline: none;
      color: #111b21;
    }

    #chatInput::placeholder {
      color: #8696a0;
    }

    #sendBtn {
      background: #008069;
      border: none;
      color: white;
      font-weight: 600;
      font-size: 14px;
      padding: 8px 20px;
      border-radius: 24px;
      cursor: pointer;
      transition: background 0.2s;
    }

    #sendBtn:active {
      background: #006b56;
    }

    /* Elementos de carga y error */
    .loading, .error {
      text-align: center;
      padding: 20px;
      color: #667781;
      font-size: 14px;
    }

    .error {
      color: #d3392c;
    }

    /* Modal selector (similar a WhatsApp) */
    .selector-modal {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 2000;
    }

    .selector-modal.show {
      display: flex;
    }

    .selector-card {
      width: 90%;
      max-width: 500px;
      max-height: 80vh;
      background: #fff;
      border-radius: 24px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.2);
    }

    .selector-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
      border-bottom: 1px solid #e9edef;
    }

    .selector-title {
      font-size: 18px;
      font-weight: 600;
      color: #111b21;
    }

    .selector-close {
      background: transparent;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: #54656f;
    }

    .selector-search-wrap {
      padding: 12px 16px;
      border-bottom: 1px solid #e9edef;
    }

    .selector-search {
      width: 100%;
      padding: 10px 12px;
      border-radius: 24px;
      border: none;
      background: #f0f2f5;
      font-size: 14px;
      outline: none;
    }

    .selector-list {
      flex: 1;
      overflow-y: auto;
    }

    .selector-item, .selector-action {
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

    .selector-item:hover, .selector-action:hover {
      background: #f5f6f6;
    }

    .selector-item.active {
      background: #e9f0e8;
    }

    .selector-item-title {
      font-weight: 500;
      color: #111b21;
    }

    .selector-item-sub {
      font-size: 13px;
      color: #667781;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .section-label {
      padding: 12px 16px 4px;
      font-size: 12px;
      font-weight: 500;
      color: #667781;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Modal para nuevo chat */
    .user-search-modal {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2100;
    }

    .modal-content {
      background: #fff;
      width: 90%;
      max-width: 400px;
      border-radius: 24px;
      padding: 20px;
    }

    .modal-content h3 {
      margin-bottom: 16px;
      font-size: 18px;
      color: #111b21;
    }

    .modal-content input {
      width: 100%;
      padding: 12px;
      border-radius: 24px;
      border: 1px solid #e9edef;
      background: #fff;
      margin-bottom: 16px;
      font-size: 15px;
      outline: none;
    }

    .user-list {
      max-height: 300px;
      overflow-y: auto;
    }

    .user-item {
      padding: 12px;
      cursor: pointer;
      border-bottom: 1px solid #f0f2f5;
    }

    .user-item:hover {
      background: #f5f6f6;
    }

    .close-modal {
      float: right;
      font-size: 24px;
      cursor: pointer;
      color: #54656f;
    }

    /* Ocultar elementos no necesarios */
    #functionalLayer {
      display: none !important;
    }

    /* Ajustes móviles */
    @media (max-width: 768px) {
      .top-buttons {
        height: 50px;
        padding: 0 8px;
      }
      .top-btn {
        padding: 6px 12px;
        font-size: 13px;
      }
      .btn-mainline {
        font-size: 13px;
      }
      .message {
        max-width: 85%;
      }
      .chat-header {
        font-size: 15px;
        padding: 10px 16px;
      }
      #chatInput {
        font-size: 14px;
      }
      #sendBtn {
        padding: 6px 16px;
      }
    }

    /* Scroll personalizado */
    .messages-area::-webkit-scrollbar {
      width: 6px;
    }
    .messages-area::-webkit-scrollbar-track {
      background: #f0f2f5;
    }
    .messages-area::-webkit-scrollbar-thumb {
      background: #c1c9d0;
      border-radius: 3px;
    }
  </style>
</head>
<body>
<div id="stage">
  <div id="plan">
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
