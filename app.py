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
# ESTILOS CSS OPTIMIZADOS PARA MÓVIL Y ESCRITORIO
# ----------------------------
def apply_custom_css():
    """Aplica estilos CSS personalizados"""
    st.markdown(f"""
    <style>
    /* RESET BÁSICO */
    .stApp {{
        background: {BG_COLOR};
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* ELIMINAR TODOS LOS ESPACIOS DE STREAMLIT */
    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    [data-testid="stMainBlockContainer"] {{
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
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
        width: 100%;
        box-sizing: border-box;
    }}
    
    /* TÍTULO PROFESIONAL Y COMPACTO */
    .page-title-section {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        padding: 30px 20px;
        text-align: center;
        margin-bottom: 0;
        width: 100%;
        box-sizing: border-box;
    }}
    
    .page-title {{
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 8px;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .page-subtitle {{
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.4;
        font-weight: 300;
    }}
    
    /* CONTENEDOR PRINCIPAL */
    .main-content {{
        padding: 30px 20px;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        box-sizing: border-box;
    }}
    
    /* CONTENEDOR DE TARJETAS CON FLEXBOX */
    .cards-container {{
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
    }}
    
    /* TARJETAS PARA ESCRITORIO: 3 por fila */
    .dashboard-card {{
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
        text-decoration: none !important;
        display: flex;
        flex-direction: column;
        min-height: 200px;
        width: calc(33.333% - 14px); /* 3 tarjetas por fila en escritorio */
        position: relative;
        overflow: hidden;
        box-sizing: border-box;
        border: 1px solid rgba(243, 112, 33, 0.1);
    }}
    
    .dashboard-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, #FF8C42);
        border-radius: 16px 16px 0 0;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(243, 112, 33, 0.15);
        border-color: {PRIMARY_COLOR};
    }}
    
    .card-icon {{
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 14px;
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
        line-height: 1.3;
    }}
    
    .card-desc {{
        color: #666;
        font-size: 0.9rem;
        line-height: 1.4;
        font-family: 'Segoe UI', sans-serif;
        opacity: 0.9;
    }}
    
    /* MÓVIL: 2 tarjetas por fila (3 filas) */
    @media (max-width: 768px) {{
        /* HEADER MÓVIL MÁS COMPACTO */
        .main-header {{
            padding: 10px 15px;
        }}
        
        /* TÍTULO MÓVIL MÁS COMPACTO */
        .page-title-section {{
            padding: 20px 15px;
        }}
        
        .page-title {{
            font-size: 1.6rem;
            margin-bottom: 5px;
        }}
        
        .page-subtitle {{
            font-size: 0.9rem;
            line-height: 1.3;
            padding: 0 10px;
        }}
        
        /* CONTENEDOR MÓVIL */
        .main-content {{
            padding: 20px 15px;
        }}
        
        /* TARJETAS MÓVIL: 2 por fila */
        .cards-container {{
            gap: 12px;
        }}
        
        .dashboard-card {{
            width: calc(50% - 6px); /* 2 tarjetas por fila en móvil */
            min-height: 170px;
            padding: 20px;
            border-radius: 14px;
        }}
        
        .card-icon {{
            width: 50px;
            height: 50px;
            font-size: 24px;
            margin-bottom: 12px;
            border-radius: 12px;
        }}
        
        .card-title {{
            font-size: 1.1rem;
            margin-bottom: 6px;
        }}
        
        .card-desc {{
            font-size: 0.85rem;
            line-height: 1.3;
        }}
    }}
    
    /* MÓVIL MUY PEQUEÑO: 1 columna */
    @media (max-width: 480px) {{
        .dashboard-card {{
            width: 100%;
        }}
        
        .page-title {{
            font-size: 1.4rem;
        }}
        
        .page-subtitle {{
            font-size: 0.85rem;
        }}
    }}
    
    /* ESTADÍSTICAS PROFESIONALES */
    .stats-container {{
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin: 35px auto 0;
        width: 100%;
        box-sizing: border-box;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    .stats-title {{
        color: {SECONDARY_COLOR};
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        width: 100%;
    }}
    
    .stat-card {{
        background: #f8f9fa;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        border-left: 4px solid {PRIMARY_COLOR};
        transition: transform 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-3px);
        background: #f0f2f5;
    }}
    
    .stat-icon {{
        font-size: 1.3rem;
        margin-bottom: 8px;
        display: block;
    }}
    
    .stat-value {{
        font-size: 1.8rem;
        font-weight: 800;
        margin: 8px 0;
        color: {SECONDARY_COLOR};
        font-family: 'Segoe UI', sans-serif;
    }}
    
    .stat-label {{
        color: #666;
        font-size: 0.85rem;
        font-weight: 500;
    }}
    
    /* RESPONSIVE PARA ESTADÍSTICAS */
    @media (max-width: 768px) {{
        .stats-container {{
            padding: 20px;
            margin: 25px auto 0;
        }}
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        
        .stat-card {{
            padding: 15px;
        }}
        
        .stat-value {{
            font-size: 1.6rem;
        }}
        
        .stats-title {{
            font-size: 1.2rem;
            margin-bottom: 15px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .stats-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    /* FOOTER PROFESIONAL */
    .footer {{
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid rgba(0,0,0,0.1);
        color: #777;
        font-size: 0.8rem;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    /* MODAL SIMPLE */
    .modal-overlay {{
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
        padding: 15px;
    }}
    
    .modal-content {{
        background: white;
        border-radius: 18px;
        padding: 25px;
        max-width: 500px;
        width: 100%;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        animation: modalSlide 0.3s ease;
    }}
    
    @keyframes modalSlide {{
        from {{ transform: translateY(30px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    .modal-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid {PRIMARY_COLOR};
    }}
    
    .modal-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .modal-close {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        font-size: 1.2rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }}
    
    .modal-close:hover {{
        background: #e55a1a;
        transform: rotate(90deg);
    }}
    
    /* OCULTAR ELEMENTOS DE STREAMLIT */
    [data-testid="stHeader"] {{ display: none !important; }}
    footer {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    
    /* FORZAR QUE LAS TARJETAS SEAN VISIBLES */
    a.dashboard-card {{
        display: flex !important;
    }}
    
    /* ANIMACIÓN SUAVE */
    .fade-in {{
        animation: fadeIn 0.5s ease;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES DE LA APLICACIÓN
# ----------------------------
def create_header():
    """Crea el encabezado profesional y compacto"""
    st.markdown(f"""
    <div class="main-header fade-in">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.3rem;">🛟</span>
            <span style="font-size: 1.2rem; font-weight: 700;">SOCORRISTA PRO</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 20px; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1rem;">👤</span>
                <div style="line-height: 1.2;">
                    <div style="font-weight: 600; font-size: 0.9rem;">Carlos Rodríguez</div>
                    <div style="font-size: 0.75rem; opacity: 0.9;">Socorrista Principal</div>
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
    
    # Título principal compacto y profesional
    st.markdown(f"""
    <div class="page-title-section fade-in">
        <h1 class="page-title">Panel de Control</h1>
        <p class="page-subtitle">Gestión centralizada de turnos, asistencia y nómina</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenedor principal
    st.markdown('<div class="main-content fade-in">', unsafe_allow_html=True)
    
    # **GRID DE TARJETAS USANDO FLEXBOX** - RESPONSIVE
    st.markdown('<div class="cards-container">', unsafe_allow_html=True)
    
    # Tarjetas en el ORDEN ESPECÍFICO solicitado
    cards_data = [
        # Fila 1 en escritorio (3 tarjetas), 2 tarjetas en móvil
        {"title": "Horarios", "icon": "📅", "desc": "Consulta y gestiona turnos", "view": "horarios", "onclick": "openCalendarModal()"},
        {"title": "Control de Asistencia", "icon": "✅", "desc": "Registro entrada/salida", "view": "asistencia", "onclick": None},
        {"title": "Nómina y Pagos", "icon": "💰", "desc": "Recibos y estados de pago", "view": "nomina", "onclick": None},
        # Fila 2 en escritorio (3 tarjetas), 2 tarjetas en móvil
        {"title": "Incidencias", "icon": "⚠️", "desc": "Reporta y consulta incidencias", "view": "incidencias", "onclick": None},
        {"title": "Formación", "icon": "🎓", "desc": "Cursos y certificaciones", "view": "formacion", "onclick": None},
        {"title": "Comunicados", "icon": "📢", "desc": "Noticias y anuncios", "view": "comunicados", "onclick": None},
    ]
    
    for card in cards_data:
        if card["view"] == "horarios":
            # Tarjeta especial para Horarios (abre modal)
            card_html = f"""
            <div class="dashboard-card" onclick="{card['onclick']}">
                <div class="card-icon">{card['icon']}</div>
                <h3 class="card-title">{card['title']}</h3>
                <p class="card-desc">{card['desc']}</p>
            </div>
            """
        else:
            # Otras tarjetas (enlaces normales)
            card_html = f"""
            <a href="?view={card['view']}" class="dashboard-card">
                <div class="card-icon">{card['icon']}</div>
                <h3 class="card-title">{card['title']}</h3>
                <p class="card-desc">{card['desc']}</p>
            </a>
            """
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra cards-container
    
    # Estadísticas profesionales
    st.markdown(f"""
    <div class="stats-container">
        <h3 class="stats-title">📊 Resumen del Mes</h3>
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-icon" style="color: #4CAF50;">✅</span>
                <div class="stat-value">12</div>
                <div class="stat-label">Turnos Completados</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon" style="color: #2196F3;">⏰</span>
                <div class="stat-value">96h</div>
                <div class="stat-label">Horas Totales</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon" style="color: #FF9800;">📅</span>
                <div class="stat-value">6</div>
                <div class="stat-label">Próximos Turnos</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon" style="color: #9C27B0;">💰</span>
                <div class="stat-value">€2,850</div>
                <div class="stat-label">Salario Estimado</div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        © {datetime.datetime.now().year} Socorrista Pro • Versión 2.2 • Sistema de Gestión Profesional
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra main-content
    
    # Modal del calendario profesional
    st.markdown(f"""
    <div id="calendar-modal" class="modal-overlay" style="display: none;">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">
                    <span>📅</span> Calendario de Turnos
                </div>
                <button class="modal-close" onclick="closeCalendarModal()">×</button>
            </div>
            <div style="color: #555; line-height: 1.5; margin-bottom: 20px;">
                <p>Esta funcionalidad está en desarrollo activo. Próximamente podrás gestionar tus turnos de forma completa.</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <button onclick="closeCalendarModal()" style="background: {PRIMARY_COLOR}; color: white; border: none; padding: 12px 20px; border-radius: 10px; cursor: pointer; font-weight: 600; flex: 1;">
                    Cerrar
                </button>
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
    
    // Cerrar modal al hacer clic fuera
    document.addEventListener('click', function(event) {{
        if (event.target.classList.contains('modal-overlay')) {{
            closeCalendarModal();
        }}
    }});
    
    // Cerrar con ESC
    document.addEventListener('keydown', function(event) {{
        if (event.key === 'Escape') {{
            closeCalendarModal();
        }}
    }});
    
    // Ajustar layout para móvil al cargar
    if (window.innerWidth <= 768) {{
        // Ya está configurado por CSS
    }}
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
    <div class="main-content fade-in" style="max-width: 800px;">
        <div style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 2.5rem; margin-bottom: 15px; color: {PRIMARY_COLOR};">📋</div>
            <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 10px; font-size: 1.8rem; font-weight: 700;">
                {title}
            </h1>
            <p style="color: #666; font-size: 1rem;">
                Esta funcionalidad está en desarrollo activo
            </p>
        </div>
        
        <div style="background: white; border-radius: 16px; padding: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 25px; border: 1px solid rgba(0,0,0,0.05);">
            <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-size: 1.3rem; font-weight: 700;">
                🚀 Próximamente
            </h3>
            <p style="color: #666; line-height: 1.5; margin-bottom: 15px; font-size: 0.95rem;">
                Estamos trabajando para implementar esta funcionalidad con los más altos estándares de calidad. 
                En las próximas semanas podrás acceder a todas las características avanzadas.
            </p>
        </div>
        
        <div style="text-align: center;">
            <a href="?" style="background: {PRIMARY_COLOR}; color: white; padding: 12px 25px; border-radius: 10px; text-decoration: none; display: inline-block; font-weight: 600; font-size: 0.95rem;">
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
