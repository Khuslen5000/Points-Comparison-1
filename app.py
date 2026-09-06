import streamlit as st
import pandas as pd
import plotly.express as px

CPP_DATA = {
    "Chase Ultimate Rewards": {
        "Flights (transfer partners)": 2.0,
        "Hotels (transfer partners)": 1.5,
        "Chase Travel portal": 1.25,
        "Cash back": 1.0,
    },
    "Amex Membership Rewards": {
        "Flights (transfer partners)": 2.0,
        "Hotels (transfer partners)": 1.4,
        "Amex Travel portal": 1.0,
        "Cash back": 0.6,
    },
    "Delta SkyMiles": {
        "Delta flights": 1.2,
        "Partner flights": 1.0,
        "Upgrades": 1.5,
        "Cash back": 0.5,
    },
    "United MileagePlus": {
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
}

st.set_page_config(page_title="Points & Miles Comparator", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #f8f9fb; }
        h1 { color: #1a1a2e; }
        h2, h3 { color: #16213e; }
        .explainer-box {
            background-color: #eef2ff;
            border-left: 4px solid #4f6ef7;
            padding: 1rem 1.25rem;
            border-radius: 6px;
            margin-bottom: 1.5rem;
            font-size: 0.92rem;
            color: #333;
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("✈️ Points & Miles Comparator")
st.markdown("Find out how much your loyalty points are actually worth — and where you'll get the most value.")

st.divider()

# Explainer box
with st.expander("📖 How does this work?"):
    st.markdown("""
<div style="font-family: sans-serif; font-size: 15px; line-height: 1.7;">

<p><strong>What is CPP (cents per point)?</strong></p>

<p>Loyalty programs all use different point currencies, so 50,000 Delta miles and 50,000 Chase points aren't worth the same — even though they're the same number. CPP converts everything into a common unit: cents per point.</p>

<p>The formula is simple: <strong>(dollar value of what you're getting ÷ points used) × 100 = CPP</strong></p>

<p>For example: if 50,000 points gets you a flight worth $750, that's <strong>1.5 CPP</strong>. If those same points gets you $500 cash back, that's only <strong>1.0 CPP</strong>. Higher CPP = more value per point.</p>

<p><strong>Where do the estimates come from?</strong></p>

<p>The CPP values used here are widely published estimates based on typical redemption rates across the travel community. They reflect realistic (not best-case) redemption scenarios. Your actual value may be higher or lower depending on the specific redemption you find.</p>

</div>
""", unsafe_allow_html=True)

st.subheader("Select your program")

col1, col2 = st.columns(2)
with col1:
    program = st.selectbox("Loyalty program", list(CPP_DATA.keys()), label_visibility="collapsed")
with col2:
    points = st.number_input("Number of points", min_value=0, step=1000, value=50000, label_visibility="collapsed")

st.caption(f"Program: **{program}** · Points: **{points:,}**")

st.divider()

if points > 0:
    redemptions = CPP_DATA[program]

    rows = []
    for category, cpp in redemptions.items():
        dollar_value = round(points * cpp / 100, 2)
        rows.append({"Redemption Type": category, "CPP": cpp, "Estimated Value ($)": dollar_value})

    df = pd.DataFrame(rows).sort_values("Estimated Value ($)", ascending=False)
    best = df.iloc[0]

    # Highlight best redemption
    st.success(f"💡 Best redemption: **{best['Redemption Type']}** — worth **${best['Estimated Value ($)']:,.0f}** at {best['CPP']}¢ per point")

    # Summary metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Best Value", f"${best['Estimated Value ($)']:,.0f}", f"{best['CPP']}¢ per point")
    m2.metric("Worst Value", f"${df.iloc[-1]['Estimated Value ($)']:,.0f}", f"{df.iloc[-1]['CPP']}¢ per point")
    m3.metric("Difference", f"${best['Estimated Value ($)'] - df.iloc[-1]['Estimated Value ($)']:,.0f}", "best vs worst")

    st.markdown("####")

    # Bar chart
    fig = px.bar(
        df,
        x="Redemption Type",
        y="Estimated Value ($)",
        color="Estimated Value ($)",
        color_continuous_scale="Blues",
        text=df["Estimated Value ($)"].apply(lambda x: f"${x:,.0f}"),
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

    # Table
    st.markdown("**Full breakdown**")
    st.dataframe(
        df.style.format({"CPP": "{:.2f}¢", "Estimated Value ($)": "${:,.2f}"}),
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("Enter your point balance above to see redemption values.")
