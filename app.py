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
# ESTILOS CSS ÚNICOS - SOLUCIÓN COMPLETA
# ----------------------------
def apply_custom_css():
    """Aplica estilos CSS personalizados con solución móvil robusta"""
    st.markdown(f"""
    <style>
    /* ELIMINAR MÁRGENES SUPERIORES */
    .stApp > header {{
        display: none !important;
    }}
    
    div.stApp {{
        background: {BG_COLOR};
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    
    #MainMenu {{
        visibility: hidden;
    }}
    
    /* HEADER */
    .custom-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }}
    
    /* TÍTULO */
    .custom-title-section {{
        background: linear-gradient(135deg, #1a5276, #1c5c82, {PRIMARY_COLOR});
        padding: 25px 20px;
        text-align: center;
        margin-top: 0;
    }}
    
    .custom-title {{
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }}
    
    .custom-subtitle {{
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
    }}
    
    /* CONTENEDOR PRINCIPAL */
    .custom-container {{
        padding: 25px 15px;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    /* ESCRITORIO: 3 COLUMNAS */
    @media (min-width: 769px) {{
        .desktop-grid {{
            display: grid !important;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            width: 100%;
        }}
        
        .desktop-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            text-align: center;
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 1px solid rgba(0,0,0,0.05);
            min-height: 180px;
            transition: all 0.3s ease;
        }}
        
        .desktop-card:hover {{
            transform: translateY(-5px);
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 12px 25px rgba(243, 112, 33, 0.15);
        }}
        
        .desktop-icon {{
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
        
        .desktop-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: {SECONDARY_COLOR};
            margin-bottom: 8px;
        }}
        
        .desktop-desc {{
            color: #666;
            font-size: 0.9rem;
            line-height: 1.4;
        }}
        
        /* OCULTAR VERSIÓN MÓVIL */
        .mobile-grid {{
            display: none !important;
        }}
    }}
    
    /* MÓVIL: 2 COLUMNAS CON FLEXBOX ROBUSTO */
    @media (max-width: 768px) {{
        /* ELIMINAR MÁRGENES DE STREAMLIT */
        .block-container {{
            padding-top: 0 !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }}
        
        .custom-container {{
            padding: 15px 10px !important;
            width: 100% !important;
            max-width: 100% !important;
        }}
        
        /* OCULTAR VERSIÓN ESCRITORIO */
        .desktop-grid {{
            display: none !important;
        }}
        
        /* SISTEMA MÓVIL CON FLEXBOX - 2 COLUMNAS */
        .mobile-grid {{
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 10px !important;
            width: 100% !important;
            justify-content: space-between !important;
        }}
        
        .mobile-card-container {{
            width: calc(50% - 5px) !important;
            min-width: calc(50% - 5px) !important;
            flex: 0 0 calc(50% - 5px) !important;
            margin-bottom: 10px !important;
        }}
        
        .custom-card {{
            background: white;
            border-radius: 12px;
            padding: 15px 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            text-align: center;
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 1px solid rgba(0,0,0,0.05);
            height: 100% !important;
            min-height: 120px;
            width: 100% !important;
        }}
        
        .custom-card:hover {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 6px 15px rgba(243, 112, 33, 0.15);
        }}
        
        .custom-icon {{
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff944d);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 8px;
            font-size: 20px;
            color: white;
            flex-shrink: 0;
        }}
        
        .custom-card-title {{
            font-size: 0.8rem !important;
            font-weight: 600;
            color: {SECONDARY_COLOR};
            margin: 0;
            line-height: 1.2;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        
        .custom-title {{
            font-size: 1.6rem !important;
        }}
        
        .custom-subtitle {{
            font-size: 0.85rem !important;
        }}
        
        .custom-header {{
            padding: 8px 15px !important;
        }}
    }}
    
    /* MÓVIL MUY PEQUEÑO - 1 COLUMNA */
    @media (max-width: 380px) {{
        .mobile-card-container {{
            width: 100% !important;
            flex: 0 0 100% !important;
        }}
    }}
    
    /* ESTADÍSTICAS */
    .custom-stats {{
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        margin-top: 30px;
    }}
    
    .custom-stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
    }}
    
    @media (max-width: 768px) {{
        .custom-stats {{
            padding: 15px !important;
            margin-top: 20px !important;
        }}
        
        .custom-stats-grid {{
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 10px !important;
        }}
        
        .custom-stat-card {{
            padding: 12px !important;
        }}
        
        .custom-stat-value {{
            font-size: 1.3rem !important;
        }}
    }}
    
    @media (max-width: 480px) {{
        .custom-stats-grid {{
            grid-template-columns: 1fr !important;
        }}
    }}
    
    .custom-stat-card {{
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border-left: 3px solid {PRIMARY_COLOR};
    }}
    
    .custom-stat-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin: 5px 0;
    }}
    
    /* FOOTER */
    .custom-footer {{
        text-align: center;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid rgba(0,0,0,0.1);
        color: #666;
        font-size: 0.8rem;
    }}
    
    /* OCULTAR ELEMENTOS STREAMLIT */
    [data-testid="stHeader"] {{ 
        display: none !important; 
        height: 0 !important;
    }}
    
    footer {{ 
        display: none !important; 
    }}
    
    .stDeployButton {{ 
        display: none !important; 
    }}
    
    /* FIX PARA STREAMLIT PADDING */
    section.main.st-emotion-cache-uf99v8.ea3mdgi5 {{
        padding-top: 0 !important;
    }}
    
    div.st-emotion-cache-1v0mbdj.e115fcil1 {{
        padding-top: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# COMPONENTES
# ----------------------------
def create_header():
    st.markdown(f"""
    <div class="custom-header">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.3rem;">🛟</span>
            <span style="font-size: 1.1rem; font-weight: 600;">SOCORRISTA PRO</span>
        </div>
        <div>
            <div style="background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 20px; display: flex; align-items: center; gap: 8px;">
                <span>👤</span>
                <div style="line-height: 1.2;">
                    <div style="font-size: 0.85rem; font-weight: 500;">Carlos Rodríguez</div>
                    <div style="font-size: 0.7rem; opacity: 0.9;">Socorrista Principal</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_dashboard():
    """Dashboard con soluciones separadas para escritorio y móvil"""
    # Aplicar CSS
    apply_custom_css()
    
    # Crear header
    create_header()
    
    # Título principal
    st.markdown(f"""
    <div class="custom-title-section">
        <h1 class="custom-title">Panel de Control</h1>
        <p class="custom-subtitle">Gestión centralizada de turnos y asistencia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenedor principal
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    
    # **VERSIÓN ESCRITORIO: Grid CSS (NO st.columns)**
    st.markdown("""
    <div class="desktop-grid">
        <!-- Fila 1 -->
        <div class="desktop-card" onclick="openCalendarModal()">
            <div class="desktop-icon">📅</div>
            <h3 class="desktop-title">Horarios</h3>
            <p class="desktop-desc">Consulta y gestiona tus turnos</p>
        </div>
        
        <a href="?view=asistencia" class="desktop-card">
            <div class="desktop-icon">✅</div>
            <h3 class="desktop-title">Control Asistencia</h3>
            <p class="desktop-desc">Registro entrada/salida</p>
        </a>
        
        <a href="?view=nomina" class="desktop-card">
            <div class="desktop-icon">💰</div>
            <h3 class="desktop-title">Nómina y Pagos</h3>
            <p class="desktop-desc">Recibos y estados de pago</p>
        </a>
        
        <!-- Fila 2 -->
        <a href="?view=incidencias" class="desktop-card">
            <div class="desktop-icon">⚠️</div>
            <h3 class="desktop-title">Incidencias</h3>
            <p class="desktop-desc">Reporta y consulta incidencias</p>
        </a>
        
        <a href="?view=formacion" class="desktop-card">
            <div class="desktop-icon">🎓</div>
            <h3 class="desktop-title">Formación</h3>
            <p class="desktop-desc">Cursos y certificaciones</p>
        </a>
        
        <a href="?view=comunicados" class="desktop-card">
            <div class="desktop-icon">📢</div>
            <h3 class="desktop-title">Comunicados</h3>
            <p class="desktop-desc">Noticias y anuncios</p>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # **VERSIÓN MÓVIL: Flexbox con contenedores (2 columnas)**
    st.markdown("""
    <div class="mobile-grid">
        <!-- Fila 1 -->
        <div class="mobile-card-container">
            <div class="custom-card" onclick="openCalendarModal()">
                <div class="custom-icon">📅</div>
                <h3 class="custom-card-title">Horarios</h3>
            </div>
        </div>
        
        <div class="mobile-card-container">
            <a href="?view=asistencia" class="custom-card">
                <div class="custom-icon">✅</div>
                <h3 class="custom-card-title">Control Asistencia</h3>
            </a>
        </div>
        
        <!-- Fila 2 -->
        <div class="mobile-card-container">
            <a href="?view=nomina" class="custom-card">
                <div class="custom-icon">💰</div>
                <h3 class="custom-card-title">Nómina y Pagos</h3>
            </a>
        </div>
        
        <div class="mobile-card-container">
            <a href="?view=incidencias" class="custom-card">
                <div class="custom-icon">⚠️</div>
                <h3 class="custom-card-title">Incidencias</h3>
            </a>
        </div>
        
        <!-- Fila 3 -->
        <div class="mobile-card-container">
            <a href="?view=formacion" class="custom-card">
                <div class="custom-icon">🎓</div>
                <h3 class="custom-card-title">Formación</h3>
            </a>
        </div>
        
        <div class="mobile-card-container">
            <a href="?view=comunicados" class="custom-card">
                <div class="custom-icon">📢</div>
                <h3 class="custom-card-title">Comunicados</h3>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas
    st.markdown(f"""
    <div class="custom-stats">
        <div class="custom-stats-grid">
            <div class="custom-stat-card">
                <div style="color: #4CAF50;">✅</div>
                <div class="custom-stat-value">12</div>
                <div style="color: #666; font-size: 0.8rem;">Turnos Completados</div>
            </div>
            <div class="custom-stat-card">
                <div style="color: #2196F3;">⏰</div>
                <div class="custom-stat-value">96h</div>
                <div style="color: #666; font-size: 0.8rem;">Horas Totales</div>
            </div>
            <div class="custom-stat-card">
                <div style="color: #FF9800;">📅</div>
                <div class="custom-stat-value">6</div>
                <div style="color: #666; font-size: 0.8rem;">Próximos Turnos</div>
            </div>
            <div class="custom-stat-card">
                <div style="color: #9C27B0;">💰</div>
                <div class="custom-stat-value">€2,850</div>
                <div style="color: #666; font-size: 0.8rem;">Salario Estimado</div>
            </div>
        </div>
    </div>
    
    <div class="custom-footer">
        © {datetime.datetime.now().year} Socorrista Pro • Versión 2.2
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Modal
    st.markdown("""
    <div id="calendar-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); z-index: 9999; align-items: center; justify-content: center; padding: 15px;">
        <div style="background: white; border-radius: 15px; padding: 20px; max-width: 400px; width: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #333; font-size: 1.2rem;">📅 Calendario</h3>
                <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; width: 30px; height: 30px; border-radius: 50%; font-size: 1rem; cursor: pointer;">×</button>
            </div>
            <div style="color: #666; margin-bottom: 15px; font-size: 0.9rem;">
                <p>Próximamente podrás gestionar tus turnos.</p>
            </div>
            <button onclick="closeCalendarModal()" style="background: #F37021; color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%;">Cerrar</button>
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
    
    // Detectar clic fuera del modal para cerrar
    document.addEventListener('click', function(event) {
        if (event.target.id === 'calendar-modal') {
            closeCalendarModal();
        }
    });
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeCalendarModal();
        }
    });
    
    // Asegurar que las tarjetas móviles mantengan su tamaño
    function fixMobileCards() {
        if (window.innerWidth <= 768) {
            const cards = document.querySelectorAll('.mobile-card-container');
            cards.forEach(card => {
                card.style.flex = '0 0 calc(50% - 5px)';
                card.style.width = 'calc(50% - 5px)';
            });
        }
    }
    
    window.addEventListener('load', fixMobileCards);
    window.addEventListener('resize', fixMobileCards);
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
    <div class="custom-container" style="max-width: 800px;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 10px; color: {PRIMARY_COLOR};">📋</div>
            <h2 style="color: {SECONDARY_COLOR}; margin-bottom: 8px; font-size: 1.4rem; font-weight: 700;">
                {title}
            </h2>
            <p style="color: #666; font-size: 0.9rem;">En desarrollo</p>
        </div>
        
        <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 20px;">
            <p style="color: #666; line-height: 1.5; margin-bottom: 15px; font-size: 0.9rem;">
                Estamos trabajando para implementar esta funcionalidad.
            </p>
        </div>
        
        <div style="text-align: center;">
            <a href="?" style="background: {PRIMARY_COLOR}; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: 600; font-size: 0.9rem;">
                ← Volver
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
