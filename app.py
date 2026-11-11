import streamlit as st
import pandas as pd
import plotly.graph_objects as go

p = {
    "bg":             "#F4F7FB",   # soft off-white (like airline sites)
    "text":           "#1B2A41",   # deep navy text
    "muted":          "#5B6B7F",   # gray-blue for secondary text
    "card_bg":        "#FFFFFF",   # white inputs/cards
    "border":         "#D6DEE8",   # light border around cards
    "input_border":   "#B4C2D3",   # always-visible outline on inputs
    "stepper_bg":     "#EEF3F9",   # background of the - / + buttons
    "brand":          "#1D5FA8",   # main blue
    "accent":         "#E0A526",   # gold for the best bar
    "bar_default":    "#A9C4E4",   # light blue for other bars
    "callout_bg":     "#E8F5EE",
    "callout_border": "#2E9E6A",
    "callout_text":   "#1B2A41",
}

PROGRAMS = {
    "Credit Cards": {
        "Chase Ultimate Rewards": {
            "Flights (transfer partners)": 2.0,
            "Hotels (transfer partners)": 1.5,
            "Chase Travel portal": "1.25 – 1.50",
            "Cash back": 1.0,
        },
        "Amex Membership Rewards": {
            "Flights (transfer partners)": 2.0,
            "Hotels (transfer partners)": 1.4,
            "Amex Travel portal": 1.0,
            "Cash back": 0.6,
        },
        "Capital One Miles": {
            "Flights (transfer partners)": 1.7,
            "Hotels (transfer partners)": 1.4,
            "Capital One Travel portal": 1.0,
            "Cash back": 1.0,
        },
        "Citi ThankYou Points": {
            "Flights (transfer partners)": 1.6,
            "Hotels (transfer partners)": 1.3,
            "Citi Travel portal": 1.0,
            "Cash back": 0.5,
        },
        "Bilt Rewards": {
            "Flights (transfer partners)": 2.0,
            "Hotels (transfer partners)": 1.5,
            "Rent payments": 1.0,
            "Cash back": 0.55,
        },
    },
    "Airlines": {
        "Delta SkyMiles": {
            "Delta flights": 1.2,
            "Partner flights": 1.0,
            "Upgrades": 1.5,
            "Cash back": 0.5,
        },
        "United MileagePlus": {
            "United flights": 1.35,
            "Partner flights": 1.2,
            "Upgrades": 1.5,
            "Cash back": 0.5,
        },
        "American Airlines AAdvantage": {
            "AA flights": 1.67,
            "Partner flights": 1.2,
            "Upgrades": 1.4,
            "Cash back": 0.5,
        },
        "Southwest Rapid Rewards": {
            "Southwest flights": 1.5,
            "Hotel partners": 0.8,
            "Car rentals": 0.8,
            "Cash back": 0.6,
        },
        "Alaska Mileage Plan": {
            "Alaska flights": 1.8,
            "Partner flights": 1.6,
            "Upgrades": 1.5,
            "Cash back": 0.5,
        },
    },
    "Hotels": {
        "World of Hyatt": {
            "Hyatt hotels": 1.7,
            "Premium properties": 2.0,
            "Airline transfers": 1.0,
            "Cash back": 0.4,
        },
        "Marriott Bonvoy": {
            "Marriott hotels": 0.7,
            "Premium properties": 1.0,
            "Airline transfers": 0.7,
            "Cash back": 0.3,
        },
        "Hilton Honors": {
            "Hilton hotels": 0.5,
            "Premium properties": 0.8,
            "Airline transfers": 0.5,
            "Cash back": 0.2,
        },
    },
}

CPP_DATA = {k: v for group in PROGRAMS.values() for k, v in group.items()}

st.set_page_config(page_title="PointsWorth — Redeem Right", layout="wide", initial_sidebar_state="auto")

FONT_BODY = "'Inter', -apple-system, 'Segoe UI', sans-serif"
FONT_DISPLAY = "'DM Serif Display', Georgia, serif"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap');

    .stApp {{ background-color: {p['bg']}; }}
    [data-testid="stHeader"] {{ background-color: {p['bg']}; }}
    .block-container {{ padding-top: 4.5rem; padding-bottom: 4rem; max-width: 1180px; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{ background-color: {p['card_bg']}; border-right: 1px solid {p['border']}; }}
    [data-testid="stSidebar"] [data-testid="stExpander"] details {{ border: none !important; }}

    /* Tabs */
    [data-baseweb="tab-list"] {{ gap: 1.75rem; border-bottom: 1px solid {p['border']}; }}
    /* Each tab is at least a screen tall, so switching tabs never snaps the page back up */
    [data-baseweb="tab-panel"] {{ min-height: 90vh; }}
    [data-baseweb="tab"] p {{ font-size: 1.02rem !important; font-weight: 600; }}
    [data-baseweb="tab-highlight"] {{ background-color: {p['brand']} !important; }}

    /* Input panel card (left column) */
    .st-key-input_panel, .st-key-finder_panel {{
        background: {p['card_bg']}; border: 1px solid {p['border']}; border-radius: 14px; padding: 1.1rem 1.2rem;
    }}
    .pw-group {{
        font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
        color: {p['muted']}; margin: 0.6rem 0 -0.3rem;
    }}

    /* Fonts — Inter for body text, DM Serif Display for headings.
       (Spans are left alone so Streamlit's arrow icons keep their icon font.) */
    .stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp button,
    [data-testid="stMarkdownContainer"] {{ font-family: {FONT_BODY}; }}
    h1, h2, h3, h4 {{ font-family: {FONT_DISPLAY} !important; font-weight: 400 !important; }}

    /* Text */
    p, li, label, span {{ color: {p['text']} !important; }}
    h1, h2, h3, h4 {{ color: {p['text']} !important; }}
    hr {{ border-color: {p['border']} !important; }}

    /* Metrics as white cards */
    [data-testid="stMetric"] {{
        background: {p['card_bg']}; border: 1px solid {p['border']};
        border-radius: 12px; padding: 0.9rem 1.1rem;
    }}
    [data-testid="stMetricValue"] > div {{ color: {p['text']} !important; font-weight: 600; }}
    [data-testid="stMetricLabel"] > div {{ color: {p['muted']} !important; }}
    [data-testid="stMetricDelta"] {{ color: {p['muted']} !important; }}

    /* Expanders as white cards */
    [data-testid="stExpander"] details {{
        background: {p['card_bg']}; border: 1px solid {p['border']} !important; border-radius: 12px;
    }}

    /* Dropdowns and inputs */
    [data-baseweb="select"] > div {{ background-color: {p['card_bg']} !important; border: 1px solid {p['input_border']} !important; }}
    [data-baseweb="select"] * {{ color: {p['text']} !important; }}
    [data-baseweb="popover"] {{ background-color: {p['card_bg']} !important; }}
    [data-baseweb="menu"] {{ background-color: {p['card_bg']} !important; }}
    [data-baseweb="option"] {{ background-color: {p['card_bg']} !important; color: {p['text']} !important; }}
    [data-baseweb="option"]:hover {{ background-color: #E6EEF8 !important; }}
    [data-testid="stNumberInput"] input {{
        background-color: {p['card_bg']} !important;
        color: {p['text']} !important;
    }}
    /* Outline is always visible (not only on hover) */
    [data-testid="stNumberInputContainer"] {{
        border: 1px solid {p['input_border']} !important; border-radius: 8px; overflow: hidden;
    }}
    [data-testid="stNumberInputContainer"]:focus-within {{ border-color: {p['brand']} !important; }}
    [data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"] {{
        background-color: {p['stepper_bg']} !important; border-left: 1px solid {p['input_border']} !important;
    }}

    /* Calculate buttons */
    [data-testid="stFormSubmitButton"] button {{
        border-radius: 8px; font-weight: 600; padding: 0.55rem 1rem;
        background-color: {p['brand']} !important; border: 1px solid {p['brand']} !important;
    }}
    [data-testid="stFormSubmitButton"] button:hover {{ background-color: #174D89 !important; border-color: #174D89 !important; }}
    [data-testid="stFormSubmitButton"] button p {{ color: #FFFFFF !important; }}

    /* Selected program tags in the multiselect */
    [data-baseweb="tag"] {{ background-color: {p['brand']} !important; }}
    [data-baseweb="tag"] span, [data-baseweb="tag"] svg {{ color: #FFFFFF !important; fill: #FFFFFF !important; }}

    .stCaption p {{ color: {p['muted']} !important; }}

    /* Hero */
    .pw-hero {{
        position: relative; overflow: hidden;
        background: {p['card_bg']}; border: 1px solid {p['border']}; border-radius: 16px;
        padding: 1.4rem 1.75rem 1.3rem; margin-bottom: 0.75rem;
    }}
    .pw-hero-art {{ position: absolute; right: -10px; top: 0; width: 320px; height: 140px; pointer-events: none; }}
    .pw-brand {{ display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1.1rem; }}
    .pw-wordmark {{ font-family: {FONT_BODY}; font-weight: 700; font-size: 1.05rem; letter-spacing: -0.01em; color: {p['text']}; }}
    .pw-headline {{ font-family: {FONT_DISPLAY}; font-size: 2.6rem; line-height: 1.1; color: {p['text']}; margin: 0 0 0.6rem; }}
    .pw-headline em {{ font-style: normal; color: {p['brand']}; }}
    .pw-lede {{ font-size: 0.98rem !important; line-height: 1.7; color: {p['muted']} !important; margin: 0; max-width: 34rem; }}
    @media (max-width: 640px) {{
        .pw-hero-art {{ opacity: 0.35; }}
        .pw-headline {{ font-size: 2rem; }}
    }}

    /* Section headings */
    .pw-eyebrow {{
        font-size: 0.72rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase;
        color: {p['brand']}; margin: 0.5rem 0 0.15rem;
    }}
    .pw-section {{ font-family: {FONT_DISPLAY}; font-size: 1.75rem; line-height: 1.2; color: {p['text']}; margin-bottom: 0.4rem; }}
    .pw-blurb {{ font-size: 0.95rem !important; color: {p['muted']} !important; margin: 0 0 0.75rem; }}

    /* Callout */
    .pw-callout {{
        display: flex; gap: 0.85rem; align-items: flex-start;
        background: {p['callout_bg']}; border: 1px solid #CBE8D8; border-left: 4px solid {p['callout_border']};
        border-radius: 10px; padding: 0.85rem 1.1rem; margin: 0.5rem 0 1rem; color: {p['callout_text']};
    }}
    .pw-callout-label {{
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
        color: {p['callout_border']}; margin-bottom: 0.15rem;
    }}
    .pw-callout-body {{ font-size: 0.98rem; line-height: 1.5; }}
</style>
""", unsafe_allow_html=True)

# --- Small graphics (inline SVG, so no image files needed) ---

# Logo: blue tile with a dotted gold flight path ending in a gold "point"
LOGO_SVG = f"""<svg width="34" height="34" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect width="34" height="34" rx="9" fill="{p['brand']}"/>
<path d="M7 25 C 12 25, 15 11, 26 9" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="0.5 4"/>
<circle cx="26" cy="9" r="3.2" fill="{p['accent']}"/>
</svg>"""

# Hero decoration: a faint dashed flight arc across the top-right corner
HERO_ART_SVG = f"""<svg class="pw-hero-art" viewBox="0 0 320 140" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<path d="M20 150 Q 170 -10 330 40" stroke="{p['brand']}" stroke-opacity="0.18" stroke-width="2" fill="none" stroke-dasharray="6 7"/>
<path d="M90 150 Q 220 30 330 95" stroke="{p['accent']}" stroke-opacity="0.35" stroke-width="2" fill="none" stroke-dasharray="6 7"/>
<circle cx="236" cy="38" r="5" fill="{p['accent']}" fill-opacity="0.85"/>
<circle cx="236" cy="38" r="11" fill="{p['accent']}" fill-opacity="0.15"/>
</svg>"""

# Small check icon for callouts
CHECK_SVG = f"""<svg width="22" height="22" viewBox="0 0 22 22" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="flex-shrink:0;margin-top:2px">
<circle cx="11" cy="11" r="11" fill="{p['callout_border']}"/>
<path d="M6.5 11.5 L9.5 14.5 L15.5 8" stroke="#FFFFFF" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def html(markup):
    """Render raw HTML. Lines are stripped so Markdown doesn't mistake indented HTML for a code block."""
    st.markdown("\n".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


def section(eyebrow, title, blurb=None):
    """Small blue label above a serif heading — used for each section of the page."""
    blurb_html = f'<p class="pw-blurb">{blurb}</p>' if blurb else ""
    html(f'<div class="pw-eyebrow">{eyebrow}</div><div class="pw-section">{title}</div>{blurb_html}')


def callout(label, body):
    """Green highlight box with a check icon."""
    html(f"""<div class="pw-callout">{CHECK_SVG}<div>
<div class="pw-callout-label">{label}</div>
<div class="pw-callout-body">{body}</div>
</div></div>""")


# --- Hero ---
html(f"""
<div class="pw-hero">
    {HERO_ART_SVG}
    <div class="pw-brand">{LOGO_SVG}<div class="pw-wordmark">PointsWorth</div></div>
    <div class="pw-headline">Redeem <em>right.</em></div>
    <p class="pw-lede">
        Hi, I built this site to show what your loyalty points are really worth.
        Enter a balance and it's converted into cents per point (CPP) across flights, hotels and cash back,
        so you can compare programs that otherwise can't be compared side by side.
    </p>
</div>
""")

# --- Sidebar: background info, pull-out on demand ---
with st.sidebar:
    html(f"""<div class="pw-brand" style="margin:0.25rem 0 0.75rem">{LOGO_SVG}<div class="pw-wordmark">PointsWorth</div></div>
<p class="pw-blurb">Background on the numbers and how this app was made.</p>""")
    with st.expander("How does this work?"):
        st.markdown(f"""
<div style="font-size: 14px; line-height: 1.7; color: {p['text']};">

<p><strong>What is CPP (cents per point)?</strong></p>

<p>Loyalty programs all use different point currencies, so 50,000 Delta miles and 50,000 Chase points
aren't worth the same — even though they're the same number. CPP converts everything into a common
unit: cents per point.</p>

<p>The formula is simple: <strong>(dollar value of what you're getting ÷ points used) × 100 = CPP</strong></p>

<p>For example: if 50,000 points gets you a flight worth $750, that's <strong>1.5 CPP</strong>.
If those same points gets you $500 cash back, that's only <strong>1.0 CPP</strong>.
Higher CPP = more value per point.</p>

<p><strong>Where do the estimates come from?</strong></p>

<p>The CPP values used here are widely published estimates based on typical redemption rates across
the travel community. They reflect realistic (not best-case) redemption scenarios. Your actual value
may be higher or lower depending on the specific redemption you find.</p>

<p><strong>What does a CPP range mean?</strong></p>

<p>Some programs show a range (e.g. "1.25 – 1.50 CPP") for portal bookings. This reflects different
card tiers — for example, Chase Sapphire Preferred earns 1.25 CPP on the Chase Travel portal while
Chase Sapphire Reserve earns 1.50 CPP.</p>

</div>
""", unsafe_allow_html=True)

    with st.expander("How was this built?"):
        st.markdown(f"""
<div style="font-size: 14px; line-height: 1.7; color: {p['text']};">

<p>This app was built in Python using three open-source libraries:</p>

<ul>
  <li><strong>Streamlit</strong> — handles the web interface: layout, inputs, and interactivity</li>
  <li><strong>Pandas</strong> — organizes and processes the redemption data as a table</li>
  <li><strong>Plotly</strong> — draws the interactive bar chart</li>
</ul>

<p>The CPP values are hardcoded estimates based on widely published redemption rates across the travel
community. The app was designed and built with the assistance of Claude, an AI assistant made by
Anthropic. It is deployed for free on Streamlit Community Cloud and version-controlled on GitHub.</p>

</div>
""", unsafe_allow_html=True)

tab_value, tab_finder = st.tabs(["Value my points", "Best Program Finder"])

# ============ Tab 1: value one program ============
with tab_value:
    left, right = st.columns([1, 2.1], gap="large")

    with left:
        with st.container(key="input_panel"):
            section("Step 1", "Choose your program")
            category = st.selectbox("Category", list(PROGRAMS.keys()))
            program = st.selectbox("Program", list(PROGRAMS[category].keys()))
            # A form waits for the button (or Enter) before recalculating
            with st.form("value_form", border=False):
                points = st.number_input("How many points do you have?", min_value=0, step=1000, value=50000)
                st.form_submit_button("Calculate value", type="primary", width="stretch")

    with right:
        if points > 0:
            redemptions = CPP_DATA[program]

            rows = []
            range_notes = []
            for redemption_type, cpp in redemptions.items():
                if isinstance(cpp, str):
                    low, high = [float(x.strip()) for x in cpp.split("–")]
                    cpp_mid = (low + high) / 2
                    dollar_low = round(points * low / 100, 2)
                    dollar_high = round(points * high / 100, 2)
                    range_notes.append(redemption_type)
                    rows.append({
                        "Redemption Type": redemption_type,
                        "CPP": cpp + "¢ *",
                        "Estimated Value ($)": f"${dollar_low:,.0f} – ${dollar_high:,.0f} *",
                        "_sort": cpp_mid,
                    })
                else:
                    dollar_value = round(points * cpp / 100, 2)
                    rows.append({
                        "Redemption Type": redemption_type,
                        "CPP": f"{cpp:.2f}¢",
                        "Estimated Value ($)": f"${dollar_value:,.0f}",
                        "_sort": cpp,
                    })

            rows_sorted = sorted(rows, key=lambda r: r["_sort"], reverse=True)
            df = pd.DataFrame(rows_sorted).drop(columns="_sort")

            best = rows_sorted[0]
            worst = rows_sorted[-1]

            section("Step 2", "What your points are worth", f"{points:,} {program} points, ranked by value.")
            callout(
                "Best redemption",
                f"<strong>{best['Redemption Type']}</strong> — "
                f"{best['Estimated Value ($)'].replace(' *', '')} at {best['CPP'].replace(' *', '')} per point",
            )

            worst_val_str = worst["Estimated Value ($)"].replace(" *", "").replace("$", "").replace(",", "").split("–")[0].strip()
            best_val_str = best["Estimated Value ($)"].replace(" *", "").replace("$", "").replace(",", "").split("–")[-1].strip()
            try:
                diff = float(best_val_str) - float(worst_val_str)
                diff_str = f"${diff:,.0f}"
            except ValueError:
                diff_str = "—"

            m1, m2, m3 = st.columns(3)
            m1.metric(f"Best: {best['Redemption Type']}", best["Estimated Value ($)"].replace(" *", ""), best["CPP"].replace(" *", "") + " per point")
            m2.metric(f"Worst: {worst['Redemption Type']}", worst["Estimated Value ($)"].replace(" *", ""), worst["CPP"].replace(" *", "") + " per point")
            m3.metric("Difference", diff_str, "best vs worst")

            # Chart — accent for best bar, bar_default for the rest
            chart_rows = []
            for r in rows_sorted:
                val_str = r["Estimated Value ($)"].replace(" *", "")
                if "–" in val_str:
                    parts = [float(x.replace("$", "").replace(",", "").strip()) for x in val_str.split("–")]
                    chart_rows.append({"Redemption Type": r["Redemption Type"], "Value": sum(parts) / len(parts), "Label": val_str})
                else:
                    chart_rows.append({"Redemption Type": r["Redemption Type"], "Value": float(val_str.replace("$", "").replace(",", "")), "Label": val_str})

            chart_df = pd.DataFrame(chart_rows)
            bar_colors = [p["accent"]] + [p["bar_default"]] * (len(chart_df) - 1)

            fig = go.Figure(go.Bar(
                x=chart_df["Redemption Type"],
                y=chart_df["Value"],
                marker_color=bar_colors,
                text=chart_df["Label"],
                textposition="outside",
                textfont=dict(color=p["text"]),
                cliponaxis=False,
            ))
            fig.update_layout(
                height=330,
                yaxis_title="Estimated Value (USD)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=13, color=p["text"]),
                yaxis=dict(color=p["text"], gridcolor=p["border"], fixedrange=True),  # fixedrange = no zoom/drag
                xaxis=dict(color=p["text"], fixedrange=True),
                dragmode=False,
                margin=dict(t=30, b=10, l=10, r=10),
            )
            st.plotly_chart(fig, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False})

            with st.expander("Full breakdown"):
                st.dataframe(df[["Redemption Type", "CPP", "Estimated Value ($)"]], width="stretch", hide_index=True)

            if range_notes:
                st.caption(f"* Range for {', '.join(range_notes)} reflects card tiers — value depends on which card you hold.")

        else:
            st.info("Enter your point balance to see redemption values.")

# ============ Tab 2: compare every program you hold ============
with tab_finder:
    left, right = st.columns([1.25, 1.85], gap="large")

    balances = {}
    with left:
        with st.container(key="finder_panel"):
            section("Your balances", "What do you hold?", "Pick your programs, then enter each balance.")
            held = st.multiselect(
                "Programs you hold",
                options=list(CPP_DATA.keys()),
                placeholder="Choose one or more programs",
            )
            if held:
                with st.form("finder_form", border=False):
                    for prog in held:
                        val = st.number_input(prog, min_value=0, step=1000, value=None,
                                              placeholder="e.g. 60,000", key=f"bal_{prog}")
                        if val:
                            balances[prog] = val
                    st.form_submit_button("Find my best program", type="primary", width="stretch")

    with right:
        section("Compare", "Best Program Finder",
                "We rank every redemption across your programs so you know which to use for your next trip.")
        if balances:
            results = []
            for prog, pts in balances.items():
                for redemption_type, cpp in CPP_DATA[prog].items():
                    if isinstance(cpp, str):
                        low, high = [float(x.strip()) for x in cpp.split("–")]
                        cpp_val = (low + high) / 2
                    else:
                        cpp_val = cpp
                    dollar_value = round(pts * cpp_val / 100)
                    results.append({
                        "Program": prog,
                        "Redemption Type": redemption_type,
                        "Points": f"{pts:,}",
                        "Est. Value ($)": f"${dollar_value:,}",
                        "_sort": dollar_value,
                    })

            results_sorted = sorted(results, key=lambda r: r["_sort"], reverse=True)
            top = results_sorted[0]

            callout(
                "Best overall",
                f"<strong>{top['Program']}</strong> — {top['Redemption Type']} — "
                f"{top['Est. Value ($)']} from {top['Points']} points",
            )

            results_df = pd.DataFrame(results_sorted).drop(columns="_sort")
            st.dataframe(results_df, width="stretch", hide_index=True)
        else:
            st.info("Choose your programs on the left, enter balances, then click **Find my best program**.")

    # Blank space at the bottom so this tab can always scroll, even before anything is entered
    html('<div style="height: 60vh"></div>')
