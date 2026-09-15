import pandas as pd
import numpy as np
from scipy.stats import shapiro, spearmanr
import matplotlib.pyplot as plt

#=================== PREPARAÇÃO DOS DADOS ==================#

# Caminho da base de dados
caminho = Path(__file__).resolve().parents[2] / "dados" / "Dados PBL fase 5.xlsx"

# Carregando as bases
df_viagens = pd.read_excel(
    caminho,
    sheet_name="viagens_onibus_autonomos_cidade"
)

df_eventos = pd.read_excel(
    caminho,
    sheet_name="eventos_parada_cidade_alfa"
)

print("Base de viagens:")
print(df_viagens.head())

print("\nBase de eventos de parada:")
print(df_eventos.head())

# Inspeção inicial das bases

print("Dimensões da base de viagens:")
print(df_viagens.shape)

print("\nDimensões da base de eventos:")
print(df_eventos.shape)

print("\n=== TIPOS DE DADOS - BASE DE VIAGENS ===")
print(df_viagens.dtypes.to_string())

print("\n=== TIPOS DE DADOS - BASE DE EVENTOS ===")
print(df_eventos.dtypes.to_string())

# Verificação de valores nulos

print("\n=== VALORES NULOS - BASE DE VIAGENS ===")
print(df_viagens.isnull().sum())

print("\n=== VALORES NULOS - BASE DE EVENTOS ===")
print(df_eventos.isnull().sum())

""" 
Resultado:
Não foram identificados valores nulos em nenhuma das duas bases.
Portanto, não foi necessário realizar imputação ou remoção de registros
por ausência de dados.
"""

# Verificação de registros duplicados

print("\n=== DUPLICIDADES - BASE DE VIAGENS ===")
print("Registros duplicados:", df_viagens.duplicated().sum())

print("\n=== DUPLICIDADES - BASE DE EVENTOS ===")
print("Registros duplicados:", df_eventos.duplicated().sum())

# Carregando o dicionário de dados

df_dicionario = pd.read_excel(
    caminho,
    sheet_name="dicionario_dados"
)

print("\n=== DICIONÁRIO DE DADOS ===")
print(df_dicionario.to_string(index=False))

# Verificação de valores negativos

colunas_nao_negativas_viagens = [
    "distancia_km",
    "tempo_previsto_min",
    "tempo_real_min",
    "velocidade_media_kmh",
    "congestionamento_pct",
    "qt_paradas",
    "qt_passageiros_embarcados",
    "ocupacao_media_pct",
    "ocupacao_maxima_pct",
    "tempo_medio_parada_min",
    "paradas_com_atraso",
    "chuva_mm",
    "qt_incidentes",
    "consumo_energia_kwh",
    "eficiencia_kwh_km"
]

print("\n=== VALORES NEGATIVOS - BASE DE VIAGENS ===")

for coluna in colunas_nao_negativas_viagens:
    quantidade = (df_viagens[coluna] < 0).sum()
    print(f"{coluna}: {quantidade}")

# Verificação dos percentuais - Base de viagens

colunas_percentuais_viagens = [
    "congestionamento_pct",
    "ocupacao_media_pct",
    "ocupacao_maxima_pct"
]

print("\n=== VALORES FORA DA FAIXA 0-100% - BASE DE VIAGENS ===")

for coluna in colunas_percentuais_viagens:
    fora_faixa = ((df_viagens[coluna] < 0) | (df_viagens[coluna] > 100)).sum()
    print(f"{coluna}: {fora_faixa}")

# Verificação dos percentuais - Base de eventos

print("\n=== VALORES FORA DA FAIXA 0-100% - BASE DE EVENTOS ===")

fora_faixa = (
    (df_eventos["ocupacao_pct"] < 0) |
    (df_eventos["ocupacao_pct"] > 100)
).sum()

print(f"ocupacao_pct: {fora_faixa}")

# Verificação de integridade referencial

viagens_ids = set(df_viagens["id_viagem"])

eventos_sem_viagem = ~df_eventos["id_viagem"].isin(viagens_ids)

print("\n=== INTEGRIDADE REFERENCIAL ===")
print(
    "Eventos com id_viagem inexistente na base de viagens:",
    eventos_sem_viagem.sum()
)

# Verificação da consistência do atraso

atraso_calculado = (
    df_viagens["tempo_real_min"] -
    df_viagens["tempo_previsto_min"]
)

inconsistencias_atraso = (
    atraso_calculado != df_viagens["atraso_min"]
).sum()

print("\n=== CONSISTÊNCIA DO ATRASO ===")
print(
    "Registros em que atraso_min não corresponde "
    "à diferença entre tempo real e previsto:",
    inconsistencias_atraso
)

# Verificação da consistência da ocupação

inconsistencias_ocupacao = (
    df_viagens["ocupacao_maxima_pct"] <
    df_viagens["ocupacao_media_pct"]
).sum()

print("\n=== CONSISTÊNCIA DA OCUPAÇÃO ===")
print(
    "Viagens em que a ocupação máxima é menor que a ocupação média:",
    inconsistencias_ocupacao
)

# Verificação da consistência das paradas com atraso

inconsistencias_paradas = (
    df_viagens["paradas_com_atraso"] >
    df_viagens["qt_paradas"]
).sum()

print("\n=== CONSISTÊNCIA DAS PARADAS ===")
print(
    "Viagens em que o número de paradas com atraso "
    "é maior que o total de paradas:",
    inconsistencias_paradas
)

# Verificação das datas

print("\n=== PERÍODO DA BASE DE VIAGENS ===")
print("Data inicial:", df_viagens["data_viagem"].min())
print("Data final:", df_viagens["data_viagem"].max())

print("\n=== PERÍODO DA BASE DE EVENTOS ===")
print("Data inicial:", df_eventos["data_evento"].min())
print("Data final:", df_eventos["data_evento"].max())

# Categorias existentes

print("\n=== CATEGORIAS - DIA DA SEMANA ===")
print(df_viagens["dia_semana"].value_counts())

print("\n=== CATEGORIAS - PERÍODO ===")
print(df_viagens["periodo"].value_counts())

print("\n=== CATEGORIAS - TIPO DE INCIDENTE ===")
print(df_viagens["tipo_incidente"].value_counts())

print("\n=== CATEGORIAS - STATUS DA VIAGEM ===")
print(df_viagens["status_viagem"].value_counts())

# Quantidade de eventos por viagem

eventos_por_viagem = df_eventos.groupby("id_viagem").size()

print("\n=== EVENTOS POR VIAGEM ===")
print(eventos_por_viagem.describe())

# Consistência entre quantidade de paradas e eventos registrados

eventos_por_viagem = df_eventos.groupby("id_viagem").size()

comparacao_paradas = df_viagens[["id_viagem", "qt_paradas"]].copy()

comparacao_paradas["eventos_registrados"] = (
    comparacao_paradas["id_viagem"].map(eventos_por_viagem)
)

comparacao_paradas["diferenca"] = (
    comparacao_paradas["qt_paradas"]
    - comparacao_paradas["eventos_registrados"]
)

inconsistencias = comparacao_paradas[
    comparacao_paradas["diferenca"] != 0
]

print("\n=== CONSISTÊNCIA ENTRE PARADAS E EVENTOS ===")
print(
    "Viagens com diferença entre qt_paradas e eventos:",
    len(inconsistencias)
)

if len(inconsistencias) > 0:
    print("\nExemplos de inconsistências:")
    print(inconsistencias.head())

""" 
CONCLUSÃO DA QUALIDADE DOS DADOS

As bases de viagens e eventos foram avaliadas quanto a:
- valores nulos
- registros duplicados
- valores negativos
- limites de variáveis percentuais
- integridade referencial
- consistência entre variáveis
- consistência entre as bases

Não foram identificadas inconsistências que exigissem
exclusão ou correção de registros.

As bases estão aptas para a etapa de análise estatística.
"""


#================ TESTANDO HIPÓTESES ==================#

# Caminho da base de dados
caminho = "dados/Dados PBL fase 5.xlsx"

# Carregando as bases
df_viagens = pd.read_excel(
    caminho,
    sheet_name="viagens_onibus_autonomos_cidade"
)

df_eventos = pd.read_excel(
    caminho,
    sheet_name="eventos_parada_cidade_alfa"
)

print("Bases carregadas com sucesso!")
print(f"Viagens: {df_viagens.shape}")
print(f"Eventos: {df_eventos.shape}")

#================== PRIMEIRA HIPÓTESE ==================#

# H1 - CONGESTIONAMENTO x ATRASO 

print("\n=== H1 - CONGESTIONAMENTO X ATRASO ===")

print("\nEstatísticas do congestionamento:")
print(df_viagens["congestionamento_pct"].describe())

print("\nEstatísticas do atraso:")
print(df_viagens["atraso_min"].describe())

# Relação entre congestionamento e atraso


plt.figure(figsize=(8, 5))

plt.scatter(
    df_viagens["congestionamento_pct"],
    df_viagens["atraso_min"],
    alpha=0.5
)

plt.xlabel("Congestionamento (%)")
plt.ylabel("Atraso (minutos)")
plt.title("Relação entre Congestionamento e Atraso")

plt.show()

# Correlação - H1
correlacao = df_viagens["congestionamento_pct"].corr(
    df_viagens["atraso_min"]
)

print("\n=== CORRELAÇÃO (Pearson)- H1 ===")
print(f"Correlação: {correlacao:.4f}")

# H1 - Congestionamento x Atraso
# Hipótese: quanto maior o congestionamento, maior tende a ser o atraso.
# Variáveis analisadas: congestionamento_pct e atraso_min

# Teste de normalidade - Shapiro-Wilk

print("\n=== TESTE DE NORMALIDADE - H1 ===")

stat_cong, p_cong = shapiro(df_viagens["congestionamento_pct"])
stat_atraso, p_atraso = shapiro(df_viagens["atraso_min"])

print(f"Congestionamento: p-valor = {p_cong:.6f}")
print(f"Atraso: p-valor = {p_atraso:.6f}")

alpha = 0.05

if p_cong < alpha:
    print("Congestionamento: distribuição não normal.")
else:
    print("Congestionamento: não há evidências suficientes para rejeitar a normalidade.")

if p_atraso < alpha:
    print("Atraso: distribuição não normal.")
else:
    print("Atraso: não há evidências suficientes para rejeitar a normalidade.")

# Correlação de Spearman

print("\n=== TESTE DE SPEARMAN - H1 ===")

rho, p_valor = spearmanr(
    df_viagens["congestionamento_pct"],
    df_viagens["atraso_min"]
)

print(f"Correlação de Spearman: {rho:.4f}")
print(f"P-valor: {p_valor:.6f}")

alpha = 0.05

if p_valor < alpha:
    print("Resultado: rejeitamos H0.")
    print("Existe associação estatisticamente significativa entre congestionamento e atraso.")
else:
    print("Resultado: não rejeitamos H0.")
    print("Não há evidências estatísticas suficientes de associação entre congestionamento e atraso.")


# ============ SEGUNDA HIPÓTESE ============ #

print("\n=== H2 - PERÍODOS DO DIA X ATRASO ===")

print("\nEstatísticas dos períodos do dia:")
print(df_viagens["periodo"].describe())

print("\nEstatísticas do atraso:")
print(df_viagens["atraso_min"].describe())

df_viagens["status_atraso"] = np.where(
    df_viagens["atraso_min"] > 0,
    "Atrasado",
    "No horario"
)

# Frequência de cada categoria
print("\nPeríodos:")
print(df_viagens["periodo"].value_counts())

print("\nStatus das viagens:")
print(df_viagens["status_atraso"].value_counts())

# Tabela de contingência
tabela_h2 = pd.crosstab(
    df_viagens["periodo"],
    df_viagens["status_atraso"]
)

print("\n=== TABELA DE CONTINGÊNCIA ===")
print(tabela_h2)

# ============================================================
# TESTE QUI-QUADRADO - H2
# ============================================================

print("\n=== TESTE QUI-QUADRADO - H2 ===")

chi2, p_valor, graus_liberdade, frequencias_esperadas = chi2_contingency(
    tabela_h2
)

print(f"Qui-quadrado: {chi2:.4f}")
print(f"Graus de liberdade: {graus_liberdade}")

if p_valor < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_valor:.4f}")

frequencias_esperadas_df = pd.DataFrame(
    frequencias_esperadas,
    index=tabela_h2.index,
    columns=tabela_h2.columns
)

print("\nFrequências esperadas caso H0 seja verdadeira:")
print(frequencias_esperadas_df.round(2))

alpha = 0.05

if p_valor < alpha:
    print("\nResultado: rejeitamos H0.")
    print(
        "Há associação estatisticamente significativa "
        "entre o período do dia e a ocorrência de atraso."
    )
else:
    print("\nResultado: não rejeitamos H0.")
    print(
        "Não há evidências estatísticas suficientes de associação "
        "entre o período do dia e a ocorrência de atraso."
    )

# ============================================================
# V DE CRAMER - H2
# ============================================================

print("\n=== V DE CRAMER - H2 ===")

n = tabela_h2.to_numpy().sum()

linhas, colunas = tabela_h2.shape

v_cramer = np.sqrt(
    chi2 / (n * min(linhas - 1, colunas - 1))
)

print(f"V de Cramer: {v_cramer:.4f}")

print("\n=== PERCENTUAL DE ATRASOS POR PERÍODO ===")

percentuais_h2 = pd.crosstab(
    df_viagens["periodo"],
    df_viagens["status_atraso"],
    normalize="index"
) * 100

print(percentuais_h2.round(2))

#=========== TERCEIRA HIPÓTESE ============#
print("\n=== H3 - CHUVA X CONGESTIONAMENTO ===")

print("\nEstatísticas da chuva:")
print(df_viagens["chuva_mm"].describe())

print("\nEstatísticas do congestionamento:")
print(df_viagens["congestionamento_pct"].describe())

plt.figure(figsize=(8, 5))

plt.scatter(
    df_viagens["chuva_mm"],
    df_viagens["congestionamento_pct"],
    alpha=0.5
)

plt.title("Chuva x Congestionamento")
plt.xlabel("Chuva (mm)")
plt.ylabel("Congestionamento (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

print("\n=== CORRELAÇÃO DE PEARSON - H3 ===")

r_pearson, p_pearson = pearsonr(
    df_viagens["chuva_mm"],
    df_viagens["congestionamento_pct"]
)

print(f"Correlação de Pearson: {r_pearson:.4f}")

if p_pearson < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_pearson:.4f}")


print("\n=== CORRELAÇÃO DE SPEARMAN - H3 ===")

rho, p_spearman = spearmanr(
    df_viagens["chuva_mm"],
    df_viagens["congestionamento_pct"]
)

print(f"Correlação de Spearman: {rho:.4f}")

if p_spearman < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_spearman:.4f}")

# ============================================================
# CONCLUSÃO - H3
# ============================================================

print("\n=== CONCLUSÃO - H3 ===")

alpha = 0.05

if p_spearman < alpha and rho > 0:
    print("Resultado: rejeitamos H0.")
    print(
        "Há evidências de associação positiva estatisticamente "
        "significativa entre chuva e congestionamento."
    )
else:
    print("Resultado: não rejeitamos H0.")
    print(
        "Não há evidências estatísticas suficientes para afirmar "
        "que maiores volumes de chuva estejam associados a "
        "maiores níveis de congestionamento."
    )


# ================== QUARTA HIPÓTESE ==================#

rint("\n=== H4 - CHUVA X OCUPAÇÃO ===")

print("\nEstatísticas da chuva:")
print(df_viagens["chuva_mm"].describe())

print("\nEstatísticas da ocupação:")
print(df_viagens["ocupacao_media_pct"].describe())

plt.figure(figsize=(8, 5))

plt.scatter(
    df_viagens["chuva_mm"],
    df_viagens["ocupacao_media_pct"],
    alpha=0.5
)

plt.title("Chuva x Ocupação média")
plt.xlabel("Chuva (mm)")
plt.ylabel("Ocupação média (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

# ============================================================
# CORRELAÇÃO DE PEARSON
# ============================================================

print("\n=== CORRELAÇÃO DE PEARSON - H4 ===")

r_pearson, p_pearson = pearsonr(
    df_viagens["chuva_mm"],
    df_viagens["ocupacao_media_pct"]
)

print(f"Correlação de Pearson: {r_pearson:.4f}")

if p_pearson < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_pearson:.4f}")

# ============================================================
# CORRELAÇÃO DE SPEARMAN
# ============================================================

print("\n=== CORRELAÇÃO DE SPEARMAN - H4 ===")

rho, p_spearman = spearmanr(
    df_viagens["chuva_mm"],
    df_viagens["ocupacao_media_pct"]
)

print(f"Correlação de Spearman: {rho:.4f}")

if p_spearman < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_spearman:.4f}")

# ============================================================
# CONCLUSÃO
# ============================================================

print("\n=== CONCLUSÃO - H4 ===")

alpha = 0.05

if p_spearman < alpha and rho > 0:
    print("Resultado: rejeitamos H0.")
    print(
        "Há evidências de associação positiva estatisticamente "
        "significativa entre chuva e ocupação média."
    )
else:
    print("Resultado: não rejeitamos H0.")
    print(
        "Não há evidências estatísticas suficientes para afirmar "
        "que maiores volumes de chuva estejam associados a "
        "maiores níveis de ocupação."
    )

#============ QUINTA HIPÓTESE ============#

print("\n=== H5 - OCUPAÇÃO X CONSUMO ENERGÉTICO POR KM ===")

print("\nEstatísticas da ocupação média:")
print(df_viagens["ocupacao_media_pct"].describe())

print("\nEstatísticas do consumo energético por km:")
print(df_viagens["eficiencia_kwh_km"].describe())

# ============================================================
# GRÁFICO DE DISPERSÃO
# ============================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    df_viagens["ocupacao_media_pct"],
    df_viagens["eficiencia_kwh_km"],
    alpha=0.5
)

plt.title("Ocupação média x Consumo energético por km")
plt.xlabel("Ocupação média (%)")
plt.ylabel("Consumo energético (kWh/km)")
plt.grid(True)
plt.tight_layout()
plt.show()

# ============================================================
# CORRELAÇÃO DE PEARSON
# ============================================================

print("\n=== CORRELAÇÃO DE PEARSON - H5 ===")

r_pearson, p_pearson = pearsonr(
    df_viagens["ocupacao_media_pct"],
    df_viagens["eficiencia_kwh_km"]
)

print(f"Correlação de Pearson: {r_pearson:.4f}")

if p_pearson < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_pearson:.4f}")

# ============================================================
# CORRELAÇÃO DE SPEARMAN
# ============================================================

print("\n=== CORRELAÇÃO DE SPEARMAN - H5 ===")

rho, p_spearman = spearmanr(
    df_viagens["ocupacao_media_pct"],
    df_viagens["eficiencia_kwh_km"]
)

print(f"Correlação de Spearman: {rho:.4f}")

if p_spearman < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_spearman:.4f}")

# ============================================================
# REGRESSÃO LINEAR - H5
# ============================================================

print("\n=== REGRESSÃO LINEAR - H5 ===")

x = df_viagens["ocupacao_media_pct"]
y = df_viagens["eficiencia_kwh_km"]

regressao = linregress(x, y)

print(f"Intercepto: {regressao.intercept:.4f}")
print(f"Coeficiente angular: {regressao.slope:.4f}")
print(f"R²: {regressao.rvalue**2:.4f}")

if regressao.pvalue < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {regressao.pvalue:.4f}")

plt.figure(figsize=(8, 5))

plt.scatter(
    x,
    y,
    alpha=0.5,
    label="Viagens"
)

plt.plot(
    x,
    regressao.intercept + regressao.slope * x,
    label="Regressão linear"
)

plt.title("Ocupação média x Consumo energético por km")
plt.xlabel("Ocupação média (%)")
plt.ylabel("Consumo energético (kWh/km)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ================= SEXTA HIPÓTESE ==================#

print("\n=== H6 - MOVIMENTAÇÃO DE PASSAGEIROS X TEMPO DE PARADA ===")

# Movimentação total de passageiros em cada parada
df_eventos["movimentacao_passageiros"] = (
    df_eventos["embarques"] +
    df_eventos["desembarques"]
)

# ============================================================
# ESTATÍSTICAS DESCRITIVAS
# ============================================================

print("\nEstatísticas da movimentação de passageiros:")
print(df_eventos["movimentacao_passageiros"].describe())

print("\nEstatísticas do tempo de parada:")
print(df_eventos["tempo_parada_min"].describe())

# ============================================================
# GRÁFICO DE DISPERSÃO
# ============================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    df_eventos["movimentacao_passageiros"],
    df_eventos["tempo_parada_min"],
    alpha=0.4
)

plt.title("Movimentação de passageiros x Tempo de parada")
plt.xlabel("Movimentação de passageiros (embarques + desembarques)")
plt.ylabel("Tempo de parada (min)")
plt.grid(True)
plt.tight_layout()
plt.show()

# ============================================================
# CORRELAÇÃO DE PEARSON
# ============================================================

print("\n=== CORRELAÇÃO DE PEARSON - H6 ===")

r_pearson, p_pearson = pearsonr(
    df_eventos["movimentacao_passageiros"],
    df_eventos["tempo_parada_min"]
)

print(f"Correlação de Pearson: {r_pearson:.4f}")

if p_pearson < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_pearson:.4f}")

# ============================================================
# CORRELAÇÃO DE SPEARMAN
# ============================================================

print("\n=== CORRELAÇÃO DE SPEARMAN - H6 ===")

rho, p_spearman = spearmanr(
    df_eventos["movimentacao_passageiros"],
    df_eventos["tempo_parada_min"]
)

print(f"Correlação de Spearman: {rho:.4f}")

if p_spearman < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_spearman:.4f}")

# ============================================================
# CONCLUSÃO
# ============================================================

print("\n=== CONCLUSÃO - H6 ===")

alpha = 0.05

if p_spearman < alpha and rho > 0:
    print("Resultado: rejeitamos H0.")
    print(
        "Há evidências de associação positiva estatisticamente "
        "significativa entre a movimentação de passageiros "
        "e o tempo de parada."
    )
else:
    print("Resultado: não rejeitamos H0.")
    print(
        "Não há evidências estatísticas suficientes para afirmar "
        "que maior movimentação de passageiros esteja associada "
        "a maior tempo de parada."
    )


#=============== DASHBOARDS ================#
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
caminho = "dados/Dados PBL fase 5.xlsx"

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

# Ocupação x Eficiência energética
with col2:
    st.markdown("**Ocupação x Eficiência energética**")

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.scatter(
        df_viagens["ocupacao_media_pct"],
        df_viagens["eficiencia_kwh_km"],
        alpha=0.35,
        s=18,
        color="#1F8A8A"
    )

    ax.set_xlabel("Ocupação média (%)")
    ax.set_ylabel("Eficiência (kWh/km)")

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
                congestionamento e atraso (r = 0,5633).
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
        <strong>Monitoramento de trechos congestionados</strong><br>
        Monitorar trechos com maior congestionamento,
        priorizando regiões onde o aumento do trânsito esteja
        associado a maiores atrasos.
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