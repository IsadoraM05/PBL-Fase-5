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
plt.savefig(
    os.path.join(PASTA_GRAFICOS, "H6_movimentacao_tempo_parada.png"),
    dpi=150,
    bbox_inches="tight"
)
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
