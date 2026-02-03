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
# ESTILOS CSS OPTIMIZADOS - CORREGIDO
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
        backdrop-filter: blur(10px);
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
    
    .page-title-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(243, 112, 33, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 140, 66, 0.1) 0%, transparent 50%);
        opacity: 0.6;
    }}
    
    .page-title-section::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="wave" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M0,50 Q25,40 50,50 T100,50" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2"/></pattern></defs><rect width="100" height="100" fill="url(%23wave)"/></svg>');
        opacity: 0.3;
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
    
    /* GRID DE TARJETAS - CORREGIDO DEFINITIVAMENTE */
    .dashboard-container {{
        padding: 40px 25px;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        box-sizing: border-box;
        position: relative;
    }}
    
    /* DESKTOP: 3 columnas x 2 filas - CORREGIDO */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        width: 100%;
        justify-items: stretch;  /* Cambiado de center a stretch */
        align-items: stretch;
    }}
    
    /* TARJETAS PROFESIONALES - CORREGIDO */
    .dashboard-card {{
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        border: none;
        text-decoration: none !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        min-height: 220px;
        width: 100%;  /* Eliminado max-width */
        position: relative;
        overflow: hidden;
        box-sizing: border-box;  /* Añadido */
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
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(243, 112, 33, 0.25);
        border-color: {PRIMARY_COLOR};
    }}
    
    .dashboard-card:hover .card-icon {{
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 10px 25px rgba(243, 112, 33, 0.3);
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
    
    /* ESTADÍSTICAS PROFESIONALES */
    .stats-container {{
        background: white;
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 40px auto 0;
        max-width: 1200px;
        width: calc(100% - 50px);
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
    }}
    
    .stats-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        width: 100%;
    }}
    
    .stat-card {{
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border-left: 5px solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
    
    .stat-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }}
    
    .stat-value {{
        font-size: 2.5rem;
        font-weight: 800;
        margin: 15px 0;
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* MODAL DE CALENDARIO PROFESIONAL */
    .calendar-modal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.9);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        padding: 20px;
        animation: fadeIn 0.4s ease;
        backdrop-filter: blur(10px);
    }}
    
    .calendar-modal {{
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 25px;
        width: 95%;
        max-width: 1400px;
        height: 85vh;
        overflow: hidden;
        box-shadow: 0 30px 80px rgba(0,0,0,0.4);
        animation: slideUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        flex-direction: column;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    @keyframes slideUp {{
        from {{ transform: translateY(100px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    .modal-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 25px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 4px solid {PRIMARY_COLOR};
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }}
    
    .modal-title {{
        font-size: 2rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 15px;
        font-family: 'Montserrat', sans-serif;
    }}
    
    .modal-close {{
        background: {PRIMARY_COLOR};
        color: white;
        border: none;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(243, 112, 33, 0.3);
    }}
    
    .modal-close:hover {{
        background: #e55a1a;
        transform: rotate(90deg) scale(1.1);
        box-shadow: 0 8px 20px rgba(229, 90, 26, 0.4);
    }}
    
    .modal-body {{
        flex: 1;
        overflow: hidden;
        padding: 0;
        background: #f5f7fa;
    }}
    
    /* CALENDARIO PROFESIONAL - MALLA DE TURNOS */
    .professional-calendar {{
        height: 100%;
        display: flex;
        flex-direction: column;
        background: #f5f7fa;
    }}
    
    .calendar-controls {{
        background: white;
        padding: 25px 30px;
        border-bottom: 1px solid #e8ecef;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
    
    .calendar-main {{
        flex: 1;
        overflow: auto;
        padding: 30px;
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
    }}
    
    /* Grid de días - Malla profesional CORREGIDA */
    .calendar-days-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 2px;
        background: #d0d7e0;
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid #d0d7e0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }}
    
    .calendar-day-header {{
        background: linear-gradient(135deg, {SECONDARY_COLOR}, #1a2530);
        color: white;
        padding: 20px 10px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.5px;
    }}
    
    .calendar-day-cell {{
        background: white;
        min-height: 140px;
        padding: 15px;
        position: relative;
        transition: all 0.3s ease;
        border-right: 1px solid #f0f0f0;
        border-bottom: 1px solid #f0f0f0;
    }}
    
    .calendar-day-cell:hover {{
        background: #f8f9fa;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        z-index: 1;
    }}
    
    .day-number {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {SECONDARY_COLOR};
        margin-bottom: 12px;
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .today-cell {{
        background: linear-gradient(135deg, rgba(243, 112, 33, 0.15), rgba(243, 112, 33, 0.05)) !important;
        border: 2px solid {PRIMARY_COLOR} !important;
        border-radius: 8px;
    }}
    
    .today-cell .day-number {{
        color: {PRIMARY_COLOR};
        font-weight: 800;
    }}
    
    .weekend-cell {{
        background: #f9fafc;
    }}
    
    .shift-item {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff8c42);
        color: white;
        padding: 10px 12px;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-top: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid rgba(255,255,255,0.5);
        box-shadow: 0 3px 10px rgba(243, 112, 33, 0.2);
    }}
    
    .shift-item:hover {{
        background: linear-gradient(135deg, #e55a1a, #f37021);
        transform: translateX(3px);
        box-shadow: 0 5px 15px rgba(229, 90, 26, 0.3);
    }}
    
    .shift-time {{
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 3px;
    }}
    
    .shift-type {{
        font-size: 0.8rem;
        opacity: 0.9;
        font-weight: 500;
    }}
    
    .calendar-summary {{
        background: white;
        padding: 30px;
        border-top: 1px solid #e8ecef;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
    }}
    
    .summary-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
    }}
    
    .summary-card {{
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {PRIMARY_COLOR};
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }}
    
    .summary-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }}
    
    /* BOTONES PROFESIONALES */
    .action-buttons {{
        display: flex;
        gap: 15px;
        margin-top: 30px;
        justify-content: center;
        flex-wrap: wrap;
    }}
    
    .btn-primary {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff8c42);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Segoe UI', sans-serif;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        box-shadow: 0 5px 15px rgba(243, 112, 33, 0.3);
        letter-spacing: 0.5px;
    }}
    
    .btn-primary:hover {{
        background: linear-gradient(135deg, #e55a1a, #f37021);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(229, 90, 26, 0.4);
    }}
    
    .btn-secondary {{
        background: white;
        color: {PRIMARY_COLOR};
        border: 2px solid {PRIMARY_COLOR};
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
    
    .btn-secondary:hover {{
        background: #fff9f5;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(243, 112, 33, 0.2);
    }}
    
    /* RESPONSIVE PARA MÓVIL - 2 columnas x 3 filas - CORREGIDO */
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
        
        /* MÓVIL: 2 columnas x 3 filas - AHORA SÍ FUNCIONA */
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 20px;
        }}
        
        .dashboard-card {{
            min-height: 200px;
            padding: 22px;
            width: 100%;
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
        
        .stats-container {{
            padding: 25px;
            margin: 30px auto 0;
            width: calc(100% - 40px);
        }}
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}
        
        .stat-card {{
            padding: 20px;
        }}
        
        .stat-value {{
            font-size: 2rem;
        }}
        
        .calendar-modal {{
            width: 98%;
            height: 90vh;
        }}
        
        .modal-header {{
            padding: 20px;
        }}
        
        .modal-title {{
            font-size: 1.6rem;
        }}
        
        .calendar-controls {{
            flex-direction: column;
            align-items: stretch;
            gap: 15px;
            padding: 20px;
        }}
        
        .calendar-days-grid {{
            grid-template-columns: repeat(7, 1fr);
        }}
        
        .calendar-day-cell {{
            min-height: 120px;
            padding: 12px;
        }}
        
        .day-number {{
            font-size: 1rem;
        }}
        
        .shift-item {{
            padding: 8px 10px;
            font-size: 0.8rem;
        }}
        
        .action-buttons {{
            flex-direction: column;
            gap: 12px;
        }}
        
        .btn-primary, .btn-secondary {{
            width: 100%;
            padding: 14px 24px;
        }}
    }}
    
    @media (max-width: 576px) {{
        /* MÓVIL PEQUEÑO: 2 columnas x 3 filas - CORREGIDO */
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr) !important;
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
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .calendar-days-grid {{
            grid-template-columns: repeat(7, 1fr);
        }}
        
        .calendar-day-cell {{
            min-height: 100px;
            padding: 10px;
        }}
        
        .calendar-day-header {{
            padding: 15px 5px;
            font-size: 0.85rem;
        }}
        
        /* Para pantallas muy pequeñas, cambiar a 1 columna */
        @media (max-width: 400px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr !important;
            }}
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
    
    /* ANIMACIONES MEJORADAS */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    /* SCROLLBAR PERSONALIZADO */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff8c42);
        border-radius: 10px;
        border: 2px solid #f1f1f1;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #e55a1a, #f37021);
    }}
    </style>
    """, unsafe_allow_html=True)

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
        
        # Número del día con indicador de fin de semana
        weekday_indicator = "⚪" if current_day.weekday() < 5 else "🔵"
        calendar_html += f'''
        <div class="day-number">
            <span>{current_day.day}</span>
            <span style="font-size: 0.8rem; opacity: 0.7;">{weekday_indicator}</span>
        </div>
        '''
        
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
        else:
            # Mostrar estado de no turnos
            calendar_html += '''
            <div style="color: #999; font-size: 0.8rem; padding: 8px 0; text-align: center;">
                Sin turnos
            </div>
            '''
        
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
                        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                            <button onclick="changeMonth(-1)" class="btn-primary" style="padding: 12px 24px;">
                                ← Mes Anterior
                            </button>
                            <button onclick="changeMonth(1)" class="btn-primary" style="padding: 12px 24px;">
                                Siguiente Mes →
                            </button>
                        </div>
                        
                        <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 20px; height: 20px; background: linear-gradient(135deg, {PRIMARY_COLOR}, #ff8c42); border-radius: 4px;"></div>
                                <span style="font-size: 0.95rem; font-weight: 500;">Turno asignado</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 20px; height: 20px; background: rgba(243, 112, 33, 0.15); border: 2px solid {PRIMARY_COLOR}; border-radius: 4px;"></div>
                                <span style="font-size: 0.95rem; font-weight: 500;">Hoy</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 20px; height: 20px; background: #f9fafc; border: 1px solid #e0e0e0; border-radius: 4px;"></div>
                                <span style="font-size: 0.95rem; font-weight: 500;">Fin de semana</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="calendar-main">
                        {calendar_html}
                    </div>
                    
                    <div class="calendar-summary">
                        <div class="summary-grid">
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 8px; font-weight: 600;">📅 Turnos del Mes</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 2.2rem; font-weight: 800;">{total_turnos}</div>
                            </div>
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 8px; font-weight: 600;">⏰ Horas Totales</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 2.2rem; font-weight: 800;">{total_turnos * 6}h</div>
                            </div>
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 8px; font-weight: 600;">👥 Socorristas</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 2.2rem; font-weight: 800;">5</div>
                            </div>
                            <div class="summary-card">
                                <div style="color: {SECONDARY_COLOR}; font-size: 1.1rem; margin-bottom: 8px; font-weight: 600;">✅ Disponibilidad</div>
                                <div style="color: {PRIMARY_COLOR}; font-size: 2.2rem; font-weight: 800;">95%</div>
                            </div>
                        </div>
                        
                        <div class="action-buttons" style="margin-top: 25px;">
                            <button class="btn-secondary" onclick="window.print()" style="padding: 12px 24px;">
                                🖨️ Imprimir Calendario
                            </button>
                            <button class="btn-secondary" onclick="alert('Exportando a Excel...')" style="padding: 12px 24px;">
                                📊 Exportar Excel
                            </button>
                            <button class="btn-primary" onclick="closeCalendarModal()" style="padding: 12px 24px;">
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
        <div class="calendar-modal" style="max-width: 550px; height: auto;">
            <div class="modal-header">
                <div class="modal-title">
                    <span>📋</span> Detalles del Turno
                </div>
                <button class="modal-close" onclick="closeShiftModal()">×</button>
            </div>
            
            <div class="modal-body" style="padding: 25px;">
                <div style="background: linear-gradient(135deg, #f8f9fa, #ffffff); padding: 25px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                        <div>
                            <div style="color: #666; font-size: 0.95rem; margin-bottom: 8px; font-weight: 500;">📅 Fecha</div>
                            <div style="font-weight: 700; color: #333; font-size: 1.1rem;" id="shift-date"></div>
                        </div>
                        <div>
                            <div style="color: #666; font-size: 0.95rem; margin-bottom: 8px; font-weight: 500;">🕒 Horario</div>
                            <div style="font-weight: 700; color: #333; font-size: 1.1rem;" id="shift-time"></div>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                        <div>
                            <div style="color: #666; font-size: 0.95rem; margin-bottom: 8px; font-weight: 500;">🏷️ Tipo de Turno</div>
                            <div style="font-weight: 700; color: #333; font-size: 1.1rem;" id="shift-type"></div>
                        </div>
                        <div>
                            <div style="color: #666; font-size: 0.95rem; margin-bottom: 8px; font-weight: 500;">👤 Socorrista</div>
                            <div style="font-weight: 700; color: #333; font-size: 1.1rem;" id="shift-person"></div>
                        </div>
                    </div>
                    <div>
                        <div style="color: #666; font-size: 0.95rem; margin-bottom: 8px; font-weight: 500;">📍 Ubicación</div>
                        <div style="font-weight: 700; color: #333; font-size: 1.1rem;">Piscina Municipal Central</div>
                        <div style="color: #666; font-size: 0.9rem; margin-top: 5px; opacity: 0.8;">Av. Deportes, 123 - Zona Centro</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 12px;">
                    <button class="btn-primary" style="flex: 1; padding: 14px 24px;" onclick="alert('Solicitud enviada para cambio de turno')">
                        🔄 Solicitar Cambio
                    </button>
                    <button class="btn-secondary" style="flex: 1; padding: 14px 24px;" onclick="closeShiftModal()">
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
        if(direction === -1) {{
            alert('Navegando al mes anterior... (Para funcionalidad completa se requiere integración con Streamlit)');
        }} else {{
            alert('Navegando al mes siguiente... (Para funcionalidad completa se requiere integración con Streamlit)');
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
    
    # Título con fondo profesional
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
        <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 25px; font-family: 'Segoe UI', sans-serif; font-size: 1.5rem; font-weight: 700;">
            📊 Resumen Rápido
        </h3>
        <div class="stats-grid">
            <div class="stat-card" style="border-left-color: #4CAF50;">
                <div style="color: #4CAF50; font-size: 1.3rem;">✅</div>
                <div class="stat-value">12</div>
                <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Turnos Completados</div>
            </div>
            <div class="stat-card" style="border-left-color: #2196F3;">
                <div style="color: #2196F3; font-size: 1.3rem;">⏰</div>
                <div class="stat-value">96h</div>
                <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Horas Totales</div>
            </div>
            <div class="stat-card" style="border-left-color: #FF9800;">
                <div style="color: #FF9800; font-size: 1.3rem;">📅</div>
                <div class="stat-value">6</div>
                <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Próximos Turnos</div>
            </div>
            <div class="stat-card" style="border-left-color: #9C27B0;">
                <div style="color: #9C27B0; font-size: 1.3rem;">💰</div>
                <div class="stat-value">€2,850</div>
                <div style="color: #666; font-size: 0.95rem; font-weight: 500;">Salario Estimado</div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin: 40px auto 30px; padding: 0 25px; max-width: 1200px;">
        <p style="color: #666; font-size: 0.9rem; opacity: 0.8;">
            © {datetime.datetime.now().year} Socorrista Pro • Versión 2.2 • Todos los derechos reservados
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
        <div class="fade-in" style="max-width: 800px; margin: 0 auto; padding: 40px 25px;">
            <div style="text-align: center; margin-bottom: 40px;">
                <div style="font-size: 4rem; margin-bottom: 20px; color: {PRIMARY_COLOR};">{icon}</div>
                <h1 style="color: {SECONDARY_COLOR}; margin-bottom: 15px; font-family: 'Montserrat', sans-serif; font-size: 2.5rem; font-weight: 800;">
                    {title}
                </h1>
                <p style="color: #666; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
                    Esta funcionalidad está en desarrollo activo
                </p>
            </div>
            
            <div style="background: linear-gradient(145deg, #ffffff, #f8f9fa); border-radius: 20px; padding: 40px; box-shadow: 0 15px 40px rgba(0,0,0,0.08); margin-bottom: 35px; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 100px; height: 100px; background: linear-gradient(135deg, rgba(243, 112, 33, 0.1), transparent); border-radius: 0 20px 0 100px;"></div>
                
                <h3 style="color: {SECONDARY_COLOR}; margin-bottom: 25px; font-family: 'Segoe UI', sans-serif; font-size: 1.6rem; font-weight: 700;">
                    🚀 Próximamente
                </h3>
                <p style="color: #666; line-height: 1.7; margin-bottom: 25px; font-size: 1.05rem;">
                    Estamos trabajando arduamente para implementar esta funcionalidad con los más altos estándares de calidad. 
                    En las próximas semanas podrás acceder a todas las características avanzadas de <strong>{title.lower()}</strong>.
                </p>
                
                <div style="background: linear-gradient(135deg, #f8f9fa, #e8ecef); padding: 25px; border-radius: 15px; margin-top: 30px; border-left: 5px solid {PRIMARY_COLOR};">
                    <h4 style="color: {PRIMARY_COLOR}; margin-bottom: 20px; font-size: 1.3rem; font-weight: 700;">📅 Cronograma de Lanzamiento</h4>
                    <ul style="color: #666; line-height: 1.8; padding-left: 25px; font-size: 1rem;">
                        <li style="margin-bottom: 12px;"><strong>Fase 1:</strong> Diseño y planificación (Completado)</li>
                        <li style="margin-bottom: 12px;"><strong>Fase 2:</strong> Desarrollo del backend (En progreso)</li>
                        <li style="margin-bottom: 12px;"><strong>Fase 3:</strong> Pruebas y ajustes (Próximamente)</li>
                        <li style="margin-bottom: 12px;"><strong>Fase 4:</strong> Lanzamiento oficial (Febrero 2024)</li>
                    </ul>
                </div>
            </div>
            
            <div class="action-buttons">
                <a href="?" class="btn-primary" style="padding: 15px 35px;">
                    ← Volver al Dashboard
                </a>
                <button class="btn-secondary" style="padding: 15px 35px;" onclick="alert('Te notificaremos cuando esté disponible. ¡Gracias por tu paciencia!')">
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
