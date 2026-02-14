# app.py
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# PLANTILLA "CALENDARIO" — BLANCO Y NEGRO (RESPONSIVA)
# ==============================================================================

# ================== AJUSTES (EDITA SOLO ESTO) ==================

# 1) CUADRO / MARCO (px)
PAD_X_PX = 10
PAD_TOP_PX = 10

# 2) ESTILO BN
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"
PANEL_BG = "#F6F6F6"
CARD_BG = "#FFFFFF"
TEXT_COLOR = "#111111"
MUTED_TEXT = "#5A5A5A"

# 3) TIPOGRAFÍA (px)
FONT_BASE_PX = 14
TITLE_PX = 18
H2_PX = 16
SMALL_PX = 12

# 4) LAYOUT VERTICAL (en % del CUADRO)
TOPBAR_H = 8
MONTHBAR_H = 10
CAL_GRID_H = 24
FILTERS_H = 9
AGENDA_H = 34
BOTTOMBAR_H = 10

# 5) MÁRGENES INTERNOS (en % del CUADRO)
INNER_L = 4
INNER_R = 4
INNER_TOP_GAP = 0.7   # ↓ reduce espacios entre CALENDARIO / FILTROS / AGENDA / BOTTOM

# 6) CALENDARIO
CAL_COLS = 7
CAL_ROWS = 3
DAY_CELL_GAP_PX = 8

# 7) AGENDA
AGENDA_ROWS = 5

# ===============================================================

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0!important;margin:0!important;max-width:100%!important;}
      section.main > div{padding:0!important;margin:0!important;}
      header, footer{display:none!important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = r"""
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
    --panel: __PANEL__;
    --card: __CARD__;
    --txt: __TXT__;
    --muted: __MUTED__;

    --fbase: __FBASE__px;
    --title: __TITLE__px;
    --h2: __H2__px;
    --small: __SMALL__px;

    --innerL: __INNERL__%;
    --innerR: __INNERR__%;
    --gapY: __GAPY__%;

    --topbarH: __TOPBARH__%;
    --monthbarH: __MONTHBARH__%;
    --calgridH: __CALGRIDH__%;
    --filtersH: __FILTERSH__%;
    --agendaH: __AGENDAH__%;
    --bottombarH: __BOTTOMH__%;

    --cellGap: __CELLGAP__px;
  }

  html, body{
    margin:0; padding:0;
    width:100%; height:100%;
    background: var(--bg);
    overflow:hidden;
    font-family: Arial, sans-serif;
    color: var(--txt);
  }

  #stage{position:fixed; inset:0; background: var(--bg);}

  /* Marco (izq/der/sup) */
  #frame{
    position:absolute;
    left:var(--padx); right:var(--padx);
    top:var(--padtop); bottom:0;
    border-left:var(--b) solid var(--bc);
    border-right:var(--b) solid var(--bc);
    border-top:var(--b) solid var(--bc);
    box-sizing:border-box;
    pointer-events:none;
  }

  /* CUADRO */
  #plan{
    position:absolute;
    left:var(--padx); right:var(--padx);
    top:var(--padtop); bottom:0;
    overflow:hidden;
    background: var(--bg);
  }

  #wrap{
    position:absolute;
    left: var(--innerL);
    right: var(--innerR);
    top: 1.4%;
    bottom: 1.2%;
    display:flex;
    flex-direction:column;
  }

  .panel{
    background: var(--panel);
    border: var(--b) solid var(--bc);
    border-radius: 14px;
    box-sizing:border-box;
  }
  .btn{
    background: var(--card);
    border: var(--b) solid var(--bc);
    border-radius: 10px;
    box-sizing:border-box;
    padding: 10px 14px;
    font-weight: 700;
    font-size: var(--fbase);
    color: var(--txt);
    display:flex;
    align-items:center;
    justify-content:center;
    min-width: 92px;
    white-space:nowrap;
  }
  .btn.primary{
    background: var(--txt);
    color: var(--bg);
  }
  .chip{
    border: var(--b) solid var(--bc);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: var(--small);
    font-weight: 800;
    background: var(--card);
    color: var(--txt);
    display:inline-flex;
    align-items:center;
    gap:8px;
    white-space:nowrap;
  }
  .iconbtn{
    width:36px;height:36px;
    border: var(--b) solid var(--bc);
    border-radius: 10px;
    background: var(--card);
    display:flex;align-items:center;justify-content:center;
    font-weight: 900;
    user-select:none;
  }
  .muted{color: var(--muted);}

  /* TOPBAR */
  #topbar{
    height: var(--topbarH);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
  }
  #topbar .center{
    flex: 1;
    text-align:center;
    font-weight: 900;
    font-size: var(--h2);
  }
  #topbar .right{
    display:flex;
    align-items:center;
    gap:10px;
    font-weight:800;
  }

  /* MONTHBAR */
  #monthbar{
    height: var(--monthbarH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 10px;
  }
  #monthbar .month{
    font-weight: 900;
    font-size: var(--title);
    letter-spacing: 1px;
    flex:1;
    text-align:left;
  }
  #monthbar .nav{display:flex; gap:10px; align-items:center;}

  /* CAL GRID */
  #calgrid{
    height: var(--calgridH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    flex-direction:column;
    gap: 10px;
  }
  #calgrid .head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
  }
  #calgrid .head .label{
    font-weight: 900;
    font-size: var(--fbase);
  }
  #calgrid .days{
    display:grid;
    grid-template-columns: repeat(__CALCOLS__, 1fr);
    grid-template-rows: repeat(__CALROWS__, 1fr);
    gap: var(--cellGap);
    flex:1;
    min-height: 0;
  }
  .day{
    background: var(--card);
    border: var(--b) solid var(--bc);
    border-radius: 10px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight: 900;
    user-select:none;
    position:relative;
    min-height: 34px;
  }
  .day.dim{opacity:.35;}
  .day.sel{outline: 2px solid var(--txt); outline-offset: -2px;}
  .day.mark::after{
    content:"";
    position:absolute;
    bottom:6px;
    width:7px;height:7px;
    border-radius:50%;
    background: var(--txt);
    opacity:.9;
  }

  #legend{
    display:flex;
    align-items:center;
    gap:14px;
    font-size: var(--small);
    font-weight: 800;
    color: var(--muted);
    margin-top: 2px;
  }
  .dot{width:8px;height:8px;border-radius:50%;background:var(--txt);display:inline-block;margin-right:6px;opacity:.35;}
  .dot.on{opacity:1;}
  .dot.mid{opacity:.65;}

  /* FILTERS */
  #filters{
    height: var(--filtersH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:flex-end;
    gap: 12px;
    overflow:hidden; /* nada puede quedar por fuera */
  }
  .select{
    min-width: 160px;
    padding: 10px 12px;
    background: var(--card);
    border: var(--b) solid var(--bc);
    border-radius: 10px;
    font-weight: 800;
    color: var(--txt);
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 10px;
    box-sizing:border-box;
    white-space:nowrap;
  }
  .caret{font-weight:900;}

  /* AGENDA */
  #agenda{
    height: var(--agendaH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    flex-direction:column;
    gap: 10px;
    min-height: 0;
  }
  #agenda h3{
    margin:0;
    font-size: var(--h2);
    font-weight: 900;
  }
  #agenda .meta{
    display:flex;
    gap: 18px;
    font-size: var(--small);
    font-weight: 800;
    color: var(--muted);
    flex-wrap:wrap;
  }

  #table{
    flex:1;
    background: var(--card);
    border: var(--b) solid var(--bc);
    border-radius: 12px;
    overflow:hidden;
    display:flex;
    flex-direction:column;
    min-height: 0;
  }

  #thead, .trow{
    display:grid;
    grid-template-columns: 30px 1fr 110px 110px 110px;
    gap: 10px;
    align-items:center;
    padding: 10px 10px;
    box-sizing:border-box;
  }
  #thead{
    background: #EFEFEF;
    font-weight: 900;
    font-size: var(--small);
  }
  .trow{
    border-top: 1px solid rgba(0,0,0,.12);
    font-weight: 800;
    font-size: var(--small);
  }
  .chk{
    width:18px;height:18px;
    border: var(--b) solid var(--bc);
    border-radius: 4px;
    background: var(--card);
  }
  .status{
    justify-self:end;
    padding: 5px 10px;
    border-radius: 999px;
    border: var(--b) solid var(--bc);
    font-weight: 900;
    font-size: 11px;
    background: var(--card);
    white-space:nowrap;
  }
  .status.free{background:#FFFFFF;}
  .status.busy{background:#EFEFEF;}

  .rowmeta{
    display:none; /* desktop off */
    margin-top: 4px;
    font-size: 11px;
    color: var(--muted);
    font-weight: 800;
    gap: 10px;
  }

  /* BOTTOM BAR */
  #bottom{
    height: var(--bottombarH);
    margin-top: var(--gapY);
    padding: 10px 12px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 12px;
  }
  #bottom .leftinfo{
    display:flex;
    align-items:center;
    gap: 12px;
    font-size: var(--small);
    font-weight: 900;
    color: var(--muted);
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
    min-width: 0;
  }
  #bottom .actions{
    display:flex;
    gap: 10px;
    align-items:center;
    flex-shrink:0;
  }

  /* ===== MOBILE (crítico: nada se sale / tabla completa) ===== */
  @media (max-width: 520px){

    /* FILTROS: 2 columnas + botón abajo (todo dentro) */
    #filters{
      height: auto;
      display:grid;
      grid-template-columns: 1fr 1fr;
      grid-auto-rows: min-content;
      gap: 10px;
      justify-content: stretch;
      align-items: stretch;
    }
    #filters .select{
      min-width: 0;
      width: 100%;
    }
    #filters .btn{
      grid-column: 1 / -1;
      width: 100%;
      min-width: 0;
    }

    /* TABLA: compacta (no recorta) */
    #thead{
      display:none;
    }
    .trow{
      grid-template-columns: 26px 1fr;
      grid-auto-rows: min-content;
      gap: 10px;
      align-items:start;
    }
    .trow > .col_time,
    .trow > .col_time2,
    .trow > .col_status{
      display:none; /* oculta columnas separadas */
    }
    .rowmeta{
      display:flex; /* muestra meta dentro del nombre */
      flex-wrap:wrap;
      align-items:center;
    }
    .rowmeta .pill{
      border: 1px solid rgba(0,0,0,.18);
      border-radius: 999px;
      padding: 3px 8px;
      background: #f3f3f3;
      font-weight: 900;
      color: #111;
      white-space:nowrap;
    }

    /* BOTTOM: que no se salga */
    #bottom{
      height:auto;
      flex-direction:column;
      align-items:stretch;
      gap: 10px;
    }
    #bottom .leftinfo{
      justify-content:space-between;
    }
    #bottom .actions{
      width:100%;
      justify-content:space-between;
    }
    #bottom .actions .btn{
      flex:1;
      min-width: 0;
    }

    #monthbar .month{font-size: 16px;}
  }
</style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="plan">
      <div id="wrap">

        <div id="topbar" class="panel">
          <div class="iconbtn">□</div>
          <div class="center">Calendario</div>
          <div class="right">
            <div>Jefe</div>
            <div class="iconbtn">⌁</div>
            <div class="iconbtn">⋮</div>
          </div>
        </div>

        <div id="monthbar" class="panel">
          <div class="nav"><div class="iconbtn">‹</div></div>
          <div class="month">FEBRERO 2026</div>
          <div class="nav"><div class="iconbtn">›</div></div>
        </div>

        <div id="calgrid" class="panel">
          <div class="head">
            <div class="label">CALENDARIO</div>
            <div class="muted" style="font-weight:900;font-size:var(--small);">MO TU WE TH FR SA SU</div>
          </div>

          <div class="days" id="days"></div>

          <div id="legend">
            <span><i class="dot on"></i>LIBRE</span>
            <span><i class="dot mid"></i>OCUPADO</span>
            <span><i class="dot"></i>OTRO</span>
          </div>
        </div>

        <div id="filters" class="panel">
          <div class="select">Mes <span class="caret">▾</span></div>
          <div class="select">Año <span class="caret">▾</span></div>
          <div class="btn primary">Aplicar</div>
        </div>

        <div id="agenda" class="panel">
          <h3>Agenda del día</h3>
          <div class="meta">
            <div><b>Fecha:</b> 15 febrero 2026</div>
            <div><b>Inicio</b></div>
            <div><b>Finaliza</b></div>
            <div><b>Estado</b></div>
          </div>

          <div id="table">
            <div id="thead">
              <div></div><div></div><div>Inicio</div><div>Finaliza</div><div>Estado</div>
            </div>
            <div id="tbody"></div>
          </div>
        </div>

        <div id="bottom" class="panel">
          <div class="leftinfo">
            <span class="chip">2026-02-15 · Rocafort · 09:00:00 → 15:00:00</span>
            <span class="status free">LIBRE</span>
          </div>
          <div class="actions">
            <div class="btn">Aplicar</div>
            <div class="btn">Modificar</div>
            <div class="btn primary">Enviar</div>
          </div>
        </div>

      </div>
    </div>
  </div>

<script>
(function(){
  // Grilla calendario
  var daysEl = document.getElementById("days");
  var COLS = __CALCOLS__;
  var ROWS = __CALROWS__;
  var total = COLS * ROWS;

  var values = [
    {n:10, dim:true},{n:2},{n:3, sel:true},{n:4},{n:5},{n:6},{n:7},
    {n:11},{n:12},{n:13},{n:14, mark:true},{n:16, sel:true},{n:17},{n:14, mark:true},
    {n:21},{n:22},{n:23},{n:24},{n:25},{n:26},{n:28, mark:true}
  ];

  for (var i=0;i<total;i++){
    var v = values[i] || {n:""};
    var d = document.createElement("div");
    d.className = "day";
    if (v.dim) d.classList.add("dim");
    if (v.sel) d.classList.add("sel");
    if (v.mark) d.classList.add("mark");
    d.textContent = v.n;
    daysEl.appendChild(d);
  }

  // Tabla agenda (con meta embebida para móvil)
  var tbody = document.getElementById("tbody");
  var rows = [
    {name:"Rocafort", ini:"09:00:00", fin:"15:00:00", st:"LIBRE", cls:"free", chk:false},
    {name:"Cn Fabra", ini:"09:00:00", fin:"06:00:00", st:"OCUPADO", cls:"busy", chk:true},
    {name:"Arsenal",  ini:"08:00:00", fin:"12:00:00", st:"OCUPADO", cls:"busy", chk:true},
    {name:"Arsenal",  ini:"15:00:00", fin:"18:00:00", st:"LIBRE", cls:"free", chk:false},
    {name:"St. Jordi",ini:"", fin:"", st:"", cls:"free", chk:false}
  ];
  rows = rows.slice(0, __AGENDAROWS__);

  rows.forEach(function(r){
    var tr = document.createElement("div");
    tr.className = "trow";

    // checkbox
    var c0 = document.createElement("div");
    c0.className = "chk";
    if (r.chk){
      c0.style.background = "#111";
      c0.style.borderColor = "#111";
    }

    // name + mobile meta
    var c1 = document.createElement("div");
    c1.style.minWidth = "0";
    var name = document.createElement("div");
    name.textContent = r.name;

    var meta = document.createElement("div");
    meta.className = "rowmeta";

    if (r.ini || r.fin){
      var t = document.createElement("span");
      t.className = "pill";
      t.textContent = (r.ini || "--:--") + " → " + (r.fin || "--:--");
      meta.appendChild(t);
    }
    if (r.st){
      var s2 = document.createElement("span");
      s2.className = "pill";
      s2.textContent = r.st;
      meta.appendChild(s2);
    }

    c1.appendChild(name);
    c1.appendChild(meta);

    // desktop cols
    var c2 = document.createElement("div");
    c2.className = "col_time";
    c2.textContent = r.ini;

    var c3 = document.createElement("div");
    c3.className = "col_time2";
    c3.textContent = r.fin;

    var c4 = document.createElement("div");
    c4.className = "col_status";
    if (r.st){
      var s = document.createElement("span");
      s.className = "status " + r.cls;
      s.textContent = r.st;
      c4.appendChild(s);
    }

    tr.appendChild(c0);
    tr.appendChild(c1);
    tr.appendChild(c2);
    tr.appendChild(c3);
    tr.appendChild(c4);

    tbody.appendChild(tr);
  });
})();
</script>

</body>
</html>
"""

html = (
    html.replace("__PADX__", str(PAD_X_PX))
        .replace("__PADTOP__", str(PAD_TOP_PX))
        .replace("__B__", str(BORDER_PX))
        .replace("__BC__", BORDER_COLOR)
        .replace("__BG__", BG_COLOR)
        .replace("__PANEL__", PANEL_BG)
        .replace("__CARD__", CARD_BG)
        .replace("__TXT__", TEXT_COLOR)
        .replace("__MUTED__", MUTED_TEXT)
        .replace("__FBASE__", str(FONT_BASE_PX))
        .replace("__TITLE__", str(TITLE_PX))
        .replace("__H2__", str(H2_PX))
        .replace("__SMALL__", str(SMALL_PX))
        .replace("__INNERL__", str(INNER_L))
        .replace("__INNERR__", str(INNER_R))
        .replace("__GAPY__", str(INNER_TOP_GAP))
        .replace("__TOPBARH__", str(TOPBAR_H))
        .replace("__MONTHBARH__", str(MONTHBAR_H))
        .replace("__CALGRIDH__", str(CAL_GRID_H))
        .replace("__FILTERSH__", str(FILTERS_H))
        .replace("__AGENDAH__", str(AGENDA_H))
        .replace("__BOTTOMH__", str(BOTTOMBAR_H))
        .replace("__CELLGAP__", str(DAY_CELL_GAP_PX))
        .replace("__CALCOLS__", str(CAL_COLS))
        .replace("__CALROWS__", str(CAL_ROWS))
        .replace("__AGENDAROWS__", str(AGENDA_ROWS))
)

components.html(html, height=1100, scrolling=False)
