# pages/calendario.py
import streamlit as st
import streamlit.components.v1 as components
import json

# ==============================================================================
# CALENDARIO - TEMA HUD NARANJA (VERSIÓN CON DEPURACIÓN VISIBLE Y DATOS SEGUROS)
# ==============================================================================

query_params = st.query_params
AUTH_USER = query_params.get("usuario") or query_params.get("user") or ""
AUTH_ROLE = query_params.get("rol") or query_params.get("role") or ""
AUTH_DNI = query_params.get("dni") or ""

if not AUTH_USER or not AUTH_ROLE:
    st.markdown('<script>window.location.href="/admin";</script>', unsafe_allow_html=True)
    st.stop()

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

# Construir un objeto JSON seguro con los datos del usuario
user_data = {
    "usuario": AUTH_USER,
    "rol": AUTH_ROLE,
    "dni": AUTH_DNI
}
user_json = json.dumps(user_data)

# HTML completo (incluye estilos, lógica y manejo de errores)
html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calendario - Socorrista Pro</title>
    <style>
        /* ========== ESTILOS COMPLETOS (MANTENIDOS) ========== */
        :root {{
            --bg-0:#070b12;
            --bg-1:#0b1320;
            --bg-2:#0f1c2a;
            --glass: rgba(255,255,255,.06);
            --glass-2: rgba(255,255,255,.08);
            --stroke: rgba(255,255,255,.10);
            --glow-orange: rgba(255, 142, 64, .50);
            --glow-orange-2: rgba(255, 142, 64, .22);
            --txt-0: rgba(255,255,255,.95);
            --txt-1: rgba(255,255,255,.78);
            --txt-2: rgba(255,255,255,.55);
            --free:#4fe38c;
            --busy:#ff4b4b;
            --other:#ff7c2c;
            --radius-outer: 26px;
            --radius-card: 18px;
            --radius-pill: 999px;
            --radius-cell: 12px;
            --shadow-soft: 0 18px 40px rgba(0,0,0,.45);
            --blur: 18px;
            --fs-title: 28px;
            --fs-sub: 12px;
            --fs-day: 11px;
            --fs-cell: 14px;
            --fs-h3: 18px;
            --fs-table: 13px;
            --fs-btn: 14px;
            --pad-outer: 16px;
            --pad-block: 14px;
        }}
        *{{box-sizing:border-box;}}
        body{{
            margin:0;
            background: #0a0f1a;
            font-family: 'Segoe UI', system-ui, sans-serif;
            color: var(--txt-0);
            padding: 20px;
        }}
        .error-box {{
            background: #ff4444;
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin: 20px;
            white-space: pre-wrap;
            font-family: monospace;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(10, 20, 35, 0.7);
            border-radius: var(--radius-outer);
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid var(--stroke);
        }}
        .month-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .month-nav button {{
            background: var(--glass);
            border: 1px solid var(--stroke);
            color: var(--txt-0);
            padding: 8px 16px;
            border-radius: 30px;
            cursor: pointer;
            font-weight: bold;
        }}
        .month-title {{
            font-size: var(--fs-title);
            font-weight: 800;
            text-transform: uppercase;
        }}
        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            margin: 20px 0;
        }}
        .day-cell {{
            background: var(--glass);
            border: 1px solid var(--stroke);
            border-radius: var(--radius-cell);
            padding: 12px 4px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
            position: relative;
        }}
        .day-cell.selected {{
            background: rgba(255,124,44,0.4);
            border-color: #ff7c2c;
            box-shadow: 0 0 12px var(--glow-orange-2);
        }}
        .day-cell.has-data::after {{
            content: "●";
            position: absolute;
            bottom: 4px;
            right: 8px;
            font-size: 10px;
            color: var(--free);
        }}
        .day-cell.other-month {{
            opacity: 0.4;
        }}
        .filters {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 20px 0;
        }}
        .filters select, .filters button {{
            background: var(--glass);
            border: 1px solid var(--stroke);
            padding: 8px 12px;
            border-radius: 30px;
            color: var(--txt-0);
            cursor: pointer;
        }}
        .agenda-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }}
        .agenda-table th, .agenda-table td {{
            border: 1px solid var(--stroke);
            padding: 8px;
            text-align: left;
        }}
        .status {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
        }}
        .status.free {{ background: #2e7d32; color: white; }}
        .status.busy {{ background: #c62828; color: white; }}
        .status.other {{ background: #6a1b9a; color: white; }}
        .btn-group {{
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }}
        .btn {{
            background: var(--glass);
            border: 1px solid var(--stroke);
            padding: 8px 16px;
            border-radius: 30px;
            cursor: pointer;
        }}
        .btn-primary {{
            background: rgba(255,124,44,0.2);
            border-color: #ff7c2c;
            color: #ff7c2c;
        }}
        .loading {{
            text-align: center;
            padding: 40px;
            font-size: 1.2rem;
        }}
    </style>
</head>
<body>
    <div id="app" class="container">
        <div class="loading">⏳ Cargando calendario...</div>
    </div>

    <!-- Datos del usuario inyectados de forma segura -->
    <script id="userData" type="application/json">{user_json}</script>

    <script>
        // ========== MANEJADOR DE ERRORES GLOBAL ==========
        window.addEventListener('error', function(e) {{
            document.getElementById('app').innerHTML = `
                <div class="error-box">
                    ❌ ERROR EN JAVASCRIPT:<br>
                    ${{e.message}}<br>
                    En ${{e.filename}}:${{e.lineno}}:${{e.colno}}
                </div>`;
            console.error(e);
        }});

        (function() {{
            try {{
                // Leer datos del usuario desde el script JSON
                const userScript = document.getElementById('userData');
                const user = JSON.parse(userScript.textContent);
                const CURRENT_USER = user.usuario;
                const CURRENT_ROLE = user.rol.toLowerCase();
                const CURRENT_DNI = user.dni;
                const IS_SOCORRISTA = CURRENT_ROLE === "socorrista";

                // Mostrar información de depuración
                document.getElementById('app').innerHTML = `
                    <div style="background: #1e2a3a; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                        ✅ Depuración: Usuario: ${{CURRENT_USER}} | Rol: ${{CURRENT_ROLE}} | DNI: ${{CURRENT_DNI}} | Socorrista: ${{IS_SOCORRISTA}}
                    </div>
                    <div class="loading">Cargando datos desde la API...</div>
                `;

                const API_URL = "https://camilo27.pythonanywhere.com/api/mallas";
                let allRows = [];
                let availableDates = new Set();
                let selectedDate = new Date();
                let currentYear = selectedDate.getFullYear();
                let currentMonth = selectedDate.getMonth();

                // Funciones auxiliares
                function formatDateKey(date) {{
                    let y = date.getFullYear();
                    let m = String(date.getMonth()+1).padStart(2,'0');
                    let d = String(date.getDate()).padStart(2,'0');
                    return `${{y}}-${{m}}-${{d}}`;
                }}

                function parseDateFromSheet(fechaStr) {{
                    if (!fechaStr) return null;
                    let parts = fechaStr.split('/');
                    if (parts.length === 3) {{
                        let d = parts[0], m = parts[1], y = parts[2];
                        if (y.length===4 && m>=1 && m<=12 && d>=1 && d<=31)
                            return `${{y}}-${{String(m).padStart(2,'0')}}-${{String(d).padStart(2,'0')}}`;
                    }}
                    if (fechaStr.match(/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/)) return fechaStr;
                    let d2 = new Date(fechaStr);
                    if (!isNaN(d2)) return formatDateKey(d2);
                    return null;
                }}

                function getField(row, keys) {{
                    for (let k of keys) if (row[k] !== undefined) return row[k];
                    return "";
                }}

                function getDisplayStatus(row) {{
                    let estado = getField(row, ["estado","Estado"]).toLowerCase();
                    let socorrista = getField(row, ["Socorrista","socorrista"]).toLowerCase();
                    if (estado.includes("disponible")) return {{ label: "Disponible", cls: "free" }};
                    if (estado.includes("programado")) {{
                        if (socorrista === CURRENT_USER.toLowerCase()) return {{ label: "Programado", cls: "free" }};
                        else return {{ label: "Cerrado", cls: "busy" }};
                    }}
                    return {{ label: estado.toUpperCase() || "OTRO", cls: "other" }};
                }}

                function formatTime(t) {{
                    if (!t) return "-";
                    let s = String(t);
                    return s.replace(/(\\d{{1,2}}:\\d{{2}}):\\d{{2}}$/, '$1');
                }}

                function renderCalendar() {{
                    let firstDay = new Date(currentYear, currentMonth, 1).getDay();
                    firstDay = firstDay === 0 ? 7 : firstDay;
                    let daysInMonth = new Date(currentYear, currentMonth+1, 0).getDate();
                    let days = [];
                    for (let i = 1; i < firstDay; i++) days.push({{ date: null, other: true }});
                    for (let d = 1; d <= daysInMonth; d++) days.push({{ date: new Date(currentYear, currentMonth, d), other: false }});
                    while (days.length % 7 !== 0) days.push({{ date: null, other: true }});

                    let weekdays = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"];
                    let html = '<div class="calendar-grid">';
                    for (let w of weekdays) html += `<div style="text-align:center; font-weight:bold;">${{w}}</div>`;
                    for (let cell of days) {{
                        if (cell.other || !cell.date) {{
                            html += '<div class="day-cell other-month"></div>';
                        }} else {{
                            let date = cell.date;
                            let key = formatDateKey(date);
                            let hasData = availableDates.has(key);
                            let isSelected = (selectedDate && formatDateKey(selectedDate) === key);
                            let classes = "day-cell";
                            if (hasData) classes += " has-data";
                            if (isSelected) classes += " selected";
                            html += `<div class="${{classes}}" data-date="${{key}}">${{date.getDate()}}</div>`;
                        }}
                    }}
                    html += '</div>';
                    document.getElementById("calendar").innerHTML = html;

                    document.querySelectorAll('.day-cell[data-date]').forEach(el => {{
                        el.addEventListener('click', () => {{
                            selectedDate = new Date(el.dataset.date);
                            renderCalendar();
                            loadAgenda();
                        }});
                    }});
                }}

                async function loadAgenda() {{
                    let key = formatDateKey(selectedDate);
                    let filtered = allRows.filter(row => {{
                        let fechaKey = parseDateFromSheet(getField(row, ["Fecha","fecha"]));
                        if (!fechaKey) return false;
                        if (fechaKey < formatDateKey(new Date())) return false;
                        if (IS_SOCORRISTA && CURRENT_DNI) {{
                            let rowDNI = String(getField(row, ["DNI","dni","Cédula","cedula"]) || "").trim();
                            if (rowDNI.toLowerCase() !== CURRENT_DNI.toLowerCase()) return false;
                        }}
                        return fechaKey === key;
                    }});
                    if (filtered.length === 0) {{
                        document.getElementById("agenda").innerHTML = "<p>Sin registros para esta fecha.</p>";
                        return;
                    }}
                    let html = `<table class="agenda-table"><thead><tr><th>Instalación</th><th>Inicio</th><th>Fin</th><th>Horas</th><th>Estado</th></tr></thead><tbody>`;
                    for (let row of filtered) {{
                        let inst = getField(row, ["Instalacion","Instalación","instalacion"]) || "-";
                        let inicio = formatTime(getField(row, ["Ingreso","Inicio","ingreso","inicio"]));
                        let fin = formatTime(getField(row, ["Salida","Finaliza","finaliza","salida"]));
                        let horas = formatTime(getField(row, ["Intensidad_horaria","Intensidad_ho","Horas","horas"]));
                        let status = getDisplayStatus(row);
                        html += `<tr>
                                    <td>${{inst}}</td>
                                    <td>${{inicio}}</td>
                                    <td>${{fin}}</td>
                                    <td>${{horas}}</td>
                                    <td><span class="status ${{status.cls}}">${{status.label}}</span></td>
                                 </tr>`;
                    }}
                    html += `</tbody></table>`;
                    document.getElementById("agenda").innerHTML = html;
                }}

                async function loadData() {{
                    try {{
                        const resp = await fetch(API_URL);
                        const data = await resp.json();
                        if (data.ok && Array.isArray(data.rows)) {{
                            allRows = data.rows;
                            availableDates.clear();
                            for (let row of allRows) {{
                                let fechaKey = parseDateFromSheet(getField(row, ["Fecha","fecha"]));
                                if (fechaKey && fechaKey >= formatDateKey(new Date())) {{
                                    if (IS_SOCORRISTA && CURRENT_DNI) {{
                                        let rowDNI = String(getField(row, ["DNI","dni","Cédula","cedula"]) || "").trim();
                                        if (rowDNI.toLowerCase() !== CURRENT_DNI.toLowerCase()) continue;
                                    }}
                                    availableDates.add(fechaKey);
                                }}
                            }}
                            // Construir interfaz completa
                            let months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
                            document.getElementById("app").innerHTML = `
                                <div class="month-nav">
                                    <button id="prevMonth">◀ Mes anterior</button>
                                    <div class="month-title" id="monthYear">${{months[currentMonth]}} ${{currentYear}}</div>
                                    <button id="nextMonth">Mes siguiente ▶</button>
                                </div>
                                <div id="calendar"></div>
                                <div class="filters">
                                    <select id="monthSelect"></select>
                                    <select id="yearSelect"></select>
                                    ${!IS_SOCORRISTA ? `<select id="socorristaSelect"><option value="">Todos los socorristas</option></select>` : ''}
                                    <select id="modeSelect">
                                        <option value="dia">Por día</option>
                                        <option value="todo">Ver todo (desde hoy)</option>
                                    </select>
                                    <button id="applyFilters">Aplicar</button>
                                </div>
                                <h3>📋 Agenda del día</h3>
                                <div id="agenda"></div>
                                <div class="btn-group">
                                    <button class="btn" id="btnAplicar">Aplicar cambios</button>
                                    <button class="btn" id="btnModificar">Modificar turno</button>
                                    <button class="btn btn-primary" id="btnEnviar">Enviar</button>
                                </div>
                            `;
                            // Llenar selects de mes y año
                            let monthSelect = document.getElementById('monthSelect');
                            for (let i=0; i<12; i++) {{
                                let opt = document.createElement('option');
                                opt.value = i;
                                opt.textContent = months[i];
                                if (i === currentMonth) opt.selected = true;
                                monthSelect.appendChild(opt);
                            }}
                            let yearSelect = document.getElementById('yearSelect');
                            let currentYearNum = new Date().getFullYear();
                            for (let y = currentYearNum-5; y <= currentYearNum+5; y++) {{
                                let opt = document.createElement('option');
                                opt.value = y;
                                opt.textContent = y;
                                if (y === currentYear) opt.selected = true;
                                yearSelect.appendChild(opt);
                            }}
                            if (!IS_SOCORRISTA) {{
                                // Cargar lista de socorristas
                                let socSet = new Set();
                                allRows.forEach(r => {{
                                    let s = getField(r, ["Socorrista","socorrista"]).trim();
                                    if (s) socSet.add(s);
                                }});
                                let socSelect = document.getElementById('socorristaSelect');
                                socSet.forEach(s => {{
                                    let opt = document.createElement('option');
                                    opt.value = s;
                                    opt.textContent = s;
                                    socSelect.appendChild(opt);
                                }});
                            }}
                            renderCalendar();
                            loadAgenda();
                            // Eventos
                            document.getElementById('prevMonth').onclick = () => {{
                                if (currentMonth === 0) {{ currentMonth = 11; currentYear--; }}
                                else currentMonth--;
                                document.getElementById('monthYear').innerText = `${{months[currentMonth]}} ${{currentYear}}`;
                                renderCalendar();
                                loadAgenda();
                            }};
                            document.getElementById('nextMonth').onclick = () => {{
                                if (currentMonth === 11) {{ currentMonth = 0; currentYear++; }}
                                else currentMonth++;
                                document.getElementById('monthYear').innerText = `${{months[currentMonth]}} ${{currentYear}}`;
                                renderCalendar();
                                loadAgenda();
                            }};
                            document.getElementById('applyFilters').onclick = () => {{
                                let newMonth = parseInt(monthSelect.value);
                                let newYear = parseInt(yearSelect.value);
                                currentMonth = newMonth;
                                currentYear = newYear;
                                document.getElementById('monthYear').innerText = `${{months[currentMonth]}} ${{currentYear}}`;
                                renderCalendar();
                                loadAgenda();
                            }};
                        }} else {{
                            throw new Error("Formato de datos inválido");
                        }}
                    }} catch(e) {{
                        document.getElementById("app").innerHTML = `<div class="error-box">❌ Error al cargar API: ${{e.message}}</div>`;
                        console.error(e);
                    }}
                }}
                loadData();
            }} catch(e) {{
                document.getElementById("app").innerHTML = `<div class="error-box">❌ Error de inicialización: ${{e.message}}<br><br>Revisa la consola (F12) para más detalles.</div>`;
                console.error(e);
            }}
        }})();
    </script>
</body>
</html>
"""

components.html(html, height=1000, scrolling=True)
