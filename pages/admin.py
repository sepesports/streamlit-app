import streamlit as st

if not st.session_state.get("auth"):
    st.switch_page("app.py")

st.set_page_config(layout="wide")
st.title("Panel Admin")

st.write(f"Usuario: {st.session_state.get('user','')}")
st.write(f"Rol: {st.session_state.get('role','')}")

if st.button("Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.role = ""
    st.switch_page("app.py")
