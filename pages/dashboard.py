"""
Dashboard stránka – přehled metrik a top fanoušků s grafy.
"""

import streamlit as st

from config import TIER_EMOJI, TIERS
from database import get_df


def page_dashboard():
    """Hlavní dashboard s přehledem metrik a grafy."""
    st.title("📊 Dashboard")
    st.markdown("Přehled tvé fanouškovské základny")

    df = get_df()

    # Metriky
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_fans = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Celkem fanoušků</h3>
            <h1>{total_fans}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        vip_count = len(df[df["tier"] == "VIP"]) if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>👑 VIP</h3>
            <h1>{vip_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        supporter_count = len(df[df["tier"] == "Supporter"]) if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ Supporters</h3>
            <h1>{supporter_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        total_support = df["total_support"].sum() if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Celková podpora</h3>
            <h1>{int(total_support)} Kč</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Analytika – grafy
    if not df.empty:
        st.subheader("📈 Analytika")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Rozložení fanoušků podle tier**")
            tier_counts = df["tier"].value_counts()
            # Ensure all tiers are present
            for tier in TIERS:
                if tier not in tier_counts.index:
                    tier_counts[tier] = 0
            st.bar_chart(tier_counts)

        with chart_col2:
            st.markdown("**Podpora podle tier (Kč)**")
            support_by_tier = df.groupby("tier")["total_support"].sum()
            for tier in TIERS:
                if tier not in support_by_tier.index:
                    support_by_tier[tier] = 0
            st.bar_chart(support_by_tier)

        st.markdown("---")

    # Top 5 fanoušků
    st.subheader("🏆 Top 5 Fanoušků")
    if not df.empty:
        top5 = df.nlargest(5, "total_support")[["nickname", "tier", "total_support"]]
        for idx, row in top5.iterrows():
            emoji = TIER_EMOJI[row["tier"]]
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"{emoji} **{row['nickname']}**")
            with col2:
                st.markdown(f"*{row['tier']}*")
            with col3:
                st.markdown(f"**{int(row['total_support'])} Kč**")
    else:
        st.info("Zatím žádní fanoušci v databázi.")
