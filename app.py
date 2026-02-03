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
    """Aplica estilos CSS personalizados con enfoque agresivo"""
    st.markdown(f"""
    <style>
    /* RESET COMPLETO PARA STREAMLIT */
    div.stApp {{
        background: {BG_COLOR};
        padding: 0 !important;
        margin: 0 !important;
        min-height: 100vh;
    }}
    
    /* ELIMINAR TODOS LOS HEADERS DE STREAMLIT */
    header {{ display: none !important; }}
    [data-testid="stHeader"] {{ 
        display: none !important; 
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* ELIMINAR PADDINGS INTERNOS */
    .main .block-container {{
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }}
    
    /* HEADER PERSONALIZADO */
    .custom-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        width: 100%;
        box-sizing: border-box;
        position: relative;
        z-index: 100;
    }}
    
    /* SECCIÓN DE TÍTULO */
    .title-section {{
        background: linear-gradient(135deg, #1a5276, #1c5c82, {PRIMARY_COLOR});
        padding: 30px 20px;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }}
    
    .main-title {{
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 5px 0;
    }}
    
    .subtitle {{
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin: 0;
    }}
    
    /* CONTENEDOR PRINCIPAL */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 30px 20px;
        box-sizing: border-box;
    }}
    
    /* ===== VERSIÓN ESCRITORIO ===== */
    @media (min-width: 769px) {{
        /* GRID DE 3 COLUMNAS PARA ESCRITORIO */
        .desktop-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        /* TARJETAS ESCRITORIO */
        .card-desktop {{
            background: white;
            border-radius: 15px;
            padding: 30px 25px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            text-align: center;
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(0,0,0,0.05);
            min-height: 180px;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }}
        
        .card-desktop:hover {{
            transform: translateY(-5px);
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 12px 25px rgba(243, 112, 33, 0.15);
        }}
        
        .icon-desktop {{
            width: 65px;
            height: 65px;
            background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            font-size: 28px;
            color: white;
        }}
        
        .title-desktop {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {SECONDARY_COLOR};
            margin: 0 0 10px 0;
            line-height: 1.3;
        }}
        
        .desc-desktop {{
            color: #666;
            font-size: 0.95rem;
            line-height: 1.4;
            margin: 0;
        }}
        
        /* OCULTAR VERSIÓN MÓVIL */
        .mobile-container {{
            display: none !important;
        }}
    }}
    
    /* ===== VERSIÓN MÓVIL ===== */
    @media (max-width: 768px) {{
        /* AJUSTES DE PADDING PARA MÓVIL */
        .main-container {{
            padding: 20px 15px !important;
            max-width: 100% !important;
        }}
        
        .title-section {{
            padding: 25px 15px !important;
        }}
        
        .main-title {{
            font-size: 1.8rem !important;
        }}
        
        .subtitle {{
            font-size: 0.9rem !important;
        }}
        
        .custom-header {{
            padding: 10px 15px !important;
        }}
        
        /* OCULTAR VERSIÓN ESCRITORIO */
        .desktop-container {{
            display: none !important;
        }}
        
        /* GRID DE 2 COLUMNAS PARA MÓVIL */
        .mobile-grid {{
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 12px !important;
            width: 100% !important;
            margin-bottom: 20px !important;
        }}
        
        /* TARJETAS MÓVIL */
        .card-mobile {{
            background: white;
            border-radius: 12px;
            padding: 20px 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            text-align: center;
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(0,0,0,0.05);
            min-height: 130px;
            transition: all 0.3s ease;
            box-sizing: border-box;
            width: 100% !important;
        }}
        
        .card-mobile:hover {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 6px 15px rgba(243, 112, 33, 0.15);
        }}
        
        .icon-mobile {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            font-size: 22px;
            color: white;
        }}
        
        .title-mobile {{
            font-size: 0.85rem !important;
            font-weight: 600;
            color: {SECONDARY_COLOR};
            margin: 0;
            line-height: 1.2;
            text-align: center;
        }}
        
        /* MÓVIL MUY PEQUEÑO: 1 COLUMNA */
        @media (max-width: 380px) {{
            .mobile-grid {{
                grid-template-columns: 1fr !important;
            }}
        }}
    }}
    
    /* ESTADÍSTICAS - COMÚN */
    .stats-section {{
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        margin-top: 30px;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }}
    
    @media (max-width: 768px) {{
        .stats-section {{
            padding: 20px !important;
            margin-top: 20px !important;
        }}
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 15px !important;
        }}
        
        .stat-card {{
            padding: 15px !important;
        }}
        
        .stat-value {{
            font-size: 1.4rem !important;
        }}
    }}
    
    @media (max-width: 480px) {{
        .stats-grid {{
            grid-template-columns: 1fr !important;
        }}
    }}
    
    .stat-card {{
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border-left: 3px solid {PRIMARY_COLOR};
    }}
    
    .stat-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin: 8px 0;
    }}
    
    .stat-label {{
        color: #666;
        font-size: 0.85rem;
    }}
    
    /* FOOTER */
    .custom-footer {{
        text-align: center;
        margin-top: 25px;
        padding-top: 15px;
        border-top: 1px solid rgba(0,0,0,0.1);
        color: #666;
        font-size: 0.8rem;
    }}
    
    /* OCULTAR ELEMENTOS STREAMLIT */
    footer {{ 
        visibility: hidden !important;
        display: none !important; 
    }}
    
    .stDeployButton {{ 
        display: none !important; 
    }}
    
    #MainMenu {{ 
        visibility: hidden !important; 
    }}
    
    /* FIX PARA PREVENIR SCROLL HORIZONTAL */
    html, body {{
        overflow-x: hidden !important;
        max-width: 100% !important;
    }}
    
    /* ANULAR CUALQUIER ESTILO DE STREAMLIT EN LAS COLUMNAS */
    [data-testid="column"] {{
        padding: 0 !important;
        margin: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES
# ----------------------------
def create_header():
    st.markdown(f"""
    <div class="custom-header">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5rem;">🛟</span>
            <span style="font-size: 1.2rem; font-weight: 700;">SOCORRISTA PRO</span>
        </div>
        <div>
            <div style="background: rgba(255,255,255,0.15); padding: 8px 15px; border-radius: 20px; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.2rem;">👤</span>
                <div style="line-height: 1.2;">
                    <div style="font-size: 0.9rem; font-weight: 600;">Carlos Rodríguez</div>
                    <div style="font-size: 0.75rem; opacity: 0.9;">Socorrista Principal</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_dashboard():
    """Dashboard con diseño responsivo puro CSS"""
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
    
    <div class="main-container">
    """, unsafe_allow_html=True)
    
    # ===== VERSIÓN ESCRITORIO (3 columnas) =====
    st.markdown("""
    <div class="desktop-container">
        <div class="desktop-grid">
            <!-- Fila 1 - 3 tarjetas -->
            <div class="card-desktop" onclick="openCalendarModal()">
                <div class="icon-desktop">📅</div>
                <h3 class="title-desktop">Horarios</h3>
                <p class="desc-desktop">Consulta y gestiona tus turnos</p>
            </div>
            
            <a href="?view=asistencia" class="card-desktop">
                <div class="icon-desktop">✅</div>
                <h3 class="title-desktop">Control Asistencia</h3>
                <p class="desc-desktop">Registro entrada/salida</p>
            </a>
            
            <a href="?view=nomina" class="card-desktop">
                <div class="icon-desktop">💰</div>
                <h3 class="title-desktop">Nómina y Pagos</h3>
                <p class="desc-desktop">Recibos y estados de pago</p>
            </a>
            
            <!-- Fila 2 - 3 tarjetas -->
            <a href="?view=incidencias" class="card-desktop">
                <div class="icon-desktop">⚠️</div>
                <h3 class="title-desktop">Incidencias</h3>
                <p class="desc-desktop">Reporta y consulta incidencias</p>
            </a>
            
            <a href="?view=formacion" class="card-desktop">
                <div class="icon-desktop">🎓</div>
                <h3 class="title-desktop">Formación</h3>
                <p class="desc-desktop">Cursos y certificaciones</p>
            </a>
            
            <a href="?view=comunicados" class="card-desktop">
                <div class="icon-desktop">📢</div>
                <h3 class="title-desktop">Comunicados</h3>
                <p class="desc-desktop">Noticias y anuncios</p>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== VERSIÓN MÓVIL (2 columnas) =====
    st.markdown("""
    <div class="mobile-container">
        <div class="mobile-grid">
            <!-- Fila 1 - 2 tarjetas -->
            <div class="card-mobile" onclick="openCalendarModal()">
                <div class="icon-mobile">📅</div>
                <h3 class="title-mobile">Horarios</h3>
            </div>
            
            <a href="?view=asistencia" class="card-mobile">
                <div class="icon-mobile">✅</div>
                <h3 class="title-mobile">Control Asistencia</h3>
            </a>
            
            <!-- Fila 2 - 2 tarjetas -->
            <a href="?view=nomina" class="card-mobile">
                <div class="icon-mobile">💰</div>
                <h3 class="title-mobile">Nómina y Pagos</h3>
            </a>
            
            <a href="?view=incidencias" class="card-mobile">
                <div class="icon-mobile">⚠️</div>
                <h3 class="title-mobile">Incidencias</h3>
            </a>
            
            <!-- Fila 3 - 2 tarjetas -->
            <a href="?view=formacion" class="card-mobile">
                <div class="icon-mobile">🎓</div>
                <h3 class="title-mobile">Formación</h3>
            </a>
            
            <a href="?view=comunicados" class="card-mobile">
                <div class="icon-mobile">📢</div>
                <h3 class="title-mobile">Comunicados</h3>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas
    st.markdown(f"""
    <div class="stats-section">
        <div class="stats-grid">
            <div class="stat-card">
                <div style="color: #4CAF50; font-size: 1.5rem;">✅</div>
                <div class="stat-value">12</div>
                <div class="stat-label">Turnos Completados</div>
            </div>
            <div class="stat-card">
                <div style="color: #2196F3; font-size: 1.5rem;">⏰</div>
                <div class="stat-value">96h</div>
                <div class="stat-label">Horas Totales</div>
            </div>
            <div class="stat-card">
                <div style="color: #FF9800; font-size: 1.5rem;">📅</div>
                <div class="stat-value">6</div>
                <div class="stat-label">Próximos Turnos</div>
            </div>
            <div class="stat-card">
                <div style="color: #9C27B0; font-size: 1.5rem;">💰</div>
                <div class="stat-value">€2,850</div>
                <div class="stat-label">Salario Estimado</div>
            </div>
        </div>
    </div>
    
    <div class="custom-footer">
        © {datetime.datetime.now().year} Socorrista Pro • Versión 2.3
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Modal (solo cuando se hace clic)
    st.markdown("""
    <div id="calendar-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.95); z-index: 9999; align-items: center; justify-content: center; padding: 20px;">
        <div style="background: white; border-radius: 15px; padding: 25px; max-width: 400px; width: 100%; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #333; font-size: 1.3rem; font-weight: 700;">📅 Calendario</h3>
                <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; width: 32px; height: 32px; border-radius: 50%; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center;">×</button>
            </div>
            <div style="color: #666; margin-bottom: 20px; font-size: 0.95rem; line-height: 1.5;">
                <p>Próximamente podrás gestionar tus turnos en esta sección.</p>
            </div>
            <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; font-size: 1rem; transition: background 0.3s;">Cerrar</button>
        </div>
    </div>
    
    <script>
    function openCalendarModal() {
        const modal = document.getElementById('calendar-modal');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    function closeCalendarModal() {
        const modal = document.getElementById('calendar-modal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    // Detectar clic fuera del modal para cerrar
    document.addEventListener('click', function(event) {
        const modal = document.getElementById('calendar-modal');
        if (event.target === modal) {
            closeCalendarModal();
        }
    });
    
    // Cerrar con tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeCalendarModal();
        }
    });
    
    // Asegurar que la versión correcta se muestre al cargar
    function checkScreenSize() {
        const isMobile = window.innerWidth <= 768;
        const desktopContainer = document.querySelector('.desktop-container');
        const mobileContainer = document.querySelector('.mobile-container');
        
        if (isMobile) {
            if (desktopContainer) desktopContainer.style.display = 'none';
            if (mobileContainer) mobileContainer.style.display = 'block';
        } else {
            if (desktopContainer) desktopContainer.style.display = 'block';
            if (mobileContainer) mobileContainer.style.display = 'none';
        }
    }
    
    window.addEventListener('load', checkScreenSize);
    window.addEventListener('resize', checkScreenSize);
    
    // Inicializar al cargar
    document.addEventListener('DOMContentLoaded', checkScreenSize);
    </script>
    """, unsafe_allow_html=True)

def create_other_view(view_name):
    """Vista para otras secciones"""
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
    <div class="main-container" style="max-width: 800px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 3rem; margin-bottom: 15px; color: {PRIMARY_COLOR};">📋</div>
            <h2 style="color: {SECONDARY_COLOR}; margin-bottom: 10px; font-size: 1.8rem; font-weight: 700;">
                {title}
            </h2>
            <p style="color: #666; font-size: 1rem;">En desarrollo</p>
        </div>
        
        <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); margin-bottom: 30px;">
            <p style="color: #666; line-height: 1.6; margin-bottom: 20px; font-size: 1rem;">
                Esta funcionalidad está actualmente en desarrollo. Estamos trabajando para implementarla lo antes posible.
            </p>
            <div style="display: flex; align-items: center; background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <div style="font-size: 1.5rem; margin-right: 15px;">🚀</div>
                <div>
                    <p style="color: #666; margin: 0; font-size: 0.9rem;">Próximamente disponible</p>
                </div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="?" style="background: {PRIMARY_COLOR}; color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: 600; font-size: 1rem; transition: background 0.3s;">
                ← Volver al Panel
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# APLICACIÓN
# ----------------------------
def main():
    query_params = st.query_params.to_dict()
    view = query_params.get("view", [""])[0] if query_params.get("view") else ""
    
    if view == "horarios":
        st.markdown('<script>openCalendarModal();</script>', unsafe_allow_html=True)
        create_dashboard()
    elif view in ["asistencia", "nomina", "incidencias", "formacion", "comunicados"]:
        create_other_view(view)
    else:
        create_dashboard()

if __name__ == "__main__":
    main()
