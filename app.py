import base64
import requests
import streamlit as st

st.set_page_config(
    page_title="Panel Socorrista",
    page_icon="🛟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

IMG_URL = "https://files.catbox.moe/0mir4o.png"
ORANGE = "#F37021"

MENU_ITEMS = [
    ("servicio-tecnico", "Servicio Técnico", "🔧"),
    ("login", "Login", "👤"),
    ("control", "Control", "🔒"),
    ("horarios", "Horarios", "📄"),
    ("notificaciones", "Notificaciones", "🔔"),
    ("nomina", "Nómina", "🪪"),
]


@st.cache_data(show_spinner=False)
def fetch_image_as_data_uri(url: str) -> str:
    r = requests.get(url, timeout=25)
    r.raise_for_status()
    ct = r.headers.get("Content-Type", "image/png")
    b64 = base64.b64encode(r.content).decode("utf-8")
    return f"data:{ct};base64,{b64}"


try:
    BG = fetch_image_as_data_uri(IMG_URL)
except Exception:
    BG = IMG_URL  # fallback


def get_view() -> str | None:
    qp = st.query_params
    v = qp.get("view", None)
    if isinstance(v, list):
        return v[0] if v else None
    return v


# ---- CSS FULL BLEED (CLAVE: .block-container) ----
st.markdown(
    f"""
<style>
/* Quita TODO el padding/margen que centra el contenido (causa del borde blanco) */
html, body {{
  width: 100%;
  height: 100%;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}}

header, footer, [data-testid="stHeader"] {{
  display: none !important;
  height: 0 !important;
}}

.stApp {{
  width: 100vw !important;
  height: 100dvh !important;
  margin: 0 !important;
  padding: 0 !important;
}}

[data-testid="stAppViewContainer"] {{
  padding: 0 !important;
  margin: 0 !important;
}}

.block-container {{
  padding: 0 !important;          /* <-- ESTE ERA EL PROBLEMA MÁS COMÚN */
  margin: 0 !important;
  max-width: 100vw !important;
}}

#app-root {{
  width: 100vw;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

/* Imagen arriba ocupa el espacio disponible */
#hero {{
  flex: 1 1 auto;
  width: 100%;
  background-image: url("{BG}");
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
}}

/* Panel inferior fijo */
#panel {{
  flex: 0 0 auto;
  width: 100%;
  background: {ORANGE};
  padding: 18px 14px 22px 14px;
  box-sizing: border-box;
}}

#panel-inner {{
  width: 100%;
  max-width: 820px;
  margin: 0 auto;
}}

#grid {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px 14px;
  justify-items: center;
}}

.tile {{
  text-decoration: none !important;
  color: #fff !important;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}}

.diamond {{
  width: clamp(60px, 7.5vw, 90px);
  height: clamp(60px, 7.5vw, 90px);
  background: #fff;
  transform: rotate(45deg);
  border-radius: 12px;
  display: grid;
  place-items: center;
  box-shadow: 0 10px 26px rgba(0,0,0,.18);
}}

.icon {{
  transform: rotate(-45deg);
  font-size: clamp(22px, 2.4vw, 34px);
  line-height: 1;
  color: {ORANGE};
}}

.label {{
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  font-size: clamp(12.5px, 1.6vw, 16px);
  line-height: 1.1;
  text-align: center;
  color: #fff;
  white-space: nowrap;
}}

@media (max-width: 520px) {{
  #grid {{ gap: 14px 10px; }}
  .label {{ white-space: normal; }}
  #panel {{ padding: 16px 12px 20px 12px; }}
}}

/* Vista interna */
#view-wrap {{
  width: 100vw;
  height: 100dvh;
  display: grid;
  place-items: center;
  background: #f3f3f3;
  padding: 18px;
  box-sizing: border-box;
}}
#view-card {{
  width: 100%;
  max-width: 820px;
  background: #fff;
  border-radius: 18px;
  padding: 18px 16px;
  box-shadow: 0 10px 28px rgba(0,0,0,.12);
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}}
.back-btn {{
  display: inline-block;
  margin-top: 12px;
  background: {ORANGE};
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


view = get_view()

if view:
    label_map = {k: lbl for (k, lbl, _ic) in MENU_ITEMS}
    shown = label_map.get(view, view)

    st.markdown(
        f"""
<div id="view-wrap">
  <div id="view-card">
    <h2 style="margin:0 0 8px 0;">Vista: {shown}</h2>
    <div>Contenido placeholder.</div>
    <a class="back-btn" href="?">Volver al menú</a>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

else:
    tiles = []
    for key, label, ico in MENU_ITEMS:
        tiles.append(
            f"""
<a class="tile" href="?view={key}">
  <div class="diamond"><div class="icon">{ico}</div></div>
  <div class="label">{label}</div>
</a>
"""
        )

    st.markdown(
        f"""
<div id="app-root">
  <div id="hero"></div>
  <div id="panel">
    <div id="panel-inner">
      <div id="grid">
        {''.join(tiles)}
      </div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
