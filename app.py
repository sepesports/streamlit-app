# app.py
import streamlit as st
from datetime import date, datetime, time, timedelta
import calendar

st.set_page_config(page_title="Calendario + Agenda (Checklist)", layout="centered")

# =========================
# ESTILO
# =========================
CSS = """
<style>
.block-container{padding-top:14px !important; max-width:640px !important; padding-bottom:120px !important;}
header, footer{display:none !important;}

.topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 14px;
  border-radius:18px;
  background: linear-gradient(180deg, #3b6cff 0%, #2a52f5 100%);
  color:#fff;
  margin-bottom:10px;
}
.badge{
  font-size:12px; padding:4px 10px; border-radius:999px;
  background: rgba(255,255,255,.18);
  border:1px solid rgba(255,255,255,.22);
  font-weight:900;
}

.card{
  background:#fff;
  border:1px solid rgba(0,0,0,.08);
  border-radius:18px;
  padding:14px;
  box-shadow: 0 10px 28px rgba(0,0,0,.06);
}
.h2{font-weight:900; margin:14px 2px 10px 2px; color:#111;}
.hr{height:1px; background: rgba(0,0,0,.06); margin:12px 0;}
.small{font-size:12px; opacity:.78; font-weight:800;}

/* Calendario */
.cal-wrap{
  border-radius:18px;
  overflow:hidden;
  border:1px solid rgba(0,0,0,.08);
  background:#fff;
}
.cal-head{
  padding:12px 14px;
  background: linear-gradient(180deg, #3b6cff 0%, #2a52f5 100%);
  color:#fff;
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.cal-title{
  font-weight:950;
  letter-spacing:.2px;
}
.cal-nav{
  display:flex;
  gap:8px;
  align-items:center;
}
.cal-btn{
  padding:6px 10px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.22);
  background: rgba(255,255,255,.14);
  color:#fff;
  font-weight:950;
  cursor:pointer;
}
.cal-btn:hover{ background: rgba(255,255,255,.20); }

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
  font-weight:950;
  text-align:center;
}
.daymark{ position:relative; margin-top:-40px; height:40px; pointer-events:none; }
.pips{ position:absolute; left:50%; transform:translateX(-50%); bottom:6px; display:flex; gap:4px; }
.pip{ width:6px; height:6px; border-radius:50%; }
.pip-free{background: rgba(20,120,60,.55);}
.pip-busy{background: rgba(200,40,40,.60);}

/* Agenda tipo tabla por instalación */
.agenda-card{
  border:1px solid rgba(0,0,0,.10);
  border-radius:18px;
  overflow:hidden;
  background:#fff;
}
.agenda-head{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap:10px;
  padding:12px 14px;
  border-bottom:1px solid rgba(0,0,0,.06);
  background: rgba(0,0,0,.02);
  font-weight:950;
}
.agenda-rowhdr{
  display:grid;
  grid-template-columns: 110px 1fr 1fr 1fr;
  gap:10px;
  padding:10px 14px;
  border-bottom:1px solid rgba(0,0,0,.06);
  color: rgba(0,0,0,.70);
  font-weight:950;
  font-size:13px;
}
.agenda-row{
  display:grid;
  grid-template-columns: 110px 1fr 1fr 1fr;
  gap:10px;
  padding:10px 14px;
  border-bottom:1px solid rgba(0,0,0,.06);
  align-items:center;
}
.agenda-row:last-child{border-bottom:none;}
.cell-strong{font-weight:950;}
.pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:12px;
  padding:4px 10px;
  border-radius:999px;
  border:1px solid rgba(0,0,0,.10);
  background: rgba(0,0,0,.03);
  font-weight:950;
}
.pill-free{ border-color: rgba(20,120,60,.25); background: rgba(20,120,60,.08); }
.pill-busy{ border-color: rgba(200,40,40,.25); background: rgba(200,40,40,.08); }

/* Barra fija inferior */
.actionbar{
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 12px;
  width: min(640px, calc(100vw - 24px));
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
  opacity:.84;
  font-weight:950;
  overflow:hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

div.stButton>button{
  border-radius:14px !important;
  padding:10px 12px !important;
  font-weight:950 !important;
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

if "selected_inst" not in st.session_state:
    st.session_state.selected_inst = None  # nombre instalación seleccionada (checklist)

# =========================
# DATA DEMO
# =========================
# Slots habilitados por supervisor: fecha -> lista por instalación
# Formato: {"inst": str, "inicio": time, "finaliza": time}
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
        ],
    }

# Ocupado (ya programado)
if "busy_blocks" not in st.session_state:
    st.session_state.busy_blocks = {
        date(2026, 2, 15): [(time(10, 0), time(11, 0))],  # ejemplo
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

def day_status(d: date) -> str:
    # verde si hay al menos 1 instalación libre en ese día (agenda supervisor)
    items = st.session_state.supervisor_agenda.get(d, [])
    if not items:
        return "free"
    for it in items:
        if not is_busy(d, it["inicio"], it["finaliza"]):
            return "free"
    return "busy"

def build_month_weeks(y: int, m: int):
    cal = calendar.Calendar(firstweekday=0)  # 0 = Monday
    weeks = cal.monthdatescalendar(y, m)
    while len(weeks) < 6:
        last = weeks[-1]
        start = last[-1] + timedelta(days=1)
        weeks.append([start + timedelta(days=i) for i in range(7)])
    return weeks

def month_title_es(y: int, m: int) -> str:
    # sin locales del sistema: mapeo manual
    meses = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
    return f"{meses[m-1]} {y}"

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
# CALENDARIO CON NAV MES/AÑO
# =========================
weeks = build_month_weeks(st.session_state.view_year, st.session_state.view_month)
title = month_title_es(st.session_state.view_year, st.session_state.view_month)

st.markdown('<div class="cal-wrap">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="cal-head">
      <div class="cal-title">{title}</div>
      <div class="cal-nav">
        <span class="cal-btn" style="pointer-events:none;">Mes</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Navegación real (sin hacks): botones Streamlit
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
    # selector mes/año
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

        with cols[i]:
            label = str(d.day)
            clicked = st.button(label, key=f"day_{d.isoformat()}", use_container_width=True, disabled=(not in_month))
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
                st.session_state.selected_inst = None
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AGENDA DEL DÍA (formato como tu imagen)
# =========================
st.markdown('<div class="h2">Agenda del día</div>', unsafe_allow_html=True)

items = st.session_state.supervisor_agenda.get(st.session_state.selected_date, [])

if not items:
    st.markdown('<div class="card"><div class="small">No hay agenda para este día.</div></div>', unsafe_allow_html=True)
else:
    for idx, it in enumerate(items):
        inst = it["inst"]
        inicio = it["inicio"]
        finaliza = it["finaliza"]
        horas = calc_hours(inicio, finaliza)

        busy = is_busy(st.session_state.selected_date, inicio, finaliza)
        pill_txt = "OCUPADO" if busy else "LIBRE"
        pill_cls = "pill-busy" if busy else "pill-free"

        checked = st.checkbox("checkis", key=f"chk_{st.session_state.selected_date}_{idx}",
                              value=(st.session_state.selected_inst == inst),
                              disabled=busy)

        # si marca, deja solo ese seleccionado
        if checked and st.session_state.selected_inst != inst:
            st.session_state.selected_inst = inst
            # desmarca otros checkboxes
            for j, _ in enumerate(items):
                k = f"chk_{st.session_state.selected_date}_{j}"
                if k in st.session_state and j != idx:
                    st.session_state[k] = False
            st.rerun()

        # card tabla
        st.markdown('<div class="agenda-card">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="agenda-head">
              <div>Instalacion</div>
              <div style="display:flex; align-items:center; justify-content:space-between;">
                <span class="cell-strong">{inst}</span>
                <span class="pill {pill_cls}">{pill_txt}</span>
              </div>
            </div>
            <div class="agenda-rowhdr">
              <div>checkis</div><div>Inicio</div><div>Finaliza</div><div>Horas</div>
            </div>
            <div class="agenda-row">
              <div class="cell-strong">{'✓' if checked else ''}</div>
              <div>{fmt_time_hms(inicio)}</div>
              <div>{fmt_time_hms(finaliza)}</div>
              <div>{horas}</div>
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

# =========================
# BARRA FIJA INFERIOR (3 botones, se habilitan al seleccionar checklist)
# =========================
selected_ok = (st.session_state.selected_inst is not None)

# trae datos del seleccionado
sel = None
if selected_ok:
    for it in items:
        if it["inst"] == st.session_state.selected_inst:
            sel = it
            break
    if sel is None:
        selected_ok = False
        st.session_state.selected_inst = None

hint = "Selecciona una instalación (checkis)"
pill_txt = "—"
pill_cls = ""

selected_busy = False
if selected_ok and sel:
    selected_busy = is_busy(st.session_state.selected_date, sel["inicio"], sel["finaliza"])
    hint = f"{st.session_state.selected_date.isoformat()} · {st.session_state.selected_inst} · {fmt_time_hms(sel['inicio'])} → {fmt_time_hms(sel['finaliza'])}"
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
            "inst": st.session_state.selected_inst,
            "inicio": sel["inicio"],
            "finaliza": sel["finaliza"],
        })
        st.rerun()

with b2:
    if st.button("Modificar", use_container_width=True, disabled=(not selected_ok)):
        # demo: alterna a "Descanso"
        for it in items:
            if it["inst"] == st.session_state.selected_inst:
                it["inst"] = "Descanso"
                st.session_state.selected_inst = "Descanso"
                break
        st.session_state.supervisor_agenda[st.session_state.selected_date] = items
        st.rerun()

with b3:
    if st.button("Enviar", use_container_width=True, disabled=(not selected_ok)):
        st.session_state["_last_send"] = {
            "date": st.session_state.selected_date.isoformat(),
            "inst": st.session_state.selected_inst,
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
