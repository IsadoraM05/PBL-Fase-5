from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, linregress

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