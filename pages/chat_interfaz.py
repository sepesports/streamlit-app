# pages/chat_interfaz.py
import json
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

USER_DNI = str(st.query_params.get("dni") or "").strip()
if not USER_DNI:
    st.error("No se pudo identificar al usuario. Por favor, vuelve a iniciar sesión.")
    st.stop()

html = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
  <title>Chat Interfaz</title>
  <style>
    :root{
      --bg:#ffffff;
      --text:#111111;
      --border:#111111;
      --muted:#666666;
      --soft:#f6f6f6;
      --soft-2:#efefef;
      --danger:#b00020;

      --frame-margin:clamp(6px, 1.2vw, 14px);
      --frame-pad:clamp(16px, 2vw, 26px);
      --border-size:2px;

      --top-row-h:clamp(58px, 8vh, 72px);
      --title-row-h:clamp(42px, 6vh, 54px);
      --input-row-h:clamp(50px, 7vh, 62px);

      --font-main:clamp(14px, 1.25vw, 18px);
      --font-small:clamp(12px, 1vw, 14px);
      --font-title:clamp(15px, 1.35vw, 19px);
      --font-body:clamp(13px, 1.15vw, 17px);

      --send-w:clamp(92px, 18vw, 130px);
      --modal-w:min(720px, calc(100vw - 24px));
      --modal-h:min(72vh, 760px);
    }

    *{
      box-sizing:border-box;
      -webkit-tap-highlight-color:transparent;
    }

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

    .top-btn + .top-btn{
      border-left:none;
    }

    .top-btn:hover{
      background:var(--soft);
    }

    .top-btn.active{
      background:var(--soft-2);
    }

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
      min-height:100%;
      display:flex;
      align-items:flex-start;
      justify-content:center;
      text-align:center;
      color:var(--muted);
      font-size:var(--font-body);
      padding-top:20px;
    }

    .msg{
      max-width:min(82%, 620px);
      border:var(--border-size) solid var(--border);
      background:#fff;
      padding:10px 12px;
      align-self:flex-start;
      word-break:break-word;
      white-space:normal;
    }

    .msg.out{
      align-self:flex-end;
      background:var(--soft);
    }

    .msg-author{
      font-size:12px;
      font-weight:700;
      margin-bottom:4px;
    }

    .msg-body{
      font-size:var(--font-body);
      line-height:1.35;
      white-space:pre-wrap;
    }

    .input-row{
      height:var(--input-row-h);
      min-height:var(--input-row-h);
      border-top:var(--border-size) solid var(--border);
      display:grid;
      grid-template-columns:1fr var(--send-w);
      background:#fff;
    }

    .chat-input{
      width:100%;
      height:100%;
      border:none;
      outline:none;
      padding:0 12px;
      font-size:var(--font-body);
      color:var(--text);
      background:#fff;
    }

    .chat-input::placeholder{
      color:var(--muted);
      opacity:1;
    }

    .chat-input:disabled{
      background:#fafafa;
      color:#999999;
      cursor:not-allowed;
    }

    .send-btn{
      width:100%;
      height:100%;
      border:none;
      border-left:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      font-size:var(--font-body);
      cursor:pointer;
    }

    .send-btn:hover:not(:disabled){
      background:var(--soft);
    }

    .send-btn:disabled{
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

    .selector-modal.show{
      display:flex;
    }

    .selector-card{
      width:var(--modal-w);
      height:var(--modal-h);
      max-height:var(--modal-h);
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

    .selector-item:hover{
      background:var(--soft);
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

    .selector-empty,
    .selector-error,
    .loading-box{
      padding:18px 12px;
      text-align:center;
      color:var(--muted);
      font-size:var(--font-body);
    }

    .selector-error{
      color:var(--danger);
    }

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

      .chat-body{
        padding:10px;
      }

      .msg{
        max-width:88%;
      }
    }

    @media (max-width: 420px){
      :root{
        --font-main:13px;
        --font-small:10px;
        --font-title:13px;
        --font-body:13px;
        --send-w:86px;
      }

      .inner{
        gap:8px;
      }
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
          <div class="chat-title" id="chatTitle">Nombre del socorrista o Grupo de instalación</div>
          <div class="chat-body" id="chatBody">
            <div class="chat-placeholder">Cargando conversaciones...</div>
          </div>
          <div class="input-row">
            <input
              id="chatInput"
              class="chat-input"
              type="text"
              autocomplete="off"
              placeholder="Dialogo para enviar Mensaje"
              disabled
            />
            <button id="sendBtn" class="send-btn" type="button" disabled>SEND</button>
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
      <div class="selector-list" id="selectorList"></div>
    </div>
  </div>

  <script>
    (function(){
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
      const currentUserId = __CURRENT_USER__;

      let threads = [];
      let currentThreadId = null;
      let lastRenderedMessageId = null;
      let pollingInterval = null;
      let threadsPollingInterval = null;
      let usersCache = [];
      let currentSelectorMode = null;

      const el = {
        btnSocorristas: document.getElementById("btnSocorristas"),
        btnInstalacion: document.getElementById("btnInstalacion"),
        btnNotificaciones: document.getElementById("btnNotificaciones"),
        chatTitle: document.getElementById("chatTitle"),
        chatBody: document.getElementById("chatBody"),
        chatInput: document.getElementById("chatInput"),
        sendBtn: document.getElementById("sendBtn"),
        selectorModal: document.getElementById("selectorModal"),
        selectorTitle: document.getElementById("selectorTitle"),
        selectorSearch: document.getElementById("selectorSearch"),
        selectorList: document.getElementById("selectorList"),
        selectorClose: document.getElementById("selectorClose")
      };

      function escapeHtml(value) {
        return String(value ?? "")
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#039;");
      }

      function safeText(value, fallback = "") {
        const text = String(value ?? "").trim();
        return text || fallback;
      }

      function safeArray(value) {
        return Array.isArray(value) ? value : [];
      }

      function isPrivateThread(thread) {
        return String(thread?.type ?? "").toLowerCase() === "private";
      }

      function getThreadTitle(thread) {
        if (!thread) return "Conversación";
        const title = safeText(thread.title);
        if (title) return title;
        return isPrivateThread(thread) ? "Chat privado" : "Grupo de instalación";
      }

      function getThreadPreview(thread) {
        return safeText(thread?.last_message);
      }

      function getPrivateThreads() {
        return threads.filter((t) => isPrivateThread(t));
      }

      function getInstallationThreads() {
        return threads.filter((t) => !isPrivateThread(t));
      }

      function setTopActive(mode) {
        el.btnSocorristas.classList.remove("active");
        el.btnInstalacion.classList.remove("active");
        el.btnNotificaciones.classList.remove("active");

        if (mode === "socorristas") el.btnSocorristas.classList.add("active");
        if (mode === "instalacion") el.btnInstalacion.classList.add("active");
        if (mode === "notificaciones") el.btnNotificaciones.classList.add("active");
      }

      function syncTopButtonsWithThread(thread) {
        if (!thread) {
          setTopActive(null);
          return;
        }
        setTopActive(isPrivateThread(thread) ? "socorristas" : "instalacion");
      }

      function renderPlaceholder(text) {
        el.chatBody.innerHTML = '<div class="chat-placeholder">' + escapeHtml(text) + '</div>';
      }

      function disableComposer(placeholderText = "Selecciona una conversación") {
        el.chatInput.disabled = true;
        el.sendBtn.disabled = true;
        el.chatInput.value = "";
        el.chatInput.placeholder = placeholderText;
      }

      function enableComposer() {
        el.chatInput.disabled = false;
        el.chatInput.placeholder = "Dialogo para enviar Mensaje";
        updateSendState();
      }

      function updateSendState() {
        const hasThread = !!currentThreadId;
        const hasText = el.chatInput.value.trim().length > 0;
        el.sendBtn.disabled = !hasThread || !hasText;
      }

      function scrollChatToBottom() {
        el.chatBody.scrollTop = el.chatBody.scrollHeight;
      }

      function isNearBottom(container) {
        return container.scrollHeight - container.scrollTop - container.clientHeight < 80;
      }

      async function fetchJSON(url, options = {}) {
        const response = await fetch(url, options);
        const raw = await response.text();
        let data = {};
        try {
          data = raw ? JSON.parse(raw) : {};
        } catch (e) {
          if (!response.ok) {
            throw new Error("Respuesta inválida del servidor");
          }
          throw new Error("No se pudo interpretar la respuesta del servidor");
        }

        if (!response.ok) {
          const msg =
            data?.error ||
            data?.message ||
            ("HTTP " + response.status + " - " + response.statusText);
          throw new Error(msg);
        }

        return data;
      }

      function findThreadById(threadId) {
        return threads.find((t) => String(t.id) === String(threadId)) || null;
      }

      async function markThreadRead(threadId) {
        if (!threadId || lastRenderedMessageId === null) return;

        try {
          await fetch(API_BASE + "/threads/" + encodeURIComponent(threadId) + "/read", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: currentUserId,
              last_read_message_id: lastRenderedMessageId
            })
          });
        } catch (error) {
          console.error("Error marking thread as read:", error);
        }
      }

      function buildMessageNode(msg) {
        const div = document.createElement("div");
        div.className = "msg" + (String(msg.sender_id) === String(currentUserId) ? " out" : "");
        div.setAttribute("data-id", String(msg.id ?? ""));

        const author = document.createElement("div");
        author.className = "msg-author";
        author.textContent = safeText(msg.sender_alias, "Usuario");

        const body = document.createElement("div");
        body.className = "msg-body";
        body.textContent = safeText(msg.body);

        div.appendChild(author);
        div.appendChild(body);
        return div;
      }

      async function loadMessages(threadId, poll = false) {
        if (!threadId) return;

        const limit = poll ? 50 : 500;
        const url =
          API_BASE +
          "/threads/" +
          encodeURIComponent(threadId) +
          "/messages?user_id=" +
          encodeURIComponent(currentUserId) +
          "&limit=" +
          limit;

        try {
          const data = await fetchJSON(url);
          let messages = safeArray(data.messages);

          if (poll && lastRenderedMessageId !== null) {
            messages = messages.filter((m) => {
              const currentId = parseInt(m.id, 10);
              return !Number.isNaN(currentId) && currentId > lastRenderedMessageId;
            });
          }

          const keepBottom = poll ? isNearBottom(el.chatBody) : true;

          if (!poll) {
            el.chatBody.innerHTML = "";
            lastRenderedMessageId = null;
          }

          if (messages.length === 0 && !poll) {
            renderPlaceholder("No hay mensajes");
            await markThreadRead(threadId);
            return;
          }

          messages.forEach((msg) => {
            const node = buildMessageNode(msg);
            el.chatBody.appendChild(node);

            const msgId = parseInt(msg.id, 10);
            if (!Number.isNaN(msgId)) {
              lastRenderedMessageId = msgId;
            }
          });

          if (keepBottom || !poll) {
            scrollChatToBottom();
          }

          await markThreadRead(threadId);
        } catch (error) {
          console.error("Error loading messages:", error);
          if (!poll) {
            el.chatBody.innerHTML =
              '<div class="selector-error">Error al cargar mensajes<br>' +
              escapeHtml(error.message) +
              "</div>";
          }
        }
      }

      async function setActiveThread(threadId, keepModalOpen = false) {
        currentThreadId = String(threadId);
        const thread = findThreadById(threadId);

        el.chatTitle.textContent = thread ? getThreadTitle(thread) : "Conversación";
        enableComposer();
        syncTopButtonsWithThread(thread);

        await loadMessages(threadId, false);

        if (pollingInterval) {
          clearInterval(pollingInterval);
        }

        pollingInterval = setInterval(async function() {
          if (currentThreadId) {
            await loadMessages(currentThreadId, true);
          }
        }, 8000);

        if (!keepModalOpen) {
          closeSelector();
        }

        updateSendState();
      }

      async function loadThreads() {
        try {
          const data = await fetchJSON(
            API_BASE + "/threads?user_id=" + encodeURIComponent(currentUserId)
          );

          threads = safeArray(data.threads);

          if (threads.length === 0) {
            currentThreadId = null;
            lastRenderedMessageId = null;
            el.chatTitle.textContent = "Nombre del socorrista o Grupo de instalación";
            renderPlaceholder("No hay conversaciones");
            disableComposer("Selecciona una conversación");
            syncTopButtonsWithThread(null);

            if (currentSelectorMode) {
              renderSelector();
            }
            return;
          }

          const stillExists = threads.some((t) => String(t.id) === String(currentThreadId));

          if (!stillExists) {
            await setActiveThread(threads[0].id, true);
          } else {
            const current = findThreadById(currentThreadId);
            el.chatTitle.textContent = current ? getThreadTitle(current) : "Conversación";
            syncTopButtonsWithThread(current);
          }

          if (currentSelectorMode) {
            renderSelector();
          }
        } catch (error) {
          console.error("Error loading threads:", error);
          currentThreadId = null;
          lastRenderedMessageId = null;
          el.chatTitle.textContent = "Nombre del socorrista o Grupo de instalación";
          el.chatBody.innerHTML =
            '<div class="selector-error">Error al cargar conversaciones<br>' +
            escapeHtml(error.message) +
            "</div>";
          disableComposer("Error al cargar");
          syncTopButtonsWithThread(null);
        }
      }

      async function fetchUsersOnce() {
        if (usersCache.length > 0) return usersCache;

        try {
          const data = await fetchJSON(API_BASE + "/users");
          usersCache = Array.isArray(data) ? data : safeArray(data.users);
          return usersCache;
        } catch (error) {
          console.error("Error loading users:", error);
          throw error;
        }
      }

      function filterThreadsByQuery(list, query) {
        const q = query.trim().toLowerCase();
        if (!q) return list;

        return list.filter((t) => {
          const title = getThreadTitle(t).toLowerCase();
          const preview = getThreadPreview(t).toLowerCase();
          return title.includes(q) || preview.includes(q);
        });
      }

      function buildThreadItems(list, emptyText) {
        if (!list.length) {
          return '<div class="selector-empty">' + escapeHtml(emptyText) + "</div>";
        }

        return list
          .map((thread) => {
            return (
              '<button class="selector-item thread-select-item" type="button" data-thread-id="' +
              escapeHtml(thread.id) +
              '">' +
                '<div class="selector-item-title">' + escapeHtml(getThreadTitle(thread)) + "</div>" +
                '<div class="selector-item-sub">' + escapeHtml(getThreadPreview(thread) || "Sin mensajes") + "</div>" +
              "</button>"
            );
          })
          .join("");
      }

      function buildUserItems(list, emptyText) {
        if (!list.length) {
          return '<div class="selector-empty">' + escapeHtml(emptyText) + "</div>";
        }

        return list
          .map((user) => {
            const alias = safeText(user.alias, "Usuario");
            const dni = safeText(user.dni);
            return (
              '<button class="selector-item user-select-item" type="button" data-dni="' +
              escapeHtml(dni) +
              '">' +
                '<div class="selector-item-title">@' + escapeHtml(alias) + "</div>" +
                '<div class="selector-item-sub">' + escapeHtml(dni) + "</div>" +
              "</button>"
            );
          })
          .join("");
      }

      function bindSelectorThreadEvents() {
        el.selectorList.querySelectorAll(".thread-select-item").forEach((btn) => {
          btn.addEventListener("click", async function() {
            const threadId = btn.getAttribute("data-thread-id");
            if (!threadId) return;
            await setActiveThread(threadId);
          });
        });
      }

      function bindSelectorUserEvents() {
        el.selectorList.querySelectorAll(".user-select-item").forEach((btn) => {
          btn.addEventListener("click", async function() {
            const otherDni = btn.getAttribute("data-dni");
            if (!otherDni) return;

            if (String(otherDni) === String(currentUserId)) {
              alert("No puedes chatear contigo mismo");
              return;
            }

            try {
              const data = await fetchJSON(
                API_BASE +
                "/private/" +
                encodeURIComponent(otherDni) +
                "?user_id=" +
                encodeURIComponent(currentUserId)
              );

              if (data.thread_id) {
                await loadThreads();
                await setActiveThread(data.thread_id);
              }
            } catch (error) {
              alert("Error al crear el chat: " + error.message);
            }
          });
        });
      }

      function openSelector(mode) {
        currentSelectorMode = mode;
        el.selectorModal.classList.add("show");
        renderSelector();
        setTimeout(() => el.selectorSearch.focus(), 30);
      }

      function closeSelector() {
        el.selectorModal.classList.remove("show");
        el.selectorSearch.value = "";
        currentSelectorMode = null;

        const current = findThreadById(currentThreadId);
        syncTopButtonsWithThread(current);
      }

      async function renderSelector() {
        const mode = currentSelectorMode;
        if (!mode) return;

        const query = el.selectorSearch.value.trim();

        if (mode === "socorristas") {
          setTopActive("socorristas");
          el.selectorTitle.textContent = "Socorristas";
          el.selectorSearch.placeholder = "Buscar por alias o DNI";
          el.selectorList.innerHTML = '<div class="loading-box">Cargando...</div>';

          try {
            await fetchUsersOnce();

            const privateThreads = filterThreadsByQuery(getPrivateThreads(), query);

            const q = query.toLowerCase();
            const users = usersCache.filter((u) => {
              const alias = safeText(u.alias).toLowerCase();
              const dni = safeText(u.dni);
              if (!dni || String(dni) === String(currentUserId)) return false;
              if (!q) return true;
              return alias.includes(q) || dni.includes(q);
            });

            let html = "";

            html += '<div class="section-label">Chats existentes</div>';
            html += buildThreadItems(privateThreads, "No hay chats privados");

            html += '<div class="section-label">Abrir o crear chat</div>';
            html += buildUserItems(users, "No se encontraron socorristas");

            el.selectorList.innerHTML = html;
            bindSelectorThreadEvents();
            bindSelectorUserEvents();
          } catch (error) {
            el.selectorList.innerHTML =
              '<div class="selector-error">Error al cargar socorristas<br>' +
              escapeHtml(error.message) +
              "</div>";
          }

          return;
        }

        if (mode === "instalacion") {
          setTopActive("instalacion");
          el.selectorTitle.textContent = "Instalación";
          el.selectorSearch.placeholder = "Buscar grupo o instalación";

          const groups = filterThreadsByQuery(getInstallationThreads(), query);

          let html = "";
          html += '<div class="section-label">Grupos de instalación</div>';
          html += buildThreadItems(groups, "No hay grupos de instalación");

          el.selectorList.innerHTML = html;
          bindSelectorThreadEvents();
          return;
        }

        if (mode === "notificaciones") {
          setTopActive("notificaciones");
          el.selectorTitle.textContent = "Notificaciones";
          el.selectorSearch.placeholder = "Buscar conversación";

          const allThreads = filterThreadsByQuery(threads, query);

          let html = "";
          html += '<div class="section-label">Conversaciones</div>';
          html += buildThreadItems(allThreads, "No hay conversaciones");

          el.selectorList.innerHTML = html;
          bindSelectorThreadEvents();
        }
      }

      async function sendMessage() {
        if (!currentThreadId) return;

        const text = el.chatInput.value.trim();
        if (!text) return;

        el.chatInput.value = "";
        updateSendState();

        try {
          await fetchJSON(
            API_BASE + "/threads/" + encodeURIComponent(currentThreadId) + "/messages",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                sender_id: currentUserId,
                body: text
              })
            }
          );

          await loadMessages(currentThreadId, false);
          await loadThreads();
          el.chatInput.focus();
        } catch (error) {
          console.error("Error sending message:", error);
          alert("Error al enviar mensaje: " + error.message);
        }
      }

      el.btnSocorristas.addEventListener("click", function() {
        openSelector("socorristas");
      });

      el.btnInstalacion.addEventListener("click", function() {
        openSelector("instalacion");
      });

      el.btnNotificaciones.addEventListener("click", async function() {
        await loadThreads();
        openSelector("notificaciones");
      });

      el.selectorClose.addEventListener("click", closeSelector);

      el.selectorModal.addEventListener("click", function(e) {
        if (e.target === el.selectorModal) {
          closeSelector();
        }
      });

      el.selectorSearch.addEventListener("input", function() {
        renderSelector();
      });

      el.chatInput.addEventListener("input", updateSendState);

      el.chatInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      });

      el.sendBtn.addEventListener("click", sendMessage);

      window.addEventListener("beforeunload", function() {
        if (pollingInterval) clearInterval(pollingInterval);
        if (threadsPollingInterval) clearInterval(threadsPollingInterval);
      });

      disableComposer("Selecciona una conversación");
      renderPlaceholder("Cargando conversaciones...");

      loadThreads();

      threadsPollingInterval = setInterval(async function() {
        await loadThreads();
      }, 15000);
    })();
  </script>
</body>
</html>
""".replace("__CURRENT_USER__", json.dumps(USER_DNI))

components.html(html, height=10, scrolling=False)
