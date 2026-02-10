import streamlit as st

if not st.session_state.get("auth"):
    st.switch_page("app.py")

st.title("Panel Admin")

st.write(f"Usuario conectado: {st.session_state.get('user')}")

if st.button("Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.switch_page("app.py")
