import os
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import shapiro, kruskal
from scikit_posthocs import posthoc_dunn
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

print("Bases carregadas com sucesso!")
print(f"Viagens: {df_viagens.shape}")

# ============================================================
# H2 - PERÍODO DO DIA X ATRASO MÉDIO
# ============================================================
# Hipótese: viagens em horário de pico apresentam maior atraso médio
# H0 = Não há diferença significativa no atraso médio entre os períodos
# H1 = Há diferença significativa no atraso médio entre pelo menos dois períodos
# Variáveis: periodo (categórica) x atraso_min (numérica)
#
# Como estamos comparando a MÉDIA de uma variável numérica (atraso_min)
# entre MAIS DE DOIS grupos (períodos), o teste adequado é uma ANOVA
# (paramétrico) ou o Kruskal-Wallis (não paramétrico, equivalente à ANOVA
# quando os dados não seguem distribuição normal).

print("\n=== H2 - PERÍODO DO DIA X ATRASO MÉDIO ===")

print("\nEstatísticas descritivas do atraso por período:")
print(df_viagens.groupby("periodo")["atraso_min"].agg(["mean", "median", "std", "count"]))

# ============================================================
# TESTE DE NORMALIDADE POR GRUPO (Shapiro-Wilk)
# ============================================================
# Verificamos a normalidade do atraso dentro de cada período para decidir
# entre ANOVA (dados normais) e Kruskal-Wallis (dados não normais).

print("\n=== TESTE DE NORMALIDADE POR PERÍODO (Shapiro-Wilk) ===")

alpha = 0.05
algum_grupo_nao_normal = False

for periodo in df_viagens["periodo"].unique():
    amostra = df_viagens[df_viagens["periodo"] == periodo]["atraso_min"]
    stat, p_valor = shapiro(amostra)
    print(f"{periodo}: p-valor = {p_valor:.6f}")
    if p_valor < alpha:
        algum_grupo_nao_normal = True

if algum_grupo_nao_normal:
    print("\nPelo menos um período não segue distribuição normal.")
    print("Optamos pelo teste não paramétrico de Kruskal-Wallis.")
else:
    print("\nTodos os períodos são compatíveis com distribuição normal.")
    print("A ANOVA também seria adequada, mas seguimos com Kruskal-Wallis "
          "por ser mais robusto.")

# ============================================================
# BOXPLOT - ATRASO POR PERÍODO
# ============================================================

grupos_labels = df_viagens["periodo"].unique()
dados_boxplot = [
    df_viagens[df_viagens["periodo"] == p]["atraso_min"]
    for p in grupos_labels
]

plt.figure(figsize=(8, 5))
plt.boxplot(dados_boxplot, tick_labels=grupos_labels)
plt.title("Distribuição do atraso por período do dia")
plt.xlabel("Período")
plt.ylabel("Atraso (minutos)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(PASTA_GRAFICOS, "H2_periodo_atraso.png"),
    dpi=150,
    bbox_inches="tight"
)
plt.show()

# ============================================================
# TESTE DE KRUSKAL-WALLIS - H2
# ============================================================

print("\n=== TESTE DE KRUSKAL-WALLIS - H2 ===")

grupos = [
    df_viagens[df_viagens["periodo"] == p]["atraso_min"]
    for p in df_viagens["periodo"].unique()
]

estatistica_h, p_valor = kruskal(*grupos)

print(f"Estatística H: {estatistica_h:.4f}")

if p_valor < 0.001:
    print("P-valor: < 0.001")
else:
    print(f"P-valor: {p_valor:.6f}")

if p_valor < alpha:
    print("\nResultado: rejeitamos H0.")
    print(
        "Há diferença estatisticamente significativa no atraso médio "
        "entre pelo menos dois períodos do dia."
    )
else:
    print("\nResultado: não rejeitamos H0.")
    print(
        "Não há evidências estatísticas suficientes de diferença "
        "no atraso médio entre os períodos."
    )

# ============================================================
# TESTE POST-HOC DE DUNN (Bonferroni) - H2
# ============================================================
# O Kruskal-Wallis é um teste omnibus: indica que pelo menos dois períodos
# diferem, mas não diz quais. O post-hoc de Dunn compara todos os pares,
# e a correção de Bonferroni ajusta os p-valores pelo número de comparações
# (6 pares), evitando falsos positivos por testagem múltipla.

print("\n=== TESTE POST-HOC DE DUNN (Bonferroni) - H2 ===")

matriz_dunn = posthoc_dunn(
    df_viagens,
    val_col="atraso_min",
    group_col="periodo",
    p_adjust="bonferroni"
)

print("\nMatriz de p-valores ajustados:")
print(matriz_dunn.round(6).to_string())

# Leitura par a par (a partir do próprio resultado do teste)

print("\nComparações par a par:")

periodos_ordenados = list(matriz_dunn.columns)
pares_diferentes = []
pares_iguais = []

for i, periodo_a in enumerate(periodos_ordenados):
    for periodo_b in periodos_ordenados[i + 1:]:
        p_par = matriz_dunn.loc[periodo_a, periodo_b]

        if p_par < alpha:
            resultado = "diferença significativa"
            pares_diferentes.append((periodo_a, periodo_b))
        else:
            resultado = "sem diferença significativa"
            pares_iguais.append((periodo_a, periodo_b))

        print(f"{periodo_a} x {periodo_b}: p = {p_par:.6f} ({resultado})")

# Conclusão do post-hoc

print("\n--- Conclusão do post-hoc ---")

verbo_diferentes = "apresenta" if len(pares_diferentes) == 1 else "apresentam"
verbo_iguais = "apresenta" if len(pares_iguais) == 1 else "apresentam"

print(
    f"Dos {len(pares_diferentes) + len(pares_iguais)} pares comparados, "
    f"{len(pares_diferentes)} {verbo_diferentes} diferença estatisticamente "
    f"significativa no atraso e {len(pares_iguais)} não {verbo_iguais}."
)

if pares_diferentes:
    print("\nPares com diferença significativa (p < 0.05):")
    for periodo_a, periodo_b in pares_diferentes:
        print(f"  - {periodo_a} x {periodo_b}")

if pares_iguais:
    print("\nPares sem diferença significativa (p >= 0.05):")
    for periodo_a, periodo_b in pares_iguais:
        print(f"  - {periodo_a} x {periodo_b}")

# ============================================================
# CONCLUSÃO - H2
# ============================================================

"""
CONCLUSÃO - H2

O teste de Kruskal-Wallis mostrou diferença estatisticamente significativa
no atraso entre os períodos do dia (p < 0.001).

Observando as médias por período, os horários de Pico da Manhã e
Pico da Tarde apresentam atraso médio consideravelmente maior
(em torno de 5,8 a 5,9 minutos) do que os períodos de Entrepico
(2,4 minutos) e Noturno (1,0 minuto).

O teste post-hoc de Dunn com correção de Bonferroni confirma essa
leitura: 5 dos 6 pares de períodos apresentam diferença significativa.
A única exceção é Pico da Manhã x Pico da Tarde (p = 1,000), ou seja,
os dois horários de pico têm atraso equivalente entre si, mas ambos
diferem de Entrepico e de Noturno.

Isso confirma a hipótese de que viagens em horário de pico
apresentam maior atraso médio, reforçando a recomendação de reforço
operacional nos horários de pico já presente no dashboard.
"""
