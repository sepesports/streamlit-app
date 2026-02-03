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
    """Aplica estilos CSS personalizados"""
    css = f"""
    <style>
    /* RESET TOTAL */
    html, body, #root, [class*="ViewContainer"] {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        overflow-x: hidden !important;
    }}
    
    /* Contenedor principal */
    .stApp {{
        background: {BG_COLOR} !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 100vh !important;
    }}
    
    /* Eliminar espacios de Streamlit */
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
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 15px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    
    .logo-container {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.3rem;
        font-weight: 700;
    }}
    
    .user-info {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 0.9rem;
    }}
    
    .user-badge {{
        background: rgba(255,255,255,0.15);
        padding: 8px 16px;
        border-radius: 25px;
        display: flex;
        align-items: center;
        gap: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    /* CONTENIDO PRINCIPAL */
    .main-content {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100%;
    }}
    
    /* TÍTULO CON FONDO PROFESIONAL */
    .page-title-section {{
        background: linear-gradient(135deg, 
            #1a5276, 
            #1c5c82, 
            #1e6790, 
            {PRIMARY_COLOR});
        padding: 40px 25px;
        text-align: center;
        margin-bottom: 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(26, 82, 118, 0.2);
    }}
    
    .page-title {{
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 15px;
        font-family: 'Montserrat', 'Segoe UI', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        letter-spacing: 0.5px;
    }}
    
    .page-subtitle {{
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        font-family: 'Segoe UI', sans-serif;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
        position: relative;
        z-index: 1;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        font-weight: 300;
    }}
    
    /* GRID DE TARJETAS - CORREGIDO */
    .dashboard-container {{
        padding: 40px 25px;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        box-sizing: border-box;
    }}
    
    /* DESKTOP: 3 columnas x 2 filas */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        width: 100%;
    }}
    
    /* TARJETAS PROFESIONALES */
    .dashboard-card {{
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        border: none;
        text-decoration: none !important;
        display: block;
        height: 100%;
        min-height: 220px;
        position: relative;
        overflow: hidden;
        color: inherit;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(243, 112, 33, 0.25);
        text-decoration: none !important;
    }}
    
    .card-icon {{
        width: 75px;
        height: 75px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        font-size: 32px;
        color: white;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(243, 112, 33, 0.2);
    }}
    
    .card-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin-bottom: 12px;
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.3;
    }}
    
    .card-desc {{
        color: #666;
        font-size: 1rem;
        line-height: 1.5;
        font-family: 'Segoe UI', sans-serif;
        opacity: 0.9;
    }}
    
    /* Línea decorativa superior */
    .dashboard-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, #FF8C42);
        border-radius: 20px 20px 0 0;
    }}
    
    /* RESPONSIVE PARA MÓVIL - 2 columnas x 3 filas */
    @media (max-width: 992px) {{
        .main-header {{
            padding: 12px 20px;
        }}
        
        .logo-container {{
            font-size: 1.1rem;
        }}
        
        .user-info {{
            font-size: 0.8rem;
        }}
        
        .page-title-section {{
            padding: 30px 20px;
        }}
        
        .page-title {{
            font-size: 2.2rem;
        }}
        
        .page-subtitle {{
            font-size: 1.1rem;
            padding: 0 15px;
        }}
        
        .dashboard-container {{
            padding: 30px 20px;
        }}
        
        /* MÓVIL: 2 columnas x 3 filas */
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        
        .dashboard-card {{
            min-height: 200px;
            padding: 22px;
        }}
        
        .card-icon {{
            width: 65px;
            height: 65px;
            font-size: 28px;
            margin-bottom: 18px;
        }}
        
        .card-title {{
            font-size: 1.2rem;
        }}
        
        .card-desc {{
            font-size: 0.95rem;
        }}
    }}
    
    @media (max-width: 576px) {{
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}
        
        .dashboard-card {{
            min-height: 180px;
            padding: 18px;
        }}
        
        .card-icon {{
            width: 55px;
            height: 55px;
            font-size: 24px;
        }}
        
        .card-title {{
            font-size: 1.1rem;
        }}
        
        .card-desc {{
            font-size: 0.9rem;
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
    
    /* ANIMACIONES */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES DE LA APLICACIÓN
# ----------------------------
def create_header():
    """Crea el encabezado profesional"""
    st.markdown(f"""
    <div class="main-header fade-in">
        <div class="logo-container">
            <span style="font-size: 1.5rem;">🛟</span>
            <span>SOCORRISTA PRO</span>
        </div>
        <div class="user-info">
            <div class="user-badge">
                <span style="font-size: 1.1rem;">👤</span>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                    <span style="font-weight: 600;">Carlos Rodríguez</span>
                    <span style="font-size: 0.8rem; opacity: 0.9;">Socorrista Principal</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_dashboard_grid():
    """Crea el grid de tarjetas del dashboard"""
    # Tarjetas del dashboard
    cards = [
        ("Horarios", "📅", "Consulta y gestiona tus turnos programados"),
        ("Control de Asistencia", "✅", "Registro de entrada y salida en tiempo real"),
        ("Nómina y Pagos", "💰", "Consulta tus recibos y estados de pago"),
        ("Incidencias", "⚠️", "Reporta y consulta incidencias"),
        ("Formación", "🎓", "Accede a cursos y certificaciones"),
        ("Comunicados", "📢", "Últimas noticias y anuncios"),
    ]
    
    # Crear el HTML del grid
    grid_html = '<div class="dashboard-grid">'
    
    for title, icon, desc in cards:
        if title == "Horarios":
            grid_html += f'''
            <div class="dashboard-card" onclick="openCalendarModal()" style="cursor: pointer;">
                <div class="card-icon">{icon}</div>
                <h3 class="card-title">{title}</h3>
                <p class="card-desc">{desc}</p>
            </div>
            '''
        else:
            # Convertir título a formato de URL
            view_name = title.lower().replace(" ", "").replace("ó", "o").replace("í", "i")
            if "control" in view_name:
                view_name = "asistencia"
            elif "nómina" in view_name:
                view_name = "nomina"
            
            grid_html += f'''
            <a href="?view={view_name}" class="dashboard-card">
                <div class="card-icon">{icon}</div>
                <h3 class="card-title">{title}</h3>
                <p class="card-desc">{desc}</p>
            </a>
            '''
    
    grid_html += '</div>'
    
    return grid_html

def create_calendar_modal():
    """Crea el modal del calendario"""
    # Estado para el mes actual
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = datetime.datetime.now().month
        st.session_state.calendar_year = datetime.datetime.now().year
    
    current_date = datetime.date(st.session_state.calendar_year, st.session_state.calendar_month, 1)
    month_name = current_date.strftime("%B %Y").upper()
    
    # Crear grid del calendario
    first_day = current_date
    last_day = datetime.date(st.session_state.calendar_year, 
                           st.session_state.calendar_month, 
                           calendar.monthrange(st.session_state.calendar_year, 
                                             st.session_state.calendar_month)[1])
    
    days_of_week = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
    
    calendar_html = '<div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; background: #e0e0e0; border-radius: 15px; overflow: hidden;">'
    
    # Cabeceras
    for day in days_of_week:
        calendar_html += f'''
        <div style="background: {SECONDARY_COLOR}; color: white; padding: 15px 10px; text-align: center; font-weight: 700;">
            {day}
        </div>
        '''
    
    # Espacios en blanco
    first_weekday = (first_day.weekday() + 1) % 7
    for _ in range(first_weekday):
        calendar_html += '<div style="background: white; min-height: 100px;"></div>'
    
    # Días del mes
    current_day = first_day
    while current_day <= last_day:
        day_class = "background: white; min-height: 120px; padding: 10px;"
        
        if current_day.weekday() >= 5:
            day_class = "background: #f9f9f9; min-height: 120px; padding: 10px;"
        
        if current_day == datetime.date.today():
            day_class = f"background: rgba(243, 112, 33, 0.1); border: 2px solid {PRIMARY_COLOR}; min-height: 120px; padding: 10px; border-radius: 5px;"
        
        calendar_html += f'<div style="{day_class}">'
        calendar_html += f'<div style="font-weight: 700; color: {SECONDARY_COLOR}; margin-bottom: 8px;">{current_day.day}</div>'
        
        date_str = current_day.strftime("%Y-%m-%d")
        if date_str in SAMPLE_SCHEDULE:
            for schedule in SAMPLE_SCHEDULE[date_str]:
                calendar_html += f'''
                <div style="background: {PRIMARY_COLOR}; color: white; padding: 5px 8px; border-radius: 5px; margin-top: 5px; font-size: 0.85rem;">
                    {schedule['hora']} - {schedule['tipo']}
                </div>
                '''
        
        calendar_html += '</div>'
        current_day += datetime.timedelta(days=1)
    
    calendar_html += '</div>'
    
    modal_html = f'''
    <div id="calendar-modal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); display: none; align-items: center; justify-content: center; z-index: 9999; padding: 20px;">
        <div style="background: white; border-radius: 20px; width: 95%; max-width: 1200px; height: 80vh; overflow: hidden; position: relative;">
            <div style="background: {SECONDARY_COLOR}; color: white; padding: 20px 30px; display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin: 0; font-size: 1.8rem;">📅 Calendario de Turnos - {month_name}</h2>
                <button onclick="closeCalendarModal()" style="background: {PRIMARY_COLOR}; color: white; border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 1.5rem; cursor: pointer;">×</button>
            </div>
            
            <div style="padding: 30px; height: calc(100% - 80px); overflow-y: auto;">
                <div style="margin-bottom: 20px; display: flex; gap: 10px;">
                    <button onclick="changeMonth(-1)" style="background: {PRIMARY_COLOR}; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">
                        ← Mes Anterior
                    </button>
                    <button onclick="changeMonth(1)" style="background: {PRIMARY_COLOR}; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">
                        Siguiente Mes →
                    </button>
                </div>
                
                {calendar_html}
                
                <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 15px;">📊 Resumen del Mes</h3>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; font-weight: 700; color: {PRIMARY_COLOR};">7</div>
                            <div style="color: #666;">Turnos Programados</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; font-weight: 700; color: {PRIMARY_COLOR};">42h</div>
                            <div style="color: #666;">Horas Totales</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; font-weight: 700; color: {PRIMARY_COLOR};">5</div>
                            <div style="color: #666;">Socorristas</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; font-weight: 700; color: {PRIMARY_COLOR};">100%</div>
                            <div style="color: #666;">Disponibilidad</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function openCalendarModal() {{
        document.getElementById('calendar-modal').style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }}
    
    function closeCalendarModal() {{
        document.getElementById('calendar-modal').style.display = 'none';
        document.body.style.overflow = 'auto';
    }}
    
    function changeMonth(direction) {{
        alert('Para navegar entre meses, se requiere integración completa con Streamlit');
    }}
    
    // Cerrar modal con ESC
    document.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape') closeCalendarModal();
    }});
    </script>
    '''
    
    return modal_html

def create_dashboard():
    """Crea el dashboard principal"""
    # Título con fondo profesional
    st.markdown(f"""
    <div class="page-title-section fade-in">
        <h1 class="page-title">Panel de Control</h1>
        <p class="page-subtitle">Gestiona tus horarios, asistencia y más desde un solo lugar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de tarjetas
    st.markdown('<div class="dashboard-container fade-in">', unsafe_allow_html=True)
    st.markdown(create_dashboard_grid(), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Estadísticas
    st.markdown(f"""
    <div style="max-width: 1200px; margin: 40px auto; padding: 0 25px;">
        <div style="background: white; border-radius: 20px; padding: 35px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">
            <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 25px; font-family: 'Segoe UI', sans-serif; font-size: 1.5rem; font-weight: 700;">
                📊 Resumen Rápido
            </h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #4CAF50;">
                    <div style="color: #4CAF50; font-size: 1.3rem;">✅</div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #4CAF50; margin: 10px 0;">12</div>
                    <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Turnos Completados</div>
                </div>
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #2196F3;">
                    <div style="color: #2196F3; font-size: 1.3rem;">⏰</div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #2196F3; margin: 10px 0;">96h</div>
                    <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Horas Totales</div>
                </div>
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #FF9800;">
                    <div style="color: #FF9800; font-size: 1.3rem;">📅</div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #FF9800; margin: 10px 0;">6</div>
                    <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Próximos Turnos</div>
                </div>
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #9C27B0;">
                    <div style="color: #9C27B0; font-size: 1.3rem;">💰</div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #9C27B0; margin: 10px 0;">€2,850</div>
                    <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Salario Estimado</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style="text-align: center; margin: 40px auto 30px; padding: 0 25px; max-width: 1200px;">
        <p style="color: #666; font-size: 0.9rem; opacity: 0.8;">
            © {datetime.datetime.now().year} Socorrista Pro • Versión 2.2 • Todos los derechos reservados
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modal del calendario
    st.markdown(create_calendar_modal(), unsafe_allow_html=True)

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
    <div style="padding: 40px 25px; max-width: 800px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 40px;">
            <div style="font-size: 4rem; margin-bottom: 20px; color: {PRIMARY_COLOR};">{icon}</div>
            <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-family: 'Montserrat', sans-serif; font-size: 2.5rem; font-weight: 800;">
                {title}
            </h1>
            <p style="color: #666; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
                Esta funcionalidad está en desarrollo activo
            </p>
        </div>
        
        <div style="background: white; border-radius: 20px; padding: 40px; box-shadow: 0 15px 40px rgba(0,0,0,0.08); margin-bottom: 35px;">
            <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 25px; font-family: 'Segoe UI', sans-serif; font-size: 1.6rem; font-weight: 700;">
                🚀 Próximamente
            </h3>
            <p style="color: #666; line-height: 1.7; margin-bottom: 25px; font-size: 1.05rem;">
                Estamos trabajando arduamente para implementar esta funcionalidad con los más altos estándares de calidad. 
                En las próximas semanas podrás acceder a todas las características avanzadas de <strong>{title.lower()}</strong>.
            </p>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; margin-top: 30px; border-left: 5px solid {PRIMARY_COLOR};">
                <h4 style="color: {PRIMARY_COLOR}; margin-bottom: 20px; font-size: 1.3rem; font-weight: 700;">📅 Cronograma de Lanzamiento</h4>
                <ul style="color: #666; line-height: 1.8; padding-left: 25px; font-size: 1rem;">
                    <li style="margin-bottom: 12px;"><strong>Fase 1:</strong> Diseño y planificación (Completado)</li>
                    <li style="margin-bottom: 12px;"><strong>Fase 2:</strong> Desarrollo del backend (En progreso)</li>
                    <li style="margin-bottom: 12px;"><strong>Fase 3:</strong> Pruebas y ajustes (Próximamente)</li>
                    <li style="margin-bottom: 12px;"><strong>Fase 4:</strong> Lanzamiento oficial (Febrero 2024)</li>
                </ul>
            </div>
        </div>
        
        <div style="display: flex; gap: 15px; justify-content: center; margin-top: 30px;">
            <a href="?" style="background: {PRIMARY_COLOR}; color: white; border: none; padding: 15px 30px; border-radius: 12px; 
                font-weight: 600; cursor: pointer; text-decoration: none; display: inline-block; text-align: center;">
                ← Volver al Dashboard
            </a>
            <button onclick="alert('Te notificaremos cuando esté disponible. ¡Gracias por tu paciencia!')" 
                style="background: white; color: {PRIMARY_COLOR}; border: 2px solid {PRIMARY_COLOR}; padding: 15px 30px; 
                border-radius: 12px; font-weight: 600; cursor: pointer;">
                🔔 Notificarme
            </button>
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
    
    # Crear header
    create_header()
    
    # Obtener vista actual
    query_params = st.query_params.to_dict()
    view = query_params.get("view", [""])[0] if query_params.get("view") else ""
    
    # Mostrar vista correspondiente
    if view == "horarios":
        # Abrir modal del calendario
        st.markdown('<script>openCalendarModal();</script>', unsafe_allow_html=True)
        create_dashboard()
    elif view in ["asistencia", "nomina", "incidencias", "formacion", "comunicados"]:
        create_other_view(view)
    else:
        create_dashboard()

if __name__ == "__main__":
    main()
