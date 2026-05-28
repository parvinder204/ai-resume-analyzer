import streamlit as st


_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;0,9..144,700;1,9..144,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:          #F7F5F0;
    --surface:     #FFFFFF;
    --surface-2:   #F0EDE6;
    --border:      #E2DDD4;
    --accent:      #1A6B55;       
    --accent-2:    #E8572A;      
    --accent-3:    #4A3F8A;       
    --text-primary:   #1C1C1C;
    --text-secondary: #6B6560;
    --text-muted:     #9E9890;
    --success:     #2D7D5A;
    --warning:     #C47A1E;
    --danger:      #C0392B;
    --radius-sm:   6px;
    --radius:      12px;
    --radius-lg:   20px;
    --shadow-sm:   0 1px 3px rgba(0,0,0,.07);
    --shadow:      0 4px 16px rgba(0,0,0,.08);
    --shadow-lg:   0 12px 40px rgba(0,0,0,.12);
    --transition:  all .2s cubic-bezier(.4,0,.2,1);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    letter-spacing: -0.02em;
}

[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    box-shadow: var(--shadow-sm);
}

[data-testid="stMetric"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: .78rem !important;
    font-weight: 500 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Fraunces', serif !important;
    font-size: 2rem !important;
    color: var(--text-primary) !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: .55rem 1.4rem !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button:hover {
    background: #155743 !important;
    box-shadow: var(--shadow) !important;
    transform: translateY(-1px);
}

[data-testid="stFileUploader"] {
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    transition: var(--transition) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

.stProgress > div > div {
    background: var(--accent) !important;
}

[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
}

.stSelectbox [data-baseweb="select"] > div,
.stTextInput > div > div {
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
}

.card-accent {
    border-left: 3px solid var(--accent);
}

.badge {
    display: inline-block;
    padding: .2rem .65rem;
    border-radius: 999px;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .04em;
    text-transform: uppercase;
}

.badge-green  { background: #E0F2EA; color: var(--success); }
.badge-orange { background: #FEF0E3; color: var(--warning); }
.badge-red    { background: #FDE8E6; color: var(--danger);  }
.badge-blue   { background: #E8F0FE; color: var(--accent-3); }

.skill-chip {
    display: inline-block;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: .25rem .8rem;
    font-size: .8rem;
    font-family: 'DM Mono', monospace;
    margin: .2rem;
    color: var(--text-primary);
    transition: var(--transition);
}

.skill-chip.matched   { background: #E0F2EA; border-color: #A8D8C0; color: var(--success); }
.skill-chip.missing   { background: #FDE8E6; border-color: #F5BBBB; color: var(--danger);  }
.skill-chip.suggested { background: #FEF0E3; border-color: #F5D5A8; color: var(--warning); }

.section-header {
    font-family: 'Fraunces', serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: .25rem;
}

.section-sub {
    font-size: .85rem;
    color: var(--text-secondary);
    margin-bottom: 1.25rem;
}

.hero-score {
    font-family: 'Fraunces', serif;
    font-size: 4rem;
    font-weight: 700;
    line-height: 1;
}

.score-ring-wrap { text-align: center; padding: 1rem; }

.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: .6rem;
    padding: .55rem .85rem;
    border-radius: var(--radius-sm);
    cursor: pointer;
    font-size: .88rem;
    font-weight: 500;
    color: var(--text-secondary);
    margin-bottom: .2rem;
    transition: var(--transition);
    text-decoration: none;
}
.nav-item:hover, .nav-item.active {
    background: #E0F2EA;
    color: var(--accent);
}

.logo-text {
    font-family: 'Fraunces', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -.03em;
}

.question-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: .75rem;
}

.question-tag {
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: .35rem;
}

.rank-badge {
    width: 2rem; height: 2rem;
    background: var(--accent);
    color: #fff;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Fraunces', serif;
    font-size: 1rem;
    font-weight: 700;
    flex-shrink: 0;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Hide Streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
"""


def inject_global_styles() -> None:
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def card(content_html: str, accent: bool = False) -> None:
    cls = "card card-accent" if accent else "card"
    st.markdown(f'<div class="{cls}">{content_html}</div>', unsafe_allow_html=True)


def badge(text: str, variant: str = "green") -> str:
    return f'<span class="badge badge-{variant}">{text}</span>'


def skill_chip(name: str, variant: str = "") -> str:
    return f'<span class="skill-chip {variant}">{name}</span>'


def section_header(title: str, subtitle: str = "") -> None:
    sub = f'<p class="section-sub">{subtitle}</p>' if subtitle else ""
    st.markdown(f'<p class="section-header">{title}</p>{sub}', unsafe_allow_html=True)
