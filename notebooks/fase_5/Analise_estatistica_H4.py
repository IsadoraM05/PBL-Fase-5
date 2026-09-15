import os
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt

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

print("\n=== H4 - CHUVA X OCUPAÇÃO ===")

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
plt.savefig(
    os.path.join(PASTA_GRAFICOS, "H4_chuva_ocupacao.png"),
    dpi=150,
    bbox_inches="tight"
)
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
