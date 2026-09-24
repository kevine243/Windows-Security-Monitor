import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Windows Security Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom styling — premium dark SOC aesthetic
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ---- Reset & base ---- */
    *, *::before, *::after { box-sizing: border-box; }

    .stApp {
        background: #0a0c10;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1440px;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0f14 0%, #0a0c10 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.08);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #c8cdd5 !important;
    }

    /* ---- Typography ---- */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
        color: #f0f2f5 !important;
    }

    h2 {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #dce0e6 !important;
    }

    h3 {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #c8cdd5 !important;
    }

    /* ---- Metric cards ---- */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(15, 18, 25, 0.95), rgba(20, 24, 33, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 20px 22px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(56, 189, 248, 0.2);
        box-shadow: 0 4px 24px rgba(56, 189, 248, 0.06);
        transform: translateY(-1px);
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', 'Inter', monospace !important;
        font-size: 1.65rem !important;
        font-weight: 600 !important;
        color: #f0f2f5 !important;
    }

    /* ---- Dataframe ---- */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        overflow: hidden;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(56, 189, 248, 0.08);
        color: #38bdf8;
        transition: all 0.25s ease;
        padding: 0.45rem 1rem;
    }

    .stButton > button:hover {
        background: rgba(56, 189, 248, 0.18);
        border-color: rgba(56, 189, 248, 0.3);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.1);
    }

    /* ---- Inputs ---- */
    input, textarea {
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
        transition: border-color 0.2s ease !important;
    }

    input:focus, textarea:focus {
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.08) !important;
    }

    /* ---- Selectbox ---- */
    div[data-testid="stSelectbox"] > div > div {
        border-radius: 8px;
    }

    /* ---- Expander ---- */
    details {
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        background: rgba(15, 18, 25, 0.6) !important;
    }

    /* ---- Horizontal rules ---- */
    hr {
        border-color: rgba(255, 255, 255, 0.05);
    }

    /* ---- Custom classes ---- */
    .header-banner {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.08) 0%, rgba(139, 92, 246, 0.06) 50%, rgba(244, 63, 94, 0.05) 100%);
        border: 1px solid rgba(56, 189, 248, 0.1);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .header-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #38bdf8, #8b5cf6, #f43f5e, #38bdf8);
        background-size: 200% 100%;
        animation: gradient-shift 4s linear infinite;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #f0f2f5;
        letter-spacing: -0.03em;
        margin: 0 0 6px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .header-subtitle {
        color: #6b7280;
        font-size: 0.82rem;
        font-weight: 400;
        margin: 0;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #34d399;
        box-shadow: 0 0 8px rgba(52, 211, 153, 0.5);
        animation: pulse-dot 2s ease-in-out infinite;
    }

    @keyframes pulse-dot {
        0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(52, 211, 153, 0.5); }
        50% { opacity: 0.6; box-shadow: 0 0 16px rgba(52, 211, 153, 0.3); }
    }

    .status-dot-error {
        background: #f43f5e;
        box-shadow: 0 0 8px rgba(244, 63, 94, 0.5);
        animation: pulse-dot-error 1.5s ease-in-out infinite;
    }

    @keyframes pulse-dot-error {
        0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(244, 63, 94, 0.5); }
        50% { opacity: 0.6; box-shadow: 0 0 16px rgba(244, 63, 94, 0.3); }
    }

    .section-label {
        color: #6b7280;
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .section-label::before {
        content: '';
        display: inline-block;
        width: 3px;
        height: 14px;
        border-radius: 2px;
        background: linear-gradient(180deg, #38bdf8, #8b5cf6);
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }

    .sidebar-brand-icon {
        font-size: 1.4rem;
    }

    .sidebar-brand-text {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: #f0f2f5;
        letter-spacing: -0.02em;
    }

    .sidebar-status {
        color: #6b7280;
        font-size: 0.75rem;
        font-weight: 400;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .sidebar-section-label {
        color: #4b5563;
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.3rem;
        margin-top: 0.2rem;
    }

    .metric-card-total {
        border-left: 3px solid #38bdf8 !important;
    }

    .metric-card-failed {
        border-left: 3px solid #f43f5e !important;
    }

    .metric-card-success {
        border-left: 3px solid #34d399 !important;
    }

    .metric-card-rate {
        border-left: 3px solid #fbbf24 !important;
    }

    .chart-container {
        background: rgba(15, 18, 25, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        transition: border-color 0.3s ease;
    }

    .chart-container:hover {
        border-color: rgba(56, 189, 248, 0.12);
    }

    .alert-banner {
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }

    .footer-text {
        color: #374151;
        font-size: 0.7rem;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.15);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Plotly theme defaults
# ---------------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#9ca3af", size=12),
    margin=dict(l=0, r=0, t=30, b=0),
    hoverlabel=dict(
        bgcolor="#1e2130",
        bordercolor="rgba(56,189,248,0.3)",
        font=dict(family="Inter, sans-serif", color="#f0f2f5", size=13),
    ),
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.markdown(
    '<div class="sidebar-brand">'
    '  <span class="sidebar-brand-icon">🛡️</span>'
    '  <span class="sidebar-brand-text">Security Monitor</span>'
    "</div>",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    '<div class="sidebar-status">'
    '  <span class="status-dot"></span>'
    "  Monitoring active"
    "</div>",
    unsafe_allow_html=True,
)

st.sidebar.divider()

st.sidebar.markdown(
    '<div class="sidebar-section-label">Connection</div>',
    unsafe_allow_html=True,
)

api_url = st.sidebar.text_input(
    "API endpoint",
    "http://localhost:8000/api/v1/logs",
    label_visibility="collapsed",
)

col_sb1, col_sb2 = st.sidebar.columns(2)

refresh_clicked = col_sb1.button(
    "⟳ Refresh",
    use_container_width=True,
)

auto_refresh = col_sb2.checkbox(
    "Auto-poll",
    value=False,
)

if auto_refresh:
    import time

    time.sleep(5)
    st.rerun()

st.sidebar.divider()

# ---------------------------------------------------------
# Simulation
# ---------------------------------------------------------
st.sidebar.markdown(
    '<div class="sidebar-section-label">Event simulation</div>',
    unsafe_allow_html=True,
)

sim_user = st.sidebar.text_input(
    "Target user",
    "admin",
)

sim_workstation = st.sidebar.text_input(
    "Workstation",
    "WORKSTATION-01",
)

sb_btn1, sb_btn2 = st.sidebar.columns(2)

if sb_btn1.button(
    "⚠ Failed",
    use_container_width=True,
    help="Simulate a failed logon event (4625)",
):
    try:
        payload = {
            "event_id": 4625,
            "time": datetime.now().isoformat(),
            "inserts": [sim_user, sim_workstation],
        }

        res = requests.post(
            f"{api_url}/failed_login",
            json=payload,
            timeout=3,
        )

        if res.status_code == 200:
            st.sidebar.success("Event sent.")
            st.rerun()
        else:
            st.sidebar.error(f"API returned {res.status_code}")

    except Exception as e:
        st.sidebar.error(f"Request failed: {e}")


if sb_btn2.button(
    "✓ Success",
    use_container_width=True,
    help="Simulate a successful logon event (4624)",
):
    try:
        payload = {
            "event_id": 4624,
            "time": datetime.now().isoformat(),
            "inserts": [sim_user, sim_workstation],
        }

        res = requests.post(
            f"{api_url}/successful_login",
            json=payload,
            timeout=3,
        )

        if res.status_code == 200:
            st.sidebar.success("Event sent.")
            st.rerun()
        else:
            st.sidebar.error(f"API returned {res.status_code}")

    except Exception as e:
        st.sidebar.error(f"Request failed: {e}")


# ---------------------------------------------------------
# Fetch logs
# ---------------------------------------------------------
@st.cache_data(ttl=2)
def fetch_logs(url: str):
    try:
        resp = requests.get(
            f"{url}/logs",
            timeout=4,
        )

        if resp.status_code == 200:
            return resp.json()

    except requests.exceptions.ConnectionError:
        return None

    except Exception:
        return None

    return None


data_resp = fetch_logs(api_url)

# ---------------------------------------------------------
# Connection error state
# ---------------------------------------------------------
if data_resp is None:
    st.markdown(
        '<div class="header-banner">'
        '  <div class="header-title">🛡️ Windows Security Monitor</div>'
        '  <p class="header-subtitle">Windows authentication event monitoring — Event IDs 4624 / 4625</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.error(
        f"Unable to connect to the API at `{api_url}/logs`."
    )

    st.caption(
        "Make sure the FastAPI service is running and the endpoint is correct."
    )

    # Update sidebar status to disconnected
    st.sidebar.markdown(
        '<div class="sidebar-status">'
        '  <span class="status-dot status-dot-error"></span>'
        "  Disconnected"
        "</div>",
        unsafe_allow_html=True,
    )

    st.stop()

# ---------------------------------------------------------
# Parse response
# ---------------------------------------------------------
logs = data_resp.get("data", [])
total_count = data_resp.get("total", len(logs))

if not logs:
    st.markdown(
        '<div class="header-banner">'
        '  <div class="header-title">🛡️ Windows Security Monitor</div>'
        '  <p class="header-subtitle">Windows authentication event monitoring — Event IDs 4624 / 4625</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.info(
        "No authentication events have been recorded yet. "
        "Use the sidebar to simulate events."
    )

    st.stop()

processed_rows = []

for entry in logs:

    event_id = entry.get("event_id")

    inserts = entry.get("inserts", [])

    user = (
        inserts[0]
        if len(inserts) > 0
        else "Unknown"
    )

    workstation = (
        inserts[1]
        if len(inserts) > 1
        else "N/A"
    )

    if event_id == 4625:
        status = "🔴 Failed"
    elif event_id == 4624:
        status = "🟢 Success"
    else:
        status = "⚪ Other"

    processed_rows.append(
        {
            "Status": status,
            "Event ID": event_id,
            "Timestamp": entry.get("time", ""),
            "Target User": user,
            "Workstation": workstation,
            "All Inserts": str(inserts),
        }
    )

df = pd.DataFrame(processed_rows)

# ---------------------------------------------------------
# Header banner
# ---------------------------------------------------------
st.markdown(
    '<div class="header-banner">'
    '  <div class="header-title">'
    "    🛡️ Windows Security Monitor"
    "  </div>"
    '  <p class="header-subtitle">'
    "    Windows authentication events · Event IDs 4624 / 4625 · "
    f"    Last refreshed {datetime.now().strftime('%H:%M:%S')}"
    "  </p>"
    "</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Metrics row
# ---------------------------------------------------------
failed_count = (df["Event ID"] == 4625).sum()
success_count = (df["Event ID"] == 4624).sum()

fail_rate = (
    failed_count / total_count * 100
    if total_count > 0
    else 0
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown('<div class="metric-card-total">', unsafe_allow_html=True)
    st.metric("Total Events", f"{total_count:,}")
    st.markdown("</div>", unsafe_allow_html=True)

with m2:
    st.markdown('<div class="metric-card-failed">', unsafe_allow_html=True)
    st.metric("Failed Logons", f"{failed_count:,}")
    st.markdown("</div>", unsafe_allow_html=True)

with m3:
    st.markdown('<div class="metric-card-success">', unsafe_allow_html=True)
    st.metric("Successful Logons", f"{success_count:,}")
    st.markdown("</div>", unsafe_allow_html=True)

with m4:
    st.markdown('<div class="metric-card-rate">', unsafe_allow_html=True)
    st.metric("Failure Rate", f"{fail_rate:.1f}%")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Security alert
# ---------------------------------------------------------
st.write("")

if failed_count >= 5:
    st.markdown(
        '<div class="alert-banner">',
        unsafe_allow_html=True,
    )
    st.error(
        f"🚨  **Critical:** {failed_count} failed logon events detected — "
        f"possible brute-force activity."
    )
    st.markdown("</div>", unsafe_allow_html=True)

elif failed_count >= 3:
    st.markdown(
        '<div class="alert-banner">',
        unsafe_allow_html=True,
    )
    st.warning(
        f"⚠️  **Warning:** {failed_count} failed logon events — "
        f"investigate for potential unauthorized access attempts."
    )
    st.markdown("</div>", unsafe_allow_html=True)

elif failed_count > 0:
    st.info(
        f"ℹ️  {failed_count} failed logon event(s) recorded."
    )

else:
    st.success(
        "✅  No failed logon events — all clear."
    )

# ---------------------------------------------------------
# Charts row
# ---------------------------------------------------------
st.write("")

chart1, chart2, chart3 = st.columns([1, 1, 1])

# ---- Donut: event distribution ----
with chart1:
    st.markdown(
        '<div class="section-label">Event distribution</div>',
        unsafe_allow_html=True,
    )

    labels = []
    values = []
    colors = []

    if success_count > 0:
        labels.append("Successful")
        values.append(int(success_count))
        colors.append("#34d399")

    if failed_count > 0:
        labels.append("Failed")
        values.append(int(failed_count))
        colors.append("#f43f5e")

    other_count = total_count - int(success_count) - int(failed_count)
    if other_count > 0:
        labels.append("Other")
        values.append(other_count)
        colors.append("#6b7280")

    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.65,
                marker=dict(colors=colors, line=dict(color="#0a0c10", width=2)),
                textinfo="label+percent",
                textfont=dict(size=11, color="#d1d5db"),
                hovertemplate="<b>%{label}</b><br>%{value} events (%{percent})<extra></extra>",
            )
        ]
    )

    fig_donut.update_layout(
        **PLOTLY_LAYOUT,
        height=300,
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{total_count}</b><br><span style='font-size:10px;color:#6b7280'>total</span>",
                x=0.5,
                y=0.5,
                font=dict(size=22, color="#f0f2f5", family="Inter, sans-serif"),
                showarrow=False,
            )
        ],
    )

    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})


# ---- Bar: failed logons by account ----
with chart2:
    st.markdown(
        '<div class="section-label">Failed logons by account</div>',
        unsafe_allow_html=True,
    )

    # Clean status emoji prefix for filtering
    failed_df = df[df["Event ID"] == 4625]

    if not failed_df.empty:
        user_counts = (
            failed_df["Target User"]
            .value_counts()
            .head(8)
        )

        fig_bar = go.Figure(
            data=[
                go.Bar(
                    x=user_counts.values,
                    y=user_counts.index,
                    orientation="h",
                    marker=dict(
                        color=user_counts.values,
                        colorscale=[[0, "#fb7185"], [1, "#f43f5e"]],
                        line=dict(width=0),
                        cornerradius=4,
                    ),
                    hovertemplate="<b>%{y}</b><br>%{x} failures<extra></extra>",
                )
            ]
        )

        fig_bar.update_layout(
            **PLOTLY_LAYOUT,
            height=300,
            yaxis=dict(
                autorange="reversed",
                gridcolor="rgba(255,255,255,0.04)",
                zerolinecolor="rgba(255,255,255,0.04)",
            ),
            xaxis=dict(
                title="Failures",
                gridcolor="rgba(255,255,255,0.04)",
                zerolinecolor="rgba(255,255,255,0.04)",
            ),
        )

        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    else:
        st.caption("No failed logons recorded.")


# ---- Timeline: events over time ----
with chart3:
    st.markdown(
        '<div class="section-label">Event timeline</div>',
        unsafe_allow_html=True,
    )

    # Try to parse timestamps for timeline
    timeline_df = df.copy()
    timeline_df["parsed_time"] = pd.to_datetime(
        timeline_df["Timestamp"], errors="coerce"
    )

    valid_times = timeline_df.dropna(subset=["parsed_time"])

    if not valid_times.empty:
        # Bin events by minute
        valid_times = valid_times.copy()
        valid_times["minute"] = valid_times["parsed_time"].dt.floor("min")

        success_timeline = (
            valid_times[valid_times["Event ID"] == 4624]
            .groupby("minute")
            .size()
            .reset_index(name="count")
        )

        failed_timeline = (
            valid_times[valid_times["Event ID"] == 4625]
            .groupby("minute")
            .size()
            .reset_index(name="count")
        )

        fig_timeline = go.Figure()

        if not success_timeline.empty:
            fig_timeline.add_trace(
                go.Scatter(
                    x=success_timeline["minute"],
                    y=success_timeline["count"],
                    name="Success",
                    mode="lines+markers",
                    line=dict(color="#34d399", width=2, shape="spline"),
                    marker=dict(size=5, color="#34d399"),
                    fill="tozeroy",
                    fillcolor="rgba(52, 211, 153, 0.08)",
                    hovertemplate="<b>Success</b><br>%{x|%H:%M}<br>%{y} events<extra></extra>",
                )
            )

        if not failed_timeline.empty:
            fig_timeline.add_trace(
                go.Scatter(
                    x=failed_timeline["minute"],
                    y=failed_timeline["count"],
                    name="Failed",
                    mode="lines+markers",
                    line=dict(color="#f43f5e", width=2, shape="spline"),
                    marker=dict(size=5, color="#f43f5e"),
                    fill="tozeroy",
                    fillcolor="rgba(244, 63, 94, 0.08)",
                    hovertemplate="<b>Failed</b><br>%{x|%H:%M}<br>%{y} events<extra></extra>",
                )
            )

        fig_timeline.update_layout(
            **PLOTLY_LAYOUT,
            height=300,
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.04)",
                zerolinecolor="rgba(255,255,255,0.04)",
                tickformat="%H:%M",
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.04)",
                zerolinecolor="rgba(255,255,255,0.04)",
                title="Events",
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )

        st.plotly_chart(fig_timeline, use_container_width=True, config={"displayModeBar": False})
    else:
        st.caption("No timestamp data available for timeline.")


# ---------------------------------------------------------
# Event explorer
# ---------------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-label">Event explorer</div>',
    unsafe_allow_html=True,
)

col_f1, col_f2 = st.columns([1, 3])

filter_type = col_f1.selectbox(
    "Event type",
    [
        "All events",
        "🔴 Failed logons (4625)",
        "🟢 Successful logons (4624)",
    ],
)

search_query = col_f2.text_input(
    "Search events",
    placeholder="Filter by username, workstation, or timestamp…",
)

filtered_df = df.copy()

if "Failed" in filter_type:
    filtered_df = filtered_df[filtered_df["Event ID"] == 4625]

elif "Successful" in filter_type:
    filtered_df = filtered_df[filtered_df["Event ID"] == 4624]

if search_query:
    mask = (
        filtered_df["Target User"].str.contains(
            search_query, case=False, na=False,
        )
        | filtered_df["Workstation"].str.contains(
            search_query, case=False, na=False,
        )
        | filtered_df["Timestamp"].str.contains(
            search_query, case=False, na=False,
        )
    )
    filtered_df = filtered_df[mask]

# Show result count
st.markdown(
    f'<div style="color:#6b7280; font-size:0.75rem; margin-bottom:0.5rem;">'
    f"Showing {len(filtered_df)} of {total_count} events"
    f"</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Event table
# ---------------------------------------------------------
st.dataframe(
    filtered_df[
        [
            "Status",
            "Event ID",
            "Timestamp",
            "Target User",
            "Workstation",
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.TextColumn("Status", width="small"),
        "Event ID": st.column_config.NumberColumn("Event ID", format="%d", width="small"),
        "Timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
        "Target User": st.column_config.TextColumn("Target User", width="medium"),
        "Workstation": st.column_config.TextColumn("Workstation", width="medium"),
    },
)

# ---------------------------------------------------------
# Raw event data
# ---------------------------------------------------------
with st.expander("📄 Raw event data"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    '<div class="footer-text">'
    "Windows Security Monitor · Event Log Analysis Dashboard"
    "</div>",
    unsafe_allow_html=True,
)