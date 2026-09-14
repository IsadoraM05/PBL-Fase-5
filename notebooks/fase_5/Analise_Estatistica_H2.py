import pandas as pd
import numpy as np
from scipy.stats import shapiro, spearmanr, chi2_contingency
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