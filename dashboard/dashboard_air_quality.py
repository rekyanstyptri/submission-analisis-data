
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch


# -----------------------------------------------------------------------------
# 1. PENGATURAN HALAMAN & PALET WARNA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Beijing Air Quality | Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#18385A"
BLUE = "#427DE5"
CYAN = "#20BBD0"
TURQUOISE = "#7DDCE2"
SKY = "#ABD7FF"
PALE = "#EFF6FF"
WHITE = "#FFFFFF"
SLATE = "#52677E"
GRID = "#E5ECF5"

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelcolor": SLATE,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "grid.color": GRID,
    "grid.alpha": 0.8,
    "figure.facecolor": WHITE,
    "axes.facecolor": WHITE,
})

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #F5F9FF 0%, #F9FCFF 54%, #F0F7FF 100%);
        color: #18385A;
    }
    .block-container { max-width: 1400px; padding-top: 1.7rem; padding-bottom: 2.5rem; }
    section[data-testid="stSidebar"] { background: #EAF3FF; border-right: 1px solid #DCE8F8; }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }
    .hero {
        background: linear-gradient(110deg, #18385A 0%, #245A91 55%, #39B9D1 100%);
        border-radius: 24px;
        padding: 31px 36px;
        box-shadow: 0 12px 30px rgba(28, 74, 122, .16);
        margin-bottom: 22px;
    }
    .hero .eyebrow { color: #BFEFF8; font-size: 12px; font-weight: 750; letter-spacing: 2px; }
    .hero h1 { color: white !important; font-size: clamp(25px, 3vw, 37px); margin: 9px 0; }
    .hero p { color: #E3F5FC; font-size: 15px; margin: 0; max-width: 790px; }
    .sidebar-brand {
        background: linear-gradient(130deg, #18385A, #3674B1);
        color: white;
        padding: 23px 20px;
        border-radius: 18px;
        margin-bottom: 20px;
    }
    .sidebar-brand h2 { color: white !important; font-size: 22px; margin: 0 0 6px; }
    .sidebar-brand p { color: #E0F0FF; font-size: 12px; margin: 0; }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #DFEAF7;
        border-radius: 19px;
        padding: 18px 19px;
        box-shadow: 0 5px 16px rgba(33, 73, 116, .075);
        min-height: 114px;
    }
    [data-testid="stMetricLabel"] { color: #52677E; font-weight: 650; }
    [data-testid="stMetricValue"] { color: #18385A; font-weight: 800; }
    [data-testid="stTabs"] button[data-baseweb="tab"] {
        color: #52677E;
        font-size: 14px;
        font-weight: 700;
        padding-left: 20px;
        padding-right: 20px;
    }
    [data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        color: #2976C9;
    }
    [data-baseweb="tag"] { background: #D6E9FF !important; color: #173D68 !important; }
    [data-baseweb="tag"] span { color: #173D68 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        border-color: #E1EBF7 !important;
        border-radius: 20px !important;
    }
    div[data-testid="stAlert"] { border-radius: 15px; }
    .section-eyebrow { color: #3C9FB6; font-size: 12px; font-weight: 800; letter-spacing: 1.4px; }
    .muted-note { color: #71859A; font-size: 12px; }
    .mini-footer { color: #71859A; text-align: center; font-size: 12px; padding: 20px 0 4px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def make_axes(figsize=(10, 4.6)):
    """Menjaga semua grafik memiliki gaya visual yang konsisten."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.9)
    ax.grid(axis="x", visible=False)
    ax.set_axisbelow(True)
    return fig, ax


def show_chart(fig):
    fig.tight_layout(pad=1.7)
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)


def section_title(label, title):
    st.markdown(f'<div class="section-eyebrow">{label}</div>', unsafe_allow_html=True)
    st.subheader(title)


# -----------------------------------------------------------------------------
# 2. BACA DATA
# -----------------------------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv.gz')
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR & FILTER
# -----------------------------------------------------------------------------
year_options = sorted(df["year"].dropna().unique().tolist())
station_options = sorted(df["station"].dropna().astype(str).unique().tolist())

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <h2>Air Quality</h2>
            <p>BEIJING / INTERACTIVE DASHBOARD</p>
            <p style="margin-top:12px;">Rekyan Setyoputri Prameswari</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### ⚙️ Filter Analisis")
    selected_years = st.multiselect(
        "📅 Pilih Tahun", options=year_options, default=year_options
    )
    selected_stations = st.multiselect(
        "📍 Pilih Stasiun", options=station_options, default=station_options
    )
    st.caption("Semua grafik dan ringkasan mengikuti pilihan filter ini.")
    st.divider()
    st.markdown("**Tentang dashboard**")
    st.caption("Analisis deskriptif kualitas udara Beijing berdasarkan pengamatan stasiun dan meteorologi.")

filtered_df = df.loc[
    df["year"].isin(selected_years) & df["station"].isin(selected_stations)
].copy()

# Untuk grafik konsentrasi, gunakan hanya observasi PM2.5 yang tidak kosong.
valid_df = filtered_df.dropna(subset=["PM2.5"]).copy()


# -----------------------------------------------------------------------------
# 4. HEADER & KARTU KPI
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <span class="eyebrow">ENVIRONMENTAL INTELLIGENCE • BEIJING</span>
        <h1>Dashboard Air Quality Beijing</h1>
        <p>Jelajahi tren PM2.5, hubungan dengan kondisi cuaca, dan perbedaan
        kualitas udara antarstasiun melalui visualisasi yang interaktif.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if filtered_df.empty or valid_df.empty:
    st.warning("Belum ada pengamatan PM2.5 untuk filter tersebut. Pilih tahun atau stasiun lain.")
    st.stop()

k1, k2, k3, k4 = st.columns(4, gap="medium")
with k1:
    st.metric("🌫️ Rata-rata PM2.5", f"{valid_df['PM2.5'].mean():,.1f} µg/m³")
with k2:
    st.metric("💨 Kecepatan angin", f"{filtered_df['WSPM'].mean():,.1f} m/s")
with k3:
    st.metric("🌡️ Suhu rata-rata", f"{filtered_df['TEMP'].mean():,.1f} °C")
with k4:
    st.metric("📍 Stasiun terpilih", f"{filtered_df['station'].nunique()} stasiun")

st.caption(
    f"Cakupan filter: {len(filtered_df):,} pengamatan • "
    f"{len(selected_years)} tahun terpilih • {len(selected_stations)} stasiun terpilih"
)
st.write("")

# -----------------------------------------------------------------------------
# 5. TIGA TAB ANALISIS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Tren PM2.5",
    "🌤️ Pengaruh Cuaca",
    "📍 Profil Stasiun",
])

MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

with tab1:
    section_title("01 / TEMPORAL ANALYSIS", "Perubahan konsentrasi PM2.5 dari waktu ke waktu")

    with st.container(border=True):
        st.markdown("#### Tren rata-rata tahunan")
        yearly = valid_df.groupby("year")["PM2.5"].mean().sort_index()
        fig, ax = make_axes()
        ax.plot(
            yearly.index, yearly.values, color=BLUE, linewidth=3,
            marker="o", markersize=9, markerfacecolor=WHITE,
            markeredgecolor=CYAN, markeredgewidth=2.5,
        )
        ax.fill_between(yearly.index, yearly.values, yearly.min() * 0.92,
                        color=SKY, alpha=0.20)
        for year, value in yearly.items():
            ax.annotate(f"{value:.1f}", (year, value), xytext=(0, 10),
                        textcoords="offset points", ha="center",
                        color=NAVY, fontweight="bold")
        ax.set_xticks(yearly.index)
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
        ax.margins(y=0.19)
        show_chart(fig)
        st.caption(
            "Panduan WHO 2021 untuk rata-rata PM2.5 tahunan adalah 5 µg/m³; "
            "angka 15 µg/m³ merupakan panduan untuk periode 24 jam. "
            "Angka pada grafik adalah rata-rata data dalam filter, bukan otomatis nilai tahunan lengkap per stasiun."
        )

    with st.container(border=True):
        st.markdown("#### Pola bulanan")
        monthly = valid_df.groupby("month")["PM2.5"].mean().sort_index()
        monthly = monthly[monthly.index.isin(range(1, 13))]
        if not monthly.empty:
            colors = [SKY] * len(monthly)
            colors[int(np.argmax(monthly.values))] = BLUE
            colors[int(np.argmin(monthly.values))] = CYAN
            fig, ax = make_axes()
            ax.bar(monthly.index.astype(int), monthly.values,
                   color=colors, width=0.68, edgecolor=WHITE, linewidth=1.5)
            ax.set_xticks(monthly.index, [MONTH_LABELS[int(m) - 1] for m in monthly.index])
            ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
            ax.legend(handles=[Patch(color=BLUE, label="Rata-rata tertinggi"),
                               Patch(color=CYAN, label="Rata-rata terendah")],
                      frameon=False, loc="upper right")
            show_chart(fig)
        else:
            st.info("Data bulan tidak tersedia pada filter ini.")

    with st.container(border=True):
        st.markdown("#### Pola rata-rata per jam")
        hourly = valid_df.groupby("hour")["PM2.5"].mean().sort_index()
        hourly = hourly[hourly.index.isin(range(24))]
        if not hourly.empty:
            fig, ax = make_axes()
            ax.fill_between(hourly.index, hourly.values, color=TURQUOISE, alpha=0.28)
            ax.plot(hourly.index, hourly.values, color=BLUE, linewidth=2.7,
                    marker="o", markersize=5, markerfacecolor=WHITE,
                    markeredgecolor=BLUE)
            ax.scatter([hourly.idxmax()], [hourly.max()], color=BLUE, s=105, zorder=5,
                       label=f"Tertinggi: {int(hourly.idxmax()):02d}:00")
            ax.scatter([hourly.idxmin()], [hourly.min()], color=CYAN, s=105, zorder=5,
                       label=f"Terendah: {int(hourly.idxmin()):02d}:00")
            ax.set_xticks(range(0, 24, 2))
            ax.set_xlabel("Jam")
            ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
            ax.legend(frameon=False)
            show_chart(fig)
        else:
            st.info("Data jam tidak tersedia pada filter ini.")

    if not yearly.empty:
        st.info(
            f"**Ringkasan berdasarkan filter:** rata-rata tahunan tertinggi tercatat "
            f"pada **{int(yearly.idxmax())}** ({yearly.max():.1f} µg/m³) dan terendah "
            f"pada **{int(yearly.idxmin())}** ({yearly.min():.1f} µg/m³). "
            "Ini temuan deskriptif dan tidak dengan sendirinya menjelaskan penyebab perubahan."
        )
    with st.expander("Lihat tabel rata-rata tahunan"):
        st.dataframe(yearly.rename("Rata-rata PM2.5").reset_index(),
                     use_container_width=True, hide_index=True)

with tab2:
    section_title("02 / WEATHER RELATIONSHIP", "Konsentrasi PM2.5 dan kondisi meteorologis")

    with st.container(border=True):
        st.markdown("#### Korelasi antarvariabel")
        corr_cols = ["PM2.5", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
        corr = filtered_df[corr_cols].corr(numeric_only=True)
        labels = ["PM2.5", "Suhu", "Tekanan", "Titik embun", "Hujan", "Kec. angin"]
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        cmap = LinearSegmentedColormap.from_list(
            "blue_cyan_diverging", ["#3F71C4", "#F7FBFF", "#20BBD0"]
        )
        fig, ax = make_axes((9, 5.2))
        sns.heatmap(
            corr, annot=True, fmt=".2f", vmin=-1, vmax=1, center=0,
            cmap=cmap, mask=mask, square=False,
            xticklabels=labels, yticklabels=labels,
            linewidths=2, linecolor=WHITE, ax=ax,
            annot_kws={"size": 10, "weight": "bold"},
            cbar_kws={"label": "Korelasi Pearson", "shrink": .8},
        )
        ax.tick_params(axis="x", rotation=0)
        ax.tick_params(axis="y", rotation=0)
        show_chart(fig)
        st.caption("Korelasi Pearson menggambarkan hubungan linear, bukan bukti sebab-akibat.")

    with st.container(border=True):
        st.markdown("#### Rata-rata PM2.5 menurut kecepatan angin")
        wind_labels = ["Tenang\n≤1 m/s", "Lemah\n1–2 m/s", "Sedang\n2–4 m/s", "Kuat\n>4 m/s"]
        wind_df = valid_df.dropna(subset=["WSPM"]).copy()
        wind_df["Kategori"] = pd.cut(
            wind_df["WSPM"], bins=[-np.inf, 1, 2, 4, np.inf],
            labels=wind_labels, include_lowest=True,
        )
        wind_mean = wind_df.groupby("Kategori", observed=False)["PM2.5"].mean()
        available = wind_mean.dropna()
        if not available.empty:
            fig, ax = make_axes()
            bar_colors = [BLUE, "#6A9AEF", "#6FC9E6", CYAN]
            palette = {label: color for label, color in zip(wind_labels, bar_colors)}
            bars = ax.bar(available.index.astype(str), available.values,
                          color=[palette[x] for x in available.index.astype(str)], width=0.58)
            for bar, value in zip(bars, available.values):
                ax.text(bar.get_x() + bar.get_width() / 2, value + max(available.max()*.015, .5),
                        f"{value:.1f}", ha="center", fontsize=10,
                        fontweight="bold", color=NAVY)
            ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
            ax.margins(y=.18)
            show_chart(fig)
        else:
            st.info("Tidak ada kecepatan angin valid untuk filter ini.")

    with st.container(border=True):
        st.markdown("#### Rata-rata PM2.5 menurut arah angin")
        wd = (valid_df.dropna(subset=["wd"])
              .groupby("wd")["PM2.5"].mean().sort_values())
        if not wd.empty:
            fig, ax = make_axes((10, 5.1))
            color_seq = [SKY if v < wd.median() else BLUE for v in wd.values]
            ax.barh(wd.index.astype(str), wd.values, color=color_seq, height=.69)
            ax.axvline(valid_df["PM2.5"].mean(), color=CYAN,
                       linestyle="--", linewidth=2, label="Rata-rata keseluruhan")
            ax.set_xlabel("Rata-rata PM2.5 (µg/m³)")
            ax.grid(axis="x", color=GRID)
            ax.grid(axis="y", visible=False)
            ax.legend(frameon=False, loc="lower right")
            show_chart(fig)
        else:
            st.info("Data arah angin tidak tersedia pada filter ini.")

    correlation = filtered_df[["PM2.5", "WSPM"]].corr().loc["PM2.5", "WSPM"]
    corr_text = f"{correlation:+.2f}" if pd.notna(correlation) else "tidak tersedia"
    st.info(
        f"**Ringkasan berdasarkan filter:** korelasi Pearson PM2.5 dengan kecepatan "
        f"angin adalah **{corr_text}**. Arah dan besar korelasi menggambarkan asosiasi "
        "dalam data yang dipilih; belum cukup untuk menyimpulkan hubungan kausal."
    )
    with st.expander("Lihat tabel arah angin"):
        st.dataframe(wd.rename("Rata-rata PM2.5").reset_index(),
                     use_container_width=True, hide_index=True)

with tab3:
    section_title("03 / STATION PROFILE", "Perbandingan konsentrasi polutan antarstasiun")

    station_profile = valid_df.groupby("station").agg(
        PM2_5=("PM2.5", "mean"),
        PM10=("PM10", "mean"),
        NO2=("NO2", "mean"),
        CO=("CO", "mean"),
        WSPM=("WSPM", "mean"),
    ).round(2).reset_index()

    # Kategori DESKRIPTIF berdasarkan batas manual, bukan algoritma clustering.
    levels = ["Polusi Rendah", "Polusi Sedang", "Polusi Tinggi"]
    level_colors = {
        "Polusi Rendah": CYAN,
        "Polusi Sedang": "#7BA5EF",
        "Polusi Tinggi": NAVY,
    }
    station_profile["Kelompok"] = pd.cut(
        station_profile["PM2_5"], bins=[-np.inf, 75, 82, np.inf],
        labels=levels, include_lowest=True,
    )

    st.caption(
        "Kategori ilustratif dengan ambang rata-rata PM2.5: rendah ≤75, "
        "sedang >75–82, tinggi >82 µg/m³. Ini kategorisasi manual, bukan "
        "hasil algoritma clustering ataupun klasifikasi resmi kualitas udara."
    )

    m1, m2, m3 = st.columns(3)
    for col, name in zip([m1, m2, m3], levels):
        group = station_profile.loc[station_profile["Kelompok"] == name]
        with col:
            st.metric(name, f"{len(group)} stasiun")

    with st.container(border=True):
        st.markdown("#### Rata-rata PM2.5 per stasiun")
        station_sorted = station_profile.sort_values("PM2_5", ascending=True)
        palette = [level_colors[str(x)] for x in station_sorted["Kelompok"]]
        fig, ax = make_axes((10, max(4.6, .47 * len(station_sorted) + 1.1)))
        bars = ax.barh(station_sorted["station"], station_sorted["PM2_5"],
                       color=palette, height=.7)
        for bar, val in zip(bars, station_sorted["PM2_5"]):
            ax.text(val + max(station_sorted["PM2_5"].max()*.007, .2),
                    bar.get_y() + bar.get_height()/2, f"{val:.1f}",
                    va="center", color=NAVY, fontsize=9)
        ax.set_xlim(0, station_sorted["PM2_5"].max() * 1.15)
        ax.grid(axis="x", color=GRID)
        ax.grid(axis="y", visible=False)
        ax.set_xlabel("Rata-rata PM2.5 (µg/m³)")
        ax.legend(handles=[Patch(facecolor=color, label=name)
                           for name, color in level_colors.items()],
                  frameon=False, loc="lower right")
        show_chart(fig)

    with st.container(border=True):
        st.markdown("#### Profil PM2.5, NO2, dan CO menurut kelompok")
        st.caption(
            "Setiap polutan memakai grafik dan skala sendiri agar perbedaan "
            "besaran maupun satuan tidak menyesatkan."
        )
        grouped = station_profile.groupby("Kelompok", observed=True)[["PM2_5", "NO2", "CO"]].mean()
        c1, c2, c3 = st.columns(3)
        for col, feature, label in zip(
            [c1, c2, c3], ["PM2_5", "NO2", "CO"], ["PM2.5", "NO₂", "CO"]
        ):
            with col:
                st.markdown(f"**{label}**")
                vals = grouped[feature].dropna()
                if not vals.empty:
                    fig, ax = make_axes((4.2, 3.5))
                    ax.bar(range(len(vals)), vals.values,
                           color=[level_colors[str(k)] for k in vals.index], width=.64)
                    ax.set_xticks(range(len(vals)),
                                  [str(k).replace("Polusi ", "") for k in vals.index])
                    ax.set_ylabel("Rata-rata (satuan dataset)")
                    show_chart(fig)
                else:
                    st.caption("Data tidak tersedia")

    with st.expander("Lihat data profil stasiun"):
        st.dataframe(
            station_profile.sort_values("PM2_5", ascending=False),
            use_container_width=True, hide_index=True,
        )

    top_station = station_profile.loc[station_profile["PM2_5"].idxmax()]
    st.info(
        f"**Ringkasan berdasarkan filter:** rata-rata PM2.5 tertinggi terdapat "
        f"pada stasiun **{top_station['station']}** "
        f"({top_station['PM2_5']:.1f} µg/m³). "
        "Perbandingan ini bersifat deskriptif untuk periode dan stasiun terpilih."
    )

st.markdown(
    "<div class='mini-footer'>2026 • Rekyan Setyoputri Prameswari • "
    "Proyek Akhir Analisis Data Dicoding</div>",
    unsafe_allow_html=True,
)
