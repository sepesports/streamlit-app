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
# ESTILOS CSS - SIMPLIFICADO
# ----------------------------
def apply_custom_css():
    """Aplica estilos CSS personalizados"""
    st.markdown(f"""
    <style>
    /* RESET */
    html, body, .stApp {{
        margin: 0;
        padding: 0;
        width: 100%;
    }}
    
    /* HEADER */
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
    
    /* TÍTULO */
    .page-title-section {{
        background: linear-gradient(135deg, #1a5276, #1c5c82, #1e6790, {PRIMARY_COLOR});
        padding: 40px 25px;
        text-align: center;
        margin-bottom: 0;
    }}
    
    .page-title {{
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 15px;
    }}
    
    /* CONTENEDOR PRINCIPAL */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 40px 25px;
        width: 100%;
    }}
    
    /* ESCRITORIO: 2 filas de 3 columnas */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(2, auto);
        gap: 25px;
        width: 100%;
    }}
    
    /* Definir posiciones específicas para cada tarjeta en escritorio */
    .card-1 {{ grid-column: 1 / 2; grid-row: 1 / 2; }}
    .card-2 {{ grid-column: 2 / 3; grid-row: 1 / 2; }}
    .card-3 {{ grid-column: 3 / 4; grid-row: 1 / 2; }}
    .card-4 {{ grid-column: 1 / 2; grid-row: 2 / 3; }}
    .card-5 {{ grid-column: 2 / 3; grid-row: 2 / 3; }}
    .card-6 {{ grid-column: 3 / 4; grid-row: 2 / 3; }}
    
    /* TARJETAS */
    .dashboard-card {{
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
        text-decoration: none !important;
        display: flex;
        flex-direction: column;
        min-height: 200px;
        width: 100%;
        position: relative;
        overflow: hidden;
    }}
    
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
    
    .dashboard-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(243, 112, 33, 0.2);
    }}
    
    .card-icon {{
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        font-size: 28px;
        color: white;
        transition: all 0.3s ease;
    }}
    
    .card-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin-bottom: 10px;
    }}
    
    .card-desc {{
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }}
    
    /* MÓVIL: 3 filas de 2 columnas */
    @media (max-width: 768px) {{
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(3, auto);
            gap: 15px;
        }}
        
        /* Redefinir posiciones para móvil */
        .card-1 {{ grid-column: 1 / 2; grid-row: 1 / 2; }}
        .card-2 {{ grid-column: 2 / 3; grid-row: 1 / 2; }}
        .card-3 {{ grid-column: 1 / 2; grid-row: 2 / 3; }}
        .card-4 {{ grid-column: 2 / 3; grid-row: 2 / 3; }}
        .card-5 {{ grid-column: 1 / 2; grid-row: 3 / 4; }}
        .card-6 {{ grid-column: 2 / 3; grid-row: 3 / 4; }}
        
        .dashboard-card {{
            padding: 20px;
            min-height: 180px;
        }}
        
        .card-icon {{
            width: 50px;
            height: 50px;
            font-size: 24px;
        }}
        
        .card-title {{
            font-size: 1.1rem;
        }}
        
        .page-title {{
            font-size: 2.2rem;
        }}
    }}
    
    /* MÓVIL PEQUEÑO: 1 columna */
    @media (max-width: 480px) {{
        .dashboard-grid {{
            grid-template-columns: 1fr;
            grid-template-rows: repeat(6, auto);
        }}
        
        .card-1 {{ grid-column: 1 / 2; grid-row: 1 / 2; }}
        .card-2 {{ grid-column: 1 / 2; grid-row: 2 / 3; }}
        .card-3 {{ grid-column: 1 / 2; grid-row: 3 / 4; }}
        .card-4 {{ grid-column: 1 / 2; grid-row: 4 / 5; }}
        .card-5 {{ grid-column: 1 / 2; grid-row: 5 / 6; }}
        .card-6 {{ grid-column: 1 / 2; grid-row: 6 / 7; }}
    }}
    
    /* ESTADÍSTICAS */
    .stats-container {{
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 40px auto 0;
        max-width: 1200px;
        width: 100%;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }}
    
    @media (max-width: 768px) {{
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
    
    @media (max-width: 480px) {{
        .stats-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    .stat-card {{
        background: #f8f9fa;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border-left: 4px solid {PRIMARY_COLOR};
    }}
    
    .stat-value {{
        font-size: 2.2rem;
        font-weight: 800;
        margin: 10px 0;
        color: {SECONDARY_COLOR};
    }}
    
    /* OCULTAR ELEMENTOS DE STREAMLIT */
    [data-testid="stHeader"] {{ display: none !important; }}
    footer {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES DE LA APLICACIÓN
# ----------------------------
def create_header():
    """Crea el encabezado profesional"""
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.5rem;">🛟</span>
            <span style="font-size: 1.3rem; font-weight: 700;">SOCORRISTA PRO</span>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 25px; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.1rem;">👤</span>
                <div>
                    <div style="font-weight: 600;">Carlos Rodríguez</div>
                    <div style="font-size: 0.8rem; opacity: 0.9;">Socorrista Principal</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_dashboard():
    """Crea el dashboard principal"""
    # Aplicar CSS
    apply_custom_css()
    
    # Crear header
    create_header()
    
    # Título principal
    st.markdown(f"""
    <div class="page-title-section">
        <h1 class="page-title">Panel de Control</h1>
        <p style="color: rgba(255,255,255,0.95); font-size: 1.2rem; max-width: 700px; margin: 0 auto;">
            Gestiona tus horarios, asistencia y más desde un solo lugar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenedor principal
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Grid de tarjetas - AHORA ORDENADO CORRECTAMENTE
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    # Fila 1 en escritorio (3 tarjetas en línea)
    # 1. Horarios
    st.markdown(f"""
    <div class="dashboard-card card-1" onclick="openCalendarModal()">
        <div class="card-icon">📅</div>
        <h3 class="card-title">Horarios</h3>
        <p class="card-desc">Consulta y gestiona tus turnos programados</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Control de Asistencia
    st.markdown(f"""
    <a href="?view=asistencia" class="dashboard-card card-2">
        <div class="card-icon">✅</div>
        <h3 class="card-title">Control de Asistencia</h3>
        <p class="card-desc">Registro de entrada y salida en tiempo real</p>
    </a>
    """, unsafe_allow_html=True)
    
    # 3. Nómina y Pagos
    st.markdown(f"""
    <a href="?view=nomina" class="dashboard-card card-3">
        <div class="card-icon">💰</div>
        <h3 class="card-title">Nómina y Pagos</h3>
        <p class="card-desc">Consulta tus recibos y estados de pago</p>
    </a>
    """, unsafe_allow_html=True)
    
    # Fila 2 en escritorio (3 tarjetas en línea)
    # 4. Incidencias
    st.markdown(f"""
    <a href="?view=incidencias" class="dashboard-card card-4">
        <div class="card-icon">⚠️</div>
        <h3 class="card-title">Incidencias</h3>
        <p class="card-desc">Reporta y consulta incidencias</p>
    </a>
    """, unsafe_allow_html=True)
    
    # 5. Formación
    st.markdown(f"""
    <a href="?view=formacion" class="dashboard-card card-5">
        <div class="card-icon">🎓</div>
        <h3 class="card-title">Formación</h3>
        <p class="card-desc">Accede a cursos y certificaciones</p>
    </a>
    """, unsafe_allow_html=True)
    
    # 6. Comunicados
    st.markdown(f"""
    <a href="?view=comunicados" class="dashboard-card card-6">
        <div class="card-icon">📢</div>
        <h3 class="card-title">Comunicados</h3>
        <p class="card-desc">Últimas noticias y anuncios</p>
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra dashboard-grid
    
    # Estadísticas
    st.markdown(f"""
    <div class="stats-container">
        <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 25px; font-size: 1.5rem; font-weight: 700;">
            📊 Resumen Rápido
        </h3>
        <div class="stats-grid">
            <div class="stat-card">
                <div style="color: #4CAF50; font-size: 1.3rem;">✅</div>
                <div class="stat-value">12</div>
                <div style="color: #666; font-size: 0.9rem;">Turnos Completados</div>
            </div>
            <div class="stat-card">
                <div style="color: #2196F3; font-size: 1.3rem;">⏰</div>
                <div class="stat-value">96h</div>
                <div style="color: #666; font-size: 0.9rem;">Horas Totales</div>
            </div>
            <div class="stat-card">
                <div style="color: #FF9800; font-size: 1.3rem;">📅</div>
                <div class="stat-value">6</div>
                <div style="color: #666; font-size: 0.9rem;">Próximos Turnos</div>
            </div>
            <div class="stat-card">
                <div style="color: #9C27B0; font-size: 1.3rem;">💰</div>
                <div class="stat-value">€2,850</div>
                <div style="color: #666; font-size: 0.9rem;">Salario Estimado</div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 40px; color: #666; font-size: 0.9rem;">
        © {datetime.datetime.now().year} Socorrista Pro • Versión 2.2 • Todos los derechos reservados
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra main-container
    
    # Modal del calendario (simplificado)
    st.markdown("""
    <div id="calendar-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); z-index: 9999; align-items: center; justify-content: center;">
        <div style="background: white; border-radius: 20px; padding: 30px; max-width: 800px; width: 90%; max-height: 90vh; overflow-y: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="margin: 0; color: #333;">📅 Calendario de Turnos</h2>
                <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 1.2rem; cursor: pointer;">×</button>
            </div>
            <div style="color: #666; margin-bottom: 20px;">
                <p>Esta funcionalidad está en desarrollo. Próximamente podrás ver tu calendario completo aquí.</p>
            </div>
            <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; padding: 12px 24px; border-radius: 10px; cursor: pointer; font-weight: 600;">Cerrar</button>
        </div>
    </div>
    
    <script>
    function openCalendarModal() {
        document.getElementById('calendar-modal').style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    function closeCalendarModal() {
        document.getElementById('calendar-modal').style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    </script>
    """, unsafe_allow_html=True)

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
    
    # Aplicar CSS
    apply_custom_css()
    
    # Crear header
    create_header()
    
    st.markdown(f"""
    <div style="max-width: 800px; margin: 0 auto; padding: 40px 25px;">
        <div style="text-align: center; margin-bottom: 40px;">
            <div style="font-size: 3rem; margin-bottom: 20px; color: {PRIMARY_COLOR};">📋</div>
            <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-size: 2.5rem; font-weight: 800;">
                {title}
            </h1>
            <p style="color: #666; font-size: 1.2rem;">
                Esta funcionalidad está en desarrollo activo
            </p>
        </div>
        
        <div style="background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 30px;">
            <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 20px; font-size: 1.4rem; font-weight: 700;">
                🚀 Próximamente
            </h3>
            <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">
                Estamos trabajando para implementar esta funcionalidad. En las próximas semanas podrás acceder a todas las características avanzadas.
            </p>
        </div>
        
        <div style="text-align: center;">
            <a href="?" style="background: {PRIMARY_COLOR}; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; display: inline-block; font-weight: 600;">
                ← Volver al Dashboard
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# APLICACIÓN PRINCIPAL
# ----------------------------
def main():
    """Función principal de la aplicación"""
    # Obtener vista actual
    query_params = st.query_params.to_dict()
    view = query_params.get("view", [""])[0] if query_params.get("view") else ""
    
    # Mostrar vista correspondiente
    if view == "horarios":
        # Si alguien accede directamente a ?view=horarios
        st.markdown('<script>openCalendarModal();</script>', unsafe_allow_html=True)
        create_dashboard()
    elif view in ["asistencia", "nomina", "incidencias", "formacion", "comunicados"]:
        create_other_view(view)
    else:
        create_dashboard()

if __name__ == "__main__":
    main()
