import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import sidetable as stb
import numpy as np
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Dashboard Olist",
    page_icon="📦",
    layout="wide"
)
st.markdown("""
<style>
/* Fondo general */
.stApp {
    background-color: #07111f;
    color: white;
}

/* Contenido principal */
[data-testid="stAppViewContainer"] {
    background-color: #07111f;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #07111f;
}

/* Texto de la sidebar */
[data-testid="stSidebar"] * {
    color: white;
}

/* Opcional: métricas y títulos algo más visibles */
h1, h2, h3, h4, h5, h6, p, label, div {
    color: white;
}
</style>
""", unsafe_allow_html=True)
# -----------------------------
# CARGA DE DATOS
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed" / "olist_final_dataset.csv"

@st.cache_data
def load_data():
    df_olist = pd.read_csv(
        DATA_PATH,
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "shipping_limit_date",
            "review_creation_date",
            "review_answer_timestamp"
        ]
    )

    df_olist["year_month"] = df_olist["order_purchase_timestamp"].dt.to_period("M").astype(str)
    df_olist["purchase_year"] = df_olist["order_purchase_timestamp"].dt.year
    df_olist["delay_flag"] = np.where(
        df_olist["delivery_delay"] > 0,
        "Con retraso",
        "En plazo o antes"
    )

    return df_olist


df_olist = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Filtros")

years = sorted(df_olist["purchase_year"].dropna().unique())
states = sorted(df_olist["state"].dropna().unique())

selected_years = st.sidebar.multiselect("Año", years, default=years)
selected_states = st.sidebar.multiselect("Estado", states, default=states)

page = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Ventas", "Logística", "Clientes", "Satisfacción"]
)

# -----------------------------
# FILTROS
# -----------------------------
df_filtered = df_olist[
    (df_olist["purchase_year"].isin(selected_years)) &
    (df_olist["state"].isin(selected_states))
].copy()

df_orders = df_filtered.drop_duplicates(subset="order_id").copy()

# -----------------------------
# KPIs
# -----------------------------
total_revenue = df_orders["payment_value"].sum()
total_orders = df_orders["order_id"].nunique()
avg_order_value = df_orders.groupby("order_id")["payment_value"].sum().mean()
avg_review = df_orders["review_score"].mean()
avg_delivery = df_orders["delivery_time_days"].mean()
pct_delayed = (df_orders["delivery_delay"] > 0).mean() * 100
total_customers = df_orders["customer_id"].nunique()

def euro(x):
    return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
 
# =========================
# PREPARACIÓN DE COLUMNAS
# =========================
if "order_purchase_timestamp" in df_olist.columns:
    df_olist["year_month"] = df_olist["order_purchase_timestamp"].dt.to_period("M").astype(str)

if "delivery_delay" in df_olist.columns:
    df_olist["delay_flag"] = df_olist["delivery_delay"].apply(lambda x: 1 if x > 0 else 0)
# -----------------------------
# INICIO
# -----------------------------
if page == "Inicio":
    st.title("Dashboard Olist")
    st.markdown("Análisis de ventas, logística, clientes y satisfacción del e-commerce Olist.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ingresos totales", euro(total_revenue))
    col2.metric("Pedidos", total_orders)
    col3.metric("Ticket medio", euro(avg_order_value))
    col4.metric("Clientes únicos", total_customers)

    col5, col6, col7 = st.columns(3)
    col5.metric("Review media", round(avg_review, 2))
    col6.metric("Tiempo medio entrega", f"{avg_delivery:.2f} días")
    col7.metric("% pedidos retrasados", f"{pct_delayed:.2f}%")

    ventas_mes = (
        df_orders.groupby("year_month", as_index=False)
        .agg(payment_value=("payment_value", "sum"))
        .sort_values("year_month")
    )

    fig = px.line(
        ventas_mes,
        x="year_month",
        y="payment_value",
        markers=True,
        title="Evolución de ventas mensuales"
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# VENTAS
# -----------------------------
elif page == "Ventas":
    st.title("Ventas")

    # KPIs
    total_revenue = df_olist["payment_value"].sum()
    total_orders = df_olist["order_id"].nunique()
    avg_order_value = df_olist.groupby("order_id")["payment_value"].sum().mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos totales", f"{total_revenue:,.2f} €")
    col2.metric("Pedidos", f"{total_orders}")
    col3.metric("Ticket medio", f"{avg_order_value:,.2f} €")

    st.divider()

    # Top categorías
    st.subheader("Top categorías por ingresos")

    top_categories = (
        df_olist.groupby("category_en")
        .agg({"payment_value": "sum"})
        .sort_values("payment_value", ascending=False)
        .head(10)
        .reset_index()
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_categories, x="payment_value", y="category_en", ax=ax2)
    ax2.set_title("Top categorías por ingresos")
    ax2.set_xlabel("Ingresos")
    ax2.set_ylabel("Categoría")
    st.pyplot(fig2)

    st.divider()

    # Ventas por estado
    st.subheader("Top estados por ingresos")

    ventas_estados = (
        df_olist.groupby("state")
        .agg({"payment_value": "sum"})
        .sort_values("payment_value", ascending=False)
        .head(10)
        .reset_index()
    )

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=ventas_estados, x="payment_value", y="state", ax=ax3)
    ax3.set_title("Top estados por ingresos")
    ax3.set_xlabel("Ingresos")
    ax3.set_ylabel("Estado")
    st.pyplot(fig3)

# -----------------------------
# LOGÍSTICA
# -----------------------------
elif page == "Logística":
    st.title("Logística")

 # KPIs
    avg_delivery_time = df_olist["delivery_time_days"].mean()
    avg_delay = df_olist["delivery_delay"].mean()
    pct_delayed = (df_olist["delivery_delay"] > 0).mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Tiempo medio de entrega", f"{avg_delivery_time:.2f} días")
    col2.metric("Retraso medio", f"{avg_delay:.2f} días")
    col3.metric("% pedidos retrasados", f"{pct_delayed:.2f}%")

    st.divider()

    # Distribución tiempo de entrega
    st.subheader("Distribución del tiempo de entrega")

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.histplot(df_olist["delivery_time_days"].dropna(), bins=50, ax=ax4)
    ax4.set_title("Distribución del tiempo de entrega")
    ax4.set_xlabel("Días de entrega")
    ax4.set_ylabel("Frecuencia")
    st.pyplot(fig4)

    st.divider()

    # Análisis retraso
    delay_analysis = df_olist.groupby("delay_flag").agg({
        "order_id": "nunique",
        "delivery_time_days": "mean"
    }).reset_index()

    delay_analysis["delay_status"] = delay_analysis["delay_flag"].map({
        0: "En plazo o antes",
        1: "Con retraso"
    })

    col1, col2 = st.columns(2)

    with col1:
        fig5, ax5 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=delay_analysis, x="delay_status", y="order_id", ax=ax5)
        ax5.set_title("Número de pedidos según retraso")
        ax5.set_xlabel("")
        ax5.set_ylabel("Número de pedidos")
        st.pyplot(fig5)

    with col2:
        fig6, ax6 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=delay_analysis, x="delay_status", y="delivery_time_days", ax=ax6)
        ax6.set_title("Tiempo medio de entrega según retraso")
        ax6.set_xlabel("")
        ax6.set_ylabel("Días de entrega")
        st.pyplot(fig6)

    st.divider()

    # Comparativa por estado
    st.subheader("Estados con mayor retraso medio")

    logistica_estado = (
        df_olist.groupby("state")
        .agg({
            "delivery_time_days": "mean",
            "delivery_delay": "mean"
        })
        .sort_values("delivery_delay", ascending=False)
    )

    top_logistica_estado = logistica_estado.head(10).reset_index()

    fig7, ax7 = plt.subplots(figsize=(12, 6))
    x = np.arange(len(top_logistica_estado))
    width = 0.35

    ax7.bar(x - width/2, top_logistica_estado["delivery_time_days"], width, label="Tiempo entrega")
    ax7.bar(x + width/2, top_logistica_estado["delivery_delay"], width, label="Retraso")

    ax7.set_xticks(x)
    ax7.set_xticklabels(top_logistica_estado["state"])
    ax7.set_title("Comparativa logística por estado")
    ax7.set_xlabel("Estado")
    ax7.set_ylabel("Días")
    ax7.legend()

    st.pyplot(fig7)

# -----------------------------
# CLIENTES
# -----------------------------
elif page == "Clientes":
    st.title("Clientes")
    # KPIs
    total_customers = df_olist["id_user"].nunique()
    clientes_pedidos = df_olist.groupby("id_user")["order_id"].nunique()
    repeat_customers = (clientes_pedidos > 1).sum()
    repeat_pct = repeat_customers / total_customers * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes únicos", f"{total_customers}")
    col2.metric("Clientes recurrentes", f"{repeat_customers}")
    col3.metric("% recurrentes", f"{repeat_pct:.2f}%")

    st.divider()

    # Top clientes
    st.subheader("Distribución del gasto entre top clientes")

    top_clientes = (
        df_olist.groupby("customer_id")
        .agg({
            "payment_value": "sum",
            "order_id": "nunique"
        })
        .sort_values("payment_value", ascending=False)
        .head(10)
        .reset_index()
    )

    top_clientes["cliente"] = [f"Cliente {i+1}" for i in range(len(top_clientes))]

    fig8, ax8 = plt.subplots(figsize=(8, 8))
    ax8.pie(
        top_clientes["payment_value"],
        labels=top_clientes["cliente"],
        autopct="%1.1f%%"
    )
    ax8.set_title("Distribución del gasto entre top clientes")
    st.pyplot(fig8)

    st.divider()

    # Curva de Pareto
    st.subheader("Curva de Pareto de clientes")

    df_clientes = df_olist.groupby("customer_id")["payment_value"].sum().reset_index()
    df_clientes = df_clientes.sort_values("payment_value", ascending=False)

    df_clientes["cum_pct"] = df_clientes["payment_value"].cumsum() / df_clientes["payment_value"].sum()
    df_clientes["cliente_pct"] = (df_clientes.index + 1) / len(df_clientes)

    df_clientes_sorted = df_clientes.sort_values("cliente_pct")
    df_clientes_sorted["bin"] = pd.cut(df_clientes_sorted["cliente_pct"], bins=100)

    pareto_smooth = df_clientes_sorted.groupby("bin", observed=False).agg({
        "cliente_pct": "mean",
        "cum_pct": "mean"
    }).reset_index()

    fig9, ax9 = plt.subplots(figsize=(10, 5))
    ax9.plot(pareto_smooth["cliente_pct"], pareto_smooth["cum_pct"])
    ax9.axhline(0.8, linestyle="--")
    ax9.axvline(0.2, linestyle="--")
    ax9.set_title("Curva de Pareto de clientes")
    ax9.set_xlabel("% de clientes")
    ax9.set_ylabel("% de ingresos")
    st.pyplot(fig9)

    st.divider()

    # Clientes por estado
    st.subheader("Clientes por estado")

    clientes_estado = (
        df_olist.groupby("state")["customer_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig10, ax10 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=clientes_estado, x="customer_id", y="state", ax=ax10)
    ax10.set_title("Top estados por clientes únicos")
    ax10.set_xlabel("Clientes únicos")
    ax10.set_ylabel("Estado")
    st.pyplot(fig10)



# -----------------------------
# SATISFACCIÓN
# -----------------------------
elif page == "Satisfacción":
    st.title("Satisfacción")

    pct_5 = (df_orders["review_score"] == 5).mean() * 100
    pct_1 = (df_orders["review_score"] == 1).mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Review media", round(avg_review, 2))
    col2.metric("% 5 estrellas", f"{pct_5:.2f}%")
    col3.metric("% 1 estrella", f"{pct_1:.2f}%")

    review_dist = (
        df_orders.groupby("review_score", as_index=False)
        .agg(order_id=("order_id", "nunique"))
        .sort_values("review_score")
    )

    fig1 = px.bar(review_dist, x="review_score", y="order_id", title="Distribución de reviews")
    st.plotly_chart(fig1, use_container_width=True)

    review_delay = (
        df_orders.groupby("delivery_delay", as_index=False)
        .agg(
            review_score=("review_score", "mean"),
            order_id=("order_id", "nunique")
        )
    )

    fig2 = px.scatter(
        review_delay,
        x="delivery_delay",
        y="review_score",
        size="order_id",
        title="Relación entre retraso y satisfacción"
    )
    st.plotly_chart(fig2, use_container_width=True)