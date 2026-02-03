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
# ESTILOS CSS ÚNICOS - SOLO ARREGLOS MÓVIL
# ----------------------------
def apply_custom_css():
    """Aplica estilos CSS personalizados solo para móvil"""
    st.markdown(f"""
    <style>
    /* ELIMINAR MÁRGENES SUPERIORES */
    [data-testid="stHeader"] {{ 
        display: none !important; 
    }}
    
    div.stApp {{
        background: {BG_COLOR};
    }}
    
    /* HEADER */
    .custom-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }}
    
    /* TÍTULO */
    .custom-title-section {{
        background: linear-gradient(135deg, #1a5276, #1c5c82, {PRIMARY_COLOR});
        padding: 30px 20px;
        text-align: center;
    }}
    
    .custom-title {{
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }}
    
    .custom-subtitle {{
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
    }}
    
    /* CONTENEDOR PRINCIPAL */
    .custom-container {{
        padding: 30px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    /* ESCRITORIO: MANTENER ST.COLUMNS NORMAL - NO TOCAR */
    /* Versión escritorio funciona perfecto */
    
    /* MÓVIL: SOLUCIÓN COMPLETA CON FLEXBOX */
    @media (max-width: 768px) {{
        /* Ocultar todo lo de escritorio */
        .stApp [data-testid="column"] {{
            width: 100% !important;
            flex: 1 1 100% !important;
        }}
        
        .desktop-version {{
            display: none !important;
        }}
        
        /* Mostrar nuestra versión móvil */
        .mobile-version {{
            display: block !important;
        }}
        
        .mobile-grid {{
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 10px !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        .mobile-card-wrapper {{
            width: calc(50% - 5px) !important;
            flex: 0 0 calc(50% - 5px) !important;
            margin-bottom: 10px !important;
            box-sizing: border-box !important;
        }}
        
        .mobile-card {{
            background: white;
            border-radius: 12px;
            padding: 15px 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            text-align: center;
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(0,0,0,0.05);
            height: 120px;
            width: 100% !important;
            transition: all 0.3s ease;
        }}
        
        .mobile-card:hover {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 6px 15px rgba(243, 112, 33, 0.15);
        }}
        
        .mobile-icon {{
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
        }}
        
        .mobile-card-title {{
            font-size: 0.8rem !important;
            font-weight: 600;
            color: {SECONDARY_COLOR};
            margin: 0;
            line-height: 1.2;
            text-align: center;
            padding: 0 5px;
        }}
        
        .custom-container {{
            padding: 20px 15px !important;
        }}
        
        .custom-title {{
            font-size: 1.8rem !important;
        }}
        
        .custom-subtitle {{
            font-size: 0.9rem !important;
        }}
        
        .custom-header {{
            padding: 10px 15px !important;
        }}
        
        /* Asegurar que las columnas de streamlit no interfieran */
        [data-testid="column"] {{
            min-width: 0 !important;
        }}
        
        /* Ajustes específicos para pantallas muy pequeñas */
        @media (max-width: 380px) {{
            .mobile-card-wrapper {{
                width: 100% !important;
                flex: 0 0 100% !important;
            }}
            
            .mobile-card {{
                height: 110px !important;
            }}
        }}
    }}
    
    /* ESCRITORIO: OCULTAR VERSIÓN MÓVIL */
    @media (min-width: 769px) {{
        .mobile-version {{
            display: none !important;
        }}
        
        .desktop-version {{
            display: block !important;
        }}
        
        /* Estilos para tarjetas en escritorio (igual que antes) */
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
            padding: 20px !important;
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
    footer {{ 
        display: none !important; 
    }}
    
    .stDeployButton {{ 
        display: none !important; 
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
    """Dashboard con versiones separadas para escritorio y móvil"""
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
    
    # **VERSIÓN ESCRITORIO ORIGINAL - FUNCIONA BIEN**
    st.markdown('<div class="desktop-version">', unsafe_allow_html=True)
    
    # Fila 1
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="desktop-card" onclick="openCalendarModal()">
            <div class="desktop-icon">📅</div>
            <h3 class="desktop-title">Horarios</h3>
            <p class="desktop-desc">Consulta y gestiona tus turnos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <a href="?view=asistencia" class="desktop-card">
            <div class="desktop-icon">✅</div>
            <h3 class="desktop-title">Control Asistencia</h3>
            <p class="desktop-desc">Registro entrada/salida</p>
        </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <a href="?view=nomina" class="desktop-card">
            <div class="desktop-icon">💰</div>
            <h3 class="desktop-title">Nómina y Pagos</h3>
            <p class="desktop-desc">Recibos y estados de pago</p>
        </a>
        """, unsafe_allow_html=True)
    
    # Fila 2
    col4, col5, col6 = st.columns(3, gap="large")
    
    with col4:
        st.markdown(f"""
        <a href="?view=incidencias" class="desktop-card">
            <div class="desktop-icon">⚠️</div>
            <h3 class="desktop-title">Incidencias</h3>
            <p class="desktop-desc">Reporta y consulta incidencias</p>
        </a>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <a href="?view=formacion" class="desktop-card">
            <div class="desktop-icon">🎓</div>
            <h3 class="desktop-title">Formación</h3>
            <p class="desktop-desc">Cursos y certificaciones</p>
        </a>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <a href="?view=comunicados" class="desktop-card">
            <div class="desktop-icon">📢</div>
            <h3 class="desktop-title">Comunicados</h3>
            <p class="desktop-desc">Noticias y anuncios</p>
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # **VERSIÓN MÓVIL NUEVA - USANDO FLEXBOX**
    st.markdown("""
    <div class="mobile-version" style="display: none;">
        <div class="mobile-grid">
            <!-- Fila 1 -->
            <div class="mobile-card-wrapper">
                <div class="mobile-card" onclick="openCalendarModal()">
                    <div class="mobile-icon">📅</div>
                    <h3 class="mobile-card-title">Horarios</h3>
                </div>
            </div>
            
            <div class="mobile-card-wrapper">
                <a href="?view=asistencia" class="mobile-card">
                    <div class="mobile-icon">✅</div>
                    <h3 class="mobile-card-title">Control Asistencia</h3>
                </a>
            </div>
            
            <!-- Fila 2 -->
            <div class="mobile-card-wrapper">
                <a href="?view=nomina" class="mobile-card">
                    <div class="mobile-icon">💰</div>
                    <h3 class="mobile-card-title">Nómina y Pagos</h3>
                </a>
            </div>
            
            <div class="mobile-card-wrapper">
                <a href="?view=incidencias" class="mobile-card">
                    <div class="mobile-icon">⚠️</div>
                    <h3 class="mobile-card-title">Incidencias</h3>
                </a>
            </div>
            
            <!-- Fila 3 -->
            <div class="mobile-card-wrapper">
                <a href="?view=formacion" class="mobile-card">
                    <div class="mobile-icon">🎓</div>
                    <h3 class="mobile-card-title">Formación</h3>
                </a>
            </div>
            
            <div class="mobile-card-wrapper">
                <a href="?view=comunicados" class="mobile-card">
                    <div class="mobile-icon">📢</div>
                    <h3 class="mobile-card-title">Comunicados</h3>
                </a>
            </div>
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
    
    // Detectar tamaño de pantalla y mostrar versión correcta
    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            // Móvil: ocultar escritorio, mostrar móvil
            document.querySelector('.desktop-version').style.display = 'none';
            document.querySelector('.mobile-version').style.display = 'block';
        } else {
            // Escritorio: ocultar móvil, mostrar escritorio
            document.querySelector('.mobile-version').style.display = 'none';
            document.querySelector('.desktop-version').style.display = 'block';
        }
    }
    
    // Ejecutar al cargar y al cambiar tamaño
    window.addEventListener('load', checkScreenSize);
    window.addEventListener('resize', checkScreenSize);
    
    // Cerrar modal
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
            const wrappers = document.querySelectorAll('.mobile-card-wrapper');
            wrappers.forEach(wrapper => {
                wrapper.style.flex = '0 0 calc(50% - 5px)';
                wrapper.style.width = 'calc(50% - 5px)';
            });
        }
    }
    
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
