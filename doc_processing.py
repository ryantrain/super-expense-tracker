import os
import json
import hashlib
import tempfile
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import plotly.graph_objects as go

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from model_gateway import invoke_llm

# ---------------------------------------------------------------------------
# Module-level singletons
# ---------------------------------------------------------------------------

_pipeline_options = PdfPipelineOptions()
_pipeline_options.do_ocr = True
_pipeline_options.do_table_structure = True

_converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=_pipeline_options)}
)

_file_cache: dict = {}


def clear_cache():
    global _file_cache
    _file_cache = {}


# ---------------------------------------------------------------------------
# PDF parsing
# ---------------------------------------------------------------------------

def _pdf_to_markdown(pdf_bytes: bytes) -> str:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        result = _converter.convert(tmp_path)
        return result.document.export_to_markdown()
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ---------------------------------------------------------------------------
# Document type detection
# ---------------------------------------------------------------------------

_TYPE_KEYWORDS = {
    "office_supplies": [
        "office", "supplies", "paper", "pens", "folders", "stationery",
        "toner", "ink", "printer", "desk", "chair", "filing",
    ],
    "equipment": [
        "equipment", "computer", "laptop", "monitor", "keyboard", "mouse",
        "hardware", "software", "technology", "device", "machinery",
    ],
    "services": [
        "services", "consulting", "maintenance", "repair", "cleaning",
        "security", "professional", "contractor", "vendor", "support",
    ],
    "utilities": [
        "utilities", "electricity", "water", "gas", "internet", "phone",
        "telecommunications", "energy", "power", "heating", "cooling",
    ],
}


def _detect_doc_type(filename: str, text: str) -> str:
    filename_lower = filename.lower()
    text_lower = text.lower()
    scores = {}
    for doc_type, keywords in _TYPE_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in filename_lower:
                score += 3
            if kw in text_lower:
                score += 1
        scores[doc_type] = score
    best = max(scores, key=lambda k: scores[k])
    if scores[best] == 0:
        return "generic"
    return best


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def _get_extraction_prompt(doc_type: str, text: str) -> str:
    if doc_type == "office_supplies":
        subject = "office supplies invoice"
        categories = (
            "Paper Products, Writing Instruments, Filing & Storage, Desk Accessories, "
            "Printer Supplies, Technology Accessories, Furniture, Taxes & Fees, Shipping, Miscellaneous"
        )
        item_rule = "One line per charge"
    elif doc_type == "equipment":
        subject = "equipment invoice"
        categories = (
            "Computer Hardware, Software Licenses, Peripherals, Networking Equipment, "
            "Maintenance, Installation, Taxes & Fees, Miscellaneous"
        )
        item_rule = "One line per charge"
    elif doc_type == "services":
        subject = "services invoice"
        categories = (
            "Consulting, Maintenance, Repair, Cleaning, Security, "
            "Professional Services, Contractor Fees, Taxes & Fees, Miscellaneous"
        )
        item_rule = "One line per item/charge"
    elif doc_type == "utilities":
        subject = "utilities invoice"
        categories = (
            "Electricity, Water, Gas, Internet, Telephone, Telecommunications, "
            "Energy, Taxes & Fees, Service Charges, Miscellaneous"
        )
        item_rule = "One line per charge"
    else:
        subject = "invoice"
        categories = (
            "Office Supplies, Equipment, Services, Utilities, Maintenance, "
            "Professional Services, Technology, Taxes & Fees, Miscellaneous"
        )
        item_rule = "One line per charge"

    prompt = (
        "Analyze this " + subject + " and extract all charges. Ignore any [image] tags.\n"
        "\n"
        "STEP 1: Create a table with these columns separated by | (pipe):\n"
        "Date | Vendor | Category | Description | Currency | Amount\n"
        "\n"
        "Categories: " + categories + "\n"
        "\n"
        "Rules:\n"
        "- " + item_rule + "\n"
        "- Date format: YYYY-MM-DD (or leave empty if not found)\n"
        "- Amount: numeric only (no currency symbols)\n"
        "- Include header row\n"
        "- Use | to separate columns\n"
        "\n"
        "Document:\n"
        + text + "\n"
        "\n"
        "Table:\n"
        "\n"
        "STEP 2: Now convert the table above into a JSON array. Each row becomes a JSON object with these fields:\n"
        "- date (from Date column)\n"
        "- vendor (from Vendor column)\n"
        "- doc_type (leave as empty string)\n"
        "- category (from Category column)\n"
        "- description (from Description column)\n"
        "- currency (from Currency column)\n"
        "- amount (from Amount column)\n"
        "- confidence (set to 0.9)\n"
        "\n"
        "Return ONLY the JSON array with no markdown, no code fences, no explanation:\n"
        '["'
    )
    return prompt


# ---------------------------------------------------------------------------
# Vendor extraction
# ---------------------------------------------------------------------------

_HEADER_KEYWORDS = {
    "invoice", "folio", "date", "page", "guest", "number",
    "charges", "credits", "description",
}


def _extract_vendor_from_text(text: str) -> str:
    lines = text.splitlines()[:10]
    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()
        if any(kw in lower for kw in _HEADER_KEYWORDS):
            continue
        if len(stripped) >= 3 and re.search(r"[a-zA-Z]", stripped):
            return stripped
    for line in lines:
        match = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", line)
        if match:
            return match.group(1)
    return "Unknown"


# ---------------------------------------------------------------------------
# Amount parsing
# ---------------------------------------------------------------------------

def _parse_amount(amount_str) -> float:
    if amount_str is None:
        return 0.0
    s = str(amount_str).strip()
    s = re.sub(r"[$\u20ac\xa3\xa5\u20b9]", "", s).strip()
    if not s:
        return 0.0
    # European format: 1.234,56 or 1,5 (comma as decimal, any decimal digits)
    if re.match(r"^-?\d{1,3}(\.\d{3})+(,\d+)$", s):
        s = s.replace(".", "").replace(",", ".")
    elif re.match(r"^-?\d+,\d+$", s):
        s = s.replace(",", ".")
    else:
        # Standard: remove thousands commas
        s = s.replace(",", "")
    try:
        return abs(float(s))
    except (ValueError, TypeError):
        return 0.0


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def _parse_json_from_llm(llm_output: str) -> list:
    text = "[" + llm_output
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()

    # Strategy 1: brace-depth scanning for [...] array boundary
    try:
        start = text.find("[")
        if start != -1:
            depth = 0
            for i in range(start, len(text)):
                ch = text[i]
                if ch == "[":
                    depth += 1
                elif ch == "]":
                    depth -= 1
                    if depth == 0:
                        candidate = text[start: i + 1]
                        parsed = json.loads(candidate)
                        if isinstance(parsed, list):
                            return parsed
                        break
    except (json.JSONDecodeError, Exception):
        pass

    # Strategy 2: extract all top-level {...} objects
    try:
        objects = []
        depth = 0
        obj_start = None
        for i, ch in enumerate(text):
            if ch == "{":
                if depth == 0:
                    obj_start = i
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and obj_start is not None:
                    try:
                        obj = json.loads(text[obj_start: i + 1])
                        objects.append(obj)
                    except json.JSONDecodeError:
                        pass
                    obj_start = None
        if objects:
            return objects
    except Exception:
        pass

    # Strategy 3: full json.loads on cleaned output
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
    except (json.JSONDecodeError, Exception):
        pass

    return []


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

_DOC_TYPE_MAP = {
    "office_supplies": "Office Supplies",
    "equipment": "Equipment",
    "services": "Services",
    "utilities": "Utilities",
    "generic": "",
}


def _normalize_expenses(rows: list, filename: str, text: str) -> list:
    doc_type_key = _detect_doc_type(filename, text)
    doc_type_label = _DOC_TYPE_MAP.get(doc_type_key, "")
    vendor_fallback = None
    normalized = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        vendor = str(row.get("vendor", "")).strip()
        if not vendor or vendor == "Unknown":
            if vendor_fallback is None:
                vendor_fallback = _extract_vendor_from_text(text)
            vendor = vendor_fallback
        try:
            amount = _parse_amount(row.get("amount", 0.0))
        except Exception:
            amount = 0.0
        try:
            confidence = float(row.get("confidence", 0.9))
        except (ValueError, TypeError):
            confidence = 0.9
        normalized.append({
            "date": str(row.get("date", "")).strip(),
            "vendor": vendor,
            "doc_type": doc_type_label,
            "category": str(row.get("category", "")).strip(),
            "description": str(row.get("description", "")).strip(),
            "currency": str(row.get("currency", "")).strip(),
            "amount": amount,
            "confidence": confidence,
        })
    return normalized


# ---------------------------------------------------------------------------
# Single-file processing
# ---------------------------------------------------------------------------

def _process_single_file(filename: str, pdf_bytes: bytes) -> tuple:
    md5 = hashlib.md5(pdf_bytes).hexdigest()
    if md5 in _file_cache:
        return _file_cache[md5], "cached"

    text = _pdf_to_markdown(pdf_bytes)
    doc_type = _detect_doc_type(filename, text)
    prompt = _get_extraction_prompt(doc_type, text)
    llm_output = invoke_llm(prompt, max_new_tokens=4096)
    raw_rows = _parse_json_from_llm(llm_output)
    rows = _normalize_expenses(raw_rows, filename, text)

    debug = " | ".join([
        "doc_type=" + doc_type,
        "llm_chars=" + str(len(llm_output)),
        "raw_rows=" + str(len(raw_rows)),
        "norm_rows=" + str(len(rows)),
    ])

    _file_cache[md5] = rows
    return rows, debug


# ---------------------------------------------------------------------------
# Public: process_invoices
# ---------------------------------------------------------------------------

_DF_COLUMNS = ["Date", "Vendor", "Doc Type", "Category", "Description",
               "Currency", "Amount", "Confidence"]

_FIELD_MAP = {
    "date": "Date",
    "vendor": "Vendor",
    "doc_type": "Doc Type",
    "category": "Category",
    "description": "Description",
    "currency": "Currency",
    "amount": "Amount",
    "confidence": "Confidence",
}


def process_invoices(uploaded_files, max_workers: int = 2, progress_callback=None):
    all_rows = []
    debug_info = {}
    total = len(uploaded_files)
    completed = 0

    futures = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for uf in uploaded_files:
            filename = uf.name
            pdf_bytes = uf.read()
            future = executor.submit(_process_single_file, filename, pdf_bytes)
            futures[future] = filename

        for future in as_completed(futures):
            filename = futures[future]
            try:
                rows, debug = future.result()
                if len(rows) == 0:
                    debug_info[filename] = "ERROR: 0 rows extracted — " + debug
                else:
                    debug_info[filename] = debug
                    all_rows.extend(rows)
            except Exception as e:
                debug_info[filename] = "ERROR: " + str(e)
            completed += 1
            if progress_callback is not None:
                progress_callback(completed, total, filename)

    if not all_rows:
        return pd.DataFrame(columns=_DF_COLUMNS), debug_info

    df = pd.DataFrame(all_rows)
    df = df.rename(columns=_FIELD_MAP)
    for col in _DF_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col not in ("Amount", "Confidence") else 0.0

    return df[_DF_COLUMNS], debug_info


# ---------------------------------------------------------------------------
# Public: analyze_invoices
# ---------------------------------------------------------------------------

_CAT_COLORS = {
    "Office Supplies": "#3B82F6",
    "Equipment": "#A855F7",
    "Services": "#10B981",
    "Utilities": "#F59E0B",
}

_TRANSPARENT = "rgba(0,0,0,0)"
_FONT = {"family": "Inter, sans-serif", "color": "#1f2328"}


def analyze_invoices(df, budgets: dict = None):
    if budgets is None:
        budgets = {"Office Supplies": 0, "Equipment": 0, "Services": 0, "Utilities": 0}

    # --- Figure 1: Total by vendor (horizontal bar, sorted ascending) ---
    if not df.empty and "Vendor" in df.columns:
        vendor_totals = df.groupby("Vendor")["Amount"].sum().sort_values(ascending=True)
    else:
        vendor_totals = pd.Series(dtype=float)

    fig1 = go.Figure(go.Bar(
        x=vendor_totals.values.tolist(),
        y=vendor_totals.index.tolist(),
        orientation="h",
        marker_color="#3B82F6",
    ))
    fig1.update_layout(
        title="Total Expenses by Vendor",
        font=_FONT,
        plot_bgcolor=_TRANSPARENT,
        paper_bgcolor=_TRANSPARENT,
        xaxis=dict(showgrid=True, gridcolor="#e5e7eb", zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    # --- Figure 2: By category (donut) ---
    if not df.empty and "Category" in df.columns:
        cat_totals = df.groupby("Category")["Amount"].sum()
    else:
        cat_totals = pd.Series(dtype=float)

    fig2 = go.Figure(go.Pie(
        labels=cat_totals.index.tolist(),
        values=cat_totals.values.tolist(),
        hole=0.4,
    ))
    fig2.update_layout(
        title="Expenses by Category",
        font=_FONT,
        plot_bgcolor=_TRANSPARENT,
        paper_bgcolor=_TRANSPARENT,
    )

    # --- Figure 3: By document type (vertical bar) ---
    if not df.empty and "Doc Type" in df.columns:
        dtype_totals = df.groupby("Doc Type")["Amount"].sum()
    else:
        dtype_totals = pd.Series(dtype=float)

    dtype_colors = [_CAT_COLORS.get(dt, "#6B7280") for dt in dtype_totals.index]

    fig3 = go.Figure(go.Bar(
        x=dtype_totals.index.tolist(),
        y=dtype_totals.values.tolist(),
        marker_color=dtype_colors,
    ))
    fig3.update_layout(
        title="Expenses by Document Type",
        font=_FONT,
        plot_bgcolor=_TRANSPARENT,
        paper_bgcolor=_TRANSPARENT,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#e5e7eb", zeroline=False),
    )

    # --- Figure 4: Budget vs Actual (overlay bar) ---
    categories = ["Office Supplies", "Equipment", "Services", "Utilities"]
    actuals = []
    for cat in categories:
        if not df.empty and "Doc Type" in df.columns:
            val = float(df[df["Doc Type"] == cat]["Amount"].sum())
        else:
            val = 0.0
        actuals.append(val)

    budget_vals = [float(budgets.get(cat, 0)) for cat in categories]
    actual_colors = [_CAT_COLORS[cat] for cat in categories]
    border_colors = [_CAT_COLORS[cat] for cat in categories]

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        name="Actual",
        x=categories,
        y=actuals,
        marker_color=actual_colors,
    ))
    fig4.add_trace(go.Bar(
        name="Budget",
        x=categories,
        y=budget_vals,
        marker=dict(
            color="rgba(0,0,0,0.15)",
            line=dict(color=border_colors, width=2),
        ),
    ))
    fig4.update_layout(
        title="Budget vs Actual",
        barmode="overlay",
        legend=dict(orientation="h", y=1.1),
        font=_FONT,
        plot_bgcolor=_TRANSPARENT,
        paper_bgcolor=_TRANSPARENT,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#e5e7eb", zeroline=False),
    )

    return fig1, fig2, fig3, fig4
