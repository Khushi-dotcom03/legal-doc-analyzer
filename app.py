import streamlit as st
from agent import legal_doc_graph, answer_followup
from utils import extract_text_from_pdf
import tempfile
import os
import math

st.set_page_config(
    page_title="LexAI — Legal Document Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080b14 !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #1a2a4a 0%, #080b14 60%) !important;
}

/* Hide Streamlit chrome */
[data-testid="stToolbar"], footer, #MainMenu,
[data-testid="stDecoration"], [data-testid="collapsedControl"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { display: none !important; }

/* ── Main padding ── */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #2a3a5c; border-radius: 2px; }

/* ── Typography ── */
.lex-wordmark {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 22px;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.lex-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 300;
    color: #4a5568;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Navbar ── */
.lex-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 40px;
    border-bottom: 1px solid #1a2440;
    background: rgba(8, 11, 20, 0.8);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 100;
}

.lex-nav-right {
    display: flex;
    align-items: center;
    gap: 24px;
}

.lex-badge {
    background: linear-gradient(135deg, rgba(96,165,250,0.15), rgba(167,139,250,0.15));
    border: 1px solid rgba(96,165,250,0.3);
    color: #93c5fd;
    font-size: 11px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 100px;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.5px;
}

.lex-model-tag {
    color: #4a5568;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hero ── */
.lex-hero {
    text-align: center;
    padding: 72px 40px 52px;
}

.lex-hero-eyebrow {
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #60a5fa;
    margin-bottom: 20px;
    font-family: 'DM Sans', sans-serif;
}

.lex-hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    color: #f0f4ff;
    margin-bottom: 20px;
}

.lex-hero-title span {
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.lex-hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: #6b7a99;
    max-width: 520px;
    margin: 0 auto 40px;
    line-height: 1.7;
}

/* ── Upload Zone ── */
.lex-upload-wrapper {
    max-width: 560px;
    margin: 0 auto;
}

.lex-upload-zone {
    border: 1.5px dashed #2a3a5c;
    border-radius: 16px;
    padding: 40px 32px;
    text-align: center;
    background: linear-gradient(135deg, rgba(26,42,74,0.4), rgba(20,30,55,0.3));
    transition: border-color 0.2s;
    cursor: pointer;
}

.lex-upload-icon {
    font-size: 36px;
    margin-bottom: 12px;
    display: block;
}

.lex-upload-text {
    color: #6b7a99;
    font-size: 14px;
    font-weight: 300;
    line-height: 1.6;
}

.lex-upload-types {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
}

.lex-type-pill {
    background: rgba(96,165,250,0.1);
    border: 1px solid rgba(96,165,250,0.2);
    color: #60a5fa;
    font-size: 10px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 100px;
    letter-spacing: 0.5px;
    font-family: 'DM Sans', sans-serif;
}

/* ── File Info Card ── */
.lex-file-card {
    background: linear-gradient(135deg, rgba(26,42,74,0.6), rgba(20,30,55,0.5));
    border: 1px solid #2a3a5c;
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 16px;
}

.lex-file-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.lex-file-name {
    font-weight: 500;
    font-size: 14px;
    color: #e8eaf0;
}

.lex-file-size {
    font-size: 12px;
    color: #4a5568;
    font-weight: 300;
    margin-top: 2px;
}

/* ── Metrics Row ── */
.lex-metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    padding: 0 40px;
    margin-bottom: 32px;
}

.lex-metric-card {
    background: linear-gradient(135deg, rgba(26,42,74,0.5), rgba(15,20,40,0.6));
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}

.lex-metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, linear-gradient(90deg, #60a5fa, #a78bfa));
}

.lex-metric-label {
    font-size: 11px;
    font-weight: 400;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
    font-family: 'DM Sans', sans-serif;
}

.lex-metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #f0f4ff;
    line-height: 1;
}

.lex-metric-sub {
    font-size: 12px;
    color: #4a5568;
    margin-top: 6px;
    font-weight: 300;
}

/* ── Risk Score ── */
.lex-risk-ring {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.lex-risk-score-text {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
}

.lex-risk-label-text {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Content Grid ── */
.lex-content {
    padding: 0 40px 40px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.lex-content-full {
    padding: 0 40px 40px;
}

/* ── Section Cards ── */
.lex-card {
    background: linear-gradient(135deg, rgba(18,25,45,0.8), rgba(12,18,35,0.9));
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    overflow: hidden;
}

.lex-card-header {
    padding: 18px 24px;
    border-bottom: 1px solid #1a2440;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.lex-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #c8d0e8;
    letter-spacing: -0.2px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.lex-card-body {
    padding: 24px;
}

/* ── Summary text ── */
.lex-summary-text {
    font-size: 14px;
    line-height: 1.8;
    color: #8892aa;
    font-weight: 300;
}

/* ── Key Findings ── */
.lex-finding {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 0;
    border-bottom: 1px solid #111827;
}

.lex-finding:last-child { border-bottom: none; }

.lex-finding-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #60a5fa;
    margin-top: 6px;
    flex-shrink: 0;
}

.lex-finding-text {
    font-size: 13px;
    line-height: 1.6;
    color: #8892aa;
    font-weight: 300;
}

/* ── Clause Cards ── */
.lex-clause {
    background: linear-gradient(135deg, rgba(239,68,68,0.08), rgba(220,38,38,0.04));
    border: 1px solid rgba(239,68,68,0.2);
    border-left: 3px solid #ef4444;
    border-radius: 0 10px 10px 0;
    padding: 14px 16px;
    margin-bottom: 12px;
}

.lex-clause-header {
    font-size: 11px;
    font-weight: 500;
    color: #f87171;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.lex-clause-text {
    font-size: 13px;
    line-height: 1.6;
    color: #8892aa;
    font-weight: 300;
}

.lex-no-risk {
    background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(5,150,105,0.04));
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    color: #34d399;
    font-size: 14px;
}

/* ── Chat ── */
.lex-chat-container {
    max-height: 400px;
    overflow-y: auto;
    padding: 0 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.lex-chat-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #1d4ed8, #4f46e5);
    color: #e8eaf0;
    padding: 10px 16px;
    border-radius: 16px 16px 4px 16px;
    font-size: 13px;
    max-width: 75%;
    line-height: 1.5;
}

.lex-chat-ai {
    align-self: flex-start;
    background: rgba(26,42,74,0.6);
    border: 1px solid #1e2d4a;
    color: #8892aa;
    padding: 12px 16px;
    border-radius: 4px 16px 16px 16px;
    font-size: 13px;
    max-width: 85%;
    line-height: 1.7;
    font-weight: 300;
}

.lex-chat-ai-label {
    font-size: 10px;
    color: #60a5fa;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* ── Download Button ── */
.lex-dl-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(96,165,250,0.1);
    border: 1px solid rgba(96,165,250,0.25);
    color: #60a5fa;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    text-decoration: none;
    transition: background 0.2s;
}

/* ── Divider ── */
.lex-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2d4a, transparent);
    margin: 8px 0;
}

/* ── Section Label ── */
.lex-section-label {
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #2d3a55;
    padding: 0 40px;
    margin-bottom: 12px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Empty state ── */
.lex-empty {
    text-align: center;
    padding: 60px 40px;
    color: #2d3a55;
}

.lex-empty-icon { font-size: 48px; margin-bottom: 16px; }
.lex-empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: #2d3a55;
    margin-bottom: 8px;
}
.lex-empty-text { font-size: 14px; color: #1e2d4a; font-weight: 300; }

/* ── Override Streamlit widgets ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}

[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFileUploader"] button {
    display: none !important;
}

div[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(135deg, rgba(26,42,74,0.4), rgba(20,30,55,0.3)) !important;
    border: 1.5px dashed #2a3a5c !important;
    border-radius: 16px !important;
    color: #4a5568 !important;
}

div[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #60a5fa !important;
}

/* Streamlit buttons */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #4f46e5 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
    letter-spacing: 0.2px !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    border: none !important;
}

/* Download button */
.stDownloadButton > button {
    background: rgba(96,165,250,0.1) !important;
    border: 1px solid rgba(96,165,250,0.25) !important;
    color: #60a5fa !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: rgba(26,42,74,0.6) !important;
    border: 1px solid #2a3a5c !important;
    border-radius: 12px !important;
}

[data-testid="stChatInput"] textarea {
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    background: transparent !important;
}

/* Spinner */
[data-testid="stSpinner"] { color: #60a5fa !important; }

/* Alert / error */
[data-testid="stAlert"] {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    border-radius: 10px !important;
    color: #f87171 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: transparent !important;
}

/* Metric */
[data-testid="stMetric"] label { color: #4a5568 !important; font-size: 11px !important; }
[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f0f4ff !important; font-family: 'Syne', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# ── NAVBAR ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lex-nav">
    <div>
        <div class="lex-wordmark">LexAI</div>
        <div class="lex-tagline">Legal Intelligence Platform</div>
    </div>
    <div class="lex-nav-right">
        <span class="lex-model-tag">llama-3.1-8b · Groq</span>
        <span class="lex-badge">✦ Beta</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN CONTENT ───────────────────────────────────────────────────────────────

if not st.session_state.file_processed:
    # ── HERO + UPLOAD ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="lex-hero">
        <span class="lex-hero-eyebrow">✦ Powered by LangGraph + Groq</span>
        <div class="lex-hero-title">
            Understand any<br><span>legal document</span><br>in seconds
        </div>
        <div class="lex-hero-sub">
            Upload a contract, offer letter, or agreement and get an AI-powered plain-English summary,
            risk analysis, and an intelligent Q&amp;A assistant.
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, upload_col, _ = st.columns([1, 2, 1])
    with upload_col:
        st.markdown("""
        <div class="lex-upload-types" style="margin-bottom:12px">
            <span class="lex-type-pill">OFFER LETTERS</span>
            <span class="lex-type-pill">RENT AGREEMENTS</span>
            <span class="lex-type-pill">T&amp;C</span>
            <span class="lex-type-pill">NDAs</span>
            <span class="lex-type-pill">CONTRACTS</span>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your PDF here",
            type=["pdf"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            size_kb = uploaded_file.size / 1024
            st.markdown(f"""
            <div class="lex-file-card">
                <div class="lex-file-icon">📄</div>
                <div>
                    <div class="lex-file-name">{uploaded_file.name}</div>
                    <div class="lex-file-size">{size_kb:.1f} KB · PDF Document</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            if st.button("⚡  Analyze Document", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                with st.spinner("Running LangGraph pipeline — summarizing, flagging, indexing…"):
                    try:
                        raw_text = extract_text_from_pdf(tmp_path)
                        result = legal_doc_graph.invoke({
                            "raw_text": raw_text, "chunks": [],
                            "summary": "", "risky_clauses": [],
                            "question": "", "answer": "", "error": ""
                        })
                        st.session_state.analysis_result = result
                        st.session_state.file_processed = True
                        st.session_state.chat_history = []
                        st.session_state.doc_name = uploaded_file.name
                        st.session_state.doc_size = f"{size_kb:.1f} KB"
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
                    finally:
                        os.unlink(tmp_path)
                st.rerun()

        st.markdown("""
        <div style="text-align:center;margin-top:24px">
            <div style="font-size:11px;color:#2d3a55;font-family:'DM Sans',sans-serif;
                        letter-spacing:0.5px">
                Not legal advice · AI-assisted review only
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── DASHBOARD ──────────────────────────────────────────────────────────────
    result = st.session_state.analysis_result

    if result.get("error"):
        st.error(f"Pipeline error: {result['error']}")
        st.stop()

    clauses = result.get("risky_clauses", [])
    chunks  = result.get("risky_clauses", [])
    n_clauses = len(clauses)
    n_chunks  = len(result.get("chunks", []))
    n_qa      = len(st.session_state.chat_history)

    # Risk score: 0–100 based on clause count
    raw_score = min(n_clauses * 18, 95) if n_clauses else 5
    if raw_score < 25:
        risk_label, risk_color, risk_emoji = "Low", "#34d399", "🟢"
    elif raw_score < 55:
        risk_label, risk_color, risk_emoji = "Moderate", "#fbbf24", "🟡"
    else:
        risk_label, risk_color, risk_emoji = "High", "#f87171", "🔴"

    doc_name = st.session_state.get("doc_name", "Document")

    # ── Doc header bar ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="padding:16px 40px;border-bottom:1px solid #1a2440;
                display:flex;align-items:center;justify-content:space-between;
                background:rgba(8,11,20,0.6)">
        <div style="display:flex;align-items:center;gap:12px">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#1d4ed8,#7c3aed);
                        border-radius:8px;display:flex;align-items:center;justify-content:center;
                        font-size:16px">📄</div>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:600;
                            color:#e8eaf0">{doc_name}</div>
                <div style="font-size:11px;color:#4a5568;font-weight:300">
                    {st.session_state.get("doc_size","—")} · Analyzed just now
                </div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px">
            <div style="font-size:11px;color:{risk_color};background:rgba(96,165,250,0.08);
                        border:1px solid {risk_color}33;padding:4px 12px;border-radius:100px;
                        font-family:'DM Sans',sans-serif">
                {risk_emoji} {risk_label} Risk
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metrics row ────────────────────────────────────────────────────────────
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="lex-metric-card" style="--accent:linear-gradient(90deg,#60a5fa,#818cf8)">
            <div class="lex-metric-label">Risk Score</div>
            <div class="lex-metric-value" style="color:{risk_color}">{raw_score}</div>
            <div class="lex-metric-sub">{risk_label} · out of 100</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="lex-metric-card" style="--accent:linear-gradient(90deg,#f87171,#fb923c)">
            <div class="lex-metric-label">Flagged Clauses</div>
            <div class="lex-metric-value">{n_clauses}</div>
            <div class="lex-metric-sub">{'Requires review' if n_clauses else 'All clear'}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="lex-metric-card" style="--accent:linear-gradient(90deg,#a78bfa,#ec4899)">
            <div class="lex-metric-label">Sections Analyzed</div>
            <div class="lex-metric-value">{n_chunks}</div>
            <div class="lex-metric-sub">Document chunks</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="lex-metric-card" style="--accent:linear-gradient(90deg,#34d399,#60a5fa)">
            <div class="lex-metric-label">Q&amp;A Sessions</div>
            <div class="lex-metric-value">{n_qa}</div>
            <div class="lex-metric-sub">Questions answered</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Content area: Summary + Clauses ───────────────────────────────────────
    left_col, right_col = st.columns([3, 2], gap="medium")

    with left_col:
        # Summary card
        st.markdown("""
        <div class="lex-card">
            <div class="lex-card-header">
                <div class="lex-card-title">
                    <span style="color:#60a5fa">▸</span> Plain English Summary
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(18,25,45,0.8),rgba(12,18,35,0.9));
                        border:1px solid #1e2d4a;border-radius:0 0 16px 16px;
                        padding:24px;margin-top:-4px">
                <div style="font-size:14px;line-height:1.9;color:#8892aa;font-weight:300;
                            font-family:'DM Sans',sans-serif">
                    {result['summary'].replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                "⬇  Download Summary",
                data=result["summary"],
                file_name="lexai_summary.txt",
                mime="text/plain"
            )

    with right_col:
        # Risk clauses card
        st.markdown("""
        <div class="lex-card">
            <div class="lex-card-header">
                <div class="lex-card-title">
                    <span style="color:#f87171">▸</span> Risk Flags
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(18,25,45,0.8),rgba(12,18,35,0.9));
                    border:1px solid #1e2d4a;border-top:none;border-radius:0 0 16px 16px;
                    padding:16px;margin-top:-4px">
        """, unsafe_allow_html=True)

        if not clauses:
            st.markdown("""
            <div class="lex-no-risk">
                <div style="font-size:24px;margin-bottom:8px">✓</div>
                No significant risks detected
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, clause in enumerate(clauses, 1):
                parts = clause.split(":", 1)
                header = parts[0].strip() if len(parts) > 1 else f"Clause {i}"
                body   = parts[1].strip() if len(parts) > 1 else clause
                st.markdown(f"""
                <div class="lex-clause">
                    <div class="lex-clause-header">⚠ {header}</div>
                    <div class="lex-clause-text">{body}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Chat section ───────────────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="lex-card" style="margin:0 0 8px">
        <div class="lex-card-header">
            <div class="lex-card-title">
                <span style="color:#a78bfa">▸</span> Document Intelligence Chat
            </div>
            <div style="font-size:11px;color:#2d3a55">
                Contextual Q&amp;A · powered by LangGraph
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(f"<div style='font-size:13px;color:#e8eaf0'>{chat['question']}</div>",
                            unsafe_allow_html=True)
            with st.chat_message("assistant"):
                st.markdown(f"<div style='font-size:13px;color:#8892aa;line-height:1.7;font-weight:300'>{chat['answer']}</div>",
                            unsafe_allow_html=True)

    question = st.chat_input("Ask about clauses, obligations, deadlines, your rights…")
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner(""):
                answer = answer_followup(st.session_state.analysis_result, question)
            st.markdown(f"<div style='font-size:13px;color:#8892aa;line-height:1.7;font-weight:300'>{answer}</div>",
                        unsafe_allow_html=True)
        st.session_state.chat_history.append({"question": question, "answer": answer})

    # ── New analysis button ────────────────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3, 1, 3])
    with btn_col:
        if st.button("↩  New Document", use_container_width=True):
            st.session_state.file_processed = False
            st.session_state.analysis_result = None
            st.session_state.chat_history = []
            st.rerun()