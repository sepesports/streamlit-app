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
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
  <title>Chat</title>
  <style>
    :root{
      --bg:#ffffff;
      --text:#111111;
      --border:#111111;
      --soft:#f5f5f5;
      --soft2:#efefef;
      --muted:#666666;
      --danger:#b00020;

      --frame-margin:clamp(6px,1.2vw,14px);
      --frame-pad:clamp(18px,2vw,28px);
      --border-size:2px;

      --top-row-h:clamp(58px,8vh,72px);
      --title-row-h:clamp(42px,6vh,54px);
      --input-row-h:clamp(52px,7vh,62px);

      --font-main:clamp(14px,1.25vw,18px);
      --font-small:clamp(12px,1vw,14px);
      --font-title:clamp(15px,1.35vw,19px);
      --font-body:clamp(13px,1.15vw,17px);

      --send-w:clamp(92px,18vw,130px);
      --modal-w:min(720px,calc(100vw - 24px));
      --modal-h:min(74vh,760px);
    }

    *{ box-sizing:border-box; -webkit-tap-highlight-color:transparent; }

    html, body{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--bg);
      color:var(--text);
      font-family:Arial, Helvetica, sans-serif;
    }

    #app{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      padding:var(--frame-margin);
      background:var(--bg);
    }

    .frame{
      width:100%;
      height:100%;
      border:var(--border-size) solid var(--border);
      background:#fff;
      overflow:hidden;
    }

    .inner{
      width:100%;
      height:100%;
      display:flex;
      flex-direction:column;
      gap:12px;
      padding:var(--frame-pad);
    }

    .top-buttons{
      display:grid;
      grid-template-columns:1fr 1fr 1.15fr;
      width:100%;
      min-height:var(--top-row-h);
    }

    .top-btn{
      border:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      margin:0;
      padding:8px 10px;
      min-height:var(--top-row-h);
      display:flex;
      align-items:flex-start;
      justify-content:flex-start;
      text-align:left;
      cursor:pointer;
      transition:background .15s ease;
      font-size:var(--font-main);
      line-height:1.1;
    }

    .top-btn + .top-btn{ border-left:none; }
    .top-btn:hover{ background:var(--soft); }
    .top-btn.active{ background:var(--soft2); }

    .btn-stack{
      display:flex;
      flex-direction:column;
      align-items:flex-start;
      justify-content:center;
      gap:4px;
      width:100%;
      height:100%;
    }

    .btn-topline{
      font-size:var(--font-small);
      line-height:1;
      font-weight:400;
    }

    .btn-mainline{
      font-size:var(--font-main);
      line-height:1.1;
      font-weight:400;
      word-break:break-word;
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
      justify-content:flex-start;
      padding:0 12px;
      font-size:var(--font-title);
      line-height:1.1;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .chat-body{
      flex:1;
      min-height:160px;
      overflow:auto;
      background:#fff;
      padding:14px;
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    .chat-placeholder{
      width:100%;
      text-align:center;
      color:var(--muted);
      font-size:var(--font-body);
      padding-top:18px;
    }

    .message{
      max-width:82%;
      padding:10px 12px;
      border:var(--border-size) solid var(--border);
      background:#fff;
      align-self:flex-start;
      word-break:break-word;
      white-space:pre-wrap;
      line-height:1.35;
      font-size:var(--font-body);
    }

    .message.out{
      background:var(--soft);
      align-self:flex-end;
    }

    .message strong{
      display:block;
      margin-bottom:4px;
      font-size:12px;
      color:var(--text);
    }

    .input-area{
      height:var(--input-row-h);
      min-height:var(--input-row-h);
      border-top:var(--border-size) solid var(--border);
      display:grid;
      grid-template-columns:1fr var(--send-w);
      background:#fff;
    }

    #chatInput{
      width:100%;
      height:100%;
      border:none;
      outline:none;
      padding:0 12px;
      font-size:var(--font-body);
      color:var(--text);
      background:#fff;
    }

    #chatInput::placeholder{
      color:var(--muted);
      opacity:1;
    }

    #chatInput:disabled{
      background:#fafafa;
      color:#999999;
      cursor:not-allowed;
    }

    #sendBtn{
      width:100%;
      height:100%;
      border:none;
      border-left:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      font-size:var(--font-body);
      cursor:pointer;
    }

    #sendBtn:hover:not(:disabled){ background:var(--soft); }
    #sendBtn:disabled{
      background:#fafafa;
      color:#999999;
      cursor:not-allowed;
    }

    .selector-modal{
      position:fixed;
      inset:0;
      display:none;
      align-items:center;
      justify-content:center;
      background:rgba(0,0,0,.42);
      z-index:999999;
      padding:12px;
    }

    .selector-modal.show{ display:flex; }

    .selector-card{
      width:var(--modal-w);
      height:var(--modal-h);
      background:#fff;
      border:var(--border-size) solid var(--border);
      display:flex;
      flex-direction:column;
      overflow:hidden;
    }

    .selector-head{
      min-height:54px;
      border-bottom:var(--border-size) solid var(--border);
      display:grid;
      grid-template-columns:1fr 48px;
      align-items:center;
    }

    .selector-title{
      padding:0 12px;
      font-size:var(--font-title);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .selector-close{
      width:48px;
      height:100%;
      border:none;
      border-left:var(--border-size) solid var(--border);
      background:#fff;
      font-size:20px;
      cursor:pointer;
    }

    .selector-search-wrap{
      border-bottom:var(--border-size) solid var(--border);
      padding:10px;
    }

    .selector-search{
      width:100%;
      height:42px;
      border:var(--border-size) solid var(--border);
      background:#fff;
      padding:0 10px;
      outline:none;
      font-size:var(--font-body);
      color:var(--text);
    }

    .selector-list{
      flex:1;
      min-height:0;
      overflow:auto;
      background:#fff;
    }

    .section-label{
      padding:10px 12px 8px;
      font-size:12px;
      font-weight:700;
      color:var(--muted);
      border-bottom:1px solid #d8d8d8;
      background:#fafafa;
    }

    .selector-item{
      width:100%;
      border:none;
      border-bottom:1px solid #d8d8d8;
      background:#fff;
      text-align:left;
      padding:12px;
      cursor:pointer;
      display:block;
    }

    .selector-item:hover{ background:var(--soft); }

    .selector-item.active{
      background:var(--soft2);
    }

    .selector-item-title{
      font-size:var(--font-body);
      line-height:1.2;
      margin-bottom:4px;
      color:var(--text);
    }

    .selector-item-sub{
      font-size:12px;
      line-height:1.2;
      color:var(--muted);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .loading, .error, .selector-empty{
      text-align:center;
      padding:18px 12px;
      color:var(--muted);
      font-size:var(--font-body);
    }

    .error{ color:var(--danger); }

    @media (max-width: 768px){
      :root{
        --frame-margin:6px;
        --frame-pad:10px;
        --top-row-h:56px;
        --title-row-h:42px;
        --input-row-h:52px;
        --font-main:14px;
        --font-small:11px;
        --font-title:14px;
        --font-body:14px;
        --send-w:92px;
      }

      .chat-body{ padding:10px; }
      .message{ max-width:88%; }
    }

    @media (max-width: 420px){
      :root{
        --font-main:13px;
        --font-small:10px;
        --font-title:13px;
        --font-body:13px;
        --send-w:86px;
      }

      .inner{ gap:8px; }
    }
  </style>
</head>
<body>
<div id="app">
  <div class="frame">
    <div class="inner">

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
        <div class="chat-title" id="chatHeader">Nombre del socorrista o Grupo de instalación</div>

        <div class="chat-body" id="messagesArea">
          <div class="chat-placeholder">Cargando conversaciones...</div>
        </div>

        <div class="input-area" id="inputArea">
          <input type="text" id="chatInput" placeholder="Dialogo para enviar Mensaje" autocomplete="off" disabled>
          <button id="sendBtn" disabled>SEND</button>
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
  (function(){
    var fe = window.frameElement;
    if (fe){
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

    const API_BASE = "https://camilo27.pythonanywhere.com/api/chat";
    const currentUserId = "REEMPLAZAR_DNI";
    let currentThreadId = null;
    let currentMode = null;
    let threads = [];
    let pollingInterval = null;
    let threadsPollingInterval = null;
    let lastRenderedMessageId = null;
    let usersCache = [];

    const btnSocorristas = document.getElementById("btnSocorristas");
    const btnInstalacion = document.getElementById("btnInstalacion");
    const btnNotificaciones = document.getElementById("btnNotificaciones");
    const chatHeader = document.getElementById("chatHeader");
    const messagesArea = document.getElementById("messagesArea");
    const inputArea = document.getElementById("inputArea");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");

    const selectorModal = document.getElementById("selectorModal");
    const selectorTitle = document.getElementById("selectorTitle");
    const selectorSearch = document.getElementById("selectorSearch");
    const selectorList = document.getElementById("selectorList");
    const selectorClose = document.getElementById("selectorClose");

    function escapeHtml(text) {
      return String(text)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
    }

    async function fetchJSON(url, options = {}) {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status} - ${response.statusText}`);
      }
      return response.json();
    }

    function setTopActive(mode) {
      btnSocorristas.classList.remove("active");
      btnInstalacion.classList.remove("active");
      btnNotificaciones.classList.remove("active");

      if (mode === "socorristas") btnSocorristas.classList.add("active");
      if (mode === "instalacion") btnInstalacion.classList.add("active");
      if (mode === "notificaciones") btnNotificaciones.classList.add("active");
    }

    function updateSendState() {
      const enabled = !!currentThreadId;
      chatInput.disabled = !enabled;
      sendBtn.disabled = !enabled;
      if (!enabled) {
        chatInput.value = "";
      }
    }

    function getThreadTitle(thread) {
      if (!thread) return "Conversación";
      return thread.title || (thread.type === "private" ? "Privado" : "Grupo");
    }

    function getPrivateThreads() {
      return threads.filter(function(t){ return t.type === "private"; });
    }

    function getGroupThreads() {
      return threads.filter(function(t){ return t.type !== "private"; });
    }

    async function loadThreads() {
      try {
        const data = await fetchJSON(API_BASE + "/threads?user_id=" + encodeURIComponent(currentUserId));
        threads = data.threads || [];

        if (threads.length === 0) {
          currentThreadId = null;
          chatHeader.innerText = "Nombre del socorrista o Grupo de instalación";
          messagesArea.innerHTML = '<div class="chat-placeholder">No hay conversaciones</div>';
          updateSendState();
          if (selectorModal.classList.contains("show")) {
            renderSelector();
          }
          return;
        }

        if (!currentThreadId) {
          setActiveThread(threads[0].id);
        } else {
          const thread = threads.find(function(t){ return String(t.id) === String(currentThreadId); });
          if (!thread) {
            setActiveThread(threads[0].id);
          } else {
            chatHeader.innerText = getThreadTitle(thread);
          }
        }

        if (selectorModal.classList.contains("show")) {
          renderSelector();
        }
      } catch (error) {
        console.error("Error loading threads:", error);
        messagesArea.innerHTML = '<div class="error">Error al cargar conversaciones.<br>' + escapeHtml(error.message) + '</div>';
      }
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

        if (!poll) {
          messagesArea.innerHTML = "";
          lastRenderedMessageId = null;
        }

        if (messages.length === 0 && !poll) {
          messagesArea.innerHTML = '<div class="chat-placeholder">No hay mensajes</div>';
          lastRenderedMessageId = null;
          return;
        }

        messages.forEach(function(msg) {
          const div = document.createElement("div");
          div.className = "message" + (msg.sender_id == currentUserId ? " out" : "");
          div.setAttribute("data-id", msg.id);
          div.innerHTML = '<strong>' + escapeHtml(msg.sender_alias || 'Usuario') + '</strong>' + escapeHtml(msg.body);
          messagesArea.appendChild(div);
          lastRenderedMessageId = parseInt(msg.id);
        });

        messagesArea.scrollTop = messagesArea.scrollHeight;
        await markThreadRead(threadId);
      } catch (error) {
        console.error("Error loading messages:", error);
        if (!poll) {
          messagesArea.innerHTML = '<div class="error">Error al cargar mensajes<br>' + escapeHtml(error.message) + '</div>';
        }
      }
    }

    async function markThreadRead(threadId) {
      const lastMsg = messagesArea.querySelector(".message:last-child");
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
      const text = chatInput.value.trim();
      if (!text) return;

      chatInput.value = "";

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
      chatHeader.innerText = thread ? getThreadTitle(thread) : "Conversación";
      updateSendState();

      if (thread) {
        if (thread.type === "private") {
          setTopActive("socorristas");
        } else {
          setTopActive("instalacion");
        }
      }

      if (pollingInterval) clearInterval(pollingInterval);
      pollingInterval = setInterval(function() {
        if (currentThreadId) loadMessages(currentThreadId, true);
      }, 10000);
    }

    function openSelector(mode) {
      currentMode = mode;
      selectorModal.classList.add("show");
      renderSelector();
      setTimeout(function(){ selectorSearch.focus(); }, 20);
    }

    function closeSelector() {
      selectorModal.classList.remove("show");
      selectorSearch.value = "";
      currentMode = null;

      const thread = threads.find(function(t) { return t.id == currentThreadId; });
      if (thread) {
        if (thread.type === "private") setTopActive("socorristas");
        else setTopActive("instalacion");
      } else {
        setTopActive(null);
      }
    }

    async function loadUsersCache() {
      if (usersCache.length > 0) return usersCache;
      const users = await fetchJSON(API_BASE + "/users");
      usersCache = users || [];
      return usersCache;
    }

    function renderThreadItems(list) {
      if (!list.length) {
        return '<div class="selector-empty">No hay conversaciones</div>';
      }

      return list.map(function(t) {
        return '<button class="selector-item thread-item-modal' + (currentThreadId == t.id ? ' active' : '') + '" data-id="' + t.id + '">' +
                 '<div class="selector-item-title">' + escapeHtml(getThreadTitle(t)) + '</div>' +
                 '<div class="selector-item-sub">' + escapeHtml(t.last_message || '') + '</div>' +
               '</button>';
      }).join('');
    }

    function bindThreadItems() {
      selectorList.querySelectorAll(".thread-item-modal").forEach(function(el) {
        el.addEventListener("click", function() {
          setActiveThread(el.getAttribute("data-id"));
          closeSelector();
        });
      });
    }

    async function renderSelector() {
      const query = selectorSearch.value.trim().toLowerCase();

      if (currentMode === "socorristas") {
        setTopActive("socorristas");
        selectorTitle.innerText = "Socorristas";
        selectorSearch.placeholder = "Buscar por alias o DNI";
        selectorList.innerHTML = '<div class="loading">Cargando...</div>';

        try {
          const users = await loadUsersCache();
          const privateThreads = getPrivateThreads().filter(function(t) {
            const title = String(getThreadTitle(t) || "").toLowerCase();
            const preview = String(t.last_message || "").toLowerCase();
            return !query || title.includes(query) || preview.includes(query);
          });

          const filteredUsers = users.filter(function(u) {
            const alias = String(u.alias || "").toLowerCase();
            const dni = String(u.dni || "");
            if (dni == currentUserId) return false;
            return !query || alias.includes(query) || dni.includes(query);
          });

          let html = '';
          html += '<div class="section-label">Chats privados</div>';
          html += renderThreadItems(privateThreads);
          html += '<div class="section-label">Abrir nuevo chat</div>';

          if (!filteredUsers.length) {
            html += '<div class="selector-empty">No se encontraron usuarios</div>';
          } else {
            html += filteredUsers.map(function(u) {
              return '<button class="selector-item user-item-modal" data-dni="' + u.dni + '">' +
                       '<div class="selector-item-title">@' + escapeHtml(u.alias || "Usuario") + '</div>' +
                       '<div class="selector-item-sub">' + escapeHtml(u.dni || '') + '</div>' +
                     '</button>';
            }).join('');
          }

          selectorList.innerHTML = html;
          bindThreadItems();

          selectorList.querySelectorAll(".user-item-modal").forEach(function(el) {
            el.addEventListener("click", async function() {
              const otherDni = el.getAttribute("data-dni");
              if (otherDni == currentUserId) {
                alert("No puedes chatear contigo mismo");
                return;
              }
              try {
                const data = await fetchJSON(API_BASE + "/private/" + encodeURIComponent(otherDni) + "?user_id=" + encodeURIComponent(currentUserId));
                if (data.thread_id) {
                  closeSelector();
                  await loadThreads();
                  setActiveThread(data.thread_id);
                }
              } catch (error) {
                alert("Error al crear el chat: " + error.message);
              }
            });
          });
        } catch (error) {
          selectorList.innerHTML = '<div class="error">Error al cargar usuarios<br>' + escapeHtml(error.message) + '</div>';
        }

        return;
      }

      if (currentMode === "instalacion") {
        setTopActive("instalacion");
        selectorTitle.innerText = "Instalación";
        selectorSearch.placeholder = "Buscar grupo o instalación";

        const groups = getGroupThreads().filter(function(t) {
          const title = String(getThreadTitle(t) || "").toLowerCase();
          const preview = String(t.last_message || "").toLowerCase();
          return !query || title.includes(query) || preview.includes(query);
        });

        selectorList.innerHTML = '<div class="section-label">Grupos de instalación</div>' + renderThreadItems(groups);
        bindThreadItems();
        return;
      }

      if (currentMode === "notificaciones") {
        setTopActive("notificaciones");
        selectorTitle.innerText = "Notificaciones";
        selectorSearch.placeholder = "Buscar conversación";

        const allThreads = threads.filter(function(t) {
          const title = String(getThreadTitle(t) || "").toLowerCase();
          const preview = String(t.last_message || "").toLowerCase();
          return !query || title.includes(query) || preview.includes(query);
        });

        selectorList.innerHTML = '<div class="section-label">Conversaciones</div>' + renderThreadItems(allThreads);
        bindThreadItems();
      }
    }

    btnSocorristas.addEventListener("click", function() {
      openSelector("socorristas");
    });

    btnInstalacion.addEventListener("click", function() {
      openSelector("instalacion");
    });

    btnNotificaciones.addEventListener("click", function() {
      openSelector("notificaciones");
    });

    selectorClose.addEventListener("click", closeSelector);

    selectorModal.addEventListener("click", function(e) {
      if (e.target === selectorModal) closeSelector();
    });

    selectorSearch.addEventListener("input", function() {
      renderSelector();
    });

    sendBtn.addEventListener("click", sendMessage);

    chatInput.addEventListener("keypress", function(e) {
      if (e.key === "Enter") sendMessage();
    });

    updateSendState();
    loadThreads();
    threadsPollingInterval = setInterval(loadThreads, 15000);
  })();
</script>
</body>
</html>
""".replace("REEMPLAZAR_DNI", USER_DNI)

components.html(html, height=800, scrolling=False)
