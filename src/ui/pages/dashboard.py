from __future__ import annotations

from collections import Counter

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.ui.styles import badge, card, section_header


def render_dashboard_page() -> None:
    st.markdown(
        '<h1 style="font-family:Fraunces,serif;font-size:2rem;margin-bottom:.1rem;">'
        '📊 Recruiter Dashboard</h1>'
        '<p style="color:var(--text-secondary);margin-bottom:1.5rem;">'
        'Aggregate insights across all resumes analysed in this session.</p>',
        unsafe_allow_html=True,
    )
    has_ats        = "ats_result"      in st.session_state
    has_comparison = "comparison_rankings" in st.session_state

    if not has_ats and not has_comparison:
        st.markdown(
            '<div class="card" style="text-align:center;padding:3rem;border-style:dashed;">'
            '<div style="font-size:3rem;margin-bottom:1rem;">📋</div>'
            '<div class="section-header">No data yet</div>'
            '<div class="section-sub">Analyse a resume on the <b>Resume Analyzer</b> page '
            'or compare resumes on the <b>Multi-Resume Compare</b> page first.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return
    
    if has_ats:
        ats      = st.session_state.ats_result
        diff     = st.session_state.skill_diff
        extracted = st.session_state.extracted
        matches  = st.session_state.get("job_matches", [])

        section_header("Resume Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("ATS Score",      f"{ats.total_score:.0f}/100")
        c2.metric("Grade",          ats.grade)
        c3.metric("Skills Matched", len(diff["matched"]))
        c4.metric("Skills Missing", len(diff["missing"]))

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        col_l, col_r = st.columns([1, 1])

        with col_l:
            section_header("Skills by Category")
            if extracted.by_category:
                labels = list(extracted.by_category.keys())
                values = [len(v) for v in extracted.by_category.values()]
                fig = go.Figure(go.Pie(
                    labels=labels, values=values,
                    hole=.45,
                    marker_colors=px.colors.qualitative.Pastel,
                    textfont_family="DM Sans",
                ))
                fig.update_layout(
                    height=300,
                    margin=dict(t=10, b=10, l=10, r=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    legend=dict(font=dict(family="DM Sans", size=11)),
                    font_family="DM Sans",
                )
                st.plotly_chart(fig, use_container_width=True)

        with col_r:
            section_header("ATS Dimension Scores")
            if ats.dimensions:
                names  = [d.name for d in ats.dimensions]
                scores = [d.score for d in ats.dimensions]
                colors = [
                    "#2D7D5A" if s >= 70 else ("#C47A1E" if s >= 50 else "#C0392B")
                    for s in scores
                ]
                fig2 = go.Figure(go.Bar(
                    x=scores, y=names, orientation="h",
                    marker_color=colors,
                    text=[f"{s:.0f}" for s in scores],
                    textposition="outside",
                ))
                fig2.update_layout(
                    height=300,
                    margin=dict(t=10, b=10, l=10, r=40),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(range=[0, 115], showgrid=False, visible=False),
                    yaxis=dict(autorange="reversed"),
                    font_family="DM Sans",
                    bargap=0.35,
                )
                st.plotly_chart(fig2, use_container_width=True)

        if matches:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            section_header("Top Job Matches")
            rows = [
                {
                    "Rank":    i + 1,
                    "Role":    m.title,
                    "Company": m.company,
                    "Match":   f"{m.similarity_score:.1f}%",
                    "Tier":    m.match_tier,
                    "Salary":  m.salary_range,
                }
                for i, m in enumerate(matches)
            ]
            st.dataframe(rows, use_container_width=True, hide_index=True)

    if has_comparison:
        rankings: list[tuple[str, float]] = st.session_state.comparison_rankings

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        section_header("Candidate Comparison")

        c1, c2, c3 = st.columns(3)
        scores = [s for _, s in rankings]
        c1.metric("Candidates",  len(rankings))
        c2.metric("Top Score",   f"{max(scores):.1f}%")
        c3.metric("Avg Score",   f"{sum(scores)/len(scores):.1f}%")

        names  = [n.replace(".pdf", "") for n, _ in rankings]
        fig3   = go.Figure(go.Bar(
            x=names, y=scores,
            marker_color=["#2D7D5A" if i == 0 else "#4A3F8A" for i in range(len(scores))],
            text=[f"{s:.1f}%" for s in scores],
            textposition="outside",
        ))
        fig3.update_layout(
            height=300,
            margin=dict(t=20, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[0, 110], showgrid=False, visible=False),
            xaxis=dict(tickfont=dict(family="DM Sans")),
            font_family="DM Sans",
            bargap=0.35,
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.dataframe(
            [{"Rank": i+1, "Candidate": n.replace(".pdf",""), "Match Score": f"{s:.1f}%"}
             for i, (n, s) in enumerate(rankings)],
            use_container_width=True,
            hide_index=True,
        )
