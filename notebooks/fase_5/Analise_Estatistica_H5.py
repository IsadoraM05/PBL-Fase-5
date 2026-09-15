import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, linregress

# Pasta de saida dos graficos (PNG para o relatorio)
PASTA_GRAFICOS = Path(__file__).resolve().parents[2] / "relatorio" / "graficos"
os.makedirs(PASTA_GRAFICOS, exist_ok=True)


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

print("Bases carregadas com sucesso!")
print(f"Viagens: {df_viagens.shape}")
print(f"Eventos: {df_eventos.shape}")

# ============================================================
# H5 - OCUPAÇÃO X CONSUMO ENERGÉTICO POR KM
# ============================================================

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
plt.savefig(
    os.path.join(PASTA_GRAFICOS, "H5_ocupacao_consumo.png"),
    dpi=150,
    bbox_inches="tight"
)
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
plt.savefig(
    os.path.join(PASTA_GRAFICOS, "H5_ocupacao_consumo_regressao.png"),
    dpi=150,
    bbox_inches="tight"
)
plt.show()

# ============================================================
# CONCLUSÃO - H5
# ============================================================

print("\n=== CONCLUSÃO - H5 ===")

alpha = 0.05

if p_pearson < alpha and r_pearson > 0:
    print("Resultado: rejeitamos H0.")
    print(
        "Há evidências de associação positiva estatisticamente "
        "significativa entre a ocupação média e o consumo "
        "energético por km."
    )
else:
    print("Resultado: não rejeitamos H0.")
    print(
        "Não há evidências estatísticas suficientes para afirmar "
        "que maior ocupação esteja associada a maior consumo "
        "energético por km."
    )

print(
    f"\nA regressão linear indica que a ocupação sozinha explica "
    f"{regressao.rvalue**2 * 100:.1f}% da variação do consumo "
    f"energético por km (R² = {regressao.rvalue**2:.4f})."
)

# ATENÇÃO - possível confundimento:
# A ocupação média também é correlacionada com o congestionamento
# (r ≈ 0,45 nesta base), e o congestionamento por si só também está
# associado ao consumo energético. Portanto, parte da relação medida
# aqui entre ocupação e consumo pode estar sendo influenciada por esse
# terceiro fator, e não apenas pelo peso dos passageiros. Isolar os dois
# efeitos exigiria regressão múltipla ou correlação parcial, o que está
# fora do escopo desta hipótese.

print(
    "\nObservação (limitação): a ocupação também é correlacionada com o "
    "congestionamento, que por sua vez também se associa ao consumo. "
    "Parte da relação observada pode, portanto, ser influenciada por "
    "esse terceiro fator."
)

"""
CONCLUSÃO - H5

A correlação de Pearson entre ocupação média e consumo energético por km
foi de 0,5975 (p < 0.001) e a de Spearman, 0,5745 (p < 0.001): uma
associação positiva moderada e estatisticamente significativa. Quanto
mais cheio o ônibus, maior o consumo de energia por quilômetro rodado.

A regressão linear reforça o resultado: cada ponto percentual a mais de
ocupação está associado a cerca de 0,0058 kWh/km a mais de consumo, e a
ocupação sozinha explica aproximadamente 35,7% da variação do consumo
(R² = 0,3570). Os outros ~64% vêm de fatores não considerados nesta
hipótese.

LIMITAÇÃO - possível confundimento:
A ocupação média não é independente do congestionamento (r ≈ 0,45 nesta
base), e o congestionamento também está associado ao consumo energético.
Isso significa que parte do efeito atribuído aqui à ocupação pode, na
verdade, vir do trânsito enfrentado na viagem. A associação continua
existindo, mas seu tamanho deve ser lido com cautela: separar as duas
contribuições exigiria uma regressão múltipla, que não foi aplicada
neste trabalho.
"""