<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Login UI (CSS)</title>
  <style>
    :root{
      --bgTop: #e06b6a;
      --bgMid: #b53a33;
      --bgDeep:#3b0707;

      --overlay1: rgba(120, 0, 0, .42);
      --overlay2: rgba(20, 0, 0, .55);

      --white: #ffffff;
      --ink: rgba(255,255,255,.92);
      --muted: rgba(255,255,255,.62);

      --pill: rgba(238, 245, 255, .92);
      --pill2: rgba(255,255,255,.86);

      --btn1:#ff4f4a;
      --btn2:#ff3a33;

      --shadow1: 0 22px 55px rgba(0,0,0,.55);
      --shadow2: 0 10px 22px rgba(0,0,0,.40);
      --inner: inset 0 1px 0 rgba(255,255,255,.22);
      --blur: 14px;
      --radius: 34px;
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      display:grid;
      place-items:center;
      background:
        radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,.18), transparent 60%),
        radial-gradient(900px 700px at 20% 120%, rgba(255,0,0,.12), transparent 60%),
        linear-gradient(180deg, #101018 0%, #07070b 100%);
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Helvetica Neue", sans-serif;
    }

    /* marco tipo “pantalla” */
    .phone{
      width:min(390px, 92vw);
      aspect-ratio: 9 / 19.5;
      border-radius: 42px;
      position:relative;
      padding: 14px;
      background: rgba(255,255,255,.06);
      box-shadow: 0 30px 90px rgba(0,0,0,.70);
      border: 1px solid rgba(255,255,255,.10);
      overflow:hidden;
    }
    .phone::before{
      content:"";
      position:absolute; inset:-2px;
      border-radius: 44px;
      background:
        radial-gradient(220px 160px at 35% 0%, rgba(255,255,255,.18), transparent 60%),
        linear-gradient(135deg, rgba(255,255,255,.10), rgba(255,255,255,0) 45%);
      pointer-events:none;
      mix-blend-mode: screen;
    }
    .phone::after{
      content:"";
      position:absolute; inset:0;
      border-radius: 42px;
      box-shadow: inset 0 0 0 1px rgba(0,0,0,.55);
      pointer-events:none;
    }

    .screen{
      height:100%;
      border-radius: 34px;
      overflow:hidden;
      position:relative;
      box-shadow: var(--shadow1);
      background:
        /* brillo superior */
        linear-gradient(180deg, rgba(255,255,255,.22) 0%, rgba(255,255,255,0) 22%),
        /* gradiente principal rojo */
        linear-gradient(180deg, var(--bgTop) 0%, var(--bgMid) 34%, #7b1b19 58%, var(--bgDeep) 100%);
    }

    /* “corte” diagonal oscuro como en la imagen */
    .screen::before{
      content:"";
      position:absolute; inset:-10%;
      background:
        linear-gradient(135deg,
          rgba(255,255,255,0) 0%,
          rgba(255,255,255,0) 32%,
          var(--overlay1) 32%,
          var(--overlay2) 66%,
          rgba(0,0,0,.0) 66%,
          rgba(0,0,0,.0) 100%);
      transform: rotate(-10deg);
      transform-origin:center;
      filter: blur(0.2px);
      opacity:.95;
      pointer-events:none;
    }

    /* viñeta + profundidad inferior */
    .screen::after{
      content:"";
      position:absolute; inset:0;
      background:
        radial-gradient(80% 70% at 50% 25%, rgba(255,255,255,.06), transparent 55%),
        radial-gradient(120% 90% at 50% 95%, rgba(0,0,0,.55), transparent 55%),
        linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,.65) 100%);
      pointer-events:none;
    }

    /* contenido centrado */
    .content{
      position:relative;
      height:100%;
      display:flex;
      flex-direction:column;
      align-items:center;
      padding: 54px 26px 34px;
      gap: 18px;
    }

    /* icono tipo “cuadro” */
    .app-icon{
      width: 56px; height: 42px;
      border-radius: 8px;
      background: rgba(255,255,255,.12);
      border: 1px solid rgba(255,255,255,.22);
      box-shadow: 0 10px 18px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.20);
      display:grid;
      place-items:center;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }
    .app-icon svg{
      width: 22px; height: 22px;
      opacity: .9;
      filter: drop-shadow(0 2px 2px rgba(0,0,0,.20));
    }

    h1{
      margin: 0;
      color: var(--ink);
      font-size: 44px;
      font-weight: 800;
      letter-spacing: .2px;
      text-shadow: 0 8px 18px rgba(0,0,0,.35);
    }

    .stack{
      width: 100%;
      max-width: 310px;
      margin-top: 10px;
      display:flex;
      flex-direction:column;
      gap: 16px;
      align-items:center;
    }

    /* inputs “pill” con sombra suave */
    .pill{
      width: 100%;
      height: 44px;
      border-radius: 999px;
      background:
        linear-gradient(180deg, var(--pill) 0%, var(--pill2) 100%);
      border: 1px solid rgba(255,255,255,.55);
      box-shadow:
        0 10px 18px rgba(0,0,0,.22),
        inset 0 1px 0 rgba(255,255,255,.55);
      display:flex;
      align-items:center;
      padding: 0 16px;
      backdrop-filter: blur(var(--blur));
      -webkit-backdrop-filter: blur(var(--blur));
    }
    .pill input{
      width:100%;
      border:0;
      outline:none;
      background:transparent;
      font-size: 14px;
      color: rgba(30,40,55,.92);
    }
    .pill input::placeholder{
      color: rgba(60,70,85,.55);
    }

    /* botón rojo “pill” con leve degradado y brillo */
    .btn{
      width: 100%;
      height: 52px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,.18);
      background:
        radial-gradient(120px 40px at 30% 25%, rgba(255,255,255,.26), transparent 60%),
        linear-gradient(180deg, var(--btn1) 0%, var(--btn2) 100%);
      box-shadow:
        0 18px 26px rgba(0,0,0,.28),
        inset 0 1px 0 rgba(255,255,255,.22);
      color: rgba(255,255,255,.92);
      font-weight: 700;
      letter-spacing: .2px;
      cursor:pointer;
      transform: translateZ(0);
      transition: transform .12s ease, filter .12s ease;
    }
    .btn:active{
      transform: scale(.985);
      filter: brightness(.98);
    }

    /* texto inferior */
    .small{
      margin-top: auto;
      font-size: 12px;
      color: rgba(255,255,255,.55);
      letter-spacing: .1px;
      text-shadow: 0 6px 14px rgba(0,0,0,.30);
      display:flex;
      gap: 10px;
      align-items:center;
      justify-content:center;
      width:100%;
      opacity:.95;
    }
    .small span:last-child{
      color: rgba(255,80,70,.75);
      font-weight: 700;
    }

    /* barra “status” minimal (solo estética) */
    .status{
      position:absolute;
      top: 10px; left: 0; right:0;
      display:flex;
      justify-content:space-between;
      padding: 0 16px;
      font-size: 11px;
      color: rgba(255,255,255,.55);
      pointer-events:none;
      mix-blend-mode: soft-light;
    }
    .dots{
      display:flex; gap:6px; align-items:center;
    }
    .dot{width:5px;height:5px;border-radius:999px;background:rgba(255,255,255,.55)}
    .bar{width:18px;height:5px;border-radius:999px;background:rgba(255,255,255,.45)}
  </style>
</head>

<body>
  <div class="phone" role="img" aria-label="Pantalla de login estilo rojo con corte diagonal">
    <div class="screen">
      <div class="status">
        <div class="dots">
          <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        </div>
        <div class="dots">
          <div class="bar"></div><div class="bar"></div>
        </div>
      </div>

      <div class="content">
        <div class="app-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M4 10.5L12 4l8 6.5v8.5a2 2 0 0 1-2 2h-4.5v-7H10.5v7H6a2 2 0 0 1-2-2v-8.5Z"
              fill="rgba(255,255,255,.92)"/>
          </svg>
        </div>

        <h1>Welcome</h1>

        <div class="stack">
          <div class="pill">
            <input type="text" placeholder="Username" autocomplete="username" />
          </div>
          <div class="pill">
            <input type="password" placeholder="Password" autocomplete="current-password" />
          </div>

          <button class="btn" type="button">Login to my account</button>
        </div>

        <div class="small">
          <span>Forgot password?</span><span>Click here</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
