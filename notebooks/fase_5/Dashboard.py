from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Alpha Transit - Dashboard",
    page_icon="🚌",
    layout="wide"
)

# Identidade visual
st.markdown("""
<style>

.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #123B4A;
    margin-bottom: 0;
    letter-spacing: -1px;
}

.main-subtitle {
    font-size: 1.05rem;
    color: #5F737B;
    margin-top: 0;
}

.alpha-line {
    height: 5px;
    border-radius: 10px;
    background: linear-gradient(
        90deg,
        #123B4A 0%,
        #1F8A8A 55%,
        #F2B84B 100%
    );
    margin: 10px 0 25px 0;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #123B4A;
    margin-top: 30px;
    margin-bottom: 15px;
    padding-left: 10px;
    border-left: 4px solid #1F8A8A;
}

.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    border: 1px solid #E1E8EB;
    border-top: 4px solid #1F8A8A;
    box-shadow: 0 2px 8px rgba(18, 59, 74, 0.08);
    min-height: 115px;
}

.kpi-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #5F737B;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #123B4A;
}

.insight-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #E1E8EB;
    border-left: 4px solid #1F8A8A;
    box-shadow: 0 2px 8px rgba(18, 59, 74, 0.06);
    min-height: 190px;
}

.insight-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #123B4A;
    margin-bottom: 10px;
}

.insight-text {
    font-size: 0.92rem;
    line-height: 1.55;
    color: #52656D;
}

.recommendation-card {
    background: #F4F8F9;
    border-radius: 10px;
    padding: 15px 18px;
    margin-bottom: 10px;
    border-left: 4px solid #F2B84B;
    color: #40545C;
    line-height: 1.5;
}

.sidebar-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #123B4A;
    margin-bottom: 5px;
}

.sidebar-text {
    font-size: 0.85rem;
    color: #5F737B;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown(
    '<div class="main-title">🚌 ALPHA TRANSIT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Inteligência para a mobilidade urbana da Cidade Alpha'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="alpha-line"></div>',
    unsafe_allow_html=True
)

# Caminho da base de dados
caminho = Path(__file__).resolve().parents[2] / "dados" / "Dados PBL fase 5.xlsx"

# Carregamento das bases
df_viagens = pd.read_excel(
    caminho,
    sheet_name="viagens_onibus_autonomos_cidade"
)

df_eventos = pd.read_excel(
    caminho,
    sheet_name="eventos_parada_cidade_alfa"
)

# Guarda a base original para análises que precisam considerar todos os períodos
df_viagens_base = df_viagens.copy()

# Filtro de período
periodos = ["Todos"] + sorted(
    df_viagens["periodo"].unique().tolist()
)

st.sidebar.markdown(
    '<div class="sidebar-title">🎛️ Filtros do painel</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-text">'
    'Selecione o período para explorar os indicadores.'
    '</div>',
    unsafe_allow_html=True
)

periodo_selecionado = st.sidebar.selectbox(
    "Período",
    periodos
)

# Aplica o filtro escolhido pelo usuário
if periodo_selecionado != "Todos":
    df_viagens = df_viagens[
        df_viagens["periodo"] == periodo_selecionado
    ]

    # Mantém nos eventos apenas as viagens do período selecionado
    ids_viagens = df_viagens["id_viagem"]

    df_eventos = df_eventos[
        df_eventos["id_viagem"].isin(ids_viagens)
    ]

# Indicadores principais
total_viagens = len(df_viagens)

atraso_medio = df_viagens["atraso_min"].mean()

congestionamento_medio = (
    df_viagens["congestionamento_pct"].mean()
)

ocupacao_media = (
    df_viagens["ocupacao_media_pct"].mean()
)

# Seção de indicadores
st.markdown(
    '<div class="section-title">📊 Indicadores principais</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🚌 Total de viagens</div>
            <div class="kpi-value">{total_viagens:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">⏱️ Atraso médio</div>
            <div class="kpi-value">{atraso_medio:.1f} min</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🚦 Congestionamento médio</div>
            <div class="kpi-value">{congestionamento_medio:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 Ocupação média</div>
            <div class="kpi-value">{ocupacao_media:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Seção de análise
st.markdown(
    '<div class="section-title">📈 Relações entre os indicadores</div>',
    unsafe_allow_html=True
)

# Congestionamento x Atraso
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Congestionamento x Atraso**")

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.scatter(
        df_viagens["congestionamento_pct"],
        df_viagens["atraso_min"],
        alpha=0.35,
        s=18,
        color="#1F8A8A"
    )

    ax.set_xlabel("Congestionamento (%)")
    ax.set_ylabel("Atraso (minutos)")

    ax.grid(
        alpha=0.18,
        linestyle="--",
        linewidth=0.7
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#123B4A")
    ax.spines["bottom"].set_color("#123B4A")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# Chuva x Congestionamento
with col2:
    st.markdown("**Chuva x Congestionamento**")

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.scatter(
        df_viagens["chuva_mm"],
        df_viagens["congestionamento_pct"],
        alpha=0.35,
        s=18,
        color="#1F8A8A"
    )

    ax.set_xlabel("Chuva (mm)")
    ax.set_ylabel("Congestionamento (%)")

    ax.grid(
        alpha=0.18,
        linestyle="--",
        linewidth=0.7
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#123B4A")
    ax.spines["bottom"].set_color("#123B4A")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# Chuva x Ocupação
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Chuva x Ocupação**")

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.scatter(
        df_viagens["chuva_mm"],
        df_viagens["ocupacao_media_pct"],
        alpha=0.35,
        s=18,
        color="#1F8A8A"
    )

    ax.set_xlabel("Chuva (mm)")
    ax.set_ylabel("Ocupação média (%)")

    ax.grid(
        alpha=0.18,
        linestyle="--",
        linewidth=0.7
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#123B4A")
    ax.spines["bottom"].set_color("#123B4A")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# Ocupação x Consumo energético por km
with col2:
    st.markdown("**Ocupação x Consumo energético (kWh/km)**")

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.scatter(
        df_viagens["ocupacao_media_pct"],
        df_viagens["eficiencia_kwh_km"],
        alpha=0.35,
        s=18,
        color="#1F8A8A"
    )

    ax.set_xlabel("Ocupação média (%)")
    ax.set_ylabel("Consumo energético (kWh/km)")

    ax.grid(
        alpha=0.18,
        linestyle="--",
        linewidth=0.7
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#123B4A")
    ax.spines["bottom"].set_color("#123B4A")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# Calcula a movimentação total em cada parada
df_eventos["movimentacao_passageiros"] = (
    df_eventos["embarques"] +
    df_eventos["desembarques"]
)

# Seção de operação nas paradas
st.markdown(
    '<div class="section-title">🚌 Operação e movimentação nas paradas</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("**Movimentação de passageiros x Tempo de parada**")

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.scatter(
        df_eventos["movimentacao_passageiros"],
        df_eventos["tempo_parada_min"],
        alpha=0.3,
        s=12,
        color="#1F8A8A"
    )

    ax.set_xlabel("Movimentação de passageiros")
    ax.set_ylabel("Tempo de parada (min)")

    ax.grid(
        alpha=0.18,
        linestyle="--",
        linewidth=0.7
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#123B4A")
    ax.spines["bottom"].set_color("#123B4A")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# Seção de desempenho por período
st.markdown(
    '<div class="section-title">🕐 Desempenho por período</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("**Atraso médio por período**")

    atraso_periodo = (
        df_viagens_base.groupby("periodo")["atraso_min"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.bar(
        atraso_periodo.index,
        atraso_periodo.values,
        color="#F2B84B"
    )

    ax.set_xlabel("Período")
    ax.set_ylabel("Atraso médio (min)")

    ax.grid(
        axis="y",
        alpha=0.18,
        linestyle="--",
        linewidth=0.7
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#123B4A")
    ax.spines["bottom"].set_color("#123B4A")

    plt.xticks(rotation=15)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# Insights
st.divider()

st.markdown(
    '<div class="section-title">💡 Principais insights</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">🚦 Congestionamento</div>
            <div class="insight-text">
                Foi observada uma correlação positiva moderada entre
                congestionamento e atraso
                (Spearman &rho; = 0,55; p &lt; 0,001).
                Isso indica que maiores níveis de congestionamento
                tendem a estar associados a maiores atrasos.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">🕐 Horários de pico</div>
            <div class="insight-text">
                Os períodos de pico da manhã e da tarde apresentam
                os maiores atrasos médios, indicando maior impacto
                sobre o tempo das viagens.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">🚌 Movimentação nas paradas</div>
            <div class="insight-text">
                Maior movimentação de passageiros nas paradas
                tende a estar associada a maior tempo de parada.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Recomendações
st.markdown(
    '<div class="section-title">🎯 Recomendações para a gestão pública</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="recommendation-card">
        <strong>Reforço operacional nos horários de pico</strong><br>
        Avaliar reforço operacional nos horários de pico,
        considerando os maiores atrasos observados nesses períodos.
    </div>

    <div class="recommendation-card">
        <strong>Monitoramento contínuo do congestionamento</strong><br>
        Monitorar continuamente os níveis de congestionamento da frota,
        já que ele está associado a mais atraso (H1), mas sem evidência
        até o momento de que alguma linha específica seja mais crítica
        que outra.
    </div>

    <div class="recommendation-card">
        <strong>Paradas com maior movimentação</strong><br>
        Identificar paradas com maior movimentação de passageiros,
        avaliando oportunidades para reduzir o tempo de embarque
        e desembarque.
    </div>
    """,
    unsafe_allow_html=True
)