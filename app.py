import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EXPLAINIFY",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ───────── GLOBAL ───────── */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #ffffff;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(0,255,255,0.12), transparent 25%),
        radial-gradient(circle at bottom right, rgba(123,92,255,0.18), transparent 30%),
        linear-gradient(135deg, #050816 0%, #0b1220 45%, #111827 100%);
    overflow-x: hidden;
}

/* animated background glow */

.stApp::before {
    content: '';
    position: fixed;
    width: 700px;
    height: 700px;
    top: -250px;
    left: -250px;
    background: rgba(0,255,255,0.08);
    border-radius: 50%;
    filter: blur(120px);
    animation: glowMove 10s infinite alternate;
    z-index: 0;
}

@keyframes glowMove {
    from {
        transform: translate(0px,0px) scale(1);
    }
    to {
        transform: translate(100px,50px) scale(1.2);
    }
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    max-width: 1400px;
    padding: 2rem 3rem 4rem;
    position: relative;
    z-index: 1;
}

/* ───────── HERO ───────── */

.hero {
    text-align: center;
    padding: 4rem 0 3rem;
}

.hero-eyebrow {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    color: #00f5ff;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(3rem, 7vw, 6rem);
    font-weight: 700;
    line-height: 1;
    margin-bottom: 1rem;
    letter-spacing: -0.04em;

    background: linear-gradient(
        90deg,
        #ffffff,
        #00f5ff,
        #7b5cff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    max-width: 720px;
    margin: auto;
    font-size: 1.05rem;
    line-height: 1.9;
    color: rgba(255,255,255,0.72);
}

/* ───────── DIVIDER ───────── */

.divider {
    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(0,245,255,0.45),
        transparent
    );

    margin: 2rem 0;
}

/* ───────── GLASS PANELS ───────── */

.input-card,
.step-card,
.result-panel,
.report-panel,
.feedback-panel {

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03),
        0 8px 40px rgba(0,0,0,0.35);
}

/* ───────── INPUT CARD ───────── */

.input-card {
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
}

/* ───────── INPUT ───────── */

.stTextInput > div > div > input {

    background: rgba(255,255,255,0.04) !important;

    border: 1px solid rgba(0,245,255,0.2) !important;

    border-radius: 14px !important;

    color: white !important;

    padding: 1rem !important;

    font-size: 1rem !important;

    transition: all 0.25s ease !important;
}

.stTextInput > div > div > input:focus {

    border-color: #00f5ff !important;

    box-shadow: 0 0 25px rgba(0,245,255,0.25) !important;
}

.stTextInput > label {

    font-family: 'Orbitron', sans-serif !important;

    color: #00f5ff !important;

    font-size: 0.72rem !important;

    letter-spacing: 0.18em !important;

    text-transform: uppercase !important;
}

/* ───────── BUTTON ───────── */

.stButton > button {

    background: linear-gradient(
        135deg,
        #00f5ff,
        #7b5cff
    ) !important;

    color: #071018 !important;

    border: none !important;

    border-radius: 14px !important;

    padding: 0.9rem 1rem !important;

    font-weight: 700 !important;

    font-size: 1rem !important;

    width: 100%;

    transition: all 0.25s ease !important;

    box-shadow:
        0 0 25px rgba(0,245,255,0.25),
        0 0 60px rgba(123,92,255,0.18);
}

.stButton > button:hover {

    transform: translateY(-3px) scale(1.01);

    box-shadow:
        0 0 35px rgba(0,245,255,0.45),
        0 0 90px rgba(123,92,255,0.28);
}

/* ───────── STEP CARDS ───────── */

.step-card {

    border-radius: 20px;

    padding: 1.5rem;

    margin-bottom: 1rem;

    transition: all 0.25s ease;

    position: relative;

    overflow: hidden;
}

.step-card:hover {
    transform: translateY(-4px);
}

.step-card::before {

    content: '';

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 4px;

    background: rgba(255,255,255,0.08);
}

.step-card.active::before {
    background: #00f5ff;
}

.step-card.done::before {
    background: #00ff88;
}

.step-card.active {

    border-color: rgba(0,245,255,0.4);

    box-shadow: 0 0 25px rgba(0,245,255,0.15);
}

.step-card.done {
    border-color: rgba(0,255,136,0.3);
}

/* ───────── STEP HEADER ───────── */

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.step-num,
.step-status {
    font-family: 'Orbitron', sans-serif;
}

.step-num {
    color: #00f5ff;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
}

.step-title {
    font-size: 1rem;
    font-weight: 700;
    color: white;
}

.status-running {
    color: #00f5ff;
}

.status-done {
    color: #00ff88;
}

/* ───────── RESULTS ───────── */

.result-panel,
.report-panel,
.feedback-panel {

    border-radius: 24px;

    padding: 2rem;

    margin-top: 1rem;
}

.result-panel-title,
.panel-label {

    font-family: 'Orbitron', sans-serif;

    text-transform: uppercase;

    letter-spacing: 0.2em;

    font-size: 0.72rem;

    margin-bottom: 1rem;
}

.result-panel-title,
.panel-label.orange {
    color: #00f5ff;
}

.panel-label.green {
    color: #00ff88;
}

.result-content {

    line-height: 1.9;

    color: rgba(255,255,255,0.8);

    font-size: 0.96rem;
}

/* ───────── EXPANDERS ───────── */

details {

    background: rgba(255,255,255,0.03);

    border-radius: 16px;

    padding: 0.7rem 1rem;

    border: 1px solid rgba(255,255,255,0.06);
}

details summary {

    color: #b7c2ff !important;

    font-family: 'Orbitron', sans-serif !important;
}

/* ───────── SECTION HEADINGS ───────── */

.section-heading {

    font-family: 'Orbitron', sans-serif;

    font-size: 1.5rem;

    font-weight: 700;

    color: white;

    margin-bottom: 1.5rem;
}

/* ───────── SCROLLBAR ───────── */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #0b1220;
}

::-webkit-scrollbar-thumb {

    background: linear-gradient(
        #00f5ff,
        #7b5cff
    );

    border-radius: 20px;
}

/* ───────── FOOTER ───────── */

.notice {

    text-align: center;

    margin-top: 4rem;

    color: rgba(255,255,255,0.35);

    font-size: 0.72rem;

    letter-spacing: 0.15em;

    font-family: 'Orbitron', sans-serif;
}

</style>
""", unsafe_allow_html=True)

# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>EXPLAINIFY</h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Next Generation AI Systems",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["AI Agents & Autonomous Systems in 2026",
                "Multimodal Generative AI & Real-Time Reasoning", " Open Source LLMs vs Closed AI Models"]
    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;
            padding:0.25rem 0.7rem;
            font-size:0.75rem;
            color:#a09890;
            font-family:'DM Sans',sans-serif;
            cursor:default;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>',
                unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"),
              "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"),
              "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"),
              "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"),
              "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                          f"Based on the following search results about '{topic_val}', "
                          f"pick the most relevant URL and scrape it for deeper content.\n\n"
                          f"Search Results:\n{results['search'][:800]}"
                          )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search'][:1000]}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader'][:1500]}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>',
                unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
   EXPLAINIFY · AI Research Engine · Powered by Multi-Agent Intelligence
</div>
""", unsafe_allow_html=True)
