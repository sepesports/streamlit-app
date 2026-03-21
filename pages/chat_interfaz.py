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

html = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
  <title>Plano 2 Chat</title>
  <style>
    /* --- Estilos de plano (marco exterior) --- */
    :root{{
      --bg: #ffffff;
      --border: #111111;
      --text: #111111;

      --frame-margin: clamp(6px, 1.4vw, 16px);
      --border-size: 2px;
      --radius: 0px;

      --top-row-h: clamp(58px, 8vh, 72px);
      --title-row-h: clamp(42px, 6vh, 52px);
      --input-row-h: clamp(52px, 7vh, 62px);

      --gap-top: clamp(8px, 1vw, 14px);
      --gap-main: 0px;

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
    }}

    *{{
      box-sizing:border-box;
      -webkit-tap-highlight-color: transparent;
    }}

    html, body{{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--bg);
      font-family: Arial, Helvetica, sans-serif;
      color:var(--text);
    }}

    #app{{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      background:var(--bg);
      padding:var(--frame-margin);
    }}

    .frame{{
      width:100%;
      height:100%;
      border:var(--border-size) solid var(--border);
      display:flex;
      flex-direction:column;
      background:#fff;
      overflow:hidden;
    }}

    .inner{{
      display:flex;
      flex-direction:column;
      width:100%;
      height:100%;
      padding:clamp(18px, 2.4vw, 28px);
      gap:var(--gap-top);
    }}

    .top-buttons{{
      display:grid;
      grid-template-columns: var(--btn1) var(--btn2) var(--btn3);
      gap:0;
      width:100%;
      min-height:var(--top-row-h);
    }}

    .top-btn{{
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
    }}

    .top-btn + .top-btn{{
      border-left:none;
    }}

    .top-btn.active{{
      background:#f5f5f5;
    }}

    .btn-stack{{
      display:flex;
      flex-direction:column;
      align-items:flex-start;
      justify-content:center;
      gap:4px;
    }}

    .btn-topline{{
      font-size:var(--font-small);
      font-weight:400;
      line-height:1;
    }}

    .btn-mainline{{
      font-size:var(--font-main);
      font-weight:400;
      line-height:1.1;
    }}

    .btn-center{{
      width:100%;
      height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      font-size:var(--font-main);
      line-height:1.1;
    }}

    /* Contenedor para el chat de codigo_interfaz: ocupa todo el espacio restante */
    #chatApp {{
      flex: 1;
      min-height: 0;
      display: flex;
      width: 100%;
    }}

    @media (max-width: 768px){{
      :root{{
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
      }}

      .inner{{
        padding:10px;
      }}

      .btn-stack{{
        gap:2px;
      }}

      .btn-mainline{{
        word-break:break-word;
      }}
    }}

    @media (max-width: 420px){{
      :root{{
        --font-main: 13px;
        --font-small: 10px;
        --font-title: 13px;
        --font-input: 13px;
        --font-send: 13px;
        --send-w: 88px;
      }}

      .inner{{
        padding:8px;
      }}
    }}
  </style>

  <style>
    /* --- Estilos de codigo_interfaz (con #app renombrado a #chatApp) --- */
    :root{{
      --chat-bg: #020a1a;
      --chat-text: #eaf2ff;
      --chat-border: #2a3a5a;
      --chat-accent: #ff9a52;
      --chat-msg-bg: #0f1a2a;
      --chat-msg-out: #2a3a5a;
    }}
    #chatApp {{
      display: flex;
      height: 100%;
      width: 100%;
      background: var(--chat-bg);
      color: var(--chat-text);
      font-family: 'Segoe UI', Arial, sans-serif;
    }}
    .threads-panel {{
      width: 280px;
      border-right: 1px solid var(--chat-border);
      display: flex;
      flex-direction: column;
      background: rgba(0,0,0,0.3);
    }}
    .threads-header {{
      padding: 12px;
      border-bottom: 1px solid var(--chat-border);
      font-weight: bold;
      display: flex;
      justify-content: space-between;
    }}
    .new-chat-btn {{
      background: var(--chat-accent);
      border: none;
      color: #000;
      padding: 4px 10px;
      border-radius: 20px;
      cursor: pointer;
      font-size: 12px;
    }}
    .thread-list {{
      flex: 1;
      overflow-y: auto;
    }}
    .thread-item {{
      padding: 12px;
      border-bottom: 1px solid var(--chat-border);
      cursor: pointer;
      transition: background 0.2s;
    }}
    .thread-item:hover {{
      background: rgba(255,255,255,0.1);
    }}
    .thread-item.active {{
      background: rgba(255,255,255,0.2);
      border-left: 3px solid var(--chat-accent);
    }}
    .thread-title {{
      font-weight: bold;
      margin-bottom: 4px;
    }}
    .thread-preview {{
      font-size: 12px;
      color: #aaa;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .chat-panel {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .chat-header {{
      padding: 12px;
      border-bottom: 1px solid var(--chat-border);
      font-weight: bold;
    }}
    .messages-area {{
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .message {{
      max-width: 70%;
      padding: 8px 12px;
      border-radius: 12px;
      background: var(--chat-msg-bg);
      align-self: flex-start;
    }}
    .message.out {{
      background: var(--chat-msg-out);
      align-self: flex-end;
    }}
    .message strong {{
      color: var(--chat-accent);
    }}
    .input-area {{
      display: flex;
      padding: 12px;
      border-top: 1px solid var(--chat-border);
      gap: 8px;
    }}
    #chatInput {{
      flex: 1;
      padding: 10px;
      border: 1px solid var(--chat-border);
      border-radius: 20px;
      background: var(--chat-msg-bg);
      color: var(--chat-text);
      outline: none;
    }}
    #sendBtn {{
      background: var(--chat-accent);
      border: none;
      padding: 0 20px;
      border-radius: 20px;
      cursor: pointer;
      font-weight: bold;
      color: #000;
    }}
    .user-search-modal {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }}
    .modal-content {{
      background: var(--chat-bg);
      border: 1px solid var(--chat-border);
      border-radius: 12px;
      width: 300px;
      max-width: 90%;
      padding: 20px;
    }}
    .modal-content input {{
      width: 100%;
      padding: 8px;
      margin-bottom: 12px;
      border: 1px solid var(--chat-border);
      background: var(--chat-msg-bg);
      color: var(--chat-text);
    }}
    .user-list {{
      max-height: 200px;
      overflow-y: auto;
    }}
    .user-item {{
      padding: 6px;
      cursor: pointer;
    }}
    .user-item:hover {{
      background: rgba(255,255,255,0.1);
    }}
    .close-modal {{
      float: right;
      cursor: pointer;
    }}
    .loading, .error {{
      text-align: center;
      padding: 20px;
      color: var(--chat-text);
    }}
    .error {{
      color: #ff6666;
    }}
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

        <!-- Aquí va el chat de codigo_interfaz (renombrado #app → #chatApp) -->
        <div id="chatApp">
          <div class="threads-panel">
            <div class="threads-header">
              <span>Conversaciones</span>
              <button class="new-chat-btn" id="newChatBtn">+ Nuevo</button>
            </div>
            <div class="thread-list" id="threadList">
              <div class="loading">Cargando conversaciones...</div>
            </div>
          </div>
          <div class="chat-panel">
            <div class="chat-header" id="chatHeader">Selecciona una conversación</div>
            <div class="messages-area" id="messagesArea">
              <div style="text-align: center; margin-top: 20px;">No hay mensajes</div>
            </div>
            <div class="input-area" style="display: none;" id="inputArea">
              <input type="text" id="chatInput" placeholder="Escribe un mensaje..." autocomplete="off">
              <button id="sendBtn">Enviar</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <script>
    // --- Script de los botones superiores (solo activar clase y cambiar título, sin interferir con el chat) ---
    (function () {{
      const btnSocorristas = document.getElementById("btnSocorristas");
      const btnInstalacion = document.getElementById("btnInstalacion");
      const btnNotificaciones = document.getElementById("btnNotificaciones");
      const chatTitle = document.getElementById("chatTitle");
      // Nota: chatTitle no existe en la nueva estructura, así que evitamos error.
      function setActive(button) {{
        [btnSocorristas, btnInstalacion, btnNotificaciones].forEach(btn => {{
          if (btn) btn.classList.remove("active");
        }});
        if (button) button.classList.add("active");
      }}

      if (btnSocorristas) btnSocorristas.addEventListener("click", function () {{ setActive(btnSocorristas); }});
      if (btnInstalacion) btnInstalacion.addEventListener("click", function () {{ setActive(btnInstalacion); }});
      if (btnNotificaciones) btnNotificaciones.addEventListener("click", function () {{ setActive(btnNotificaciones); }});
    }})();

    // --- Script de codigo_interfaz (íntegro, solo se renombró #app → #chatApp) ---
    const API_BASE = "https://camilo27.pythonanywhere.com/api/chat";
    const currentUserId = "{USER_DNI}";
    let currentThreadId = null;
    let threads = [];
    let pollingInterval = null;
    let threadsPollingInterval = null;
    let lastRenderedMessageId = null;

    function escapeHtml(text) {{
      return String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
    }}

    async function fetchJSON(url, options = {{}}) {{
      const response = await fetch(url, options);
      if (!response.ok) {{
        throw new Error(`HTTP ${{response.status}} - ${{response.statusText}}`);
      }}
      return response.json();
    }}

    async function loadThreads() {{
      const listDiv = document.getElementById("threadList");
      try {{
        const data = await fetchJSON(API_BASE + "/threads?user_id=" + encodeURIComponent(currentUserId));
        threads = data.threads || [];
        renderThreadList();
        if (threads.length > 0 && !currentThreadId) {{
          setActiveThread(threads[0].id);
        }}
      }} catch (error) {{
        console.error("Error loading threads:", error);
        listDiv.innerHTML = '<div class="error">Error al cargar conversaciones.<br>' + escapeHtml(error.message) + '</div>';
      }}
    }}

    function renderThreadList() {{
      const container = document.getElementById("threadList");
      if (threads.length === 0) {{
        container.innerHTML = '<div style="padding: 12px; text-align: center;">No hay conversaciones</div>';
        return;
      }}
      container.innerHTML = threads.map(function(t) {{
        return '<div class="thread-item' + (currentThreadId == t.id ? ' active' : '') + '" data-id="' + t.id + '">' +
                 '<div class="thread-title">' + escapeHtml(t.title || (t.type === 'private' ? 'Privado' : 'Grupo')) + '</div>' +
                 '<div class="thread-preview">' + escapeHtml(t.last_message || '') + '</div>' +
               '</div>';
      }}).join('');
      document.querySelectorAll('.thread-item').forEach(function(el) {{
        el.addEventListener('click', function() {{ setActiveThread(el.getAttribute('data-id')); }});
      }});
    }}

    async function loadMessages(threadId, poll = false) {{
      const limit = poll ? 30 : 500;
      let url = API_BASE + "/threads/" + threadId + "/messages?user_id=" + encodeURIComponent(currentUserId) + "&limit=" + limit;
      try {{
        const data = await fetchJSON(url);
        let messages = data.messages || [];
        if (poll && lastRenderedMessageId !== null) {{
          messages = messages.filter(function(m) {{ return parseInt(m.id) > lastRenderedMessageId; }});
        }}
        const container = document.getElementById("messagesArea");
        if (!poll) {{
          container.innerHTML = '';
          lastRenderedMessageId = null;
        }}
        if (messages.length === 0 && !poll) {{
          container.innerHTML = '<div style="text-align: center; margin-top: 20px;">No hay mensajes</div>';
          lastRenderedMessageId = null;
          return;
        }}
        messages.forEach(function(msg) {{
          const div = document.createElement("div");
          div.className = "message" + (msg.sender_id == currentUserId ? " out" : "");
          div.innerHTML = '<strong>' + escapeHtml(msg.sender_alias || 'Usuario') + ':</strong> ' + escapeHtml(msg.body);
          container.appendChild(div);
          lastRenderedMessageId = parseInt(msg.id);
        }});
        container.scrollTop = container.scrollHeight;
        await markThreadRead(threadId);
      }} catch (error) {{
        console.error("Error loading messages:", error);
        const container = document.getElementById("messagesArea");
        if (!poll) container.innerHTML = '<div class="error">Error al cargar mensajes<br>' + escapeHtml(error.message) + '</div>';
      }}
    }}

    async function markThreadRead(threadId) {{
      const messagesDiv = document.getElementById("messagesArea");
      const lastMsg = messagesDiv.querySelector(".message:last-child");
      if (!lastMsg) return;
      const lastId = lastMsg.getAttribute("data-id");
      if (!lastId) return;
      try {{
        await fetch(API_BASE + "/threads/" + threadId + "/read", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ user_id: currentUserId, last_read_message_id: lastId }})
        }});
      }} catch (error) {{
        console.error("Error marking read:", error);
      }}
    }}

    async function sendMessage() {{
      if (!currentThreadId) return;
      const input = document.getElementById("chatInput");
      const text = input.value.trim();
      if (!text) return;
      input.value = "";
      try {{
        await fetch(API_BASE + "/threads/" + currentThreadId + "/messages", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ sender_id: currentUserId, body: text }})
        }});
        await loadMessages(currentThreadId, false);
      }} catch (error) {{
        console.error("Error sending message:", error);
        alert("Error al enviar mensaje: " + error.message);
      }}
    }}

    function setActiveThread(threadId) {{
      currentThreadId = threadId;
      loadMessages(threadId, false);
      const thread = threads.find(function(t) {{ return t.id == threadId; }});
      document.getElementById("chatHeader").innerText = thread ? thread.title : "Conversación";
      document.getElementById("inputArea").style.display = "flex";
      renderThreadList();
      if (pollingInterval) clearInterval(pollingInterval);
      pollingInterval = setInterval(function() {{
        if (currentThreadId) loadMessages(currentThreadId, true);
      }}, 10000);
    }}

    function showNewChatModal() {{
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
      closeBtn.onclick = function() {{ modal.remove(); }};
      const searchInput = modal.querySelector("#userSearch");
      const resultsDiv = modal.querySelector("#userSearchResults");

      async function searchUsers() {{
        const query = searchInput.value.trim().toLowerCase();
        if (query.length < 2) {{
          resultsDiv.innerHTML = '<div>Escribe al menos 2 caracteres</div>';
          return;
        }}
        try {{
          const users = await fetchJSON(API_BASE + "/users");
          const filtered = users.filter(function(u) {{ return u.alias.toLowerCase().includes(query) || u.dni.includes(query); }});
          if (filtered.length === 0) {{
            resultsDiv.innerHTML = '<div>No se encontraron usuarios</div>';
            return;
          }}
          resultsDiv.innerHTML = filtered.map(function(u) {{
            return '<div class="user-item" data-dni="' + u.dni + '">@' + escapeHtml(u.alias) + ' (' + u.dni + ')</div>';
          }}).join('');
          resultsDiv.querySelectorAll(".user-item").forEach(function(el) {{
            el.addEventListener("click", async function() {{
              const otherDni = el.getAttribute("data-dni");
              if (otherDni == currentUserId) {{
                alert("No puedes chatear contigo mismo");
                return;
              }}
              try {{
                const data = await fetchJSON(API_BASE + "/private/" + encodeURIComponent(otherDni) + "?user_id=" + encodeURIComponent(currentUserId));
                if (data.thread_id) {{
                  setActiveThread(data.thread_id);
                  modal.remove();
                  await loadThreads();
                }}
              }} catch (error) {{
                alert("Error al crear el chat: " + error.message);
              }}
            }});
          }});
        }} catch (error) {{
          resultsDiv.innerHTML = '<div class="error">Error al cargar usuarios<br>' + escapeHtml(error.message) + '</div>';
        }}
      }}
      searchInput.addEventListener("input", searchUsers);
      searchUsers();
    }}

    document.getElementById("newChatBtn").addEventListener("click", showNewChatModal);
    document.getElementById("sendBtn").addEventListener("click", sendMessage);
    document.getElementById("chatInput").addEventListener("keypress", function(e) {{
      if (e.key === "Enter") sendMessage();
    }});

    loadThreads();
    threadsPollingInterval = setInterval(loadThreads, 15000);
  </script>
</body>
</html>
"""

components.html(html, height=800, scrolling=False)
