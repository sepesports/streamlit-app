import base64
import requests
import streamlit as st
import pandas as pd
import datetime
import calendar
from dateutil.relativedelta import relativedelta

# ----------------------------
# CONFIGURACIÓN PRINCIPAL
# ----------------------------
st.set_page_config(
    page_title="Socorrista Pro - Panel de Control",
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
    """Convierte imagen URL a Data URI"""
    try:
        r = requests.get(url, timeout=25)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "image/png")
        b64 = base64.b64encode(r.content).decode("utf-8")
        return f"data:{content_type};base64,{b64}"
    except Exception:
        return ""

def apply_custom_css():
    """Aplica estilos CSS personalizados"""
    bg_image = fetch_image_as_data_uri(IMG_URL) if IMG_URL else ""
    
    st.markdown(f"""
    <style>
    /* Reset y base */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    html, body, #root, .stApp {{
        height: 100vh;
        width: 100vw;
        overflow-x: hidden;
    }}
    
    /* Contenedor principal sin márgenes */
    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
    }}
    
    /* Header personalizado */
    .custom-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 1.5rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    .header-title {{
        font-size: 1.8rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    
    .user-info {{
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1rem;
        border-radius: 50px;
    }}
    
    /* Dashboard grid */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        padding: 2rem;
        background: {BG_COLOR};
        min-height: calc(100vh - 80px);
    }}
    
    /* Cards de dashboard */
    .dashboard-card {{
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        cursor: pointer;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.12);
    }}
    
    .card-icon {{
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }}
    
    .card-title {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {SECONDARY_COLOR};
        margin-bottom: 0.5rem;
    }}
    
    .card-desc {{
        color: #666;
        font-size: 0.9rem;
        line-height: 1.4;
    }}
    
    /* Calendario */
    .calendar-container {{
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        margin: 2rem;
    }}
    
    .calendar-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid {BG_COLOR};
    }}
    
    .month-navigation {{
        display: flex;
        gap: 1rem;
        align-items: center;
    }}
    
    .nav-btn {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }}
    
    .nav-btn:hover {{
        background: #e55a1a;
        transform: scale(1.05);
    }}
    
    .current-month {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        min-width: 200px;
        text-align: center;
    }}
    
    /* Grid de días del calendario */
    .calendar-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 1px;
        background: {BG_COLOR};
        border-radius: 8px;
        overflow: hidden;
    }}
    
    .calendar-day-header {{
        background: {SECONDARY_COLOR};
        color: white;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
    }}
    
    .calendar-day {{
        background: white;
        min-height: 120px;
        padding: 0.8rem;
        border: 1px solid {BG_COLOR};
        transition: all 0.3s;
    }}
    
    .calendar-day:hover {{
        background: #fffaf5;
    }}
    
    .day-number {{
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: {SECONDARY_COLOR};
    }}
    
    .has-schedule {{
        background: linear-gradient(135deg, rgba(243, 112, 33, 0.1), rgba(243, 112, 33, 0.05));
        border-left: 4px solid {PRIMARY_COLOR};
    }}
    
    .schedule-item {{
        background: {PRIMARY_COLOR};
        color: white;
        padding: 0.4rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-top: 0.4rem;
        cursor: pointer;
        transition: all 0.3s;
    }}
    
    .schedule-item:hover {{
        background: #e55a1a;
        transform: translateX(2px);
    }}
    
    /* Vista de detalles */
    .detail-view {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    .detail-content {{
        background: white;
        width: 90%;
        max-width: 500px;
        border-radius: 16px;
        padding: 2rem;
        animation: slideUp 0.3s ease;
    }}
    
    @keyframes slideUp {{
        from {{ transform: translateY(20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .dashboard-grid {{
            grid-template-columns: 1fr;
            padding: 1rem;
        }}
        
        .custom-header {{
            flex-direction: column;
            gap: 1rem;
            padding: 1rem;
        }}
        
        .calendar-day {{
            min-height: 80px;
            padding: 0.4rem;
        }}
        
        .calendar-container {{
            margin: 1rem;
            padding: 1rem;
        }}
    }}
    
    /* Animaciones */
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    /* Días de fin de semana */
    .weekend {{
        background-color: #f9f9f9;
    }}
    
    /* Día actual */
    .today {{
        background-color: rgba(243, 112, 33, 0.15);
        border: 2px solid {PRIMARY_COLOR};
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES REUTILIZABLES
# ----------------------------
def create_header():
    """Crea el encabezado profesional"""
    st.markdown(f"""
    <div class="custom-header">
        <div class="header-title">
            <span>🛟</span>
            SOCORRISTA PRO - PANEL DE CONTROL
        </div>
        <div class="user-info">
            <span>👤 Carlos Rodríguez</span>
            <span style="font-size: 0.9rem; opacity: 0.9;">Socorrista Principal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_dashboard():
    """Crea el dashboard principal"""
    st.markdown("""
    <div class="dashboard-grid">
    """, unsafe_allow_html=True)
    
    # Tarjetas del dashboard
    cards = [
        ("Horarios", "Ver y gestionar turnos programados", "📅", "primary", "horarios"),
        ("Control de Asistencia", "Registro de entrada y salida", "✅", "secondary", "asistencia"),
        ("Nómina", "Consulta de pagos y recibos", "💰", "secondary", "nomina"),
        ("Incidencias", "Reporte de incidentes", "⚠️", "secondary", "incidencias"),
        ("Formación", "Cursos y certificaciones", "🎓", "secondary", "formacion"),
        ("Comunicados", "Noticias y anuncios", "📢", "secondary", "comunicados"),
    ]
    
    for title, desc, icon, color, view in cards:
        bg_color = PRIMARY_COLOR if color == "primary" else SECONDARY_COLOR
        card_html = f"""
        <div class="dashboard-card" onclick="window.location.href='?view={view}'">
            <div class="card-icon" style="background: linear-gradient(135deg, {bg_color}, {bg_color}99);">
                <span style="font-size: 1.5rem; color: white;">{icon}</span>
            </div>
            <h3 class="card-title">{title}</h3>
            <p class="card-desc">{desc}</p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

def create_calendar(year=None, month=None):
    """Crea un calendario interactivo profesional"""
    now = datetime.datetime.now()
    current_year = year or now.year
    current_month = month or now.month
    
    # Calcular primer día del mes
    first_day = datetime.date(current_year, current_month, 1)
    last_day = datetime.date(current_year, current_month, 
                           calendar.monthrange(current_year, current_month)[1])
    
    # Nombres de días
    days_of_week = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    
    # Generar grid de días
    calendar_html = '<div class="calendar-grid">'
    
    # Encabezados de días
    for day in days_of_week:
        calendar_html += f'<div class="calendar-day-header">{day}</div>'
    
    # Días en blanco antes del primer día
    first_weekday = (first_day.weekday() + 1) % 7
    for _ in range(first_weekday):
        calendar_html += '<div class="calendar-day"></div>'
    
    # Días del mes
    current_day = first_day
    while current_day <= last_day:
        day_class = "calendar-day"
        day_number = current_day.day
        
        # Verificar si es fin de semana
        if current_day.weekday() >= 5:
            day_class += " weekend"
        
        # Verificar si es hoy
        if current_day == datetime.date.today():
            day_class += " today"
        
        # Verificar si hay turnos este día
        date_str = current_day.strftime("%Y-%m-%d")
        has_schedule = date_str in SAMPLE_SCHEDULE
        if has_schedule:
            day_class += " has-schedule"
        
        calendar_html += f'<div class="{day_class}" id="day-{date_str}">'
        calendar_html += f'<div class="day-number">{day_number}</div>'
        
        # Mostrar turnos si existen
        if has_schedule:
            for schedule in SAMPLE_SCHEDULE[date_str]:
                schedule_json = str(schedule).replace("'", '"')
                calendar_html += f'''
                <div class="schedule-item" onclick="showScheduleDetail('{date_str}', '{schedule["hora"]}', '{schedule["tipo"]}', '{schedule["socorrista"]}')">
                    {schedule["hora"]} - {schedule["tipo"]}
                </div>
                '''
        
        calendar_html += '</div>'
        current_day += datetime.timedelta(days=1)
    
    calendar_html += '</div>'
    
    return calendar_html

def show_schedule():
    """Muestra el calendario de horarios completo"""
    create_header()
    
    # Estado para el mes actual
    if 'current_month' not in st.session_state:
        st.session_state.current_month = datetime.datetime.now().month
        st.session_state.current_year = datetime.datetime.now().year
    
    # Navegación de meses
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Mes Anterior", use_container_width=True):
            new_date = datetime.date(st.session_state.current_year, 
                                   st.session_state.current_month, 1) - relativedelta(months=1)
            st.session_state.current_month = new_date.month
            st.session_state.current_year = new_date.year
            st.rerun()
    
    with col2:
        month_name = datetime.date(st.session_state.current_year, 
                                 st.session_state.current_month, 1).strftime("%B %Y").upper()
        st.markdown(f'<h2 style="text-align: center; color: {SECONDARY_COLOR};">{month_name}</h2>', 
                   unsafe_allow_html=True)
    
    with col3:
        if st.button("Siguiente Mes →", use_container_width=True):
            new_date = datetime.date(st.session_state.current_year, 
                                   st.session_state.current_month, 1) + relativedelta(months=1)
            st.session_state.current_month = new_date.month
            st.session_state.current_year = new_date.year
            st.rerun()
    
    # Mostrar calendario
    calendar_html = create_calendar(st.session_state.current_year, st.session_state.current_month)
    
    # Estadísticas
    total_shifts = 0
    total_hours = 0
    completed = 0
    upcoming = 0
    
    for date_str, schedules in SAMPLE_SCHEDULE.items():
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_obj.year == st.session_state.current_year and date_obj.month == st.session_state.current_month:
            total_shifts += len(schedules)
            for schedule in schedules:
                # Calcular horas
                if "-" in schedule["hora"]:
                    try:
                        start, end = schedule["hora"].split("-")
                        start_h = int(start.split(":")[0])
                        end_h = int(end.split(":")[0])
                        total_hours += (end_h - start_h)
                    except:
                        total_hours += 6  # Valor por defecto
                
                # Contar completados vs próximos
                if date_obj < datetime.date.today():
                    completed += 1
                else:
                    upcoming += 1
    
    # JavaScript para detalles
    js_script = """
    <script>
    function showScheduleDetail(date, time, type, lifeguard) {
        // Crear modal de detalles
        const detailHtml = `
        <div class="detail-view" onclick="closeDetail()">
            <div class="detail-content" onclick="event.stopPropagation()">
                <h3 style="color: #F37021; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>📋</span> Detalles del Turno
                </h3>
                
                <div style="margin-bottom: 1.5rem;">
                    <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #F37021;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                            <div>
                                <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.2rem;">📅 Fecha</p>
                                <p style="font-weight: bold; color: #333;">${date}</p>
                            </div>
                            <div>
                                <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.2rem;">🕒 Horario</p>
                                <p style="font-weight: bold; color: #333;">${time}</p>
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                            <div>
                                <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.2rem;">🏷️ Tipo de Turno</p>
                                <p style="font-weight: bold; color: #333;">${type}</p>
                            </div>
                            <div>
                                <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.2rem;">👤 Socorrista</p>
                                <p style="font-weight: bold; color: #333;">${lifeguard}</p>
                            </div>
                        </div>
                        
                        <div>
                            <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.2rem;">📍 Ubicación</p>
                            <p style="font-weight: bold; color: #333;">Piscina Municipal Principal</p>
                            <p style="font-size: 0.9rem; color: #666; margin-top: 0.2rem;">Calle Deportes, 123 - Zona Centro</p>
                        </div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 1rem;">
                    <button onclick="closeDetail()" style="
                        background: #6c757d;
                        color: white;
                        border: none;
                        padding: 0.8rem 1.5rem;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                        flex: 1;
                    ">Cerrar</button>
                    
                    <button onclick="alert('Solicitud enviada para cambiar turno')" style="
                        background: #F37021;
                        color: white;
                        border: none;
                        padding: 0.8rem 1.5rem;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                        flex: 2;
                    ">🔄 Solicitar Cambio</button>
                </div>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', detailHtml);
    }
    
    function closeDetail() {
        const detail = document.querySelector('.detail-view');
        if (detail) detail.remove();
    }
    
    // Mejorar interacción con calendario
    document.addEventListener('DOMContentLoaded', function() {
        const days = document.querySelectorAll('.has-schedule');
        days.forEach(day => {
            day.style.cursor = 'pointer';
            day.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 12px rgba(243, 112, 33, 0.2)';
            });
            day.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            });
        });
    });
    </script>
    """
    
    # Mostrar todo
    st.markdown(f"""
    <div class="calendar-container">
        {calendar_html}
    </div>
    
    <div style="padding: 2rem; background: white; margin: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 1rem;">📊 Resumen del Mes</h3>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
            <div style="background: #e8f5e9; padding: 1rem; border-radius: 8px;">
                <h4 style="color: #2e7d32;">🎯 Turnos Asignados</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #2e7d32;">{total_shifts}</p>
            </div>
            
            <div style="background: #fff3e0; padding: 1rem; border-radius: 8px;">
                <h4 style="color: #ef6c00;">⏰ Horas Totales</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #ef6c00;">{total_hours}h</p>
            </div>
            
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px;">
                <h4 style="color: #1565c0;">✅ Completados</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #1565c0;">{completed}</p>
            </div>
            
            <div style="background: #f3e5f5; padding: 1rem; border-radius: 8px;">
                <h4 style="color: #7b1fa2;">📅 Próximos</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #7b1fa2;">{upcoming}</p>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin: 2rem;">
        <button onclick="window.location.href='?'" style="
            background: {SECONDARY_COLOR};
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            margin-right: 1rem;
        ">← Volver al Dashboard</button>
        
        <button onclick="window.print()" style="
            background: white;
            color: {PRIMARY_COLOR};
            border: 2px solid {PRIMARY_COLOR};
            padding: 1rem 2rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
        ">🖨️ Imprimir Horario</button>
    </div>
    
    {js_script}
    """, unsafe_allow_html=True)

def show_other_view(view_name):
    """Muestra otras vistas de la aplicación"""
    create_header()
    
    view_titles = {
        "asistencia": "Control de Asistencia",
        "nomina": "Nómina y Pagos",
        "incidencias": "Reporte de Incidencias",
        "formacion": "Formación y Certificaciones",
        "comunicados": "Comunicados y Noticias"
    }
    
    title = view_titles.get(view_name, view_name.capitalize())
    
    st.markdown(f"""
    <div style="padding: 2rem;">
        <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 2rem;">{title}</h1>
        <div style="background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <p style="color: #666; font-size: 1.1rem; margin-bottom: 1.5rem;">
                Esta funcionalidad está en desarrollo. Próximamente estará disponible con todas las características.
            </p>
            
            <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                <button onclick="window.location.href='?'" style="
                    background: {PRIMARY_COLOR};
                    color: white;
                    border: none;
                    padding: 0.8rem 1.5rem;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                ">← Volver al Dashboard</button>
                
                <button onclick="alert('Función en desarrollo')" style="
                    background: {SECONDARY_COLOR};
                    color: white;
                    border: none;
                    padding: 0.8rem 1.5rem;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                ">🔄 Actualizar</button>
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
    
    # Obtener vista actual de query parameters
    query_params = st.query_params.to_dict()
    view = query_params.get("view", [""])[0] if query_params.get("view") else ""
    
    # Mostrar vista correspondiente
    if view == "horarios":
        show_schedule()
    elif view in ["asistencia", "nomina", "incidencias", "formacion", "comunicados"]:
        show_other_view(view)
    else:
        # Dashboard principal
        create_header()
        create_dashboard()
        
        # Footer informativo
        st.markdown(f"""
        <div style="padding: 1.5rem; background: {SECONDARY_COLOR}; color: white; text-align: center; margin-top: auto;">
            <p style="margin: 0; font-size: 0.9rem;">© 2024 Socorrista Pro - Panel de Control</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.8;">
                Versión 2.0 • Última actualización: {datetime.datetime.now().strftime("%d/%m/%Y")}
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
