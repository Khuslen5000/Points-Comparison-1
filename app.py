import streamlit as st
import pandas as pd
import plotly.express as px

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

# Flat lookup for display
CPP_DATA = {k: v for group in PROGRAMS.values() for k, v in group.items()}

st.set_page_config(page_title="Points & Miles Comparator", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #f8f9fb; }
        h1 { color: #1a1a2e; }
        h2, h3 { color: #16213e; }
    </style>
""", unsafe_allow_html=True)

st.title("✈️ Points & Miles Comparator")
st.markdown("Find out how much your loyalty points are actually worth — and where you'll get the most value.")

st.markdown("""
<div style="font-family: sans-serif; font-size: 15px; line-height: 1.7; padding: 1rem 0;">
Airline and credit card loyalty programs make it hard to know what your points are actually worth.
A flight that costs 50,000 miles might be a great deal — or a terrible one — depending on the program
and how you redeem. This tool cuts through the confusion by converting every option into a single
comparable number: <strong>cents per point (CPP)</strong>. Pick your program, enter your balance,
and instantly see which redemption gives you the most value.
</div>
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

<p>Some programs show a range (e.g. "1.25 – 1.50 CPP") for portal bookings. This reflects different card tiers — for example, Chase Sapphire Preferred earns 1.25 CPP on the Chase Travel portal while Chase Sapphire Reserve earns 1.50 CPP. The range shows what's possible depending on which card you hold.</p>

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

# Group selector then program selector
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
            # Range value — use the midpoint for sorting/calculations, display as range
            low, high = [float(x.strip()) for x in cpp.split("–")]
            cpp_mid = (low + high) / 2
            dollar_low = round(points * low / 100, 2)
            dollar_high = round(points * high / 100, 2)
            dollar_display = f"${dollar_low:,.0f} – ${dollar_high:,.0f}"
            range_notes.append(redemption_type)
            rows.append({
                "Redemption Type": redemption_type,
                "CPP": cpp + "¢ *",
                "Estimated Value ($)": dollar_display + " *",
                "_sort": cpp_mid,
            })
        else:
            dollar_value = round(points * cpp / 100, 2)
            rows.append({
                "Redemption Type": redemption_type,
                "CPP": f"{cpp:.2f}¢",
                "Estimated Value ($)": f"${dollar_value:,.2f}",
                "_sort": cpp,
            })

    df = pd.DataFrame(rows).sort_values("_sort", ascending=False).drop(columns="_sort")

    # Best and worst (numeric only for metrics)
    numeric_rows = [r for r in rows if "–" not in str(r["Estimated Value ($)"])]
    numeric_df = pd.DataFrame(numeric_rows).sort_values("_sort", ascending=False).drop(columns="_sort") if numeric_rows else None

    best_label = df.iloc[0]["Redemption Type"]
    worst_label = df.iloc[-1]["Redemption Type"]

    st.success(f"💡 Best redemption: **{best_label}** — {df.iloc[0]['Estimated Value ($)']} at {df.iloc[0]['CPP']} per point")

    if numeric_df is not None and len(numeric_df) >= 2:
        best_n = numeric_df.iloc[0]
        worst_n = numeric_df.iloc[-1]
        best_val = float(best_n["Estimated Value ($)"].replace("$", "").replace(",", ""))
        worst_val = float(worst_n["Estimated Value ($)"].replace("$", "").replace(",", ""))
        m1, m2, m3 = st.columns(3)
        m1.metric(f"Best: {best_n['Redemption Type']}", f"${best_val:,.0f}", best_n["CPP"] + " per point")
        m2.metric(f"Worst: {worst_n['Redemption Type']}", f"${worst_val:,.0f}", worst_n["CPP"] + " per point")
        m3.metric("Difference", f"${best_val - worst_val:,.0f}", "best vs worst")

    st.markdown("####")

    # Bar chart — only numeric rows
    chart_rows = []
    for r in rows:
        val = r["Estimated Value ($)"].replace(" *", "")
        if "–" in str(val):
            low, high = [float(x.replace("$", "").replace(",", "").strip()) for x in val.split("–")]
            chart_rows.append({"Redemption Type": r["Redemption Type"], "Value": (low + high) / 2, "Label": val})
        else:
            v = float(val.replace("$", "").replace(",", ""))
            chart_rows.append({"Redemption Type": r["Redemption Type"], "Value": v, "Label": val})

    chart_df = pd.DataFrame(chart_rows).sort_values("Value", ascending=False)

    fig = px.bar(
        chart_df,
        x="Redemption Type",
        y="Value",
        color="Value",
        color_continuous_scale="Blues",
        text="Label",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Estimated Value (USD)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", size=13),
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Full breakdown**")
    st.dataframe(df[["Redemption Type", "CPP", "Estimated Value ($)"]], use_container_width=True, hide_index=True)

    if range_notes:
        st.caption(f"* Range shown for {', '.join(range_notes)} reflects different card tiers — value depends on which card you hold.")

else:
    st.info("Enter your point balance above to see redemption values.")
