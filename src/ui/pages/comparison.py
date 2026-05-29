from __future__ import annotations

import time

import plotly.graph_objects as go
import streamlit as st

from src.core.job_matcher import compare_resumes
from src.core.pdf_parser import PDFExtractionError, extract_text_from_pdf
from src.core.skill_extractor import extract_skills
from src.ui.styles import badge, section_header


def render_comparison_page() -> None:
    st.markdown(
        '<h1 style="font-family:Fraunces,serif;font-size:2rem;margin-bottom:.1rem;">'
        '⚖️  Multi-Resume Compare</h1>'
        '<p style="color:var(--text-secondary);margin-bottom:1.5rem;">'
        'Upload multiple resumes and a job description to rank candidates semantically.</p>',
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        section_header("Upload Resumes", "Up to 5 PDF files")
        uploaded_files = st.file_uploader(
            "Drop resumes here",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

    with col_right:
        section_header("Job Description")
        job_text = st.text_area(
            "Paste the target job description",
            height=180,
            placeholder="Paste the full job description here…",
            label_visibility="collapsed",
        )

    if not uploaded_files or not job_text.strip():
        st.info("Upload at least 2 resumes and paste a job description to compare.")
        return

    if len(uploaded_files) > 5:
        st.warning("Maximum 5 resumes supported. Only the first 5 will be processed.")
        uploaded_files = uploaded_files[:5]

    if st.button("🏆  Rank Candidates", use_container_width=False):
        resumes: list[tuple[str, str]] = []
        errors:  list[str]             = []

        with st.spinner("Extracting resume texts…"):
            for f in uploaded_files:
                try:
                    text = extract_text_from_pdf(f.read())
                    resumes.append((f.name, text))
                except PDFExtractionError as exc:
                    errors.append(f"{f.name}: {exc}")

        if errors:
            for e in errors:
                st.warning(e)

        if len(resumes) < 2:
            st.error("Need at least 2 readable resumes to compare.")
            return

        with st.spinner("Running semantic comparison…"):
            rankings = compare_resumes(resumes, job_text)

        st.session_state.comparison_rankings = rankings
        st.session_state.comparison_resumes  = {name: text for name, text in resumes}

    if "comparison_rankings" not in st.session_state:
        return

    rankings: list[tuple[str, float]] = st.session_state.comparison_rankings
    resumes_dict: dict[str, str]      = st.session_state.comparison_resumes

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    section_header("Candidate Rankings", "Sorted by semantic fit to the job description")

    names  = [r[0].replace(".pdf", "") for r in rankings]
    scores = [r[1] for r in rankings]
    colors = ["#2D7D5A" if i == 0 else ("#C47A1E" if i == 1 else "#6B7280") for i in range(len(scores))]

    fig = go.Figure(go.Bar(
        x=scores, y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{s:.1f}%" for s in scores],
        textposition="outside",
    ))
    fig.update_layout(
        height=max(200, len(rankings) * 60),
        margin=dict(t=10, b=10, l=10, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 110], showgrid=False, visible=False),
        yaxis=dict(autorange="reversed", tickfont=dict(family="DM Sans")),
        font_family="DM Sans",
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)

    medals = ["🥇", "🥈", "🥉"]
    for rank, (name, score) in enumerate(rankings):
        medal = medals[rank] if rank < 3 else f"#{rank+1}"
        tier  = "Excellent" if score >= 75 else ("Strong" if score >= 60 else "Good")
        color = "green" if score >= 75 else ("orange" if score >= 60 else "red")

        short_name = name.replace(".pdf", "")
        skills = extract_skills(resumes_dict.get(name, "")).all_skills

        with st.expander(f"{medal}  {short_name}  —  {score:.1f}% match  {badge(tier, color)}", expanded=(rank == 0)):
            st.markdown(
                f'**Similarity Score:** {score:.1f} / 100  \n'
                f'**Skills detected:** {len(skills)}',
                unsafe_allow_html=True,
            )
            if skills:
                st.markdown(
                    "".join(
                        f'<span class="skill-chip">{s}</span>'
                        for s in skills[:15]
                    ) + ("…" if len(skills) > 15 else ""),
                    unsafe_allow_html=True,
                )
            with st.expander("View resume text", expanded=False):
                st.text(resumes_dict.get(name, "")[:1500] + "…")
