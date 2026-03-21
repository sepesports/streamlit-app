# pages/chat_interfaz.py
import streamlit as st
import streamlit.components.v1 as components
import json

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

escaped_dni = json.dumps(USER_DNI)

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

    .top-btn, .top-select{{
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
      width:100%;
      font-family: inherit;
    }}

    .top-select{{
      background-color: #fff;
      background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>');
      background-repeat: no-repeat;
      background-position: right var(--pad-x) center;
      background-size: 1.2em;
    }}

    .top-select select{{
      opacity: 0;
      position: absolute;
      width: 100%;
      height: 100%;
      left: 0;
      top: 0;
      cursor: pointer;
    }}

    .btn-stack{{
      display:flex;
      flex-direction:column;
      align-items:flex-start;
      justify-content:center;
      gap:4px;
      pointer-events: none;
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
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
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

    .chat-title{{
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

    .chat-empty{{
      flex:1;
      min-height:100%;
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
    .top-btn:active,
    .top-select:active{{
      background:#ececec;
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
        white-space: normal;
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
        <!-- Socorristas dropdown -->
        <div class="top-select" id="socorristasContainer">
          <div class="btn-stack">
            <span class="btn-topline">seleccióna</span>
            <span class="btn-mainline" id="selectedSocorrista">Socorristas</span>
          </div>
          <select id="socorristasSelect" style="opacity:0; position:absolute; width:100%; height:100%; left:0; top:0; cursor:pointer;">
            <option value="">Cargando...</option>
          </select>
        </div>

        <!-- Instalación dropdown -->
        <div class="top-select" id="instalacionContainer">
          <div class="btn-stack">
            <span class="btn-topline">seleccióna</span>
            <span class="btn-mainline" id="selectedInstalacion">Instalación</span>
          </div>
          <select id="instalacionSelect" style="opacity:0; position:absolute; width:100%; height:100%; left:0; top:0; cursor:pointer;">
            <option value="">Cargando...</option>
          </select>
        </div>

        <!-- Notificaciones botón -->
        <button class="top-btn" id="btnNotificaciones" type="button">
          <div class="btn-center">Notificaciones</div>
        </button>
      </div>

      <div class="chat-shell">
        <div class="chat-title" id="chatTitle">Selecciona un contacto</div>

        <div class="chat-body" id="chatBody">
          <div class="chat-empty"></div>
        </div>

        <div class="input-row">
          <input
            id="chatInput"
            class="chat-input"
            type="text"
            placeholder="Escribe un mensaje..."
            autocomplete="off"
          />
          <button id="sendBtn" class="send-btn" type="button">SEND</button>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
  (function () {{
    // ========== CONFIGURACIÓN ==========
    const API_BASE = "https://camilo27.pythonanywhere.com";
    const CHAT_API_BASE = API_BASE + "/api/chat";
    const MALLAS_URL = API_BASE + "/api/mallas";
    const currentUserId = {escaped_dni};
    // ===================================

    let currentThreadId = null;
    let currentContactName = null;
    let threads = [];
    let pollingInterval = null;
    let threadsPollingInterval = null;
    let lastRenderedMessageId = null;

    const chatTitleEl = document.getElementById("chatTitle");
    const chatBody = document.getElementById("chatBody");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const socorristasSelect = document.getElementById("socorristasSelect");
    const instalacionSelect = document.getElementById("instalacionSelect");
    const selectedSocorristaSpan = document.getElementById("selectedSocorrista");
    const selectedInstalacionSpan = document.getElementById("selectedInstalacion");
    const btnNotificaciones = document.getElementById("btnNotificaciones");

    function escapeHtml(text) {{
      if (!text) return '';
      return String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
    }}

    async function fetchJSON(url, options = {{}}) {{
      const response = await fetch(url, options);
      if (!response.ok) {{
        throw new Error(`HTTP ${{response.status}} - ${{response.statusText}}`);
      }}
      return response.json();
    }}

    // ========== OBTENER DATOS REALES DESDE MALLAS ==========
    async function fetchSocorristas() {{
      try {{
        const data = await fetchJSON(MALLAS_URL);
        if (!data.ok || !Array.isArray(data.rows)) throw new Error("Formato inválido");
        const socorristasSet = new Set();
        data.rows.forEach(row => {{
          // Intentar obtener el nombre del socorrista (puede estar en diferentes campos)
          const nombre = row["Socorrista"] || row["socorrista"] || "";
          if (nombre.trim()) socorristasSet.add(nombre.trim());
        }});
        // Devolver array de objetos con dni y nombre (dni podría no estar, usamos el nombre como identificador)
        // Si tienes DNI en los datos, ajústalo aquí; de lo contrario, usamos el nombre como identificador único.
        return Array.from(socorristasSet).sort().map(nombre => ({{ dni: nombre, nombre: nombre }}));
      }} catch (error) {{
        console.error("Error cargando socorristas:", error);
        throw error;
      }}
    }}

    async function fetchInstalaciones() {{
      try {{
        const data = await fetchJSON(MALLAS_URL);
        if (!data.ok || !Array.isArray(data.rows)) throw new Error("Formato inválido");
        const instalacionesSet = new Set();
        data.rows.forEach(row => {{
          const inst = row["Instalacion"] || row["Instalación"] || row["instalacion"] || "";
          if (inst.trim()) instalacionesSet.add(inst.trim());
        }});
        return Array.from(instalacionesSet).sort().map(nombre => ({{ id: nombre, nombre: nombre }}));
      }} catch (error) {{
        console.error("Error cargando instalaciones:", error);
        throw error;
      }}
    }}
    // =================================================================

    async function loadDropdowns() {{
      // Cargar socorristas
      try {{
        const socorristas = await fetchSocorristas();
        socorristasSelect.innerHTML = '<option value="">Selecciona...</option>';
        socorristas.forEach(s => {{
          const option = document.createElement('option');
          option.value = s.dni;
          option.textContent = s.nombre;
          socorristasSelect.appendChild(option);
        }});
        socorristasSelect.disabled = false;
        console.log("Socorristas cargados:", socorristas.length);
      }} catch (error) {{
        console.error("Error cargando socorristas:", error);
        socorristasSelect.innerHTML = '<option value="">Error al cargar</option>';
      }}

      // Cargar instalaciones
      try {{
        const instalaciones = await fetchInstalaciones();
        instalacionSelect.innerHTML = '<option value="">Selecciona...</option>';
        instalaciones.forEach(i => {{
          const option = document.createElement('option');
          option.value = i.id;
          option.textContent = i.nombre;
          instalacionSelect.appendChild(option);
        }});
        instalacionSelect.disabled = false;
        console.log("Instalaciones cargadas:", instalaciones.length);
      }} catch (error) {{
        console.error("Error cargando instalaciones:", error);
        instalacionSelect.innerHTML = '<option value="">Error al cargar</option>';
      }}
    }}

    // ========== CHAT FUNCTIONS (igual que antes) ==========
    async function loadThreads() {{
      try {{
        const data = await fetchJSON(`${{CHAT_API_BASE}}/threads?user_id=${{encodeURIComponent(currentUserId)}}`);
        threads = data.threads || [];
      }} catch (error) {{
        console.error("Error loading threads:", error);
      }}
    }}

    function findPrivateThread(otherId) {{
      return threads.find(t => t.type === 'private' && t.participants && t.participants.includes(otherId));
    }}

    async function getOrCreatePrivateThread(otherId, contactName) {{
      let thread = findPrivateThread(otherId);
      if (thread) return thread.id;
      try {{
        const data = await fetchJSON(`${{CHAT_API_BASE}}/private/${{encodeURIComponent(otherId)}}?user_id=${{encodeURIComponent(currentUserId)}}`);
        if (data.thread_id) {{
          await loadThreads();
          return data.thread_id;
        }} else {{
          throw new Error("No se pudo crear el hilo");
        }}
      }} catch (error) {{
        console.error("Error creating private thread:", error);
        throw error;
      }}
    }}

    async function loadMessages(threadId, poll = false) {{
      const limit = poll ? 30 : 500;
      let url = `${{CHAT_API_BASE}}/threads/${{threadId}}/messages?user_id=${{encodeURIComponent(currentUserId)}}&limit=${{limit}}`;
      try {{
        const data = await fetchJSON(url);
        let messages = data.messages || [];
        if (poll && lastRenderedMessageId !== null) {{
          messages = messages.filter(m => parseInt(m.id) > lastRenderedMessageId);
        }}
        if (!poll) {{
          chatBody.innerHTML = '';
          lastRenderedMessageId = null;
        }}
        if (messages.length === 0 && !poll) {{
          chatBody.innerHTML = '<div class="chat-empty"></div>';
          lastRenderedMessageId = null;
          return;
        }}
        messages.forEach(msg => {{
          const div = document.createElement("div");
          div.className = "msg" + (msg.sender_id == currentUserId ? " out" : "");
          div.textContent = msg.body;
          chatBody.appendChild(div);
          lastRenderedMessageId = parseInt(msg.id);
        }});
        chatBody.scrollTop = chatBody.scrollHeight;
        await markThreadRead(threadId);
      }} catch (error) {{
        console.error("Error loading messages:", error);
        if (!poll) chatBody.innerHTML = `<div class="chat-empty" style="color:red;">Error al cargar mensajes: ${{escapeHtml(error.message)}}</div>`;
      }}
    }}

    async function markThreadRead(threadId) {{
      const lastMsg = chatBody.querySelector(".msg:last-child");
      if (!lastMsg) return;
      const lastId = lastMsg.getAttribute("data-id");
      if (!lastId) return;
      try {{
        await fetch(`${{CHAT_API_BASE}}/threads/${{threadId}}/read`, {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ user_id: currentUserId, last_read_message_id: lastId }})
        }});
      }} catch (error) {{
        console.error("Error marking read:", error);
      }}
    }}

    async function sendMessage() {{
      if (!currentThreadId) {{
        alert("Selecciona un socorrista o instalación primero.");
        return;
      }}
      const text = chatInput.value.trim();
      if (!text) return;
      chatInput.value = "";
      try {{
        await fetch(`${{CHAT_API_BASE}}/threads/${{currentThreadId}}/messages`, {{
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

    async function setActiveThread(threadId, contactName) {{
      if (pollingInterval) clearInterval(pollingInterval);
      currentThreadId = threadId;
      currentContactName = contactName;
      chatTitleEl.textContent = contactName;
      await loadMessages(threadId, false);
      pollingInterval = setInterval(() => {{
        if (currentThreadId) loadMessages(currentThreadId, true);
      }}, 10000);
    }}

    async function onSelectSocorrista(dni, nombre) {{
      if (!dni) return;
      selectedSocorristaSpan.textContent = nombre;
      instalacionSelect.value = "";
      selectedInstalacionSpan.textContent = "Instalación";
      try {{
        const threadId = await getOrCreatePrivateThread(dni, nombre);
        await setActiveThread(threadId, nombre);
      }} catch (error) {{
        alert("Error al iniciar chat con el socorrista: " + error.message);
      }}
    }}

    async function onSelectInstalacion(id, nombre) {{
      if (!id) return;
      selectedInstalacionSpan.textContent = nombre;
      socorristasSelect.value = "";
      selectedSocorristaSpan.textContent = "Socorristas";
      const instalacionDni = `INST_${{id}}`;
      try {{
        const threadId = await getOrCreatePrivateThread(instalacionDni, nombre);
        await setActiveThread(threadId, nombre);
      }} catch (error) {{
        alert("Error al iniciar chat con la instalación: " + error.message);
      }}
    }}

    socorristasSelect.addEventListener("change", (e) => {{
      const selectedDni = e.target.value;
      if (!selectedDni) return;
      const option = socorristasSelect.options[socorristasSelect.selectedIndex];
      const nombre = option.text;
      onSelectSocorrista(selectedDni, nombre);
    }});

    instalacionSelect.addEventListener("change", (e) => {{
      const selectedId = e.target.value;
      if (!selectedId) return;
      const option = instalacionSelect.options[instalacionSelect.selectedIndex];
      const nombre = option.text;
      onSelectInstalacion(selectedId, nombre);
    }});

    btnNotificaciones.addEventListener("click", () => {{
      alert("Funcionalidad de notificaciones en desarrollo.");
    }});

    sendBtn.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", (e) => {{
      if (e.key === "Enter") sendMessage();
    }});

    async function init() {{
      console.log("Iniciando chat, usuario:", currentUserId);
      if (!currentUserId || currentUserId === "") {{
        console.error("DNI de usuario no configurado");
        chatTitleEl.textContent = "Error: usuario no identificado";
        return;
      }}

      await loadDropdowns();
      await loadThreads();
      threadsPollingInterval = setInterval(loadThreads, 15000);
      chatTitleEl.textContent = "Selecciona un contacto";
      chatBody.innerHTML = '<div class="chat-empty"></div>';
    }}

    init();
  }})();
</script>
</body>
</html>
"""

components.html(html, height=800, scrolling=False)
