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

html = """
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

    .top-buttons{
      display:grid;
      grid-template-columns: var(--btn1) var(--btn2) var(--btn3);
      gap:0;
      width:100%;
      min-height:var(--top-row-h);
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
      background:#f5f5f5;
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
    .top-btn:active{
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
          <div class="chat-title" id="chatTitle">Nombre del socorrista o Grupo de instalación</div>

          <div class="chat-body" id="chatBody">
            <div class="chat-empty"></div>
          </div>

          <div class="input-row">
            <input
              id="chatInput"
              class="chat-input"
              type="text"
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

      const btnSocorristas = document.getElementById("btnSocorristas");
      const btnInstalacion = document.getElementById("btnInstalacion");
      const btnNotificaciones = document.getElementById("btnNotificaciones");
      const chatTitle = document.getElementById("chatTitle");
      const chatInput = document.getElementById("chatInput");
      const chatBody = document.getElementById("chatBody");
      const sendBtn = document.getElementById("sendBtn");

      function setActive(button) {
        [btnSocorristas, btnInstalacion, btnNotificaciones].forEach(btn => {
          btn.classList.remove("active");
        });
        button.classList.add("active");
      }

      btnSocorristas.addEventListener("click", function () {
        setActive(btnSocorristas);
        chatTitle.textContent = "Nombre del socorrista o Grupo de instalación";
      });

      btnInstalacion.addEventListener("click", function () {
        setActive(btnInstalacion);
        chatTitle.textContent = "Nombre del socorrista o Grupo de instalación";
      });

      btnNotificaciones.addEventListener("click", function () {
        setActive(btnNotificaciones);
        chatTitle.textContent = "Notificaciones";
      });

      function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        const empty = chatBody.querySelector(".chat-empty");
        if (empty) empty.remove();

        const bubble = document.createElement("div");
        bubble.className = "msg out";
        bubble.textContent = text;

        chatBody.appendChild(bubble);
        chatInput.value = "";
        chatBody.scrollTop = chatBody.scrollHeight;
      }

      sendBtn.addEventListener("click", sendMessage);

      chatInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          sendMessage();
        }
      });
    })();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
