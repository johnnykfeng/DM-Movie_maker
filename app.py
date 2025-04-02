import streamlit as st

pages = [
    st.Page("streamlit_pages/st_frame_viewer.py", title="Frame Viewer"),
    st.Page("streamlit_pages/st_animate_frame.py", title="Frame Animation"),
    st.Page("deploy_dm-frame-viewer.py", title="Frame by Frame Analyzer"),
]
pg = st.navigation(pages)

pg.run()



