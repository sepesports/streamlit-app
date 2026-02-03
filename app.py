import base64
import requests
import streamlit as st

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(
    page_title="Panel Socorrista",
    page_icon="🛟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

IMG_URL = "https://files.catbox.moe/0mir4o.png"

MENU_ITEMS = [
    ("servicio-tecnico", "Servicio Técnico", "wrench"),
    ("login", "Login", "user"),
    ("control", "Control", "lock"),
    ("horarios", "Horarios", "file"),
    ("notificaciones", "Notificaciones", "bell"),
    ("nomina", "Nómina", "id"),
]

ORANGE = "#F37021"


# ----------------------------
# IMAGE (FAST) -> DATA URI
# ----------------------------
@st.cache_data(show_spinner=False)
def fetch_image_as_data_uri(url: str) -> str:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    content_type = r.headers.get("Content-Type", "image/png")
    b64 = base64.b64encode(r.content).decode("utf-8")
    return f"data:{content_type};base64,{b64}"


try:
    IMG_DATA_URI = fetch_image_as_data_uri(IMG_URL)
except Exception:
    IMG_DATA_URI = ""  # fallback: no background image


# ----------------------------
# HELPERS
# ----------------------------
def svg_icon(name: str) -> str:
    if name == "wrench":
        return """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M21 7.5a6 6 0 0 1-8.77 5.3L6.3 18.73a2 2 0 0 1-2.83 0l-.2-.2a2 2 0 0 1 0-2.83l5.93-5.93A6 6 0 0 1 16.5 3l-3 3 4.5 4.5 3-3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """
    if name == "user":
        return """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M20 21a8 8 0 0 0-16 0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M12 13a5 5 0 1 0-5-5 5 5 0 0 0 5 5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """
    if name == "lock":
        return """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M17 11H7a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          <path d="M8 11V8a4 4 0 0 1 8 0v3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """
    if name == "file":
        return """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          <path d="M14 2v6h6" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          <path d="M8 13h8M8 17h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """
    if name == "bell":
        return """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M18 8a6 6 0 1 0-12 0c0 7-3 7-3 7h18s-3 0-3-7Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """
    if name == "id":
        return """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M4 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          <path d="M8 11h4M8 15h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M16.5 12.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0Z" stroke="currentColor" stroke-width="2"/>
        </svg>
        """
    return "<svg viewBox='0 0 24 24' fill='none'></svg>"


def get_view() -> str | None:
    qp = st.query_params
    v = qp.get("view", None)
    if isinstance(v, list):
        return v[0] if v else None
    return v


# ----------------------------
# CSS (RESPONSIVE REAL)
# ----------------------------
bg = IMG_DATA_URI if IMG_DATA_URI else IMG_URL

st.markdown(
    f"""
<style>
  :root {{
    --orange: {ORANGE};
    --panelText: #ffffff;
    --diamondBg: #ffffff;
    --iconColor: var(--orange);
  }}

  /* Full-bleed */
  .stApp {{ background: transparent; }}
  section.main > div {{ padding: 0 !important; }}
  header, footer {{ visibility: hidden; height: 0px; }}

  /* Page uses dynamic viewport height to fit mobile browsers */
  .page {{
    height: 100dvh;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  /* Hero grows, panel fixed-ish by clamp */
  .hero {{
    flex: 1 1 auto;
    width: 100%;
    background-image: url('{bg}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }}

  .panel {{
    flex: 0 0 auto;
    width: 100%;
    background: var(--orange);
    padding: 16px 14px 20px 14px;
  }}

  /* Panel height responsive: mobile bigger, desktop controlled */
  .panel-inner {{
    width: 100%;
    margin: 0 auto;
    max-width: 720px;
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px 14px;
    align-items: start;
    justify-items: center;
  }}

  .tile {{
    text-decoration: none !important;
    color: var(--panelText) !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    user-select: none;
    width: 100%;
  }}

  .diamond {{
    width: clamp(58px, 7.2vw, 84px);
    height: clamp(58px, 7.2vw, 84px);
    background: var(--diamondBg);
    transform: rotate(45deg);
    border-radius: 12px;
    display: grid;
    place-items: center;
    box-shadow: 0 10px 26px rgba(0,0,0,.18);
  }}

  .diamond > .icon {{
    transform: rotate(-45deg);
    width: clamp(30px, 3.4vw, 40px);
    height: clamp(30px, 3.4vw, 40px);
    color: var(--iconColor);
    display: grid;
    place-items: center;
  }}
  .diamond svg {{
    width: 100%;
    height: 100%;
  }}

  .label {{
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    font-size: clamp(12.5px, 1.6vw, 16px);
    line-height: 1.1;
    text-align: center;
    color: var(--panelText);
    white-space: nowrap;
  }}

  .tile:hover .diamond {{
    filter: brightness(0.985);
    transform: rotate(45deg) scale(1.03);
  }}
  .tile:active .diamond {{
    transform: rotate(45deg) scale(0.99);
  }}

  /* Mobile fine-tune */
  @media (max-width: 520px) {{
    .grid {{
      gap: 14px 10px;
    }}
    .label {{
      white-space: normal;
    }}
  }}

  /* Views */
  .view-wrap {{
    height: 100dvh;
    min-height: 100dvh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 18px;
    background: #f3f3f3;
  }}
  .view-card {{
    width: 100%;
    max-width: 720px;
    border-radius: 18px;
    padding: 18px 16px;
    background: #ffffff;
    box-shadow: 0 10px 28px rgba(0,0,0,.12);
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  }}
  .view-title {{
    margin: 0 0 10px 0;
    font-size: 20px;
    font-weight: 800;
  }}
  .back-btn {{
    display: inline-block;
    margin-top: 10px;
    background: var(--orange);
    color: #fff !important;
    padding: 10px 14px;
    border-radius: 12px;
    text-decoration: none !important;
    font-weight: 700;
  }}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# ROUTING
# ----------------------------
view = get_view()

if view:
    label_map = {k: lbl for (k, lbl, _ic) in MENU_ITEMS}
    shown = label_map.get(view, view)

    st.markdown(
        f"""
<div class="view-wrap">
  <div class="view-card">
    <h1 class="view-title">Vista: {shown}</h1>
    <div>Contenido placeholder.</div>
    <a class="back-btn" href="?">Volver al menú</a>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    tiles_html = []
    for key, label, icon_name in MENU_ITEMS:
        tiles_html.append(
            f"""
<a class="tile" href="?view={key}">
  <div class="diamond">
    <div class="icon">{svg_icon(icon_name)}</div>
  </div>
  <div class="label">{label}</div>
</a>
"""
        )

    st.markdown(
        f"""
<div class="page">
  <div class="hero"></div>
  <div class="panel">
    <div class="panel-inner">
      <div class="grid">
        {''.join(tiles_html)}
      </div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
