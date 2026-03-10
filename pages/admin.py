# pages/admin.py
import json
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Asignacion Horarios Socorristas", layout="wide")

# =========================
# DATA (DEMO) - reemplaza por tu fuente real (API/DB)
# =========================
def build_demo_data():
    base = datetime(2022, 1, 17, 8, 0, 0)
    rows = []
    instalaciones = ["Piscina Norte", "Piscina Sur", "Gimnasio", "Club"]
    socorristas = ["Ana", "Juan", "Carlos", "Sofia", "Pedro", "Luisa"]
    turnos = ["Mañana", "Tarde", "Noche"]
    for i in range(1, 15):  # 1..14
        inst = instalaciones[(i - 1) % len(instalaciones)]
        soc = socorristas[(i - 1) % len(socorristas)]
        turno = turnos[(i - 1) % len(turnos)]
        inicio = base + timedelta(hours=((i - 1) % 6) * 2, days=((i - 1) % 7))
        horas = 6 if turno != "Noche" else 8
        finaliza = inicio + timedelta(hours=horas)
        rows.append(
            {
                "Instalacion": inst,
                "Socorrista": soc,
                "Turno": turno,
                "Inicio": inicio.strftime("%Y-%m-%d %H:%M"),
                "Finaliza": finaliza.strftime("%Y-%m-%d %H:%M"),
                "Horas": horas,
            }
        )
    return pd.DataFrame(rows)

df = build_demo_data()

inst_options = ["Todas"] + sorted(df["Instalacion"].unique().tolist())
soc_options = ["Todos"] + sorted(df["Socorrista"].unique().tolist())

payload = {
    "data": df.to_dict(orient="records"),
    "instalaciones": inst_options,
    "socorristas": soc_options,
}
payload_json = json.dumps(payload, ensure_ascii=False)

# =========================
# HTML UI (RESPONSIVE)
# =========================
html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {
      --bg: #ffffff;
      --text: #111111;
      --muted: #6b7280;
      --line: #111111;
      --soft: rgba(17,17,17,.10);
      --soft2: rgba(17,17,17,.06);
      --btn-green: #2f7d32;
      --btn-red: #c62828;
      --btn-green-h: #256528;
      --btn-red-h: #a81f1f;
      --shadow: 0 8px 22px rgba(0,0,0,.08);
      --font: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif;
    }

    html, body {
      margin:0; padding:0; width:100%; height:100%;
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      overflow-x: hidden; /* evita desbordes */
    }

    * { box-sizing: border-box; }

    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 18px 14px 24px;
      overflow: hidden; /* nada se sale del contenedor */
    }

    .frame {
      width: 100%;
      border: 2px solid var(--line);
      border-radius: 0;
      padding: 14px 12px 16px;
      overflow: hidden; /* nada se sale del borde */
    }

    .title {
      border: 2px solid var(--line);
      padding: 8px 10px;
      text-align: center;
      font-weight: 700;
      letter-spacing: .2px;
      font-size: 16px;
      margin-bottom: 14px;
      width: 100%;
    }

    .top-actions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      align-items: center;
      margin-bottom: 16px;
      width: 100%;
    }

    .btn {
      border: 0;
      border-radius: 8px;
      padding: 12px 14px;
      color: #fff;
      font-weight: 700;
      cursor: pointer;
      display:flex;
      align-items:center;
      justify-content:center;
      gap: 10px;
      box-shadow: var(--shadow);
      user-select:none;
      width: 100%;
      min-width: 0;
    }
    .btn .ico {
      width: 18px; height: 18px;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      filter: drop-shadow(0 2px 2px rgba(0,0,0,.15));
    }
    .btn.green { background: var(--btn-green); }
    .btn.red { background: var(--btn-red); }
    .btn.green:hover { background: var(--btn-green-h); }
    .btn.red:hover { background: var(--btn-red-h); }

    .section { margin-top: 6px; width: 100%; }

    .section-head {
      display:flex;
      align-items:center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 10px;
      width: 100%;
      min-width: 0;
    }
    .subtitle {
      font-weight: 800;
      font-size: 18px;
      color: #1f3b6f;
      min-width: 0;
    }

    .weekbox {
      display:flex;
      align-items:center;
      gap: 8px;
      border: 1px solid var(--soft);
      background: #fff;
      border-radius: 10px;
      padding: 6px 8px;
      box-shadow: 0 6px 18px rgba(0,0,0,.06);
      min-width: 0;
      max-width: 100%;
    }
    .weekbox .label {
      font-size: 12px;
      color: var(--muted);
      font-weight: 700;
      white-space: nowrap;
    }
    .weekbox .nav {
      border: 1px solid var(--soft);
      background: #fff;
      border-radius: 8px;
      width: 32px;
      height: 30px;
      cursor: pointer;
      font-weight: 800;
      flex: 0 0 auto;
    }
    .weekbox .nav:hover { background: var(--soft2); }
    .weekbox .range {
      font-size: 13px;
      font-weight: 800;
      padding: 0 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 180px;
    }

    .filters {
      display:grid;
      grid-template-columns: 260px 1fr 1fr 160px;
      gap: 10px;
      align-items: end;
      margin-top: 10px;
      margin-bottom: 10px;
      width: 100%;
      min-width: 0;
    }

    .field label {
      display:block;
      font-size: 12px;
      font-weight: 800;
      color: var(--text);
      margin: 0 0 6px;
    }

    select {
      width: 100%;
      border: 2px solid var(--line);
      border-radius: 0;
      padding: 10px 10px;
      background: #fff;
      font-weight: 700;
      font-size: 13px;
      outline: none;
      min-width: 0;
    }

    .searchbtn {
      width: 100%;
      border: 2px solid var(--line);
      border-radius: 0;
      padding: 10px 10px;
      background: #fff;
      font-weight: 900;
      cursor: pointer;
      min-width: 0;
    }
    .searchbtn:hover { background: var(--soft2); }

    /* Tabla SOLO la caja de tabla */
    .tablewrap {
      border: 2px solid var(--line);
      padding: 10px;
      margin-top: 10px;
      width: 100%;
      overflow-x: auto; /* si algo aprieta, no desborda */
    }

    .table-title {
      font-weight: 900;
      margin-bottom: 8px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      min-width: 640px; /* mantiene estructura desktop sin romper */
    }
    thead th {
      text-align: left;
      padding: 8px 6px;
      border-bottom: 1px solid var(--soft);
      font-weight: 900;
      white-space: nowrap;
    }
    tbody td {
      padding: 10px 6px;
      border-bottom: 1px solid rgba(0,0,0,.06);
      vertical-align: middle;
      font-weight: 600;
      white-space: nowrap;
    }

    .actions {
      display:flex;
      gap: 10px;
      align-items:center;
      justify-content:flex-start;
    }
    .iconbtn {
      width: 28px;
      height: 28px;
      border: 1px solid var(--soft);
      background: #fff;
      border-radius: 8px;
      cursor: pointer;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      flex: 0 0 auto;
    }
    .iconbtn:hover { background: var(--soft2); }
    .icon { width: 16px; height: 16px; display:block; }

    /* Paginación FUERA de la tabla, esquina inferior derecha */
    .pagerbar {
      width: 100%;
      display:flex;
      align-items:center;
      justify-content:flex-end;
      gap: 10px;
      margin-top: 10px;
      padding-right: 2px; /* asegura que no toque borde */
      overflow: hidden; /* nada se sale */
    }
    .showing {
      font-size: 12px;
      color: var(--muted);
      font-weight: 800;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 55%;
    }
    .pager {
      display:inline-flex;
      align-items:center;
      gap: 6px;
      flex: 0 0 auto;
      max-width: 45%;
    }
    .pgbtn {
      height: 28px;
      border: 1px solid var(--soft);
      background: #fff;
      border-radius: 8px;
      cursor:pointer;
      font-weight: 900;
      padding: 0 10px;
      white-space: nowrap;
      min-width: 34px;
    }
    .pgbtn:hover { background: var(--soft2); }
    .pgbtn.prev { padding: 0; width: 30px; display:inline-flex; align-items:center; justify-content:center; }
    .pgcur {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background: #2563eb;
      color: #fff;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      font-weight: 900;
      font-size: 12px;
      flex: 0 0 auto;
    }

    /* -------- MOBILE -------- */
    @media (max-width: 768px) {
      .wrap { padding: 10px 10px 18px; }
      .top-actions { grid-template-columns: 1fr; }

      .section-head { flex-direction: column; align-items: flex-start; }
      .weekbox { width: 100%; justify-content: space-between; }
      .weekbox .range { max-width: 220px; }

      .filters { grid-template-columns: 1fr; }

      /* Tabla móvil: 4 columnas -> Turno, Inicio, Finaliza, Estado */
      table { min-width: 0; width: 100%; }
      .col-instalacion, .col-socorrista, .col-horas { display: none; }
      thead th.col-instalacion,
      thead th.col-socorrista,
      thead th.col-horas { display: none; }

      /* en móvil, mostrar Finaliza (en desktop la ocultamos por no estar en tus 6 cols) */
      .col-finaliza { display: table-cell; }
      thead th.col-finaliza { display: table-cell; }

      .table-title { display:none; }

      /* pagerbar: que nunca se salga */
      .pagerbar { gap: 8px; }
      .showing { max-width: 60%; }
      .pager { max-width: 40%; }
      .pgbtn { padding: 0 8px; }
      .pgbtn.prev { width: 30px; }
    }

    /* Desktop: Finaliza NO se muestra (porque en 6 columnas no va) */
    .col-finaliza { display: none; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="frame">

      <div class="title">Asignacion Horarios Socorristas</div>

      <div class="top-actions">
        <button class="btn green" id="btnPlantillas" type="button">
          <span class="ico">⬇️</span>
          <span>Descargar Plantilla</span>
        </button>

        <button class="btn red" id="btnSubir" type="button">
          <span class="ico">⬆️</span>
          <span>Subir Horarios Masivos</span>
        </button>
      </div>

      <div class="section">
        <div class="section-head">
          <div class="subtitle">Horarios de Socorristas</div>

          <div class="weekbox" aria-label="Filtro de semana">
            <span class="label">Ver Semana:</span>
            <button class="nav" id="prevWeek" type="button">‹</button>
            <span class="range" id="weekRange">17 - 23 Ene 2022</span>
            <button class="nav" id="nextWeek" type="button">›</button>
          </div>
        </div>

        <div class="filters">
          <div class="field">
            <label for="modeSel">Modo</label>
            <select id="modeSel">
              <option value="Individual">Individual</option>
              <option value="Cargar Plantilla">Cargar Plantilla</option>
            </select>
          </div>

          <div class="field">
            <label for="instSel">Instalación</label>
            <select id="instSel"></select>
          </div>

          <div class="field">
            <label for="socSel">Socorrista</label>
            <select id="socSel"></select>
          </div>

          <div class="field">
            <label>&nbsp;</label>
            <button class="searchbtn" id="btnBuscar" type="button">Buscar</button>
          </div>
        </div>

        <div class="tablewrap">
          <div class="table-title">Tabla Horarios</div>

          <table>
            <thead>
              <tr>
                <th class="col-instalacion">Instalacion</th>
                <th class="col-socorrista">Socorrista</th>
                <th>Turno</th>
                <th>Inicio</th>
                <th class="col-finaliza">Finaliza</th>
                <th class="col-horas">Horas</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody id="tbody"></tbody>
          </table>
        </div>

        <!-- FUERA de .tablewrap (requisito #2) -->
        <div class="pagerbar">
          <span class="showing" id="showingTxt">Mostrando 0 a 0 de 0</span>
          <div class="pager">
            <button class="pgbtn prev" id="pgPrev" type="button">‹</button>
            <span class="pgcur" id="pgCur">1</span>
            <button class="pgbtn" id="pgNext" type="button">Siguiente</button>
          </div>
        </div>

      </div>
    </div>
  </div>

  <script>
    const PAYLOAD = """ + payload_json + """;

    let payloadObj = null;
    try {
      payloadObj = JSON.parse(PAYLOAD);
    } catch(e) {
      payloadObj = { data: [], instalaciones: ["Todas"], socorristas: ["Todos"] };
    }

    let allRows = payloadObj.data || [];
    let filtered = [...allRows];

    let page = 1;
    const pageSize = 14;

    const instSel = document.getElementById("instSel");
    const socSel  = document.getElementById("socSel");
    const tbody   = document.getElementById("tbody");

    const showingTxt = document.getElementById("showingTxt");
    const pgCur = document.getElementById("pgCur");
    const pgPrev = document.getElementById("pgPrev");
    const pgNext = document.getElementById("pgNext");

    function svgEdit() {
      return `
        <svg class="icon" viewBox="0 0 24 24" fill="none">
          <path d="M12 20h9" stroke="#111" stroke-width="2" stroke-linecap="round"/>
          <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4 11.5-11.5Z"
                stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;
    }
    function svgTrash() {
      return `
        <svg class="icon" viewBox="0 0 24 24" fill="none">
          <path d="M3 6h18" stroke="#111" stroke-width="2" stroke-linecap="round"/>
          <path d="M8 6V4h8v2" stroke="#111" stroke-width="2" stroke-linecap="round"/>
          <path d="M19 6l-1 14H6L5 6" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M10 11v6" stroke="#111" stroke-width="2" stroke-linecap="round"/>
          <path d="M14 11v6" stroke="#111" stroke-width="2" stroke-linecap="round"/>
        </svg>`;
    }

    function fillSelect(sel, items) {
      sel.innerHTML = "";
      items.forEach(v => {
        const opt = document.createElement("option");
        opt.value = v;
        opt.textContent = v;
        sel.appendChild(opt);
      });
    }

    function applyFilters() {
      const inst = instSel.value || "Todas";
      const soc  = socSel.value || "Todos";

      filtered = allRows.filter(r => {
        const okInst = (inst === "Todas") || (r.Instalacion === inst);
        const okSoc  = (soc === "Todos") || (r.Socorrista === soc);
        return okInst && okSoc;
      });

      page = 1;
      render();
    }

    function render() {
      const total = filtered.length;
      const pages = Math.max(1, Math.ceil(total / pageSize));
      page = Math.min(page, pages);

      const startIdx = (page - 1) * pageSize;
      const endIdx = Math.min(startIdx + pageSize, total);

      tbody.innerHTML = "";
      const slice = filtered.slice(startIdx, endIdx);

      slice.forEach((r, idx) => {
        const tr = document.createElement("tr");

        const tdInst = document.createElement("td");
        tdInst.className = "col-instalacion";
        tdInst.textContent = r.Instalacion || "";

        const tdSoc = document.createElement("td");
        tdSoc.className = "col-socorrista";
        tdSoc.textContent = r.Socorrista || "";

        const tdTurno = document.createElement("td");
        tdTurno.textContent = r.Turno || "";

        const tdInicio = document.createElement("td");
        tdInicio.textContent = r.Inicio || "";

        const tdFinaliza = document.createElement("td");
        tdFinaliza.className = "col-finaliza";
        tdFinaliza.textContent = r.Finaliza || "";

        const tdHoras = document.createElement("td");
        tdHoras.className = "col-horas";
        tdHoras.textContent = (r.Horas ?? "");

        const tdEstado = document.createElement("td");
        const wrap = document.createElement("div");
        wrap.className = "actions";

        const b1 = document.createElement("button");
        b1.className = "iconbtn";
        b1.type = "button";
        b1.innerHTML = svgEdit();
        b1.addEventListener("click", () => { alert("Editar: " + (startIdx + idx + 1)); });

        const b2 = document.createElement("button");
        b2.className = "iconbtn";
        b2.type = "button";
        b2.innerHTML = svgTrash();
        b2.addEventListener("click", () => { alert("Eliminar: " + (startIdx + idx + 1)); });

        wrap.appendChild(b1);
        wrap.appendChild(b2);
        tdEstado.appendChild(wrap);

        tr.appendChild(tdInst);
        tr.appendChild(tdSoc);
        tr.appendChild(tdTurno);
        tr.appendChild(tdInicio);
        tr.appendChild(tdFinaliza);
        tr.appendChild(tdHoras);
        tr.appendChild(tdEstado);

        tbody.appendChild(tr);
      });

      const showingA = total === 0 ? 0 : (startIdx + 1);
      const showingB = endIdx;

      showingTxt.textContent = `Mostrando ${showingA} a ${showingB} de ${total}`;
      pgCur.textContent = String(page);

      pgPrev.disabled = page <= 1;
      pgNext.disabled = page >= pages;
    }

    fillSelect(instSel, payloadObj.instalaciones || ["Todas"]);
    fillSelect(socSel, payloadObj.socorristas || ["Todos"]);

    document.getElementById("btnBuscar").addEventListener("click", applyFilters);

    pgPrev.addEventListener("click", () => {
      if (page > 1) { page--; render(); }
    });
    pgNext.addEventListener("click", () => {
      if (!pgNext.disabled) { page++; render(); }
    });

    document.getElementById("btnPlantillas").addEventListener("click", () => {
      alert("Descargar Plantilla (pendiente integrar)");
    });
    document.getElementById("btnSubir").addEventListener("click", () => {
      alert("Subir Horarios Masivos (pendiente integrar)");
    });

    document.getElementById("prevWeek").addEventListener("click", () => {
      alert("Semana anterior (pendiente integrar)");
    });
    document.getElementById("nextWeek").addEventListener("click", () => {
      alert("Semana siguiente (pendiente integrar)");
    });

    render();
  </script>
</body>
</html>
"""

# =========================
# STREAMLIT SHELL (sin padding)
# =========================
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

components.html(html, height=950, scrolling=True)
