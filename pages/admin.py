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

    /* Nueva sección para agregar desde bloque */
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
      flex: 1 1 200px;
      min-width: 150px;
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
      min-width: 640px;
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

    @media (max-width: 768px) {
      .wrap { padding: 10px 10px 18px; }
      .top-actions { grid-template-columns: 1fr; }
      .agregar-row { flex-direction: column; align-items: stretch; }
      .section-head { flex-direction: column; align-items: flex-start; }
      .weekbox { width: 100%; justify-content: space-between; }
      .weekbox .range { max-width: 220px; }
      .filters { grid-template-columns: 1fr; }
      table { min-width: 0; width: 100%; }
      .col-instalacion, .col-socorrista, .col-horas { display: none; }
      thead th.col-instalacion,
      thead th.col-socorrista,
      thead th.col-horas { display: none; }
      .col-finaliza { display: table-cell; }
      thead th.col-finaliza { display: table-cell; }
      .table-title { display:none; }
      .pagerbar { gap: 8px; }
      .showing { max-width: 60%; }
      .pager { max-width: 40%; }
    }
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

      <!-- NUEVA SECCIÓN: AGREGAR DESDE BLOQUE -->
      <div class="agregar-section">
        <div class="agregar-title">➕ Agregar desde bloque</div>
        <div class="agregar-row">
          <div class="agregar-field">
            <label for="fechaInput">Fecha (dd/mm/aaaa)</label>
            <input type="text" id="fechaInput" placeholder="ej. 17/01/2025" value="">
          </div>
          <div class="agregar-field">
            <label for="bloqueInput">Número de bloque</label>
            <input type="number" id="bloqueInput" placeholder="ej. 1" min="1" value="">
          </div>
          <button class="agregar-btn" id="btnAgregar">Agregar</button>
        </div>
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
                <th>Día</th>   <!-- Antes era Turno, ahora Día -->
                <th>Inicio</th>
                <th class="col-finaliza">Finaliza</th>
                <th class="col-horas">Horas</th>
                <th>Estado</th>
                <th style="display:none;">llave</th> <!-- oculto para almacenar -->
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

  <!-- Modal para editar turno -->
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

    let allRows = [];
    let filtered = [];
    let page = 1;
    const pageSize = 14;

    // Elementos DOM
    const instSel = document.getElementById("instSel");
    const socSel = document.getElementById("socSel");
    const tbody = document.getElementById("tbody");
    const showingTxt = document.getElementById("showingTxt");
    const pgCur = document.getElementById("pgCur");
    const pgPrev = document.getElementById("pgPrev");
    const pgNext = document.getElementById("pgNext");
    const btnBuscar = document.getElementById("btnBuscar");
    const btnAgregar = document.getElementById("btnAgregar");
    const fechaInput = document.getElementById("fechaInput");
    const bloqueInput = document.getElementById("bloqueInput");

    // Modal de edición
    const editModal = document.getElementById("editModal");
    const editSocorrista = document.getElementById("editSocorrista");
    const editInstalacion = document.getElementById("editInstalacion");
    const editIngreso = document.getElementById("editIngreso");
    const editSalida = document.getElementById("editSalida");
    const modalCancel = document.getElementById("modalCancel");
    const modalSave = document.getElementById("modalSave");

    let currentEditLlave = null; // guarda la llave del turno que se está editando

    // Iconos SVG
    function svgEdit() {
      return `<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M12 20h9" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4 11.5-11.5Z" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    }
    function svgTrash() {
      return `<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M3 6h18" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M8 6V4h8v2" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M19 6l-1 14H6L5 6" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11v6" stroke="#111" stroke-width="2" stroke-linecap="round"/><path d="M14 11v6" stroke="#111" stroke-width="2" stroke-linecap="round"/></svg>`;
    }

    // Cargar datos desde la API
    async function loadMallas() {
      try {
        const res = await fetch(ENDPOINT_MALLAS);
        if (!res.ok) throw new Error("Error HTTP " + res.status);
        const data = await res.json();
        if (!data.ok) throw new Error("Respuesta no ok");
        allRows = data.rows || [];
        // Extraer opciones únicas para filtros
        const instalacionesSet = new Set();
        const socorristasSet = new Set();
        allRows.forEach(r => {
          if (r.Instalacion) instalacionesSet.add(r.Instalacion);
          if (r.Socorrista) socorristasSet.add(r.Socorrista);
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
        const okInst = (inst === "Todas") || (r.Instalacion === inst);
        const okSoc = (soc === "Todos") || (r.Socorrista === soc);
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
        // Guardar llave como data-attribute
        tr.dataset.llave = r.llave || "";

        // Instalacion
        const tdInst = document.createElement("td");
        tdInst.className = "col-instalacion";
        tdInst.textContent = r.Instalacion || "";

        // Socorrista
        const tdSoc = document.createElement("td");
        tdSoc.className = "col-socorrista";
        tdSoc.textContent = r.Socorrista || "";

        // Día (antes Turno) -> r.Dia
        const tdDia = document.createElement("td");
        tdDia.textContent = r.Dia || "";

        // Inicio -> r.Ingreso
        const tdInicio = document.createElement("td");
        tdInicio.textContent = r.Ingreso || "";

        // Finaliza -> r.Salida
        const tdFinaliza = document.createElement("td");
        tdFinaliza.className = "col-finaliza";
        tdFinaliza.textContent = r.Salida || "";

        // Horas -> r.Intensidad_horaria
        const tdHoras = document.createElement("td");
        tdHoras.className = "col-horas";
        tdHoras.textContent = r.Intensidad_horaria || "";

        // Estado -> r.estado
        const tdEstado = document.createElement("td");
        const wrap = document.createElement("div");
        wrap.className = "actions";

        const b1 = document.createElement("button");
        b1.className = "iconbtn";
        b1.type = "button";
        b1.innerHTML = svgEdit();
        b1.addEventListener("click", (e) => {
          e.stopPropagation();
          openEditModal(r);
        });

        const b2 = document.createElement("button");
        b2.className = "iconbtn";
        b2.type = "button";
        b2.innerHTML = svgTrash();
        b2.addEventListener("click", (e) => {
          e.stopPropagation();
          if (confirm("¿Está seguro de eliminar este turno?")) {
            eliminarTurno(r.llave);
          }
        });

        wrap.appendChild(b1);
        wrap.appendChild(b2);
        tdEstado.appendChild(wrap);

        // Columna oculta para llave (no se muestra)
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

    // Abrir modal de edición con datos actuales
    function openEditModal(row) {
      currentEditLlave = row.llave;
      editSocorrista.value = row.Socorrista || "";
      editInstalacion.value = row.Instalacion || "";
      editIngreso.value = row.Ingreso || "";
      editSalida.value = row.Salida || "";
      editModal.style.display = "flex";
    }

    // Cerrar modal
    function closeModal() {
      editModal.style.display = "none";
      currentEditLlave = null;
    }

    // Guardar cambios de edición
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
          loadMallas(); // recargar datos
        } else {
          alert("Error al editar: " + (data.error || "desconocido"));
        }
      } catch (e) {
        alert("Error de red al editar");
      }
    }

    // Eliminar turno
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

    // Agregar desde bloque
    async function agregarDesdeBloque() {
      const fecha = fechaInput.value.trim();
      const bloque = bloqueInput.value.trim();
      if (!fecha || !bloque) {
        alert("Debe ingresar fecha y bloque");
        return;
      }
      // Validar formato fecha dd/mm/yyyy
      if (!/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(fecha)) {
        alert("La fecha debe tener formato dd/mm/aaaa");
        return;
      }
      try {
        const res = await fetch(ENDPOINT_AGREGAR, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ fecha: fecha, bloque: bloque })
        });
        const data = await res.json();
        if (data.ok) {
          alert("Turnos agregados correctamente");
          fechaInput.value = "";
          bloqueInput.value = "";
          loadMallas();
        } else {
          alert("Error al agregar: " + (data.error || "desconocido"));
        }
      } catch (e) {
        alert("Error de red al agregar");
      }
    }

    // Eventos
    btnBuscar.addEventListener("click", applyFilters);

    pgPrev.addEventListener("click", () => {
      if (page > 1) { page--; render(); }
    });
    pgNext.addEventListener("click", () => {
      if (!pgNext.disabled) { page++; render(); }
    });

    btnAgregar.addEventListener("click", agregarDesdeBloque);

    modalCancel.addEventListener("click", closeModal);
    modalSave.addEventListener("click", guardarEdicion);

    // Cerrar modal si se hace clic fuera del contenido
    editModal.addEventListener("click", (e) => {
      if (e.target === editModal) closeModal();
    });

    // Placeholders de botones existentes
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

    // Inicializar
    loadMallas();
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

components.html(html, height=1100, scrolling=True)
