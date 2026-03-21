# pages/chat_interfaz.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{
        padding:0 !important;
        margin:0 !important;
        max-width:100% !important;
      }
      section.main > div{
        padding:0 !important;
        margin:0 !important;
      }
      header, footer{
        display:none !important;
      }
      [data-testid="stSidebar"],
      [data-testid="collapsedControl"]{
        display:none !important;
      }
      iframe{
        border:0 !important;
      }
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
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
  <title>Chat</title>
  <style>
    :root{
      --bg: #ffffff;
      --panel: #ffffff;
      --border: #111111;
      --text: #111111;
      --muted: #5c5c5c;
      --hover: #f2f2f2;
      --active: #eaeaea;
      --danger: #b3261e;

      --frame-margin: clamp(6px, 1.4vw, 16px);
      --border-size: 2px;

      --top-row-h: clamp(58px, 8vh, 72px);
      --title-row-h: clamp(42px, 6vh, 52px);
      --input-row-h: clamp(52px, 7vh, 62px);

      --gap-top: clamp(8px, 1vw, 14px);

      --font-main: clamp(14px, 1.5vw, 20px);
      --font-small: clamp(12px, 1.1vw, 15px);
      --font-title: clamp(15px, 1.5vw, 20px);
      --font-input: clamp(14px, 1.4vw, 18px);
      --font-send: clamp(14px, 1.4vw, 18px);

      --pad-x: clamp(8px, 1.2vw, 14px);
      --pad-y: clamp(6px, 0.8vw, 10px);

      --btn1: 1fr;
      --btn2: 1fr;
      --btn3: 1.15fr;
      --send-w: clamp(96px, 22vw, 130px);
      --selector-max-h: min(34vh, 340px);
    }

    *{
      box-sizing:border-box;
      -webkit-tap-highlight-color: transparent;
    }

    html, body{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--bg);
      font-family: Arial, Helvetica, sans-serif;
      color:var(--text);
    }

    body{
      overscroll-behavior:none;
    }

    #app{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      background:var(--bg);
      padding:var(--frame-margin);
    }

    .frame{
      width:100%;
      height:100%;
      border:var(--border-size) solid var(--border);
      display:flex;
      flex-direction:column;
      background:var(--panel);
      overflow:hidden;
    }

    .inner{
      display:flex;
      flex-direction:column;
      width:100%;
      height:100%;
      padding:clamp(18px, 2.4vw, 28px);
      gap:var(--gap-top);
      min-height:0;
    }

    .top-buttons{
      display:grid;
      grid-template-columns: var(--btn1) var(--btn2) var(--btn3);
      gap:0;
      width:100%;
      min-height:var(--top-row-h);
      flex:0 0 auto;
    }

    .top-btn{
      appearance:none;
      border:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      margin:0;
      padding:var(--pad-y) var(--pad-x);
      cursor:pointer;
      display:flex;
      align-items:flex-start;
      justify-content:flex-start;
      text-align:left;
      line-height:1.1;
      min-height:var(--top-row-h);
      font-size:var(--font-main);
      font-weight:400;
      transition:background .15s ease, color .15s ease;
    }

    .top-btn + .top-btn{
      border-left:none;
    }

    .top-btn.active{
      background:var(--active);
    }

    .btn-stack{
      display:flex;
      flex-direction:column;
      align-items:flex-start;
      justify-content:center;
      gap:4px;
    }

    .btn-topline{
      font-size:var(--font-small);
      font-weight:400;
      line-height:1;
    }

    .btn-mainline{
      font-size:var(--font-main);
      font-weight:400;
      line-height:1.1;
    }

    .btn-center{
      width:100%;
      height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      font-size:var(--font-main);
      line-height:1.1;
    }

    .selector-panel{
      width:100%;
      border:var(--border-size) solid var(--border);
      background:#fff;
      overflow:hidden;
      max-height:0;
      opacity:0;
      transform:translateY(-6px);
      transition:max-height .22s ease, opacity .18s ease, transform .18s ease, margin .18s ease;
      margin-top:0;
      flex:0 0 auto;
    }

    .selector-panel.open{
      max-height:var(--selector-max-h);
      opacity:1;
      transform:translateY(0);
      margin-top:0;
    }

    .selector-toolbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding:10px 12px;
      border-bottom:var(--border-size) solid var(--border);
      min-height:54px;
    }

    .selector-status{
      font-size:var(--font-title);
      line-height:1.1;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .selector-action{
      border:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      min-height:36px;
      padding:6px 12px;
      cursor:pointer;
      font-size:13px;
      white-space:nowrap;
    }

    .selector-search-wrap{
      padding:10px 12px;
      border-bottom:var(--border-size) solid var(--border);
    }

    .selector-search{
      width:100%;
      height:42px;
      border:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      outline:none;
      padding:0 12px;
      font-size:14px;
    }

    .selector-list{
      overflow:auto;
      max-height:calc(var(--selector-max-h) - 108px);
      background:#fff;
    }

    .thread-item{
      border-bottom:var(--border-size) solid var(--border);
      padding:12px;
      cursor:pointer;
      background:#fff;
      transition:background .15s ease;
    }

    .thread-item:last-child{
      border-bottom:none;
    }

    .thread-item:hover{
      background:var(--hover);
    }

    .thread-item.active{
      background:var(--active);
    }

    .thread-top{
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:8px;
      margin-bottom:6px;
    }

    .thread-title{
      font-size:15px;
      line-height:1.2;
      word-break:break-word;
    }

    .thread-type{
      flex:0 0 auto;
      border:1px solid var(--border);
      padding:2px 6px;
      font-size:11px;
      line-height:1.2;
      background:#fff;
      text-transform:uppercase;
    }

    .thread-preview{
      font-size:13px;
      line-height:1.25;
      color:var(--muted);
      word-break:break-word;
    }

    .chat-shell{
      flex:1;
      min-height:0;
      display:flex;
      flex-direction:column;
      border:var(--border-size) solid var(--border);
      background:#fff;
    }

    .chat-title{
      height:var(--title-row-h);
      min-height:var(--title-row-h);
      border-bottom:var(--border-size) solid var(--border);
      display:flex;
      align-items:center;
      padding:0 var(--pad-x);
      font-size:var(--font-title);
      font-weight:400;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
      background:#fff;
    }

    .messages-area{
      flex:1;
      min-height:160px;
      overflow:auto;
      background:#fff;
      padding:14px;
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    .empty-state{
      flex:1;
      min-height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      padding:20px;
      color:var(--muted);
      font-size:14px;
      line-height:1.4;
    }

    .message{
      max-width:min(78%, 560px);
      border:var(--border-size) solid var(--border);
      padding:10px 12px;
      font-size:var(--font-input);
      line-height:1.3;
      background:#fff;
      word-break:break-word;
      align-self:flex-start;
    }

    .message.out{
      align-self:flex-end;
    }

    .message strong{
      display:block;
      margin-bottom:4px;
      font-size:12px;
      font-weight:700;
      color:var(--text);
    }

    .input-row{
      height:var(--input-row-h);
      min-height:var(--input-row-h);
      border-top:var(--border-size) solid var(--border);
      display:grid;
      grid-template-columns: 1fr var(--send-w);
      gap:0;
      background:#fff;
    }

    .chat-input{
      width:100%;
      height:100%;
      border:none;
      outline:none;
      padding:0 var(--pad-x);
      font-size:var(--font-input);
      color:var(--text);
      background:#fff;
    }

    .chat-input::placeholder{
      color:#111111;
      opacity:1;
    }

    .chat-input:disabled,
    .send-btn:disabled{
      cursor:not-allowed;
      opacity:.5;
    }

    .send-btn{
      height:100%;
      width:100%;
      border:none;
      border-left:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      font-size:var(--font-send);
      font-weight:400;
      cursor:pointer;
    }

    .send-btn:active,
    .top-btn:active,
    .selector-action:active{
      background:#ececec;
    }

    .user-search-modal{
      position:fixed;
      inset:0;
      background:rgba(0,0,0,.28);
      display:flex;
      align-items:center;
      justify-content:center;
      padding:12px;
      z-index:2000;
    }

    .modal-content{
      width:min(520px, 100%);
      max-height:min(82vh, 720px);
      border:var(--border-size) solid var(--border);
      background:#fff;
      display:flex;
      flex-direction:column;
      overflow:hidden;
    }

    .modal-header{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding:12px;
      border-bottom:var(--border-size) solid var(--border);
    }

    .modal-title{
      font-size:var(--font-title);
      line-height:1.2;
    }

    .close-modal{
      border:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      min-width:36px;
      height:36px;
      cursor:pointer;
      font-size:18px;
      line-height:1;
    }

    .modal-body{
      padding:12px;
      display:flex;
      flex-direction:column;
      gap:12px;
      min-height:0;
    }

    .modal-body input{
      width:100%;
      height:42px;
      border:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      outline:none;
      padding:0 12px;
      font-size:14px;
    }

    .user-list{
      overflow:auto;
      min-height:120px;
      max-height:min(50vh, 420px);
      border:var(--border-size) solid var(--border);
      background:#fff;
    }

    .user-item{
      padding:10px 12px;
      border-bottom:var(--border-size) solid var(--border);
      cursor:pointer;
      background:#fff;
    }

    .user-item:last-child{
      border-bottom:none;
    }

    .user-item:hover{
      background:var(--hover);
    }

    .loading,
    .error{
      padding:16px;
      text-align:center;
      font-size:14px;
      line-height:1.4;
    }

    .error{
      color:var(--danger);
    }

    @media (max-width: 768px){
      :root{
        --frame-margin: 6px;
        --border-size: 2px;
        --top-row-h: 56px;
        --title-row-h: 42px;
        --input-row-h: 52px;
        --pad-x: 8px;
        --pad-y: 6px;
        --font-main: 14px;
        --font-small: 11px;
        --font-title: 14px;
        --font-input: 14px;
        --font-send: 14px;
        --send-w: 96px;
        --selector-max-h: min(40vh, 360px);
      }

      .inner{
        padding:10px;
      }

      .btn-stack{
        gap:2px;
      }

      .btn-mainline{
        word-break:break-word;
      }

      .messages-area{
        padding:10px;
      }

      .thread-top{
        align-items:center;
      }

      .thread-title{
        font-size:14px;
      }

      .thread-preview{
        font-size:12px;
      }

      .selector-toolbar{
        padding:8px 10px;
        min-height:50px;
      }

      .selector-search-wrap,
      .modal-body{
        padding:10px;
      }
    }

    @media (max-width: 420px){
      :root{
        --font-main: 13px;
        --font-small: 10px;
        --font-title: 13px;
        --font-input: 13px;
        --font-send: 13px;
        --send-w: 88px;
      }

      .inner{
        padding:8px;
      }

      .selector-action{
        font-size:12px;
        padding:6px 8px;
      }

      .thread-type{
        font-size:10px;
        padding:2px 5px;
      }
    }
  </style>
</head>
<body>
  <div id="app">
    <div class="frame">
      <div class="inner">

        <div class="top-buttons">
          <button class="top-btn active" id="btnSocorristas" type="button">
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

        <div class="selector-panel" id="selectorPanel">
          <div class="selector-toolbar">
            <div class="selector-status" id="selectorStatus">Conversaciones</div>
            <button class="selector-action" id="newChatBtn" type="button">+ Nuevo chat</button>
          </div>
          <div class="selector-search-wrap">
            <input type="text" id="threadSearch" class="selector-search" placeholder="Buscar conversación" autocomplete="off" />
          </div>
          <div class="selector-list" id="threadList">
            <div class="loading">Cargando conversaciones...</div>
          </div>
        </div>

        <div class="chat-shell">
          <div class="chat-title" id="chatHeader">Selecciona una conversación</div>

          <div class="messages-area" id="messagesArea">
            <div class="empty-state">No hay mensajes</div>
          </div>

          <div class="input-row" id="inputArea" style="display:none;">
            <input
              id="chatInput"
              class="chat-input"
              type="text"
              placeholder="Dialogo para enviar Mensaje"
              autocomplete="off"
            />
            <button id="sendBtn" class="send-btn" type="button">SEND</button>
          </div>
        </div>

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
  let currentTopMode = "socorristas";

  function escapeHtml(text) {
    return String(text)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function setFrameFullscreen() {
    const fe = window.frameElement;
    if (!fe) return;
    fe.style.position = "fixed";
    fe.style.inset = "0";
    fe.style.width = "100vw";
    fe.style.height = "100vh";
    fe.style.border = "0";
    fe.style.margin = "0";
    fe.style.padding = "0";
    fe.style.zIndex = "999999";
    fe.style.background = "transparent";
  }

  function getThreadTypeLabel(thread) {
    const type = String(thread && thread.type ? thread.type : "").toLowerCase();
    if (type === "private") return "SOC";
    if (type === "group") return "INST";
    return "CHAT";
  }

  function getModeLabel(mode) {
    if (mode === "socorristas") return "Socorristas";
    if (mode === "instalacion") return "Instalación";
    return "Notificaciones";
  }

  function getThreadMode(thread) {
    const type = String(thread && thread.type ? thread.type : "").toLowerCase();
    if (type === "private") return "socorristas";
    if (type === "group") return "instalacion";
    return "notificaciones";
  }

  function getFilteredThreads() {
    const query = (document.getElementById("threadSearch")?.value || "").trim().toLowerCase();
    return threads.filter(function(thread) {
      const type = String(thread.type || "").toLowerCase();
      let passesMode = true;

      if (currentTopMode === "socorristas") {
        passesMode = type === "private";
      } else if (currentTopMode === "instalacion") {
        passesMode = type !== "private";
      } else {
        passesMode = true;
      }

      if (!passesMode) return false;

      if (!query) return true;

      const title = String(thread.title || "").toLowerCase();
      const lastMessage = String(thread.last_message || "").toLowerCase();
      return title.includes(query) || lastMessage.includes(query) || String(thread.id).includes(query);
    });
  }

  function showSelectorPanel(show) {
    const panel = document.getElementById("selectorPanel");
    if (!panel) return;
    panel.classList.toggle("open", !!show);
  }

  function setTopMode(mode, keepPanelOpen = true) {
    currentTopMode = mode;

    document.getElementById("btnSocorristas").classList.toggle("active", mode === "socorristas");
    document.getElementById("btnInstalacion").classList.toggle("active", mode === "instalacion");
    document.getElementById("btnNotificaciones").classList.toggle("active", mode === "notificaciones");

    document.getElementById("selectorStatus").textContent = getModeLabel(mode);
    renderThreadList();

    if (keepPanelOpen) {
      showSelectorPanel(true);
    }
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
        const firstThread = threads[0];
        setTopMode(getThreadMode(firstThread), false);
        setActiveThread(firstThread.id);
      }

      if (threads.length === 0) {
        document.getElementById("chatHeader").textContent = "Selecciona una conversación";
        document.getElementById("messagesArea").innerHTML = '<div class="empty-state">No hay conversaciones disponibles</div>';
        document.getElementById("inputArea").style.display = "none";
        showSelectorPanel(true);
      }
    } catch (error) {
      console.error("Error loading threads:", error);
      listDiv.innerHTML = '<div class="error">Error al cargar conversaciones.<br>' + escapeHtml(error.message) + '</div>';
    }
  }

  function renderThreadList() {
    const container = document.getElementById("threadList");
    const filteredThreads = getFilteredThreads();

    if (filteredThreads.length === 0) {
      container.innerHTML = '<div class="loading">No hay conversaciones para mostrar</div>';
      return;
    }

    container.innerHTML = filteredThreads.map(function(thread) {
      const title = thread.title || (thread.type === "private" ? "Privado" : "Grupo");
      return ''
        + '<div class="thread-item' + (String(currentThreadId) === String(thread.id) ? ' active' : '') + '" data-id="' + escapeHtml(thread.id) + '">'
        +   '<div class="thread-top">'
        +     '<div class="thread-title">' + escapeHtml(title) + '</div>'
        +     '<div class="thread-type">' + escapeHtml(getThreadTypeLabel(thread)) + '</div>'
        +   '</div>'
        +   '<div class="thread-preview">' + escapeHtml(thread.last_message || 'Sin mensajes') + '</div>'
        + '</div>';
    }).join("");

    container.querySelectorAll(".thread-item").forEach(function(el) {
      el.addEventListener("click", function() {
        setActiveThread(el.getAttribute("data-id"));
      });
    });
  }

  async function loadMessages(threadId, poll = false) {
    const limit = poll ? 30 : 500;
    const url = API_BASE + "/threads/" + threadId + "/messages?user_id=" + encodeURIComponent(currentUserId) + "&limit=" + limit;

    try {
      const data = await fetchJSON(url);
      let messages = data.messages || [];
      if (poll && lastRenderedMessageId !== null) {
        messages = messages.filter(function(msg) {
          return parseInt(msg.id, 10) > lastRenderedMessageId;
        });
      }

      const container = document.getElementById("messagesArea");

      if (!poll) {
        container.innerHTML = "";
        lastRenderedMessageId = null;
      }

      if (messages.length === 0 && !poll) {
        container.innerHTML = '<div class="empty-state">No hay mensajes</div>';
        lastRenderedMessageId = null;
        return;
      }

      messages.forEach(function(msg) {
        const div = document.createElement("div");
        div.className = "message" + (String(msg.sender_id) === String(currentUserId) ? " out" : "");
        div.setAttribute("data-id", msg.id);
        div.innerHTML = '<strong>' + escapeHtml(msg.sender_alias || "Usuario") + '</strong>' + escapeHtml(msg.body || "");
        container.appendChild(div);
        lastRenderedMessageId = parseInt(msg.id, 10);
      });

      container.scrollTop = container.scrollHeight;
      await markThreadRead(threadId);
    } catch (error) {
      console.error("Error loading messages:", error);
      const container = document.getElementById("messagesArea");
      if (!poll) {
        container.innerHTML = '<div class="error">Error al cargar mensajes<br>' + escapeHtml(error.message) + '</div>';
      }
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
        body: JSON.stringify({
          user_id: currentUserId,
          last_read_message_id: lastId
        })
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
        body: JSON.stringify({
          sender_id: currentUserId,
          body: text
        })
      });
      await loadMessages(currentThreadId, false);
      await loadThreads();
    } catch (error) {
      console.error("Error sending message:", error);
      alert("Error al enviar mensaje: " + error.message);
    }
  }

  function setActiveThread(threadId) {
    currentThreadId = threadId;

    const thread = threads.find(function(item) {
      return String(item.id) === String(threadId);
    });

    if (thread) {
      setTopMode(getThreadMode(thread), false);
      document.getElementById("chatHeader").innerText = thread.title || (thread.type === "private" ? "Privado" : "Grupo");
    } else {
      document.getElementById("chatHeader").innerText = "Conversación";
    }

    document.getElementById("inputArea").style.display = "grid";
    document.getElementById("chatInput").disabled = false;
    document.getElementById("sendBtn").disabled = false;

    showSelectorPanel(false);
    renderThreadList();
    loadMessages(threadId, false);

    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(function() {
      if (currentThreadId) {
        loadMessages(currentThreadId, true);
      }
    }, 10000);
  }

  function showNewChatModal() {
    const modal = document.createElement("div");
    modal.className = "user-search-modal";
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">Nuevo chat</div>
          <button class="close-modal" type="button">&times;</button>
        </div>
        <div class="modal-body">
          <input type="text" id="userSearch" placeholder="Buscar por alias o DNI" autocomplete="off" />
          <div id="userSearchResults" class="user-list">
            <div class="loading">Escribe al menos 2 caracteres</div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const closeBtn = modal.querySelector(".close-modal");
    const searchInput = modal.querySelector("#userSearch");
    const resultsDiv = modal.querySelector("#userSearchResults");

    function closeModal() {
      modal.remove();
    }

    closeBtn.addEventListener("click", closeModal);
    modal.addEventListener("click", function(event) {
      if (event.target === modal) {
        closeModal();
      }
    });

    async function searchUsers() {
      const query = searchInput.value.trim().toLowerCase();

      if (query.length < 2) {
        resultsDiv.innerHTML = '<div class="loading">Escribe al menos 2 caracteres</div>';
        return;
      }

      try {
        const users = await fetchJSON(API_BASE + "/users");
        const filtered = users.filter(function(user) {
          const alias = String(user.alias || "").toLowerCase();
          const dni = String(user.dni || "");
          return alias.includes(query) || dni.includes(query);
        });

        if (filtered.length === 0) {
          resultsDiv.innerHTML = '<div class="loading">No se encontraron usuarios</div>';
          return;
        }

        resultsDiv.innerHTML = filtered.map(function(user) {
          return '<div class="user-item" data-dni="' + escapeHtml(user.dni) + '">@' + escapeHtml(user.alias || "Usuario") + ' (' + escapeHtml(user.dni) + ')</div>';
        }).join("");

        resultsDiv.querySelectorAll(".user-item").forEach(function(el) {
          el.addEventListener("click", async function() {
            const otherDni = el.getAttribute("data-dni");

            if (String(otherDni) === String(currentUserId)) {
              alert("No puedes chatear contigo mismo");
              return;
            }

            try {
              const data = await fetchJSON(API_BASE + "/private/" + encodeURIComponent(otherDni) + "?user_id=" + encodeURIComponent(currentUserId));
              if (data.thread_id) {
                closeModal();
                await loadThreads();
                setActiveThread(data.thread_id);
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
    searchInput.focus();
  }

  function bindEvents() {
    document.getElementById("btnSocorristas").addEventListener("click", function() {
      setTopMode("socorristas", true);
    });

    document.getElementById("btnInstalacion").addEventListener("click", function() {
      setTopMode("instalacion", true);
    });

    document.getElementById("btnNotificaciones").addEventListener("click", function() {
      setTopMode("notificaciones", true);
    });

    document.getElementById("newChatBtn").addEventListener("click", showNewChatModal);
    document.getElementById("sendBtn").addEventListener("click", sendMessage);

    document.getElementById("chatInput").addEventListener("keydown", function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
      }
    });

    document.getElementById("threadSearch").addEventListener("input", function() {
      renderThreadList();
    });
  }

  setFrameFullscreen();
  bindEvents();
  showSelectorPanel(true);
  loadThreads();
  threadsPollingInterval = setInterval(loadThreads, 15000);
</script>
</body>
</html>
""".replace("REEMPLAZAR_DNI", USER_DNI)

components.html(html, height=10, scrolling=False)
