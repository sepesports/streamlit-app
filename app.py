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

# Colores corporativos
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
# ESTILOS CSS OPTIMIZADOS
# ----------------------------
def apply_custom_css():
    """Aplica estilos CSS personalizados sin espacios en blanco"""
    st.markdown(f"""
    <style>
    /* RESET TOTAL - SIN ESPACIOS BLANCOS */
    html, body, #root, [class*="ViewContainer"] {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        overflow-x: hidden !important;
    }}
    
    /* Contenedor principal SIN márgenes */
    .stApp {{
        background: {BG_COLOR} !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 100vh !important;
    }}
    
    /* Eliminar TODOS los espacios de Streamlit */
    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }}
    
    [data-testid="stMainBlockContainer"] {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }}
    
    .main .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }}
    
    /* HEADER COMPACTO */
    .main-header {{
        background: {SECONDARY_COLOR};
        color: white;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: relative;
        z-index: 100;
    }}
    
    .logo-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.3rem;
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
    
    /* CONTENIDO PRINCIPAL - SIN ESPACIOS */
    .main-content {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100%;
    }}
    
    /* TÍTULO PRINCIPAL COMPACTO */
    .page-title-section {{
        background: white;
        padding: 25px 20px;
        text-align: center;
        border-bottom: 3px solid {PRIMARY_COLOR};
        margin-bottom: 0;
    }}
    
    .page-title {{
        color: {SECONDARY_COLOR};
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 8px;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .page-subtitle {{
        color: #666;
        font-size: 1.1rem;
        font-family: 'Segoe UI', sans-serif;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.4;
    }}
    
    /* GRID DE TARJETAS - COMPACTO */
    .dashboard-container {{
        padding: 25px 20px;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        box-sizing: border-box;
    }}
    
    /* DESKTOP: 3 columnas x 2 filas */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        width: 100%;
    }}
    
    /* TARJETAS COMPACTAS */
    .dashboard-card {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(0,0,0,0.05);
        text-decoration: none !important;
        display: block;
        height: 100%;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        border-color: {PRIMARY_COLOR};
    }}
    
    .card-icon {{
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        font-size: 26px;
        color: white;
    }}
    
    .card-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin-bottom: 8px;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .card-desc {{
        color: #666;
        font-size: 0.9rem;
        line-height: 1.4;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    /* ESTADÍSTICAS COMPACTAS */
    .stats-container {{
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 25px auto 0;
        max-width: 1200px;
        width: calc(100% - 40px);
        box-sizing: border-box;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        width: 100%;
    }}
    
    .stat-card {{
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-left: 4px solid;
        transition: transform 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-2px);
    }}
    
    .stat-value {{
        font-size: 1.8rem;
        font-weight: 700;
        margin: 8px 0;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    /* CALENDARIO OPTIMIZADO */
    .calendar-container {{
        padding: 25px 20px;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        box-sizing: border-box;
    }}
    
    .calendar-header {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    .month-navigation {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        flex-wrap: wrap;
        gap: 10px;
    }}
    
    .nav-btn {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .nav-btn:hover {{
        background: #e55a1a;
        transform: scale(1.03);
    }}
    
    .current-month {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    /* GRID DEL CALENDARIO */
    .calendar-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 2px;
        background: #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
        border: 2px solid #e0e0e0;
    }}
    
    .day-header {{
        background: {SECONDARY_COLOR};
        color: white;
        padding: 12px 5px;
        text-align: center;
        font-weight: 600;
        font-size: 0.85rem;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .calendar-day {{
        background: white;
        min-height: 100px;
        padding: 8px;
        position: relative;
        transition: all 0.3s;
    }}
    
    .calendar-day:hover {{
        background: #fff9f5;
    }}
    
    .day-number {{
        font-size: 1rem;
        font-weight: 600;
        color: {SECONDARY_COLOR};
        margin-bottom: 6px;
        font-family: 'Segoe UI', sans-serif;
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
        border-left: 3px solid {PRIMARY_COLOR};
    }}
    
    .event-badge {{
        background: {PRIMARY_COLOR};
        color: white;
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        margin-top: 4px;
        display: block;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .event-badge:hover {{
        background: #e55a1a;
    }}
    
    /* BOTONES COMPACTOS */
    .action-buttons {{
        display: flex;
        gap: 12px;
        margin-top: 25px;
        justify-content: center;
        flex-wrap: wrap;
    }}
    
    .btn-primary {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Segoe UI', sans-serif;
        text-decoration: none;
        display: inline-block;
        text-align: center;
    }}
    
    .btn-primary:hover {{
        background: #e55a1a;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(243, 112, 33, 0.3);
    }}
    
    .btn-secondary {{
        background: white;
        color: {PRIMARY_COLOR};
        border: 2px solid {PRIMARY_COLOR};
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .btn-secondary:hover {{
        background: #fff9f5;
        transform: translateY(-2px);
    }}
    
    /* MODAL COMPACTO */
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
        padding: 15px;
    }}
    
    .modal-content {{
        background: white;
        border-radius: 12px;
        padding: 25px;
        max-width: 500px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
        position: relative;
        animation: modalSlide 0.3s ease;
    }}
    
    @keyframes modalSlide {{
        from {{ transform: translateY(-20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    .modal-close {{
        position: absolute;
        top: 12px;
        right: 12px;
        background: none;
        border: none;
        font-size: 1.3rem;
        cursor: pointer;
        color: #666;
    }}
    
    /* RESPONSIVE PARA MÓVIL - 2 columnas x 3 filas */
    @media (max-width: 768px) {{
        .main-header {{
            padding: 12px 15px;
        }}
        
        .logo-container {{
            font-size: 1.1rem;
        }}
        
        .user-info {{
            font-size: 0.8rem;
        }}
        
        .page-title-section {{
            padding: 20px 15px;
        }}
        
        .page-title {{
            font-size: 1.6rem;
        }}
        
        .page-subtitle {{
            font-size: 1rem;
            padding: 0 10px;
        }}
        
        .dashboard-container {{
            padding: 20px 15px;
        }}
        
        /* MÓVIL: 2 columnas x 3 filas */
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 15px;
        }}
        
        .dashboard-card {{
            min-height: 150px;
            padding: 18px;
        }}
        
        .card-icon {{
            width: 50px;
            height: 50px;
            font-size: 22px;
            margin-bottom: 12px;
        }}
        
        .card-title {{
            font-size: 1.1rem;
        }}
        
        .card-desc {{
            font-size: 0.85rem;
        }}
        
        .stats-container {{
            padding: 20px;
            margin: 20px auto 0;
            width: calc(100% - 30px);
        }}
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        
        .stat-card {{
            padding: 12px;
        }}
        
        .stat-value {{
            font-size: 1.5rem;
        }}
        
        .calendar-container {{
            padding: 20px 15px;
        }}
        
        .calendar-day {{
            min-height: 80px;
            padding: 6px;
        }}
        
        .day-header {{
            padding: 10px 3px;
            font-size: 0.8rem;
        }}
        
        .day-number {{
            font-size: 0.9rem;
        }}
        
        .event-badge {{
            font-size: 0.7rem;
            padding: 2px 4px;
        }}
        
        .nav-btn {{
            padding: 8px 15px;
            font-size: 0.9rem;
        }}
        
        .current-month {{
            font-size: 1.3rem;
        }}
        
        .action-buttons {{
            flex-direction: column;
            gap: 10px;
        }}
        
        .btn-primary, .btn-secondary {{
            width: 100%;
            padding: 10px 18px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 12px;
        }}
        
        .dashboard-card {{
            min-height: 140px;
            padding: 15px;
        }}
        
        .card-icon {{
            width: 45px;
            height: 45px;
            font-size: 20px;
        }}
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .calendar-day {{
            min-height: 70px;
        }}
    }}
    
    /* OCULTAR ELEMENTOS DE STREAMLIT */
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    
    footer {{
        display: none !important;
    }}
    
    .stDeployButton {{
        display: none !important;
    }}
    
    /* ANIMACIONES SUTILES */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.4s ease-out;
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES DE LA APLICACIÓN
# ----------------------------
def create_header():
    """Crea el encabezado compacto"""
    st.markdown(f"""
    <div class="main-header fade-in">
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
    """Crea el dashboard principal compacto"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Título principal compacto
    st.markdown(f"""
    <div class="page-title-section fade-in">
        <h1 class="page-title">Panel de Control</h1>
        <p class="page-subtitle">Gestiona tus horarios, asistencia y más desde un solo lugar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de tarjetas - Desktop: 3 columnas x 2 filas, Móvil: 2 columnas x 3 filas
    st.markdown('<div class="dashboard-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    cards = [
        ("Horarios", "📅", "Consulta y gestiona tus turnos programados", "horarios"),
        ("Control de Asistencia", "✅", "Registro de entrada y salida en tiempo real", "asistencia"),
        ("Nómina y Pagos", "💰", "Consulta tus recibos y estados de pago", "nomina"),
        ("Incidencias", "⚠️", "Reporta y consulta incidencias", "incidencias"),
        ("Formación", "🎓", "Accede a cursos y certificaciones", "formacion"),
        ("Comunicados", "📢", "Últimas noticias y anuncios", "comunicados"),
    ]
    
    for title, icon, desc, view in cards:
        card_html = f"""
        <a href="?view={view}" class="dashboard-card">
            <div class="card-icon">{icon}</div>
            <h3 class="card-title">{title}</h3>
            <p class="card-desc">{desc}</p>
        </a>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Estadísticas rápidas compactas
    st.markdown(f"""
    <div class="stats-container fade-in">
        <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-family: 'Segoe UI', sans-serif; font-size: 1.3rem;">
            📊 Resumen Rápido
        </h3>
        <div class="stats-grid">
            <div class="stat-card" style="border-left-color: #4CAF50;">
                <div style="color: #4CAF50; font-size: 1.1rem;">✅</div>
                <div class="stat-value" style="color: #4CAF50;">12</div>
                <div style="color: #666; font-size: 0.85rem;">Turnos Completados</div>
            </div>
            <div class="stat-card" style="border-left-color: #2196F3;">
                <div style="color: #2196F3; font-size: 1.1rem;">⏰</div>
                <div class="stat-value" style="color: #2196F3;">96h</div>
                <div style="color: #666; font-size: 0.85rem;">Horas Totales</div>
            </div>
            <div class="stat-card" style="border-left-color: #FF9800;">
                <div style="color: #FF9800; font-size: 1.1rem;">📅</div>
                <div class="stat-value" style="color: #FF9800;">6</div>
                <div style="color: #666; font-size: 0.85rem;">Próximos Turnos</div>
            </div>
            <div class="stat-card" style="border-left-color: #9C27B0;">
                <div style="color: #9C27B0; font-size: 1.1rem;">💰</div>
                <div class="stat-value" style="color: #9C27B0;">€2,850</div>
                <div style="color: #666; font-size: 0.85rem;">Salario Estimado</div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin: 25px auto; padding: 0 20px; max-width: 1200px;">
        <p style="color: #666; font-size: 0.85rem;">
            © {datetime.datetime.now().year} Socorrista Pro • Versión 2.1
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_calendar():
    """Crea y muestra el calendario interactivo compacto"""
    # Inicializar estado del calendario
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = datetime.datetime.now().month
        st.session_state.calendar_year = datetime.datetime.now().year
    
    # Navegación del calendario
    current_date = datetime.date(st.session_state.calendar_year, st.session_state.calendar_month, 1)
    month_name = current_date.strftime("%B %Y").upper()
    
    # Crear interfaz del calendario
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="calendar-container fade-in">', unsafe_allow_html=True)
    
    # Cabecera con navegación
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Mes Anterior", use_container_width=True, type="primary"):
            prev_month = current_date - relativedelta(months=1)
            st.session_state.calendar_month = prev_month.month
            st.session_state.calendar_year = prev_month.year
            st.rerun()
    
    with col2:
        st.markdown(f'<div class="current-month">{month_name}</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("Siguiente Mes →", use_container_width=True, type="primary"):
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
    <div style="margin-top: 25px; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-family: 'Segoe UI', sans-serif; font-size: 1.3rem;">
            📈 Resumen del Mes
        </h3>
        <div class="stats-grid">
            <div class="stat-card" style="border-left-color: {PRIMARY_COLOR};">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.1rem;">📅</div>
                <div class="stat-value" style="color: {PRIMARY_COLOR};">{total_turnos}</div>
                <div style="color: #666; font-size: 0.85rem;">Turnos Programados</div>
            </div>
            <div class="stat-card" style="border-left-color: {PRIMARY_COLOR};">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.1rem;">⏰</div>
                <div class="stat-value" style="color: {PRIMARY_COLOR};">{total_turnos * 6}h</div>
                <div style="color: #666; font-size: 0.85rem;">Horas Totales</div>
            </div>
            <div class="stat-card" style="border-left-color: {PRIMARY_COLOR};">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.1rem;">👥</div>
                <div class="stat-value" style="color: {PRIMARY_COLOR};">5</div>
                <div style="color: #666; font-size: 0.85rem;">Socorristas Activos</div>
            </div>
            <div class="stat-card" style="border-left-color: {PRIMARY_COLOR};">
                <div style="color: {PRIMARY_COLOR}; font-size: 1.1rem;">✅</div>
                <div class="stat-value" style="color: {PRIMARY_COLOR};">{total_turnos - 2}</div>
                <div style="color: #666; font-size: 0.85rem;">Turnos Cubiertos</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de acción
    st.markdown("""
    <div class="action-buttons">
        <a href="?" class="btn-primary">← Volver al Dashboard</a>
        <button class="btn-secondary" onclick="window.print()">🖨️ Imprimir Horario</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Modal para detalles del evento
    st.markdown("""
    <div id="event-modal" class="modal-overlay" style="display: none;">
        <div class="modal-content">
            <button class="modal-close" onclick="document.getElementById('event-modal').style.display='none'">×</button>
            <h3 style="color: #F37021; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; font-size: 1.4rem;">
                📋 Detalles del Turno
            </h3>
            <div style="background: #f8f9fa; padding: 18px; border-radius: 8px; margin-bottom: 18px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                    <div>
                        <div style="color: #666; font-size: 0.85rem; margin-bottom: 4px;">📅 Fecha</div>
                        <div style="font-weight: 700; color: #333;" id="selected-date"></div>
                    </div>
                    <div>
                        <div style="color: #666; font-size: 0.85rem; margin-bottom: 4px;">🕒 Horario</div>
                        <div style="font-weight: 700; color: #333;" id="selected-time"></div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                    <div>
                        <div style="color: #666; font-size: 0.85rem; margin-bottom: 4px;">🏷️ Tipo</div>
                        <div style="font-weight: 700; color: #333;" id="selected-type"></div>
                    </div>
                    <div>
                        <div style="color: #666; font-size: 0.85rem; margin-bottom: 4px;">👤 Socorrista</div>
                        <div style="font-weight: 700; color: #333;" id="selected-person"></div>
                    </div>
                </div>
                <div>
                    <div style="color: #666; font-size: 0.85rem; margin-bottom: 4px;">📍 Ubicación</div>
                    <div style="font-weight: 700; color: #333;">Piscina Municipal Central</div>
                    <div style="color: #666; font-size: 0.8rem; margin-top: 3px;">Av. Deportes, 123</div>
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
    
    st.markdown('</div></div>', unsafe_allow_html=True)

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
        <div class="fade-in" style="max-width: 800px; margin: 0 auto; padding: 25px 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 2.5rem; margin-bottom: 12px;">{icon}</div>
                <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 8px; font-family: 'Segoe UI', sans-serif; font-size: 1.8rem;">
                    {title}
                </h1>
                <p style="color: #666; font-size: 1rem;">
                    Esta funcionalidad está en desarrollo activo
                </p>
            </div>
            
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 25px;">
                <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-family: 'Segoe UI', sans-serif; font-size: 1.3rem;">
                    🚀 Próximamente
                </h3>
                <p style="color: #666; line-height: 1.5; margin-bottom: 15px; font-size: 0.95rem;">
                    Estamos trabajando arduamente para implementar esta funcionalidad. 
                    En las próximas semanas podrás acceder a todas las características de {title.lower()}.
                </p>
                
                <div style="background: #f8f9fa; padding: 18px; border-radius: 8px; margin-top: 20px;">
                    <h4 style="color: {PRIMARY_COLOR}; margin-bottom: 12px; font-size: 1.1rem;">📅 Cronograma de Lanzamiento</h4>
                    <ul style="color: #666; line-height: 1.6; padding-left: 18px; font-size: 0.9rem;">
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
    
    # Crear header compacto
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

if __name__ == "__main__":
    main()
