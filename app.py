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
    st.markdown(f"""
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
        background: {SECONDARY_COLOR};
        color: white;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }}
    
    .logo-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
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
    
    /* CONTENIDO PRINCIPAL */
    .main-content {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100%;
    }}
    
    /* TÍTULO CON FONDO LLAMATIVO */
    .page-title-section {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #FF8C42, #FFA366);
        padding: 25px 20px;
        text-align: center;
        margin-bottom: 0;
        position: relative;
        overflow: hidden;
    }}
    
    .page-title-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M20,20 L80,80 M80,20 L20,80" stroke="rgba(255,255,255,0.1)" stroke-width="2"/></svg>');
        opacity: 0.3;
    }}
    
    .page-title {{
        color: white;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 8px;
        font-family: 'Segoe UI', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }}
    
    .page-subtitle {{
        color: white;
        font-size: 1.1rem;
        font-family: 'Segoe UI', sans-serif;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.4;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
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
    
    /* MODAL DE CALENDARIO PROFESIONAL */
    .calendar-modal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.85);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        padding: 20px;
        animation: fadeIn 0.3s ease;
    }}
    
    .calendar-modal {{
        background: white;
        border-radius: 16px;
        width: 95%;
        max-width: 1400px;
        height: 85vh;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: slideUp 0.4s ease;
        display: flex;
        flex-direction: column;
    }}
    
    @keyframes slideUp {{
        from {{ transform: translateY(50px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    .modal-header {{
        background: {SECONDARY_COLOR};
        color: white;
        padding: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid {PRIMARY_COLOR};
    }}
    
    .modal-title {{
        font-size: 1.8rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .modal-close {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }}
    
    .modal-close:hover {{
        background: #e55a1a;
        transform: rotate(90deg);
    }}
    
    .modal-body {{
        flex: 1;
        overflow: hidden;
        padding: 0;
    }}
    
    /* CALENDARIO PROFESIONAL - MALLA DE TURNOS */
    .professional-calendar {{
        height: 100%;
        display: flex;
        flex-direction: column;
        background: #f8f9fa;
    }}
    
    .calendar-controls {{
        background: white;
        padding: 20px;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }}
    
    .calendar-main {{
        flex: 1;
        overflow: auto;
        padding: 20px;
    }}
    
    /* Grid de días - Malla profesional */
    .calendar-days-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 1px;
        background: #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
    }}
    
    .calendar-day-header {{
        background: {SECONDARY_COLOR};
        color: white;
        padding: 15px 5px;
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .calendar-day-cell {{
        background: white;
        min-height: 120px;
        padding: 10px;
        position: relative;
        transition: all 0.3s;
    }}
    
    .calendar-day-cell:hover {{
        background: #f8f9fa;
    }}
    
    .day-number {{
        font-size: 1rem;
        font-weight: 600;
        color: {SECONDARY_COLOR};
        margin-bottom: 8px;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .today-cell {{
        background: rgba(243, 112, 33, 0.1) !important;
        border: 2px solid {PRIMARY_COLOR} !important;
    }}
    
    .today-cell .day-number {{
        color: {PRIMARY_COLOR};
        font-weight: 800;
    }}
    
    .weekend-cell {{
        background: #f9f9f9;
    }}
    
    .shift-item {{
        background: {PRIMARY_COLOR};
        color: white;
        padding: 6px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-top: 5px;
        cursor: pointer;
        transition: all 0.3s;
        border-left: 3px solid #ff944d;
    }}
    
    .shift-item:hover {{
        background: #e55a1a;
        transform: translateX(2px);
    }}
    
    .shift-time {{
        font-weight: 700;
        font-size: 0.9rem;
    }}
    
    .shift-type {{
        font-size: 0.75rem;
        opacity: 0.9;
    }}
    
    .calendar-summary {{
        background: white;
        padding: 20px;
        border-top: 1px solid #e0e0e0;
    }}
    
    .summary-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
    }}
    
    .summary-card {{
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid {PRIMARY_COLOR};
    }}
    
    /* BOTONES */
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
    
    /* RESPONSIVE PARA MÓVIL - 2 columnas x 3 filas */
    @media (max-width: 768px) {{
        .main-header {{
            padding: 10px 15px;
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
            font-size: 1.8rem;
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
        
        .calendar-modal {{
            width: 98%;
            height: 90vh;
        }}
        
        .modal-header {{
            padding: 15px;
        }}
        
        .modal-title {{
            font-size: 1.4rem;
        }}
        
        .calendar-controls {{
            flex-direction: column;
            align-items: stretch;
            gap: 10px;
            padding: 15px;
        }}
        
        .calendar-day-cell {{
            min-height: 100px;
            padding: 8px;
        }}
        
        .day-number {{
            font-size: 0.9rem;
        }}
        
        .shift-item {{
            padding: 4px 6px;
            font-size: 0.75rem;
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
        
        .calendar-days-grid {{
            grid-template-columns: repeat(7, 1fr);
        }}
        
        .calendar-day-cell {{
            min-height: 90px;
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

def create_professional_calendar():
    """Crea un calendario profesional tipo malla de turnos"""
    # Estado para el mes actual
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = datetime.datetime.now().month
        st.session_state.calendar_year = datetime.datetime.now().year
    
    # Navegación del calendario
    current_date = datetime.date(st.session_state.calendar_year, st.session_state.calendar_month, 1)
    month_name = current_date.strftime("%B %Y").upper()
    
    # Generar grid del calendario
    first_day = current_date
    last_day = datetime.date(st.session_state.calendar_year, 
                           st.session_state.calendar_month, 
                           calendar.monthrange(st.session_state.calendar_year, 
                                             st.session_state.calendar_month)[1])
    
    # Cabeceras de días
    days_of_week = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
    
    # Crear HTML del calendario
    calendar_html = '<div class="calendar-days-grid">'
    
    # Mostrar cabeceras
    for day in days_of_week:
        calendar_html += f'<div class="calendar-day-header">{day}</div>'
    
    # Espacios en blanco para el primer día
    first_weekday = (first_day.weekday() + 1) % 7  # Lunes = 0
    for _ in range(first_weekday):
        calendar_html += '<div class="calendar-day-cell"></div>'
    
    # Días del mes
    current_day = first_day
    while current_day <= last_day:
        day_class = "calendar-day-cell"
        
        # Verificar si es fin de semana
        if current_day.weekday() >= 5:
            day_class += " weekend-cell"
        
        # Verificar si es hoy
        if current_day == datetime.date.today():
            day_class += " today-cell"
        
        # Verificar si tiene turnos
        date_str = current_day.strftime("%Y-%m-%d")
        has_shifts = date_str in SAMPLE_SCHEDULE
        
        # Crear el día
        calendar_html += f'<div class="{day_class}">'
        calendar_html += f'<div class="day-number">{current_day.day}</div>'
        
        # Mostrar turnos si existen
        if has_shifts:
            for schedule in SAMPLE_SCHEDULE[date_str]:
                calendar_html += f"""
                <div class="shift-item" onclick="
                    document.getElementById('shift-date').textContent = '{date_str}';
                    document.getElementById('shift-time').textContent = '{schedule['hora']}';
                    document.getElementById('shift-type').textContent = '{schedule['tipo']}';
                    document.getElementById('shift-person').textContent = '{schedule['socorrista']}';
                    document.getElementById('shift-modal').style.display = 'flex';
                ">
                    <div class="shift-time">{schedule['hora'].split('-')[0]}</div>
                    <div class="shift-type">{schedule['tipo']}</div>
                </div>
                """
        
        calendar_html += '</div>'
        current_day += datetime.timedelta(days=1)
    
    calendar_html += '</div>'
    
    # Calcular estadísticas
    total_turnos = sum(1 for date in SAMPLE_SCHEDULE 
                      if datetime.datetime.strptime(date, "%Y-%m-%d").date().month == st.session_state.calendar_month)
    
    return calendar_html, month_name, total_turnos

def create_calendar_modal():
    """Crea el modal del calendario profesional"""
    calendar_html, month_name, total_turnos = create_professional_calendar()
    
    modal_html = f"""
    <div id="calendar-modal" class="calendar-modal-overlay" style="display: none;">
        <div class="calendar-modal">
            <div class="modal-header">
                <div class="modal-title">
                    <span>📅</span> Calendario de Turnos - {month_name}
                </div>
                <button class="modal-close" onclick="closeCalendarModal()">×</button>
            </div>
            
            <div class="modal-body">
                <div class="professional-calendar">
                    <div class="calendar-controls">
                        <div style="display: flex; gap: 10px;">
                            <button onclick="changeMonth(-1)" class="btn-primary" style="padding: 10px 20px;">
                                ← Mes Anterior
                            </button>
                            <button onclick="changeMonth(1)" class="btn-primary" style="padding: 10px 20px;">
                                Siguiente Mes →
                            </button>
                        </div>
                        
                        <div style="display: flex; gap: 15px; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <div style="width: 15px; height: 15px; background: {PRIMARY_COLOR}; border-radius: 3px;"></div>
                                <span style="font-size: 0.9rem;">Turno asignado</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <div style="width: 15px; height: 15px; background: rgba(243, 112, 33, 0.1); border: 2px solid {PRIMARY_COLOR}; border-radius: 3px;"></div>
                                <span style="font-size: 0.9rem;">Hoy</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="calendar-main">
                        {calendar_html}
                    </div>
                    
                    <div class="calendar-summary">
                        <div class="summary-grid">
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 5px;">📅 Turnos del Mes</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 1.8rem; font-weight: 700;">{total_turnos}</div>
                            </div>
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 5px;">⏰ Horas Totales</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 1.8rem; font-weight: 700;">{total_turnos * 6}h</div>
                            </div>
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 5px;">👥 Socorristas</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 1.8rem; font-weight: 700;">5</div>
                            </div>
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 5px;">✅ Disponibilidad</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 1.8rem; font-weight: 700;">95%</div>
                            </div>
                        </div>
                        
                        <div class="action-buttons" style="margin-top: 20px;">
                            <button class="btn-secondary" onclick="window.print()">
                                🖨️ Imprimir Calendario
                            </button>
                            <button class="btn-secondary" onclick="alert('Exportando a Excel...')">
                                📊 Exportar Excel
                            </button>
                            <button class="btn-primary" onclick="closeCalendarModal()">
                                Cerrar Calendario
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal para detalles del turno -->
    <div id="shift-modal" class="calendar-modal-overlay" style="display: none;">
        <div class="calendar-modal" style="max-width: 500px; height: auto;">
            <div class="modal-header">
                <div class="modal-title">
                    <span>📋</span> Detalles del Turno
                </div>
                <button class="modal-close" onclick="closeShiftModal()">×</button>
            </div>
            
            <div class="modal-body" style="padding: 20px;">
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                        <div>
                            <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">📅 Fecha</div>
                            <div style="font-weight: 700; color: #333;" id="shift-date"></div>
                        </div>
                        <div>
                            <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">🕒 Horario</div>
                            <div style="font-weight: 700; color: #333;" id="shift-time"></div>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                        <div>
                            <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">🏷️ Tipo de Turno</div>
                            <div style="font-weight: 700; color: #333;" id="shift-type"></div>
                        </div>
                        <div>
                            <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">👤 Socorrista</div>
                            <div style="font-weight: 700; color: #333;" id="shift-person"></div>
                        </div>
                    </div>
                    <div>
                        <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">📍 Ubicación</div>
                        <div style="font-weight: 700; color: #333;">Piscina Municipal Central</div>
                        <div style="color: #666; font-size: 0.85rem; margin-top: 3px;">Av. Deportes, 123 - Zona Centro</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button class="btn-primary" style="flex: 1;" onclick="alert('Solicitud enviada para cambio de turno')">
                        🔄 Solicitar Cambio
                    </button>
                    <button class="btn-secondary" style="flex: 1;" onclick="closeShiftModal()">
                        Cerrar
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    // Funciones para el calendario
    function openCalendarModal() {{
        document.getElementById('calendar-modal').style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }}
    
    function closeCalendarModal() {{
        document.getElementById('calendar-modal').style.display = 'none';
        document.body.style.overflow = 'auto';
    }}
    
    function closeShiftModal() {{
        document.getElementById('shift-modal').style.display = 'none';
    }}
    
    function changeMonth(direction) {{
        // Esta función requeriría una recarga con Streamlit para cambiar el mes
        // Por ahora solo muestra un mensaje
        if(direction === -1) {{
            alert('Navegando al mes anterior... (Funcionalidad completa requeriría recarga)');
        }} else {{
            alert('Navegando al mes siguiente... (Funcionalidad completa requeriría recarga)');
        }}
    }}
    
    // Cerrar modal con ESC
    document.addEventListener('keydown', function(event) {{
        if (event.key === 'Escape') {{
            closeCalendarModal();
            closeShiftModal();
        }}
    }});
    
    // Cerrar modal al hacer clic fuera
    document.addEventListener('click', function(event) {{
        if (event.target.classList.contains('calendar-modal-overlay')) {{
            closeCalendarModal();
            closeShiftModal();
        }}
    }});
    </script>
    """
    
    return modal_html

def create_dashboard():
    """Crea el dashboard principal"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Título con fondo llamativo
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
        if view == "horarios":
            # Para Horarios, usamos onclick para abrir el modal
            card_html = f"""
            <div class="dashboard-card" onclick="openCalendarModal()">
                <div class="card-icon">{icon}</div>
                <h3 class="card-title">{title}</h3>
                <p class="card-desc">{desc}</p>
            </div>
            """
        else:
            # Para otras vistas, usamos enlace normal
            card_html = f"""
            <a href="?view={view}" class="dashboard-card">
                <div class="card-icon">{icon}</div>
                <h3 class="card-title">{title}</h3>
                <p class="card-desc">{desc}</p>
            </a>
            """
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Estadísticas rápidas
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
    
    # Añadir el modal del calendario
    calendar_modal_html = create_calendar_modal()
    st.markdown(calendar_modal_html, unsafe_allow_html=True)
    
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
    
    # Crear header
    create_header()
    
    # Obtener vista actual
    query_params = st.query_params.to_dict()
    view = query_params.get("view", [""])[0] if query_params.get("view") else ""
    
    # Mostrar vista correspondiente
    if view == "horarios":
        # Si alguien accede directamente a ?view=horarios, mostramos el modal
        st.markdown('<script>openCalendarModal();</script>', unsafe_allow_html=True)
        create_dashboard()
    elif view in ["asistencia", "nomina", "incidencias", "formacion", "comunicados"]:
        create_other_view(view)
    else:
        create_dashboard()

if __name__ == "__main__":
    main()
