import base64
import requests
import streamlit as st
import datetime
import calendar
from dateutil.relativedelta import relativedelta

# ----------------------------
# CONFIGURACIÓN PRINCIPAL
# ----------------------------
st.set_page_config(
    page_title="Socorrista Pro",
    page_icon="🛟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# URLs y colores
IMG_URL = "https://files.catbox.moe/0mir4o.png"
PRIMARY_COLOR = "#F37021"
SECONDARY_COLOR = "#2C3E50"
BG_COLOR = "#F8F9FA"

# Datos de ejemplo para horarios
SAMPLE_SCHEDULE = {
    "2024-01-15": [{"hora": "08:00-14:00", "tipo": "Turno Mañana", "socorrista": "Juan Pérez"}],
    "2024-01-16": [{"hora": "14:00-20:00", "tipo": "Turno Tarde", "socorrista": "María Gómez"}],
    "2024-01-17": [{"hora": "08:00-14:00", "tipo": "Turno Mañana", "socorrista": "Carlos Ruiz"}],
    "2024-01-18": [{"hora": "14:00-20:00", "tipo": "Turno Tarde", "socorrista": "Ana López"}],
    "2024-01-19": [{"hora": "08:00-20:00", "tipo": "Doble Turno", "socorrista": "Pedro Sánchez"}],
    "2024-01-22": [{"hora": "08:00-14:00", "tipo": "Turno Mañana", "socorrista": "Juan Pérez"}],
    "2024-01-23": [{"hora": "14:00-20:00", "tipo": "Turno Tarde", "socorrista": "María Gómez"}],
}

# ----------------------------
# FUNCIONES AUXILIARES
# ----------------------------
@st.cache_data(show_spinner=False)
def fetch_image_as_data_uri(url: str) -> str:
    """Convierte imagen URL a Data URI con manejo de errores"""
    try:
        if not url:
            return ""
        # Usar una imagen por defecto si falla la carga
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "image/png")
        b64 = base64.b64encode(r.content).decode("utf-8")
        return f"data:{content_type};base64,{b64}"
    except Exception as e:
        st.warning(f"Imagen no disponible, usando color de fondo: {str(e)}")
        return ""

def apply_custom_css():
    """Aplica estilos CSS personalizados responsive"""
    st.markdown(f"""
    <style>
    /* RESET COMPLETO PARA STREAMLIT */
    html, body, [data-testid="stAppViewContainer"], 
    [data-testid="stMainBlockContainer"], [data-testid="block-container"] {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100vw !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }}
    
    .stApp {{
        background: {BG_COLOR} !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
    }}
    
    /* HEADER FIJADO ARRIBA */
    .main-header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        height: 70px;
    }}
    
    .logo-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.4rem;
        font-weight: 700;
    }}
    
    .user-info {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.9rem;
    }}
    
    .user-badge {{
        background: rgba(255,255,255,0.1);
        padding: 5px 12px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    /* CONTENEDOR PRINCIPAL CON ESPACIO PARA HEADER */
    .main-content {{
        margin-top: 70px;
        padding: 20px;
        min-height: calc(100vh - 70px);
        width: 100%;
    }}
    
    /* DASHBOARD GRID RESPONSIVE */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    /* TARJETAS DEL DASHBOARD */
    .dashboard-card {{
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(0,0,0,0.05);
        text-decoration: none !important;
        display: block;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.12);
        border-color: {PRIMARY_COLOR};
    }}
    
    .card-icon {{
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        font-size: 30px;
        color: white;
    }}
    
    .card-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin-bottom: 10px;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    .card-desc {{
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    /* CALENDARIO COMPLETO */
    .calendar-page {{
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }}
    
    .calendar-header {{
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }}
    
    .month-navigation {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }}
    
    .nav-btn {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    .nav-btn:hover {{
        background: #e55a1a;
        transform: scale(1.05);
    }}
    
    .current-month {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        text-align: center;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    /* GRID DEL CALENDARIO */
    .calendar-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 2px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        border: 2px solid #e0e0e0;
    }}
    
    .day-header {{
        background: {SECONDARY_COLOR};
        color: white;
        padding: 15px 5px;
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    .calendar-day {{
        background: white;
        min-height: 120px;
        padding: 10px;
        position: relative;
        transition: all 0.3s;
    }}
    
    .calendar-day:hover {{
        background: #fff9f5;
    }}
    
    .day-number {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {SECONDARY_COLOR};
        margin-bottom: 8px;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    .today {{
        background: rgba(243, 112, 33, 0.1) !important;
        border: 2px solid {PRIMARY_COLOR} !important;
    }}
    
    .today .day-number {{
        color: {PRIMARY_COLOR};
        font-weight: 800;
    }}
    
    .weekend {{
        background: #f9f9f9;
    }}
    
    .has-events {{
        border-left: 4px solid {PRIMARY_COLOR};
    }}
    
    .event-badge {{
        background: {PRIMARY_COLOR};
        color: white;
        padding: 4px 8px;
        border-radius: 5px;
        font-size: 0.8rem;
        margin-top: 5px;
        display: block;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    .event-badge:hover {{
        background: #e55a1a;
        transform: translateX(2px);
    }}
    
    /* ESTADÍSTICAS */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 25px;
    }}
    
    .stat-card {{
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }}
    
    .stat-value {{
        font-size: 2rem;
        font-weight: 700;
        margin: 10px 0;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    /* BOTONES DE ACCIÓN */
    .action-buttons {{
        display: flex;
        gap: 15px;
        margin-top: 30px;
        justify-content: center;
        flex-wrap: wrap;
    }}
    
    .btn-primary {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Segoe UI', system-ui, sans-serif;
        text-decoration: none;
        display: inline-block;
        text-align: center;
    }}
    
    .btn-primary:hover {{
        background: #e55a1a;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(243, 112, 33, 0.3);
    }}
    
    .btn-secondary {{
        background: white;
        color: {PRIMARY_COLOR};
        border: 2px solid {PRIMARY_COLOR};
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    
    .btn-secondary:hover {{
        background: #fff9f5;
        transform: translateY(-2px);
    }}
    
    /* MODAL DE DETALLES */
    .modal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
        padding: 20px;
    }}
    
    .modal-content {{
        background: white;
        border-radius: 15px;
        padding: 30px;
        max-width: 500px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
        position: relative;
        animation: modalSlide 0.3s ease;
    }}
    
    @keyframes modalSlide {{
        from {{ transform: translateY(-30px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    .modal-close {{
        position: absolute;
        top: 15px;
        right: 15px;
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: #666;
    }}
    
    /* RESPONSIVE PARA MÓVIL */
    @media (max-width: 768px) {{
        .main-content {{ padding: 15px; }}
        .dashboard-grid {{ grid-template-columns: 1fr; gap: 15px; }}
        .calendar-grid {{ grid-template-columns: repeat(7, 1fr); }}
        .calendar-day {{ min-height: 80px; padding: 5px; }}
        .day-header {{ padding: 10px 2px; font-size: 0.8rem; }}
        .day-number {{ font-size: 0.9rem; }}
        .event-badge {{ font-size: 0.7rem; padding: 3px 5px; }}
        .nav-btn {{ padding: 10px 15px; font-size: 0.9rem; }}
        .current-month {{ font-size: 1.4rem; }}
        .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
        .action-buttons {{ flex-direction: column; }}
        .btn-primary, .btn-secondary {{ width: 100%; }}
    }}
    
    @media (max-width: 480px) {{
        .main-header {{ padding: 10px 15px; }}
        .logo-container {{ font-size: 1.1rem; }}
        .user-info {{ font-size: 0.8rem; }}
        .calendar-grid {{ grid-template-columns: repeat(7, 1fr); }}
        .calendar-day {{ min-height: 70px; }}
        .stats-grid {{ grid-template-columns: 1fr; }}
    }}
    
    /* OCULTAR ELEMENTOS DE STREAMLIT */
    [data-testid="stHeader"] {{ display: none !important; }}
    footer {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    
    /* SCROLLBAR PERSONALIZADO */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: #f1f1f1; }}
    ::-webkit-scrollbar-thumb {{ background: {PRIMARY_COLOR}; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #e55a1a; }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES DE LA APLICACIÓN
# ----------------------------
def create_header():
    """Crea el encabezado de la aplicación"""
    st.markdown(f"""
    <div class="main-header">
        <div class="logo-container">
            <span>🛟</span>
            <span>SOCORRISTA PRO</span>
        </div>
        <div class="user-info">
            <div class="user-badge">
                <span>👤</span>
                <span>Carlos Rodríguez</span>
                <span style="opacity: 0.8; font-size: 0.85rem;">Socorrista Principal</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_dashboard():
    """Crea el dashboard principal"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Título del dashboard
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 10px; font-family: 'Segoe UI', sans-serif;">
            🏊 Panel de Control
        </h1>
        <p style="color: #666; font-size: 1.1rem;">
            Gestiona tus horarios, asistencia y más desde un solo lugar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de tarjetas
    cards = [
        ("Horarios", "📅", "Consulta y gestiona tus turnos programados", "horarios"),
        ("Control de Asistencia", "✅", "Registro de entrada y salida en tiempo real", "asistencia"),
        ("Nómina y Pagos", "💰", "Consulta tus recibos y estados de pago", "nomina"),
        ("Incidencias", "⚠️", "Reporta y consulta incidencias", "incidencias"),
        ("Formación", "🎓", "Accede a cursos y certificaciones", "formacion"),
        ("Comunicados", "📢", "Últimas noticias y anuncios", "comunicados"),
    ]
    
    # Crear grid de tarjetas
    cols = st.columns(3)
    for idx, (title, icon, desc, view) in enumerate(cards):
        with cols[idx % 3]:
            card_html = f"""
            <a href="?view={view}" class="dashboard-card">
                <div class="card-icon">{icon}</div>
                <h3 class="card-title">{title}</h3>
                <p class="card-desc">{desc}</p>
            </a>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    
    # Estadísticas rápidas
    st.markdown(f"""
    <div style="margin-top: 40px; background: white; border-radius: 15px; padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
        <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif;">
            📊 Resumen Rápido
        </h3>
        <div class="stats-grid">
            <div class="stat-card" style="border-left: 4px solid #4CAF50;">
                <div style="color: #4CAF50; font-size: 1.2rem;">✅</div>
                <div class="stat-value" style="color: #4CAF50;">12</div>
                <div style="color: #666; font-size: 0.9rem;">Turnos Completados</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid #2196F3;">
                <div style="color: #2196F3; font-size: 1.2rem;">⏰</div>
                <div class="stat-value" style="color: #2196F3;">96h</div>
                <div style="color: #666; font-size: 0.9rem;">Horas Totales</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid #FF9800;">
                <div style="color: #FF9800; font-size: 1.2rem;">📅</div>
                <div class="stat-value" style="color: #FF9800;">6</div>
                <div style="color: #666; font-size: 0.9rem;">Próximos Turnos</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid #9C27B0;">
                <div style="color: #9C27B0; font-size: 1.2rem;">💰</div>
                <div class="stat-value" style="color: #9C27B0;">€2,850</div>
                <div style="color: #666; font-size: 0.9rem;">Salario Estimado</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_calendar():
    """Crea y muestra el calendario interactivo"""
    # Inicializar estado del calendario
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = datetime.datetime.now().month
        st.session_state.calendar_year = datetime.datetime.now().year
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = None
    
    # Navegación del calendario
    current_date = datetime.date(st.session_state.calendar_year, st.session_state.calendar_month, 1)
    month_name = current_date.strftime("%B %Y").upper()
    
    # Crear interfaz del calendario
    st.markdown('<div class="calendar-page">', unsafe_allow_html=True)
    
    # Cabecera con navegación
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Mes Anterior", use_container_width=True):
            prev_month = current_date - relativedelta(months=1)
            st.session_state.calendar_month = prev_month.month
            st.session_state.calendar_year = prev_month.year
            st.rerun()
    
    with col2:
        st.markdown(f'<div class="current-month">{month_name}</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("Siguiente Mes →", use_container_width=True):
            next_month = current_date + relativedelta(months=1)
            st.session_state.calendar_month = next_month.month
            st.session_state.calendar_year = next_month.year
            st.rerun()
    
    # Generar grid del calendario
    first_day = current_date
    last_day = datetime.date(st.session_state.calendar_year, 
                           st.session_state.calendar_month, 
                           calendar.monthrange(st.session_state.calendar_year, 
                                             st.session_state.calendar_month)[1])
    
    # Cabeceras de días
    days_of_week = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
    
    st.markdown('<div class="calendar-grid">', unsafe_allow_html=True)
    
    # Mostrar cabeceras
    for day in days_of_week:
        st.markdown(f'<div class="day-header">{day}</div>', unsafe_allow_html=True)
    
    # Espacios en blanco para el primer día
    first_weekday = (first_day.weekday() + 1) % 7  # Lunes = 0
    for _ in range(first_weekday):
        st.markdown('<div class="calendar-day"></div>', unsafe_allow_html=True)
    
    # Días del mes
    current_day = first_day
    while current_day <= last_day:
        day_class = "calendar-day"
        
        # Verificar si es fin de semana
        if current_day.weekday() >= 5:
            day_class += " weekend"
        
        # Verificar si es hoy
        if current_day == datetime.date.today():
            day_class += " today"
        
        # Verificar si tiene eventos
        date_str = current_day.strftime("%Y-%m-%d")
        has_events = date_str in SAMPLE_SCHEDULE
        if has_events:
            day_class += " has-events"
        
        # Crear el día
        day_html = f'<div class="{day_class}">'
        day_html += f'<div class="day-number">{current_day.day}</div>'
        
        # Mostrar eventos si existen
        if has_events:
            for schedule in SAMPLE_SCHEDULE[date_str]:
                schedule_json = str(schedule).replace("'", '"')
                day_html += f"""
                <div class="event-badge" onclick="
                    document.getElementById('selected-date').textContent = '{date_str}';
                    document.getElementById('selected-time').textContent = '{schedule['hora']}';
                    document.getElementById('selected-type').textContent = '{schedule['tipo']}';
                    document.getElementById('selected-person').textContent = '{schedule['socorrista']}';
                    document.getElementById('event-modal').style.display = 'flex';
                ">
                    {schedule['hora'].split('-')[0]}
                </div>
                """
        
        day_html += '</div>'
        st.markdown(day_html, unsafe_allow_html=True)
        
        current_day += datetime.timedelta(days=1)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Estadísticas del mes
    total_turnos = sum(1 for date in SAMPLE_SCHEDULE 
                      if datetime.datetime.strptime(date, "%Y-%m-%d").date().month == st.session_state.calendar_month)
    
    st.markdown(f"""
    <div style="margin-top: 30px; background: white; border-radius: 15px; padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
        <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif;">
            📈 Resumen del Mes
        </h3>
        <div class="stats-grid">
            <div class="stat-card">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.2rem;">📅</div>
                <div class="stat-value">{total_turnos}</div>
                <div style="color: #666; font-size: 0.9rem;">Turnos Programados</div>
            </div>
            <div class="stat-card">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.2rem;">⏰</div>
                <div class="stat-value">{total_turnos * 6}h</div>
                <div style="color: #666; font-size: 0.9rem;">Horas Totales</div>
            </div>
            <div class="stat-card">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.2rem;">👥</div>
                <div class="stat-value">5</div>
                <div style="color: #666; font-size: 0.9rem;">Socorristas Activos</div>
            </div>
            <div class="stat-card">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.2rem;">✅</div>
                <div class="stat-value">{total_turnos - 2}</div>
                <div style="color: #666; font-size: 0.9rem;">Turnos Cubiertos</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de acción
    st.markdown("""
    <div class="action-buttons">
        <a href="?" class="btn-primary">← Volver al Dashboard</a>
        <button class="btn-secondary" onclick="window.print()">🖨️ Imprimir Horario</button>
        <button class="btn-secondary" onclick="alert('Generando PDF...')">📄 Exportar PDF</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Modal para detalles del evento
    st.markdown("""
    <div id="event-modal" class="modal-overlay" style="display: none;">
        <div class="modal-content">
            <button class="modal-close" onclick="document.getElementById('event-modal').style.display='none'">×</button>
            <h3 style="color: #F37021; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
                📋 Detalles del Turno
            </h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                    <div>
                        <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">📅 Fecha</div>
                        <div style="font-weight: 700; color: #333;" id="selected-date"></div>
                    </div>
                    <div>
                        <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">🕒 Horario</div>
                        <div style="font-weight: 700; color: #333;" id="selected-time"></div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                    <div>
                        <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">🏷️ Tipo</div>
                        <div style="font-weight: 700; color: #333;" id="selected-type"></div>
                    </div>
                    <div>
                        <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">👤 Socorrista</div>
                        <div style="font-weight: 700; color: #333;" id="selected-person"></div>
                    </div>
                </div>
                <div>
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">📍 Ubicación</div>
                    <div style="font-weight: 700; color: #333;">Piscina Municipal Central</div>
                    <div style="color: #666; font-size: 0.85rem; margin-top: 3px;">Av. Deportes, 123</div>
                </div>
            </div>
            <div style="display: flex; gap: 10px;">
                <button class="btn-primary" style="flex: 1;" onclick="alert('Cambio solicitado')">🔄 Solicitar Cambio</button>
                <button class="btn-secondary" style="flex: 1;" onclick="document.getElementById('event-modal').style.display='none'">Cerrar</button>
            </div>
        </div>
    </div>
    
    <script>
    // Asegurar que los enlaces funcionen correctamente
    document.querySelectorAll('a[href^="?view="]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = this.getAttribute('href');
        });
    });
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_other_view(view_name):
    """Crea vistas para otras secciones"""
    view_titles = {
        "asistencia": "Control de Asistencia",
        "nomina": "Nómina y Pagos",
        "incidencias": "Reporte de Incidencias",
        "formacion": "Formación y Certificaciones",
        "comunicados": "Comunicados y Noticias"
    }
    
    title = view_titles.get(view_name, view_name.capitalize())
    icon = {
        "asistencia": "✅",
        "nomina": "💰",
        "incidencias": "⚠️",
        "formacion": "🎓",
        "comunicados": "📢"
    }.get(view_name, "📋")
    
    st.markdown(f"""
    <div class="main-content">
        <div style="max-width: 800px; margin: 0 auto;">
            <div style="text-align: center; margin-bottom: 40px;">
                <div style="font-size: 3rem; margin-bottom: 15px;">{icon}</div>
                <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 10px; font-family: 'Segoe UI', sans-serif;">
                    {title}
                </h1>
                <p style="color: #666; font-size: 1.1rem;">
                    Esta funcionalidad está en desarrollo activo
                </p>
            </div>
            
            <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); margin-bottom: 30px;">
                <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif;">
                    🚀 Próximamente
                </h3>
                <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">
                    Estamos trabajando arduamente para implementar esta funcionalidad. 
                    En las próximas semanas podrás acceder a todas las características de {title.lower()}.
                </p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 25px;">
                    <h4 style="color: {PRIMARY_COLOR}; margin-bottom: 15px;">📅 Cronograma de Lanzamiento</h4>
                    <ul style="color: #666; line-height: 1.8; padding-left: 20px;">
                        <li><strong>Fase 1:</strong> Diseño y planificación (Completado)</li>
                        <li><strong>Fase 2:</strong> Desarrollo del backend (En progreso)</li>
                        <li><strong>Fase 3:</strong> Pruebas y ajustes (Próximamente)</li>
                        <li><strong>Fase 4:</strong> Lanzamiento oficial (Febrero 2024)</li>
                    </ul>
                </div>
            </div>
            
            <div class="action-buttons">
                <a href="?" class="btn-primary">← Volver al Dashboard</a>
                <button class="btn-secondary" onclick="alert('Te notificaremos cuando esté disponible')">
                    🔔 Notificarme
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# APLICACIÓN PRINCIPAL
# ----------------------------
def main():
    """Función principal de la aplicación"""
    # Aplicar CSS personalizado
    apply_custom_css()
    
    # Crear header fijo
    create_header()
    
    # Obtener vista actual
    query_params = st.query_params.to_dict()
    view = query_params.get("view", [""])[0] if query_params.get("view") else ""
    
    # Mostrar vista correspondiente
    if view == "horarios":
        create_calendar()
    elif view in ["asistencia", "nomina", "incidencias", "formacion", "comunicados"]:
        create_other_view(view)
    else:
        create_dashboard()
    
    # Footer
    current_year = datetime.datetime.now().year
    st.markdown(f"""
    <div style="padding: 20px; text-align: center; color: #666; font-size: 0.9rem; margin-top: 40px;">
        <p>© {current_year} Socorrista Pro • Versión 2.1 • Todos los derechos reservados</p>
        <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px;">
            Sistema optimizado para Chrome, Firefox y Safari • Soporte técnico: soporte@socorristapro.com
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
