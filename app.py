# app.py
import streamlit as st
from datetime import date, datetime, time, timedelta

st.set_page_config(page_title="Agenda tipo Calendario", layout="centered")

# =========================
# ESTILO (iOS-like) + BARRA FIJA FINAL
# =========================
CSS = """
<style>
.block-container{padding-top:14px !important; max-width:560px !important; padding-bottom:120px !important;}
header, footer{display:none !important;}

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
.daymark{ position:relative; margin-top:-40px; height:40px; pointer-events:none; }
.pips{ position:absolute; left:50%; transform:translateX(-50%); bottom:6px; display:flex; gap:4px; }
.pip{ width:6px; height:6px; border-radius:50%; }
.pip-free{background: rgba(20,120,60,.55);}
.pip-busy{background: rgba(200,40,40,.60);}
.pip-part{background: rgba(255,170,0,.70);}

/* Agenda: filas compactas por "Instalación" */
.agenda{
  border:1px solid rgba(0,0,0,.08);
  border-radius:18px;
  overflow:hidden;
  background:#fff;
}
.arow{
  display:grid;
  grid-template-columns: 92px 1fr;
  gap:10px;
  padding:10px 12px;
  border-bottom:1px solid rgba(0,0,0,.06);
  align-items:center;
}
.arow:last-child{border-bottom:none;}
.alabel{
  font-weight:900;
  color: rgba(0,0,0,.65);
  font-size:12px;
}
.acard{
  border-radius:14px;
  border:1px solid rgba(0,0,0,.08);
  padding:10px 12px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  user-select:none;
}
.free{ background: rgba(20,120,60,.08); border-color: rgba(20,120,60,.22); }
.busy{ background: rgba(200,40,40,.08); border-color: rgba(200,40,40,.22); }
.part{ background: rgba(255,170,0,.10); border-color: rgba(255,170,0,.24); }
.sel{
  outline: 3px solid rgba(59,108,255,.22);
  border-color: rgba(59,108,255,.70) !important;
  background: rgba(59,108,255,.12) !important;
}
.tmeta{font-size:12px; opacity:.78; font-weight:800;}
/* Barra fija inferior */
.actionbar{
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 12px;
  width: min(560px, calc(100vw - 24px));
  z-index: 9999;
}
.actioninner{
  background:#fff;
  border:1px solid rgba(0,0,0,.08);
  border-radius:18px;
  padding:10px 10px 12px 10px;
  box-shadow: 0 16px 40px rgba(0,0,0,.14);
}
.actionline{
  display:flex;
  gap:8px;
  align-items:center;
  justify-content:space-between;
  margin-bottom:8px;
}
.actionhint{
  font-size:12px;
  opacity:.80;
  font-weight:800;
  overflow:hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.pill{
  font-size:12px;
  padding:4px 10px;
  border-radius:999px;
  border:1px solid rgba(0,0,0,.10);
  background: rgba(0,0,0,.03);
  font-weight:900;
}
.pill-free{ border-color: rgba(20,120,60,.25); background: rgba(20,120,60,.08); }
.pill-busy{ border-color: rgba(200,40,40,.25); background: rgba(200,40,40,.08); }
div.stButton>button{
  border-radius:14px !important;
  padding:10px 12px !important;
  font-weight:900 !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# DATA DEMO
# =========================
# 1) Bloques ocupados (lo que ya está programado)
if "busy_blocks" not in st.session_state:
    st.session_state.busy_blocks = {
        date(2026, 2, 15): [(time(10, 0), time(11, 0))],
    }

# 2) Slots habilitados por supervisor para el día (Agenda del día SOLO muestra esto)
# Formato: fecha -> lista de opciones
# Cada opción: {"start": time, "end": time, "inst": str, "estado": "libre"|"ocupado"} (estado puede ser derivado)
if "supervisor_slots" not in st.session_state:
    st.session_state.supervisor_slots = {
        date(2026, 2, 15): [
            {"start": time(8, 0),  "end": time(9, 0),  "inst": "Rocafort"},
            {"start": time(12, 0), "end": time(13, 0), "inst": "Cn Fabra"},
            {"start": time(15, 0), "end": time(16, 0), "inst": "St. Jordi"},
        ],
        date(2026, 2, 14): [
            {"start": time(9, 0),  "end": time(10, 0), "inst": "Cem"},
            {"start": time(11, 0), "end": time(12, 0), "inst": "Arsenal"},
            {"start": time(14, 0), "end": time(15, 0), "inst": "Guissona"},
        ],
    }

if "bookings" not in st.session_state:
    st.session_state.bookings = []

if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

if "selected_slot_idx" not in st.session_state:
    st.session_state.selected_slot_idx = None  # índice dentro de supervisor_slots[selected_date]

# =========================
# HELPERS
# =========================
def to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute

def overlaps(a0: time, a1: time, b0: time, b1: time) -> bool:
    return max(to_minutes(a0), to_minutes(b0)) < min(to_minutes(a1), to_minutes(b1))

def is_busy(d: date, s: time, e: time) -> bool:
    for bs, be in st.session_state.busy_blocks.get(d, []):
        if overlaps(s, e, bs, be):
            return True
    for item in st.session_state.bookings:
        if item["date"] == d and overlaps(s, e, item["start"], item["end"]):
            return True
    return False

def fmt_time(t: time) -> str:
    h = t.hour
    m = t.minute
    suffix = "a.m." if h < 12 else "p.m."
    hh = h % 12
    if hh == 0:
        hh = 12
    return f"{hh}:{m:02d} {suffix}"

def month_matrix(any_day: date):
    y, m = any_day.year, any_day.month
    first = date(y, m, 1)
    offset = first.weekday()  # monday=0
    start = first - timedelta(days=offset)
    weeks = []
    cur = start
    for _ in range(6):
        week = []
        for _ in range(7):
            week.append(cur)
            cur += timedelta(days=1)
        weeks.append(week)
    return y, m, weeks

def day_status(d: date):
    # "busy" si hay bloques ocupados o reservas o si supervisor habilitó slots pero todos están ocupados
    slots = st.session_state.supervisor_slots.get(d, [])
    if slots:
        # si existe al menos 1 libre => free, si todos ocupados => busy
        any_free = False
        for s in slots:
            if not is_busy(d, s["start"], s["end"]):
                any_free = True
                break
        return "free" if any_free else "busy"

    has_busy = bool(st.session_state.busy_blocks.get(d, []))
    has_book = any(b["date"] == d for b in st.session_state.bookings)
    if has_busy or has_book:
        return "busy"
    return "free"

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
    st.markdown('<div class="small">Selecciona un día. En “Agenda del día” solo verás franjas habilitadas por supervisor (por instalación).</div>', unsafe_allow_html=True)
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

for w in weeks:
    cols = st.columns(7, gap="small")
    for i, d in enumerate(w):
        status = day_status(d)
        pip_class = "pip-free" if status == "free" else "pip-busy"

        with cols[i]:
            clicked = st.button(str(d.day), key=f"day_{d.isoformat()}", use_container_width=True)
            st.markdown(
                f"""
                <div class="daymark">
                  <div class="pips">
                    <span class="pip {pip_class}"></span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if clicked:
                st.session_state.selected_date = d
                st.session_state.selected_slot_idx = None
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AGENDA DEL DÍA (SOLO slots habilitados por supervisor)
# =========================
st.markdown('<div class="h2">Agenda del día</div>', unsafe_allow_html=True)

slots = st.session_state.supervisor_slots.get(st.session_state.selected_date, [])

if not slots:
    st.markdown('<div class="card"><div class="small">No hay franjas habilitadas para este día.</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="agenda">', unsafe_allow_html=True)

    for idx, s in enumerate(slots):
        start = s["start"]
        end = s["end"]
        inst = s["inst"]

        busy = is_busy(st.session_state.selected_date, start, end)
        cls = "busy" if busy else "free"
        tag = "OCUPADO" if busy else "LIBRE"

        is_sel = (st.session_state.selected_slot_idx == idx)
        extra_sel = " sel" if is_sel else ""

        st.markdown(
            f"""
            <div class="arow">
              <div class="alabel">{fmt_time(start)}</div>
              <div class="acard {cls}{extra_sel}">
                <div class="tmeta">{inst}</div>
                <div class="tmeta">{tag}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Seleccionar", key=f"slot_{st.session_state.selected_date}_{idx}", use_container_width=True):
            st.session_state.selected_slot_idx = idx
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BARRA FIJA INFERIOR (3 botones)
# =========================
selected_ok = (st.session_state.selected_slot_idx is not None and slots)
selected_busy = False
sel_start = sel_end = sel_inst = None

if selected_ok:
    sel = slots[st.session_state.selected_slot_idx]
    sel_start = sel["start"]
    sel_end = sel["end"]
    sel_inst = sel["inst"]
    selected_busy = is_busy(st.session_state.selected_date, sel_start, sel_end)

hint = "Selecciona un bloque"
pill_txt = "—"
pill_cls = ""

if selected_ok:
    hint = f"{st.session_state.selected_date.isoformat()} · {fmt_time(sel_start)} → {fmt_time(sel_end)} · {sel_inst}"
    if selected_busy:
        pill_txt = "OCUPADO"
        pill_cls = "pill-busy"
    else:
        pill_txt = "LIBRE"
        pill_cls = "pill-free"

st.markdown('<div class="actionbar"><div class="actioninner">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="actionline">
      <div class="actionhint">{hint}</div>
      <div class="pill {pill_cls}">{pill_txt}</div>
    </div>
    """,
    unsafe_allow_html=True
)

b1, b2, b3 = st.columns(3, gap="small")

with b1:
    if st.button("Aplicar", use_container_width=True, disabled=(not selected_ok or selected_busy)):
        # crea reserva (demo)
        st.session_state.bookings.append(
            {"date": st.session_state.selected_date, "start": sel_start, "end": sel_end, "inst": sel_inst, "tz": tz}
        )
        st.rerun()

with b2:
    if st.button("Modificar", use_container_width=True, disabled=(not selected_ok)):
        # demo: cambia instalación a "Descanso" (solo para mostrar)
        slots[st.session_state.selected_slot_idx]["inst"] = "Descanso"
        st.session_state.supervisor_slots[st.session_state.selected_date] = slots
        st.rerun()

with b3:
    if st.button("Enviar", use_container_width=True, disabled=(not selected_ok)):
        st.session_state["_last_send"] = {
            "date": st.session_state.selected_date.isoformat(),
            "start": fmt_time(sel_start),
            "end": fmt_time(sel_end),
            "inst": sel_inst,
            "tz": tz,
            "status": "OCUPADO" if selected_busy else "LIBRE",
        }
        st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

if "_last_send" in st.session_state:
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight:900;">Enviar (demo)</div>', unsafe_allow_html=True)
    st.code(st.session_state["_last_send"], language="json")
    st.markdown('</div>', unsafe_allow_html=True)
