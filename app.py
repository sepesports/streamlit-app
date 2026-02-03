import streamlit as st
import datetime

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

# ----------------------------
# ESTILOS CSS SIMPLIFICADOS Y EFECTIVOS
# ----------------------------
def apply_custom_css():
    """Aplica estilos CSS personalizados"""
    st.markdown(f"""
    <style>
    /* RESET COMPLETO */
    .stApp {{
        background: {BG_COLOR} !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* ELIMINAR ESPACIOS STREAMLIT */
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
    }}
    
    /* HEADER COMPACTO */
    .main-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    
    /* TÍTULO COMPACTO */
    .page-title-section {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        padding: 25px 20px;
        text-align: center;
        margin-bottom: 0;
    }}
    
    .page-title {{
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }}
    
    .page-subtitle {{
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
        max-width: 500px;
        margin: 0 auto;
    }}
    
    /* CONTENEDOR PRINCIPAL */
    .main-content {{
        padding: 30px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    /* GRID UNIFICADO - FUNCIONA EN ESCRITORIO Y MÓVIL */
    .dashboard-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        justify-content: center;
    }}
    
    /* TARJETAS - ANCHO FIJO PARA CONTROL */
    .dashboard-card {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        text-decoration: none !important;
        border: 1px solid rgba(0,0,0,0.05);
        width: 180px; /* ANCHO FIJO */
        min-height: 150px;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(243, 112, 33, 0.2);
        border-color: {PRIMARY_COLOR};
    }}
    
    .card-icon {{
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
        font-size: 22px;
        color: white;
    }}
    
    .card-title {{
        font-size: 0.95rem;
        font-weight: 600;
        color: {SECONDARY_COLOR};
        margin: 0;
        line-height: 1.2;
    }}
    
    /* ESCRITORIO: 3 columnas */
    @media (min-width: 769px) {{
        .dashboard-grid {{
            justify-content: space-between;
        }}
        
        .dashboard-card {{
            width: calc(33.333% - 10px);
        }}
    }}
    
    /* MÓVIL: 2 columnas */
    @media (max-width: 768px) {{
        .main-header {{
            padding: 10px 15px;
        }}
        
        .page-title-section {{
            padding: 20px 15px;
        }}
        
        .page-title {{
            font-size: 1.6rem;
        }}
        
        .page-subtitle {{
            font-size: 0.9rem;
        }}
        
        .main-content {{
            padding: 20px 15px;
        }}
        
        .dashboard-grid {{
            gap: 10px;
        }}
        
        .dashboard-card {{
            width: calc(50% - 5px);
            min-height: 130px;
            padding: 15px;
        }}
        
        .card-icon {{
            width: 45px;
            height: 45px;
            font-size: 20px;
        }}
        
        .card-title {{
            font-size: 0.9rem;
        }}
    }}
    
    /* ESTADÍSTICAS COMPACTAS */
    .stats-container {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-top: 25px;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
    }}
    
    @media (max-width: 768px) {{
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .stats-container {{
            padding: 15px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .stats-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    .stat-card {{
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-left: 3px solid {PRIMARY_COLOR};
    }}
    
    .stat-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin: 5px 0;
    }}
    
    /* FOOTER MINIMALISTA */
    .footer {{
        text-align: center;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid rgba(0,0,0,0.1);
        color: #777;
        font-size: 0.8rem;
    }}
    
    /* OCULTAR ELEMENTOS STREAMLIT */
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
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.3rem;">🛟</span>
            <span style="font-size: 1.1rem; font-weight: 600;">SOCORRISTA PRO</span>
        </div>
        <div>
            <div style="background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 20px; display: flex; align-items: center; gap: 8px;">
                <span>👤</span>
                <div>
                    <div style="font-size: 0.85rem; font-weight: 500;">Carlos Rodríguez</div>
                    <div style="font-size: 0.7rem; opacity: 0.9;">Socorrista Principal</div>
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
    
    # Título principal compacto
    st.markdown(f"""
    <div class="page-title-section">
        <h1 class="page-title">Panel de Control</h1>
        <p class="page-subtitle">Gestión centralizada de turnos y asistencia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenedor principal
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # **GRID UNIFICADO - FUNCIONA EN TODOS LOS DISPOSITIVOS**
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    # Tarjetas en el orden específico
    cards = [
        {"title": "Horarios", "icon": "📅", "desc": "Turnos programados", "view": "horarios", "onclick": "openCalendarModal()"},
        {"title": "Control Asistencia", "icon": "✅", "desc": "Registro entrada/salida", "view": "asistencia", "onclick": None},
        {"title": "Nómina y Pagos", "icon": "💰", "desc": "Recibos y estados", "view": "nomina", "onclick": None},
        {"title": "Incidencias", "icon": "⚠️", "desc": "Reporte de incidencias", "view": "incidencias", "onclick": None},
        {"title": "Formación", "icon": "🎓", "desc": "Cursos y certificaciones", "view": "formacion", "onclick": None},
        {"title": "Comunicados", "icon": "📢", "desc": "Noticias y anuncios", "view": "comunicados", "onclick": None},
    ]
    
    for card in cards:
        if card["view"] == "horarios":
            st.markdown(f"""
            <div class="dashboard-card" onclick="{card['onclick']}">
                <div class="card-icon">{card['icon']}</div>
                <h3 class="card-title">{card['title']}</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <a href="?view={card['view']}" class="dashboard-card">
                <div class="card-icon">{card['icon']}</div>
                <h3 class="card-title">{card['title']}</h3>
            </a>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra dashboard-grid
    
    # Estadísticas compactas
    st.markdown(f"""
    <div class="stats-container">
        <div class="stats-grid">
            <div class="stat-card">
                <div style="color: #4CAF50;">✅</div>
                <div class="stat-value">12</div>
                <div style="color: #666; font-size: 0.8rem;">Turnos Completados</div>
            </div>
            <div class="stat-card">
                <div style="color: #2196F3;">⏰</div>
                <div class="stat-value">96h</div>
                <div style="color: #666; font-size: 0.8rem;">Horas Totales</div>
            </div>
            <div class="stat-card">
                <div style="color: #FF9800;">📅</div>
                <div class="stat-value">6</div>
                <div style="color: #666; font-size: 0.8rem;">Próximos Turnos</div>
            </div>
            <div class="stat-card">
                <div style="color: #9C27B0;">💰</div>
                <div class="stat-value">€2,850</div>
                <div style="color: #666; font-size: 0.8rem;">Salario Estimado</div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        © {datetime.datetime.now().year} Socorrista Pro • Versión 2.2
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra main-content
    
    # Modal simple
    st.markdown("""
    <div id="calendar-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); z-index: 9999; align-items: center; justify-content: center; padding: 15px;">
        <div style="background: white; border-radius: 15px; padding: 20px; max-width: 400px; width: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #333; font-size: 1.2rem;">📅 Calendario de Turnos</h3>
                <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; width: 30px; height: 30px; border-radius: 50%; font-size: 1rem; cursor: pointer;">×</button>
            </div>
            <div style="color: #666; margin-bottom: 15px; font-size: 0.9rem;">
                <p>Próximamente podrás gestionar tus turnos de forma completa.</p>
            </div>
            <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%;">Cerrar</button>
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
    
    // Cerrar modal al hacer clic fuera
    document.addEventListener('click', function(event) {
        if (event.target.id === 'calendar-modal') {
            closeCalendarModal();
        }
    });
    
    // Cerrar con ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeCalendarModal();
        }
    });
    </script>
    """, unsafe_allow_html=True)

def create_other_view(view_name):
    """Crea vistas para otras secciones - Versión compacta"""
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
    <div class="main-content" style="max-width: 800px;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 10px; color: {PRIMARY_COLOR};">📋</div>
            <h2 style="color: {SECONDARY_COLOR}; margin-bottom: 8px; font-size: 1.4rem; font-weight: 700;">
                {title}
            </h2>
            <p style="color: #666; font-size: 0.9rem;">
                Esta funcionalidad está en desarrollo activo
            </p>
        </div>
        
        <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 20px;">
            <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-size: 1.1rem; font-weight: 700;">
                🚀 Próximamente
            </h3>
            <p style="color: #666; line-height: 1.5; margin-bottom: 15px; font-size: 0.9rem;">
                Estamos trabajando para implementar esta funcionalidad con los más altos estándares de calidad.
            </p>
        </div>
        
        <div style="text-align: center;">
            <a href="?" style="background: {PRIMARY_COLOR}; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: 600; font-size: 0.9rem;">
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
