# pages/admin.py
import streamlit as st
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Asignacion Horarios Socorristas", layout="wide")

# =========================
# HTML UI (RESPONSIVE) con integración real a Mallas
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
      --modal-bg: #ffffff;
      --modal-overlay: rgba(0,0,0,0.5);
    }

    html, body {
      margin:0; padding:0; width:100%; height:100%;
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      overflow-x: hidden;
    }

    * { box-sizing: border-box; }

    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 18px 14px 24px;
      overflow: hidden;
    }

    .frame {
      width: 100%;
      border: 2px solid var(--line);
      border-radius: 0;
      padding: 14px 12px 16px;
      overflow: hidden;
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

    /* Sección para agregar desde bloque (con rango de fechas) */
    .agregar-section {
      border: 2px solid var(--line);
      padding: 12px;
      margin-bottom: 20px;
      background: #f9f9f9;
    }
    .agregar-title {
      font-weight: 800;
      font-size: 16px;
      margin-bottom: 10px;
    }
    .agregar-row {
      display: flex;
      gap: 10px;
      align-items: flex-end;
      flex-wrap: wrap;
    }
    .agregar-field {
      flex: 1 1 150px;
      min-width: 130px;
    }
    .agregar-field label {
      display: block;
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 4px;
    }
    .agregar-field input {
      width: 100%;
      border: 2px solid var(--line);
      border-radius: 0;
      padding: 10px;
      font-size: 14px;
    }
    .agregar-btn {
      background: var(--btn-green);
      color: white;
      border: none;
      padding: 10px 20px;
      font-weight: 700;
      cursor: pointer;
      border-radius: 8px;
      min-width: 120px;
    }
    .agregar-btn:hover { background: var(--btn-green-h); }

    /* Selector de rango */
    .rango-opciones {
      display: flex;
      gap: 10px;
      margin-top: 10px;
      flex-wrap: wrap;
    }
    .rango-btn {
      background: #e0e0e0;
      border: none;
      padding: 8px 12px;
      font-weight: 600;
      cursor: pointer;
      border-radius: 4px;
    }
    .rango-btn.activo {
      background: var(--btn-green);
      color: white;
    }

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

    /* ELIMINADO: .weekbox */

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

    .tablewrap {
      border: 2px solid var(--line);
      padding: 10px;
      margin-top: 10px;
      width: 100%;
      overflow-x: auto;
    }

    .table-title {
      font-weight: 900;
      margin-bottom: 8px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      min-width: 700px;
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

    .pagerbar {
      width: 100%;
      display:flex;
      align-items:center;
      justify-content:flex-end;
      gap: 10px;
      margin-top: 10px;
      padding-right: 2px;
      overflow: hidden;
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

    /* Modal para edición */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: var(--modal-overlay);
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal {
      background: var(--modal-bg);
      border: 2px solid var(--line);
      padding: 24px;
      max-width: 400px;
      width: 90%;
      box-shadow: var(--shadow);
    }
    .modal h3 {
      margin-top: 0;
      font-weight: 800;
    }
    .modal-field {
      margin-bottom: 16px;
    }
    .modal-field label {
      display: block;
      font-weight: 700;
      font-size: 13px;
      margin-bottom: 4px;
    }
    .modal-field input {
      width: 100%;
      border: 2px solid var(--line);
      padding: 8px;
      font-size: 14px;
    }
    .modal-actions {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      margin-top: 24px;
    }
    .modal-actions button {
      padding: 8px 16px;
      border: none;
      font-weight: 700;
      cursor: pointer;
    }
    .modal-actions .cancel {
      background: #ccc;
    }
    .modal-actions .save {
      background: var(--btn-green);
      color: white;
    }

    /* ===== AJUSTES MÓVIL ===== */
    @media (max-width: 768px) {
      .wrap { padding: 5px; }
      .top-actions { grid-template-columns: 1fr; }

      .agregar-section {
        padding: 8px;
        margin-bottom: 10px;
      }
      .agregar-title {
        font-size: 16px;
        margin-bottom: 6px;
      }
      .agregar-row {
        display: block;
      }
      .agregar-field {
        margin-bottom: 4px;
      }
      .agregar-field label {
        font-size: 12px;
        margin-bottom: 2px;
        font-weight: 700;
      }
      .agregar-field input {
        width: 100%;
        padding: 6px 8px;
        font-size: 14px;
        border-width: 1px;
      }
      .agregar-btn {
        padding: 8px 12px;
        font-size: 14px;
        margin-top: 4px;
        width: 100%;
      }
      .rango-opciones {
        gap: 4px;
        margin-top: 6px;
      }
      .rango-btn {
        padding: 4px 8px;
        font-size: 12px;
      }

      .filters { grid-template-columns: 1fr; }

      /* Tabla móvil: ocultar columnas por clase */
      .col-instalacion, .col-socorrista, .col-horas {
        display: none;
      }
      /* Mostrar solo las cuatro columnas */
      .col-dia, .col-inicio, .col-finaliza, .col-estado {
        display: table-cell;
      }
      /* Usar table-layout fixed para respetar anchos */
      table {
        table-layout: fixed;
        min-width: 0; /* eliminar el min-width de escritorio */
      }
      /* Asignar anchos porcentuales ajustados: más espacio para Día */
      .col-dia { width: 35%; }
      .col-inicio { width: 20%; }
      .col-finaliza { width: 20%; }
      .col-estado { width: 25%; }

      td.col-estado .actions {
        justify-content: flex-start;
        gap: 2px;
      }
      .iconbtn {
        width: 20px;
        height: 20px;
      }
      .iconbtn .icon {
        width: 12px;
        height: 12px;
      }

      .table-title { display:none; }
      .pagerbar { gap: 8px; }
      .showing { max-width: 60%; }
      .pager { max-width: 40%; }
    }
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

      <div class="agregar-section">
        <div class="agregar-title">➕ Agregar desde bloque</div>
        <div class="agregar-row">
          <div class="agregar-field">
            <label for="fechaInicio">Fecha inicio (dd/mm/aaaa)</label>
            <input type="text" id="fechaInicio" placeholder="ej. 17/01/2025" value="">
          </div>
          <div class="agregar-field">
            <label for="fechaFin">Fecha fin (dd/mm/aaaa)</label>
            <input type="text" id="fechaFin" placeholder="ej. 23/01/2025" value="">
          </div>
          <div class="agregar-field">
            <label for="bloqueInput">Número de bloque</label>
            <input type="number" id="bloqueInput" placeholder="ej. 1" min="1" value="">
          </div>
          <button class="agregar-btn" id="btnAgregarRango">Agregar rango</button>
        </div>
        <div class="rango-opciones">
          <button class="rango-btn" data-rango="dia">Día</button>
          <button class="rango-btn" data-rango="semana">Semana</button>
          <button class="rango-btn" data-rango="mes">Mes</button>
        </div>
        <small style="color: #666;">Seleccione un rango o ingrese las fechas manualmente.</small>
      </div>

      <div class="section">
        <div class="section-head">
          <div class="subtitle">Horarios de Socorristas</div>
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

          <table id="data-table">
            <thead>
              <tr>
                <th class="col-instalacion">Instalacion</th>
                <th class="col-socorrista">Socorrista</th>
                <th class="col-dia">Día</th>
                <th class="col-inicio">Inicio</th>
                <th class="col-finaliza">Finaliza</th>
                <th class="col-horas">Horas</th>
                <th class="col-estado">Estado</th>
                <th style="display:none;">llave</th>
              </tr>
            </thead>
            <tbody id="tbody"></tbody>
          </table>
        </div>

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

  <div class="modal-overlay" id="editModal">
    <div class="modal">
      <h3>Editar turno</h3>
      <div class="modal-field">
        <label for="editSocorrista">Socorrista</label>
        <input type="text" id="editSocorrista">
      </div>
      <div class="modal-field">
        <label for="editInstalacion">Instalacion</label>
        <input type="text" id="editInstalacion">
      </div>
      <div class="modal-field">
        <label for="editIngreso">Ingreso</label>
        <input type="text" id="editIngreso" placeholder="HH:MM">
      </div>
      <div class="modal-field">
        <label for="editSalida">Salida</label>
        <input type="text" id="editSalida" placeholder="HH:MM">
      </div>
      <div class="modal-actions">
        <button class="cancel" id="modalCancel">Cancelar</button>
        <button class="save" id="modalSave">Guardar</button>
      </div>
    </div>
  </div>

  <script>
    const API_BASE = "https://camilo27.pythonanywhere.com";
    const ENDPOINT_MALLAS = API_BASE + "/api/mallas";
    const ENDPOINT_AGREGAR = API_BASE + "/api/horarios/agregar";
    const ENDPOINT_EDITAR = API_BASE + "/api/horarios/editar";
    const ENDPOINT_ELIMINAR = API_BASE + "/api/horarios/eliminar";

    // Helper simplificado
    function getField(row, key) {
      if (!row) return "";
      if (row[key] !== undefined && row[key] !== null) return row[key];
      const lowerKey = key.toLowerCase();
      for (let k in row) {
        if (k.toLowerCase() === lowerKey) return row[k];
      }
      return "";
    }

    // Formatear hora a HH:MM
    function formatTime(timeStr) {
      if (!timeStr) return "";
      const str = String(timeStr);
      const parts = str.split(':');
      if (parts.length >= 2) {
        return parts[0] + ':' + parts[1];
      }
      return str;
    }

    let allRows = [];
    let filtered = [];
    let page = 1;
    const pageSize = 14;

    const instSel = document.getElementById("instSel");
    const socSel = document.getElementById("socSel");
    const tbody = document.getElementById("tbody");
    const showingTxt = document.getElementById("showingTxt");
    const pgCur = document.getElementById("pgCur");
    const pgPrev = document.getElementById("pgPrev");
    const pgNext = document.getElementById("pgNext");
    const btnBuscar = document.getElementById("btnBuscar");

    const fechaInicio = document.getElementById("fechaInicio");
    const fechaFin = document.getElementById("fechaFin");
    const bloqueInput = document.getElementById("bloqueInput");
    const btnAgregarRango = document.getElementById("btnAgregarRango");
    const rangoBtns = document.querySelectorAll(".rango-btn");

    const editModal = document.getElementById("editModal");
    const editSocorrista = document.getElementById("editSocorrista");
    const editInstalacion = document.getElementById("editInstalacion");
    const editIngreso = document.getElementById("editIngreso");
    const editSalida = document.getElementById("editSalida");
    const modalCancel = document.getElementById("modalCancel");
    const modalSave = document.getElementById("modalSave");

    let currentEditLlave = null;

    function svgEdit() {
      return `<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M12 20h9" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4 11.5-11.5Z" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    }
    function svgTrash() {
      return `<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M3 6h18" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M8 6V4h8v2" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M19 6l-1 14H6L5 6" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11v6" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M14 11v6" stroke="#111" stroke-width="2" stroke-linecap="round"/></svg>`;
    }

    function parseFechaDDMMYYYY(fechaStr) {
      if (!/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(fechaStr)) return null;
      const [dd, mm, yyyy] = fechaStr.split('/').map(Number);
      return new Date(yyyy, mm-1, dd);
    }
    function formatDateToDDMMYYYY(date) {
      const d = date.getDate().toString().padStart(2,'0');
      const m = (date.getMonth()+1).toString().padStart(2,'0');
      const y = date.getFullYear();
      return `${d}/${m}/${y}`;
    }
    function getDatesInRange(startStr, endStr) {
      const start = parseFechaDDMMYYYY(startStr);
      const end = parseFechaDDMMYYYY(endStr);
      if (!start || !end) return [];
      const dates = [];
      let current = new Date(start);
      while (current <= end) {
        dates.push(formatDateToDDMMYYYY(current));
        current.setDate(current.getDate() + 1);
      }
      return dates;
    }

    async function loadMallas() {
      try {
        const res = await fetch(ENDPOINT_MALLAS);
        if (!res.ok) throw new Error("Error HTTP " + res.status);
        const data = await res.json();
        if (!data.ok) throw new Error("Respuesta no ok");
        allRows = data.rows || [];
        const instalacionesSet = new Set();
        const socorristasSet = new Set();
        allRows.forEach(r => {
          const inst = getField(r, "Instalacion") || getField(r, "instalacion");
          if (inst) instalacionesSet.add(inst);
          const soc = getField(r, "Socorrista") || getField(r, "socorrista");
          if (soc) socorristasSet.add(soc);
        });
        const instalaciones = Array.from(instalacionesSet).sort();
        const socorristas = Array.from(socorristasSet).sort();
        fillSelect(instSel, ["Todas", ...instalaciones]);
        fillSelect(socSel, ["Todos", ...socorristas]);
        applyFilters();
      } catch (e) {
        console.error("Error cargando mallas:", e);
        allRows = [];
        fillSelect(instSel, ["Todas"]);
        fillSelect(socSel, ["Todos"]);
        applyFilters();
      }
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
      const soc = socSel.value || "Todos";
      filtered = allRows.filter(r => {
        const rInst = getField(r, "Instalacion") || getField(r, "instalacion");
        const rSoc = getField(r, "Socorrista") || getField(r, "socorrista");
        const okInst = (inst === "Todas") || (rInst === inst);
        const okSoc = (soc === "Todos") || (rSoc === soc);
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
        tr.dataset.llave = r.llave || "";

        const instalacion = r.Instalacion || r.instalacion || "";
        const socorrista = r.Socorrista || r.socorrista || "";
        const dia = r.Dia || r.dia || "";
        const inicioRaw = r.Ingreso || r.ingreso || r.Inicio || r.inicio || "";
        const salidaRaw = r.Salida || r.salida || r.Finaliza || r.finaliza || "";
        const horas = r.Intensidad_horaria || r.intensidad_horaria || r.Horas || r.horas || "";

        const inicio = formatTime(inicioRaw);
        const salida = formatTime(salidaRaw);

        const tdInst = document.createElement("td");
        tdInst.className = "col-instalacion";
        tdInst.textContent = instalacion;

        const tdSoc = document.createElement("td");
        tdSoc.className = "col-socorrista";
        tdSoc.textContent = socorrista;

        const tdDia = document.createElement("td");
        tdDia.className = "col-dia";
        tdDia.textContent = dia;

        const tdInicio = document.createElement("td");
        tdInicio.className = "col-inicio";
        tdInicio.textContent = inicio;

        const tdFinaliza = document.createElement("td");
        tdFinaliza.className = "col-finaliza";
        tdFinaliza.textContent = salida;

        const tdHoras = document.createElement("td");
        tdHoras.className = "col-horas";
        tdHoras.textContent = horas;

        const tdEstado = document.createElement("td");
        tdEstado.className = "col-estado";
        const wrap = document.createElement("div");
        wrap.className = "actions";

        const b1 = document.createElement("button");
        b1.className = "iconbtn";
        b1.type = "button";
        b1.innerHTML = svgEdit();
        b1.addEventListener("click", (e) => {
          e.stopPropagation();
          if (!r.llave) {
            alert("Este turno no tiene una llave válida. No se puede editar.");
            return;
          }
          openEditModal(r);
        });

        const b2 = document.createElement("button");
        b2.className = "iconbtn";
        b2.type = "button";
        b2.innerHTML = svgTrash();
        b2.addEventListener("click", (e) => {
          e.stopPropagation();
          if (!r.llave) {
            alert("Este turno no tiene una llave válida. No se puede eliminar.");
            return;
          }
          if (confirm("¿Está seguro de eliminar este turno?")) {
            eliminarTurno(r.llave);
          }
        });

        wrap.appendChild(b1);
        wrap.appendChild(b2);
        tdEstado.appendChild(wrap);

        const tdLlave = document.createElement("td");
        tdLlave.style.display = "none";
        tdLlave.textContent = r.llave || "";

        tr.appendChild(tdInst);
        tr.appendChild(tdSoc);
        tr.appendChild(tdDia);
        tr.appendChild(tdInicio);
        tr.appendChild(tdFinaliza);
        tr.appendChild(tdHoras);
        tr.appendChild(tdEstado);
        tr.appendChild(tdLlave);

        tbody.appendChild(tr);
      });

      const showingA = total === 0 ? 0 : (startIdx + 1);
      const showingB = endIdx;
      showingTxt.textContent = `Mostrando ${showingA} a ${showingB} de ${total}`;
      pgCur.textContent = String(page);
      pgPrev.disabled = page <= 1;
      pgNext.disabled = page >= pages;
    }

    function openEditModal(row) {
      currentEditLlave = row.llave;
      editSocorrista.value = row.Socorrista || row.socorrista || "";
      editInstalacion.value = row.Instalacion || row.instalacion || "";
      editIngreso.value = row.Ingreso || row.ingreso || row.Inicio || row.inicio || "";
      editSalida.value = row.Salida || row.salida || row.Finaliza || row.finaliza || "";
      editModal.style.display = "flex";
    }

    function closeModal() {
      editModal.style.display = "none";
      currentEditLlave = null;
    }

    async function guardarEdicion() {
      if (!currentEditLlave) return;
      const payload = {
        llave: currentEditLlave,
        Socorrista: editSocorrista.value.trim(),
        Instalacion: editInstalacion.value.trim(),
        Ingreso: editIngreso.value.trim(),
        Salida: editSalida.value.trim()
      };
      try {
        const res = await fetch(ENDPOINT_EDITAR, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.ok) {
          closeModal();
          loadMallas();
        } else {
          alert("Error al editar: " + (data.error || "desconocido"));
        }
      } catch (e) {
        alert("Error de red al editar");
      }
    }

    async function eliminarTurno(llave) {
      try {
        const res = await fetch(ENDPOINT_ELIMINAR, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ llave: llave })
        });
        const data = await res.json();
        if (data.ok) {
          loadMallas();
        } else {
          alert("Error al eliminar: " + (data.error || "desconocido"));
        }
      } catch (e) {
        alert("Error de red al eliminar");
      }
    }

    async function agregarRango() {
      const inicio = fechaInicio.value.trim();
      const fin = fechaFin.value.trim();
      const bloque = bloqueInput.value.trim();
      if (!inicio || !fin || !bloque) {
        alert("Debe ingresar fecha inicio, fecha fin y bloque");
        return;
      }
      if (!/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(inicio) || !/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(fin)) {
        alert("Las fechas deben tener formato dd/mm/aaaa");
        return;
      }
      const fechas = getDatesInRange(inicio, fin);
      if (fechas.length === 0) {
        alert("Rango de fechas inválido");
        return;
      }
      const total = fechas.length;
      let exitos = 0, errores = 0;
      for (let i = 0; i < fechas.length; i++) {
        const fecha = fechas[i];
        try {
          const res = await fetch(ENDPOINT_AGREGAR, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fecha: fecha, bloque: bloque })
          });
          const data = await res.json();
          if (data.ok) exitos++;
          else errores++;
        } catch (e) {
          errores++;
        }
        await new Promise(r => setTimeout(r, 200));
      }
      alert(`Proceso completado: ${exitos} exitosos, ${errores} errores.`);
      if (exitos > 0) {
        fechaInicio.value = "";
        fechaFin.value = "";
        bloqueInput.value = "";
        loadMallas();
      }
    }

    function setRango(tipo) {
      const hoy = new Date();
      let inicio, fin;
      if (tipo === 'dia') {
        inicio = fin = formatDateToDDMMYYYY(hoy);
      } else if (tipo === 'semana') {
        const diaSem = hoy.getDay();
        const diffLunes = (diaSem === 0 ? 6 : diaSem - 1);
        const lunes = new Date(hoy);
        lunes.setDate(hoy.getDate() - diffLunes);
        const domingo = new Date(lunes);
        domingo.setDate(lunes.getDate() + 6);
        inicio = formatDateToDDMMYYYY(lunes);
        fin = formatDateToDDMMYYYY(domingo);
      } else if (tipo === 'mes') {
        const primerDia = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
        const ultimoDia = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0);
        inicio = formatDateToDDMMYYYY(primerDia);
        fin = formatDateToDDMMYYYY(ultimoDia);
      }
      fechaInicio.value = inicio;
      fechaFin.value = fin;
    }

    btnBuscar.addEventListener("click", applyFilters);
    pgPrev.addEventListener("click", () => { if (page > 1) { page--; render(); } });
    pgNext.addEventListener("click", () => { if (!pgNext.disabled) { page++; render(); } });
    btnAgregarRango.addEventListener("click", agregarRango);
    rangoBtns.forEach(btn => {
      btn.addEventListener("click", () => setRango(btn.dataset.rango));
    });
    modalCancel.addEventListener("click", closeModal);
    modalSave.addEventListener("click", guardarEdicion);
    editModal.addEventListener("click", (e) => { if (e.target === editModal) closeModal(); });

    document.getElementById("btnPlantillas").addEventListener("click", () => alert("Descargar Plantilla (pendiente integrar)"));
    document.getElementById("btnSubir").addEventListener("click", () => alert("Subir Horarios Masivos (pendiente integrar)"));

    loadMallas();
  </script>
</body>
</html>
"""

# =========================
# STREAMLIT SHELL
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

components.html(html, height=1200, scrolling=True)
