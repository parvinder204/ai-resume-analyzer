from __future__ import annotations

import json
import time

import plotly.graph_objects as go
import streamlit as st

from src.core.ats_scorer import ATSResult, Strictness, compute_ats_score
from src.core.job_matcher import JobMatch, match_jobs
from src.core.pdf_parser import PDFExtractionError, extract_text_from_pdf
from src.core.skill_extractor import compare_skills, extract_skills
from src.ui.styles import badge, card, section_header, skill_chip
from src.utils.job_loader import load_jobs, parse_custom_job


_TRANSPARENT = "rgba(0,0,0,0)"

def _score_gauge(score: float, grade: str) -> go.Figure:
    color = "#2D7D5A" if score >= 70 else ("#C47A1E" if score >= 50 else "#C0392B")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        number={"suffix": "", "font": {"size": 48, "family": "Fraunces", "color": "#1C1C1C"}},
        gauge={
            "axis":      {"range": [0, 100], "tickwidth": 1, "tickcolor": "#E2DDD4"},
            "bar":       {"color": color, "thickness": 0.25},
            "bgcolor":   "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50],  "color": "#FDE8E6"},
                {"range": [50, 70], "color": "#FEF0E3"},
                {"range": [70, 100],"color": "#E0F2EA"},
            ],
            "threshold": {
                "line":      {"color": color, "width": 4},
                "thickness": 0.8,
                "value":     score,
            },
        },
    ))
    fig.update_layout(
        height=220, margin=dict(t=20, b=10, l=10, r=10),
        paper_bgcolor=_TRANSPARENT, plot_bgcolor=_TRANSPARENT,
        font_family="DM Sans",
    )
    return fig


def _radar_chart(dimensions) -> go.Figure:
    labels  = [d.name for d in dimensions]
    values  = [d.score for d in dimensions]
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        fillcolor="rgba(26,107,85,0.15)",
        line=dict(color="#1A6B55", width=2),
        marker=dict(color="#1A6B55", size=6),
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont_size=10),
            angularaxis=dict(tickfont_size=11),
            bgcolor=_TRANSPARENT,
        ),
        showlegend=False,
        height=320,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor=_TRANSPARENT,
        plot_bgcolor=_TRANSPARENT,
        font_family="DM Sans",
    )
    return fig


def _bar_dimensions(dimensions) -> go.Figure:
    names  = [d.name for d in dimensions]
    scores = [d.score for d in dimensions]
    colors = ["#2D7D5A" if s >= 70 else ("#C47A1E" if s >= 50 else "#C0392B") for s in scores]

    fig = go.Figure(go.Bar(
        x=scores, y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{s:.0f}" for s in scores],
        textposition="outside",
    ))
    fig.update_layout(
        height=280,
        margin=dict(t=10, b=10, l=10, r=40),
        paper_bgcolor=_TRANSPARENT, plot_bgcolor=_TRANSPARENT,
        xaxis=dict(range=[0, 110], showgrid=False, visible=False),
        yaxis=dict(autorange="reversed"),
        font_family="DM Sans",
        bargap=0.35,
    )
    return fig

def render_analyzer_page() -> None:
    st.markdown(
        '<h1 style="font-family:Fraunces,serif;font-size:2rem;margin-bottom:.1rem;">'
        '🔍 Resume Analyzer</h1>'
        '<p style="color:var(--text-secondary);margin-bottom:1.5rem;">'
        'Upload your resume and a job description to get your ATS score, '
        'skill gap analysis, and personalised improvement tips.</p>',
        unsafe_allow_html=True,
    )

    col_upload, col_job = st.columns([1, 1], gap="large")

    with col_upload:
        section_header("Your Resume", "PDF format required")
        uploaded = st.file_uploader(
            "Drop PDF here or click to browse",
            type=["pdf"],
            label_visibility="collapsed",
        )

    with col_job:
        section_header("Job Description", "Paste or choose a sample role")
        job_source = st.radio(
            "Source", ["Sample Jobs", "Custom Paste"],
            horizontal=True, label_visibility="collapsed",
        )
        jobs = load_jobs()

        if job_source == "Sample Jobs":
            job_titles = [f"{j['title']} @ {j['company']}" for j in jobs]
            selected   = st.selectbox("Choose a role", job_titles, label_visibility="collapsed")
            chosen_job = jobs[job_titles.index(selected)]
        else:
            custom_text = st.text_area(
                "Paste job description",
                height=160,
                placeholder="Paste the full job description here…",
                label_visibility="collapsed",
            )
            chosen_job = parse_custom_job(custom_text) if custom_text.strip() else None

    if not uploaded:
        _render_landing_cta()
        return

    if chosen_job is None:
        st.info("Please paste a job description or select a sample role.")
        return

    if st.button("⚡  Analyse Resume", use_container_width=False):
        _run_analysis(uploaded, chosen_job, jobs)
    elif "ats_result" in st.session_state:
        _render_results()


def _run_analysis(uploaded_file, chosen_job: dict, all_jobs: list[dict]) -> None:
    with st.spinner("Extracting text…"):
        try:
            resume_text = extract_text_from_pdf(uploaded_file.read())
        except PDFExtractionError as exc:
            st.error(str(exc))
            return

    progress = st.progress(0, text="Extracting skills…")

    extracted        = extract_skills(resume_text)
    job_skills_raw   = chosen_job.get("required_skills", [])

    job_extracted = extract_skills(chosen_job.get("description", ""))
    job_skills    = set(job_skills_raw) | job_extracted.raw_matches
    skill_diff    = compare_skills(extracted.raw_matches, job_skills)

    progress.progress(40, text="Computing ATS score…")
    strictness  = Strictness(st.session_state.get("ats_strictness", "Balanced"))
    ats_result  = compute_ats_score(
        resume_text,
        chosen_job.get("description", ""),
        skill_diff["matched"],
        skill_diff["missing"],
        strictness,
    )

    progress.progress(70, text="Matching jobs semantically…")
    top_k   = st.session_state.get("top_k_jobs", 5)
    matches = match_jobs(resume_text, extracted.raw_matches, all_jobs, top_k=top_k)

    progress.progress(100, text="Done!")
    time.sleep(0.3)
    progress.empty()
    
    st.session_state.ats_result      = ats_result
    st.session_state.skill_diff      = skill_diff
    st.session_state.extracted       = extracted
    st.session_state.job_matches     = matches
    st.session_state.resume_text     = resume_text
    st.session_state.chosen_job      = chosen_job

    _render_results()


def _render_results() -> None:
    ats: ATSResult    = st.session_state.ats_result
    diff: dict        = st.session_state.skill_diff
    extracted         = st.session_state.extracted
    matches: list[JobMatch] = st.session_state.job_matches

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    col_g, col_m, col_m2, col_m3 = st.columns([1.2, 1, 1, 1])
    with col_g:
        st.plotly_chart(_score_gauge(ats.total_score, ats.grade), use_container_width=True)
        st.markdown(
            f'<div style="text-align:center;margin-top:-.5rem;">'
            f'{badge(f"Grade {ats.grade}", ats.color)}</div>',
            unsafe_allow_html=True,
        )

    with col_m:
        st.metric("Skills Matched", f"{len(diff['matched'])}")
    with col_m2:
        st.metric("Skills Missing", f"{len(diff['missing'])}")
    with col_m3:
        st.metric("Bonus Skills", f"{len(diff['bonus'])}")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Score Breakdown", "🧩 Skills", "💼 Job Matches", "💡 Suggestions"]
    )

    with tab1:
        c1, c2 = st.columns([1, 1])
        with c1:
            section_header("Dimension Radar")
            st.plotly_chart(_radar_chart(ats.dimensions), use_container_width=True)
        with c2:
            section_header("Score by Dimension")
            st.plotly_chart(_bar_dimensions(ats.dimensions), use_container_width=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        section_header("Dimension Details")
        for dim in ats.dimensions:
            color  = "green" if dim.score >= 70 else ("orange" if dim.score >= 50 else "red")
            with st.expander(f"{dim.name}  —  {dim.score:.0f}/100 {badge(color.upper(), color)}", expanded=False):
                for note in dim.notes:
                    st.markdown(f"• {note}")
                st.progress(int(dim.score) / 100)

    with tab2:
        c1, c2, c3 = st.columns(3)
        with c1:
            section_header("✅ Matched Skills")
            chips = "".join(skill_chip(s, "matched") for s in diff["matched"]) or "<i>None</i>"
            st.markdown(chips, unsafe_allow_html=True)
        with c2:
            section_header("❌ Missing Skills")
            chips = "".join(skill_chip(s, "missing") for s in diff["missing"]) or "<i>None</i>"
            st.markdown(chips, unsafe_allow_html=True)
        with c3:
            section_header("⭐ Bonus Skills")
            chips = "".join(skill_chip(s, "suggested") for s in diff["bonus"]) or "<i>None</i>"
            st.markdown(chips, unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        section_header("All Detected Skills", "Grouped by category")
        for cat, skills in extracted.by_category.items():
            st.markdown(f"**{cat}**", unsafe_allow_html=True)
            st.markdown(
                "".join(skill_chip(s) for s in skills),
                unsafe_allow_html=True,
            )
            st.markdown("")

    with tab3:
        section_header("Top Job Matches", "Ranked by semantic similarity to your resume")
        for i, match in enumerate(matches):
            _render_job_card(match, i + 1)

    with tab4:
        section_header("Improvement Suggestions", "Personalised tips to boost your ATS score")
        for i, tip in enumerate(ats.suggestions, 1):
            st.markdown(
                f'<div class="question-card">'
                f'<div class="question-tag">Tip {i}</div>'
                f'<div>{tip}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        section_header("Resume Text Preview")
        with st.expander("View extracted text", expanded=False):
            st.text(st.session_state.resume_text[:3000] + "…")


def _render_job_card(match: JobMatch, rank: int) -> None:
    tier_colors = {"Excellent": "#2D7D5A", "Strong": "#1A6B55",
                   "Good": "#C47A1E", "Fair": "#C0392B"}
    color = tier_colors[match.match_tier]

    st.markdown(
        f'<div class="card" style="border-left:3px solid {color};margin-bottom:.8rem;">'
        f'<div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem;">'
        f'<div class="rank-badge" style="background:{color};">{rank}</div>'
        f'<div>'
        f'<div style="font-family:Fraunces,serif;font-size:1rem;font-weight:600;">{match.title}</div>'
        f'<div style="font-size:.82rem;color:var(--text-secondary);">{match.company} · {match.location}</div>'
        f'</div>'
        f'<div style="margin-left:auto;text-align:right;">'
        f'<div style="font-family:Fraunces,serif;font-size:1.4rem;font-weight:700;color:{color};">'
        f'{match.similarity_score:.0f}%</div>'
        f'<div style="font-size:.72rem;color:var(--text-muted);">{match.match_tier} Match</div>'
        f'</div></div>'
        f'<div style="font-size:.83rem;color:var(--text-secondary);margin-bottom:.6rem;">'
        f'💰 {match.salary_range}</div>'
        f'<div>{"".join(skill_chip(s,"matched") for s in match.matched_skills[:6])}'
        f'{"".join(skill_chip(s,"missing") for s in match.missing_skills[:4])}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_landing_cta() -> None:
    st.markdown(
        '<div class="card" style="text-align:center;padding:3rem;border-style:dashed;">'
        '<div style="font-size:3rem;margin-bottom:1rem;">📄</div>'
        '<div class="section-header">Upload your resume to get started</div>'
        '<div class="section-sub">We\'ll analyse your ATS score, extract skills, '
        'and match you to the best-fit roles — all in seconds.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
