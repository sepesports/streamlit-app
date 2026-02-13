# app.py
import streamlit as st
import streamlit.components.v1 as components

# 🔒 GATE: solo entra con ?auth=ok
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

# ===================== BASE (NO CAMBIAR ESTRUCTURA) =====================

PAD_X_PX = 8
PAD_TOP_PX = 8

BORDER_PX = 1
BORDER_COLOR = "rgba(255,255,255,.12)"

BG_COLOR = "#020a1a" 
HEADER_BG = "transparent"
IMG_BG = "transparent"
BTN_BG = "transparent"
FOOTER_BG = "transparent"

IMG_LEFT = 0
IMG_RIGHT = 0
IMG_TOP = 10
IMG_HEIGHT = 44

HEADER_TOP = 0
HEADER_HEIGHT = 10

BTN_AREA_TOP = 55
BTN_H = 23
BTN_GAP_X = 2
BTN_GAP_Y = 2
BTN_LEFT = 5
BTN_RIGHT = 5

BTN_TEXTS = [
    "Horarios",
    "Control de\nAsistencia",
    "Nomina y\nPagos",
    "Incidencias",
    "Formación",
    "Comunicados",
]

FOOTER_H = 18
FOOTER_BOTTOM = 5
FOOTER_LEFT = 6
FOOTER_RIGHT = 6

MIN_BTN_W_PX = 130
MOBILE_MAX_W_PX = 500

# ===================== CONTENIDO =====================

LOGO_URL = "https://files.catbox.moe/056m6v.jpg"
FOOTER_TEXT = "2026 Socorrista ProVersión 1.0. Todos los derechos reservados"

# nombre del usuario (prioriza ?usuario=..., si no existe usa ?user=..., si no existe deja "Login")
USER_NAME = st.query_params.get("usuario") or st.query_params.get("user") or "Login"

# ===================== AJUSTES EDITABLES (DESKTOP / MÓVIL) =====================
# (solo cambia estilo, NO mueve estructura)

# Tipografías generales
HERO_FONT_SIZE_DESKTOP_PX = 44
HERO_FONT_SIZE_MOBILE_PX = 13

HEADER_FONT_SIZE_DESKTOP_PX = 40
HEADER_FONT_SIZE_MOBILE_PX = 23

BTN_FONT_SIZE_DESKTOP_PX = 17
BTN_FONT_SIZE_MOBILE_PX = 17

FOOTER_FONT_SIZE_DESKTOP_PX = 13
FOOTER_FONT_SIZE_MOBILE_PX = 13

# Tamaño de texto por botón (índice 0..5) — opcional
BTN_FONT_OVERRIDES_DESKTOP_PX = {
    # 0: 17,  # Horarios
    # 1: 17,  # Control de Asistencia
    # 2: 17,  # Nomina y Pagos
    # 3: 17,  # Incidencias
    # 4: 17,  # Formación
    # 5: 17,  # Comunicados 17
}
BTN_FONT_OVERRIDES_MOBILE_PX = {
    # 0: 14,
    # 1: 14,
    # 2: 14,
    # 3: 14,
    # 4: 14,
    # 5: 14,
}

# Logo (ocupa TODA la caja)
LOGO_PADDING_PX_DESKTOP = 0
LOGO_PADDING_PX_MOBILE = 0
LOGO_BORDER_RADIUS_PX = 0
LOGO_OBJECT_FIT = "cover"  # cover / contain
LOGO_BORDER = "0px solid rgba(255,255,255,.0)"

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{
      --padx: __PADX__px;
      --padtop: __PADTOP__px;

      --b: __B__px;
      --bc: __BC__;

      --bg: __BG__;
      --headerbg: __HEADERBG__;
      --imgbg: __IMGBG__;
      --btnbg: __BTNBG__;
      --footerbg: __FOOTERBG__;

      --txt: #eaf2ff;
      --txt2: rgba(234,242,255,.85);

      --shadow0: 0 18px 40px rgba(0,0,0,.60);
      --shadow1: 0 12px 26px rgba(0,0,0,.55);
      --shadow2: 0 10px 18px rgba(0,0,0,.45);

      /* EDITABLES (desktop) */
      --heroFs: __HERO_FS_D__px;
      --hdrFs: __HDR_FS_D__px;
      --btnFs: __BTN_FS_D__px;
      --footFs: __FOOT_FS_D__px;

      --logoPad: __LOGO_PAD_D__px;
      --logoRad: __LOGO_RAD__px;
    }

    html, body{
      margin:0;padding:0;width:100%;height:100%;
      overflow:hidden;
      background: var(--bg);
      font-family: "Segoe UI", Arial, Helvetica, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    #stage{
      position:fixed;inset:0;width:100vw;height:100vh;
      background:
        radial-gradient(1200px 700px at 50% 18%, rgba(40,130,255,.22) 0%, rgba(8,35,95,.15) 35%, rgba(2,10,26,0) 70%),
        linear-gradient(180deg, #03102a 0%, #FFFFFF 70%, #010612 100%);
    }

    /* marco (no cambia estructura) */
    #frame{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      border-left:var(--b) solid var(--bc);
      border-right:var(--b) solid var(--bc);
      border-top:var(--b) solid var(--bc);
      box-sizing:border-box;
      pointer-events:none;
      background: transparent;
      box-shadow: inset 0 0 0 1px rgba(0,0,0,.35);
    }

    #plan{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      overflow:hidden;
    }

    /* ================= HEADER ================= */
    #hdr{
      position:absolute;
      left:0; right:0;
      top: __HDR_TOP__%;
      height: __HDR_H__%;
      border: var(--b) solid var(--bc);
      box-sizing:border-box;
      display:flex;
      gap:0;
      overflow:hidden;
      box-shadow: var(--shadow2);
      border-radius: 0;
      background:
        linear-gradient(180deg, rgba(22,48,110,.82) 0%, rgba(7,22,62,.86) 58%, rgba(2,10,26,.92) 100%);
    }

    .hdr-cell{
      border-right: var(--b) solid rgba(255,255,255,.10);
      box-sizing:border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size: var(--hdrFs);
      font-weight: 700;
      color: var(--txt2);
      white-space: nowrap;
      overflow:hidden;
      text-overflow: ellipsis;
      background: transparent;
      text-shadow: 0 2px 10px rgba(0,0,0,.55);
      padding: 0 10px;
    }
    .hdr-cell.white{
      background:
        linear-gradient(180deg, rgba(255,255,255,.12) 0%, rgba(255,255,255,.07) 55%, rgba(255,255,255,.05) 100%);
      color: var(--txt);
      border-left: 1px solid rgba(255,255,255,.06);
      border-right: 1px solid rgba(255,255,255,.06);
    }
    .hdr-cell:last-child{ border-right: none; }

    /* Logo: ocupa toda la caja asignada */
    .hdr-logo{
      padding: var(--logoPad) !important;
    }
    .hdr-logo img{
      width: 100%;
      height: 100%;
      display:block;
      object-fit: __LOGO_FIT__;
      border-radius: var(--logoRad);
      border: __LOGO_BORDER__;
      background: rgba(0,0,0,.10);
    }

    /* ================= HERO (img) ================= */
    #img{
      position:absolute;
      left: __IMG_L__%;
      right: __IMG_R__%;
      top: __IMG_T__%;
      height: __IMG_H__%;
      border: 1px solid rgba(255,255,255,.10);
      box-sizing:border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size: var(--heroFs);
      font-weight: 800;
      letter-spacing: 1px;
      color: var(--txt);
      text-transform: uppercase;
      text-shadow: 0 2px 0 rgba(0,0,0,.20), 0 10px 28px rgba(0,0,0,.55);
      border-radius: 14px;
      box-shadow: var(--shadow0);
      overflow:hidden;

      background:
        radial-gradient(900px 220px at 50% 35%, rgba(100,190,255,.28) 0%, rgba(35,120,255,.14) 32%, rgba(2,10,26,0) 68%),
        linear-gradient(135deg, rgba(10,40,105,.88) 0%, rgba(5,22,64,.90) 52%, rgba(2,10,26,.94) 100%);
    }

    #img::before{
      content:"";
      position:absolute;
      inset:-40px -60px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,0) 40%),
        radial-gradient(600px 240px at 30% 50%, rgba(120,210,255,.14) 0%, rgba(120,210,255,0) 70%),
        radial-gradient(700px 260px at 70% 60%, rgba(60,140,255,.10) 0%, rgba(60,140,255,0) 70%);
      opacity:.9;
      pointer-events:none;
    }

    #img::after{
      content:"";
      position:absolute;
      left:-18%;
      right:-18%;
      bottom:-40%;
      height:120%;
      background:
        radial-gradient(closest-side at 50% 50%, rgba(140,220,255,.18), rgba(140,220,255,0) 65%),
        linear-gradient(90deg, rgba(120,210,255,.22), rgba(120,210,255,0) 55%, rgba(120,210,255,.18));
      transform:skewY(-6deg);
      opacity:.75;
      pointer-events:none;
    }

    /* ================= BUTTON AREA ================= */
    #btn-area{
      position:absolute;
      left:0; right:0;
      top: __BTN_AREA_TOP__%;
      bottom: 0;
      background: transparent;
      box-sizing:border-box;
    }

    #btn-grid{
      position:absolute;
      left: __BTN_L__%;
      right: __BTN_R__%;
      top: 0;
      bottom: 0;
    }

    .btn{
      position:absolute;
      border: 1px solid rgba(255,255,255,.12);
      box-sizing:border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      padding: 8px 10px;
      font-size: var(--btnFs);
      font-weight: 700;
      color: var(--txt);
      overflow:hidden;
      border-radius: 12px;
      box-shadow: var(--shadow1);
      background:
        radial-gradient(220px 80px at 24% 50%, rgba(120,210,255,.24) 0%, rgba(120,210,255,0) 68%),
        linear-gradient(180deg, rgba(18,78,185,.44) 0%, rgba(8,42,110,.58) 55%, rgba(4,24,66,.78) 100%);
      transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, filter .12s ease;
      cursor:pointer;
      user-select:none;
    }

    .btn::before{
      content:"";
      position:absolute;
      inset:0;
      border-radius:12px;
      background: linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,0) 45%);
      opacity:.85;
      pointer-events:none;
    }

    .btn:hover{
      transform: translateY(-2px);
      box-shadow: 0 16px 34px rgba(0,0,0,.62);
      border-color: rgba(170,230,255,.22);
      filter: saturate(1.06);
    }

    .btn:active{
      transform: translateY(0px);
      box-shadow: var(--shadow1);
    }

    .btn span{
      position:relative;
      display:block;
      line-height:1.05;
      white-space: pre-line;
      text-shadow: 0 1px 0 rgba(0,0,0,.25);
    }

    /* Footer */
    #footer{
      position:absolute;
      left: __FOOT_L__%;
      right: __FOOT_R__%;
      height: __FOOT_H__%;
      bottom: __FOOT_BOTTOM__%;
      border: 1px solid rgba(255,255,255,.10);
      box-sizing:border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size: var(--footFs);
      font-weight: 700;
      color: rgba(234,242,255,.72);
      border-radius: 12px;
      box-shadow: var(--shadow2);
      background:
        linear-gradient(180deg, rgba(22,48,110,.60) 0%, rgba(7,22,62,.78) 58%, rgba(2,10,26,.88) 100%);
      padding: 0 14px;
      text-align:center;
    }

    /* ==== EDITABLES (mobile) ==== */
    @media (max-width: 520px){
      :root{
        --heroFs: __HERO_FS_M__px;
        --hdrFs: __HDR_FS_M__px;
        --btnFs: __BTN_FS_M__px;
        --footFs: __FOOT_FS_M__px;
        --logoPad: __LOGO_PAD_M__px;
      }
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="plan">
      <div id="hdr"></div>
      <div id="img">¡BIENVENIDO!</div>

      <div id="btn-area">
        <div id="btn-grid"></div>
        <div id="footer">__FOOTER_TEXT__</div>
      </div>
    </div>
  </div>

  <script>
    (function(){
      var fe = window.frameElement;
      if (fe){
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

      var BTN_TEXTS = __BTN_TEXTS__;
      var MIN_BTN_W_PX = __MIN_BTN_W_PX__;
      var MOBILE_MAX_W_PX = __MOBILE_MAX_W_PX__;
      var LOGO_URL = "__LOGO_URL__";
      var USER_NAME = "__USER_NAME__";

      var BTN_OVR_D = __BTN_OVR_D__;
      var BTN_OVR_M = __BTN_OVR_M__;

      var hdr = document.getElementById("hdr");
      hdr.innerHTML = "";
      var cells = [
        {w: 6,  t:"",        white:false, kind:"blank"},
        {w: 22, t:"",        white:true,  kind:"logo"},
        {w: 44, t:"Fondo 1", white:false, kind:"text"},
        {w: 22, t:"",        white:true,  kind:"user"},
        {w: 6,  t:"",        white:false, kind:"blank"},
      ];

      cells.forEach(function(c){
        var d = document.createElement("div");
        d.className = "hdr-cell" + (c.white ? " white" : "");
        d.style.width = c.w + "%";

        if (c.kind === "logo"){
          d.className += " hdr-logo";
          var img = document.createElement("img");
          img.src = LOGO_URL;
          img.alt = "Logo";
          img.loading = "eager";
          img.decoding = "async";
          d.appendChild(img);
        } else if (c.kind === "user"){
          d.textContent = USER_NAME || "";
        } else {
          d.textContent = c.t;
        }

        hdr.appendChild(d);
      });

      var grid = document.getElementById("btn-grid");
      var plan = document.getElementById("plan");

      function ceilDiv(a,b){ return Math.floor((a + b - 1) / b); }

      function overrideFs(i){
        var vw = window.innerWidth;
        if (vw <= 520){
          if (BTN_OVR_M && BTN_OVR_M[i] != null) return BTN_OVR_M[i];
          return null;
        } else {
          if (BTN_OVR_D && BTN_OVR_D[i] != null) return BTN_OVR_D[i];
          return null;
        }
      }

      function buildButtons(){
        grid.innerHTML = "";

        var vw = window.innerWidth;
        var r = plan.getBoundingClientRect();
        var planW = r.width;

        var left = __BTN_L__;
        var right = __BTN_R__;
        var gapX = __BTN_GAP_X__;
        var gapY = __BTN_GAP_Y__;
        var btnH = __BTN_H__;

        if (vw <= MOBILE_MAX_W_PX){
          if (gapX < 2) gapX = 2;
          if (gapY < 3) gapY = 3;
        }

        var count = BTN_TEXTS.length;

        var cols = 3;
        var usable = 100 - left - right;

        while (cols > 1){
          var wPctTry = (usable - (gapX * (cols - 1))) / cols;
          var wPxTry = (wPctTry / 100) * planW;
          if (wPctTry > 0 && wPxTry >= MIN_BTN_W_PX) break;
          cols -= 1;
        }

        var rows = ceilDiv(count, cols);
        var w = (usable - (gapX * (cols - 1))) / cols;
        if (w < 0) w = 0;

        for (var i=0;i<count;i++){
          var row = Math.floor(i/cols);
          var col = i%cols;

          var x = left + col*(w + gapX);
          var y = row*(btnH + gapY);

          var d = document.createElement("div");
          d.className = "btn";
          d.style.left = x + "%";
          d.style.top = y + "%";
          d.style.width = w + "%";
          d.style.height = btnH + "%";

          var sp = document.createElement("span");
          sp.textContent = BTN_TEXTS[i];

          var fs = overrideFs(i);
          if (fs != null) sp.style.fontSize = fs + "px";

          d.appendChild(sp);
          grid.appendChild(d);
        }
      }

      function update(){ buildButtons(); }
      window.addEventListener("resize", update);
      update();
    })();
  </script>
</body>
</html>
"""

def _dict_to_js_obj(d: dict) -> str:
    # {0:15,1:14} -> {"0":15,"1":14} (usable como objeto en JS)
    parts = []
    for k, v in d.items():
        try:
            ik = int(k)
            fv = float(v)
        except Exception:
            continue
        if fv <= 0:
            continue
        parts.append(f'"{ik}":{fv}')
    return "{" + ",".join(parts) + "}"

html = (
    html.replace("__PADX__", str(PAD_X_PX))
        .replace("__PADTOP__", str(PAD_TOP_PX))
        .replace("__B__", str(BORDER_PX))
        .replace("__BC__", BORDER_COLOR)
        .replace("__BG__", BG_COLOR)
        .replace("__HEADERBG__", HEADER_BG)
        .replace("__IMGBG__", IMG_BG)
        .replace("__BTNBG__", BTN_BG)
        .replace("__FOOTERBG__", FOOTER_BG)
        .replace("__HDR_TOP__", str(HEADER_TOP))
        .replace("__HDR_H__", str(HEADER_HEIGHT))
        .replace("__IMG_L__", str(IMG_LEFT))
        .replace("__IMG_R__", str(IMG_RIGHT))
        .replace("__IMG_T__", str(IMG_TOP))
        .replace("__IMG_H__", str(IMG_HEIGHT))
        .replace("__BTN_AREA_TOP__", str(BTN_AREA_TOP))
        .replace("__BTN_L__", str(BTN_LEFT))
        .replace("__BTN_R__", str(BTN_RIGHT))
        .replace("__BTN_H__", str(BTN_H))
        .replace("__BTN_GAP_X__", str(BTN_GAP_X))
        .replace("__BTN_GAP_Y__", str(BTN_GAP_Y))
        .replace("__FOOT_L__", str(FOOTER_LEFT))
        .replace("__FOOT_R__", str(FOOTER_RIGHT))
        .replace("__FOOT_H__", str(FOOTER_H))
        .replace("__FOOT_BOTTOM__", str(FOOTER_BOTTOM))
        .replace("__BTN_TEXTS__", str(BTN_TEXTS).replace("'", '"'))
        .replace("__MIN_BTN_W_PX__", str(MIN_BTN_W_PX))
        .replace("__MOBILE_MAX_W_PX__", str(MOBILE_MAX_W_PX))
        .replace("__LOGO_URL__", LOGO_URL)
        .replace("__USER_NAME__", str(USER_NAME).replace('"', '\\"'))
        .replace("__FOOTER_TEXT__", FOOTER_TEXT)
        .replace("__HERO_FS_D__", str(HERO_FONT_SIZE_DESKTOP_PX))
        .replace("__HERO_FS_M__", str(HERO_FONT_SIZE_MOBILE_PX))
        .replace("__HDR_FS_D__", str(HEADER_FONT_SIZE_DESKTOP_PX))
        .replace("__HDR_FS_M__", str(HEADER_FONT_SIZE_MOBILE_PX))
        .replace("__BTN_FS_D__", str(BTN_FONT_SIZE_DESKTOP_PX))
        .replace("__BTN_FS_M__", str(BTN_FONT_SIZE_MOBILE_PX))
        .replace("__FOOT_FS_D__", str(FOOTER_FONT_SIZE_DESKTOP_PX))
        .replace("__FOOT_FS_M__", str(FOOTER_FONT_SIZE_MOBILE_PX))
        .replace("__LOGO_PAD_D__", str(LOGO_PADDING_PX_DESKTOP))
        .replace("__LOGO_PAD_M__", str(LOGO_PADDING_PX_MOBILE))
        .replace("__LOGO_RAD__", str(LOGO_BORDER_RADIUS_PX))
        .replace("__LOGO_FIT__", LOGO_OBJECT_FIT)
        .replace("__LOGO_BORDER__", LOGO_BORDER)
        .replace("__BTN_OVR_D__", _dict_to_js_obj(BTN_FONT_OVERRIDES_DESKTOP_PX))
        .replace("__BTN_OVR_M__", _dict_to_js_obj(BTN_FONT_OVERRIDES_MOBILE_PX))
)

components.html(html, height=10, scrolling=False)
