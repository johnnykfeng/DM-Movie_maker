import streamlit as st


pages = [
    st.Page("pages/st_frame_viewer.py", title="Frame Viewer"),
    st.Page("pages/st_animate_frame.py", title="Frame Animation"),
]
pg = st.navigation(pages)

pg.run()



