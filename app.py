# app.py
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="Popups / Modals Demo", layout="wide")

# -----------------------------
# STATE
# -----------------------------
if "show_overlay" not in st.session_state:
    st.session_state.show_overlay = False

if "show_dialog_trigger" not in st.session_state:
    st.session_state.show_dialog_trigger = 0

if "logs" not in st.session_state:
    st.session_state.logs = []


def log(msg: str):
    st.session_state.logs.insert(0, f"{datetime.now().strftime('%H:%M:%S')} · {msg}")


# -----------------------------
# UI
# -----------------------------
st.title("Demo: Ventanas emergentes en Streamlit (Modal/Dialog + Overlay HTML)")

colA, colB, colC = st.columns([1, 1, 2])

with colA:
    st.subheader("1) Modal/Dialog (nativo)")
    open_dialog = st.button("Abrir modal nativo", use_container_width=True)

with colB:
    st.subheader("2) Overlay HTML (components)")
    open_overlay = st.button("Abrir overlay HTML", use_container_width=True)

with colC:
    st.subheader("Notas rápidas")
    st.write(
        "- Modal nativo: recomendado si tu versión de Streamlit lo soporta.\n"
        "- Overlay HTML: funciona en cualquier versión, controlado por session_state."
    )

# -----------------------------
# ACTIONS
# -----------------------------
if open_dialog:
    st.session_state.show_dialog_trigger += 1
    log("Se solicitó abrir modal nativo")

if open_overlay:
    st.session_state.show_overlay = True
    log("Se solicitó abrir overlay HTML")

# -----------------------------
# MODAL / DIALOG NATIVO (si existe)
# -----------------------------
if hasattr(st, "dialog") and st.session_state.show_dialog_trigger > 0:

    @st.dialog("Modal nativo — Streamlit", width="large")
    def native_modal():
        st.write("Este es un modal nativo dentro de Streamlit.")
        st.text_input("Campo dentro del modal", key="native_modal_input")
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            if st.button("Guardar", type="primary", use_container_width=True):
                log(f"Modal nativo: Guardar -> {st.session_state.get('native_modal_input','')}")
                st.success("Guardado")
        with c2:
            if st.button("Cerrar", use_container_width=True):
                log("Modal nativo: Cerrar")
                st.rerun()
        with c3:
            st.caption("Tip: este modal no abre una nueva pestaña, es un popup dentro de la app.")

    native_modal()

elif st.session_state.show_dialog_trigger > 0:
    st.warning("Tu versión de Streamlit no expone st.dialog(). Usa el Overlay HTML para probar popups.")
    st.session_state.show_dialog_trigger = 0

# -----------------------------
# OVERLAY HTML (robusto, sin dependencias externas)
# -----------------------------
def render_overlay_html():
    # Overlay con estilos y cierre por:
    # - Click en el fondo
    # - Botón X
    # - Botón Cerrar
    # - ESC
    html = r"""
    <div id="st_overlay_root">
      <style>
        #st_overlay_root{
          position: fixed;
          inset: 0;
          z-index: 999999;
          font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        }
        .ov_backdrop{
          position: absolute;
          inset: 0;
          background: rgba(0,0,0,.55);
          backdrop-filter: blur(4px);
        }
        .ov_modal{
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          width: min(760px, calc(100vw - 26px));
          max-height: calc(100vh - 26px);
          overflow: auto;
          border-radius: 16px;
          background: #0b1220;
          color: #e8eefc;
          border: 1px solid rgba(255,255,255,.10);
          box-shadow: 0 24px 80px rgba(0,0,0,.60);
        }
        .ov_header{
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 14px 14px 10px 14px;
          position: sticky;
          top: 0;
          background: linear-gradient(180deg, rgba(18, 35, 70, .92), rgba(11, 18, 32, .92));
          border-bottom: 1px solid rgba(255,255,255,.08);
          z-index: 2;
        }
        .ov_title{
          display:flex;
          align-items:center;
          gap:10px;
          font-weight: 700;
          letter-spacing: .2px;
        }
        .ov_badge{
          font-size: 12px;
          padding: 4px 8px;
          border-radius: 999px;
          background: rgba(120,210,255,.16);
          border: 1px solid rgba(120,210,255,.22);
          color: #cfeeff;
        }
        .ov_close{
          width: 34px;
          height: 34px;
          border-radius: 10px;
          border: 1px solid rgba(255,255,255,.12);
          background: rgba(255,255,255,.06);
          color: #e8eefc;
          cursor: pointer;
          display:flex;
          align-items:center;
          justify-content:center;
          font-size: 18px;
          line-height: 1;
        }
        .ov_close:hover{
          background: rgba(255,255,255,.10);
        }
        .ov_body{
          padding: 14px;
        }
        .ov_grid{
          display:grid;
          grid-template-columns: 1fr 1fr;
          gap: 12px;
          margin-top: 10px;
        }
        .ov_card{
          border-radius: 14px;
          border: 1px solid rgba(255,255,255,.10);
          background: rgba(255,255,255,.04);
          padding: 12px;
        }
        .ov_label{
          font-size: 12px;
          opacity: .85;
          margin-bottom: 6px;
        }
        .ov_input{
          width: 100%;
          padding: 10px 12px;
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,.14);
          background: rgba(0,0,0,.22);
          color: #e8eefc;
          outline: none;
        }
        .ov_input:focus{
          border-color: rgba(120,210,255,.55);
          box-shadow: 0 0 0 3px rgba(120,210,255,.18);
        }
        .ov_footer{
          display:flex;
          gap: 10px;
          justify-content: flex-end;
          padding: 14px;
          border-top: 1px solid rgba(255,255,255,.08);
          background: rgba(11, 18, 32, .92);
          position: sticky;
          bottom: 0;
          z-index: 2;
        }
        .ov_btn{
          padding: 10px 12px;
          border-radius: 12px;
          cursor: pointer;
          border: 1px solid rgba(255,255,255,.12);
          background: rgba(255,255,255,.06);
          color: #e8eefc;
          font-weight: 600;
        }
        .ov_btn:hover{
          background: rgba(255,255,255,.10);
        }
        .ov_btn_primary{
          border-color: rgba(120,210,255,.35);
          background: rgba(120,210,255,.18);
        }
        .ov_btn_primary:hover{
          background: rgba(120,210,255,.26);
        }
        .ov_hint{
          font-size: 12px;
          opacity: .75;
          margin-top: 8px;
        }
        @media (max-width: 720px){
          .ov_grid{ grid-template-columns: 1fr; }
        }
      </style>

      <div class="ov_backdrop" id="ov_backdrop"></div>

      <div class="ov_modal" role="dialog" aria-modal="true" aria-label="Overlay Modal">
        <div class="ov_header">
          <div class="ov_title">
            <span>Overlay HTML</span>
            <span class="ov_badge">components.html</span>
          </div>
          <button class="ov_close" id="ov_x" aria-label="Cerrar">×</button>
        </div>

        <div class="ov_body">
          <div class="ov_card">
            <div><b>Prueba rápida:</b> escribe algo abajo. El cierre lo haces en Streamlit (botón "Cerrar overlay").</div>
            <div class="ov_hint">Este overlay se cierra visualmente con JS (x / fondo / ESC), pero el estado real lo controlas en Python.</div>
          </div>

          <div class="ov_grid">
            <div class="ov_card">
              <div class="ov_label">Nombre</div>
              <input class="ov_input" id="ov_name" placeholder="Ej: Jefe" />
            </div>
            <div class="ov_card">
              <div class="ov_label">Correo</div>
              <input class="ov_input" id="ov_email" placeholder="correo@dominio.com" />
            </div>
          </div>

          <div class="ov_card" style="margin-top:12px;">
            <div class="ov_label">Texto libre</div>
            <textarea class="ov_input" id="ov_text" rows="4" placeholder="Escribe algo..."></textarea>
          </div>
        </div>

        <div class="ov_footer">
          <button class="ov_btn" id="ov_close_btn">Cerrar (solo UI)</button>
          <button class="ov_btn ov_btn_primary" id="ov_save_btn">Simular Guardar (solo UI)</button>
        </div>
      </div>

      <script>
        (function(){
          const root = document.getElementById("st_overlay_root");
          const backdrop = document.getElementById("ov_backdrop");
          const xbtn = document.getElementById("ov_x");
          const closeBtn = document.getElementById("ov_close_btn");
          const saveBtn = document.getElementById("ov_save_btn");

          function hideUI(){
            if(root) root.style.display = "none";
          }

          function onEsc(e){
            if(e.key === "Escape"){ hideUI(); }
          }

          backdrop.addEventListener("click", hideUI);
          xbtn.addEventListener("click", hideUI);
          closeBtn.addEventListener("click", hideUI);

          saveBtn.addEventListener("click", function(){
            const name = (document.getElementById("ov_name")||{}).value || "";
            const email = (document.getElementById("ov_email")||{}).value || "";
            const text = (document.getElementById("ov_text")||{}).value || "";
            console.log("[Overlay Save]", {name, email, text});
            hideUI();
          });

          document.addEventListener("keydown", onEsc);
        })();
      </script>
    </div>
    """
    components.html(html, height=0, width=0)


if st.session_state.show_overlay:
    render_overlay_html()
    st.info("Overlay visible. Ciérralo en UI (X / fondo / ESC) y luego cierra el estado aquí para finalizar.")

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Cerrar overlay (estado)", type="primary", use_container_width=True):
            st.session_state.show_overlay = False
            log("Overlay: estado cerrado desde Streamlit")
            st.rerun()
    with c2:
        st.caption("El cierre por JS solo oculta la UI; este botón cierra el estado real en Streamlit.")


# -----------------------------
# LOGS
# -----------------------------
st.divider()
st.subheader("Logs")
if st.session_state.logs:
    st.code("\n".join(st.session_state.logs), language="text")
else:
    st.caption("Sin eventos todavía.")
