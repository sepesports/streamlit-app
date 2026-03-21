<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
  <title>Plano 2 Chat</title>
  <style>
    :root{
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
      background:#fff;
      overflow:hidden;
    }

    .inner{
      display:flex;
      flex-direction:column;
      width:100%;
      height:100%;
      padding:clamp(18px, 2.4vw, 28px);
      gap:var(--gap-top);
    }

    /* Contenedor de los tres elementos superiores: dos selects y un botón */
    .top-buttons{
      display:grid;
      grid-template-columns: var(--btn1) var(--btn2) var(--btn3);
      gap:0;
      width:100%;
      min-height:var(--top-row-h);
    }

    /* Estilo base para selects y botón */
    .top-btn, .top-select{
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
    }

    /* Para los selects, anulamos el estilo nativo y los hacemos como botones */
    .top-select{
      background-color: #fff;
      /* flecha personalizada */
      background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>');
      background-repeat: no-repeat;
      background-position: right var(--pad-x) center;
      background-size: 1.2em;
    }

    .top-select select{
      opacity: 0;
      position: absolute;
      width: 100%;
      height: 100%;
      left: 0;
      top: 0;
      cursor: pointer;
    }

    /* Para mantener la estructura de texto apilada similar a los botones originales */
    .btn-stack{
      display:flex;
      flex-direction:column;
      align-items:flex-start;
      justify-content:center;
      gap:4px;
      pointer-events: none;
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
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
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
      padding:0 var(--pad-x);
      font-size:var(--font-title);
      font-weight:400;
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

    .chat-empty{
      flex:1;
      min-height:100%;
    }

    .msg{
      max-width:min(78%, 560px);
      border:var(--border-size) solid var(--border);
      padding:10px 12px;
      font-size:var(--font-input);
      line-height:1.3;
      background:#fff;
      word-break:break-word;
    }

    .msg.out{
      margin-left:auto;
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

    .send-btn:active,
    .top-btn:active,
    .top-select:active{
      background:#ececec;
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
      }

      .inner{
        padding:10px;
      }

      .btn-stack{
        gap:2px;
      }

      .btn-mainline{
        word-break:break-word;
        white-space: normal;
      }

      .chat-body{
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
    }
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
  (function () {
    // ========== CONFIGURACIÓN ==========
    const API_BASE = "https://camilo27.pythonanywhere.com/api/chat";
    // Obtener DNI del usuario desde query params (injectado por Streamlit)
    const currentUserId = "REEMPLAZAR_DNI"; // Será reemplazado en el backend
    // ===================================

    // Estado de la aplicación
    let currentThreadId = null;
    let currentContactName = null;   // Nombre mostrado en el título
    let threads = [];                // Lista de hilos del usuario
    let pollingInterval = null;      // Polling de mensajes
    let threadsPollingInterval = null;
    let lastRenderedMessageId = null;

    // Elementos DOM
    const chatTitleEl = document.getElementById("chatTitle");
    const chatBody = document.getElementById("chatBody");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const socorristasSelect = document.getElementById("socorristasSelect");
    const instalacionSelect = document.getElementById("instalacionSelect");
    const selectedSocorristaSpan = document.getElementById("selectedSocorrista");
    const selectedInstalacionSpan = document.getElementById("selectedInstalacion");
    const btnNotificaciones = document.getElementById("btnNotificaciones");

    // ========== FUNCIONES AUXILIARES ==========
    function escapeHtml(text) {
      if (!text) return '';
      return String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
    }

    async function fetchJSON(url, options = {}) {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status} - ${response.statusText}`);
      }
      return response.json();
    }

    // ========== OBTENER DATOS DE ALTAS (socorristas e instalaciones) ==========
    // Aquí debes reemplazar las URLs por los endpoints reales que devuelvan:
    // Para socorristas: [{ dni: "12345678", nombre: "Juan Pérez" }]
    // Para instalaciones: [{ id: "grupo1", nombre: "Playa Central" }]
    // En este ejemplo simulamos con datos de prueba (pero manteniendo la estructura real)
    async function fetchSocorristas() {
      // TODO: Reemplazar con endpoint real que consulte la hoja ALTAS columna NOMBRE
      // Ejemplo:
      // const response = await fetch("/api/altas/socorristas");
      // return await response.json();
      // Simulación para pruebas:
      return new Promise(resolve => {
        setTimeout(() => {
          resolve([
            { dni: "11111111", nombre: "Ana García" },
            { dni: "22222222", nombre: "Carlos López" },
            { dni: "33333333", nombre: "María Rodríguez" }
          ]);
        }, 200);
      });
    }

    async function fetchInstalaciones() {
      // TODO: Reemplazar con endpoint real que consulte la hoja ALTAS columna INSTALACION
      // Puede devolver objetos con un identificador único (por ejemplo, id) y nombre
      // Simulación:
      return new Promise(resolve => {
        setTimeout(() => {
          resolve([
            { id: "inst1", nombre: "Piscina Municipal" },
            { id: "inst2", nombre: "Playa del Faro" },
            { id: "inst3", nombre: "Club Náutico" }
          ]);
        }, 200);
      });
    }

    // Cargar y poblar los dropdowns
    async function loadDropdowns() {
      try {
        const socorristas = await fetchSocorristas();
        socorristasSelect.innerHTML = '<option value="">Selecciona...</option>' +
          socorristas.map(s => `<option value="${s.dni}">${escapeHtml(s.nombre)}</option>`).join('');
        socorristasSelect.disabled = false;
        // Si hay algún valor seleccionado anteriormente, mantenerlo (no hay)
      } catch (error) {
        console.error("Error cargando socorristas:", error);
        socorristasSelect.innerHTML = '<option value="">Error al cargar</option>';
      }

      try {
        const instalaciones = await fetchInstalaciones();
        instalacionSelect.innerHTML = '<option value="">Selecciona...</option>' +
          instalaciones.map(i => `<option value="${i.id}">${escapeHtml(i.nombre)}</option>`).join('');
        instalacionSelect.disabled = false;
      } catch (error) {
        console.error("Error cargando instalaciones:", error);
        instalacionSelect.innerHTML = '<option value="">Error al cargar</option>';
      }
    }

    // ========== GESTIÓN DE HILOS Y MENSAJES ==========
    // Cargar todos los hilos del usuario actual
    async function loadThreads() {
      try {
        const data = await fetchJSON(`${API_BASE}/threads?user_id=${encodeURIComponent(currentUserId)}`);
        threads = data.threads || [];
        // No mostramos lista visual, solo almacenamos para saber si ya existe un hilo con un contacto
      } catch (error) {
        console.error("Error loading threads:", error);
      }
    }

    // Buscar si ya existe un hilo privado con otro usuario (por DNI)
    function findPrivateThread(otherDni) {
      return threads.find(t => t.type === 'private' && t.participants && t.participants.includes(otherDni));
    }

    // Obtener o crear un hilo privado con otro usuario
    async function getOrCreatePrivateThread(otherDni, contactName) {
      // Primero buscar localmente
      let thread = findPrivateThread(otherDni);
      if (thread) {
        return thread.id;
      }
      // Si no, llamar al endpoint /private para crearlo
      try {
        const data = await fetchJSON(`${API_BASE}/private/${encodeURIComponent(otherDni)}?user_id=${encodeURIComponent(currentUserId)}`);
        if (data.thread_id) {
          // Recargar threads para actualizar la lista local
          await loadThreads();
          return data.thread_id;
        } else {
          throw new Error("No se pudo crear el hilo");
        }
      } catch (error) {
        console.error("Error creating private thread:", error);
        throw error;
      }
    }

    // Cargar mensajes de un hilo
    async function loadMessages(threadId, poll = false) {
      const limit = poll ? 30 : 500;
      let url = `${API_BASE}/threads/${threadId}/messages?user_id=${encodeURIComponent(currentUserId)}&limit=${limit}`;
      try {
        const data = await fetchJSON(url);
        let messages = data.messages || [];
        if (poll && lastRenderedMessageId !== null) {
          messages = messages.filter(m => parseInt(m.id) > lastRenderedMessageId);
        }
        if (!poll) {
          // Limpiar área de mensajes
          chatBody.innerHTML = '';
          lastRenderedMessageId = null;
        }
        if (messages.length === 0 && !poll) {
          chatBody.innerHTML = '<div class="chat-empty"></div>';
          lastRenderedMessageId = null;
          return;
        }
        messages.forEach(msg => {
          const div = document.createElement("div");
          div.className = "msg" + (msg.sender_id == currentUserId ? " out" : "");
          div.innerHTML = escapeHtml(msg.body);
          chatBody.appendChild(div);
          lastRenderedMessageId = parseInt(msg.id);
        });
        chatBody.scrollTop = chatBody.scrollHeight;
        await markThreadRead(threadId);
      } catch (error) {
        console.error("Error loading messages:", error);
        if (!poll) chatBody.innerHTML = `<div class="chat-empty" style="color:red;">Error al cargar mensajes: ${escapeHtml(error.message)}</div>`;
      }
    }

    async function markThreadRead(threadId) {
      const lastMsg = chatBody.querySelector(".msg:last-child");
      if (!lastMsg) return;
      const lastId = lastMsg.getAttribute("data-id");
      if (!lastId) return;
      try {
        await fetch(`${API_BASE}/threads/${threadId}/read`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: currentUserId, last_read_message_id: lastId })
        });
      } catch (error) {
        console.error("Error marking read:", error);
      }
    }

    async function sendMessage() {
      if (!currentThreadId) {
        alert("Selecciona un socorrista o instalación primero.");
        return;
      }
      const text = chatInput.value.trim();
      if (!text) return;
      chatInput.value = "";
      try {
        await fetch(`${API_BASE}/threads/${currentThreadId}/messages`, {
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

    // Activar un hilo (cargar mensajes, iniciar polling)
    async function setActiveThread(threadId, contactName) {
      if (pollingInterval) clearInterval(pollingInterval);
      currentThreadId = threadId;
      currentContactName = contactName;
      chatTitleEl.textContent = contactName;
      await loadMessages(threadId, false);
      // Iniciar polling de mensajes cada 10 segundos
      pollingInterval = setInterval(() => {
        if (currentThreadId) loadMessages(currentThreadId, true);
      }, 10000);
    }

    // Acción al seleccionar un socorrista
    async function onSelectSocorrista(dni, nombre) {
      if (!dni) return;
      // Actualizar el texto mostrado en el botón (para UI)
      selectedSocorristaSpan.textContent = nombre;
      // Limpiar la selección del otro dropdown para mantener coherencia visual
      instalacionSelect.value = "";
      selectedInstalacionSpan.textContent = "Instalación";
      try {
        const threadId = await getOrCreatePrivateThread(dni, nombre);
        await setActiveThread(threadId, nombre);
      } catch (error) {
        alert("Error al iniciar chat con el socorrista: " + error.message);
      }
    }

    // Acción al seleccionar una instalación
    async function onSelectInstalacion(id, nombre) {
      if (!id) return;
      selectedInstalacionSpan.textContent = nombre;
      socorristasSelect.value = "";
      selectedSocorristaSpan.textContent = "Socorristas";
      // Asumimos que las instalaciones también son usuarios con un DNI especial o que se manejan como grupos.
      // Para este ejemplo, tratamos la instalación como un usuario especial con DNI = id (prefijado)
      // Si la API soporta grupos, debería ajustarse. Por ahora usamos el mismo endpoint privado con un DNI especial.
      const instalacionDni = `INST_${id}`;  // Identificador ficticio, ajustar según la realidad
      try {
        const threadId = await getOrCreatePrivateThread(instalacionDni, nombre);
        await setActiveThread(threadId, nombre);
      } catch (error) {
        alert("Error al iniciar chat con la instalación: " + error.message);
      }
    }

    // ========== EVENTOS ==========
    socorristasSelect.addEventListener("change", (e) => {
      const selectedDni = e.target.value;
      if (!selectedDni) return;
      const option = socorristasSelect.options[socorristasSelect.selectedIndex];
      const nombre = option.text;
      onSelectSocorrista(selectedDni, nombre);
    });

    instalacionSelect.addEventListener("change", (e) => {
      const selectedId = e.target.value;
      if (!selectedId) return;
      const option = instalacionSelect.options[instalacionSelect.selectedIndex];
      const nombre = option.text;
      onSelectInstalacion(selectedId, nombre);
    });

    btnNotificaciones.addEventListener("click", () => {
      alert("Funcionalidad de notificaciones en desarrollo.");
    });

    sendBtn.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") sendMessage();
    });

    // ========== INICIALIZACIÓN ==========
    async function init() {
      // Reemplazar el DNI del usuario (inyectado desde Streamlit)
      // El script recibirá el valor real desde el backend (por ejemplo, mediante una variable global)
      // Simulamos que el valor ya está en currentUserId (será reemplazado en el string final)
      if (currentUserId === "REEMPLAZAR_DNI") {
        console.error("DNI de usuario no configurado");
        chatTitleEl.textContent = "Error: usuario no identificado";
        return;
      }

      await loadDropdowns();
      await loadThreads();

      // Polling periódico para actualizar la lista de hilos (por si hay nuevos)
      threadsPollingInterval = setInterval(loadThreads, 15000);

      // No seleccionamos ningún hilo automáticamente, el usuario debe elegir un contacto.
      // Si se desea cargar el último hilo activo, se podría implementar, pero por ahora queda en blanco.
      chatTitleEl.textContent = "Selecciona un contacto";
      chatBody.innerHTML = '<div class="chat-empty"></div>';
    }

    init();
  })();
</script>
</body>
</html>
