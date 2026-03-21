# pages/chat_interfaz.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Verificar autenticación
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

# Eliminar márgenes de Streamlit
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

html = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>Chat</title>
  <style>
    *{{
      margin:0;
      padding:0;
      box-sizing:border-box;
    }}
    html, body {{
      width:100%;
      height:100%;
      overflow:hidden;
      background: #020a1a;
      font-family: 'Segoe UI', Arial, sans-serif;
    }}
    #app {{
      width:100%;
      height:100%;
      display:flex;
      flex-direction:row;
      background:#020a1a;
    }}
    .threads-panel {{
      width: 280px;
      background: rgba(0,0,0,0.3);
      border-right: 1px solid #2a3a5a;
      display: flex;
      flex-direction: column;
      flex-shrink:0;
    }}
    .threads-header {{
      padding: 12px;
      border-bottom: 1px solid #2a3a5a;
      font-weight: bold;
      display: flex;
      justify-content: space-between;
      color: #eaf2ff;
    }}
    .new-chat-btn {{
      background: #ff9a52;
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
      border-bottom: 1px solid #2a3a5a;
      cursor: pointer;
      transition: background 0.2s;
      color: #eaf2ff;
    }}
    .thread-item:hover {{
      background: rgba(255,255,255,0.1);
    }}
    .thread-item.active {{
      background: rgba(255,255,255,0.2);
      border-left: 3px solid #ff9a52;
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
      background: #020a1a;
    }}
    .chat-header {{
      padding: 12px;
      border-bottom: 1px solid #2a3a5a;
      font-weight: bold;
      color: #eaf2ff;
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
      background: #0f1a2a;
      align-self: flex-start;
      color: #eaf2ff;
    }}
    .message.out {{
      background: #2a3a5a;
      align-self: flex-end;
    }}
    .message strong {{
      color: #ff9a52;
    }}
    .input-area {{
      display: flex;
      padding: 12px;
      border-top: 1px solid #2a3a5a;
      gap: 8px;
      background: #020a1a;
    }}
    #chatInput {{
      flex: 1;
      padding: 10px;
      border: 1px solid #2a3a5a;
      border-radius: 20px;
      background: #0f1a2a;
      color: #eaf2ff;
      outline: none;
    }}
    #sendBtn {{
      background: #ff9a52;
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
      background: #020a1a;
      border: 1px solid #2a3a5a;
      border-radius: 12px;
      width: 300px;
      max-width: 90%;
      padding: 20px;
      color: #eaf2ff;
    }}
    .modal-content input {{
      width: 100%;
      padding: 8px;
      margin-bottom: 12px;
      border: 1px solid #2a3a5a;
      background: #0f1a2a;
      color: #eaf2ff;
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
    /* Scrollbars */
    .thread-list::-webkit-scrollbar, .messages-area::-webkit-scrollbar {{
      width: 6px;
    }}
    .thread-list::-webkit-scrollbar-track, .messages-area::-webkit-scrollbar-track {{
      background: #0a1a2a;
    }}
    .thread-list::-webkit-scrollbar-thumb, .messages-area::-webkit-scrollbar-thumb {{
      background: #ff9a52;
      border-radius: 3px;
    }}
  </style>
</head>
<body>
<div id="app">
  <div class="threads-panel">
    <div class="threads-header">
      <span>Conversaciones</span>
      <button class="new-chat-btn" id="newChatBtn">+ Nuevo</button>
    </div>
    <div class="thread-list" id="threadList">
      <div style="padding: 12px; text-align: center;">Cargando...</div>
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

<script>
  const API_BASE = "https://camilo27.pythonanywhere.com/api/chat";
  const currentUserId = "{USER_DNI}";
  let currentThreadId = null;
  let threads = [];
  let pollingInterval = null;
  let lastRenderedMessageId = null;

  function escapeHtml(text) {{
    return String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
  }}

  async function fetchJSON(url, options = {{}}) {{
    const response = await fetch(url, options);
    return response.json();
  }}

  async function loadThreads() {{
    try {{
      const data = await fetchJSON(`${{API_BASE}}/threads?user_id=${{currentUserId}}`);
      threads = data.threads || [];
      renderThreadList();
      if (threads.length > 0 && !currentThreadId) {{
        setActiveThread(threads[0].id);
      }}
    }} catch(e) {{
      console.error('Error loading threads', e);
      document.getElementById("threadList").innerHTML = '<div style="padding: 12px; text-align: center;">Error al cargar conversaciones</div>';
    }}
  }}

  function renderThreadList() {{
    const container = document.getElementById("threadList");
    if (threads.length === 0) {{
      container.innerHTML = '<div style="padding: 12px; text-align: center;">No hay conversaciones</div>';
      return;
    }}
    container.innerHTML = threads.map(t => `
      <div class="thread-item ${{currentThreadId == t.id ? 'active' : ''}}" data-id="${{t.id}}">
        <div class="thread-title">${{escapeHtml(t.title || (t.type === 'private' ? 'Privado' : 'Grupo'))}}</div>
        <div class="thread-preview">${{escapeHtml(t.last_message || '')}}</div>
      </div>
    `).join('');
    document.querySelectorAll('.thread-item').forEach(el => {{
      el.addEventListener('click', () => setActiveThread(el.getAttribute('data-id')));
    }});
  }}

  async function loadMessages(threadId, poll = false) {{
    const limit = poll ? 50 : 500;
    let url = `${{API_BASE}}/threads/${{threadId}}/messages?user_id=${{currentUserId}}&limit=${{limit}}`;
    try {{
      const data = await fetchJSON(url);
      let messages = data.messages || [];
      if (poll && lastRenderedMessageId !== null) {{
        messages = messages.filter(m => parseInt(m.id) > lastRenderedMessageId);
      }}
      if (messages.length === 0 && !poll) {{
        document.getElementById("messagesArea").innerHTML = '<div style="text-align: center; margin-top: 20px;">No hay mensajes</div>';
        lastRenderedMessageId = null;
        return;
      }}
      const container = document.getElementById("messagesArea");
      if (!poll) {{
        container.innerHTML = '';
        lastRenderedMessageId = null;
      }}
      messages.forEach(msg => {{
        const div = document.createElement("div");
        div.className = "message" + (msg.sender_id == currentUserId ? " out" : "");
        div.innerHTML = `<strong>${{escapeHtml(msg.sender_alias || 'Usuario')}}:</strong> ${{escapeHtml(msg.body)}}`;
        container.appendChild(div);
        lastRenderedMessageId = parseInt(msg.id);
      }});
      container.scrollTop = container.scrollHeight;
      await markThreadRead(threadId);
    }} catch(e) {{
      console.error('Error loading messages', e);
    }}
  }}

  async function markThreadRead(threadId) {{
    const messagesDiv = document.getElementById("messagesArea");
    const lastMsg = messagesDiv.querySelector(".message:last-child");
    if (!lastMsg) return;
    const lastId = lastMsg.getAttribute("data-id");
    if (!lastId) return;
    try {{
      await fetch(`${{API_BASE}}/threads/${{threadId}}/read`, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ user_id: currentUserId, last_read_message_id: lastId }})
      }});
    }} catch(e) {{
      console.error('Error marking read', e);
    }}
  }}

  async function sendMessage() {{
    if (!currentThreadId) return;
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    try {{
      await fetch(`${{API_BASE}}/threads/${{currentThreadId}}/messages`, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ sender_id: currentUserId, body: text }})
      }});
      await loadMessages(currentThreadId, false);
    }} catch (e) {{
      console.error("Error sending message", e);
      alert("Error al enviar mensaje");
    }}
  }}

  function setActiveThread(threadId) {{
    currentThreadId = threadId;
    loadMessages(threadId, false);
    const thread = threads.find(t => t.id == threadId);
    document.getElementById("chatHeader").innerText = thread?.title || "Conversación";
    document.getElementById("inputArea").style.display = "flex";
    renderThreadList();
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(() => {{
      if (currentThreadId) loadMessages(currentThreadId, true);
    }}, 3000);
  }}

  function showNewChatModal() {{
    const modal = document.createElement("div");
    modal.className = "user-search-modal";
    modal.innerHTML = `
      <div class="modal-content">
        <span class="close-modal">&times;</span>
        <h3>Nuevo chat</h3>
        <input type="text" id="userSearch" placeholder="Buscar por alias o DNI">
        <div id="userSearchResults" class="user-list"></div>
      </div>
    `;
    document.body.appendChild(modal);
    const closeBtn = modal.querySelector(".close-modal");
    closeBtn.onclick = () => modal.remove();
    const searchInput = modal.querySelector("#userSearch");
    const resultsDiv = modal.querySelector("#userSearchResults");

    async function searchUsers() {{
      const query = searchInput.value.trim().toLowerCase();
      if (query.length < 2) {{
        resultsDiv.innerHTML = '<div>Escribe al menos 2 caracteres</div>';
        return;
      }}
      try {{
        const users = await fetchJSON(`${{API_BASE}}/users`);
        const filtered = users.filter(u => u.alias.toLowerCase().includes(query) || u.dni.includes(query));
        if (filtered.length === 0) {{
          resultsDiv.innerHTML = '<div>No se encontraron usuarios</div>';
          return;
        }}
        resultsDiv.innerHTML = filtered.map(u => `
          <div class="user-item" data-dni="${{u.dni}}">@${{escapeHtml(u.alias)}} (${{u.dni}})</div>
        `).join('');
        resultsDiv.querySelectorAll(".user-item").forEach(el => {{
          el.addEventListener("click", async () => {{
            const otherDni = el.getAttribute("data-dni");
            if (otherDni == currentUserId) {{
              alert("No puedes chatear contigo mismo");
              return;
            }}
            const data = await fetchJSON(`${{API_BASE}}/private/${{otherDni}}?user_id=${{currentUserId}}`);
            if (data.thread_id) {{
              setActiveThread(data.thread_id);
              modal.remove();
              await loadThreads();
            }}
          }});
        }});
      }} catch (e) {{
        resultsDiv.innerHTML = '<div>Error al cargar usuarios</div>';
      }}
    }}
    searchInput.addEventListener("input", searchUsers);
    searchUsers();
  }}

  document.getElementById("newChatBtn").addEventListener("click", showNewChatModal);
  document.getElementById("sendBtn").addEventListener("click", sendMessage);
  document.getElementById("chatInput").addEventListener("keypress", e => {{
    if (e.key === "Enter") sendMessage();
  }});

  loadThreads();
  setInterval(() => loadThreads(), 5000);
</script>
</body>
</html>
"""

components.html(html, height=800, scrolling=False)
