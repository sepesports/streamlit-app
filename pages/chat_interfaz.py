import html
from urllib.parse import urlencode

import requests
import streamlit as st

st.set_page_config(layout="wide")

if st.query_params.get("auth") != "ok":
    st.markdown(
        """
        <script>
          window.location.href="/admin";
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

USER_EMAIL = (st.query_params.get("usuario") or "").strip()
USER_ROLE = (st.query_params.get("rol") or "").strip()
USER_DNI = (st.query_params.get("dni") or "").strip()
API_BASE = "https://camilo27.pythonanywhere.com"
TIMEOUT = 25

st.markdown(
    """
    <style>
      .block-container{padding-top:0.8rem !important;padding-bottom:0 !important;max-width:100% !important;}
      header, footer{display:none !important;}
      [data-testid="stSidebar"]{display:none !important;}
      .stApp{background:#ffffff;}
      .chat-shell{border:2px solid #111111;border-radius:0;padding:12px;background:#ffffff;}
      .chat-toolbar{border:2px solid #111111;padding:10px 12px;margin-bottom:12px;background:#ffffff;}
      .list-card{border:2px solid #111111;padding:10px 12px;margin-bottom:8px;background:#ffffff;}
      .list-card small{color:#444444;}
      .bubble-wrap{border:2px solid #111111;padding:12px;background:#ffffff;height:58vh;overflow-y:auto;}
      .bubble-row{display:flex;width:100%;margin:0 0 10px 0;}
      .bubble-row.me{justify-content:flex-end;}
      .bubble{max-width:80%;border:2px solid #111111;padding:10px 12px;background:#ffffff;word-break:break-word;}
      .bubble-name{font-size:12px;color:#555555;margin-bottom:4px;}
      .bubble-time{font-size:11px;color:#666666;margin-top:6px;}
      .section-title{border:2px solid #111111;padding:10px 12px;margin-bottom:10px;background:#ffffff;font-weight:600;}
      .empty-box{border:2px solid #111111;padding:16px;background:#ffffff;}
      .notif-pill{display:inline-block;border:2px solid #111111;border-radius:999px;padding:2px 10px;font-size:12px;margin-left:8px;}
      div[data-testid="stHorizontalBlock"] button[kind="secondary"],
      div[data-testid="stHorizontalBlock"] button[kind="primary"]{min-height:58px;font-weight:500;}
      .menu-link a{display:inline-block;text-decoration:none;border:2px solid #111111;padding:9px 14px;color:#111111;background:#ffffff;}
      .menu-link a:hover{background:#f3f3f3;}
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_chat_state():
    keys = [
        "chat_tab",
        "chat_selected_thread_id",
        "chat_selected_thread_title",
        "chat_selected_thread_type",
        "chat_soc_search",
        "chat_inst_search",
        "chat_draft",
        "chat_user_signature",
        "chat_last_error",
    ]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]


def current_signature() -> str:
    return f"{USER_EMAIL}|{USER_DNI}|{USER_ROLE}"


if st.session_state.get("chat_user_signature") != current_signature():
    reset_chat_state()
    st.session_state["chat_user_signature"] = current_signature()

st.session_state.setdefault("chat_tab", "socorristas")
st.session_state.setdefault("chat_selected_thread_id", "")
st.session_state.setdefault("chat_selected_thread_title", "")
st.session_state.setdefault("chat_selected_thread_type", "")
st.session_state.setdefault("chat_soc_search", "")
st.session_state.setdefault("chat_inst_search", "")
st.session_state.setdefault("chat_draft", "")
st.session_state.setdefault("chat_last_error", "")


def build_auth_params(extra=None):
    params = {"auth": "ok"}
    if USER_EMAIL:
        params["usuario"] = USER_EMAIL
    if USER_ROLE:
        params["rol"] = USER_ROLE
    if USER_DNI:
        params["dni"] = USER_DNI
    if extra:
        params.update({k: v for k, v in extra.items() if v is not None and v != ""})
    return params


def menu_url() -> str:
    return "/?" + urlencode(build_auth_params())


def api_get(path: str, params=None):
    final_params = build_auth_params(params or {})
    response = requests.get(f"{API_BASE}{path}", params=final_params, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload=None):
    final_payload = build_auth_params(payload or {})
    response = requests.post(f"{API_BASE}{path}", json=final_payload, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def show_error(message: str):
    st.session_state["chat_last_error"] = str(message or "")


def clear_error():
    st.session_state["chat_last_error"] = ""


def get_me():
    response = api_get("/api/chat/me")
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible resolver el usuario actual")
    return response["user"]


def get_users():
    response = api_get("/api/chat/users")
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible cargar usuarios")
    return response.get("items", [])


def get_threads():
    response = api_get("/api/chat/threads")
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible cargar hilos")
    return response.get("items", [])


def get_installation_threads(installation_name=""):
    payload = {}
    if installation_name:
        payload["installation"] = installation_name
    response = api_get("/api/chat/installations", payload)
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible cargar instalaciones")
    return response.get("installation", ""), response.get("items", [])


def get_installation_names():
    response = api_get("/api/chat/installations/list")
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible cargar instalaciones")
    return response.get("current_installation", ""), response.get("items", [])


def open_private_thread(other_user_id: str):
    response = api_post("/api/chat/threads/private", {"other_user_id": other_user_id})
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible abrir el chat privado")
    thread = response.get("thread") or {}
    st.session_state["chat_selected_thread_id"] = thread.get("id", "")
    st.session_state["chat_selected_thread_title"] = thread.get("title", "")
    st.session_state["chat_selected_thread_type"] = thread.get("type", "")


def open_installation_thread(installation_name: str):
    response = api_post("/api/chat/threads/installation", {"installation": installation_name})
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible abrir el grupo de instalación")
    thread = response.get("thread") or {}
    st.session_state["chat_selected_thread_id"] = thread.get("id", "")
    st.session_state["chat_selected_thread_title"] = thread.get("title", "")
    st.session_state["chat_selected_thread_type"] = thread.get("type", "")


def get_thread_messages(thread_id: str):
    response = api_get(f"/api/chat/threads/{thread_id}/messages")
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible cargar mensajes")
    thread = response.get("thread") or {}
    messages = response.get("messages") or []
    st.session_state["chat_selected_thread_title"] = thread.get("title", st.session_state.get("chat_selected_thread_title", ""))
    st.session_state["chat_selected_thread_type"] = thread.get("type", st.session_state.get("chat_selected_thread_type", ""))
    return thread, messages


def send_message(thread_id: str, body: str):
    response = api_post(f"/api/chat/threads/{thread_id}/messages", {"body": body})
    if not response.get("ok"):
        raise RuntimeError(response.get("error") or "No fue posible enviar el mensaje")
    return response.get("message") or {}


def format_timestamp(value: str) -> str:
    if not value:
        return ""
    text = value.replace("Z", "+00:00")
    try:
        dt = st.session_state.get("_tmp_dt")
        del dt
    except Exception:
        pass
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(text)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return value


def render_message_history(messages, my_user_id: str):
    if not messages:
        st.markdown('<div class="empty-box">No hay mensajes todavía en este chat.</div>', unsafe_allow_html=True)
        return

    blocks = ['<div class="bubble-wrap">']
    for item in messages:
        mine = str(item.get("sender_id") or "") == str(my_user_id or "") or bool(item.get("mine"))
        row_class = "bubble-row me" if mine else "bubble-row"
        sender = "Tú" if mine else html.escape(str(item.get("sender_name") or item.get("sender_id") or "Usuario"))
        body = html.escape(str(item.get("body") or "")).replace("\n", "<br>")
        created_at = html.escape(format_timestamp(str(item.get("created_at") or "")))
        blocks.append(
            f'<div class="{row_class}"><div class="bubble"><div class="bubble-name">{sender}</div><div>{body}</div><div class="bubble-time">{created_at}</div></div></div>'
        )
    blocks.append("</div>")
    st.markdown("".join(blocks), unsafe_allow_html=True)


try:
    clear_error()
    me = get_me()
    all_threads = get_threads()
except Exception as exc:
    st.markdown(f'<div class="empty-box">{html.escape(str(exc))}</div>', unsafe_allow_html=True)
    st.stop()

unread_total = sum(int(item.get("unread_count") or 0) for item in all_threads)

col_top_1, col_top_2, col_top_3 = st.columns([1, 1, 1.15], gap="small")
with col_top_1:
    if st.button("seleccióna\nSocorristas", use_container_width=True, type="primary" if st.session_state["chat_tab"] == "socorristas" else "secondary"):
        st.session_state["chat_tab"] = "socorristas"
        st.rerun()
with col_top_2:
    if st.button("seleccióna\nInstalación", use_container_width=True, type="primary" if st.session_state["chat_tab"] == "instalacion" else "secondary"):
        st.session_state["chat_tab"] = "instalacion"
        st.rerun()
with col_top_3:
    notif_label = f"Notificaciones ({unread_total})" if unread_total else "Notificaciones"
    if st.button(notif_label, use_container_width=True, type="primary" if st.session_state["chat_tab"] == "notificaciones" else "secondary"):
        st.session_state["chat_tab"] = "notificaciones"
        st.rerun()

col_toolbar_1, col_toolbar_2, col_toolbar_3 = st.columns([1, 5, 1], gap="small")
with col_toolbar_1:
    st.markdown(f'<div class="menu-link"><a href="{menu_url()}">Menú</a></div>', unsafe_allow_html=True)
with col_toolbar_2:
    toolbar_parts = [me.get("display_name") or me.get("correo") or "Usuario"]
    if me.get("role"):
        toolbar_parts.append(me["role"])
    if me.get("installation"):
        toolbar_parts.append(me["installation"])
    st.markdown(f'<div class="chat-toolbar">{" · ".join(html.escape(str(x)) for x in toolbar_parts if x)}</div>', unsafe_allow_html=True)
with col_toolbar_3:
    if st.button("Actualizar", use_container_width=True):
        st.rerun()

left_col, right_col = st.columns([1.05, 1.45], gap="medium")

selected_thread = None
selected_messages = []
selected_thread_id = st.session_state.get("chat_selected_thread_id", "")
if selected_thread_id:
    try:
        selected_thread, selected_messages = get_thread_messages(selected_thread_id)
    except Exception as exc:
        show_error(str(exc))
        st.session_state["chat_selected_thread_id"] = ""
        st.session_state["chat_selected_thread_title"] = ""
        st.session_state["chat_selected_thread_type"] = ""
        selected_thread = None
        selected_messages = []

with left_col:
    if st.session_state.get("chat_last_error"):
        st.markdown(f'<div class="empty-box">{html.escape(st.session_state["chat_last_error"])}</div>', unsafe_allow_html=True)

    current_tab = st.session_state["chat_tab"]

    if current_tab == "socorristas":
        st.markdown('<div class="section-title">Socorristas</div>', unsafe_allow_html=True)
        st.text_input("Filtrar socorristas", key="chat_soc_search", placeholder="Nombre, correo o rol")
        try:
            users = get_users()
        except Exception as exc:
            users = []
            show_error(str(exc))

        term = (st.session_state.get("chat_soc_search") or "").strip().lower()
        filtered_users = []
        for item in users:
            text = " ".join([
                str(item.get("display_name") or ""),
                str(item.get("correo") or ""),
                str(item.get("role") or ""),
                str(item.get("installation") or ""),
            ]).lower()
            if not term or term in text:
                filtered_users.append(item)

        if not filtered_users:
            st.markdown('<div class="empty-box">No hay usuarios visibles para este filtro.</div>', unsafe_allow_html=True)
        else:
            for item in filtered_users:
                label = item.get("display_name") or item.get("correo") or item.get("user_id") or "Usuario"
                subtitle_parts = [item.get("role") or "", item.get("correo") or ""]
                if item.get("installation"):
                    subtitle_parts.append(item["installation"])
                st.markdown(
                    f'<div class="list-card"><strong>{html.escape(str(label))}</strong><br><small>{html.escape(" · ".join([str(x) for x in subtitle_parts if x]))}</small></div>',
                    unsafe_allow_html=True,
                )
                if st.button(f"Abrir chat con {label}", key=f"open_user_{item.get('user_id')}", use_container_width=True):
                    try:
                        open_private_thread(str(item.get("user_id") or ""))
                        clear_error()
                        st.rerun()
                    except Exception as exc:
                        show_error(str(exc))
                        st.rerun()

    elif current_tab == "instalacion":
        st.markdown('<div class="section-title">Instalación</div>', unsafe_allow_html=True)
        st.text_input("Buscar instalación", key="chat_inst_search", placeholder="Nombre de instalación")
        try:
            current_installation, installation_names = get_installation_names()
            _, group_threads = get_installation_threads(current_installation or "")
        except Exception as exc:
            current_installation, installation_names, group_threads = "", [], []
            show_error(str(exc))

        search_term = (st.session_state.get("chat_inst_search") or "").strip().lower()

        if current_installation:
            st.markdown(
                f'<div class="list-card"><strong>Mi instalación</strong><br><small>{html.escape(current_installation)}</small></div>',
                unsafe_allow_html=True,
            )
            if st.button("Abrir grupo de mi instalación", key="open_my_installation", use_container_width=True):
                try:
                    open_installation_thread(current_installation)
                    clear_error()
                    st.rerun()
                except Exception as exc:
                    show_error(str(exc))
                    st.rerun()
        else:
            st.markdown('<div class="empty-box">El usuario actual no tiene instalación detectada.</div>', unsafe_allow_html=True)

        filtered_installations = [name for name in installation_names if not search_term or search_term in name.lower()]
        if filtered_installations:
            st.markdown('<div class="section-title">Abrir por instalación</div>', unsafe_allow_html=True)
            for name in filtered_installations:
                st.markdown(f'<div class="list-card"><strong>{html.escape(name)}</strong></div>', unsafe_allow_html=True)
                if st.button(f"Abrir {name}", key=f"inst_name_{name}", use_container_width=True):
                    try:
                        open_installation_thread(name)
                        clear_error()
                        st.rerun()
                    except Exception as exc:
                        show_error(str(exc))
                        st.rerun()
        else:
            st.markdown('<div class="empty-box">No hay instalaciones que coincidan.</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Mis grupos de instalación</div>', unsafe_allow_html=True)
        visible_groups = [g for g in group_threads if not search_term or search_term in str(g.get("title") or "").lower()]
        if not visible_groups:
            st.markdown('<div class="empty-box">No hay grupos visibles para este filtro.</div>', unsafe_allow_html=True)
        else:
            for item in visible_groups:
                title = item.get("title") or "Grupo"
                meta = []
                if item.get("last_message_preview"):
                    meta.append(str(item.get("last_message_preview")))
                if item.get("last_message_at"):
                    meta.append(format_timestamp(str(item.get("last_message_at"))))
                if int(item.get("unread_count") or 0) > 0:
                    meta.append(f"Pendientes: {int(item.get('unread_count') or 0)}")
                st.markdown(
                    f'<div class="list-card"><strong>{html.escape(title)}</strong><br><small>{html.escape(" · ".join(meta))}</small></div>',
                    unsafe_allow_html=True,
                )
                if st.button(f"Abrir grupo {title}", key=f"group_{item.get('id')}", use_container_width=True):
                    st.session_state["chat_selected_thread_id"] = item.get("id", "")
                    st.session_state["chat_selected_thread_title"] = title
                    st.session_state["chat_selected_thread_type"] = item.get("type", "group")
                    clear_error()
                    st.rerun()

    else:
        st.markdown('<div class="section-title">Notificaciones</div>', unsafe_allow_html=True)
        notifications = [item for item in all_threads if int(item.get("unread_count") or 0) > 0]
        if not notifications:
            st.markdown('<div class="empty-box">No hay notificaciones pendientes.</div>', unsafe_allow_html=True)
        else:
            for item in notifications:
                title = item.get("title") or "Chat"
                meta = []
                if item.get("last_message_preview"):
                    meta.append(str(item.get("last_message_preview")))
                if item.get("last_message_at"):
                    meta.append(format_timestamp(str(item.get("last_message_at"))))
                badge = f' <span class="notif-pill">{int(item.get("unread_count") or 0)}</span>' if int(item.get("unread_count") or 0) > 0 else ""
                st.markdown(
                    f'<div class="list-card"><strong>{html.escape(title)}</strong>{badge}<br><small>{html.escape(" · ".join(meta))}</small></div>',
                    unsafe_allow_html=True,
                )
                if st.button(f"Abrir notificación {title}", key=f"notif_{item.get('id')}", use_container_width=True):
                    st.session_state["chat_selected_thread_id"] = item.get("id", "")
                    st.session_state["chat_selected_thread_title"] = title
                    st.session_state["chat_selected_thread_type"] = item.get("type", "")
                    clear_error()
                    st.rerun()

with right_col:
    title = st.session_state.get("chat_selected_thread_title") or "Nombre del socorrista o Grupo de instalación"
    type_label = st.session_state.get("chat_selected_thread_type") or ""
    title_suffix = " · Grupo" if type_label == "group" else " · Privado" if type_label == "private" else ""
    st.markdown(f'<div class="section-title">{html.escape(title + title_suffix)}</div>', unsafe_allow_html=True)

    if not st.session_state.get("chat_selected_thread_id"):
        st.markdown('<div class="empty-box">Selecciona un socorrista, una instalación o una notificación para abrir el chat.</div>', unsafe_allow_html=True)
        st.text_input("Dialogo para enviar Mensaje", value="", disabled=True)
        st.button("SEND", disabled=True, use_container_width=True)
    else:
        render_message_history(selected_messages, me.get("user_id") or "")
        with st.form("chat_send_form", clear_on_submit=True):
            draft = st.text_input("Dialogo para enviar Mensaje", key="chat_draft_input")
            submitted = st.form_submit_button("SEND", use_container_width=True)
        if submitted:
            clean = (draft or "").strip()
            if not clean:
                show_error("Mensaje vacío")
                st.rerun()
            try:
                send_message(st.session_state["chat_selected_thread_id"], clean)
                clear_error()
                st.rerun()
            except Exception as exc:
                show_error(str(exc))
                st.rerun()
