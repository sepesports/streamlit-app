# pages/chat_interfaz.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
      iframe{border:0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

USER_NAME = st.query_params.get("usuario") or ""
USER_ROLE = st.query_params.get("rol") or ""
USER_DNI = st.query_params.get("dni") or ""
API_BASE = "https://camilo27.pythonanywhere.com/api/chat"

BOOT = {
    "usuario": USER_NAME,
    "rol": USER_ROLE,
    "dni": USER_DNI,
    "api_base": API_BASE,
}

html = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
  <title>Chat</title>
  <style>
    :root{{
      --bg: #ffffff;
      --border: #111111;
      --text: #111111;
      --muted: #555555;
      --soft: #f6f6f6;
      --soft2: #efefef;
      --frame-margin: clamp(6px, 1.4vw, 16px);
      --border-size: 2px;
      --top-row-h: clamp(58px, 8vh, 72px);
      --panel-row-h: clamp(66px, 10vh, 88px);
      --title-row-h: clamp(42px, 6vh, 52px);
      --input-row-h: clamp(52px, 7vh, 62px);
      --font-main: clamp(14px, 1.5vw, 20px);
      --font-small: clamp(12px, 1.1vw, 15px);
      --font-title: clamp(15px, 1.5vw, 20px);
      --font-input: clamp(14px, 1.4vw, 18px);
      --font-send: clamp(14px, 1.4vw, 18px);
      --pad-x: clamp(8px, 1.2vw, 14px);
      --pad-y: clamp(6px, 0.8vw, 10px);
      --send-w: clamp(96px, 22vw, 130px);
    }}

    *{{ box-sizing:border-box; -webkit-tap-highlight-color:transparent; }}
    html, body{{ margin:0; padding:0; width:100%; height:100%; overflow:hidden; background:var(--bg); font-family:Arial, Helvetica, sans-serif; color:var(--text); }}

    #app{{ position:fixed; inset:0; width:100vw; height:100vh; background:var(--bg); padding:var(--frame-margin); }}
    .frame{{ width:100%; height:100%; border:var(--border-size) solid var(--border); display:flex; flex-direction:column; background:#fff; overflow:hidden; }}
    .inner{{ display:flex; flex-direction:column; width:100%; height:100%; padding:clamp(12px, 2vw, 22px); gap:10px; }}

    .top-buttons{{ display:grid; grid-template-columns:1fr 1fr 1.15fr; gap:0; width:100%; min-height:var(--top-row-h); }}
    .top-btn{{
      appearance:none; border:var(--border-size) solid var(--border); background:#fff; color:var(--text); margin:0;
      padding:var(--pad-y) var(--pad-x); cursor:pointer; display:flex; align-items:flex-start; justify-content:flex-start;
      text-align:left; line-height:1.1; min-height:var(--top-row-h); font-size:var(--font-main); font-weight:400;
      transition:background .15s ease, color .15s ease;
    }}
    .top-btn + .top-btn{{ border-left:none; }}
    .top-btn.active{{ background:var(--soft); }}
    .btn-stack{{ display:flex; flex-direction:column; align-items:flex-start; justify-content:center; gap:4px; }}
    .btn-topline{{ font-size:var(--font-small); line-height:1; }}
    .btn-mainline{{ font-size:var(--font-main); line-height:1.1; }}
    .btn-center{{ width:100%; height:100%; display:flex; align-items:center; justify-content:center; text-align:center; font-size:var(--font-main); line-height:1.1; }}

    .tool-panel{{
      min-height:var(--panel-row-h);
      border:var(--border-size) solid var(--border);
      background:#fff;
      display:flex;
      flex-direction:column;
      justify-content:center;
      padding:10px;
      gap:8px;
    }}
    .panel-hidden{{ display:none !important; }}
    .panel-row{{ display:grid; grid-template-columns: 1fr 1fr auto; gap:8px; align-items:center; }}
    .panel-row.install{{ grid-template-columns: 1fr auto; }}
    .panel-title{{ font-size:12px; color:var(--muted); }}
    .ctrl-input, .ctrl-select{{
      width:100%; height:42px; border:var(--border-size) solid var(--border); outline:none; padding:0 10px;
      font-size:var(--font-input); color:var(--text); background:#fff;
    }}
    .ctrl-button{{
      min-width:110px; height:42px; border:var(--border-size) solid var(--border); background:#fff; color:var(--text);
      font-size:var(--font-input); cursor:pointer;
    }}
    .ctrl-button:disabled{{ opacity:.45; cursor:not-allowed; }}
    .helper{{ font-size:12px; color:var(--muted); min-height:16px; }}

    .notifications-list{{
      display:flex; flex-direction:column; gap:6px; max-height:110px; overflow:auto; padding-right:4px;
    }}
    .notif-item{{
      border:var(--border-size) solid var(--border); background:#fff; padding:8px 10px; cursor:pointer;
      display:flex; align-items:center; justify-content:space-between; gap:8px;
    }}
    .notif-item:hover{{ background:var(--soft); }}
    .notif-left{{ display:flex; flex-direction:column; gap:2px; min-width:0; }}
    .notif-title{{ font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .notif-sub{{ font-size:12px; color:var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .badge{{ min-width:24px; height:24px; border:var(--border-size) solid var(--border); display:flex; align-items:center; justify-content:center; font-size:12px; background:var(--soft); padding:0 6px; }}

    .chat-shell{{ flex:1; min-height:0; display:flex; flex-direction:column; border:var(--border-size) solid var(--border); background:#fff; }}
    .chat-title{{ height:var(--title-row-h); min-height:var(--title-row-h); border-bottom:var(--border-size) solid var(--border); display:flex; align-items:center; justify-content:space-between; gap:10px; padding:0 var(--pad-x); font-size:var(--font-title); white-space:nowrap; overflow:hidden; }}
    .chat-title-text{{ min-width:0; overflow:hidden; text-overflow:ellipsis; }}
    .chat-title-meta{{ font-size:12px; color:var(--muted); }}

    .chat-body{{ flex:1; min-height:160px; overflow:auto; background:#fff; padding:14px; display:flex; flex-direction:column; gap:10px; }}
    .chat-empty{{ flex:1; min-height:100%; display:flex; align-items:center; justify-content:center; color:var(--muted); text-align:center; padding:14px; }}
    .msg{{ max-width:min(80%, 620px); border:var(--border-size) solid var(--border); padding:10px 12px; font-size:var(--font-input); line-height:1.3; background:#fff; word-break:break-word; }}
    .msg.out{{ margin-left:auto; background:var(--soft); }}
    .msg-head{{ font-size:12px; color:var(--muted); margin-bottom:4px; display:flex; justify-content:space-between; gap:8px; }}
    .msg-body{{ white-space:pre-wrap; }}

    .input-row{{ height:var(--input-row-h); min-height:var(--input-row-h); border-top:var(--border-size) solid var(--border); display:grid; grid-template-columns:1fr var(--send-w); gap:0; background:#fff; }}
    .chat-input{{ width:100%; height:100%; border:none; outline:none; padding:0 var(--pad-x); font-size:var(--font-input); color:var(--text); background:#fff; }}
    .chat-input::placeholder{{ color:#777; opacity:1; }}
    .send-btn{{ height:100%; width:100%; border:none; border-left:var(--border-size) solid var(--border); background:#fff; color:var(--text); font-size:var(--font-send); cursor:pointer; }}
    .send-btn:disabled{{ opacity:.45; cursor:not-allowed; }}
    .status-bar{{ min-height:18px; font-size:12px; color:var(--muted); padding:0 2px; }}
    .error{{ color:#9f1d1d; }}

    @media (max-width: 768px){{
      :root{{ --top-row-h:56px; --panel-row-h:92px; --title-row-h:42px; --input-row-h:52px; --send-w:92px; }}
      .inner{{ padding:10px; }}
      .panel-row{{ grid-template-columns:1fr; }}
      .panel-row.install{{ grid-template-columns:1fr; }}
      .ctrl-button{{ width:100%; }}
      .chat-title{{ flex-direction:column; align-items:flex-start; justify-content:center; padding:6px 10px; height:auto; min-height:var(--title-row-h); }}
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

        <div class="tool-panel" id="panelSocorristas">
          <div class="panel-title">Selecciona socorrista</div>
          <div class="panel-row">
            <input id="userSearch" class="ctrl-input" type="text" placeholder="Buscar socorrista" autocomplete="off"/>
            <select id="userSelect" class="ctrl-select"></select>
            <button id="openUserBtn" class="ctrl-button" type="button">Abrir chat</button>
          </div>
          <div class="helper" id="userHelper"></div>
        </div>

        <div class="tool-panel panel-hidden" id="panelInstalacion">
          <div class="panel-title">Selecciona instalación</div>
          <div class="panel-row install">
            <select id="installationSelect" class="ctrl-select"></select>
            <button id="openInstallationBtn" class="ctrl-button" type="button">Abrir grupo</button>
          </div>
          <div class="helper" id="installationHelper"></div>
        </div>

        <div class="tool-panel panel-hidden" id="panelNotificaciones">
          <div class="panel-title">Notificaciones</div>
          <div class="notifications-list" id="notificationsList"></div>
        </div>

        <div class="chat-shell">
          <div class="chat-title">
            <div class="chat-title-text" id="chatTitle">Nombre del socorrista o Grupo de instalación</div>
            <div class="chat-title-meta" id="chatMeta"></div>
          </div>

          <div class="chat-body" id="chatBody">
            <div class="chat-empty">Selecciona un socorrista, una instalación o una notificación.</div>
          </div>

          <div class="input-row">
            <input id="chatInput" class="chat-input" type="text" placeholder="Dialogo para enviar Mensaje" autocomplete="off" disabled />
            <button id="sendBtn" class="send-btn" type="button" disabled>SEND</button>
          </div>
        </div>

        <div class="status-bar" id="statusBar"></div>
      </div>
    </div>
  </div>

  <script>
    (function () {{
      const BOOT = {json.dumps(BOOT, ensure_ascii=False)};
      const API_BASE = BOOT.api_base;
      const CURRENT_USER = {{
        usuario: BOOT.usuario || "",
        rol: BOOT.rol || "",
        dni: BOOT.dni || ""
      }};

      const fe = window.frameElement;
      if (fe) {{
        fe.style.position = "fixed";
        fe.style.inset = "0";
        fe.style.width = "100vw";
        fe.style.height = "100vh";
        fe.style.border = "0";
        fe.style.margin = "0";
        fe.style.padding = "0";
        fe.style.zIndex = "999999";
        fe.style.background = "transparent";
      }}

      const btnSocorristas = document.getElementById("btnSocorristas");
      const btnInstalacion = document.getElementById("btnInstalacion");
      const btnNotificaciones = document.getElementById("btnNotificaciones");

      const panelSocorristas = document.getElementById("panelSocorristas");
      const panelInstalacion = document.getElementById("panelInstalacion");
      const panelNotificaciones = document.getElementById("panelNotificaciones");

      const userSearch = document.getElementById("userSearch");
      const userSelect = document.getElementById("userSelect");
      const openUserBtn = document.getElementById("openUserBtn");
      const userHelper = document.getElementById("userHelper");

      const installationSelect = document.getElementById("installationSelect");
      const openInstallationBtn = document.getElementById("openInstallationBtn");
      const installationHelper = document.getElementById("installationHelper");

      const notificationsList = document.getElementById("notificationsList");
      const chatTitle = document.getElementById("chatTitle");
      const chatMeta = document.getElementById("chatMeta");
      const chatBody = document.getElementById("chatBody");
      const chatInput = document.getElementById("chatInput");
      const sendBtn = document.getElementById("sendBtn");
      const statusBar = document.getElementById("statusBar");

      let users = [];
      let filteredUsers = [];
      let installations = [];
      let threads = [];
      let selectedThreadId = "";
      let pollHandle = null;
      let currentUserInfo = null;

      function setStatus(text, isError) {{
        statusBar.textContent = text || "";
        statusBar.className = "status-bar" + (isError ? " error" : "");
      }}

      function setActive(button) {{
        [btnSocorristas, btnInstalacion, btnNotificaciones].forEach(btn => btn.classList.remove("active"));
        button.classList.add("active");
        panelSocorristas.classList.add("panel-hidden");
        panelInstalacion.classList.add("panel-hidden");
        panelNotificaciones.classList.add("panel-hidden");

        if (button === btnSocorristas) panelSocorristas.classList.remove("panel-hidden");
        if (button === btnInstalacion) panelInstalacion.classList.remove("panel-hidden");
        if (button === btnNotificaciones) panelNotificaciones.classList.remove("panel-hidden");
      }}

      function authParams(extra) {{
        const p = new URLSearchParams();
        if (CURRENT_USER.usuario) p.set("usuario", CURRENT_USER.usuario);
        if (CURRENT_USER.dni) p.set("dni", CURRENT_USER.dni);
        if (CURRENT_USER.rol) p.set("rol", CURRENT_USER.rol);
        if (extra) {{
          Object.keys(extra).forEach(key => {{
            const val = extra[key];
            if (val !== undefined && val !== null && String(val) !== "") p.set(key, String(val));
          }});
        }}
        return p;
      }}

      async function apiGet(path, extra) {{
        const qs = authParams(extra).toString();
        const url = API_BASE + path + (qs ? ("?" + qs) : "");
        const r = await fetch(url, {{ method: "GET" }});
        const text = await r.text();
        let data = null;
        try {{ data = JSON.parse(text); }} catch (_) {{ data = {{ ok:false, error:text || ("HTTP " + r.status) }}; }}
        if (!r.ok && !data.error) data.error = "HTTP " + r.status;
        return data;
      }}

      async function apiPost(path, body) {{
        const payload = Object.assign({{}}, body || {{}}, {{
          usuario: CURRENT_USER.usuario || "",
          dni: CURRENT_USER.dni || "",
          rol: CURRENT_USER.rol || ""
        }});
        const r = await fetch(API_BASE + path, {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify(payload)
        }});
        const text = await r.text();
        let data = null;
        try {{ data = JSON.parse(text); }} catch (_) {{ data = {{ ok:false, error:text || ("HTTP " + r.status) }}; }}
        if (!r.ok && !data.error) data.error = "HTTP " + r.status;
        return data;
      }}

      function escapeHtml(value) {{
        return String(value || "")
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#39;");
      }}

      function formatDate(value) {{
        if (!value) return "";
        try {{
          const d = new Date(value);
          if (Number.isNaN(d.getTime())) return value;
          return d.toLocaleString("es-ES", {{
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit"
          }});
        }} catch (_) {{
          return value;
        }}
      }}

      function findThreadById(threadId) {{
        return threads.find(t => String(t.id) === String(threadId)) || null;
      }}

      function renderUsers() {{
        const term = (userSearch.value || "").trim().toLowerCase();
        filteredUsers = users.filter(item => !term || String(item.display_name || "").toLowerCase().includes(term) || String(item.correo || "").toLowerCase().includes(term));
        userSelect.innerHTML = "";
        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = filteredUsers.length ? "Selecciona socorrista" : "No hay socorristas";
        userSelect.appendChild(placeholder);

        filteredUsers.forEach(item => {{
          const opt = document.createElement("option");
          opt.value = item.user_id;
          opt.textContent = item.display_name + (item.role ? (" · " + item.role) : "");
          userSelect.appendChild(opt);
        }});

        userHelper.textContent = filteredUsers.length ? (filteredUsers.length + " socorrista(s) disponible(s)") : "Sin resultados";
        openUserBtn.disabled = !filteredUsers.length;
      }}

      function renderInstallations() {{
        installationSelect.innerHTML = "";
        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = installations.length ? "Selecciona instalación" : "No hay instalaciones";
        installationSelect.appendChild(placeholder);

        installations.forEach(item => {{
          const opt = document.createElement("option");
          opt.value = item;
          opt.textContent = item;
          installationSelect.appendChild(opt);
        }});
      }}

      function renderNotifications() {{
        const unread = threads.filter(t => Number(t.unread_count || 0) > 0);
        notificationsList.innerHTML = "";
        if (!unread.length) {{
          const div = document.createElement("div");
          div.className = "helper";
          div.textContent = "Sin notificaciones pendientes";
          notificationsList.appendChild(div);
          return;
        }}

        unread.forEach(item => {{
          const row = document.createElement("div");
          row.className = "notif-item";
          row.innerHTML = `
            <div class="notif-left">
              <div class="notif-title">${{escapeHtml(item.title || "Chat")}}</div>
              <div class="notif-sub">${{escapeHtml(item.last_message_preview || "Nuevo mensaje")}}</div>
            </div>
            <div class="badge">${{escapeHtml(item.unread_count || 0)}}</div>
          `;
          row.addEventListener("click", function(){{
            setActive(btnNotificaciones);
            openThread(item.id);
          }});
          notificationsList.appendChild(row);
        }});
      }}

      function setComposerState(enabled) {{
        chatInput.disabled = !enabled;
        sendBtn.disabled = !enabled;
      }}

      function renderMessages(thread, messages) {{
        if (!thread) {{
          chatTitle.textContent = "Nombre del socorrista o Grupo de instalación";
          chatMeta.textContent = "";
          chatBody.innerHTML = '<div class="chat-empty">Selecciona un socorrista, una instalación o una notificación.</div>';
          setComposerState(false);
          return;
        }}

        chatTitle.textContent = thread.title || "Chat";
        const unreadText = Number(thread.unread_count || 0) > 0 ? (" · " + thread.unread_count + " sin leer") : "";
        chatMeta.textContent = (thread.type === "group" ? "Grupo" : "Privado") + unreadText;

        if (!messages.length) {{
          chatBody.innerHTML = '<div class="chat-empty">Sin mensajes todavía.</div>';
        }} else {{
          chatBody.innerHTML = messages.map(msg => `
            <div class="msg ${{msg.mine ? 'out' : 'in'}}">
              <div class="msg-head">
                <span>${{escapeHtml(msg.sender_name || msg.sender_id || "Usuario")}}</span>
                <span>${{escapeHtml(formatDate(msg.created_at))}}</span>
              </div>
              <div class="msg-body">${{escapeHtml(msg.body || "")}}</div>
            </div>
          `).join("");
          chatBody.scrollTop = chatBody.scrollHeight;
        }}

        setComposerState(true);
      }}

      async function loadCurrentUser() {{
        setStatus("Validando usuario…", false);
        const data = await apiGet("/me");
        if (!data.ok) {{
          setStatus(data.error || "No se pudo validar el usuario", true);
          return false;
        }}
        currentUserInfo = data.user || null;
        if (!currentUserInfo) {{
          setStatus("Usuario no encontrado", true);
          return false;
        }}
        installationHelper.textContent = currentUserInfo.installation ? ("Instalación actual: " + currentUserInfo.installation) : "El usuario no tiene instalación asignada";
        setStatus("", false);
        return true;
      }}

      async function loadUsers() {{
        const data = await apiGet("/users");
        users = data.ok && Array.isArray(data.items) ? data.items : [];
        renderUsers();
      }}

      async function loadInstallations() {{
        const data = await apiGet("/installations/list");
        installations = data.ok && Array.isArray(data.items) ? data.items : [];
        renderInstallations();
        if (data.ok && data.current_installation) {{
          installationSelect.value = data.current_installation;
        }}
      }}

      async function loadThreads(preserveSelection) {{
        const data = await apiGet("/threads");
        if (!(data.ok && Array.isArray(data.items))) {{
          threads = [];
          renderNotifications();
          return;
        }}
        threads = data.items;
        renderNotifications();

        if (!preserveSelection && !selectedThreadId && threads.length) {{
          return;
        }}

        if (selectedThreadId) {{
          const selected = findThreadById(selectedThreadId);
          if (!selected) {{
            selectedThreadId = "";
            renderMessages(null, []);
            return;
          }}
        }}
      }}

      async function openThread(threadId) {{
        selectedThreadId = String(threadId || "");
        if (!selectedThreadId) {{
          renderMessages(null, []);
          return;
        }}
        const data = await apiGet("/threads/" + encodeURIComponent(selectedThreadId) + "/messages");
        if (!data.ok) {{
          setStatus(data.error || "No se pudo abrir el chat", true);
          return;
        }}
        const thread = data.thread || findThreadById(selectedThreadId) || {{ id: selectedThreadId, title: "Chat" }};
        const messages = Array.isArray(data.messages) ? data.messages : [];
        renderMessages(thread, messages);
        await loadThreads(true);
        setStatus("", false);
      }}

      async function createOrOpenPrivateThread() {{
        const otherUserId = userSelect.value || "";
        if (!otherUserId) {{
          setStatus("Selecciona un socorrista", true);
          return;
        }}
        setStatus("Abriendo chat…", false);
        const data = await apiPost("/threads/private", {{ other_user_id: otherUserId }});
        if (!data.ok || !data.thread) {{
          setStatus(data.error || "No se pudo abrir el chat privado", true);
          return;
        }}
        await loadThreads(true);
        await openThread(data.thread.id);
      }}

      async function createOrOpenInstallationThread() {{
        const installation = installationSelect.value || "";
        if (!installation) {{
          setStatus("Selecciona una instalación", true);
          return;
        }}
        setStatus("Abriendo grupo…", false);
        const data = await apiPost("/threads/installation", {{ installation }});
        if (!data.ok || !data.thread) {{
          setStatus(data.error || "No se pudo abrir el grupo", true);
          return;
        }}
        await loadThreads(true);
        await openThread(data.thread.id);
      }}

      async function sendMessage() {{
        const body = (chatInput.value || "").trim();
        if (!selectedThreadId) {{
          setStatus("Selecciona un chat antes de enviar", true);
          return;
        }}
        if (!body) {{
          return;
        }}
        sendBtn.disabled = true;
        const data = await apiPost("/threads/" + encodeURIComponent(selectedThreadId) + "/messages", {{ body }});
        sendBtn.disabled = false;
        if (!data.ok) {{
          setStatus(data.error || "No se pudo enviar el mensaje", true);
          return;
        }}
        chatInput.value = "";
        await openThread(selectedThreadId);
      }}

      async function refreshLoop() {{
        await loadThreads(true);
        if (selectedThreadId) {{
          await openThread(selectedThreadId);
        }}
      }}

      btnSocorristas.addEventListener("click", function () {{
        setActive(btnSocorristas);
      }});

      btnInstalacion.addEventListener("click", function () {{
        setActive(btnInstalacion);
      }});

      btnNotificaciones.addEventListener("click", function () {{
        setActive(btnNotificaciones);
      }});

      userSearch.addEventListener("input", renderUsers);
      openUserBtn.addEventListener("click", createOrOpenPrivateThread);
      openInstallationBtn.addEventListener("click", createOrOpenInstallationThread);
      sendBtn.addEventListener("click", sendMessage);

      chatInput.addEventListener("keydown", function (e) {{
        if (e.key === "Enter" && !e.shiftKey) {{
          e.preventDefault();
          sendMessage();
        }}
      }});

      (async function init() {{
        setActive(btnSocorristas);
        setComposerState(false);

        const ok = await loadCurrentUser();
        if (!ok) return;

        await loadUsers();
        await loadInstallations();
        await loadThreads(false);

        if (pollHandle) clearInterval(pollHandle);
        pollHandle = setInterval(refreshLoop, 6000);
      }})();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
