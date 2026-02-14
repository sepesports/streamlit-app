# app.py
import streamlit as st
from datetime import date, datetime, time, timedelta
import calendar

st.set_page_config(page_title="Calendario + Agenda (Checklist)", layout="centered")

# =========================
# ESTILO (SOLO VISUAL / MISMA ESTRUCTURA Y MEDIDAS)
# =========================
CSS = """
<style>
/* ======= BASE / STREAMLIT ======= */
:root{
  --bg0:#06132c;
  --bg1:#081a3a;
  --bg2:#0c2248;

  --txt:#eaf2ff;
  --txt2:rgba(234,242,255,.85);
  --muted:rgba(234,242,255,.72);

  --line:rgba(255,255,255,.12);
  --line2:rgba(255,255,255,.10);

  --shadow0:0 18px 40px rgba(0,0,0,.55);
  --shadow1:0 12px 26px rgba(0,0,0,.45);
  --shadow2:0 10px 18px rgba(0,0,0,.38);

  --accent:#ff7c2c;
  --accentGlow:0 0 18px rgba(255,124,44,.35);

  --ok:rgba(40,200,120,.95);
  --okBg:rgba(40,200,120,.12);
  --okLine:rgba(40,200,120,.28);

  --bad:rgba(255,80,80,.95);
  --badBg:rgba(255,80,80,.12);
  --badLine:rgba(255,80,80,.28);
}

html, body, .stApp{
  background:
    radial-gradient(1200px 700px at 50% 12%, rgba(60,140,255,.35) 0%, rgba(60,140,255,.12) 35%, rgba(6,19,44,0) 72%),
    radial-gradient(900px 520px at 20% 55%, rgba(255,124,44,.12) 0%, rgba(255,124,44,0) 65%),
    linear-gradient(180deg, var(--bg2) 0%, var(--bg1) 55%, var(--bg0) 100%) !important;
  color: var(--txt);
}

.block-container{
  padding-top:14px !important;
  max-width:640px !important;
  padding-bottom:120px !important;
}
header, footer{display:none !important;}

/* ======= TOPBAR (MISMA CLASE / MISMA CAJA) ======= */
.topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 14px;
  border-radius:18px;
  border:1px solid var(--line);
  background:
    radial-gradient(900px 240px at 35% 25%, rgba(120,210,255,.18) 0%, rgba(120,210,255,0) 70%),
    linear-gradient(180deg, rgba(30,70,150,.86) 0%, rgba(10,30,80,.92) 70%, rgba(6,19,44,.94) 100%);
  color:var(--txt);
  margin-bottom:10px;
  box-shadow: var(--shadow2);
}
.badge{
  font-size:12px; padding:4px 10px; border-radius:999px;
  background: rgba(255,255,255,.10);
  border:1px solid rgba(255,255,255,.18);
  font-weight:900;
  color: var(--txt);
}

/* ======= CARD (MISMA CLASE / MISMA MEDIDA) ======= */
.card{
  background:
    linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 55%, rgba(255,255,255,.04) 100%);
  border:1px solid var(--line);
  border-radius:18px;
  padding:14px;
  box-shadow: var(--shadow1);
  color: var(--txt);
  backdrop-filter: blur(10px);
}
.h2{font-weight:900; margin:14px 2px 10px 2px; color:var(--txt); text-shadow: 0 2px 12px rgba(0,0,0,.35);}
.hr{height:1px; background: rgba(255,255,255,.10); margin:12px 0;}
.small{font-size:12px; opacity:.86; font-weight:800; color: var(--txt2);}

/* ======= CALENDARIO (MISMA ESTRUCTURA) ======= */
.cal-wrap{
  border-radius:18px;
  overflow:hidden;
  border:1px solid var(--line);
  background:
    linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  box-shadow: var(--shadow1);
  backdrop-filter: blur(10px);
}
.cal-head{
  padding:12px 14px;
  background:
    radial-gradient(900px 240px at 35% 25%, rgba(120,210,255,.18) 0%, rgba(120,210,255,0) 70%),
    linear-gradient(180deg, rgba(30,70,150,.86) 0%, rgba(10,30,80,.92) 70%, rgba(6,19,44,.94) 100%);
  color:var(--txt);
  display:flex;
  align-items:center;
  justify-content:space-between;
  border-bottom:1px solid rgba(255,255,255,.10);
}
.cal-title{font-weight:950; letter-spacing:.2px;}
.cal-grid{
  padding:12px 12px 14px 12px;
  background: transparent;
}
.cal-dow{
  display:grid;
  grid-template-columns: repeat(7, 1fr);
  gap:8px;
  margin-bottom:8px;
  color: rgba(234,242,255,.75);
  font-size:12px;
  font-weight:950;
  text-align:center;
}

.daymark{ position:relative; margin-top:-40px; height:40px; pointer-events:none; }
.pips{ position:absolute; left:50%; transform:translateX(-50%); bottom:6px; display:flex; gap:4px; }
.pip{ width:6px; height:6px; border-radius:50%; }
.pip-free{background: rgba(40,200,120,.60);}
.pip-busy{background: rgba(255,80,80,.65);}

/* ======= AGENDA (MISMA ESTRUCTURA) ======= */
.agenda-card{
  border:1px solid var(--line);
  border-radius:18px;
  overflow:hidden;
  background:
    linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 55%, rgba(255,255,255,.04) 100%);
  box-shadow: var(--shadow1);
  backdrop-filter: blur(10px);
}
.agenda-head{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap:10px;
  padding:12px 14px;
  border-bottom:1px solid rgba(255,255,255,.10);
  background:
    linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 100%);
  font-weight:950;
  color: var(--txt);
}
.agenda-rowhdr{
  display:grid;
  grid-template-columns: 110px 1.2fr 1fr 1fr 1fr;
  gap:10px;
  padding:10px 14px;
  border-bottom:1px solid rgba(255,255,255,.10);
  color: rgba(234,242,255,.80);
  font-weight:950;
  font-size:13px;
}
.agenda-row{
  display:grid;
  grid-template-columns: 110px 1.2fr 1fr 1fr 1fr;
  gap:10px;
  padding:10px 14px;
  border-bottom:1px solid rgba(255,255,255,.08);
  align-items:center;
  color: var(--txt);
}
.agenda-row:last-child{border-bottom:none;}
.cell-strong{font-weight:950; color: var(--txt);}

.pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:12px;
  padding:4px 10px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.06);
  font-weight:950;
  color: var(--txt);
}
.pill-free{ border-color: var(--okLine); background: var(--okBg); color: rgba(210,255,235,.95); }
.pill-busy{ border-color: var(--badLine); background: var(--badBg); color: rgba(255,220,220,.95); }

/* ======= BARRA FIJA INFERIOR (MISMA ESTRUCTURA) ======= */
.actionbar{
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 12px;
  width: min(640px, calc(100vw - 24px));
  z-index: 9999;
}
.actioninner{
  background:
    radial-gradient(900px 240px at 30% 10%, rgba(120,210,255,.12) 0%, rgba(120,210,255,0) 70%),
    linear-gradient(180deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,.05) 55%, rgba(255,255,255,.04) 100%);
  border:1px solid var(--line);
  border-radius:18px;
  padding:10px 10px 12px 10px;
  box-shadow: var(--shadow0);
  backdrop-filter: blur(10px);
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
  opacity:.92;
  font-weight:950;
  overflow:hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--txt2);
}

/* ======= BOTONES STREAMLIT (MISMO TAMAÑO, SOLO COLOR) ======= */
div.stButton>button{
  border-radius:14px !important;
  padding:10px 12px !important;
  font-weight:950 !important;

  border:1px solid rgba(255,255,255,.14) !important;
  background:
    radial-gradient(220px 80px at 24% 50%, rgba(120,210,255,.18) 0%, rgba(120,210,255,0) 68%),
    linear-gradient(180deg, rgba(18,78,185,.30) 0%, rgba(8,42,110,.42) 55%, rgba(4,24,66,.62) 100%) !important;
  color: var(--txt) !important;
  box-shadow: var(--shadow2) !important;
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, filter .12s ease;
}
div.stButton>button:hover{
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(0,0,0,.52) !important;
  border-color: rgba(255,124,44,.35) !important;
  filter: saturate(1.06);
}
div.stButton>button:active{
  transform: translateY(0px);
}

/* Botón "primario" cuando Streamlit lo renderiza como kind="primary" (si aplica) */
button[kind="primary"]{
  background: linear-gradient(180deg, rgba(255,124,44,.95) 0%, rgba(255,106,0,.92) 100%) !important;
  border-color: rgba(255,124,44,.55) !important;
  color:#fff !important;
  box-shadow: var(--accentGlow), var(--shadow2) !important;
}
button[kind="primary"]:hover{
  border-color: rgba(255,124,44,.75) !important;
  box-shadow: 0 0 22px rgba(255,124,44,.42), 0 16px 34px rgba(0,0,0,.52) !important;
}

/* Selectbox / Inputs (solo visual) */
div[data-baseweb="select"] > div{
  background: rgba(255,255,255,.06) !important;
  border: 1px solid rgba(255,255,255,.14) !important;
  box-shadow: var(--shadow2) !important;
}
div[data-baseweb="select"] *{
  color: var(--txt) !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "view_year" not in st.session_state:
    today = date.today()
    st.session_state.view_year = today.year
    st.session_state.view_month = today.month

if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

if "selected_key" not in st.session_state:
    st.session_state.selected_key = None  # identifica la franja seleccionada (idx)

if "filter_only_scheduled" not in st.session_state:
    st.session_state.filter_only_scheduled = False

# =========================
# DATA DEMO
# =========================
# Un día puede tener múltiples franjas por diferentes instalaciones
# Formato: fecha -> lista de franjas {inst, inicio, finaliza}
if "supervisor_agenda" not in st.session_state:
    st.session_state.supervisor_agenda = {
        date(2026, 2, 15): [
            {"inst": "Rocafort", "inicio": time(9, 0), "finaliza": time(15, 0)},
            {"inst": "Cn Fabra", "inicio": time(9, 0), "finaliza": time(15, 0)},
            {"inst": "Arsenal", "inicio": time(8, 0), "finaliza": time(12, 0)},
        ],
        date(2026, 2, 16): [
            {"inst": "Cem", "inicio": time(10, 0), "finaliza": time(14, 0)},
            {"inst": "Guissona", "inicio": time(9, 0), "finaliza": time(13, 0)},
            {"inst": "St. Jordi", "inicio": time(15, 0), "finaliza": time(18, 0)},
        ],
    }

# Ocupado (ya programado)
if "busy_blocks" not in st.session_state:
    st.session_state.busy_blocks = {
        date(2026, 2, 15): [(time(10, 0), time(11, 0))],
    }

# Reservas creadas desde la app
if "bookings" not in st.session_state:
    st.session_state.bookings = []  # {"date", "inst", "inicio", "finaliza"}

# =========================
# HELPERS
# =========================
def to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute

def overlaps(a0: time, a1: time, b0: time, b1: time) -> bool:
    return max(to_minutes(a0), to_minutes(b0)) < min(to_minutes(a1), to_minutes(b1))

def is_busy(d: date, inicio: time, finaliza: time) -> bool:
    for bs, be in st.session_state.busy_blocks.get(d, []):
        if overlaps(inicio, finaliza, bs, be):
            return True
    for b in st.session_state.bookings:
        if b["date"] == d and overlaps(inicio, finaliza, b["inicio"], b["finaliza"]):
            return True
    return False

def fmt_time_hms(t: time) -> str:
    return f"{t.hour:02d}:{t.minute:02d}:00"

def calc_hours(inicio: time, finaliza: time) -> str:
    mins = to_minutes(finaliza) - to_minutes(inicio)
    if mins < 0:
        mins = 0
    h = mins // 60
    m = mins % 60
    return f"{h}:{m:02d}:00"

def day_has_agenda(d: date) -> bool:
    return bool(st.session_state.supervisor_agenda.get(d, []))

def day_status(d: date) -> str:
    items = st.session_state.supervisor_agenda.get(d, [])
    if not items:
        return "free"
    for it in items:
        if not is_busy(d, it["inicio"], it["finaliza"]):
            return "free"
    return "busy"

def build_month_weeks(y: int, m: int):
    cal = calendar.Calendar(firstweekday=0)  # Monday
    weeks = cal.monthdatescalendar(y, m)
    while len(weeks) < 6:
        last = weeks[-1]
        start = last[-1] + timedelta(days=1)
        weeks.append([start + timedelta(days=i) for i in range(7)])
    return weeks

def month_title_es(y: int, m: int) -> str:
    meses = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
    return f"{meses[m-1]} {y}"

def scheduled_days_sorted():
    days = [d for d, items in st.session_state.supervisor_agenda.items() if items]
    days.sort()
    return days

def next_scheduled_day(from_day: date):
    days = scheduled_days_sorted()
    for d in days:
        if d >= from_day:
            return d
    return days[0] if days else None

def date_title_es(d: date) -> str:
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    return f"{d.day:02d} {meses[d.month-1]} {d.year}"

# =========================
# TOP BAR
# =========================
st.markdown(
    """
    <div class="topbar">
      <div style="font-weight:950;">Calendario</div>
      <div class="badge">Agenda</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# BARRA DE FILTRO / SALTO
# =========================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Filtrar: solo días con agenda", use_container_width=True):
            st.session_state.filter_only_scheduled = not st.session_state.filter_only_scheduled
            if st.session_state.filter_only_scheduled and not day_has_agenda(st.session_state.selected_date):
                nd = next_scheduled_day(st.session_state.selected_date)
                if nd:
                    st.session_state.selected_date = nd
                    st.session_state.view_year = nd.year
                    st.session_state.view_month = nd.month
                    st.session_state.selected_key = None
            st.rerun()
    with c2:
        if st.button("Ir al próximo programado", use_container_width=True):
            nd = next_scheduled_day(st.session_state.selected_date)
            if nd:
                st.session_state.selected_date = nd
                st.session_state.view_year = nd.year
                st.session_state.view_month = nd.month
                st.session_state.selected_key = None
            st.rerun()

    estado_filtro = "ACTIVO" if st.session_state.filter_only_scheduled else "INACTIVO"
    st.markdown(f'<div class="small">Filtro días con agenda: <b>{estado_filtro}</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CALENDARIO CON NAV MES/AÑO
# =========================
weeks = build_month_weeks(st.session_state.view_year, st.session_state.view_month)
title = month_title_es(st.session_state.view_year, st.session_state.view_month)

st.markdown('<div class="cal-wrap">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="cal-head">
      <div class="cal-title">{title}</div>
      <div class="badge">Mes / Año</div>
    </div>
    """,
    unsafe_allow_html=True
)

nav1, nav2, nav3 = st.columns([1, 2, 1])
with nav1:
    if st.button("◀", use_container_width=True):
        y = st.session_state.view_year
        m = st.session_state.view_month - 1
        if m == 0:
            m = 12
            y -= 1
        st.session_state.view_year = y
        st.session_state.view_month = m
        st.rerun()
with nav2:
    months = list(range(1, 13))
    years = list(range(st.session_state.view_year - 3, st.session_state.view_year + 4))
    c1, c2 = st.columns(2)
    with c1:
        msel = st.selectbox("Mes", months, index=st.session_state.view_month - 1, label_visibility="collapsed")
    with c2:
        ysel = st.selectbox("Año", years, index=years.index(st.session_state.view_year), label_visibility="collapsed")
    if (msel != st.session_state.view_month) or (ysel != st.session_state.view_year):
        st.session_state.view_month = msel
        st.session_state.view_year = ysel
        st.rerun()
with nav3:
    if st.button("▶", use_container_width=True):
        y = st.session_state.view_year
        m = st.session_state.view_month + 1
        if m == 13:
            m = 1
            y += 1
        st.session_state.view_year = y
        st.session_state.view_month = m
        st.rerun()

st.markdown('<div class="cal-grid">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="cal-dow">
      <div>L</div><div>M</div><div>X</div><div>J</div><div>V</div><div>S</div><div>D</div>
    </div>
    """,
    unsafe_allow_html=True
)

for w in weeks[:6]:
    cols = st.columns(7, gap="small")
    for i, d in enumerate(w):
        in_month = (d.month == st.session_state.view_month)
        status = day_status(d)
        pip = "pip-free" if status == "free" else "pip-busy"

        disable_by_filter = st.session_state.filter_only_scheduled and (not day_has_agenda(d))
        disabled = (not in_month) or disable_by_filter

        with cols[i]:
            clicked = st.button(str(d.day), key=f"day_{d.isoformat()}", use_container_width=True, disabled=disabled)
            st.markdown(
                f"""
                <div class="daymark">
                  <div class="pips">
                    <span class="pip {pip}"></span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if clicked:
                st.session_state.selected_date = d
                st.session_state.selected_key = None
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AGENDA DEL DÍA (HEADER = FECHA)
# =========================
st.markdown('<div class="h2">Agenda del día</div>', unsafe_allow_html=True)

items = st.session_state.supervisor_agenda.get(st.session_state.selected_date, [])

st.markdown(
    f"""
    <div class="agenda-card" style="margin-bottom:10px;">
      <div class="agenda-head" style="grid-template-columns: 1fr;">
        <div>Fecha: <span class="cell-strong">{date_title_es(st.session_state.selected_date)}</span></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

if not items:
    st.markdown(
        f'<div class="card"><div class="small">No hay franjas para este día.</div></div>',
        unsafe_allow_html=True
    )
else:
    st.markdown('<div class="agenda-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="agenda-rowhdr">
          <div>checkis</div><div>Instalacion</div><div>Inicio</div><div>Finaliza</div><div>Horas</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    for idx, it in enumerate(items):
        inst = it["inst"]
        inicio = it["inicio"]
        finaliza = it["finaliza"]
        horas = calc_hours(inicio, finaliza)

        busy = is_busy(st.session_state.selected_date, inicio, finaliza)
        pill_txt = "OCUPADO" if busy else "LIBRE"
        pill_cls = "pill-busy" if busy else "pill-free"

        checked = st.checkbox(
            "",
            key=f"chk_{st.session_state.selected_date}_{idx}",
            value=(st.session_state.selected_key == idx),
            disabled=busy
        )

        if checked and st.session_state.selected_key != idx:
            st.session_state.selected_key = idx
            for j in range(len(items)):
                k = f"chk_{st.session_state.selected_date}_{j}"
                if k in st.session_state and j != idx:
                    st.session_state[k] = False
            st.rerun()

        st.markdown(
            f"""
            <div class="agenda-row">
              <div class="cell-strong">{'✓' if checked else ''}</div>
              <div class="cell-strong">{inst}</div>
              <div>{fmt_time_hms(inicio)}</div>
              <div>{fmt_time_hms(finaliza)}</div>
              <div style="display:flex; gap:8px; align-items:center; justify-content:space-between;">
                <span>{horas}</span>
                <span class="pill {pill_cls}">{pill_txt}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BARRA FIJA INFERIOR (3 botones)
# =========================
selected_ok = (st.session_state.selected_key is not None and bool(items))
sel = None
selected_busy = False

if selected_ok:
    sel = items[st.session_state.selected_key]
    selected_busy = is_busy(st.session_state.selected_date, sel["inicio"], sel["finaliza"])

hint = "Selecciona una franja (checkis)"
pill_txt = "—"
pill_cls = ""

if selected_ok and sel:
    hint = f"{st.session_state.selected_date.isoformat()} · {sel['inst']} · {fmt_time_hms(sel['inicio'])} → {fmt_time_hms(sel['finaliza'])}"
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
        st.session_state.bookings.append({
            "date": st.session_state.selected_date,
            "inst": sel["inst"],
            "inicio": sel["inicio"],
            "finaliza": sel["finaliza"],
        })
        st.rerun()

with b2:
    if st.button("Modificar", use_container_width=True, disabled=(not selected_ok)):
        items[st.session_state.selected_key]["inst"] = "Descanso"
        st.session_state.supervisor_agenda[st.session_state.selected_date] = items
        sel = items[st.session_state.selected_key]
        st.rerun()

with b3:
    if st.button("Enviar", use_container_width=True, disabled=(not selected_ok)):
        st.session_state["_last_send"] = {
            "date": st.session_state.selected_date.isoformat(),
            "inst": sel["inst"],
            "inicio": fmt_time_hms(sel["inicio"]),
            "finaliza": fmt_time_hms(sel["finaliza"]),
            "status": "OCUPADO" if selected_busy else "LIBRE",
        }
        st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

if "_last_send" in st.session_state:
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight:950;">Enviar (demo)</div>', unsafe_allow_html=True)
    st.code(st.session_state["_last_send"], language="json")
    st.markdown('</div>', unsafe_allow_html=True)
