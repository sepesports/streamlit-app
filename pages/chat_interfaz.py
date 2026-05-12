<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>
  html,
  body{
    margin:0 !important;
    padding:0 !important;
    width:100% !important;
    height:100% !important;
    overflow:hidden !important;
    overscroll-behavior:none !important;
    background:#020614 !important;
  }

  body.admin-bar{
    margin-top:0 !important;
    padding-top:0 !important;
  }

  #wpadminbar,
  header,
  footer{
    display:none !important;
  }
</style>

<div id="syntra-chat-root">
  <style>
    #syntra-chat-root{
      --app-h:100dvh;
      --vv-top:0px;
      --safe-bottom:env(safe-area-inset-bottom,0px);
      --bg0:#020614;
      --bg1:#040e31;
      --bg2:#0a1a55;
      --bg3:#061240;
      --line:rgba(255,255,255,.14);
      --txt:rgba(255,255,255,.94);
      --muted:rgba(255,255,255,.66);
      --green:#008069;
      --blue:#2f7de1;
      --blue2:#1e5fc4;
      --red:#ff2d55;
      --chatbg:#efeae2;
      --incoming:#ffffff;
      --outgoing:#d9f0c3;
      position:fixed !important;
      top:var(--vv-top) !important;
      left:0 !important;
      right:0 !important;
      bottom:auto !important;
      z-index:2147483647 !important;
      width:100vw !important;
      height:var(--app-h) !important;
      min-height:var(--app-h) !important;
      margin:0 !important;
      padding:0 !important;
      background:
        radial-gradient(1100px 620px at 50% -8%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(40,120,255,.12), transparent 60%),
        linear-gradient(180deg,var(--bg0),var(--bg1));
      overflow:hidden !important;
      color:var(--txt);
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
      touch-action:manipulation;
    }

    #syntra-chat-root *{
      box-sizing:border-box;
    }

    #syntra-chat-root button,
    #syntra-chat-root input{
      font-family:inherit;
    }

    #syntra-chat-root .auth-layer{
      position:absolute;
      inset:0;
      z-index:100;
      display:none;
      align-items:center;
      justify-content:center;
      padding:18px;
      background:linear-gradient(180deg,#020614,#040e31);
    }

    #syntra-chat-root .auth-layer.show{
      display:flex;
    }

    #syntra-chat-root .auth-box{
      width:min(430px,94vw);
      border:1px solid var(--line);
      border-radius:28px;
      padding:22px;
      background:rgba(255,255,255,.075);
      box-shadow:0 22px 55px rgba(0,0,0,.52);
      backdrop-filter:blur(14px);
      -webkit-backdrop-filter:blur(14px);
    }

    #syntra-chat-root .auth-title{
      font-size:22px;
      font-weight:900;
      text-align:center;
      margin-bottom:16px;
    }

    #syntra-chat-root .auth-input{
      width:100%;
      height:46px;
      border:1px solid rgba(255,255,255,.22);
      border-radius:999px;
      background:rgba(0,0,0,.28);
      color:var(--txt);
      outline:0;
      padding:0 16px;
      font-size:16px;
      margin-bottom:10px;
    }

    #syntra-chat-root .auth-btn{
      width:100%;
      height:46px;
      border:0;
      border-radius:999px;
      background:linear-gradient(180deg,var(--blue),var(--blue2));
      color:#fff;
      font-weight:900;
      cursor:pointer;
      margin-top:6px;
    }

    #syntra-chat-root .auth-error{
      display:none;
      color:#ffb4b4;
      font-size:13px;
      font-weight:800;
      margin-top:12px;
      text-align:center;
    }

    #syntra-chat-root .topbar{
      position:absolute;
      top:4px;
      left:8px;
      right:8px;
      height:56px;
      z-index:40;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding:0 12px;
      border:1px solid var(--line);
      border-radius:20px;
      background:
        linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04)),
        linear-gradient(180deg,var(--bg2),var(--bg3));
      box-shadow:0 12px 28px rgba(0,0,0,.34);
      backdrop-filter:blur(14px);
      -webkit-backdrop-filter:blur(14px);
    }

    #syntra-chat-root .brand{
      min-width:0;
      display:flex;
      align-items:center;
      gap:10px;
    }

    #syntra-chat-root .brand-mark{
      width:34px;
      height:34px;
      flex:0 0 34px;
      border-radius:12px;
      display:grid;
      place-items:center;
      background:linear-gradient(135deg,#2f7de1,#008069);
      color:#fff;
      font-weight:900;
    }

    #syntra-chat-root .brand-copy{
      min-width:0;
    }

    #syntra-chat-root .brand-title{
      font-size:16px;
      line-height:1;
      font-weight:1000;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    #syntra-chat-root .brand-sub{
      margin-top:4px;
      font-size:10.5px;
      color:var(--muted);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
      max-width:58vw;
    }

    #syntra-chat-root .top-pill{
      height:32px;
      border:1px solid rgba(255,255,255,.14);
      border-radius:999px;
      background:rgba(255,255,255,.08);
      color:var(--txt);
      padding:0 12px;
      font-size:12px;
      font-weight:900;
      cursor:pointer;
    }

    #syntra-chat-root .chat-window{
      position:absolute;
      z-index:20;
      top:64px;
      left:8px;
      right:8px;
      bottom:calc(66px + var(--safe-bottom));
      border:1px solid var(--line);
      border-radius:22px;
      overflow:hidden;
      background:
        linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04)),
        linear-gradient(180deg,var(--bg2),var(--bg3) 32%,#02071c);
      box-shadow:0 22px 55px rgba(0,0,0,.52);
      display:grid;
      grid-template-rows:54px minmax(0,1fr) 58px;
    }

    #syntra-chat-root .chat-head{
      height:54px;
      min-height:54px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding:0 12px;
      border-bottom:1px solid var(--line);
      background:rgba(255,255,255,.06);
      min-width:0;
    }

    #syntra-chat-root .chat-title{
      min-width:0;
    }

    #syntra-chat-root .chat-name{
      font-size:15px;
      font-weight:1000;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    #syntra-chat-root .chat-status{
      margin-top:2px;
      font-size:10.5px;
      color:var(--muted);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    #syntra-chat-root .chat-kind{
      height:28px;
      flex:0 0 auto;
      border-radius:999px;
      padding:0 8px;
      border:1px solid rgba(255,255,255,.13);
      background:rgba(255,255,255,.08);
      color:var(--muted);
      font-size:10px;
      font-weight:900;
      display:flex;
      align-items:center;
      gap:5px;
    }

    #syntra-chat-root .messages{
      min-height:0;
      overflow-y:auto;
      overflow-x:hidden;
      background:var(--chatbg);
      padding:11px;
      display:flex;
      flex-direction:column;
      gap:8px;
      overscroll-behavior:contain;
      -webkit-overflow-scrolling:touch;
    }

    #syntra-chat-root .empty{
      margin:auto;
      max-width:320px;
      color:#667781;
      text-align:center;
      font-size:14px;
      font-weight:800;
      line-height:1.4;
    }

    #syntra-chat-root .msg{
      max-width:86%;
      padding:8px 11px;
      border-radius:16px;
      background:var(--incoming);
      color:#111b21;
      box-shadow:0 1px .5px rgba(0,0,0,.14);
      font-size:13px;
      line-height:1.35;
      overflow-wrap:anywhere;
      align-self:flex-start;
    }

    #syntra-chat-root .msg.out{
      background:var(--outgoing);
      align-self:flex-end;
    }

    #syntra-chat-root .msg.pending{
      opacity:.66;
    }

    #syntra-chat-root .msg strong{
      display:block;
      font-size:11px;
      color:#54656f;
      margin-bottom:3px;
    }

    #syntra-chat-root .msg-time{
      display:block;
      text-align:right;
      font-size:10px;
      color:#667781;
      margin-top:3px;
    }

    #syntra-chat-root .composer{
      min-height:58px;
      display:grid;
      grid-template-columns:minmax(0,1fr) 74px;
      gap:7px;
      align-items:center;
      padding:8px;
      background:#f0f2f5;
      border-top:1px solid #e9edef;
    }

    #syntra-chat-root .composer input{
      width:100%;
      min-width:0;
      height:42px;
      border:0;
      outline:0;
      border-radius:999px;
      background:#fff;
      color:#111b21;
      padding:0 16px;
      font-size:16px !important;
    }

    #syntra-chat-root .send{
      width:74px;
      height:42px;
      border:0;
      border-radius:999px;
      background:var(--green);
      color:#fff;
      font-weight:1000;
      cursor:pointer;
      font-size:13px;
    }

    #syntra-chat-root .send:disabled{
      opacity:.55;
      cursor:not-allowed;
    }

    #syntra-chat-root .bottom-nav{
      position:absolute;
      z-index:50;
      left:8px;
      right:8px;
      bottom:calc(6px + var(--safe-bottom));
      height:52px;
      border:1px solid var(--line);
      border-radius:18px;
      background:
        linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04)),
        linear-gradient(180deg,var(--bg2),#061240);
      box-shadow:0 12px 30px rgba(0,0,0,.38);
      display:grid;
      grid-template-columns:repeat(4,1fr);
      overflow:hidden;
      backdrop-filter:blur(14px);
      -webkit-backdrop-filter:blur(14px);
    }

    #syntra-chat-root .nav-btn{
      position:relative;
      border:0;
      border-right:1px solid rgba(255,255,255,.08);
      background:transparent;
      color:var(--muted);
      cursor:pointer;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      gap:3px;
      font-size:14px;
      font-weight:900;
      min-width:0;
    }

    #syntra-chat-root .nav-btn:last-child{
      border-right:0;
    }

    #syntra-chat-root .nav-btn span{
      font-size:8px;
      line-height:1;
      font-weight:1000;
      letter-spacing:.1px;
      white-space:nowrap;
    }

    #syntra-chat-root .nav-btn.active{
      color:#fff;
      background:rgba(0,128,105,.24);
    }

    #syntra-chat-root .nav-badge{
      position:absolute;
      top:4px;
      right:calc(50% - 23px);
      min-width:18px;
      height:18px;
      padding:0 5px;
      border-radius:999px;
      background:var(--red);
      color:#fff;
      font-size:10px;
      font-weight:1000;
      display:none;
      align-items:center;
      justify-content:center;
      border:1px solid #fff;
      box-shadow:0 0 10px rgba(255,45,85,.80);
    }

    #syntra-chat-root .nav-badge.show{
      display:flex;
    }

    #syntra-chat-root .backdrop{
      position:absolute;
      inset:0;
      z-index:60;
      display:none;
      background:rgba(0,0,0,.42);
      backdrop-filter:blur(3px);
      -webkit-backdrop-filter:blur(3px);
    }

    #syntra-chat-root .backdrop.show{
      display:block;
    }

    #syntra-chat-root .drawer{
      position:absolute;
      z-index:70;
      left:8px;
      right:8px;
      bottom:calc(64px + var(--safe-bottom));
      max-height:min(72dvh,620px);
      border:1px solid var(--line);
      border-radius:20px;
      background:
        linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04)),
        linear-gradient(180deg,var(--bg2),#061240 38%,#02071c);
      box-shadow:0 22px 55px rgba(0,0,0,.52);
      display:none;
      grid-template-rows:54px 52px minmax(0,1fr);
      overflow:hidden;
      backdrop-filter:blur(14px);
      -webkit-backdrop-filter:blur(14px);
    }

    #syntra-chat-root .drawer.show{
      display:grid;
    }

    #syntra-chat-root .drawer-head{
      height:54px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      padding:0 14px;
      border-bottom:1px solid var(--line);
    }

    #syntra-chat-root .drawer-title{
      font-size:15px;
      font-weight:1000;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    #syntra-chat-root .drawer-close{
      width:34px;
      height:30px;
      border:1px solid rgba(255,255,255,.15);
      border-radius:999px;
      background:rgba(255,255,255,.08);
      color:var(--txt);
      font-weight:1000;
      cursor:pointer;
    }

    #syntra-chat-root .drawer-search{
      padding:8px 10px;
      border-bottom:1px solid rgba(255,255,255,.08);
    }

    #syntra-chat-root .drawer-search input{
      width:100%;
      height:36px;
      border:1px solid rgba(255,255,255,.14);
      border-radius:999px;
      outline:0;
      background:rgba(0,0,0,.24);
      color:var(--txt);
      padding:0 14px;
      font-size:16px;
    }

    #syntra-chat-root .drawer-list{
      min-height:0;
      overflow-y:auto;
      padding:8px;
      overscroll-behavior:contain;
      -webkit-overflow-scrolling:touch;
    }

    #syntra-chat-root .item{
      width:100%;
      border:1px solid rgba(255,255,255,.10);
      border-radius:16px;
      background:rgba(255,255,255,.055);
      color:var(--txt);
      padding:12px;
      margin-bottom:8px;
      text-align:left;
      cursor:pointer;
    }

    #syntra-chat-root .item.active{
      border-color:rgba(0,128,105,.95);
      box-shadow:0 0 0 2px rgba(0,128,105,.20);
    }

    #syntra-chat-root .item-title{
      font-size:14px;
      font-weight:1000;
      margin-bottom:4px;
      overflow:hidden;
      text-overflow:ellipsis;
      white-space:nowrap;
    }

    #syntra-chat-root .item-sub{
      font-size:12px;
      color:var(--muted);
      overflow:hidden;
      text-overflow:ellipsis;
      white-space:nowrap;
    }

    #syntra-chat-root .item-meta{
      margin-top:6px;
      display:flex;
      flex-wrap:wrap;
      gap:6px;
    }

    #syntra-chat-root .chip{
      display:inline-flex;
      align-items:center;
      gap:5px;
      height:22px;
      padding:0 8px;
      border-radius:999px;
      background:rgba(255,255,255,.08);
      border:1px solid rgba(255,255,255,.10);
      color:var(--muted);
      font-size:10px;
      font-weight:900;
    }

    #syntra-chat-root .item-badge{
      float:right;
      min-width:20px;
      height:20px;
      padding:0 6px;
      border-radius:999px;
      background:var(--red);
      color:#fff;
      font-size:11px;
      font-weight:1000;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      margin-left:6px;
    }

    #syntra-chat-root .toast{
      position:absolute;
      left:16px;
      right:16px;
      bottom:calc(70px + var(--safe-bottom));
      z-index:120;
      display:none;
      max-width:520px;
      margin:0 auto;
      border:1px solid rgba(255,255,255,.16);
      border-radius:16px;
      background:rgba(2,6,20,.96);
      color:var(--txt);
      padding:12px 14px;
      text-align:center;
      font-size:13px;
      font-weight:900;
      box-shadow:0 18px 38px rgba(0,0,0,.42);
    }

    #syntra-chat-root .toast.show{
      display:block;
    }

    #syntra-chat-root.syntra-keyboard .topbar{
      top:4px;
      height:42px;
    }

    #syntra-chat-root.syntra-keyboard .brand-mark{
      width:28px;
      height:28px;
      flex-basis:28px;
      border-radius:10px;
    }

    #syntra-chat-root.syntra-keyboard .brand-title{
      font-size:13px;
    }

    #syntra-chat-root.syntra-keyboard .brand-sub{
      display:none;
    }

    #syntra-chat-root.syntra-keyboard .top-pill{
      height:28px;
      font-size:10px;
      padding:0 10px;
    }

    #syntra-chat-root.syntra-keyboard .chat-window{
      top:50px;
      bottom:4px;
      border-radius:18px;
      grid-template-rows:44px minmax(0,1fr) 54px;
    }

    #syntra-chat-root.syntra-keyboard .chat-head{
      height:44px;
      min-height:44px;
      padding:0 10px;
    }

    #syntra-chat-root.syntra-keyboard .chat-name{
      font-size:13px;
    }

    #syntra-chat-root.syntra-keyboard .chat-status{
      display:none;
    }

    #syntra-chat-root.syntra-keyboard .chat-kind{
      display:none;
    }

    #syntra-chat-root.syntra-keyboard .messages{
      padding:8px;
    }

    #syntra-chat-root.syntra-keyboard .composer{
      min-height:54px;
      grid-template-columns:minmax(0,1fr) 72px;
      gap:7px;
      padding:7px 8px;
    }

    #syntra-chat-root.syntra-keyboard .composer input{
      height:40px;
    }

    #syntra-chat-root.syntra-keyboard .send{
      width:72px;
      height:40px;
    }

    #syntra-chat-root.syntra-keyboard .bottom-nav,
    #syntra-chat-root.syntra-keyboard .drawer,
    #syntra-chat-root.syntra-keyboard .backdrop{
      display:none !important;
    }

    @media (min-width:900px){
      #syntra-chat-root{
        display:none !important;
      }

      html,
      body{
        overflow:hidden !important;
        background:#020614 !important;
      }
    }
  </style>

  <div class="auth-layer" id="authLayer">
    <div class="auth-box">
      <div class="auth-title">Acceso al chat</div>
      <input class="auth-input" id="authCorreo" type="email" placeholder="Correo" autocomplete="username">
      <input class="auth-input" id="authDni" type="password" placeholder="DNI" autocomplete="current-password">
      <button class="auth-btn" id="authBtn" type="button">Ingresar</button>
      <div class="auth-error" id="authError"></div>
    </div>
  </div>

  <header class="topbar">
    <div class="brand">
      <div class="brand-mark"><i class="fa-solid fa-user-shield"></i></div>
      <div class="brand-copy">
        <div class="brand-title">Chat Socorristas</div>
        <div class="brand-sub" id="sessionLabel">Validando sesión.</div>
      </div>
    </div>
    <button class="top-pill" id="logoutBtn" type="button">Salir</button>
  </header>

  <main class="chat-window">
    <div class="chat-head">
      <div class="chat-title">
        <div class="chat-name" id="chatName">Selecciona una conversación</div>
        <div class="chat-status" id="chatStatus">Chat conectado a Google Sheets</div>
      </div>
      <div class="chat-kind" id="chatKind">
        <i class="fa-solid fa-comments"></i>
        <span>Chat</span>
      </div>
    </div>

    <div class="messages" id="messagesBox">
      <div class="empty">Selecciona un chat, socorrista o instalación para iniciar.</div>
    </div>

    <div class="composer">
      <input id="messageInput" type="text" placeholder="Mensaje" autocomplete="off">
      <button class="send" id="sendBtn" type="button">Enviar</button>
    </div>
  </main>

  <div class="backdrop" id="backdrop"></div>

  <section class="drawer" id="drawer">
    <div class="drawer-head">
      <div class="drawer-title" id="drawerTitle">Chats</div>
      <button class="drawer-close" id="drawerClose" type="button">×</button>
    </div>
    <div class="drawer-search">
      <input id="drawerSearch" type="text" placeholder="Buscar..." autocomplete="off">
    </div>
    <div class="drawer-list" id="drawerList"></div>
  </section>

  <nav class="bottom-nav">
    <button class="nav-btn active" id="navChats" type="button" data-panel="chats">
      <i class="fa-solid fa-comment-dots"></i>
      <span>Chats</span>
      <em class="nav-badge" id="badgeChats"></em>
    </button>
    <button class="nav-btn" id="navSocorristas" type="button" data-panel="socorristas">
      <i class="fa-solid fa-user-group"></i>
      <span>Socorristas</span>
    </button>
    <button class="nav-btn" id="navInstalaciones" type="button" data-panel="instalaciones">
      <i class="fa-solid fa-building-shield"></i>
      <span>Instalación</span>
    </button>
    <button class="nav-btn" id="navAlertas" type="button" data-panel="alertas">
      <i class="fa-solid fa-bell"></i>
      <span>Alertas</span>
      <em class="nav-badge" id="badgeAlertas"></em>
    </button>
  </nav>

  <div class="toast" id="toast"></div>

  <script>
    (function(){
      const API_ROOT = "https://camilo27.pythonanywhere.com";
      const AUTH_API = API_ROOT + "/api/auth";
      const CHAT_API = API_ROOT + "/api/chat";
      const SESSION_KEY = "syntra_chat_session_v1";
      const SEEN_PREFIX = "syntra_chat_seen_";

      let session = null;
      let threads = [];
      let users = [];
      let installations = [];
      let currentThreadId = null;
      let currentThreadTitle = "";
      let currentThreadType = "";
      let activePanel = "chats";
      let pollingThreads = null;
      let pollingMessages = null;
      let lastMessageId = null;
      let isSending = false;

      const root = document.getElementById("syntra-chat-root");
      const authLayer = document.getElementById("authLayer");
      const authCorreo = document.getElementById("authCorreo");
      const authDni = document.getElementById("authDni");
      const authBtn = document.getElementById("authBtn");
      const authError = document.getElementById("authError");

      const sessionLabel = document.getElementById("sessionLabel");
      const logoutBtn = document.getElementById("logoutBtn");

      const chatName = document.getElementById("chatName");
      const chatStatus = document.getElementById("chatStatus");
      const chatKind = document.getElementById("chatKind");
      const messagesBox = document.getElementById("messagesBox");
      const messageInput = document.getElementById("messageInput");
      const sendBtn = document.getElementById("sendBtn");

      const backdrop = document.getElementById("backdrop");
      const drawer = document.getElementById("drawer");
      const drawerTitle = document.getElementById("drawerTitle");
      const drawerClose = document.getElementById("drawerClose");
      const drawerSearch = document.getElementById("drawerSearch");
      const drawerList = document.getElementById("drawerList");

      const navChats = document.getElementById("navChats");
      const navSocorristas = document.getElementById("navSocorristas");
      const navInstalaciones = document.getElementById("navInstalaciones");
      const navAlertas = document.getElementById("navAlertas");
      const badgeChats = document.getElementById("badgeChats");
      const badgeAlertas = document.getElementById("badgeAlertas");

      const toast = document.getElementById("toast");

      function esc(value){
        return String(value ?? "")
          .replaceAll("&","&amp;")
          .replaceAll("<","&lt;")
          .replaceAll(">","&gt;")
          .replaceAll('"',"&quot;")
          .replaceAll("'","&#039;");
      }

      function showToast(text){
        toast.textContent = text;
        toast.classList.add("show");
        setTimeout(function(){ toast.classList.remove("show"); }, 2400);
      }

      async function fetchJson(url, options){
        const response = await fetch(url, Object.assign({ cache:"no-store" }, options || {}));
        const data = await response.json().catch(function(){ return {}; });

        if(!response.ok){
          throw new Error(data.error || "HTTP " + response.status);
        }

        return data;
      }

      function setAppHeight(){
        const vv = window.visualViewport;
        const h = vv ? vv.height : window.innerHeight;
        const top = vv ? vv.offsetTop : 0;

        root.style.setProperty("--app-h", Math.max(320, Math.round(h)) + "px");
        root.style.setProperty("--vv-top", Math.round(top) + "px");
      }

      function keyboardOn(){
        setAppHeight();
        closeDrawer();
        root.classList.add("syntra-keyboard");
        setTimeout(scrollBottom, 140);
      }

      function keyboardOff(){
        setTimeout(function(){
          root.classList.remove("syntra-keyboard");
          setAppHeight();
          setTimeout(scrollBottom, 100);
        }, 140);
      }

      function initViewport(){
        setAppHeight();

        if(window.visualViewport){
          window.visualViewport.addEventListener("resize", function(){
            setAppHeight();
            if(document.activeElement === messageInput){
              root.classList.add("syntra-keyboard");
              closeDrawer();
              setTimeout(scrollBottom, 100);
            }
          });

          window.visualViewport.addEventListener("scroll", setAppHeight);
        }

        window.addEventListener("resize", setAppHeight);

        window.addEventListener("orientationchange", function(){
          setTimeout(setAppHeight, 300);
          setTimeout(setAppHeight, 800);
        });

        messageInput.addEventListener("focus", keyboardOn);
        messageInput.addEventListener("click", keyboardOn);
        messageInput.addEventListener("blur", keyboardOff);
      }

      function getUrlSession(){
        const p = new URLSearchParams(window.location.search);
        const dni = (p.get("dni") || "").trim();
        const usuario = (p.get("usuario") || p.get("user") || "").trim();
        const rol = (p.get("rol") || p.get("role") || "").trim();

        if(!dni) return null;

        return {
          dni:dni,
          usuario:usuario || "socorrista",
          rol:rol || ""
        };
      }

      function loadSession(){
        const fromUrl = getUrlSession();

        if(fromUrl){
          sessionStorage.setItem(SESSION_KEY, JSON.stringify(fromUrl));
          return fromUrl;
        }

        try{
          const raw = sessionStorage.getItem(SESSION_KEY);
          return raw ? JSON.parse(raw) : null;
        }catch(e){
          return null;
        }
      }

      function saveSession(data){
        session = {
          dni:String(data.dni || ""),
          usuario:String(data.usuario || ""),
          rol:String(data.rol || "")
        };
        sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
      }

      function clearSession(){
        sessionStorage.removeItem(SESSION_KEY);
        session = null;
      }

      function seenKey(){
        return SEEN_PREFIX + String(session && session.dni ? session.dni : "anon");
      }

      function getSeenMap(){
        try{
          return JSON.parse(localStorage.getItem(seenKey()) || "{}");
        }catch(e){
          return {};
        }
      }

      function setSeen(threadId, lastAt, lastId){
        const map = getSeenMap();
        map[String(threadId)] = {
          last_message_at:String(lastAt || ""),
          last_message_id:String(lastId || "")
        };
        localStorage.setItem(seenKey(), JSON.stringify(map));
      }

      function isUnread(thread){
        if(!thread || !thread.id) return false;
        if(String(thread.id) === String(currentThreadId)) return false;

        const count = Number(thread.unread_count || 0);

        if(count > 0) return true;

        if(!thread.last_message_at) return false;

        const seen = getSeenMap()[String(thread.id)];

        if(!seen){
          return String(thread.last_sender_id || "") !== String(session && session.dni ? session.dni : "");
        }

        return String(thread.last_message_at || "") > String(seen.last_message_at || "");
      }

      function unreadThreads(){
        return threads.filter(isUnread);
      }

      function updateBadges(){
        const unread = unreadThreads();
        const total = unread.reduce(function(acc, thread){
          return acc + Math.max(1, Number(thread.unread_count || 1));
        }, 0);

        badgeAlertas.textContent = total > 99 ? "99+" : String(total);
        badgeChats.textContent = total > 99 ? "99+" : String(total);

        badgeAlertas.classList.toggle("show", total > 0);
        badgeChats.classList.toggle("show", total > 0);
      }

      function updateSessionLabel(){
        sessionLabel.textContent = session
          ? session.usuario + " · " + (session.rol || "sin rol") + " · DNI " + session.dni
          : "Sin sesión";
      }

      function setChatKind(type){
        let icon = "fa-comments";
        let label = "Chat";

        if(type === "private"){
          icon = "fa-user";
          label = "Privado";
        }

        if(type === "installation"){
          icon = "fa-building-shield";
          label = "Instalación";
        }

        chatKind.innerHTML = '<i class="fa-solid ' + icon + '"></i><span>' + esc(label) + '</span>';
      }

      function setActiveNav(panel){
        activePanel = panel;

        [navChats, navSocorristas, navInstalaciones, navAlertas].forEach(function(btn){
          btn.classList.toggle("active", btn.getAttribute("data-panel") === panel);
        });
      }

      function openDrawer(panel){
        if(root.classList.contains("syntra-keyboard")) return;

        setActiveNav(panel);
        drawerSearch.value = "";
        drawer.classList.add("show");
        backdrop.classList.add("show");
        renderDrawer();
      }

      function closeDrawer(){
        drawer.classList.remove("show");
        backdrop.classList.remove("show");
      }

      function renderDrawer(){
        const q = drawerSearch.value.trim().toLowerCase();

        if(activePanel === "socorristas"){
          drawerTitle.textContent = "Socorristas";
          renderSocorristas(q);
          return;
        }

        if(activePanel === "instalaciones"){
          drawerTitle.textContent = "Instalaciones";
          renderInstalaciones(q);
          return;
        }

        if(activePanel === "alertas"){
          drawerTitle.textContent = "Alertas";
          renderAlertas(q);
          return;
        }

        drawerTitle.textContent = "Chats";
        renderChats(q);
      }

      function renderChats(q){
        const list = threads.filter(function(thread){
          return String(thread.title || "").toLowerCase().includes(q) ||
                 String(thread.last_message || "").toLowerCase().includes(q);
        });

        if(!list.length){
          drawerList.innerHTML =
            '<button class="item" type="button">' +
              '<div class="item-title">Sin conversaciones</div>' +
              '<div class="item-sub">Abre Socorristas o Instalación para iniciar.</div>' +
            '</button>';
          return;
        }

        drawerList.innerHTML = list.map(function(thread){
          const count = Number(thread.unread_count || 0);
          const unread = isUnread(thread);
          const active = String(thread.id) === String(currentThreadId);

          return '' +
            '<button class="item ' + (active ? "active" : "") + '" type="button" data-thread-id="' + esc(thread.id) + '">' +
              '<div class="item-title">' +
                (unread ? '<span class="item-badge">' + esc(count > 0 ? count : 1) + '</span>' : '') +
                esc(thread.title || "Chat") +
              '</div>' +
              '<div class="item-sub">' + esc(thread.last_message || "Sin mensajes") + '</div>' +
              '<div class="item-meta">' +
                '<span class="chip"><i class="fa-solid fa-message"></i>' + esc(thread.message_count || 0) + '</span>' +
                '<span class="chip"><i class="fa-solid ' + (thread.type === "installation" ? "fa-building-shield" : "fa-user") + '"></i>' + esc(thread.type === "installation" ? "Instalación" : "Privado") + '</span>' +
              '</div>' +
            '</button>';
        }).join("");

        drawerList.querySelectorAll("[data-thread-id]").forEach(function(btn){
          btn.addEventListener("click", function(){
            setActiveThread(btn.getAttribute("data-thread-id"));
            closeDrawer();
          });
        });
      }

      function renderSocorristas(q){
        const list = users.filter(function(user){
          return String(user.alias || "").toLowerCase().includes(q) ||
                 String(user.nombre || "").toLowerCase().includes(q) ||
                 String(user.dni || "").toLowerCase().includes(q) ||
                 String(user.instalacion || "").toLowerCase().includes(q);
        }).filter(function(user){
          return String(user.dni).toLowerCase() !== String(session.dni).toLowerCase();
        });

        if(!list.length){
          drawerList.innerHTML =
            '<button class="item" type="button">' +
              '<div class="item-title">Sin socorristas</div>' +
              '<div class="item-sub">No hay resultados.</div>' +
            '</button>';
          return;
        }

        drawerList.innerHTML = list.map(function(user){
          return '' +
            '<button class="item" type="button" data-user-dni="' + esc(user.dni) + '" data-user-alias="' + esc(user.alias) + '">' +
              '<div class="item-title">@' + esc(user.alias || "socorrista") + '</div>' +
              '<div class="item-sub">' + esc(user.nombre || user.correo || "Socorrista") + '</div>' +
              '<div class="item-meta">' +
                '<span class="chip"><i class="fa-solid fa-id-card"></i>DNI ' + esc(user.dni || "") + '</span>' +
                '<span class="chip"><i class="fa-solid fa-building"></i>' + esc(user.instalacion || "Sin instalación") + '</span>' +
              '</div>' +
            '</button>';
        }).join("");

        drawerList.querySelectorAll("[data-user-dni]").forEach(function(btn){
          btn.addEventListener("click", function(){
            openPrivateThread(btn.getAttribute("data-user-dni"), btn.getAttribute("data-user-alias"));
          });
        });
      }

      function renderInstalaciones(q){
        const list = installations.filter(function(item){
          return String(item.instalacion || "").toLowerCase().includes(q);
        });

        if(!list.length){
          drawerList.innerHTML =
            '<button class="item" type="button">' +
              '<div class="item-title">Sin instalaciones</div>' +
              '<div class="item-sub">No hay instalaciones disponibles para este perfil.</div>' +
            '</button>';
          return;
        }

        drawerList.innerHTML = list.map(function(item){
          const sample = Array.isArray(item.socorristas)
            ? item.socorristas.slice(0,3).map(function(u){ return "@" + (u.alias || "socorrista"); }).join(", ")
            : "";

          return '' +
            '<button class="item" type="button" data-installation="' + esc(item.instalacion) + '">' +
              '<div class="item-title">' + esc(item.instalacion || "Instalación") + '</div>' +
              '<div class="item-sub">' + esc(item.total || 0) + ' socorristas vinculados</div>' +
              '<div class="item-meta">' +
                '<span class="chip"><i class="fa-solid fa-users"></i>' + esc(item.total || 0) + '</span>' +
                '<span class="chip"><i class="fa-solid fa-comments"></i>Grupo</span>' +
              '</div>' +
              (sample ? '<div class="item-sub" style="margin-top:7px;">' + esc(sample) + '</div>' : '') +
            '</button>';
        }).join("");

        drawerList.querySelectorAll("[data-installation]").forEach(function(btn){
          btn.addEventListener("click", function(){
            openInstallationThread(btn.getAttribute("data-installation"));
          });
        });
      }

      function renderAlertas(q){
        const list = unreadThreads().filter(function(thread){
          return String(thread.title || "").toLowerCase().includes(q) ||
                 String(thread.last_message || "").toLowerCase().includes(q);
        });

        if(!list.length){
          drawerList.innerHTML =
            '<button class="item" type="button">' +
              '<div class="item-title">Sin alertas</div>' +
              '<div class="item-sub">No hay mensajes pendientes.</div>' +
            '</button>';
          return;
        }

        drawerList.innerHTML = list.map(function(thread){
          const count = Number(thread.unread_count || 1);

          return '' +
            '<button class="item" type="button" data-thread-id="' + esc(thread.id) + '">' +
              '<div class="item-title"><span class="item-badge">' + esc(count) + '</span>' + esc(thread.title || "Chat") + '</div>' +
              '<div class="item-sub">' + esc(thread.last_message || "Mensaje nuevo") + '</div>' +
            '</button>';
        }).join("");

        drawerList.querySelectorAll("[data-thread-id]").forEach(function(btn){
          btn.addEventListener("click", function(){
            setActiveThread(btn.getAttribute("data-thread-id"));
            closeDrawer();
          });
        });
      }

      async function loadUsers(){
        try{
          users = await fetchJson(CHAT_API + "/users?_=" + Date.now());
        }catch(e){
          users = [];
          showToast("Error al cargar socorristas.");
        }
      }

      async function loadInstallations(){
        if(!session || !session.dni) return;

        try{
          const data = await fetchJson(CHAT_API + "/installations?user_id=" + encodeURIComponent(session.dni) + "&_=" + Date.now());
          installations = Array.isArray(data.installations) ? data.installations : [];
        }catch(e){
          installations = [];
        }
      }

      async function loadThreads(silent){
        if(!session || !session.dni) return;

        try{
          const data = await fetchJson(CHAT_API + "/threads?user_id=" + encodeURIComponent(session.dni) + "&_=" + Date.now());
          threads = Array.isArray(data.threads) ? data.threads : [];
          updateBadges();

          if(drawer.classList.contains("show")){
            renderDrawer();
          }

          if(!silent && threads.length && !currentThreadId){
            await setActiveThread(threads[0].id);
          }
        }catch(e){
          if(!silent){
            showToast("Error al cargar chats.");
          }
        }
      }

      async function openPrivateThread(otherDni, alias){
        if(!otherDni || !session || !session.dni) return;

        closeDrawer();
        chatName.textContent = alias || "Socorrista";
        chatStatus.textContent = "Abriendo chat privado.";
        messagesBox.innerHTML = '<div class="empty">Abriendo conversación.</div>';

        try{
          const data = await fetchJson(
            CHAT_API + "/private/" + encodeURIComponent(otherDni) +
            "?user_id=" + encodeURIComponent(session.dni) +
            "&_=" + Date.now()
          );

          if(!data.thread_id){
            showToast("No se pudo abrir el chat privado.");
            messagesBox.innerHTML = '<div class="empty">No se pudo abrir esta conversación.</div>';
            return;
          }

          await loadThreads(true);
          await setActiveThread(data.thread_id, alias || "Socorrista");
        }catch(e){
          showToast("Error al abrir el chat privado.");
          messagesBox.innerHTML = '<div class="empty">No se pudo abrir esta conversación.</div>';
        }
      }

      async function openInstallationThread(instalacion){
        if(!instalacion || !session || !session.dni) return;

        closeDrawer();
        chatName.textContent = "Instalación · " + instalacion;
        chatStatus.textContent = "Abriendo grupo de instalación.";
        messagesBox.innerHTML = '<div class="empty">Abriendo grupo.</div>';

        try{
          const data = await fetchJson(
            CHAT_API + "/installation/" + encodeURIComponent(instalacion) +
            "?user_id=" + encodeURIComponent(session.dni) +
            "&_=" + Date.now()
          );

          if(!data.thread_id){
            showToast("No se pudo abrir el grupo.");
            messagesBox.innerHTML = '<div class="empty">No se pudo abrir este grupo.</div>';
            return;
          }

          await loadThreads(true);
          await setActiveThread(data.thread_id, "Instalación · " + instalacion);
        }catch(e){
          showToast("Error al abrir grupo de instalación.");
          messagesBox.innerHTML = '<div class="empty">No se pudo abrir este grupo.</div>';
        }
      }

      async function setActiveThread(threadId, fallbackTitle){
        currentThreadId = String(threadId || "");
        lastMessageId = null;

        const found = threads.find(function(thread){
          return String(thread.id) === String(currentThreadId);
        });

        currentThreadTitle = found ? found.title : (fallbackTitle || "Conversación");
        currentThreadType = found ? found.type : "";

        chatName.textContent = currentThreadTitle || "Conversación";
        chatStatus.textContent = "Cargando mensajes.";
        setChatKind(currentThreadType);

        messagesBox.innerHTML = '<div class="empty">Cargando mensajes.</div>';

        await loadMessages(false);
        startMessagePolling();
      }

      function formatTime(value){
        if(!value) return "";

        try{
          const date = new Date(value);
          if(isNaN(date.getTime())) return "";

          return date.toLocaleTimeString("es-ES", {
            hour:"2-digit",
            minute:"2-digit"
          });
        }catch(e){
          return "";
        }
      }

      function renderMessages(messages){
        const list = Array.isArray(messages) ? messages : [];

        if(!list.length){
          messagesBox.innerHTML = '<div class="empty">No hay mensajes todavía.</div>';
          chatStatus.textContent = "Sin mensajes.";
          lastMessageId = null;
          return;
        }

        messagesBox.innerHTML = list.map(function(msg){
          const mine = String(msg.sender_id).toLowerCase() === String(session.dni).toLowerCase();
          const created = formatTime(msg.created_at);

          return '' +
            '<div class="msg ' + (mine ? "out" : "") + '" data-id="' + esc(msg.id) + '">' +
              '<strong>' + (mine ? "Tú" : "@" + esc(msg.sender_alias || "Socorrista")) + '</strong>' +
              esc(msg.body || "") +
              '<span class="msg-time">' + esc(created) + '</span>' +
            '</div>';
        }).join("");

        const last = list[list.length - 1];
        lastMessageId = Number(last.id || 0) || null;
        chatStatus.textContent = list.length + " mensajes";
        scrollBottom();
        markRead(last);
      }

      function appendNewMessages(messages){
        if(!Array.isArray(messages) || !messages.length) return;

        const existing = new Set(
          Array.from(messagesBox.querySelectorAll(".msg")).map(function(el){
            return String(el.getAttribute("data-id"));
          })
        );

        let added = false;

        messages.forEach(function(msg){
          const id = String(msg.id || "");

          if(!id || existing.has(id)) return;
          if(lastMessageId && Number(id) <= Number(lastMessageId)) return;

          const mine = String(msg.sender_id).toLowerCase() === String(session.dni).toLowerCase();
          const div = document.createElement("div");

          div.className = "msg" + (mine ? " out" : "");
          div.setAttribute("data-id", id);
          div.innerHTML =
            '<strong>' + (mine ? "Tú" : "@" + esc(msg.sender_alias || "Socorrista")) + '</strong>' +
            esc(msg.body || "") +
            '<span class="msg-time">' + esc(formatTime(msg.created_at)) + '</span>';

          messagesBox.appendChild(div);
          lastMessageId = Number(id) || lastMessageId;
          added = true;
        });

        if(added){
          scrollBottom();
          const last = messages[messages.length - 1];
          markRead(last);
        }
      }

      async function loadMessages(poll){
        if(!currentThreadId || !session || !session.dni) return;

        try{
          const data = await fetchJson(
            CHAT_API + "/threads/" + encodeURIComponent(currentThreadId) +
            "/messages?user_id=" + encodeURIComponent(session.dni) +
            "&limit=90&_=" + Date.now()
          );

          const messages = Array.isArray(data.messages) ? data.messages : [];

          if(poll && lastMessageId){
            appendNewMessages(messages);
          }else{
            renderMessages(messages);
          }
        }catch(e){
          if(!poll){
            messagesBox.innerHTML = '<div class="empty">No se pudieron cargar mensajes.</div>';
            chatStatus.textContent = "Sin conexión temporal";
          }
        }
      }

      async function markRead(last){
        if(!last || !currentThreadId || !session || !session.dni) return;

        setSeen(currentThreadId, last.created_at || "", last.id || "");

        try{
          await fetchJson(CHAT_API + "/threads/" + encodeURIComponent(currentThreadId) + "/read", {
            method:"POST",
            headers:{ "Content-Type":"application/json" },
            body:JSON.stringify({
              user_id:session.dni,
              last_read_message_id:String(last.id || "")
            })
          });
        }catch(e){}

        await loadThreads(true);
      }

      function appendPending(body){
        const div = document.createElement("div");
        div.className = "msg out pending";
        div.setAttribute("data-id", "pending-" + Date.now());
        div.innerHTML =
          '<strong>Tú</strong>' +
          esc(body) +
          '<span class="msg-time">Enviando.</span>';

        const empty = messagesBox.querySelector(".empty");

        if(empty){
          messagesBox.innerHTML = "";
        }

        messagesBox.appendChild(div);
        scrollBottom();
      }

      async function sendMessage(){
        if(isSending) return;

        if(!currentThreadId){
          showToast("Selecciona una conversación.");
          return;
        }

        const body = messageInput.value.trim();

        if(!body) return;

        isSending = true;
        sendBtn.disabled = true;
        sendBtn.textContent = "Enviando";

        appendPending(body);
        messageInput.value = "";

        try{
          const data = await fetchJson(CHAT_API + "/threads/" + encodeURIComponent(currentThreadId) + "/messages", {
            method:"POST",
            headers:{ "Content-Type":"application/json" },
            body:JSON.stringify({
              sender_id:session.dni,
              body:body
            })
          });

          if(!data || !data.ok || !data.message){
            showToast("No se confirmó el envío.");
          }

          await loadMessages(false);
          await loadThreads(true);
        }catch(e){
          showToast("Error al enviar mensaje.");
          await loadMessages(false);
        }finally{
          isSending = false;
          sendBtn.disabled = false;
          sendBtn.textContent = "Enviar";
          messageInput.focus({ preventScroll:true });
        }
      }

      function scrollBottom(){
        requestAnimationFrame(function(){
          messagesBox.scrollTop = messagesBox.scrollHeight;
        });
      }

      function startMessagePolling(){
        clearInterval(pollingMessages);
        pollingMessages = setInterval(function(){
          loadMessages(true);
        }, 2300);
      }

      function startThreadPolling(){
        clearInterval(pollingThreads);
        pollingThreads = setInterval(function(){
          loadThreads(true);
        }, 3000);
      }

      async function login(){
        const usuario = authCorreo.value.trim().toLowerCase();
        const dni = authDni.value.trim();

        authError.style.display = "none";
        authBtn.disabled = true;

        try{
          const data = await fetchJson(AUTH_API, {
            method:"POST",
            headers:{ "Content-Type":"application/json" },
            body:JSON.stringify({
              usuario:usuario,
              password:dni
            })
          });

          if(!data.ok){
            authError.textContent = "Credenciales inválidas.";
            authError.style.display = "block";
            return;
          }

          saveSession(data);
          authLayer.classList.remove("show");
          await initChat();
        }catch(e){
          authError.textContent = "Error de conexión.";
          authError.style.display = "block";
        }finally{
          authBtn.disabled = false;
        }
      }

      async function initChat(){
        updateSessionLabel();

        await Promise.all([
          loadUsers(),
          loadInstallations()
        ]);

        await loadThreads(false);
        startThreadPolling();

        if(!threads.length){
          messagesBox.innerHTML = '<div class="empty">Abre Socorristas o Instalación para iniciar.</div>';
        }
      }

      navChats.addEventListener("click", function(){ openDrawer("chats"); });
      navSocorristas.addEventListener("click", function(){ openDrawer("socorristas"); });
      navInstalaciones.addEventListener("click", function(){ openDrawer("instalaciones"); });
      navAlertas.addEventListener("click", function(){ openDrawer("alertas"); });

      drawerClose.addEventListener("click", closeDrawer);
      backdrop.addEventListener("click", closeDrawer);
      drawerSearch.addEventListener("input", renderDrawer);

      sendBtn.addEventListener("click", sendMessage);

      messageInput.addEventListener("keydown", function(e){
        if(e.key === "Enter"){
          e.preventDefault();
          sendMessage();
        }
      });

      authBtn.addEventListener("click", login);

      authDni.addEventListener("keydown", function(e){
        if(e.key === "Enter"){
          e.preventDefault();
          login();
        }
      });

      logoutBtn.addEventListener("click", function(){
        clearSession();
        location.href = location.pathname;
      });

      initViewport();

      session = loadSession();

      if(!session || !session.dni){
        authLayer.classList.add("show");
      }else{
        authLayer.classList.remove("show");
        initChat();
      }

      setTimeout(setAppHeight, 100);
      setTimeout(setAppHeight, 500);
      setTimeout(setAppHeight, 1200);
    })();
  </script>
</div>
