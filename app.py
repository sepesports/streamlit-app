# app.py
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, time, timedelta

st.set_page_config(page_title="Agenda tipo iOS", layout="centered")

# =========================
# ESTILO (tipo iOS)
# =========================
CSS = """
<style>
/* Layout general */
.block-container{padding-top:14px !important; max-width:520px !important;}
header, footer{display:none !important;}
/* Tarjetas */
.card{
  background:#fff;
  border:1px solid rgba(0,0,0,.08);
  border-radius:16px;
  padding:14px;
  box-shadow: 0 10px 28px rgba(0,0,0,.06);
}
/* Header calendario */
.cal-header{
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 14px;
  border-radius:18px;
  background: linear-gradient(180deg, #3b6cff 0%, #2a52f5 100%);
  color:#fff;
  margin-bottom:10px;
}
.cal-title{font-weight:700; letter-spacing:.3px;}
.badge{
  font-size:12px; padding:4px 8px; border-radius:999px;
  background: rgba(255,255,255,.18);
  border:1px solid rgba(255,255,255,.22);
}
.section-title{
  font-weight:700; margin:10px 2px 8px 2px; color:#111;
}
.pill{
  display:inline-flex; align-items:center; gap:8px;
  background: rgba(0,0,0,.04);
  border:1px solid rgba(0,0,0,.06);
  padding:8px 10px;
  border-radius:999px;
  font-size:13px;
}
/* Slots */
.slot{
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 12px; border-radius:14px;
  border:1px solid rgba(0,0,0,.08);
  background:#fff;
  margin-bottom:8px;
}
.slot-left{display:flex; flex-direction:column; gap:2px;}
.slot-time{font-weight:700;}
.slot-meta{font-size:12px; opacity:.7;}
.tag{
  font-size:12px; padding:5px 10px; border-radius:999px;
  border:1px solid rgba(0,0,0,.10);
  background: rgba(0,0,0,.03);
}
.tag-free{border-color: rgba(20,120,60,.25); background: rgba(20,120,60,.08);}
.tag-busy{border-color: rgba(200,40,40,.25); background: rgba(200,40,40,.08);}
.hr{height:1px; background: rgba(0,0,0,.06); margin:12px 0;}
.small{font-size:12px; opacity:.75;}
/* Botones Streamlit */
div.stButton>button{
  border-radius:14px !important;
  padding:10px 12px !important;
  font-weight:700 !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# ESTADO / DATA MOCK (agenda existente)
# =========================
# Simula "yo estoy programado" (bloques ocupados)
# En producción esto vendría de Google Calendar / DB / API.
if "busy_blocks" not in st.session_state:
    st.session_state.busy_blocks = {
        # fecha: lista de rangos ocupados (inicio, fin)
        # (horas 24h)
        date(2025, 4, 1): [(time(12, 0), time(13, 0)), (time(15, 30), time(16, 30))],
        date(2025, 4, 2): [(time(9, 0), time(10, 0))],
    }

if "bookings" not in st.session_state:
    st.session_state.bookings = []  # reservas hechas desde la app (demo)

# =========================
# HELPERS
# =========================
def overlaps(a_start: time, a_end: time, b_start: time, b_end: time) -> bool:
    # convierte a minutos para comparar
    a0 = a_start.hour * 60 + a_start.minute
    a1 = a_end.hour * 60 + a_end.minute
    b0 = b_start.hour * 60 + b_start.minute
    b1 = b_end.hour * 60 + b_end.minute
    return max(a0, b0) < min(a1, b1)

def is_busy(d: date, s: time, e: time) -> bool:
    for bs, be in st.session_state.busy_blocks.get(d, []):
        if overlaps(s, e, bs, be):
            return True
    for item in st.session_state.bookings:
        if item["date"] == d and overlaps(s, e, item["start"], item["end"]):
            return True
    return False

def fmt_time(t: time) -> str:
    # formato 12h tipo iOS: 12:00 p.m.
    h = t.hour
    m = t.minute
    suffix = "a.m." if h < 12 else "p.m."
    hh = h % 12
    if hh == 0:
        hh = 12
    return f"{hh}:{m:02d} {suffix}"

def add_minutes(t: time, minutes: int) -> time:
    dt = datetime.combine(date.today(), t) + timedelta(minutes=minutes)
    return dt.time()

def generate_slots(day_start=time(8, 0), day_end=time(18, 0), slot_minutes=30):
    slots = []
    cur = day_start
    while True:
        nxt = add_minutes(cur, slot_minutes)
        if (nxt.hour * 60 + nxt.minute) > (day_end.hour * 60 + day_end.minute):
            break
        slots.append((cur, nxt))
        cur = nxt
    return slots

# =========================
# UI
# =========================
st.markdown(
    f"""
    <div class="cal-header">
      <div class="cal-title">Calendario</div>
      <div class="badge">Disponibilidad</div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        selected_date = st.date_input("Día", value=date.today(), label_visibility="collapsed")
    with col2:
        timezone = st.selectbox("Zona horaria", ["America/Bogota", "America/Mexico_City", "America/Los_Angeles"], index=0, label_visibility="collapsed")

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    cA, cB = st.columns([1, 1])
    with cA:
        duration_min = st.selectbox("Duración", [15, 30, 45, 60, 90, 120], index=1)
    with cB:
        slot_step = st.selectbox("Paso (slots)", [15, 30, 60], index=1)

    st.markdown('<div class="small">Selecciona un día y revisa franjas: libre u ocupado.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Franjas del día</div>', unsafe_allow_html=True)

slots = generate_slots(day_start=time(8, 0), day_end=time(18, 0), slot_minutes=slot_step)

# =========================
# LISTADO DE SLOTS (ver si hay franja desocupada / programado)
# =========================
for s, e in slots:
    # la "aplicación" usa duración seleccionada, no necesariamente slot_step
    e2 = add_minutes(s, duration_min)
    # no mostrar si se pasa del final del día
    if (e2.hour * 60 + e2.minute) > (18 * 60):
        continue

    busy = is_busy(selected_date, s, e2)

    tag_class = "tag-busy" if busy else "tag-free"
    tag_text = "OCUPADO" if busy else "LIBRE"

    st.markdown(
        f"""
        <div class="slot">
          <div class="slot-left">
            <div class="slot-time">{fmt_time(s)} → {fmt_time(e2)}</div>
            <div class="slot-meta">{timezone} · {duration_min} min</div>
          </div>
          <div class="tag {tag_class}">{tag_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Acción: "Aplicar" solo si está libre
    cols = st.columns([1, 1, 2])
    with cols[0]:
        if not busy:
            if st.button("Aplicar", key=f"apply_{selected_date}_{s}_{duration_min}", use_container_width=True):
                st.session_state.bookings.append(
                    {"date": selected_date, "start": s, "end": e2, "tz": timezone}
                )
                st.rerun()
        else:
            st.button("Aplicar", key=f"apply_disabled_{selected_date}_{s}_{duration_min}", disabled=True, use_container_width=True)
    with cols[1]:
        if st.button("Ver detalle", key=f"detail_{selected_date}_{s}_{duration_min}", use_container_width=True):
            # modal overlay simple (solo UI) para simular "ventana emergente"
            html = f"""
            <div id="ovroot">
              <style>
                #ovroot{{position:fixed; inset:0; z-index:999999; font-family:system-ui;}}
                .bk{{position:absolute; inset:0; background:rgba(0,0,0,.55); backdrop-filter:blur(4px);}}
                .md{{position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
                     width:min(460px, calc(100vw - 28px));
                     border-radius:18px; background:#fff; border:1px solid rgba(0,0,0,.10);
                     box-shadow:0 20px 70px rgba(0,0,0,.35); overflow:hidden;}}
                .hd{{padding:14px 14px 10px 14px; background:linear-gradient(180deg,#f5f7ff,#ffffff);
                     display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid rgba(0,0,0,.06);}}
                .tt{{font-weight:800;}}
                .x{{width:34px; height:34px; border-radius:12px; border:1px solid rgba(0,0,0,.10);
                    background:rgba(0,0,0,.03); cursor:pointer; font-size:18px;}}
                .bd{{padding:14px;}}
                .row{{display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid rgba(0,0,0,.06);}}
                .k{{opacity:.75;}}
                .v{{font-weight:800;}}
                .ft{{padding:14px; display:flex; gap:10px; justify-content:flex-end;}}
                .btn{{padding:10px 12px; border-radius:14px; border:1px solid rgba(0,0,0,.12); background:rgba(0,0,0,.03); cursor:pointer; font-weight:800;}}
              </style>
              <div class="bk" id="bk"></div>
              <div class="md" role="dialog" aria-modal="true">
                <div class="hd">
                  <div class="tt">Detalle de franja</div>
                  <button class="x" id="x">×</button>
                </div>
                <div class="bd">
                  <div class="row"><div class="k">Día</div><div class="v">{selected_date.isoformat()}</div></div>
                  <div class="row"><div class="k">Hora</div><div class="v">{fmt_time(s)} → {fmt_time(e2)}</div></div>
                  <div class="row"><div class="k">Estado</div><div class="v">{"OCUPADO" if busy else "LIBRE"}</div></div>
                  <div class="row" style="border-bottom:none;"><div class="k">Zona horaria</div><div class="v">{timezone}</div></div>
                </div>
                <div class="ft">
                  <button class="btn" id="c">Cerrar</button>
                </div>
              </div>
              <script>
                (function(){{
                  const r = document.getElementById("ovroot");
                  const bk = document.getElementById("bk");
                  const x = document.getElementById("x");
                  const c = document.getElementById("c");
                  function close(){{ if(r) r.remove(); }}
                  bk.addEventListener("click", close);
                  x.addEventListener("click", close);
                  c.addEventListener("click", close);
                  document.addEventListener("keydown", (e)=>{{ if(e.key==="Escape") close(); }});
                }})();
              </script>
            </div>
            """
            components.html(html, height=0, width=0)

    with cols[2]:
        st.markdown("", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Reservas hechas (demo)</div>', unsafe_allow_html=True)

if not st.session_state.bookings:
    st.markdown('<div class="pill">Sin reservas todavía</div>', unsafe_allow_html=True)
else:
    for i, b in enumerate(st.session_state.bookings):
        st.markdown(
            f"""
            <div class="card" style="margin-bottom:10px;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-weight:800;">{b["date"].isoformat()}</div>
                <div class="tag tag-free">RESERVADO</div>
              </div>
              <div class="small">{fmt_time(b["start"])} → {fmt_time(b["end"])} · {b["tz"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Eliminar", key=f"del_{i}", use_container_width=True):
            st.session_state.bookings.pop(i)
            st.rerun()
