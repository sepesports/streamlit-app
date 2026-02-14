# app.py
import streamlit as st
from datetime import date, datetime, time, timedelta

st.set_page_config(page_title="Agenda tipo Calendario", layout="centered")

# =========================
# ESTILO (iOS-like)
# =========================
CSS = """
<style>
.block-container{padding-top:14px !important; max-width:560px !important;}
header, footer{display:none !important;}
/* Cards */
.card{
  background:#fff;
  border:1px solid rgba(0,0,0,.08);
  border-radius:18px;
  padding:14px;
  box-shadow: 0 10px 28px rgba(0,0,0,.06);
}
.topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 14px;
  border-radius:18px;
  background: linear-gradient(180deg, #3b6cff 0%, #2a52f5 100%);
  color:#fff;
  margin-bottom:10px;
}
.badge{
  font-size:12px; padding:4px 8px; border-radius:999px;
  background: rgba(255,255,255,.18);
  border:1px solid rgba(255,255,255,.22);
}
.h2{font-weight:800; margin:12px 2px 8px 2px; color:#111;}
.hr{height:1px; background: rgba(0,0,0,.06); margin:12px 0;}
.small{font-size:12px; opacity:.75;}
/* Calendar */
.cal-wrap{
  border-radius:18px;
  overflow:hidden;
  border:1px solid rgba(0,0,0,.08);
}
.cal-head{
  padding:12px 14px;
  background: linear-gradient(180deg, #3b6cff 0%, #2a52f5 100%);
  color:#fff;
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.cal-month{font-weight:900; letter-spacing:.2px;}
.cal-legend{
  display:flex; gap:8px; align-items:center; font-size:12px;
  background: rgba(255,255,255,.16);
  border: 1px solid rgba(255,255,255,.20);
  padding:6px 10px;
  border-radius:999px;
}
.dot{width:10px; height:10px; border-radius:50%;}
.dot-free{background: rgba(20,120,60,.65);}
.dot-busy{background: rgba(200,40,40,.70);}
.dot-part{background: rgba(255,170,0,.80);}
.cal-grid{
  padding:12px 12px 14px 12px;
  background:#fff;
}
.cal-dow{
  display:grid;
  grid-template-columns: repeat(7, 1fr);
  gap:8px;
  margin-bottom:8px;
  color: rgba(0,0,0,.55);
  font-size:12px;
  font-weight:800;
  text-align:center;
}
.cal-days{
  display:grid;
  grid-template-columns: repeat(7, 1fr);
  gap:8px;
}
.daybtn{
  border-radius:14px !important;
  height:42px !important;
  padding:0 !important;
  font-weight:900 !important;
  border:1px solid rgba(0,0,0,.08) !important;
  background:#fff !important;
  color:#111 !important;
}
.daybtn:hover{border-color: rgba(59,108,255,.55) !important;}
.daybtn.selected{
  background: rgba(59,108,255,.14) !important;
  border-color: rgba(59,108,255,.70) !important;
}
.daybtn.muted{
  opacity:.35 !important;
}
.daymark{
  position:relative;
}
.pips{
  position:absolute;
  left:50%;
  transform:translateX(-50%);
  bottom:6px;
  display:flex;
  gap:4px;
}
.pip{width:6px; height:6px; border-radius:50%;}
.pip-free{background: rgba(20,120,60,.55);}
.pip-busy{background: rgba(200,40,40,.60);}
.pip-part{background: rgba(255,170,0,.70);}
/* Timeline blocks */
.timeline{
  border:1px solid rgba(0,0,0,.08);
  border-radius:18px;
  overflow:hidden;
  background:#fff;
}
.trow{
  display:grid;
  grid-template-columns: 78px 1fr;
  gap:10px;
  padding:10px 12px;
  border-bottom:1px solid rgba(0,0,0,.06);
  align-items:center;
}
.trow:last-child{border-bottom:none;}
.tlabel{
  font-weight:900;
  color: rgba(0,0,0,.65);
  font-size:12px;
}
.tblock{
  border-radius:14px;
  border:1px solid rgba(0,0,0,.08);
  padding:10px 12px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  cursor:pointer;
  user-select:none;
}
.free{
  background: rgba(20,120,60,.08);
  border-color: rgba(20,120,60,.22);
}
.busy{
  background: rgba(200,40,40,.08);
  border-color: rgba(200,40,40,.22);
}
.part{
  background: rgba(255,170,0,.10);
  border-color: rgba(255,170,0,.24);
}
.sel{
  outline: 3px solid rgba(59,108,255,.22);
  border-color: rgba(59,108,255,.70) !important;
  background: rgba(59,108,255,.12) !important;
}
.tmeta{font-size:12px; opacity:.75; font-weight:800;}
/* Bottom action bar */
.actionbar{
  position: sticky;
  bottom: 10px;
  margin-top: 12px;
  z-index: 10;
}
.actioninner{
  background:#fff;
  border:1px solid rgba(0,0,0,.08);
  border-radius:18px;
  padding:12px;
  box-shadow: 0 16px 40px rgba(0,0,0,.12);
}
div.stButton>button{
  border-radius:14px !important;
  padding:10px 12px !important;
  font-weight:900 !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# DATA DEMO (ocupado / libre)
# =========================
# Estructura: fecha -> lista de bloques (inicio, fin)
# NOTA: esto se reemplaza por Google Calendar / DB / API.
if "busy_blocks" not in st.session_state:
    st.session_state.busy_blocks = {
        date(2025, 4, 1): [(time(12, 0), time(13, 0)), (time(15, 0), time(16, 30))],
        date(2025, 4, 2): [(time(9, 0), time(10, 30)), (time(14, 0), time(15, 0))],
        date(2025, 4, 14): [(time(10, 0), time(12, 0))],
    }

if "bookings" not in st.session_state:
    st.session_state.bookings = []  # reservas creadas desde la app

if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

if "selected_start" not in st.session_state:
    st.session_state.selected_start = None  # time
if "selected_end" not in st.session_state:
    st.session_state.selected_end = None  # time

# =========================
# HELPERS
# =========================
def to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute

def overlaps(a0: time, a1: time, b0: time, b1: time) -> bool:
    return max(to_minutes(a0), to_minutes(b0)) < min(to_minutes(a1), to_minutes(b1))

def is_busy_block(d: date, start: time, end: time) -> bool:
    for bs, be in st.session_state.busy_blocks.get(d, []):
        if overlaps(start, end, bs, be):
            return True
    for item in st.session_state.bookings:
        if item["date"] == d and overlaps(start, end, item["start"], item["end"]):
            return True
    return False

def add_minutes(t: time, mins: int) -> time:
    dt = datetime.combine(date.today(), t) + timedelta(minutes=mins)
    return dt.time()

def fmt_time(t: time) -> str:
    h = t.hour
    m = t.minute
    suffix = "a.m." if h < 12 else "p.m."
    hh = h % 12
    if hh == 0:
        hh = 12
    return f"{hh}:{m:02d} {suffix}"

def month_matrix(any_day: date):
    # returns (year, month, matrix weeks where each week is list[date or None])
    y, m = any_day.year, any_day.month
    first = date(y, m, 1)
    # monday=0 ... sunday=6  | queremos iniciar en Lunes
    offset = first.weekday()
    # start at monday of the first week
    start = first - timedelta(days=offset)
    weeks = []
    cur = start
    for _ in range(6):  # max 6 semanas
        week = []
        for _ in range(7):
            week.append(cur)
            cur += timedelta(days=1)
        weeks.append(week)
    return y, m, weeks

def day_status(d: date):
    # status for dots: busy/part/free based on any busy blocks or any booking
    has_busy = bool(st.session_state.busy_blocks.get(d, []))
    has_book = any(b["date"] == d for b in st.session_state.bookings)
    if has_busy and has_book:
        return "part"
    if has_busy or has_book:
        return "busy"
    return "free"

def slot_class(d: date, s: time, e: time):
    busy = is_busy_block(d, s, e)
    if busy:
        return "busy", "OCUPADO"
    return "free", "LIBRE"

def normalize_selection():
    if st.session_state.selected_start and st.session_state.selected_end:
        if to_minutes(st.session_state.selected_end) <= to_minutes(st.session_state.selected_start):
            st.session_state.selected_end = add_minutes(st.session_state.selected_start, 60)

# =========================
# TOP BAR
# =========================
st.markdown(
    """
    <div class="topbar">
      <div style="font-weight:900;">Calendario</div>
      <div class="badge">Disponibilidad</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# CONTROLES (Zona horaria + Duración)
# =========================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        tz = st.selectbox("Zona horaria", ["America/Bogota", "America/Mexico_City", "America/Los_Angeles"], index=0)
    with c2:
        duration_min = st.selectbox("Duración", [30, 45, 60, 90, 120], index=2)

    st.markdown('<div class="small">Selecciona un día del calendario y luego un bloque de hora (tipo agenda por colores).</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CALENDARIO (grid mensual)
# =========================
y, m, weeks = month_matrix(st.session_state.selected_date)
month_name = datetime(y, m, 1).strftime("%B %Y").upper()

st.markdown('<div class="cal-wrap">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="cal-head">
      <div class="cal-month">{month_name}</div>
      <div class="cal-legend">
        <span class="dot dot-free"></span> Libre
        <span class="dot dot-busy" style="margin-left:8px;"></span> Ocupado
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="cal-grid">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="cal-dow">
      <div>L</div><div>M</div><div>X</div><div>J</div><div>V</div><div>S</div><div>D</div>
    </div>
    """,
    unsafe_allow_html=True
)

# grid 6 semanas x 7
for w in weeks:
    cols = st.columns(7, gap="small")
    for i, d in enumerate(w):
        in_month = (d.month == m)
        status = day_status(d)
        is_sel = (d == st.session_state.selected_date)

        # marcadores
        pip_class = "pip-free" if status == "free" else ("pip-busy" if status == "busy" else "pip-part")

        label = str(d.day)
        key = f"day_{d.isoformat()}"
        with cols[i]:
            btn_label = label if in_month else f"{label}"
            clicked = st.button(btn_label, key=key, use_container_width=True)
            # aplica clases via markdown + css? (streamlit buttons no permiten class)
            # workaround: si seleccionado, mostramos un indicador debajo (sin hacks raros)
            st.markdown(
                f"""
                <div class="daymark" style="margin-top:-40px; height:40px; pointer-events:none;">
                  <div class="pips">
                    <span class="pip {pip_class}"></span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if clicked:
                st.session_state.selected_date = d
                st.session_state.selected_start = None
                st.session_state.selected_end = None
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # cal-grid
st.markdown('</div>', unsafe_allow_html=True)  # cal-wrap

# =========================
# AGENDA POR COLORES (bloques por hora, no lista infinita)
# =========================
st.markdown('<div class="h2">Agenda del día</div>', unsafe_allow_html=True)

day_start = time(8, 0)
day_end = time(18, 0)

# Genera bloques "compactos": 1 hora visual (y la duración real se aplica al seleccionar)
blocks = []
cur = day_start
while to_minutes(cur) < to_minutes(day_end):
    nxt = add_minutes(cur, 60)
    blocks.append((cur, nxt))
    cur = nxt

# Si hay selección previa, ajusta end según duración
if st.session_state.selected_start is not None:
    st.session_state.selected_end = add_minutes(st.session_state.selected_start, duration_min)
    normalize_selection()

selected_ok = (st.session_state.selected_start is not None and st.session_state.selected_end is not None)
selected_busy = False
if selected_ok:
    selected_busy = is_busy_block(st.session_state.selected_date, st.session_state.selected_start, st.session_state.selected_end)

st.markdown('<div class="timeline">', unsafe_allow_html=True)

for s, e in blocks:
    # estado del bloque visual: ocupado si choca con algo (en esa hora)
    cls, tag = slot_class(st.session_state.selected_date, s, e)

    # si este bloque es el seleccionado (por start)
    is_sel = (st.session_state.selected_start == s)
    extra_sel = " sel" if is_sel else ""

    # Render fila
    st.markdown(
        f"""
        <div class="trow">
          <div class="tlabel">{fmt_time(s)}</div>
          <div class="tblock {cls}{extra_sel}">
            <div class="tmeta">{tag}</div>
            <div class="tmeta">+{duration_min} min</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Click real (botón invisible por fila) para seleccionar start
    # (sin inventar JS; control 100% Streamlit)
    if st.button("Seleccionar", key=f"sel_{st.session_state.selected_date}_{s}", use_container_width=True):
        st.session_state.selected_start = s
        st.session_state.selected_end = add_minutes(s, duration_min)
        normalize_selection()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BARRA DE ACCIONES (3 botones) - se activan al seleccionar rango
# =========================
st.markdown('<div class="actionbar"><div class="actioninner">', unsafe_allow_html=True)

# Estado texto
if not selected_ok:
    st.markdown('<div class="small">Selecciona un bloque de hora para habilitar acciones.</div>', unsafe_allow_html=True)
else:
    estado = "OCUPADO" if selected_busy else "LIBRE"
    st.markdown(
        f'<div class="small"><b>{st.session_state.selected_date.isoformat()}</b> · {fmt_time(st.session_state.selected_start)} → {fmt_time(st.session_state.selected_end)} · {tz} · <b>{estado}</b></div>',
        unsafe_allow_html=True
    )

b1, b2, b3 = st.columns(3, gap="small")

with b1:
    # Aplicar: solo si hay selección y está libre
    if st.button("Aplicar", use_container_width=True, disabled=(not selected_ok or selected_busy)):
        st.session_state.bookings.append(
            {"date": st.session_state.selected_date, "start": st.session_state.selected_start, "end": st.session_state.selected_end, "tz": tz}
        )
        # bloquea ocupación “demo”
        st.rerun()

with b2:
    # Modificar: si hay selección (libre u ocupado), aquí solo demo: cambia duración a 60
    if st.button("Modificar", use_container_width=True, disabled=(not selected_ok)):
        # demo: alterna duración entre 60 y la seleccionada
        new_dur = 60 if duration_min != 60 else 90
        # fuerza cambio visual: setea duration seleccionada via session_state auxiliar
        st.session_state["_force_duration"] = new_dur
        # aplica
        st.session_state.selected_end = add_minutes(st.session_state.selected_start, new_dur)
        st.rerun()

with b3:
    # Enviar: demo (solo log visual)
    if st.button("Enviar", use_container_width=True, disabled=(not selected_ok)):
        st.session_state["_last_send"] = {
            "date": st.session_state.selected_date.isoformat(),
            "start": fmt_time(st.session_state.selected_start),
            "end": fmt_time(st.session_state.selected_end),
            "tz": tz,
            "status": "OCUPADO" if selected_busy else "LIBRE",
        }
        st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# =========================
# LOG / DEMO OUTPUT (mínimo)
# =========================
if "_force_duration" in st.session_state:
    st.markdown(f'<div class="small">Duración aplicada por "Modificar": {st.session_state["_force_duration"]} min (demo)</div>', unsafe_allow_html=True)
    del st.session_state["_force_duration"]

if "_last_send" in st.session_state:
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-weight:900;">Enviar (demo)</div>', unsafe_allow_html=True)
    st.code(st.session_state["_last_send"], language="json")
    st.markdown('</div>', unsafe_allow_html=True)
