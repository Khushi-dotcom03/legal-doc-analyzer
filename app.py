"""
ClauseGuard AI — Corporate Legal-Tech Platform
UI/UX Redesign: Enterprise Edition

Design philosophy:
- Deep navy + legal gold = trustworthy premium feel
- Risk meter as signature element (unique, immediately valuable)
- Card-based information architecture with clear visual hierarchy
- Streamlit-native: no fragile hacks, fully maintainable
"""

import streamlit as st
import time
import random

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ClauseGuard AI · Legal Intelligence Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — CORPORATE LEGAL-TECH THEME
# ─────────────────────────────────────────────
CORPORATE_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── CSS Variables ── */
:root {
    --navy:       #0F1C2E;
    --navy-mid:   #1A3A5C;
    --navy-light: #243E60;
    --gold:       #C8A96E;
    --gold-light: #E8C98A;
    --bg:         #F0F4F8;
    --bg-card:    #FFFFFF;
    --text-primary:   #0F1C2E;
    --text-secondary: #4A6080;
    --text-muted:     #8A9BB0;
    --risk-red:    #DC2626;
    --risk-amber:  #D97706;
    --risk-green:  #059669;
    --risk-red-bg: #FEF2F2;
    --risk-amber-bg: #FFFBEB;
    --risk-green-bg: #ECFDF5;
    --border:      #DDE4EE;
    --shadow-sm:   0 1px 3px rgba(15,28,46,0.08);
    --shadow-md:   0 4px 12px rgba(15,28,46,0.10);
    --shadow-lg:   0 8px 24px rgba(15,28,46,0.12);
    --radius:      10px;
    --radius-lg:   16px;
}

/* ── Global Reset ── */
* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: 1px solid var(--navy-mid);
}
[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FFFFFF !important;
}

/* ── Top header bar ── */
.cg-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%);
    padding: 18px 28px;
    border-radius: var(--radius-lg);
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-md);
}
.cg-header-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}
.cg-header-logo {
    font-size: 28px;
    line-height: 1;
}
.cg-header-title {
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.3px;
}
.cg-header-subtitle {
    font-size: 12px;
    color: var(--gold);
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-top: 2px;
}
.cg-header-badge {
    background: rgba(200,169,110,0.15);
    border: 1px solid rgba(200,169,110,0.4);
    color: var(--gold-light);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ── Upload zone ── */
.cg-upload-zone {
    background: var(--bg-card);
    border: 2px dashed var(--border);
    border-radius: var(--radius-lg);
    padding: 48px 32px;
    text-align: center;
    transition: border-color 0.2s;
    margin-bottom: 24px;
}
.cg-upload-zone:hover { border-color: var(--navy-mid); }
.cg-upload-icon { font-size: 48px; margin-bottom: 16px; }
.cg-upload-title {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.cg-upload-sub {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 20px;
}
.cg-supported {
    display: inline-flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 16px;
}
.cg-tag {
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
}

/* ── Risk Meter (SIGNATURE ELEMENT) ── */
.cg-risk-meter-wrap {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
}
.cg-risk-meter-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 18px;
}
.cg-risk-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
}
.cg-risk-score-display {
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.cg-risk-verdict {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.risk-low    { background: var(--risk-green-bg); color: var(--risk-green); }
.risk-medium { background: var(--risk-amber-bg); color: var(--risk-amber); }
.risk-high   { background: var(--risk-red-bg);   color: var(--risk-red);   }

.cg-gauge-track {
    height: 10px;
    border-radius: 5px;
    background: linear-gradient(to right, #059669 0%, #10B981 25%, #F59E0B 50%, #D97706 70%, #DC2626 100%);
    position: relative;
    margin-bottom: 8px;
}
.cg-gauge-needle {
    position: absolute;
    top: -4px;
    width: 18px;
    height: 18px;
    background: var(--navy);
    border: 3px solid white;
    border-radius: 50%;
    transform: translateX(-50%);
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    transition: left 0.8s cubic-bezier(0.34,1.56,0.64,1);
}
.cg-gauge-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 500;
    margin-top: 4px;
}

/* ── Stat cards row ── */
.cg-stat-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.cg-stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 20px;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}
.cg-stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--gold);
}
.cg-stat-icon { font-size: 20px; margin-bottom: 10px; }
.cg-stat-value {
    font-size: 26px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 4px;
}
.cg-stat-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 500;
}

/* ── Section cards ── */
.cg-section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
}
.cg-section-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 6px;
}
.cg-section-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.cg-section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 16px 0;
}
.cg-prose {
    font-size: 14px;
    line-height: 1.75;
    color: #334155;
}

/* ── Obligation / right items ── */
.cg-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
}
.cg-item:last-child { border-bottom: none; }
.cg-item-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-top: 6px;
    flex-shrink: 0;
}
.dot-obligation { background: var(--navy-mid); }
.dot-right      { background: var(--risk-green); }
.dot-deadline   { background: var(--gold); }
.cg-item-text {
    font-size: 14px;
    color: #334155;
    line-height: 1.6;
    flex: 1;
}
.cg-item-badge {
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
    white-space: nowrap;
    flex-shrink: 0;
    margin-top: 2px;
}
.badge-you    { background: #EFF6FF; color: #1D4ED8; }
.badge-them   { background: #F0FDF4; color: #15803D; }
.badge-mutual { background: #F5F3FF; color: #7C3AED; }

/* ── Risk clause cards ── */
.cg-risk-clause {
    border-left: 4px solid var(--risk-red);
    background: var(--risk-red-bg);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 14px 18px;
    margin-bottom: 12px;
}
.cg-risk-clause.medium {
    border-left-color: var(--risk-amber);
    background: var(--risk-amber-bg);
}
.cg-risk-clause-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.cg-risk-clause-name {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
}
.cg-risk-severity {
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.sev-high   { background: var(--risk-red);   color: white; }
.sev-medium { background: var(--risk-amber); color: white; }
.cg-risk-clause-text {
    font-size: 13px;
    color: #374151;
    line-height: 1.6;
}
.cg-risk-clause-why {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 8px;
    font-style: italic;
}

/* ── Date / deadline cards ── */
.cg-date-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid var(--border);
}
.cg-date-item:last-child { border-bottom: none; }
.cg-date-icon-wrap {
    background: var(--navy);
    color: var(--gold);
    width: 42px; height: 42px;
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.cg-date-info-label {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
}
.cg-date-info-value {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}

/* ── Chat bubbles ── */
.cg-chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 20px;
}
.cg-bubble {
    max-width: 82%;
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.6;
}
.cg-bubble-user {
    background: var(--navy);
    color: #E2E8F0;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
}
.cg-bubble-ai {
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: #334155;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
}
.cg-bubble-ai-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* ── Download button ── */
.cg-download-btn {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%);
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: var(--radius);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: opacity 0.2s;
    width: 100%;
    justify-content: center;
    margin-top: 8px;
}

/* ── Processing state ── */
.cg-processing {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 48px 32px;
    text-align: center;
    box-shadow: var(--shadow-sm);
}
.cg-processing-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.cg-processing-sub {
    font-size: 14px;
    color: var(--text-secondary);
}
.cg-step-list {
    list-style: none;
    padding: 0;
    margin: 24px 0 0;
    text-align: left;
    max-width: 340px;
    margin-left: auto;
    margin-right: auto;
}
.cg-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    font-size: 13px;
    color: var(--text-secondary);
}
.cg-step.done  { color: var(--risk-green); }
.cg-step.active { color: var(--text-primary); font-weight: 600; }
.cg-step-dot {
    width: 20px; height: 20px;
    border-radius: 50%;
    background: var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 11px;
    flex-shrink: 0;
}
.cg-step.done  .cg-step-dot { background: var(--risk-green); color: white; }
.cg-step.active .cg-step-dot { background: var(--navy); color: white; }

/* ── Sidebar doc info ── */
.cg-sidebar-section {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: var(--radius);
    padding: 14px 16px;
    margin-bottom: 16px;
}
.cg-sidebar-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: rgba(200,169,110,0.9) !important;
    margin-bottom: 10px;
}
.cg-sidebar-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 12px;
}
.cg-sidebar-row:last-child { border-bottom: none; }
.cg-sidebar-key { color: rgba(203,213,225,0.7) !important; }
.cg-sidebar-val { color: #FFFFFF !important; font-weight: 600; }

/* ── Status pill ── */
.cg-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(5,150,105,0.15);
    border: 1px solid rgba(5,150,105,0.3);
    color: #34D399;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 8px;
}
.cg-status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #34D399;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ── Streamlit widget overrides ── */
.stButton > button {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.9 !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    background: var(--bg-card) !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--navy-mid) !important;
    box-shadow: 0 0 0 3px rgba(26,58,92,0.08) !important;
}

[data-testid="stFileUploader"] {
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius-lg) !important;
    background: var(--bg-card) !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--navy-mid), var(--gold)) !important;
    border-radius: 10px !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
    border-bottom: 2px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: var(--radius) var(--radius) 0 0 !important;
    padding: 10px 18px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
    border-bottom: 2px solid var(--navy) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 20px 0 !important; }
</style>
"""

# ─────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": "upload",       # upload | processing | results
        "filename": None,
        "analysis": None,
        "chat_history": [],
        "processing_step": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
st.markdown(CORPORATE_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MOCK DATA — replace with your actual AI pipeline
# ─────────────────────────────────────────────
MOCK_ANALYSIS = {
    "doc_type": "Employment Offer Letter",
    "pages": 8,
    "word_count": "3,412",
    "clauses": 24,
    "risk_score": 68,   # 0–100
    "risk_level": "medium",
    "risk_verdict": "Review Recommended",
    "summary": (
        "This employment agreement is a standard fixed-term offer letter from Nexus Technologies Ltd "
        "for a Senior Software Engineer position. The document grants standard employment rights "
        "including paid leave and health benefits, but contains several clauses that significantly "
        "restrict the employee's post-employment activities. The non-compete clause is unusually broad "
        "in its geographic and temporal scope. Intellectual property assignment provisions are expansive "
        "and may cover personal projects developed outside working hours. Overall the agreement is "
        "enforceable but warrants legal review before signing."
    ),
    "obligations": [
        {"text": "Maintain confidentiality of all company information indefinitely, including after termination.", "party": "you"},
        {"text": "Assign all intellectual property created during employment — including work done on personal time using personal equipment.", "party": "you"},
        {"text": "Provide 90 days written notice before resignation; failure incurs salary clawback.", "party": "you"},
        {"text": "Abide by a 24-month non-compete restriction covering the entire APAC region.", "party": "you"},
        {"text": "Provide annual performance reviews and notify of role changes within 30 days.", "party": "them"},
        {"text": "Pay base salary of ₹28,00,000 per annum plus performance bonus of up to 20%.", "party": "them"},
        {"text": "Provide health insurance for employee and immediate family members.", "party": "them"},
        {"text": "Both parties agree to resolve disputes via binding arbitration in Singapore.", "party": "mutual"},
    ],
    "risks": [
        {
            "name": "Overly Broad Non-Compete",
            "severity": "high",
            "text": "Employee agrees not to directly or indirectly engage in any competing business activity within the APAC region for a period of twenty-four (24) months following termination.",
            "why": "A 24-month APAC-wide non-compete is exceptionally broad and may be unenforceable, but agreeing to it creates negotiating risk.",
        },
        {
            "name": "IP Assignment on Personal Projects",
            "severity": "high",
            "text": "All inventions, discoveries, and creative works produced during the term of employment — regardless of where developed or resources used — shall be the sole property of the Company.",
            "why": "\"Regardless of resources used\" means personal side projects could be claimed by the company.",
        },
        {
            "name": "Unilateral Contract Modification",
            "severity": "medium",
            "text": "The Company reserves the right to amend the terms of this agreement with 14 days written notice to the employee.",
            "why": "One-sided modification rights allow the company to change your terms with minimal notice.",
        },
        {
            "name": "Salary Clawback on Early Exit",
            "severity": "medium",
            "text": "Failure to provide the required 90-day notice period will result in forfeiture of the final month's salary and any accrued bonuses.",
            "why": "Bonus clawback on notice breach is aggressive; ensure you understand the financial exposure.",
        },
    ],
    "dates": [
        {"icon": "+", "label": "Start Date", "value": "15 August 2026"},
        {"icon": "+", "label": "Probation Period", "value": "6 months (ends 15 Feb 2027)"},
        {"icon": "+", "label": "Notice Period (Employee)", "value": "90 days written notice"},
        {"icon": "+", "label": "Non-Compete Duration", "value": "24 months post-termination"},
        {"icon": "+", "label": "Contract Renewal Review", "value": "Annually in December"},
    ],
}

MOCK_CHAT = [
    {
        "role": "ai",
        "text": "I've finished analysing your document. I'm ready to answer specific questions about the clauses, obligations, or any terms you'd like clarified. What would you like to know?",
    }
]


# ─────────────────────────────────────────────
#  HELPER: Risk score → gauge needle position
# ─────────────────────────────────────────────
def risk_meter_html(score: int, level: str, verdict: str) -> str:
    pct = min(max(score, 0), 100)
    needle_left = pct  # percentage across gauge

    verdict_class = f"risk-{level}"

    return f"""
    <div class="cg-risk-meter-wrap">
        <div class="cg-risk-meter-header">
            <div>
                <div class="cg-risk-label">Overall Risk Assessment</div>
                <div class="cg-risk-score-display">{score}<span style="font-size:18px;font-weight:400;color:var(--text-muted)">/100</span></div>
            </div>
            <span class="cg-risk-verdict {verdict_class}">{verdict}</span>
        </div>
        <div class="cg-gauge-track">
            <div class="cg-gauge-needle" style="left:{needle_left}%"></div>
        </div>
        <div class="cg-gauge-labels">
            <span>Low Risk</span>
            <span>Moderate</span>
            <span>High Risk</span>
        </div>
    </div>
    """


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Brand mark
    st.markdown("""
    <div style="padding: 8px 0 20px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <span style="font-size:24px;">⚖️</span>
            <span style="font-size:17px;font-weight:700;color:#FFFFFF;">ClauseGuard AI</span>
        </div>
        <div style="font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(200,169,110,0.9);">
            Legal Intelligence Platform
        </div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.1);margin:0 0 20px;">
    """, unsafe_allow_html=True)

    if st.session_state.stage == "results" and st.session_state.analysis:
        a = st.session_state.analysis

        # Status
        st.markdown("""
        <div style="margin-bottom:20px;">
            <span class="cg-status-pill">
                <span class="cg-status-dot"></span> Analysis Complete
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Document info card
        st.markdown(f"""
        <div class="cg-sidebar-section">
            <div class="cg-sidebar-label"> Document</div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">Type</span>
                <span class="cg-sidebar-val">{a['doc_type']}</span>
            </div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">File</span>
                <span class="cg-sidebar-val">{st.session_state.filename or 'document.pdf'}</span>
            </div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">Pages</span>
                <span class="cg-sidebar-val">{a['pages']}</span>
            </div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">Words</span>
                <span class="cg-sidebar-val">{a['word_count']}</span>
            </div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">Clauses</span>
                <span class="cg-sidebar-val">{a['clauses']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk summary
        risk_color = {"low": "#34D399", "medium": "#F59E0B", "high": "#F87171"}[a["risk_level"]]
        st.markdown(f"""
        <div class="cg-sidebar-section">
            <div class="cg-sidebar-label"> Risk Overview</div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">Score</span>
                <span class="cg-sidebar-val" style="color:{risk_color}!important">{a['risk_score']}/100</span>
            </div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">Level</span>
                <span class="cg-sidebar-val" style="color:{risk_color}!important">{a['risk_level'].title()}</span>
            </div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">High risks</span>
                <span class="cg-sidebar-val">{sum(1 for r in a['risks'] if r['severity']=='high')}</span>
            </div>
            <div class="cg-sidebar-row">
                <span class="cg-sidebar-key">Med. risks</span>
                <span class="cg-sidebar-val">{sum(1 for r in a['risks'] if r['severity']=='medium')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇  Download Full Report",
            data=f"ClauseGuard AI — Analysis Report\n\nDocument: {st.session_state.filename}\nRisk Score: {a['risk_score']}/100\n\nSummary:\n{a['summary']}",
            file_name="clauseguard_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("  Analyse New Document", use_container_width=True):
            st.session_state.stage = "upload"
            st.session_state.analysis = None
            st.session_state.chat_history = []
            st.session_state.filename = None
            st.rerun()

    else:
        st.markdown("""
        <div class="cg-sidebar-section">
            <div class="cg-sidebar-label">How it works</div>
        </div>
        """, unsafe_allow_html=True)

        steps = [
            ("-", "Upload your legal document"),
            ("-", "AI extracts and chunks text"),
            ("-", "Groq LLM analyses clauses"),
            ("-", "Risk clauses are flagged"),
            ("-", "Ask follow-up questions"),
        ]
        for icon, text in steps:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
                <span style="font-size:15px;margin-top:1px;">{icon}</span>
                <span style="font-size:12px;color:rgba(203,213,225,0.85);">{text}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""<br>
        <div style="font-size:10px;color:rgba(203,213,225,0.4);text-align:center;padding-top:8px;">
            Supported formats: PDF<br>
            Powered by Groq LLM + LangGraph
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN AREA — HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="cg-header">
    <div class="cg-header-brand">
        <span class="cg-header-logo">⚖️</span>
        <div>
            <div class="cg-header-title">ClauseGuard AI</div>
            <div class="cg-header-subtitle">Legal Intelligence Platform</div>
        </div>
    </div>
    <span class="cg-header-badge">✦ AI-POWERED</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  STAGE: UPLOAD
# ─────────────────────────────────────────────
if st.session_state.stage == "upload":

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown("""
        <div class="cg-section-card">
            <div class="cg-section-eyebrow">Get Started</div>
            <div class="cg-section-title">⬆ Upload Your Legal Document</div>
            <p class="cg-prose">
                ClauseGuard AI reviews your legal documents in seconds, surfacing hidden risks,
                key obligations, and critical deadlines — in plain English.
            </p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            label="Drop your PDF here or click to browse",
            type=["pdf"],
            help="Supported: Employment contracts, NDAs, Rental agreements, T&Cs, Service agreements",
            label_visibility="collapsed",
        )

        if uploaded_file:
            st.markdown(f"""
            <div style="background:#F0FDF4;border:1.5px solid #BBF7D0;border-radius:10px;
                        padding:14px 18px;display:flex;align-items:center;gap:12px;margin-top:12px;">
                <span style="font-size:22px;"></span>
                <div>
                    <div style="font-size:13px;font-weight:700;color:#15803D;">{uploaded_file.name}</div>
                    <div style="font-size:11px;color:#16A34A;">{uploaded_file.size / 1024:.1f} KB · PDF</div>
                </div>
                <span style="margin-left:auto;font-size:18px;">✅</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("  Analyse Document", use_container_width=True):
                st.session_state.filename = uploaded_file.name
                st.session_state.stage = "processing"
                st.session_state.processing_step = 0
                st.rerun()

    with col_right:
        st.markdown("""
        <div class="cg-section-card">
            <div class="cg-section-eyebrow">What We Detect</div>
            <div class="cg-section-title">🛡 Document Intelligence</div>
        """, unsafe_allow_html=True)

        features = [
            ("🛡", "Risk Clauses", "Identifies clauses that may disadvantage you"),
            ("🛡", "Key Obligations", "Separates your duties from theirs"),
            ("🛡", "Critical Dates", "Deadlines, notice periods, renewals"),
            ("🛡", "Plain Summary", "Legal jargon explained simply"),
            ("🛡", "AI Chat", "Ask follow-up questions instantly"),
        ]
        for icon, title, desc in features:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:14px;padding:12px 0;
                        border-bottom:1px solid var(--border);">
                <div style="width:36px;height:36px;background:#F0F4F8;border-radius:8px;
                            display:flex;align-items:center;justify-content:center;
                            font-size:16px;flex-shrink:0;">{icon}</div>
                <div>
                    <div style="font-size:13px;font-weight:700;color:#0F1C2E;">{title}</div>
                    <div style="font-size:12px;color:#64748B;margin-top:2px;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:11px;color:var(--text-muted);margin-top:16px;padding:12px;
                    background:var(--bg);border-radius:8px;line-height:1.6;">
             Analysis typically completes in under 30 seconds.<br>
             Your document is processed securely and never stored.
        </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  STAGE: PROCESSING
# ─────────────────────────────────────────────
elif st.session_state.stage == "processing":

    processing_steps = [
        "Extracting text from PDF",
        "Chunking document sections",
        "Sending to Groq LLM",
        "Analysing obligations and rights",
        "Detecting risk clauses",
        "Generating executive summary",
        "Finalising report",
    ]

    step = st.session_state.processing_step

    # Build step list HTML
    step_items_html = ""
    for i, s in enumerate(processing_steps):
        if i < step:
            cls = "done"
            dot_content = "✓"
        elif i == step:
            cls = "active"
            dot_content = "●"
        else:
            cls = ""
            dot_content = str(i + 1)
        step_items_html += f"""
        <li class="cg-step {cls}">
            <div class="cg-step-dot">{dot_content}</div>
            {s}
        </li>"""

    progress_pct = int((step / len(processing_steps)) * 100)

    st.markdown(f"""
    <div class="cg-processing">
        <div style="font-size:48px;margin-bottom:16px;">🔍</div>
        <div class="cg-processing-title">Analysing Your Document</div>
        <div class="cg-processing-sub">
            {st.session_state.filename or 'document.pdf'} · Powered by Groq LLM
        </div>
        <ul class="cg-step-list">{step_items_html}</ul>
    </div>
    """, unsafe_allow_html=True)

    progress_bar = st.progress(progress_pct)

    # Advance steps
    if step < len(processing_steps):
        time.sleep(0.55)
        st.session_state.processing_step += 1
        st.rerun()
    else:
        # Done — load mock analysis (replace with your actual pipeline call)
        st.session_state.analysis = MOCK_ANALYSIS
        st.session_state.chat_history = list(MOCK_CHAT)
        st.session_state.stage = "results"
        st.rerun()


# ─────────────────────────────────────────────
#  STAGE: RESULTS
# ─────────────────────────────────────────────
elif st.session_state.stage == "results":
    a = st.session_state.analysis

    # ── Risk Meter (signature element) ──
    st.markdown(risk_meter_html(a["risk_score"], a["risk_level"], a["risk_verdict"]),
                unsafe_allow_html=True)

    # ── Stat cards ──
    high_risks  = sum(1 for r in a["risks"] if r["severity"] == "high")
    med_risks   = sum(1 for r in a["risks"] if r["severity"] == "medium")
    obligations = sum(1 for o in a["obligations"] if o["party"] == "you")

    st.markdown(f"""
    <div class="cg-stat-row">
        <div class="cg-stat-card">
            <div class="cg-stat-icon"></div>
            <div class="cg-stat-value">{a['clauses']}</div>
            <div class="cg-stat-label">Total Clauses</div>
        </div>
        <div class="cg-stat-card">
            <div class="cg-stat-icon">🔴</div>
            <div class="cg-stat-value" style="color:var(--risk-red)">{high_risks}</div>
            <div class="cg-stat-label">High-Risk Clauses</div>
        </div>
        <div class="cg-stat-card">
            <div class="cg-stat-icon">🟡</div>
            <div class="cg-stat-value" style="color:var(--risk-amber)">{med_risks}</div>
            <div class="cg-stat-label">Medium-Risk Clauses</div>
        </div>
        <div class="cg-stat-card">
            <div class="cg-stat-icon"></div>
            <div class="cg-stat-value">{obligations}</div>
            <div class="cg-stat-label">Your Obligations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──
    tab_summary, tab_obligations, tab_risks, tab_dates, tab_chat = st.tabs([
        "  Summary",
        "  Obligations & Rights",
        "  Risk Clauses",
        "  Dates & Deadlines",
        "  AI Assistant",
    ])

    # ── TAB 1: Summary ──
    with tab_summary:
        st.markdown(f"""
        <div class="cg-section-card">
            <div class="cg-section-eyebrow">Plain-English Analysis</div>
            <div class="cg-section-title"> Executive Summary</div>
            <p class="cg-prose">{a['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cg-section-card" style="background:linear-gradient(135deg,#0F1C2E,#1A3A5C);border:none;">
            <div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;
                        color:rgba(200,169,110,0.9);margin-bottom:8px;">Recommendation</div>
            <div style="font-size:16px;font-weight:600;color:#FFFFFF;margin-bottom:10px;">
                ⚠️ Professional Review Recommended
            </div>
            <p style="font-size:13px;color:#94A3B8;line-height:1.7;margin:0;">
                This document contains several clauses with elevated risk — particularly the non-compete
                and IP assignment provisions. We recommend consulting a qualified employment lawyer
                before signing. Use the AI Assistant tab to explore specific clauses further.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 2: Obligations ──
    with tab_obligations:
        col_you, col_them = st.columns(2, gap="large")

        with col_you:
            st.markdown("""
            <div class="cg-section-card">
                <div class="cg-section-eyebrow">Your Responsibilities</div>
                <div class="cg-section-title"> Your Obligations</div>
            """, unsafe_allow_html=True)
            for o in a["obligations"]:
                if o["party"] == "you":
                    st.markdown(f"""
                    <div class="cg-item">
                        <div class="cg-item-dot dot-obligation"></div>
                        <div class="cg-item-text">{o['text']}</div>
                        <span class="cg-item-badge badge-you">You</span>
                    </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_them:
            st.markdown("""
            <div class="cg-section-card">
                <div class="cg-section-eyebrow">Their Commitments</div>
                <div class="cg-section-title"> Their Obligations</div>
            """, unsafe_allow_html=True)
            for o in a["obligations"]:
                if o["party"] == "them":
                    st.markdown(f"""
                    <div class="cg-item">
                        <div class="cg-item-dot dot-right"></div>
                        <div class="cg-item-text">{o['text']}</div>
                        <span class="cg-item-badge badge-them">Them</span>
                    </div>""", unsafe_allow_html=True)
            for o in a["obligations"]:
                if o["party"] == "mutual":
                    st.markdown(f"""
                    <div class="cg-item">
                        <div class="cg-item-dot" style="background:#7C3AED"></div>
                        <div class="cg-item-text">{o['text']}</div>
                        <span class="cg-item-badge badge-mutual">Mutual</span>
                    </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 3: Risk Clauses ──
    with tab_risks:
        high_count = sum(1 for r in a["risks"] if r["severity"] == "high")
        med_count  = sum(1 for r in a["risks"] if r["severity"] == "medium")

        st.markdown(f"""
        <div style="display:flex;gap:12px;margin-bottom:20px;align-items:center;">
            <div style="background:var(--risk-red-bg);border:1.5px solid var(--risk-red);
                        border-radius:8px;padding:10px 18px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:var(--risk-red)">{high_count}</div>
                <div style="font-size:11px;font-weight:600;color:var(--risk-red)">High Risk</div>
            </div>
            <div style="background:var(--risk-amber-bg);border:1.5px solid var(--risk-amber);
                        border-radius:8px;padding:10px 18px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:var(--risk-amber)">{med_count}</div>
                <div style="font-size:11px;font-weight:600;color:var(--risk-amber)">Medium Risk</div>
            </div>
            <div style="font-size:13px;color:var(--text-secondary);margin-left:8px;">
                Review each flagged clause carefully before signing.
            </div>
        </div>
        """, unsafe_allow_html=True)

        for r in a["risks"]:
            severity_class = "medium" if r["severity"] == "medium" else ""
            badge_class    = "sev-medium" if r["severity"] == "medium" else "sev-high"
            st.markdown(f"""
            <div class="cg-risk-clause {severity_class}">
                <div class="cg-risk-clause-header">
                    <div class="cg-risk-clause-name">⚠ {r['name']}</div>
                    <span class="cg-risk-severity {badge_class}">{r['severity'].upper()}</span>
                </div>
                <div class="cg-risk-clause-text">"{r['text']}"</div>
                <div class="cg-risk-clause-why"> Why this matters: {r['why']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 4: Dates ──
    with tab_dates:
        st.markdown("""
        <div class="cg-section-card">
            <div class="cg-section-eyebrow">Timeline</div>
            <div class="cg-section-title"> Important Dates & Deadlines</div>
        """, unsafe_allow_html=True)
        for d in a["dates"]:
            st.markdown(f"""
            <div class="cg-date-item">
                <div class="cg-date-icon-wrap">{d['icon']}</div>
                <div>
                    <div class="cg-date-info-label">{d['label']}</div>
                    <div class="cg-date-info-value">{d['value']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 5: Chat ──
    with tab_chat:
        st.markdown("""
        <div class="cg-section-card" style="padding-bottom:8px;">
            <div class="cg-section-eyebrow">AI Legal Assistant</div>
            <div class="cg-section-title"> Ask Questions About Your Document</div>
            <p class="cg-prose" style="margin-bottom:20px;">
                Ask anything about the clauses, obligations, or terms in your document.
            </p>
        """, unsafe_allow_html=True)

        # Render chat history
        chat_html = '<div class="cg-chat-wrap">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "ai":
                chat_html += f"""
                <div style="align-self:flex-start;max-width:82%;">
                    <div class="cg-bubble-ai-label">⚖ ClauseGuard AI</div>
                    <div class="cg-bubble cg-bubble-ai">{msg['text']}</div>
                </div>"""
            else:
                chat_html += f'<div class="cg-bubble cg-bubble-user" style="align-self:flex-end;">{msg["text"]}</div>'
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Input
        with st.form("chat_form", clear_on_submit=True):
            col_inp, col_btn = st.columns([5, 1], gap="small")
            with col_inp:
                user_q = st.text_input(
                    "Question",
                    placeholder="e.g. What does the non-compete clause mean for me?",
                    label_visibility="collapsed",
                )
            with col_btn:
                send = st.form_submit_button("Send", use_container_width=True)

            if send and user_q.strip():
                st.session_state.chat_history.append({"role": "user", "text": user_q})
                # ── REPLACE THIS with your actual Groq/LangGraph call ──
                mock_response = (
                    "Based on the document, the non-compete clause (Section 8.2) restricts you from "
                    "working with any direct or indirect competitor within the APAC region for 24 months "
                    "after your employment ends. This is broader than industry standard (typically 6–12 months "
                    "within a specific city or country). You should negotiate to narrow the geographic scope "
                    "or reduce the duration before signing."
                )
                st.session_state.chat_history.append({"role": "ai", "text": mock_response})
                st.rerun()

        # Quick-ask suggestions
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:11px;font-weight:600;color:var(--text-muted);
                    text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">
            Quick Questions
        </div>""", unsafe_allow_html=True)

        suggestion_cols = st.columns(2)
        suggestions = [
            "Is the non-compete enforceable?",
            "What happens if I leave early?",
            "Can they change my salary terms?",
            "Does this cover my side projects?",
        ]
        for i, s in enumerate(suggestions):
            with suggestion_cols[i % 2]:
                if st.button(s, key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "text": s})
                    st.session_state.chat_history.append({
                        "role": "ai",
                        "text": f"Regarding \"{s}\" — based on the document clauses, this is governed by Section 8. I recommend reviewing the specific wording with a qualified legal professional for your jurisdiction.",
                    })
                    st.rerun()