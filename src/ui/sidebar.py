import streamlit as st


_PAGES = [
    ("analyzer",   "🔍", "Resume Analyzer"),
    ("interview",  "💬", "Interview Coach"),
    ("comparison", "⚖️",  "Multi-Resume Compare"),
    ("dashboard",  "📊", "Recruiter Dashboard"),
]


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            '<div style="padding:1rem 0 .5rem">'
            '<span class="logo-text">Resume<span style="color:#E8572A">AI</span></span>'
            '<p style="font-size:.75rem;color:var(--text-muted);margin-top:.25rem;">'
            'Intelligent Career Assistant</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        if "page" not in st.session_state:
            st.session_state.page = "analyzer"

        st.markdown(
            '<p style="font-size:.7rem;font-weight:600;letter-spacing:.1em;'
            'text-transform:uppercase;color:var(--text-muted);'
            'margin-bottom:.4rem;">Navigation</p>',
            unsafe_allow_html=True,
        )

        for key, icon, label in _PAGES:
            active = "active" if st.session_state.page == key else ""
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state.page = key

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        with st.expander("⚙️  Settings", expanded=False):
            st.session_state.ats_strictness = st.select_slider(
                "ATS Strictness",
                options=["Lenient", "Balanced", "Strict"],
                value=st.session_state.get("ats_strictness", "Balanced"),
            )
            st.session_state.top_k_jobs = st.slider(
                "Job recommendations", 3, 10,
                value=st.session_state.get("top_k_jobs", 5),
            )
            st.session_state.num_questions = st.slider(
                "Interview questions", 5, 20,
                value=st.session_state.get("num_questions", 10),
            )

        st.markdown(
            '<div style="position:fixed;bottom:1rem;left:0;width:17rem;'
            'padding:0 1rem;font-size:.72rem;color:var(--text-muted);">'
            '© 2024 ResumeAI · v1.0.0</div>',
            unsafe_allow_html=True,
        )

    return st.session_state.page
