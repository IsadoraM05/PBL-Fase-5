import pandas as pd
import numpy as np
from scipy.stats import shapiro, spearmanr
import matplotlib.pyplot as plt

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

# H1 - Congestionamento x Atraso

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