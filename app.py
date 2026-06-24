import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analytics import AdvancedTournamentEngine

# Enforce system configurations and full-width rendering layout
st.set_page_config(page_title="FIFA 2026 Core Analytics", page_icon="📈", layout="wide")

# Custom UI Skinning injection
st.markdown("""
    <style>
        .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        h1, h2, h3 {font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 700;}
        .metric-card-container {
            background-color: #171E31; border: 1px solid #30363D; padding: 20px; border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Data engine initializing
@st.cache_data
def initialize_engine():
    return AdvancedTournamentEngine("fifa_world_cup_2026_player_performance.csv")

try:
    engine = initialize_engine()
except Exception as e:
    st.error(f"Failed infrastructure binding. Ensure CSV dataset file is present. Technical Stacktrace: {e}")
    st.stop()

# Matplotlib/Seaborn design formatting properties
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#171E31', 'axes.facecolor': '#171E31',
    'grid.color': '#262F4D', 'text.color': '#FFFFFF',
    'axes.edgecolor': '#262F4D', 'xtick.color': '#A3B3D2', 'ytick.color': '#A3B3D2'
})

# Header App Workspace Banner
st.markdown("<h1 style='text-align: left; color: #00FF66; margin-bottom:0px;'>⚽ FIFA World Cup 2026 Analytics Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: #8B949E; font-size:16px; margin-top:5px;'>Advanced Multi-Dimensional Player Performance & Tactical Engine Architecture</p>", unsafe_allow_html=True)
st.markdown("---")

# Main Filters Panel Container
with st.sidebar:
    st.image("https://img.icons8.com/neon/96/football-ball.png", width=80)
    st.markdown("### Control Matrix Engine")
    min_mins = st.slider("Minimum Tournament Minutes Tracked", int(engine.df['total_minutes_tournament'].min()), int(engine.df['total_minutes_tournament'].max()), 90)
    cohort_limit = st.slider("Leaderboard Cohort Sample Depth", 5, 50, 15)
    
    st.markdown("---")
    st.markdown("### Tactical Deep Dive Scope")
    target_pos = st.selectbox("Position Scope Isolator", engine.df['position'].unique())

# Core Performance KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Total Database Records", value=len(engine.df), delta="Vector Validated")
with kpi2:
    st.metric(label="Mean Tactical Competency", value=f"{engine.df['tournament_rating'].mean():.2f} / 10")
with kpi3:
    st.metric(label="Max Intensity Speed", value=f"{engine.df['top_speed_kmh'].max()} km/h")
with kpi4:
    st.metric(label="Average xG Production Rate", value=f"{engine.df['expected_goals_xg'].mean():.3f} per match")

st.markdown("---")

# Master Row Layout Workspace 
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.markdown(f"### 🏆 Elite Performance Cohort Matrix (Top {cohort_limit})")
    mvp_data = engine.compute_mvp_cohort(min_minutes=min_mins, top_n=cohort_limit)
    
    # Render interactive clean structural table layout view
    st.dataframe(
        mvp_data[['player_name', 'team', 'position', 'avg_rating', 'peak_z_score', 'goals', 'market_value']],
        column_config={
            "player_name": "Player", "team": "Nation", "position": "Tactical Field Position",
            "avg_rating": st.column_config.NumberColumn("Avg Rating ⭐", format="%.2f"),
            "peak_z_score": st.column_config.NumberColumn("Positional Z-Score", format="%.2f"),
            "market_value": st.column_config.NumberColumn("Market Value (€)", format="€%d")
        },
        use_container_width=True, hide_index=True
    )

with col_right:
    st.markdown("### 🧬 Positional Trait & Fingerprint Variance Maps")
    traits = engine.segment_tactical_archetypes()
    
    fig, ax = plt.subplots(figsize=(7, 4.8))
    sns.heatmap(
        traits.set_index('position')[['stamina', 'creativity', 'consistency', 'pressure_resistance']],
        annot=True, fmt=".2f", cmap="YlGnBu", cbar=False, linewidths=.5, ax=ax
    )
    plt.title("Biometric & Mental Performance Densities by Tactical Alignment", fontsize=12, color='#00FF66', pad=15)
    plt.ylabel("")
    st.pyplot(fig)

st.markdown("---")

# Deep Analytical Outlier Section
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown("### 📊 Performance Efficiency Matrix (xG vs Actual Outputs)")
    efficiency_df = engine.get_efficiency_outliers().head(25)
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=efficiency_df, x="expected_goals", y="actual_goals",
        hue="xg_delta", palette="Spectral", size="minutes", sizes=(40, 400), ax=ax2
    )
    # Line representing perfectly neutral statistical expectations alignment
    lims = [0, max(efficiency_df['actual_goals'].max(), efficiency_df['expected_goals'].max()) + 1]
    ax2.plot(lims, lims, 'w--', alpha=0.5, zorder=1, label="Base Expectations Benchmark")
    
    ax2.set_title("Clinical Finishing Multipliers vs. Stochastic Modeling Profiles", color="#00FF66", pad=12)
    ax2.set_xlabel("Expected Scoring Profile Model (xG Evaluated)")
    ax2.set_ylabel("Actual Field Finishes Visualized")
    st.pyplot(fig2)

with col_b2:
    st.markdown("### 🏃 Physical Output Profiles (Top Speed vs Total Workload)")
    pos_filtered_df = engine.df[engine.df['position'] == target_pos]
    
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.kdeplot(
        data=pos_filtered_df, x="distance_covered_km", y="top_speed_kmh",
        cmap="mako", fill=True, thresh=0.05, ax=ax3
    )
    sns.scatterplot(
        data=pos_filtered_df, x="distance_covered_km", y="top_speed_kmh",
        color="#00FF66", alpha=0.3, s=15, ax=ax3
    )
    ax3.set_title(f"Density Clusters for '{target_pos}' Physical Profiles", color="#FFFFFF")
    ax3.set_xlabel("Gross Operational Field Output (KM Covered)")
    ax3.set_ylabel("Peak Intermittent Vector Velocity (KM/H Recorded)")
    st.pyplot(fig3)