from __future__ import annotations

import streamlit as st

from src.core.interview_gen import InterviewQuestion, QuestionType, generate_questions
from src.ui.styles import badge, section_header

_TYPE_COLORS = {
    QuestionType.TECHNICAL:     "blue",
    QuestionType.BEHAVIOURAL:   "green",
    QuestionType.SITUATIONAL:   "orange",
    QuestionType.CULTURE_FIT:   "red",
    QuestionType.ROLE_SPECIFIC: "blue",
}

_DIFFICULTY_COLORS = {
    "Easy":   "green",
    "Medium": "orange",
    "Hard":   "red",
}


def render_interview_page() -> None:
    st.markdown(
        '<h1 style="font-family:Fraunces,serif;font-size:2rem;margin-bottom:.1rem;">'
        '💬 Interview Coach</h1>'
        '<p style="color:var(--text-secondary);margin-bottom:1.5rem;">'
        'Generate a personalised interview question bank based on your skills and target role.</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        skills_input = st.text_input(
            "Your Skills (comma-separated)",
            value=", ".join(st.session_state.get("extracted", type("", (), {"all_skills": []})()).all_skills[:10])
                  if "extracted" in st.session_state else "",
            placeholder="Python, React, Docker, AWS, …",
        )

    with col2:
        job_title = st.text_input("Target Job Title", placeholder="e.g. Senior Engineer")

    with col3:
        num_q = st.number_input(
            "# Questions",
            min_value=5, max_value=20,
            value=st.session_state.get("num_questions", 10),
        )

    generate = st.button("🎯  Generate Questions", use_container_width=False)

    if generate:
        skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        if not skills:
            st.warning("Please enter at least one skill.")
            return
        questions = generate_questions(skills, job_title, int(num_q))
        st.session_state.interview_questions = questions

    if "interview_questions" not in st.session_state:
        st.info("Enter your skills and click 'Generate Questions' to start practising.")
        return

    questions: list[InterviewQuestion] = st.session_state.interview_questions

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    col_f1, col_f2, _ = st.columns([1, 1, 2])
    with col_f1:
        filter_type = st.selectbox(
            "Filter by type",
            ["All"] + [t.value for t in QuestionType],
        )
    with col_f2:
        filter_diff = st.selectbox("Filter by difficulty", ["All", "Easy", "Medium", "Hard"])

    tech_count  = sum(1 for q in questions if q.type == QuestionType.TECHNICAL)
    behav_count = sum(1 for q in questions if q.type == QuestionType.BEHAVIOURAL)
    sit_count   = sum(1 for q in questions if q.type == QuestionType.SITUATIONAL)

    st.markdown(
        f'{badge(f"Technical: {tech_count}", "blue")} &nbsp;'
        f'{badge(f"Behavioural: {behav_count}", "green")} &nbsp;'
        f'{badge(f"Situational: {sit_count}", "orange")}',
        unsafe_allow_html=True,
    )
    st.markdown("")

    filtered = [
        q for q in questions
        if (filter_type == "All" or q.type.value == filter_type)
        and (filter_diff == "All" or q.difficulty == filter_diff)
    ]

    section_header(f"Question Bank ({len(filtered)} questions)")

    for i, q in enumerate(filtered, 1):
        type_color = _TYPE_COLORS.get(q.type, "blue")
        diff_color = _DIFFICULTY_COLORS.get(q.difficulty, "green")

        tip_html = (
            f'<div style="margin-top:.6rem;padding:.5rem .75rem;'
            f'background:var(--surface-2);border-radius:var(--radius-sm);'
            f'font-size:.8rem;color:var(--text-secondary);">'
            f'💡 <b>Tip:</b> {q.tip}</div>'
        ) if q.tip else ""

        skill_html = (
            f'<span style="font-size:.72rem;color:var(--text-muted);'
            f'font-family:DM Mono,monospace;">#{q.skill_tag}</span> &nbsp;'
        ) if q.skill_tag else ""

        st.markdown(
            f'<div class="question-card">'
            f'<div style="display:flex;align-items:center;gap:.4rem;margin-bottom:.4rem;">'
            f'<span style="font-size:.7rem;font-weight:600;color:var(--text-muted);">Q{i}</span>'
            f'&nbsp;{badge(q.type.value, type_color)}'
            f'&nbsp;{badge(q.difficulty, diff_color)}'
            f'&nbsp;{skill_html}'
            f'</div>'
            f'<div style="font-size:.95rem;line-height:1.5;">{q.question}</div>'
            f'{tip_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

    if not filtered:
        st.info("No questions match the selected filters.")
