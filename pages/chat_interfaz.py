# chat_interfaz.py
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

USER_EMAIL = st.query_params.get("usuario") or ""
USER_ROLE = st.query_params.get("rol") or ""
USER_DNI = st.query_params.get("dni") or ""
API_BASE = "https://camilo27.pythonanywhere.com"

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
      --muted: #666666;
      --soft: #f5f5f5;
      --soft2: #efefef;
      --danger: #c0392b;
      --ok: #1f7a1f;

      --frame-margin: clamp(6px, 1.4vw, 16px);
      --border-size: 2px;
      --top-row-h: clamp(58px, 8vh, 72px);
      --toolbar-row-h: clamp(42px, 6vh, 52px);
      --input-row-h: clamp(52px, 7vh, 62px);
      --gap-top: clamp(8px, 1vw, 14px);
      --font-main: clamp(14px, 1.5vw, 20px);
      --font-small: clamp(12px, 1.1vw, 15px);
      --font-title: clamp(15px, 1.5vw, 20px);
      --font-input: clamp(14px, 1.4vw, 18px);
      --font-send: clamp(14px, 1.4vw, 18px);
      --pad-x: clamp(8px, 1.2vw, 14px);
      --pad-y: clamp(6px, 0.8vw, 10px);
      --send-w: clamp(96px, 22vw, 130px);
    }}

    *{{box-sizing:border-box; -webkit-tap-highlight-color: transparent;}}
    html, body{{margin:0; padding:0; width:100%; height:100%; overflow:hidden; background:var(--bg); font-family: Arial, Helvetica, sans-serif; color:var(--text);}}

    #app{{position:fixed; inset:0; width:100vw; height:100vh; background:var(--bg); padding:var(--frame-margin);}}
    .frame{{width:100%; height:100%; border:var(--border-size) solid var(--border); display:flex; flex-direction:column; background:#fff; overflow:hidden;}}
    .inner{{display:flex; flex-direction:column; width:100%; height:100%; padding:clamp(18px, 2.4vw, 28px); gap:var(--gap-top);}}

    .top-buttons{{display:grid; grid-template-columns: 1fr 1fr 1.1fr; gap:0; width:100%; min-height:var(--top-row-h);}}
    .top-btn{{appearance:none; border:var(--border-size) solid var(--border); background:#fff; color:var(--text); margin:0; padding:var(--pad-y) var(--pad-x); cursor:pointer; display:flex; align-items:flex-start; justify-content:flex-start; text-align:left; line-height:1.1; min-height:var(--top-row-h); font-size:var(--font-main); font-weight:400; transition:background .15s ease, color .15s ease; position:relative;}}
    .top-btn + .top-btn{{border-left:none;}}
    .top-btn.active{{background:#f5f5f5;}}
    .btn-stack{{display:flex; flex-direction:column; align-items:flex-start; justify-content:center; gap:4px;}}
    .btn-topline{{font-size:var(--font-small); font-weight:400; line-height:1;}}
    .btn-mainline{{font-size:var(--font-main); font-weight:400; line-height:1.1;}}
    .btn-center{{width:100%; height:100%; display:flex; align-items:center; justify-content:center; text-align:center; font-size:var(--font-main); line-height:1.1;}}
    .badge{{position:absolute; top:8px; right:8px; min-width:22px; height:22px; border:2px solid var(--border); border-radius:999px; display:none; align-items:center; justify-content:center; padding:0 6px; font-size:12px; background:#fff;}}
    .badge.show{{display:flex;}}

    .toolbar{{height:var(--toolbar-row-h); min-height:var(--toolbar-row-h); border:var(--border-size) solid var(--border); display:grid; grid-template-columns: 84px 1fr 96px; align-items:center; overflow:hidden;}}
    .toolbar-btn{{height:100%; border:none; background:#fff; cursor:pointer; font-size:14px; border-right:var(--border-size) solid var(--border);}}
    .toolbar-btn.right{{border-right:none; border-left:var(--border-size) solid var(--border);}}
    .toolbar-label{{padding:0 12px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-size:14px;}}

    .chat-shell{{flex:1; min-height:0; display:flex; flex-direction:column; border:var(--border-size) solid var(--border); background:#fff;}}
    .chat-title{{height:var(--toolbar-row-h); min-height:var(--toolbar-row-h); border-bottom:var(--border-size) solid var(--border); display:flex; align-items:center; gap:8px; padding:0 var(--pad-x); font-size:var(--font-title); font-weight:400; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}}
    .chat-status{{margin-left:auto; font-size:12px; color:var(--muted);}}
    .chat-body{{flex:1; min-height:160px; overflow:auto; background:#fff; padding:14px; display:flex; flex-direction:column; gap:10px;}}

    .empty-box{{border:var(--border-size) solid var(--border); padding:16px; background:#fff; font-size:14px;}}
    .list-item{{border:var(--border-size) solid var(--border); background:#fff; padding:12px; cursor:pointer; display:flex; flex-direction:column; gap:6px;}}
    .list-item:hover{{background:var(--soft);}}
    .list-title{{font-size:15px; font-weight:700;}}
    .list-sub{{font-size:13px; color:var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}}
    .list-row{{display:flex; align-items:center; justify-content:space-between; gap:12px;}}
    .list-count{{min-width:24px; height:24px; border:var(--border-size) solid var(--border); border-radius:999px; display:flex; align-items:center; justify-content:center; font-size:12px; padding:0 6px;}}

    .msg{{max-width:min(82%, 680px); border:var(--border-size) solid var(--border); padding:10px 12px; font-size:var(--font-input); line-height:1.3; background:#fff; word-break:break-word;}}
    .msg.out{{margin-left:auto;}}
    .msg-head{{font-size:12px; color:var(--muted); margin-bottom:6px;}}
    .msg-time{{margin-top:6px; font-size:11px; color:var(--muted);}}

    .input-row{{height:var(--input-row-h); min-height:var(--input-row-h); border-top:var(--border-size) solid var(--border); display:grid; grid-template-columns: 1fr var(--send-w); gap:0; background:#fff;}}
    .chat-input{{width:100%; height:100%; border:none; outline:none; padding:0 var(--pad-x); font-size:var(--font-input); color:var(--text); background:#fff;}}
    .chat-input::placeholder{{color:#111111; opacity:1;}}
    .chat-input:disabled{{background:var(--soft);}}
    .send-btn{{height:100%; width:100%; border:none; border-left:var(--border-size) solid var(--border); background:#fff; color:var(--text); font-size:var(--font-send); font-weight:400; cursor:pointer;}}
    .send-btn:disabled{{background:var(--soft); cursor:not-allowed;}}
    .send-btn:active,.top-btn:active,.toolbar-btn:active{{background:#ececec;}}

    .error{{border:var(--border-size) solid var(--border); padding:12px; font-size:13px; background:#fff; color:var(--danger);}}
    .ok{{color:var(--ok);}}

    @media (max-width: 768px){{
      :root{{
        --frame-margin: 6px;
        --border-size: 2px;
        --top-row-h: 56px;
        --toolbar-row-h: 42px;
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
      .inner{{padding:10px;}}
      .btn-stack{{gap:2px;}}
      .chat-body{{padding:10px;}}
      .toolbar{{grid-template-columns: 72px 1fr 88px;}}
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
      .inner{{padding:8px;}}
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
            <div class="badge" id="notifBadge">0</div>
          </button>
        </div>

        <div class="toolbar">
          <button id="backMenuBtn" class="toolbar-btn" type="button">Menú</button>
          <div class="toolbar-label" id="toolbarLabel">Cargando usuario…</div>
          <button id="refreshBtn" class="toolbar-btn right" type="button">Actualizar</button>
        </div>

        <div class="chat-shell">
          <div class="chat-title">
            <span id="chatTitle">Nombre del socorrista o Grupo de instalación</span>
            <span class="chat-status" id="chatStatus"></span>
          </div>

          <div class="chat-body" id="chatBody"></div>

          <div class="input-row">
            <input id="chatInput" class="chat-input" type="text" placeholder="Dialogo para enviar Mensaje" autocomplete="off" disabled />
            <button id="sendBtn" class="send-btn" type="button" disabled>SEND</button>
          </div>
        </div>

      </div>
    </div>
  </div>

  <script>
    (function () {{
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

      const API_BASE = {json.dumps(API_BASE)};
      const INITIAL_EMAIL = {json.dumps(USER_EMAIL)};
      const INITIAL_ROLE = {json.dumps(USER_ROLE)};
      const INITIAL_DNI = {json.dumps(USER_DNI)};

      const btnSocorristas = document.getElementById("btnSocorristas");
      const btnInstalacion = document.getElementById("btnInstalacion");
      const btnNotificaciones = document.getElementById("btnNotificaciones");
      const notifBadge = document.getElementById("notifBadge");
      const toolbarLabel = document.getElementById("toolbarLabel");
      const backMenuBtn = document.getElementById("backMenuBtn");
      const refreshBtn = document.getElementById("refreshBtn");
      const chatTitle = document.getElementById("chatTitle");
      const chatStatus = document.getElementById("chatStatus");
      const chatInput = document.getElementById("chatInput");
      const chatBody = document.getElementById("chatBody");
      const sendBtn = document.getElementById("sendBtn");

      const state = {{
        me: null,
        currentTab: "socorristas",
        selectedThread: null,
        selectedThreadId: "",
        messagesTimer: null,
        notificationsTimer: null,
        threads: [],
      }};

      function qs(params) {{
        const q = new URLSearchParams();
        Object.keys(params || {{}}).forEach((key) => {{
          const value = params[key];
          if (value !== undefined && value !== null && String(value) !== "") q.set(key, value);
        }});
        const s = q.toString();
        return s ? `?${{s}}` : "";
      }}

      async function apiGet(path, params) {{
        const url = API_BASE + path + qs(params);
        const r = await fetch(url, {{ method: "GET" }});
        return r.json();
      }}

      async function apiPost(path, body) {{
        const r = await fetch(API_BASE + path, {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify(body || {{}}),
        }});
        return r.json();
      }}

      function clearIntervals() {{
        if (state.messagesTimer) clearInterval(state.messagesTimer);
        if (state.notificationsTimer) clearInterval(state.notificationsTimer);
        state.messagesTimer = null;
        state.notificationsTimer = null;
      }}

      function setActive(button) {{
        [btnSocorristas, btnInstalacion, btnNotificaciones].forEach(btn => btn.classList.remove("active"));
        button.classList.add("active");
      }}

      function escapeText(value) {{
        return String(value || "");
      }}

      function setTitle(text) {{
        chatTitle.textContent = text || "";
      }}

      function setStatus(text) {{
        chatStatus.textContent = text || "";
      }}

      function setComposerEnabled(enabled) {{
        chatInput.disabled = !enabled;
        sendBtn.disabled = !enabled;
      }}

      function renderError(text) {{
        chatBody.innerHTML = "";
        const div = document.createElement("div");
        div.className = "error";
        div.textContent = text;
        chatBody.appendChild(div);
      }}

      function renderEmpty(text) {{
        chatBody.innerHTML = "";
        const div = document.createElement("div");
        div.className = "empty-box";
        div.textContent = text;
        chatBody.appendChild(div);
      }}

      function updateToolbar() {{
        if (!state.me) {{
          toolbarLabel.textContent = "Cargando usuario…";
          return;
        }}
        const parts = [state.me.display_name || state.me.correo || "Usuario"];
        if (state.me.role) parts.push(state.me.role);
        if (state.me.installation) parts.push(state.me.installation);
        toolbarLabel.textContent = parts.join(" · ");
      }}

      function updateNotificationBadge() {{
        const total = (state.threads || []).reduce((acc, t) => acc + Number(t.unread_count || 0), 0);
        notifBadge.textContent = String(total);
        notifBadge.classList.toggle("show", total > 0);
      }}

      function formatDateTime(value) {{
        if (!value) return "";
        const d = new Date(value);
        if (Number.isNaN(d.getTime())) return value;
        return d.toLocaleString("es-CO", {{ hour12: false }});
      }}

      function resetSelection() {{
        state.selectedThread = null;
        state.selectedThreadId = "";
        setComposerEnabled(false);
        chatInput.value = "";
      }}

      function goToMenu() {{
        try {{
          const params = new URLSearchParams(window.location.search || "");
          params.set("auth", "ok");
          window.location.href = "/?" + params.toString();
        }} catch (e) {{
          window.location.href = "/?auth=ok";
        }}
      }}

      async function resolveMe() {{
        const response = await apiGet("/api/chat/me", {{ usuario: INITIAL_EMAIL, dni: INITIAL_DNI }});
        if (!response || response.ok !== true || !response.user) {{
          throw new Error(response && response.error ? response.error : "No fue posible resolver el usuario actual");
        }}
        state.me = response.user;
        updateToolbar();
      }}

      async function loadThreadsForNotifications() {{
        if (!state.me) return;
        const response = await apiGet("/api/chat/threads", {{ user_id: state.me.user_id, usuario: state.me.correo }});
        if (response && response.ok === true && Array.isArray(response.items)) {{
          state.threads = response.items;
          updateNotificationBadge();
          if (state.currentTab === "notificaciones" && !state.selectedThreadId) {{
            renderNotificationsList();
          }}
        }}
      }}

      function renderContactList(items) {{
        chatBody.innerHTML = "";
        if (!items || !items.length) {{
          renderEmpty("No hay socorristas disponibles para este usuario.");
          return;
        }}

        items.forEach((item) => {{
          const card = document.createElement("div");
          card.className = "list-item";
          card.dataset.userId = item.user_id || "";

          const row = document.createElement("div");
          row.className = "list-row";

          const title = document.createElement("div");
          title.className = "list-title";
          title.textContent = escapeText(item.display_name || item.correo || item.user_id);

          row.appendChild(title);
          card.appendChild(row);

          const sub = document.createElement("div");
          sub.className = "list-sub";
          sub.textContent = [item.role || "", item.correo || ""].filter(Boolean).join(" · ");
          card.appendChild(sub);

          card.addEventListener("click", async () => {{
            const r = await apiPost("/api/chat/threads/private", {{
              user_id: state.me.user_id,
              usuario: state.me.correo,
              other_user_id: item.user_id,
            }});
            if (!r || r.ok !== true || !r.thread) {{
              renderError(r && r.error ? r.error : "No fue posible abrir el chat privado");
              return;
            }}
            await openThread(r.thread.id);
          }});

          chatBody.appendChild(card);
        }});
      }}

      function renderGroupList(items, installationName) {{
        chatBody.innerHTML = "";
        if (installationName) {{
          const info = document.createElement("div");
          info.className = "empty-box";
          info.textContent = "Instalación detectada: " + installationName;
          chatBody.appendChild(info);
        }}

        if (!items || !items.length) {{
          if (!installationName) {{
            renderEmpty("No hay grupo de instalación disponible para este usuario.");
          }} else {{
            const div = document.createElement("div");
            div.className = "empty-box";
            div.textContent = "No hay hilos grupales creados para esta instalación.";
            chatBody.appendChild(div);
          }}
          return;
        }}

        items.forEach((item) => {{
          const card = document.createElement("div");
          card.className = "list-item";
          card.dataset.threadId = item.id || "";

          const row = document.createElement("div");
          row.className = "list-row";

          const title = document.createElement("div");
          title.className = "list-title";
          title.textContent = escapeText(item.title || "Grupo instalación");
          row.appendChild(title);

          if (Number(item.unread_count || 0) > 0) {{
            const count = document.createElement("div");
            count.className = "list-count";
            count.textContent = String(item.unread_count);
            row.appendChild(count);
          }}

          card.appendChild(row);

          const sub = document.createElement("div");
          sub.className = "list-sub";
          const parts = [];
          if (item.last_message_preview) parts.push(item.last_message_preview);
          if (item.last_message_at) parts.push(formatDateTime(item.last_message_at));
          sub.textContent = parts.join(" · ") || "Sin mensajes";
          card.appendChild(sub);

          card.addEventListener("click", async () => {{
            await openThread(item.id);
          }});

          chatBody.appendChild(card);
        }});
      }}

      function renderNotificationsList() {{
        chatBody.innerHTML = "";
        const items = (state.threads || []).filter((t) => Number(t.unread_count || 0) > 0);

        if (!items.length) {{
          renderEmpty("No hay notificaciones pendientes.");
          return;
        }}

        items.forEach((item) => {{
          const card = document.createElement("div");
          card.className = "list-item";

          const row = document.createElement("div");
          row.className = "list-row";

          const title = document.createElement("div");
          title.className = "list-title";
          title.textContent = escapeText(item.title || "Chat");
          row.appendChild(title);

          const count = document.createElement("div");
          count.className = "list-count";
          count.textContent = String(item.unread_count || 0);
          row.appendChild(count);
          card.appendChild(row);

          const sub = document.createElement("div");
          sub.className = "list-sub";
          const parts = [];
          if (item.last_message_preview) parts.push(item.last_message_preview);
          if (item.last_message_at) parts.push(formatDateTime(item.last_message_at));
          sub.textContent = parts.join(" · ");
          card.appendChild(sub);

          card.addEventListener("click", async () => {{
            await openThread(item.id);
          }});

          chatBody.appendChild(card);
        }});
      }}

      function renderMessages(messages) {{
        chatBody.innerHTML = "";
        if (!messages || !messages.length) {{
          renderEmpty("No hay mensajes todavía en este chat.");
          return;
        }}

        messages.forEach((item) => {{
          const bubble = document.createElement("div");
          bubble.className = "msg" + (item.mine ? " out" : "");

          const head = document.createElement("div");
          head.className = "msg-head";
          head.textContent = item.mine ? "Tú" : escapeText(item.sender_name || item.sender_id || "Usuario");
          bubble.appendChild(head);

          const body = document.createElement("div");
          body.textContent = escapeText(item.body || "");
          bubble.appendChild(body);

          const time = document.createElement("div");
          time.className = "msg-time";
          time.textContent = formatDateTime(item.created_at);
          bubble.appendChild(time);

          chatBody.appendChild(bubble);
        }});

        chatBody.scrollTop = chatBody.scrollHeight;
      }}

      async function loadSocorristas() {{
        resetSelection();
        setTitle("Selecciona un socorrista");
        setStatus("");
        const response = await apiGet("/api/chat/users", {{ user_id: state.me.user_id, usuario: state.me.correo }});
        if (!response || response.ok !== true) {{
          renderError(response && response.error ? response.error : "No fue posible cargar los socorristas");
          return;
        }}
        renderContactList(response.items || []);
      }}

      async function loadInstalacion() {{
        resetSelection();
        setTitle("Grupo de instalación");
        setStatus("");
        const response = await apiGet("/api/chat/installations", {{ user_id: state.me.user_id, usuario: state.me.correo }});
        if (!response || response.ok !== true) {{
          renderError(response && response.error ? response.error : "No fue posible cargar la instalación");
          return;
        }}
        renderGroupList(response.items || [], response.installation || "");
      }}

      async function loadNotifications() {{
        resetSelection();
        setTitle("Notificaciones");
        setStatus("");
        await loadThreadsForNotifications();
        renderNotificationsList();
      }}

      async function openThread(threadId) {{
        state.selectedThreadId = threadId || "";
        if (!state.selectedThreadId) return;

        const response = await apiGet(`/api/chat/threads/${{encodeURIComponent(state.selectedThreadId)}}/messages`, {{
          user_id: state.me.user_id,
          usuario: state.me.correo,
        }});

        if (!response || response.ok !== true) {{
          renderError(response && response.error ? response.error : "No fue posible cargar el chat");
          return;
        }}

        state.selectedThread = response.thread || null;
        setComposerEnabled(true);
        setTitle((response.thread && response.thread.title) || "Chat");
        setStatus((response.thread && response.thread.type === "group") ? "Grupo" : "Privado");
        renderMessages(response.messages || []);
        chatInput.focus();
        await loadThreadsForNotifications();
      }}

      async function refreshCurrentView() {{
        if (!state.me) return;

        if (state.selectedThreadId) {{
          await openThread(state.selectedThreadId);
          return;
        }}

        if (state.currentTab === "socorristas") await loadSocorristas();
        else if (state.currentTab === "instalacion") await loadInstalacion();
        else await loadNotifications();
      }}

      async function sendMessage() {{
        const text = (chatInput.value || "").trim();
        if (!text || !state.selectedThreadId || !state.me) return;

        const response = await apiPost(`/api/chat/threads/${{encodeURIComponent(state.selectedThreadId)}}/messages`, {{
          user_id: state.me.user_id,
          usuario: state.me.correo,
          body: text,
        }});

        if (!response || response.ok !== true) {{
          renderError(response && response.error ? response.error : "No fue posible enviar el mensaje");
          return;
        }}

        chatInput.value = "";
        await openThread(state.selectedThreadId);
      }}

      function startPolling() {{
        clearIntervals();

        state.notificationsTimer = setInterval(async () => {{
          try {{
            await loadThreadsForNotifications();
          }} catch (e) {{}}
        }}, 5000);

        state.messagesTimer = setInterval(async () => {{
          try {{
            if (state.selectedThreadId) await openThread(state.selectedThreadId);
          }} catch (e) {{}}
        }}, 3000);
      }}

      btnSocorristas.addEventListener("click", async function () {{
        state.currentTab = "socorristas";
        setActive(btnSocorristas);
        await loadSocorristas();
      }});

      btnInstalacion.addEventListener("click", async function () {{
        state.currentTab = "instalacion";
        setActive(btnInstalacion);
        await loadInstalacion();
      }});

      btnNotificaciones.addEventListener("click", async function () {{
        state.currentTab = "notificaciones";
        setActive(btnNotificaciones);
        await loadNotifications();
      }});

      backMenuBtn.addEventListener("click", goToMenu);
      refreshBtn.addEventListener("click", refreshCurrentView);
      sendBtn.addEventListener("click", sendMessage);

      chatInput.addEventListener("keydown", function (e) {{
        if (e.key === "Enter") {{
          e.preventDefault();
          sendMessage();
        }}
      }});

      async function init() {{
        try {{
          await resolveMe();
          await loadThreadsForNotifications();
          await loadSocorristas();
          startPolling();
        }} catch (e) {{
          renderError(e && e.message ? e.message : "No fue posible iniciar el chat");
        }}
      }}

      init();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
