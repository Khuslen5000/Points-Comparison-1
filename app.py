import streamlit as st
import pandas as pd
import plotly.graph_objects as go

NAVY = "#1B2A41"
GOLD = "#C9A84C"

PROGRAMS = {
    "💳 Credit Cards": {
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
    "✈️ Airlines": {
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
    "🏨 Hotels": {
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

BENCHMARKS = {
    "Chase Ultimate Rewards":       {"range": "1.5 – 2.0¢", "note": "Strong via transfer partners"},
    "Amex Membership Rewards":      {"range": "1.4 – 2.0¢", "note": "Best via airline transfers"},
    "Capital One Miles":            {"range": "1.4 – 1.7¢", "note": "Solid via transfer partners"},
    "Citi ThankYou Points":         {"range": "1.2 – 1.6¢", "note": "Best via premium airlines"},
    "Bilt Rewards":                 {"range": "1.5 – 2.0¢", "note": "Great program for renters"},
    "Delta SkyMiles":               {"range": "1.0 – 1.5¢", "note": "Variable — shop for awards"},
    "United MileagePlus":           {"range": "1.2 – 1.5¢", "note": "Strong for international"},
    "American Airlines AAdvantage": {"range": "1.2 – 1.7¢", "note": "Good for domestic awards"},
    "Southwest Rapid Rewards":      {"range": "1.3 – 1.5¢", "note": "Consistent domestic value"},
    "Alaska Mileage Plan":          {"range": "1.4 – 1.8¢", "note": "Top tier for partner awards"},
    "World of Hyatt":               {"range": "1.5 – 2.0¢", "note": "Best hotel program by CPP"},
    "Marriott Bonvoy":              {"range": "0.6 – 0.9¢", "note": "Large network, lower CPP"},
    "Hilton Honors":                {"range": "0.4 – 0.6¢", "note": "Best for free night certs"},
}

CPP_DATA = {k: v for group in PROGRAMS.values() for k, v in group.items()}

st.set_page_config(page_title="Points & Miles Comparator", layout="centered")

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stMetric { background-color: #F0EBE0; border-radius: 8px; padding: 0.5rem; }
    .stCaption p { color: #4A5568 !important; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("✈️ Points & Miles Comparator")
st.markdown(f"""
<p style="font-size: 1.3rem; font-weight: 600; color: {NAVY}; margin-bottom: 0.25rem;">
    See what your points are actually worth.
</p>
<p style="font-size: 0.97rem; color: #4A5568; line-height: 1.7; margin-top: 0;">
    Hi, I'm Khuslen. This site converts your loyalty points balance into cents per point
    (CPP — how much each point is actually worth) across redemption options — flights, hotels,
    cash back — so you can compare programs that otherwise can't be compared directly.
    Enter your balance below to find out.
</p>
""", unsafe_allow_html=True)

st.divider()

with st.expander("📖 How does this work?"):
    st.markdown("""
<div style="font-family: sans-serif; font-size: 15px; line-height: 1.7;">

<p><strong>What is CPP (cents per point)?</strong></p>

<p>Loyalty programs all use different point currencies, so 50,000 Delta miles and 50,000 Chase points aren't worth the same — even though they're the same number. CPP converts everything into a common unit: cents per point.</p>

<p>The formula is simple: <strong>(dollar value of what you're getting ÷ points used) × 100 = CPP</strong></p>

<p>For example: if 50,000 points gets you a flight worth $750, that's <strong>1.5 CPP</strong>. If those same points gets you $500 cash back, that's only <strong>1.0 CPP</strong>. Higher CPP = more value per point.</p>

<p><strong>Where do the estimates come from?</strong></p>

<p>The CPP values used here are widely published estimates based on typical redemption rates across the travel community. They reflect realistic (not best-case) redemption scenarios. Your actual value may be higher or lower depending on the specific redemption you find.</p>

<p><strong>What does a CPP range mean?</strong></p>

<p>Some programs show a range (e.g. "1.25 – 1.50 CPP") for portal bookings. This reflects different card tiers — for example, Chase Sapphire Preferred earns 1.25 CPP on the Chase Travel portal while Chase Sapphire Reserve earns 1.50 CPP.</p>

</div>
""", unsafe_allow_html=True)

with st.expander("🛠️ How was this built?"):
    st.markdown("""
<div style="font-family: sans-serif; font-size: 15px; line-height: 1.7;">

<p>This app was built in Python using three open-source libraries:</p>

<ul>
  <li><strong>Streamlit</strong> — handles the web interface: layout, inputs, and interactivity</li>
  <li><strong>Pandas</strong> — organizes and processes the redemption data as a table</li>
  <li><strong>Plotly</strong> — draws the interactive bar chart</li>
</ul>

<p>The CPP values are hardcoded estimates based on widely published redemption rates across the travel community. The app was designed and built with the assistance of Claude, an AI assistant made by Anthropic. It is deployed for free on Streamlit Community Cloud and version-controlled on GitHub.</p>

</div>
""", unsafe_allow_html=True)

st.subheader("Select your program")

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Category", list(PROGRAMS.keys()))
with col2:
    program = st.selectbox("Program", list(PROGRAMS[category].keys()))

points = st.number_input("How many points do you have?", min_value=0, step=1000, value=50000)

st.divider()

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

    # Best redemption callout (sage/mint, not green)
    st.markdown(f"""
<div style="background-color: #E8F2EC; border-left: 4px solid #2D6A4F;
            padding: 0.75rem 1rem; border-radius: 6px; color: #1B4332;
            font-size: 0.95rem; margin-bottom: 1rem;">
    💡 <strong>Best redemption: {best['Redemption Type']}</strong> —
    {best['Estimated Value ($)'].replace(' *','')} at {best['CPP'].replace(' *','')} per point
</div>
""", unsafe_allow_html=True)

    # Metrics: best | worst | difference
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

    st.markdown("####")

    # Chart — gold for best bar, navy for the rest
    chart_rows = []
    for r in rows_sorted:
        val_str = r["Estimated Value ($)"].replace(" *", "")
        if "–" in val_str:
            parts = [float(x.replace("$", "").replace(",", "").strip()) for x in val_str.split("–")]
            mid = sum(parts) / len(parts)
            chart_rows.append({"Redemption Type": r["Redemption Type"], "Value": mid, "Label": val_str})
        else:
            v = float(val_str.replace("$", "").replace(",", ""))
            chart_rows.append({"Redemption Type": r["Redemption Type"], "Value": v, "Label": val_str})

    chart_df = pd.DataFrame(chart_rows)
    bar_colors = [GOLD] + [NAVY] * (len(chart_df) - 1)

    fig = go.Figure(go.Bar(
        x=chart_df["Redemption Type"],
        y=chart_df["Value"],
        marker_color=bar_colors,
        text=chart_df["Label"],
        textposition="outside",
        textfont=dict(color=NAVY),
    ))
    fig.update_layout(
        yaxis_title="Estimated Value (USD)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", size=13, color=NAVY),
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Full breakdown**")
    st.dataframe(df[["Redemption Type", "CPP", "Estimated Value ($)"]], use_container_width=True, hide_index=True)

    if range_notes:
        st.caption(f"* Range shown for {', '.join(range_notes)} reflects different card tiers — value depends on which card you hold.")

else:
    st.info("Enter your point balance above to see redemption values.")
