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
      transition:max-height .22s ease, opacity .18s ease, transform .18s ease;
      flex:0 0 auto;
    }

    .selector-panel.open{
      max-height:var(--selector-max-h);
      opacity:1;
      transform:translateY(0);
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

    .selector-list{
      overflow:auto;
      max-height:calc(var(--selector-max-h) - 56px);
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

    .thread-title{
      font-size:15px;
      line-height:1.2;
      word-break:break-word;
      margin-bottom:6px;
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

      .selector-toolbar{
        padding:8px 10px;
        min-height:50px;
      }

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

        <div class="selector-panel open" id="selectorPanel">
          <div class="selector-toolbar">
            <div class="selector-status" id="selectorStatus">Conversaciones</div>
            <button class="selector-action" id="newChatBtn" type="button">+ Nuevo chat</button>
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

          <div class="input-row" style="display:none;" id="inputArea">
            <input
              type="text"
              id="chatInput"
              class="chat-input"
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
  (function () {
    const fe = window.frameElement;
    if (fe) {
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
    let threads = [];
    let pollingInterval = null;
    let threadsPollingInterval = null;
    let lastRenderedMessageId = null;

    const btnSocorristas = document.getElementById("btnSocorristas");
    const btnInstalacion = document.getElementById("btnInstalacion");
    const btnNotificaciones = document.getElementById("btnNotificaciones");
    const selectorPanel = document.getElementById("selectorPanel");
    const selectorStatus = document.getElementById("selectorStatus");

    function escapeHtml(text) {
      return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function setActiveTop(button, label) {
      [btnSocorristas, btnInstalacion, btnNotificaciones].forEach(function(btn) {
        btn.classList.remove("active");
      });
      button.classList.add("active");
      selectorStatus.textContent = label;
      selectorPanel.classList.add("open");
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
        container.innerHTML = '<div class="loading">No hay conversaciones</div>';
        return;
      }
      container.innerHTML = threads.map(function(t) {
        return '<div class="thread-item' + (currentThreadId == t.id ? ' active' : '') + '" data-id="' + t.id + '">' +
                 '<div class="thread-title">' + escapeHtml(t.title || (t.type === "private" ? "Privado" : "Grupo")) + '</div>' +
                 '<div class="thread-preview">' + escapeHtml(t.last_message || "") + '</div>' +
               '</div>';
      }).join("");
      document.querySelectorAll(".thread-item").forEach(function(el) {
        el.addEventListener("click", function() {
          setActiveThread(el.getAttribute("data-id"));
        });
      });
    }

    async function loadMessages(threadId, poll = false) {
      const limit = poll ? 30 : 500;
      let url = API_BASE + "/threads/" + threadId + "/messages?user_id=" + encodeURIComponent(currentUserId) + "&limit=" + limit;
      try {
        const data = await fetchJSON(url);
        let messages = data.messages || [];
        if (poll && lastRenderedMessageId !== null) {
          messages = messages.filter(function(m) {
            return parseInt(m.id) > lastRenderedMessageId;
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
          div.className = "message" + (msg.sender_id == currentUserId ? " out" : "");
          div.setAttribute("data-id", msg.id);
          div.innerHTML = '<strong>' + escapeHtml(msg.sender_alias || "Usuario") + ':</strong>' + escapeHtml(msg.body || "");
          container.appendChild(div);
          lastRenderedMessageId = parseInt(msg.id);
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
      const thread = threads.find(function(t) {
        return t.id == threadId;
      });
      document.getElementById("chatHeader").innerText = thread ? thread.title : "Conversación";
      document.getElementById("inputArea").style.display = "grid";
      renderThreadList();
      selectorPanel.classList.remove("open");
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
          <div class="modal-header">
            <div class="modal-title">Nuevo chat</div>
            <button class="close-modal" type="button">&times;</button>
          </div>
          <div class="modal-body">
            <input type="text" id="userSearch" placeholder="Buscar por alias o DNI" autocomplete="off">
            <div id="userSearchResults" class="user-list"><div class="loading">Escribe al menos 2 caracteres</div></div>
          </div>
        </div>
      `;
      document.body.appendChild(modal);

      const closeBtn = modal.querySelector(".close-modal");
      closeBtn.onclick = function() {
        modal.remove();
      };

      modal.addEventListener("click", function(e) {
        if (e.target === modal) {
          modal.remove();
        }
      });

      const searchInput = modal.querySelector("#userSearch");
      const resultsDiv = modal.querySelector("#userSearchResults");

      async function searchUsers() {
        const query = searchInput.value.trim().toLowerCase();
        if (query.length < 2) {
          resultsDiv.innerHTML = '<div class="loading">Escribe al menos 2 caracteres</div>';
          return;
        }
        try {
          const users = await fetchJSON(API_BASE + "/users");
          const filtered = users.filter(function(u) {
            return u.alias.toLowerCase().includes(query) || u.dni.includes(query);
          });
          if (filtered.length === 0) {
            resultsDiv.innerHTML = '<div class="loading">No se encontraron usuarios</div>';
            return;
          }
          resultsDiv.innerHTML = filtered.map(function(u) {
            return '<div class="user-item" data-dni="' + u.dni + '">@' + escapeHtml(u.alias) + ' (' + u.dni + ')</div>';
          }).join("");
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
      searchInput.focus();
    }

    btnSocorristas.addEventListener("click", function() {
      setActiveTop(btnSocorristas, "Socorristas");
    });

    btnInstalacion.addEventListener("click", function() {
      setActiveTop(btnInstalacion, "Instalación");
    });

    btnNotificaciones.addEventListener("click", function() {
      setActiveTop(btnNotificaciones, "Notificaciones");
    });

    document.getElementById("newChatBtn").addEventListener("click", showNewChatModal);
    document.getElementById("sendBtn").addEventListener("click", sendMessage);
    document.getElementById("chatInput").addEventListener("keypress", function(e) {
      if (e.key === "Enter") sendMessage();
    });

    loadThreads();
    threadsPollingInterval = setInterval(loadThreads, 15000);
  })();
</script>
</body>
</html>
""".replace("REEMPLAZAR_DNI", USER_DNI)

components.html(html, height=10, scrolling=False)
