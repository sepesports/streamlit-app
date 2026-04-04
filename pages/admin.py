# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES =====
PHONE_W_PX = 390
PHONE_H_PX = 844
PHONE_BORDER_PX = 3
PHONE_BORDER_COLOR = "#111111"
PHONE_BG = "#FFFFFF"
OUTSIDE_BG = "#EDEDED"

GRID_COLOR = "rgba(0,0,0,0.10)"
MID_COLOR = "rgba(0,0,0,0.25)"
BLOCK_BORDER = "2px dashed rgba(0,0,0,.55)"
BLOCK_BG = "rgba(0,0,0,.03)"
LABEL_BG = "rgba(255,255,255,.92)"

# BLOQUES MOBILE (0–100 dentro del área del teléfono)
# id, left, top, width, height
BLOCKS = [
    {"id": "SOCIAL_BAR",        "left": 4,   "top": 2,    "width": 28,  "height": 4.5},
    {"id": "LOGO",              "left": 32,  "top": 1.5,  "width": 36,  "height": 5.5},
    {"id": "BTN_LOGIN",         "left": 6,   "top": 8.5,  "width": 42,  "height": 5.5},
    {"id": "BTN_REGISTRATE",    "left": 52,  "top": 8.5,  "width": 42,  "height": 5.5},
    {"id": "BTN_JUGAR_AHORA",   "left": 6,   "top": 15.5, "width": 88,  "height": 6.0},

    {"id": "HERO_BANNER",       "left": 0,   "top": 23.0, "width": 100, "height": 22.0},
    {"id": "HERO_ARROW_L",      "left": 2,   "top": 31.5, "width": 8,   "height": 6.5},
    {"id": "HERO_ARROW_R",      "left": 90,  "top": 31.5, "width": 8,   "height": 6.5},
    {"id": "HERO_DOTS",         "left": 37,  "top": 43.0, "width": 26,  "height": 2.5},

    {"id": "MODE_CLASSIC",      "left": 6,   "top": 48.0, "width": 42,  "height": 6.5},
    {"id": "MODE_PPM",          "left": 52,  "top": 48.0, "width": 42,  "height": 6.5},
    {"id": "MODE_FANTASY",      "left": 6,   "top": 56.0, "width": 88,  "height": 6.5},

    {"id": "MATCH_01",          "left": 4,   "top": 65.5, "width": 44,  "height": 9.0},
    {"id": "MATCH_02",          "left": 52,  "top": 65.5, "width": 44,  "height": 9.0},
    {"id": "MATCH_03",          "left": 4,   "top": 76.0, "width": 44,  "height": 9.0},
    {"id": "MATCH_04",          "left": 52,  "top": 76.0, "width": 44,  "height": 9.0},
    {"id": "MATCH_05",          "left": 4,   "top": 86.5, "width": 44,  "height": 9.0},
    {"id": "MATCH_06",          "left": 52,  "top": 86.5, "width": 44,  "height": 9.0},

    {"id": "RETO_01",           "left": 4,   "top": 98.5, "width": 92,  "height": 11.0},
    {"id": "RETO_02",           "left": 4,   "top": 111.0,"width": 92,  "height": 11.0},
    {"id": "RETO_03",           "left": 4,   "top": 123.5,"width": 92,  "height": 11.0},
    {"id": "RETO_04",           "left": 4,   "top": 136.0,"width": 92,  "height": 11.0},
]
# ===================

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
      iframe{display:block !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

def blocks_to_html(blocks):
    out = []
    for b in blocks:
        out.append(
            f"""
            <div class="blk"
                 style="left:{b["left"]}%; top:{b["top"]}%;
                        width:{b["width"]}%; height:{b["height"]}%;">

              <span class="blk-label">{b["id"]}</span>
            </div>
            """
        )
    return "\n".join(out)

html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{{
      --phone-w:{PHONE_W_PX}px;
      --phone-h:{PHONE_H_PX}px;
      --phone-border:{PHONE_BORDER_PX}px;
      --phone-border-color:{PHONE_BORDER_COLOR};
      --phone-bg:{PHONE_BG};
      --outside-bg:{OUTSIDE_BG};
      --grid-color:{GRID_COLOR};
      --mid-color:{MID_COLOR};
      --block-border:{BLOCK_BORDER};
      --block-bg:{BLOCK_BG};
      --label-bg:{LABEL_BG};
    }}

    *{{box-sizing:border-box;}}
    html, body{{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--outside-bg);
      font-family:Arial, sans-serif;
    }}

    #stage{{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      background:var(--outside-bg);
    }}

    #phone{{
      position:relative;
      width:min(var(--phone-w), 96vw);
      height:min(var(--phone-h), 96vh);
      aspect-ratio:390 / 844;
      border:var(--phone-border) solid var(--phone-border-color);
      border-radius:28px;
      background:var(--phone-bg);
      overflow:auto;
      box-shadow:0 10px 35px rgba(0,0,0,.18);
    }}

    #screen{{
      position:relative;
      width:100%;
      height:148%;
      background:var(--phone-bg);
    }}

    #overlay{{
      position:absolute;
      inset:0;
      pointer-events:none;
    }}

    .grid{{
      position:absolute;
      inset:0;
      background-image:
        linear-gradient(to right, var(--grid-color) 1px, transparent 1px),
        linear-gradient(to bottom, var(--grid-color) 1px, transparent 1px);
      background-size:10% 10%;
    }}

    .mid-v{{
      position:absolute;
      left:50%;
      top:0;
      bottom:0;
      width:1px;
      background:var(--mid-color);
    }}

    .mid-h{{
      position:absolute;
      top:50%;
      left:0;
      right:0;
      height:1px;
      background:var(--mid-color);
    }}

    .blk{{
      position:absolute;
      border:var(--block-border);
      background:var(--block-bg);
    }}

    .blk-label{{
      position:absolute;
      top:2px;
      left:2px;
      font:11px Arial, sans-serif;
      background:var(--label-bg);
      border:1px solid rgba(0,0,0,.15);
      border-radius:4px;
      padding:2px 6px;
      white-space:nowrap;
    }}

    #hud{{
      position:sticky;
      top:8px;
      left:8px;
      margin:8px;
      width:max-content;
      font:12px Arial, sans-serif;
      background:rgba(255,255,255,.95);
      border:1px solid rgba(0,0,0,.2);
      border-radius:6px;
      padding:6px 10px;
      z-index:3;
      pointer-events:none;
    }}
  </style>
</head>
<body>
  <div id="stage">
    <div id="phone">
      <div id="screen">
        <div id="overlay">
          <div class="grid"></div>
          <div class="mid-v"></div>
          <div class="mid-h"></div>
          {blocks_to_html(BLOCKS)}
        </div>
        <div id="hud">Cargando...</div>
      </div>
    </div>
  </div>

  <script>
    (function(){{
      var hud = document.getElementById("hud");
      var phone = document.getElementById("phone");
      var screen = document.getElementById("screen");

      function update(){{
        var pw = Math.round(phone.clientWidth);
        var ph = Math.round(phone.clientHeight);
        var sh = Math.round(screen.clientHeight);

        hud.textContent =
          "Phone(px): " + pw + " x " + ph +
          " | Alto plano: " + sh +
          " | 10% ancho=" + Math.round(pw * 0.10) + "px" +
          " | 10% alto plano=" + Math.round(sh * 0.10) + "px";
      }}

      window.addEventListener("resize", update);
      update();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=960, scrolling=False)
