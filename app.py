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
# ESTILOS CSS - ENFOQUE COMPLETAMENTE NUEVO
# ----------------------------
def apply_custom_css():
    """Aplica estilos CSS con enfoque moderno sin conflictos"""
    st.markdown(f"""
    <style>
    /* RESET BÁSICO */
    .stApp {{
        background: {BG_COLOR};
    }}
    
    /* ELIMINAR ESPACIOS DE STREAMLIT */
    header {{ 
        display: none !important; 
    }}
    
    [data-testid="stHeader"] {{ 
        display: none !important; 
    }}
    
    /* CONTENEDOR PRINCIPAL SIN MÁRGENES */
    .main-block {{
        width: 100%;
        max-width: 100%;
        margin: 0;
        padding: 0;
    }}
    
    /* HEADER PERSONALIZADO */
    .custom-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 15px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }}
    
    /* TÍTULO PRINCIPAL */
    .title-section {{
        background: linear-gradient(135deg, #1a5276, #1c5c82, {PRIMARY_COLOR});
        padding: 35px 20px;
        text-align: center;
    }}
    
    .main-title {{
        color: white;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0 0 10px 0;
    }}
    
    .subtitle {{
        color: rgba(255,255,255,0.95);
        font-size: 1rem;
        margin: 0;
    }}
    
    /* CONTENEDOR PARA TARJETAS */
    .cards-wrapper {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 25px 20px;
    }}
    
    /* ====== VERSIÓN ESCRITORIO ====== */
    .desktop-layout {{
        display: block;
    }}
    
    .desktop-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin-bottom: 30px;
    }}
    
    .desktop-card {{
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-decoration: none !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        min-height: 220px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    .desktop-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, #FF8C42);
        border-radius: 20px 20px 0 0;
    }}
    
    .desktop-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(243, 112, 33, 0.2);
    }}
    
    .desktop-icon {{
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        font-size: 28px;
        color: white;
    }}
    
    .desktop-card-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin: 0 0 10px 0;
    }}
    
    .desktop-card-desc {{
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }}
    
    /* ====== VERSIÓN MÓVIL ====== */
    @media (max-width: 768px) {{
        /* OCULTAR VERSIÓN ESCRITORIO */
        .desktop-layout {{
            display: none !important;
        }}
        
        /* MOSTRAR VERSIÓN MÓVIL */
        .mobile-layout {{
            display: block !important;
        }}
        
        .cards-wrapper {{
            padding: 20px 15px;
        }}
        
        .mobile-grid {{
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 15px !important;
            width: 100% !important;
            margin: 0 auto !important;
        }}
        
        /* AJUSTES PARA GARANTIZAR 2 COLUMNAS */
        .mobile-grid > * {{
            grid-column: span 1 !important;
            width: 100% !important;
        }}
        
        .mobile-card {{
            background: white;
            border-radius: 15px;
            padding: 20px 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            min-height: 135px;
            transition: all 0.3s ease;
            border: 1px solid rgba(0,0,0,0.05);
            width: 100% !important;
            position: relative;
        }}
        
        .mobile-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, {PRIMARY_COLOR}, #FF8C42);
            border-radius: 15px 15px 0 0;
        }}
        
        .mobile-card:hover {{
            border-color: {PRIMARY_COLOR};
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(243, 112, 33, 0.15);
        }}
        
        .mobile-icon {{
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
        
        .mobile-card-title {{
            font-size: 0.9rem !important;
            font-weight: 600;
            color: {SECONDARY_COLOR};
            margin: 0;
            line-height: 1.2;
        }}
        
        .title-section {{
            padding: 25px 15px;
        }}
        
        .main-title {{
            font-size: 1.9rem;
        }}
        
        .subtitle {{
            font-size: 0.9rem;
        }}
        
        .custom-header {{
            padding: 12px 15px;
        }}
        
        /* Asegurar que no haya desbordamiento horizontal */
        html, body, .stApp {{
            overflow-x: hidden !important;
            max-width: 100% !important;
        }}
        
        /* Forzar 2 columnas incluso en pantallas muy pequeñas */
        @media (max-width: 380px) {{
            .mobile-grid {{
                gap: 10px !important;
            }}
            
            .mobile-card {{
                padding: 15px 10px !important;
                min-height: 125px !important;
            }}
            
            .mobile-icon {{
                width: 45px !important;
                height: 45px !important;
                font-size: 20px !important;
            }}
            
            .mobile-card-title {{
                font-size: 0.85rem !important;
            }}
        }}
    }}
    
    /* ESCRITORIO: OCULTAR VERSIÓN MÓVIL */
    @media (min-width: 769px) {{
        .mobile-layout {{
            display: none !important;
        }}
        
        .desktop-layout {{
            display: block;
        }}
    }}
    
    /* ESTADÍSTICAS */
    .stats-container {{
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 40px auto 0;
        max-width: 1200px;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }}
    
    @media (max-width: 768px) {{
        .stats-container {{
            padding: 20px;
            margin-top: 25px;
        }}
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
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
    footer {{ 
        display: none !important; 
    }}
    
    .stDeployButton {{ 
        display: none !important; 
    }}
    
    /* FIX PARA LAS COLUMNAS DE STREAMLIT */
    [data-testid="column"] {{
        min-width: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES
# ----------------------------
def create_header():
    """Crea el encabezado"""
    st.markdown(f"""
    <div class="custom-header">
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
    <div class="title-section">
        <h1 class="main-title">Panel de Control</h1>
        <p class="subtitle">Gestión centralizada de turnos y asistencia</p>
    </div>
    
    <div class="cards-wrapper">
    """, unsafe_allow_html=True)
    
    # ====== VERSIÓN ESCRITORIO ======
    # Usamos st.columns para escritorio - NO TOCAR ESTO
    st.markdown('<div class="desktop-layout">', unsafe_allow_html=True)
    
    # Fila 1
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="desktop-card" onclick="openCalendarModal()">
            <div class="desktop-icon">📅</div>
            <h3 class="desktop-card-title">Horarios</h3>
            <p class="desktop-card-desc">Consulta y gestiona tus turnos programados</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <a href="?view=asistencia" class="desktop-card">
            <div class="desktop-icon">✅</div>
            <h3 class="desktop-card-title">Control de Asistencia</h3>
            <p class="desktop-card-desc">Registro de entrada y salida en tiempo real</p>
        </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <a href="?view=nomina" class="desktop-card">
            <div class="desktop-icon">💰</div>
            <h3 class="desktop-card-title">Nómina y Pagos</h3>
            <p class="desktop-card-desc">Consulta tus recibos y estados de pago</p>
        </a>
        """, unsafe_allow_html=True)
    
    # Fila 2
    col4, col5, col6 = st.columns(3, gap="large")
    
    with col4:
        st.markdown(f"""
        <a href="?view=incidencias" class="desktop-card">
            <div class="desktop-icon">⚠️</div>
            <h3 class="desktop-card-title">Incidencias</h3>
            <p class="desktop-card-desc">Reporta y consulta incidencias</p>
        </a>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <a href="?view=formacion" class="desktop-card">
            <div class="desktop-icon">🎓</div>
            <h3 class="desktop-card-title">Formación</h3>
            <p class="desktop-card-desc">Accede a cursos y certificaciones</p>
        </a>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <a href="?view=comunicados" class="desktop-card">
            <div class="desktop-icon">📢</div>
            <h3 class="desktop-card-title">Comunicados</h3>
            <p class="desktop-card-desc">Últimas noticias y anuncios</p>
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra desktop-layout
    
    # ====== VERSIÓN MÓVIL ======
    # Grid CSS puro para móvil - ESTA ES LA SOLUCIÓN
    st.markdown("""
    <div class="mobile-layout" style="display: none;">
        <div class="mobile-grid">
            <!-- Fila 1 - 2 tarjetas -->
            <div class="mobile-card" onclick="openCalendarModal()">
                <div class="mobile-icon">📅</div>
                <h3 class="mobile-card-title">Horarios</h3>
            </div>
            
            <a href="?view=asistencia" class="mobile-card">
                <div class="mobile-icon">✅</div>
                <h3 class="mobile-card-title">Control Asistencia</h3>
            </a>
            
            <!-- Fila 2 - 2 tarjetas -->
            <a href="?view=nomina" class="mobile-card">
                <div class="mobile-icon">💰</div>
                <h3 class="mobile-card-title">Nómina y Pagos</h3>
            </a>
            
            <a href="?view=incidencias" class="mobile-card">
                <div class="mobile-icon">⚠️</div>
                <h3 class="mobile-card-title">Incidencias</h3>
            </a>
            
            <!-- Fila 3 - 2 tarjetas -->
            <a href="?view=formacion" class="mobile-card">
                <div class="mobile-icon">🎓</div>
                <h3 class="mobile-card-title">Formación</h3>
            </a>
            
            <a href="?view=comunicados" class="mobile-card">
                <div class="mobile-icon">📢</div>
                <h3 class="mobile-card-title">Comunicados</h3>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cerrar cards-wrapper
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # Modal del calendario (oculto por defecto)
    st.markdown("""
    <div id="calendar-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.95); z-index: 9999; align-items: center; justify-content: center; padding: 20px;">
        <div style="background: white; border-radius: 20px; padding: 30px; max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="margin: 0; color: #333; font-size: 1.5rem;">📅 Calendario de Turnos</h2>
                <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center;">×</button>
            </div>
            <div style="color: #666; margin-bottom: 20px; line-height: 1.6;">
                <p>Esta funcionalidad está en desarrollo. Próximamente podrás ver tu calendario completo aquí.</p>
            </div>
            <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; padding: 12px 24px; border-radius: 10px; cursor: pointer; font-weight: 600; width: 100%;">Cerrar</button>
        </div>
    </div>
    
    <script>
    // Funciones para el modal
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
    
    // Detectar tamaño de pantalla y mostrar versión correcta
    function adjustLayout() {
        const isMobile = window.innerWidth <= 768;
        const desktopLayout = document.querySelector('.desktop-layout');
        const mobileLayout = document.querySelector('.mobile-layout');
        
        if (isMobile) {
            // Móvil: mostrar grid, ocultar columnas
            if (desktopLayout) desktopLayout.style.display = 'none';
            if (mobileLayout) mobileLayout.style.display = 'block';
        } else {
            // Escritorio: mostrar columnas, ocultar grid
            if (desktopLayout) desktopLayout.style.display = 'block';
            if (mobileLayout) mobileLayout.style.display = 'none';
        }
    }
    
    // Ejecutar al cargar y al cambiar tamaño
    window.addEventListener('load', adjustLayout);
    window.addEventListener('resize', adjustLayout);
    
    // Asegurar que el grid móvil mantenga 2 columnas
    function fixMobileGrid() {
        if (window.innerWidth <= 768) {
            const mobileGrid = document.querySelector('.mobile-grid');
            if (mobileGrid) {
                mobileGrid.style.gridTemplateColumns = 'repeat(2, 1fr)';
                mobileGrid.style.display = 'grid';
            }
        }
    }
    
    window.addEventListener('resize', fixMobileGrid);
    </script>
    """, unsafe_allow_html=True)

def create_other_view(view_name):
    """Crea vistas para otras secciones"""
    view_titles = {
        "asistencia": "Control de Asistencia",
        "nomina": "Nómina y Pagos", 
        "incidencias": "Incidencias",
        "formacion": "Formación",
        "comunicados": "Comunicados"
    }
    
    title = view_titles.get(view_name, view_name.capitalize())
    
    apply_custom_css()
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
        st.markdown('<script>openCalendarModal();</script>', unsafe_allow_html=True)
        create_dashboard()
    elif view in ["asistencia", "nomina", "incidencias", "formacion", "comunicados"]:
        create_other_view(view)
    else:
        create_dashboard()

if __name__ == "__main__":
    main()
