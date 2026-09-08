import hashlib
import os
import re
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from doc_processing import analyze_invoices, clear_cache, process_invoices
from model_gateway import invoke_llm
from spoof_data import get_spoof_df

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon="🏛️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #F97316;
    }

    .stApp {
        background-color: #0A0A0A;
    }

    /* Streamlit native text elements */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #F97316 !important;
    }

    /* Inputs, selects, textareas */
    .stTextInput input, .stSelectbox div[data-baseweb="select"],
    .stFileUploader, .stFileUploader label,
    textarea {
        background-color: #1A1A1A !important;
        color: #F97316 !important;
        border-color: #F97316 !important;
    }

    /* Dataframe */
    .stDataFrame, [data-testid="stDataFrame"] {
        background-color: #111111 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1A1A1A !important;
        color: #F97316 !important;
        border: 1px solid #F97316 !important;
        border-radius: 8px !important;
    }
    .stButton > button:hover {
        background-color: #F97316 !important;
        color: #0A0A0A !important;
    }
    [data-testid="baseButton-primary"] {
        background-color: #F97316 !important;
        color: #0A0A0A !important;
        border: none !important;
    }
    [data-testid="baseButton-primary"]:hover {
        background-color: #EA6A0A !important;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #1A1A1A !important;
        color: #F97316 !important;
        border: 1px solid #F97316 !important;
        border-radius: 8px !important;
    }

    /* Divider */
    hr {
        border-color: #2A2A2A !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Cards */
    .card {
        background: #111111;
        border: 1px solid #2A2A2A;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 8px rgba(249,115,22,0.08);
        margin-bottom: 16px;
    }

    /* Metric cards */
    .metric-card {
        background: #111111;
        border: 1px solid #2A2A2A;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 8px rgba(249,115,22,0.08);
        text-align: center;
    }
    .metric-label {
        font-size: 13px;
        color: #C2410C !important;
        font-weight: 500;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #F97316 !important;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #0A0A0A 0%, #7C2D12 100%);
        border: 1px solid #F97316;
        border-radius: 16px;
        padding: 48px 40px;
        margin-bottom: 28px;
    }
    .hero h1 {
        font-size: 36px;
        font-weight: 700;
        margin: 0 0 10px 0;
        color: #F97316 !important;
    }
    .hero p {
        font-size: 16px;
        color: #FDBA74 !important;
        margin: 0 0 20px 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(249,115,22,0.15);
        border: 1px solid #F97316;
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 13px;
        font-weight: 500;
        color: #FDBA74 !important;
    }

    /* Futuristic neon pop-out cards */
    .neon-card {
        background: #0D0D0D;
        border: 1px solid #F97316;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 20px;
        box-shadow:
            0 0 8px rgba(249,115,22,0.4),
            0 0 24px rgba(249,115,22,0.2),
            0 0 60px rgba(249,115,22,0.08),
            inset 0 1px 0 rgba(249,115,22,0.15);
        position: relative;
        overflow: hidden;
    }
    .neon-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #F97316, transparent);
        opacity: 0.8;
    }

    .neon-metric {
        background: #0D0D0D;
        border: 1px solid #F97316;
        border-radius: 14px;
        padding: 22px 28px;
        text-align: center;
        box-shadow:
            0 0 10px rgba(249,115,22,0.5),
            0 0 30px rgba(249,115,22,0.2),
            inset 0 1px 0 rgba(249,115,22,0.2);
        position: relative;
    }
    .neon-metric-label {
        font-size: 11px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #C2410C !important;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .neon-metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #F97316 !important;
        text-shadow: 0 0 12px rgba(249,115,22,0.8), 0 0 30px rgba(249,115,22,0.4);
    }

    /* Budget progress bars */
    .budget-row {
        margin-bottom: 18px;
    }
    .budget-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 5px;
    }
    .budget-cat {
        font-size: 13px;
        font-weight: 600;
        color: #F97316 !important;
    }
    .budget-nums {
        font-size: 12px;
        color: #C2410C !important;
    }
    .budget-track {
        width: 100%;
        height: 10px;
        background: #1A1A1A;
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid #2A2A2A;
    }
    .budget-fill-ok   { height: 100%; border-radius: 6px; background: #22c55e; box-shadow: 0 0 6px rgba(34,197,94,0.6); }
    .budget-fill-warn { height: 100%; border-radius: 6px; background: #F97316; box-shadow: 0 0 6px rgba(249,115,22,0.8); }
    .budget-fill-over { height: 100%; border-radius: 6px; background: #ef4444; box-shadow: 0 0 8px rgba(239,68,68,0.9); }
    .budget-pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 8px;
    }
    .pill-ok   { background: rgba(34,197,94,0.15);  color: #22c55e; border: 1px solid #22c55e; }
    .pill-warn { background: rgba(249,115,22,0.15); color: #F97316; border: 1px solid #F97316; }
    .pill-over { background: rgba(239,68,68,0.15);  color: #ef4444; border: 1px solid #ef4444; }
    .burn-rate {
        font-size: 11px;
        color: #57606a !important;
        margin-top: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session auto-save helpers + anomaly flagging
# ---------------------------------------------------------------------------

_CACHE_PATH = Path(__file__).parent / ".cache" / "session.csv"


def _save_session(df: pd.DataFrame) -> None:
    _CACHE_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(_CACHE_PATH, index=False)


def _load_session() -> pd.DataFrame | None:
    if _CACHE_PATH.exists():
        try:
            return pd.read_csv(_CACHE_PATH)
        except Exception:
            pass
    return None


def _flag_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Add a Flag column: DUPLICATE, UNUSUAL, or empty."""
    df = df.copy()
    flags = [""] * len(df)
    if {"Vendor", "Amount", "Date"}.issubset(df.columns):
        dup_mask = df.duplicated(subset=["Vendor", "Amount", "Date"], keep=False)
        for i in df.index[dup_mask]:
            flags[i] = "DUPLICATE"
    if {"Category", "Amount"}.issubset(df.columns):
        medians = df.groupby("Category")["Amount"].median()
        for i, row in df.iterrows():
            if flags[i]:
                continue
            cat = row.get("Category", "")
            amt = row.get("Amount", 0)
            if cat in medians and medians[cat] > 0 and amt > 2.5 * medians[cat]:
                flags[i] = "UNUSUAL"
    df["Flag"] = flags
    return df


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "df" not in st.session_state:
    _restored = _load_session()
    if _restored is not None:
        st.session_state.df = _flag_rows(_restored)
        st.session_state._session_restored = True
    else:
        st.session_state.df = None
        st.session_state._session_restored = False
else:
    st.session_state._session_restored = False
if "summary" not in st.session_state:
    st.session_state.summary = None
if "processed_hashes" not in st.session_state:
    st.session_state.processed_hashes = set()
if "demo_loaded" not in st.session_state:
    st.session_state.demo_loaded = False
if "budgets" not in st.session_state:
    st.session_state.budgets = {
        "Office Supplies": 500.0,
        "Equipment": 3000.0,
        "Services": 5000.0,
        "Utilities": 2000.0,
    }
if "show_flagged_only" not in st.session_state:
    st.session_state.show_flagged_only = False
if "nlq_answer" not in st.session_state:
    st.session_state.nlq_answer = ""
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

# ---------------------------------------------------------------------------
# Helper: generate summary
# ---------------------------------------------------------------------------


def generate_summary(df: pd.DataFrame) -> str:
    total_amount = df["Amount"].sum() if "Amount" in df.columns else 0.0
    num_items = len(df)

    cat_breakdown = ""
    if "Category" in df.columns:
        cat_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        parts = [cat + ": $" + "{:.2f}".format(val) for cat, val in cat_totals.items()]
        cat_breakdown = ", ".join(parts)

    top_vendor = ""
    top_vendor_amount = 0.0
    if "Vendor" in df.columns:
        vendor_totals = df.groupby("Vendor")["Amount"].sum().sort_values(ascending=False)
        if not vendor_totals.empty:
            top_vendor = vendor_totals.index[0]
            top_vendor_amount = float(vendor_totals.iloc[0])

    doc_type_breakdown = ""
    if "Doc Type" in df.columns:
        dt_totals = df.groupby("Doc Type")["Amount"].sum().sort_values(ascending=False)
        parts = [dt + ": $" + "{:.2f}".format(val) for dt, val in dt_totals.items()]
        doc_type_breakdown = ", ".join(parts)

    date_range = ""
    avg_daily = 0.0
    if "Date" in df.columns:
        try:
            dates = pd.to_datetime(df["Date"], errors="coerce").dropna()
            if not dates.empty:
                min_date = dates.min().strftime("%Y-%m-%d")
                max_date = dates.max().strftime("%Y-%m-%d")
                date_range = min_date + " to " + max_date
                num_days = max((dates.max() - dates.min()).days, 1)
                avg_daily = total_amount / num_days
        except Exception:
            pass

    prompt = (
        "You are a professional expense analyst.\n"
        "Write exactly 3 short sentences covering:\n"
        "1. Total spend and date range.\n"
        "2. Largest spending category and top vendor.\n"
        "3. One specific actionable recommendation to reduce costs.\n"
        "Do not restate every number. Do not use markdown. Do not use bullet points. "
        "Do not use headers. Do not use bold text. "
        "Do not add preamble, commentary, self-evaluation, or revision notes. "
        "Return plain text only.\n\n"
        "Data:\n"
        "- Total amount: $" + "{:.2f}".format(total_amount) + "\n"
        "- Line items: " + str(num_items) + "\n"
        "- Date range: " + (date_range if date_range else "unknown") + "\n"
        "- Average daily spend: $" + "{:.2f}".format(avg_daily) + "\n"
        "- Category breakdown: " + (cat_breakdown if cat_breakdown else "none") + "\n"
        "- Top vendor: " + (top_vendor + " ($" + "{:.2f}".format(top_vendor_amount) + ")" if top_vendor else "unknown") + "\n"
        "- Document type breakdown: " + (doc_type_breakdown if doc_type_breakdown else "none") + "\n"
    )

    raw = invoke_llm(prompt, max_new_tokens=300)

    cleaned = re.sub(r"\*\*", "", raw)
    cleaned = re.sub(r"##\s*", "", cleaned)
    cleaned = re.sub(r"\*", "", cleaned)
    cleaned = re.sub(r"(?m)^-\s+", "", cleaned)
    summary = cleaned.strip()
    return summary


def ask_data(question: str, df: pd.DataFrame) -> str:
    """Answer a free-text question grounded entirely in the DataFrame."""
    total = float(df["Amount"].sum()) if "Amount" in df.columns else 0.0
    cats = ""
    if "Category" in df.columns:
        ct = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        cats = "; ".join(c + "=$" + "{:,.0f}".format(v) for c, v in ct.items())
    vendors = ""
    if "Vendor" in df.columns:
        vt = df.groupby("Vendor")["Amount"].sum().sort_values(ascending=False)
        vendors = "; ".join(v + "=$" + "{:,.0f}".format(a) for v, a in vt.items())
    dtypes = ""
    if "Doc Type" in df.columns:
        dt = df.groupby("Doc Type")["Amount"].sum().sort_values(ascending=False)
        dtypes = "; ".join(d + "=$" + "{:,.0f}".format(a) for d, a in dt.items())
    dates = ""
    if "Date" in df.columns:
        parsed = pd.to_datetime(df["Date"], errors="coerce").dropna()
        if not parsed.empty:
            dates = parsed.min().strftime("%Y-%m-%d") + " to " + parsed.max().strftime("%Y-%m-%d")

    prompt = (
        "You are a financial analyst. Answer the user's question using ONLY the data below. "
        "Be concise — 1 to 3 sentences. Cite specific numbers. No markdown, no preamble.\n\n"
        "DATA:\n"
        "- Total spend: ${:,.2f}\n".format(total) +
        "- Date range: " + (dates or "unknown") + "\n"
        "- By doc type: " + (dtypes or "none") + "\n"
        "- By category: " + (cats or "none") + "\n"
        "- By vendor: " + (vendors or "none") + "\n\n"
        "QUESTION: " + question + "\n\nANSWER:"
    )
    raw = invoke_llm(prompt, max_new_tokens=200)
    return re.sub(r"\*\*|##\s*|\*", "", raw).strip()


def _detect_recurring(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows flagged as likely recurring (same vendor+category, >=3 months, <10% amount variance)."""
    if not {"Vendor", "Category", "Amount", "Date"}.issubset(df.columns):
        return pd.DataFrame()
    _d = df.copy()
    _d["_mon"] = pd.to_datetime(_d["Date"], errors="coerce").dt.to_period("M")
    _d = _d.dropna(subset=["_mon"])
    rows = []
    for (vendor, cat), grp in _d.groupby(["Vendor", "Category"]):
        months = grp["_mon"].nunique()
        if months < 3:
            continue
        mean_amt = float(grp["Amount"].mean())
        cv = float(grp["Amount"].std() / mean_amt) if mean_amt > 0 else 1.0
        if cv > 0.10:
            continue
        rows.append({
            "Vendor": vendor,
            "Category": cat,
            "Avg Monthly": mean_amt,
            "Months Seen": int(months),
            "Est. Annual Cost": mean_amt * 12,
        })
    return pd.DataFrame(rows).sort_values("Est. Annual Cost", ascending=False) if rows else pd.DataFrame()


# ---------------------------------------------------------------------------
# Hero banner
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🏛️ AI Expense Tracker</h1>
        <p>Upload PDF receipts and invoices to automatically extract, categorize, and analyze your business expenses.</p>
        <span class="hero-badge">Powered by IBM watsonx.ai</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Session restored banner
if st.session_state.get("_session_restored"):
    st.info("📂 Session restored from your last visit. Click **Clear All** to start fresh.")
    st.session_state._session_restored = False

# ---------------------------------------------------------------------------
# File uploader + Camera capture
# ---------------------------------------------------------------------------

_up_col, _cam_col = st.columns([3, 1])
with _up_col:
    uploaded_files = st.file_uploader(
        "Upload PDF receipts or invoices (max 10 files)",
        type=["pdf"],
        accept_multiple_files=True,
    )
with _cam_col:
    st.markdown("**📷 Or capture on mobile**")
    _camera_image = st.camera_input("Take a photo of a receipt", label_visibility="collapsed")

if uploaded_files and len(uploaded_files) > 10:
    st.error("Maximum 10 files allowed. Only the first 10 will be processed.")
    uploaded_files = uploaded_files[:10]

# Wrap camera image as a file-like object compatible with process_invoices
if _camera_image is not None:
    import io
    from PIL import Image
    import tempfile

    _img = Image.open(_camera_image)
    _img_tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    _img.save(_img_tmp.name, format="JPEG")
    _img_tmp.close()

    class _CameraFile:
        def __init__(self, path: str) -> None:
            self.name = "camera_receipt.jpg"
            self._path = path
        def read(self) -> bytes:
            with open(self._path, "rb") as f:
                return f.read()
        def getvalue(self) -> bytes:
            return self.read()

    _camera_file_obj = _CameraFile(_img_tmp.name)
    if uploaded_files:
        uploaded_files = list(uploaded_files) + [_camera_file_obj]
    else:
        uploaded_files = [_camera_file_obj]

# ---------------------------------------------------------------------------
# Action buttons
# ---------------------------------------------------------------------------

col_submit, col_analyze, col_summary, col_export, col_demo, col_clear = st.columns([1, 1, 1.4, 1.2, 1.4, 1])

with col_submit:
    submit_clicked = st.button("Submit", type="primary", use_container_width=True)

with col_analyze:
    analyze_clicked = st.button("Analyze", use_container_width=True)

with col_summary:
    summary_clicked = st.button("Generate Summary", use_container_width=True)

with col_export:
    if st.session_state.df is not None and not st.session_state.df.empty:
        csv_data = st.session_state.df.to_csv(index=False)
        st.download_button(
            label="Export CSV",
            data=csv_data,
            file_name="expenses.csv",
            mime="text/csv",
            use_container_width=True,
        )

with col_demo:
    demo_clicked = st.button("Load Demo Data", use_container_width=True)

with col_clear:
    clear_clicked = st.button("Clear All", use_container_width=True)

# ---------------------------------------------------------------------------
# Load Demo Data
# ---------------------------------------------------------------------------

if demo_clicked:
    _demo_df = _flag_rows(get_spoof_df())
    st.session_state.df = _demo_df
    st.session_state.summary = None
    st.session_state.processed_hashes = {"demo_1", "demo_2", "demo_3", "demo_4", "demo_5"}
    st.session_state.demo_loaded = True
    _save_session(_demo_df)

# ---------------------------------------------------------------------------
# Clear All
# ---------------------------------------------------------------------------

if clear_clicked:
    st.session_state.df = None
    st.session_state.summary = None
    st.session_state.processed_hashes = set()
    st.session_state.demo_loaded = False
    st.session_state.show_flagged_only = False
    clear_cache()
    if _CACHE_PATH.exists():
        _CACHE_PATH.unlink()
    st.rerun()

# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------

if submit_clicked:
    if not uploaded_files:
        st.warning("Please upload at least one PDF file before submitting.")
    else:
        new_files = []
        for uf in uploaded_files:
            file_bytes = uf.getvalue()
            file_hash = hashlib.md5(file_bytes).hexdigest()
            if file_hash not in st.session_state.processed_hashes:
                new_files.append(uf)

        if not new_files:
            st.warning("All uploaded files have already been processed.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()

            def progress_callback(completed, total, filename):
                progress_bar.progress(int(completed / total * 100))
                status_text.text(
                    "Processing file " + str(completed) + " of " + str(total) + ": " + filename + "..."
                )

            df_new, debug_info = process_invoices(
                new_files,
                max_workers=2,
                progress_callback=progress_callback,
            )

            progress_bar.empty()
            status_text.empty()

            if st.session_state.df is None or st.session_state.df.empty:
                merged = df_new
            else:
                merged = pd.concat([st.session_state.df, df_new], ignore_index=True)
            st.session_state.df = _flag_rows(merged)
            _save_session(st.session_state.df)

            failed_files = []
            for uf in new_files:
                file_bytes = uf.getvalue()
                file_hash = hashlib.md5(file_bytes).hexdigest()
                debug_val = debug_info.get(uf.name, "")
                if not debug_val.startswith("ERROR"):
                    st.session_state.processed_hashes.add(file_hash)
                else:
                    failed_files.append(uf.name)

            st.session_state.summary = None

            success_count = len(new_files) - len(failed_files)
            if success_count > 0:
                st.success(str(success_count) + " file(s) processed successfully.")
            if failed_files:
                st.warning("The following files could not be processed: " + ", ".join(failed_files))

# ---------------------------------------------------------------------------
# Results section
# ---------------------------------------------------------------------------

if st.session_state.df is not None and not st.session_state.df.empty:
    df = st.session_state.df.copy()

    # ------------------------------------------------------------------
    # Sidebar: date range filter
    # ------------------------------------------------------------------
    _parsed_dates = pd.to_datetime(df["Date"], errors="coerce").dropna()
    if not _parsed_dates.empty:
        _min_date = _parsed_dates.min().date()
        _max_date = _parsed_dates.max().date()
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 📅 Date Filter")
            _date_range = st.date_input(
                "Show expenses between",
                value=(_min_date, _max_date),
                min_value=_min_date,
                max_value=_max_date,
                key="date_filter",
            )
        if isinstance(_date_range, (list, tuple)) and len(_date_range) == 2:
            _d0, _d1 = _date_range
            _date_col = pd.to_datetime(df["Date"], errors="coerce")
            df = df[(_date_col >= pd.Timestamp(_d0)) & (_date_col <= pd.Timestamp(_d1))]

    # ------------------------------------------------------------------
    # Anomaly badge
    # ------------------------------------------------------------------
    _flag_counts = df["Flag"].value_counts() if "Flag" in df.columns else {}
    _n_dup = int(_flag_counts.get("DUPLICATE", 0))
    _n_unusual = int(_flag_counts.get("UNUSUAL", 0))
    _n_flagged = _n_dup + _n_unusual
    if _n_flagged > 0:
        _badge_parts = []
        if _n_dup:
            _badge_parts.append(str(_n_dup) + " duplicate" + ("s" if _n_dup > 1 else ""))
        if _n_unusual:
            _badge_parts.append(str(_n_unusual) + " unusual amount" + ("s" if _n_unusual > 1 else ""))
        _alert_msg = "⚠️ " + " and ".join(_badge_parts) + " flagged — review highlighted rows below."
        st.warning(_alert_msg)
        _col_f1, _col_f2 = st.columns([3, 1])
        with _col_f2:
            if st.button("Show flagged only" if not st.session_state.show_flagged_only else "Show all rows",
                         use_container_width=True):
                st.session_state.show_flagged_only = not st.session_state.show_flagged_only

    # ------------------------------------------------------------------
    # Metric cards (on filtered df)
    # ------------------------------------------------------------------
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)

    total_amount = float(df["Amount"].sum()) if "Amount" in df.columns else 0.0
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            "<div class='neon-metric'>"
            "<div class='neon-metric-label'>Files Processed</div>"
            "<div class='neon-metric-value'>" + str(len(st.session_state.processed_hashes)) + "</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            "<div class='neon-metric'>"
            "<div class='neon-metric-label'>Line Items</div>"
            "<div class='neon-metric-value'>" + str(len(df)) + "</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            "<div class='neon-metric'>"
            "<div class='neon-metric-label'>Total Amount</div>"
            "<div class='neon-metric-value'>$" + "{:,.2f}".format(total_amount) + "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Inline data editor
    # ------------------------------------------------------------------
    _edit_cols = ["Date", "Vendor", "Doc Type", "Category", "Description", "Currency", "Amount"]
    for _c in _edit_cols:
        if _c not in df.columns:
            df[_c] = ""

    _view_df = df[_edit_cols + (["Flag"] if "Flag" in df.columns else [])].copy()
    if st.session_state.show_flagged_only and "Flag" in _view_df.columns:
        _view_df = _view_df[_view_df["Flag"] != ""]

    st.markdown("**📋 Expense Data** — edit any cell then click **Save Edits** to apply corrections.")
    _edited = st.data_editor(
        _view_df,
        use_container_width=True,
        hide_index=True,
        key="expense_editor",
    )
    if st.button("💾 Save Edits", key="save_edits_btn"):
        # Merge edits back: update matching rows in the full session df by index
        for idx in _edited.index:
            for col in _edit_cols:
                if col in _edited.columns and idx in st.session_state.df.index:
                    st.session_state.df.at[idx, col] = _edited.at[idx, col]
        st.session_state.df = _flag_rows(st.session_state.df)
        _save_session(st.session_state.df)
        st.success("Edits saved.")

    # ------------------------------------------------------------------
    # HST / Tax Report
    # ------------------------------------------------------------------
    with st.expander("🧾 Tax Report (HST / GST / VAT)"):
        if "Category" in df.columns and "Amount" in df.columns:
            _tax_df = df[df["Category"].str.strip() == "Taxes & Fees"].copy()
            _net_df = df[df["Category"].str.strip() != "Taxes & Fees"].copy()
            _total_tax = float(_tax_df["Amount"].sum())
            _total_net = float(_net_df["Amount"].sum())
            _eff_rate = (_total_tax / _total_net * 100) if _total_net > 0 else 0.0

            _tc1, _tc2, _tc3 = st.columns(3)
            _tc1.metric("Net Spend (ex-tax)", "${:,.2f}".format(_total_net))
            _tc2.metric("Total Tax Paid", "${:,.2f}".format(_total_tax))
            _tc3.metric("Effective Tax Rate", "{:.1f}%".format(_eff_rate))

            if not _tax_df.empty:
                st.markdown("**Tax by vendor:**")
                _vendor_tax = (
                    _tax_df.groupby("Vendor")["Amount"]
                    .sum()
                    .reset_index()
                    .rename(columns={"Amount": "Tax Paid"})
                    .sort_values("Tax Paid", ascending=False)
                )
                _vendor_tax["Tax Paid"] = _vendor_tax["Tax Paid"].map(lambda x: "${:,.2f}".format(x))
                st.dataframe(_vendor_tax, use_container_width=True, hide_index=True)

                _cra_df = _net_df[["Date", "Vendor", "Category", "Amount"]].copy()
                _cra_df.columns = ["Date", "Vendor", "Expense Category", "Net Amount"]
                _cra_df["HST Paid"] = _cra_df["Vendor"].map(
                    _tax_df.groupby("Vendor")["Amount"].sum().to_dict()
                ).fillna(0.0)
                st.download_button(
                    label="⬇️ Download CRA CSV",
                    data=_cra_df.to_csv(index=False),
                    file_name="cra_itc_report.csv",
                    mime="text/csv",
                )
        else:
            st.info("No category data available for tax breakdown.")

# ---------------------------------------------------------------------------
# Budget Alerts
# ---------------------------------------------------------------------------

if st.session_state.df is not None and not st.session_state.df.empty:
    _bdf = st.session_state.df.copy()
    _budget_cats = ["Office Supplies", "Equipment", "Services", "Utilities"]

    # Map Doc Type spend to budget categories
    _actual = {}
    for _cat in _budget_cats:
        if "Doc Type" in _bdf.columns:
            _actual[_cat] = float(_bdf[_bdf["Doc Type"] == _cat]["Amount"].sum())
        else:
            _actual[_cat] = 0.0

    # Compute weekly burn rate for projection
    _weekly_spend = {}
    if "Date" in _bdf.columns:
        _bdf["_bdate"] = pd.to_datetime(_bdf["Date"], errors="coerce")
        _bdf = _bdf.dropna(subset=["_bdate"])
        if not _bdf.empty:
            _n_weeks = max(
                ((_bdf["_bdate"].max() - _bdf["_bdate"].min()).days / 7.0), 1.0
            )
            for _cat in _budget_cats:
                _weekly_spend[_cat] = _actual[_cat] / _n_weeks

    _has_alert = any(
        _actual[c] >= st.session_state.budgets[c] * 0.8
        for c in _budget_cats
        if st.session_state.budgets[c] > 0
    )

    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.subheader("💰 Budget Tracker")

    # Sidebar budget inputs
    with st.sidebar:
        st.markdown("### 💰 Monthly Budgets")
        st.caption("Set a monthly budget per doc type category.")
        for _cat in _budget_cats:
            st.session_state.budgets[_cat] = st.number_input(
                _cat,
                min_value=0.0,
                max_value=100000.0,
                value=st.session_state.budgets[_cat],
                step=100.0,
                format="%.0f",
                key="budget_input_" + _cat,
            )

    # Build progress rows
    _budget_html = ""
    for _cat in _budget_cats:
        _spent = _actual[_cat]
        _limit = st.session_state.budgets[_cat]
        if _limit <= 0:
            continue
        _pct = min(_spent / _limit * 100, 100)
        _remaining = max(_limit - _spent, 0.0)

        if _pct >= 100:
            _fill_class = "budget-fill-over"
            _pill_class = "pill-over"
            _pill_text = "OVER BUDGET"
        elif _pct >= 80:
            _fill_class = "budget-fill-warn"
            _pill_class = "pill-warn"
            _pill_text = "WARNING"
        else:
            _fill_class = "budget-fill-ok"
            _pill_class = "pill-ok"
            _pill_text = "ON TRACK"

        _burn = _weekly_spend.get(_cat, 0.0)
        if _burn > 0 and _remaining > 0:
            _weeks_left = _remaining / _burn
            _burn_str = "Burn rate: ${:.0f}/wk — budget lasts ~{:.1f} more weeks".format(_burn, _weeks_left)
        elif _burn > 0 and _remaining <= 0:
            _burn_str = "Budget exhausted — still spending ${:.0f}/wk".format(_burn)
        else:
            _burn_str = ""

        _budget_html += (
            "<div class='budget-row'>"
            "<div class='budget-header'>"
            "<span class='budget-cat'>" + _cat + "<span class='budget-pill " + _pill_class + "'>" + _pill_text + "</span></span>"
            "<span class='budget-nums'>${:,.0f} spent &nbsp;/&nbsp; ${:,.0f} budget &nbsp;({:.0f}%)</span>".format(_spent, _limit, _pct) +
            "</div>"
            "<div class='budget-track'><div class='" + _fill_class + "' style='width:" + "{:.1f}".format(_pct) + "%'></div></div>"
            + ("<div class='burn-rate'>" + _burn_str + "</div>" if _burn_str else "") +
            "</div>"
        )

    st.markdown(_budget_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Analyze
# ---------------------------------------------------------------------------

if analyze_clicked:
    if st.session_state.df is None or st.session_state.df.empty:
        st.warning("Please upload and submit receipts first.")
    else:
        vendor_chart, category_chart, doc_type_chart, _ = analyze_invoices(
            st.session_state.df
        )
        chart1, chart2, chart3 = st.columns(3)
        with chart1:
            st.plotly_chart(vendor_chart, use_container_width=True)
        with chart2:
            st.plotly_chart(category_chart, use_container_width=True)
        with chart3:
            st.plotly_chart(doc_type_chart, use_container_width=True)

# ---------------------------------------------------------------------------
# Generate Summary
# ---------------------------------------------------------------------------

if summary_clicked:
    if st.session_state.df is None or st.session_state.df.empty:
        st.warning("Please upload and submit receipts first.")
    else:
        with st.spinner("Generating AI summary..."):
            st.session_state.summary = generate_summary(st.session_state.df)

if st.session_state.summary:
    st.info(st.session_state.summary)

# ---------------------------------------------------------------------------
# Category Trends
# ---------------------------------------------------------------------------

if st.session_state.df is not None and not st.session_state.df.empty:
    _df = st.session_state.df.copy()

    # ---- Require Date and Category columns --------------------------------
    if "Date" in _df.columns and "Category" in _df.columns and "Amount" in _df.columns:

        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.subheader("📊 Category Trends")

        # Parse dates; drop rows where date is unparseable
        _df["_date"] = pd.to_datetime(_df["Date"], errors="coerce")
        _df = _df.dropna(subset=["_date"])

        if not _df.empty:
            # ----------------------------------------------------------------
            # Derive calendar month label and ISO week bucket
            # ----------------------------------------------------------------
            _df["_month"] = _df["_date"].dt.to_period("M").astype(str)   # e.g. "2025-03"
            _df["_week"]  = _df["_date"].dt.to_period("W").apply(
                lambda p: p.start_time.strftime("%Y-%m-%d")
            )  # week start date string, sortable

            # ----------------------------------------------------------------
            # Summary table: avg spend & avg purchases per month per category
            # ----------------------------------------------------------------

            # Monthly totals per category
            _monthly = (
                _df.groupby(["Category", "_month"])["Amount"]
                .agg(monthly_spend="sum", monthly_count="count")
                .reset_index()
            )

            # Average across months
            _cat_summary = (
                _monthly.groupby("Category")
                .agg(
                    avg_monthly_spend=("monthly_spend", "mean"),
                    avg_monthly_count=("monthly_count", "mean"),
                )
                .reset_index()
                .sort_values("avg_monthly_spend", ascending=False)
            )
            _cat_summary["avg_monthly_spend"] = _cat_summary["avg_monthly_spend"].map(
                lambda x: "${:,.2f}".format(x)
            )
            _cat_summary["avg_monthly_count"] = _cat_summary["avg_monthly_count"].map(
                lambda x: "{:.1f}".format(x)
            )
            _cat_summary = _cat_summary.rename(columns={
                "Category": "Category",
                "avg_monthly_spend": "Avg Monthly Spend",
                "avg_monthly_count": "Avg Purchases / Month",
            })

            st.markdown("**Average usage per category (across all months in data)**")
            st.dataframe(
                _cat_summary,
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # ----------------------------------------------------------------
            # Weekly spend chart with category dropdown
            # ----------------------------------------------------------------

            _categories = sorted(_df["Category"].dropna().unique().tolist())

            selected_cat = st.selectbox(
                "Select a category to view weekly spend",
                options=_categories,
                key="trend_category_select",
            )

            _cat_df = _df[_df["Category"] == selected_cat].copy()

            # Aggregate by week
            _weekly = (
                _cat_df.groupby("_week")["Amount"]
                .sum()
                .reset_index()
                .rename(columns={"_week": "Week", "Amount": "Total Spend"})
                .sort_values("Week")
            )

            if _weekly.empty:
                st.info("No data for the selected category.")
            else:
                import plotly.graph_objects as go

                _fig = go.Figure()
                _fig.add_trace(go.Scatter(
                    x=_weekly["Week"].tolist(),
                    y=_weekly["Total Spend"].tolist(),
                    mode="lines+markers",
                    line=dict(color="#F97316", width=2.5),
                    marker=dict(color="#F97316", size=8, line=dict(color="#0A0A0A", width=1.5)),
                    fill="tozeroy",
                    fillcolor="rgba(249,115,22,0.12)",
                    hovertemplate="Week of %{x}<br>$%{y:,.2f}<extra></extra>",
                ))
                _fig.update_layout(
                    title=dict(
                        text="Weekly Spend — " + selected_cat,
                        font=dict(color="#F97316", family="Inter, sans-serif"),
                    ),
                    xaxis=dict(
                        title=dict(
                            text="Week (starting date)",
                            font=dict(color="#F97316"),
                        ),
                        type="category",
                        tickangle=-45,
                        showgrid=False,
                        zeroline=False,
                        color="#F97316",
                        tickfont=dict(color="#F97316"),
                    ),
                    yaxis=dict(
                        title=dict(
                            text="Total Spend ($)",
                            font=dict(color="#F97316"),
                        ),
                        showgrid=True,
                        gridcolor="#2A2A2A",
                        zeroline=False,
                        tickprefix="$",
                        color="#F97316",
                        tickfont=dict(color="#F97316"),
                    ),
                    font={"family": "Inter, sans-serif", "color": "#F97316"},
                    plot_bgcolor="#111111",
                    paper_bgcolor="#111111",
                )
                st.plotly_chart(_fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
