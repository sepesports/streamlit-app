# app.py
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
      iframe{
        border:0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Autenticación: redirige si no hay auth=ok
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

    .chat-shell{{
      flex:1;
      min-height:0;
      display:flex;
      flex-direction:column;
      border:var(--border-size) solid var(--border);
      background:#fff;
    }}

    .chat-header{{
      height:var(--title-row-h);
      min-height:var(--title-row-h);
      border-bottom:var(--border-size) solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:0 var(--pad-x);
      font-size:var(--font-title);
      font-weight:400;
    }}

    .chat-title{{
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }}

    .thread-select{{
      border:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      font-size:var(--font-small);
      padding:4px 8px;
      max-width:200px;
    }}

    .chat-body{{
      flex:1;
      min-height:160px;
      overflow:auto;
      background:#fff;
      padding:14px;
      display:flex;
      flex-direction:column;
      gap:10px;
    }}

    .msg{{
      max-width:min(78%, 560px);
      border:var(--border-size) solid var(--border);
      padding:10px 12px;
      font-size:var(--font-input);
      line-height:1.3;
      background:#fff;
      word-break:break-word;
    }}

    .msg.out{{
      margin-left:auto;
    }}

    .input-row{{
      height:var(--input-row-h);
      min-height:var(--input-row-h);
      border-top:var(--border-size) solid var(--border);
      display:grid;
      grid-template-columns: 1fr var(--send-w);
      gap:0;
      background:#fff;
    }}

    .chat-input{{
      width:100%;
      height:100%;
      border:none;
      outline:none;
      padding:0 var(--pad-x);
      font-size:var(--font-input);
      color:var(--text);
      background:#fff;
    }}

    .chat-input::placeholder{{
      color:#111111;
      opacity:1;
    }}

    .send-btn{{
      height:100%;
      width:100%;
      border:none;
      border-left:var(--border-size) solid var(--border);
      background:#fff;
      color:var(--text);
      font-size:var(--font-send);
      font-weight:400;
      cursor:pointer;
    }}

    .send-btn:active,
    .top-btn:active{{
      background:#ececec;
    }}

    /* Panel de notificaciones */
    .notifications-panel{{
      height:100%;
      overflow:auto;
      padding:14px;
    }}

    .notification-item{{
      border-bottom:1px solid var(--border);
      padding:8px 0;
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

      .chat-body{{
        padding:10px;
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

      <div class="chat-shell">
        <div class="chat-header">
          <span class="chat-title" id="chatTitle">Selecciona una conversación</span>
          <select id="threadSelect" class="thread-select" style="display:none;"></select>
        </div>

        <div class="chat-body" id="chatBody">
          <div class="chat-empty"></div>
        </div>

        <div class="input-row">
          <input id="chatInput" class="chat-input" type="text" placeholder="Diálogo para enviar Mensaje" autocomplete="off" disabled />
          <button id="sendBtn" class="send-btn" type="button" disabled>SEND</button>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
  const API_BASE = "https://camilo27.pythonanywhere.com/api/chat";
  const currentUserId = "{USER_DNI}";
  let currentThreadId = null;
  let threads = [];           // Lista completa de hilos del usuario
  let lastRenderedMessageId = null;
  let pollingInterval = null;
  let threadsPollingInterval = null;
  let currentMode = "socorristas";  // "socorristas", "instalacion", "notificaciones"

  function escapeHtml(text) {{
    return String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
  }}

  async function fetchJSON(url, options = {{}}) {{
    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`HTTP ${{response.status}} - ${{response.statusText}}`);
    return response.json();
  }}

  // Cargar todos los hilos del usuario desde el backend
  async function loadThreads() {{
    try {{
      const data = await fetchJSON(API_BASE + "/threads?user_id=" + encodeURIComponent(currentUserId));
      threads = data.threads || [];
      updateUIForMode();  // Actualizar desplegable según modo actual
    }} catch (error) {{
      console.error("Error loading threads:", error);
    }}
  }}

  // Actualizar la interfaz según el modo (socorristas / instalación / notificaciones)
  function updateUIForMode() {{
    const selectEl = document.getElementById("threadSelect");
    const chatTitle = document.getElementById("chatTitle");
    const chatBody = document.getElementById("chatBody");
    const inputRow = document.querySelector(".input-row");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");

    if (currentMode === "notificaciones") {{
      // Mostrar panel de notificaciones (mensajes no leídos en otros hilos)
      selectEl.style.display = "none";
      chatTitle.textContent = "Notificaciones";
      chatBody.innerHTML = '<div class="notifications-panel" id="notifPanel">Cargando...</div>';
      inputRow.style.display = "none";
      // Detener polling de mensajes si estaba activo
      if (pollingInterval) clearInterval(pollingInterval);
      // Cargar notificaciones
      loadNotifications();
      return;
    }}

    // Modos con chat: mostrar input y desplegable
    inputRow.style.display = "grid";
    selectEl.style.display = "block";

    // Filtrar hilos según modo
    let filteredThreads = [];
    if (currentMode === "socorristas") {{
      filteredThreads = threads.filter(t => t.type === "private");
    }} else if (currentMode === "instalacion") {{
      filteredThreads = threads.filter(t => t.type === "group");
    }}

    // Construir opciones del desplegable
    if (filteredThreads.length === 0) {{
      selectEl.innerHTML = '<option value="">No hay conversaciones</option>';
      chatTitle.textContent = "Sin conversaciones";
      // Limpiar área de mensajes y deshabilitar input
      chatBody.innerHTML = '<div class="chat-empty"></div>';
      chatInput.disabled = true;
      sendBtn.disabled = true;
      currentThreadId = null;
      return;
    }}

    chatInput.disabled = false;
    sendBtn.disabled = false;
    selectEl.innerHTML = filteredThreads.map(t => `<option value="${{t.id}}">${{escapeHtml(t.title || (t.type === 'private' ? 'Privado' : 'Grupo'))}}</option>`).join('');
    
    // Si ya había un hilo seleccionado y aún existe en la lista, mantenerlo; si no, seleccionar el primero
    let selectedId = currentThreadId;
    if (selectedId && filteredThreads.some(t => t.id == selectedId)) {{
      selectEl.value = selectedId;
    }} else {{
      if (filteredThreads.length > 0) {{
        selectedId = filteredThreads[0].id;
        selectEl.value = selectedId;
      }} else {{
        selectedId = null;
      }}
    }}

    if (selectedId) {{
      setActiveThread(selectedId);
    }} else {{
      // Sin hilos: limpiar chat
      chatBody.innerHTML = '<div class="chat-empty"></div>';
      chatTitle.textContent = "Selecciona una conversación";
      currentThreadId = null;
      if (pollingInterval) clearInterval(pollingInterval);
    }}
  }}

  async function loadNotifications() {{
    try {{
      // Obtener todos los threads y sus estados de lectura
      const data = await fetchJSON(API_BASE + "/threads?user_id=" + encodeURIComponent(currentUserId));
      const threads = data.threads || [];
      const panel = document.getElementById("notifPanel");
      if (!panel) return;
      const unread = threads.filter(t => t.unread_count > 0);
      if (unread.length === 0) {{
        panel.innerHTML = '<div>No hay notificaciones pendientes</div>';
      }} else {{
        panel.innerHTML = unread.map(t => `
          <div class="notification-item" data-thread="${{t.id}}">
            <strong>${{escapeHtml(t.title || (t.type === 'private' ? 'Privado' : 'Grupo'))}}</strong><br>
            <span>Mensajes no leídos: ${{t.unread_count}}</span>
          </div>
        `).join('');
        // Al hacer clic en una notificación, cambiar al modo correspondiente y abrir ese hilo
        document.querySelectorAll('.notification-item').forEach(el => {{
          el.addEventListener('click', () => {{
            const threadId = el.getAttribute('data-thread');
            const thread = threads.find(t => t.id == threadId);
            if (thread) {{
              if (thread.type === "private") {{
                document.getElementById("btnSocorristas").click();
              }} else {{
                document.getElementById("btnInstalacion").click();
              }}
              setTimeout(() => {{
                const selectEl = document.getElementById("threadSelect");
                if (selectEl) {{
                  selectEl.value = threadId;
                  setActiveThread(threadId);
                }}
              }}, 100);
            }}
          }});
        }});
      }}
    }} catch (error) {{
      console.error("Error loading notifications:", error);
      const panel = document.getElementById("notifPanel");
      if (panel) panel.innerHTML = '<div>Error al cargar notificaciones</div>';
    }}
  }}

  async function loadMessages(threadId, poll = false) {{
    const limit = poll ? 30 : 500;
    const url = API_BASE + "/threads/" + threadId + "/messages?user_id=" + encodeURIComponent(currentUserId) + "&limit=" + limit;
    try {{
      const data = await fetchJSON(url);
      let messages = data.messages || [];
      if (poll && lastRenderedMessageId !== null) {{
        messages = messages.filter(m => parseInt(m.id) > lastRenderedMessageId);
      }}
      const container = document.getElementById("chatBody");
      if (!poll) {{
        container.innerHTML = '';
        lastRenderedMessageId = null;
      }}
      if (messages.length === 0 && !poll) {{
        container.innerHTML = '<div class="chat-empty"></div>';
        lastRenderedMessageId = null;
        return;
      }}
      messages.forEach(msg => {{
        const div = document.createElement("div");
        div.className = "msg" + (msg.sender_id == currentUserId ? " out" : "");
        div.innerHTML = '<strong>' + escapeHtml(msg.sender_alias || 'Usuario') + ':</strong> ' + escapeHtml(msg.body);
        container.appendChild(div);
        lastRenderedMessageId = parseInt(msg.id);
      }});
      container.scrollTop = container.scrollHeight;
      await markThreadRead(threadId);
    }} catch (error) {{
      console.error("Error loading messages:", error);
      if (!poll) {{
        const container = document.getElementById("chatBody");
        container.innerHTML = '<div class="error">Error al cargar mensajes</div>';
      }}
    }}
  }}

  async function markThreadRead(threadId) {{
    if (!lastRenderedMessageId) return;
    try {{
      await fetch(API_BASE + "/threads/" + threadId + "/read", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ user_id: currentUserId, last_read_message_id: lastRenderedMessageId }})
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
    const thread = threads.find(t => t.id == threadId);
    const title = thread ? thread.title : (thread.type === "private" ? "Chat privado" : "Grupo");
    document.getElementById("chatTitle").textContent = title;
    // Reiniciar polling para este hilo
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(() => {{
      if (currentThreadId && currentMode !== "notificaciones") loadMessages(currentThreadId, true);
    }}, 10000);
  }}

  // Eventos de los botones superiores
  document.getElementById("btnSocorristas").addEventListener("click", () => {{
    document.getElementById("btnSocorristas").classList.add("active");
    document.getElementById("btnInstalacion").classList.remove("active");
    document.getElementById("btnNotificaciones").classList.remove("active");
    currentMode = "socorristas";
    updateUIForMode();
  }});

  document.getElementById("btnInstalacion").addEventListener("click", () => {{
    document.getElementById("btnInstalacion").classList.add("active");
    document.getElementById("btnSocorristas").classList.remove("active");
    document.getElementById("btnNotificaciones").classList.remove("active");
    currentMode = "instalacion";
    updateUIForMode();
  }});

  document.getElementById("btnNotificaciones").addEventListener("click", () => {{
    document.getElementById("btnNotificaciones").classList.add("active");
    document.getElementById("btnSocorristas").classList.remove("active");
    document.getElementById("btnInstalacion").classList.remove("active");
    currentMode = "notificaciones";
    updateUIForMode();
  }});

  // Evento cambio de selección en desplegable
  document.getElementById("threadSelect").addEventListener("change", (e) => {{
    const newId = e.target.value;
    if (newId) setActiveThread(newId);
  }});

  // Eventos de envío
  document.getElementById("sendBtn").addEventListener("click", sendMessage);
  document.getElementById("chatInput").addEventListener("keypress", (e) => {{
    if (e.key === "Enter") sendMessage();
  }});

  // Inicialización
  loadThreads();
  threadsPollingInterval = setInterval(loadThreads, 15000);
</script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
