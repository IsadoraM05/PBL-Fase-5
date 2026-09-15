"""
=============================================================
MoveData | AlphaTransit Intelligence | Cidade Alpha
FASE 4 – Desafio: Mobilidade Urbana

PERGUNTA 5: As viagens estão ficando mais atrasadas ao longo
            dos dias? Como o congestionamento influencia
            o tempo real de viagem por linha?

ENTREGÁVEL 2 – Análise Exploratória com Python
Versões: pandas 3.0.3 | NumPy 2.4.6 | Matplotlib 3.10+

Alinhamento com fases anteriores:
  - Fase 1: Persona Ana — depende de previsões confiáveis
  - Fase 2: RN01 (viagens), RN03 (trânsito), RN04 (desempenho)
  - Fase 3: Arquitetura Databricks Bronze → Silver → Gold
            Dados ingeridos: t_viagem, t_linha, t_transito
=============================================================
NOTAS DE COMPATIBILIDADE (pandas 3.0 - jan/2026):
  - Copy-on-Write ativo por padrão: modificações usam .loc
  - Colunas de string inferidas como dtype 'str' (não 'object')
  - groupby: observed=True é o novo padrão
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json

print(f"Versões: pandas {pd.__version__} | numpy {np.__version__}")

# =============================================================
# 1. CARREGAMENTO DO CSV GERADO PELA INSTRUÇÃO SQL
# =============================================================
df = pd.read_csv(
    'MoveData_atraso_transito.csv',
    sep=';',
    decimal=','
)

print("=" * 65)
print("MoveData | AlphaTransit Intelligence | ANÁLISE EXPLORATÓRIA")
print("Pergunta 5: Evolução do Atraso e Congestionamento nas Viagens")
print("=" * 65)
print(f"\n[1] Registros carregados: {len(df)}")
print(f"    Colunas: {list(df.columns)}")

# =============================================================
# 2. PREPARAÇÃO E TRANSFORMAÇÃO DOS DADOS
# =============================================================

# pandas 3.0: pd.to_datetime retorna dtype com resolução inferida
# (microseconds em vez de nanoseconds por padrão)
df['dt_inicio'] = pd.to_datetime(df['dt_inicio'])

# pandas 3.0: pd.to_numeric ainda funciona igual, sem mudanças
df['qt_tempo_previsto']           = pd.to_numeric(df['qt_tempo_previsto'], errors='coerce')
df['qt_tempo_real']               = pd.to_numeric(df['qt_tempo_real'], errors='coerce')
df['qt_nivel_congestionamento_pct'] = pd.to_numeric(df['qt_nivel_congestionamento_pct'], errors='coerce')
df['qt_velocidade_media_kmh']     = pd.to_numeric(df['qt_velocidade_media_kmh'], errors='coerce')

# Calcular atraso (positivo = atrasado, negativo = adiantado)
df['qt_atraso_min'] = df['qt_tempo_real'] - df['qt_tempo_previsto']

# Extrair data e hora com dt accessor (sem mudanças no pandas 3.0)
df['DATA']      = df['dt_inicio'].dt.date
df['DIA_SEMANA']= df['dt_inicio'].dt.day_name()
df['HORA']      = df['dt_inicio'].dt.hour
df['DIA']       = df['dt_inicio'].dt.day

# pandas 3.0 Copy-on-Write: usamos .loc para atribuição segura
# Classificação de desempenho (RN04 da Fase 2)
df.loc[df['qt_atraso_min'] <= 0, 'DS_DESEMPENHO']            = 'No horário / Adiantada'
df.loc[(df['qt_atraso_min'] > 0) & (df['qt_atraso_min'] <= 10), 'DS_DESEMPENHO'] = 'Atraso leve (1-10 min)'
df.loc[df['qt_atraso_min'] > 10, 'DS_DESEMPENHO']            = 'Atraso grave (>10 min)'

# Classificação de congestionamento
df.loc[df['qt_nivel_congestionamento_pct'] < 30,  'DS_CONGESTIONAMENTO'] = 'Livre (<30%)'
df.loc[(df['qt_nivel_congestionamento_pct'] >= 30) & (df['qt_nivel_congestionamento_pct'] < 60), 'DS_CONGESTIONAMENTO'] = 'Moderado (30-60%)'
df.loc[df['qt_nivel_congestionamento_pct'] >= 60, 'DS_CONGESTIONAMENTO'] = 'Congestionado (>60%)'

print(f"\n[2] Verificação de nulos após transformação:")
print(df[['qt_tempo_previsto','qt_tempo_real','qt_atraso_min',
          'qt_nivel_congestionamento_pct']].isnull().sum())

# Remover linhas com atraso nulo residual
df = df.dropna(subset=['qt_atraso_min'])
print(f"\n[3] Registros após limpeza: {len(df)}")

# pandas 3.0: verificação de dtype — strings agora são 'str', não 'object'
print(f"\n[4] Tipos de dados (pandas 3.0):")
print(df[['nm_linha','ds_status','DS_DESEMPENHO']].dtypes)

# =============================================================
# 3. ANÁLISE ESTATÍSTICA DESCRITIVA
# =============================================================
print("\n[5] Estatísticas descritivas do atraso (minutos):")
print(df['qt_atraso_min'].describe().round(2))

print("\n[6] Distribuição de desempenho das viagens (RN04):")
desemp_count = df['DS_DESEMPENHO'].value_counts()
desemp_pct   = df['DS_DESEMPENHO'].value_counts(normalize=True).mul(100).round(1)
print(pd.DataFrame({'Quantidade': desemp_count, 'Percentual (%)': desemp_pct}))

# pandas 3.0: groupby com observed=True é o padrão (não precisa declarar para strings)
df_dia = df.groupby('DIA', as_index=False).agg(
    QTD_VIAGENS              = ('id_viagem', 'count'),
    ATRASO_MEDIO             = ('qt_atraso_min', 'mean'),
    CONGESTIONAMENTO_MEDIO   = ('qt_nivel_congestionamento_pct', 'mean'),
    VELOCIDADE_MEDIA         = ('qt_velocidade_media_kmh', 'mean'),
    PCT_ATRASADAS            = ('qt_atraso_min', lambda x: (x > 0).mean() * 100),
).round(2)

print("\n[7] Atraso e congestionamento por dia do mês (maio/2026):")
print(df_dia.to_string(index=False))

df_linha = df.groupby('nm_linha', as_index=False).agg(
    QTD                     = ('id_viagem', 'count'),
    ATRASO_MEDIO            = ('qt_atraso_min', 'mean'),
    CONGESTIONAMENTO_MEDIO  = ('qt_nivel_congestionamento_pct', 'mean'),
    VELOCIDADE_MEDIA        = ('qt_velocidade_media_kmh', 'mean'),
).sort_values('ATRASO_MEDIO', ascending=False).round(2)

print("\n[8] Linhas com maior atraso médio (top 10):")
print(df_linha.head(10).to_string(index=False))

corr = df[['qt_atraso_min','qt_nivel_congestionamento_pct','qt_velocidade_media_kmh']].corr()
print("\n[9] Correlação entre variáveis:")
print(corr.round(3))

df_hora = df.groupby('HORA', as_index=False).agg(
    QTD           = ('id_viagem', 'count'),
    ATRASO_MEDIO  = ('qt_atraso_min', 'mean'),
    CONGESTIONAMENTO = ('qt_nivel_congestionamento_pct', 'mean'),
).round(2)

print("\n[10] Atraso médio por hora do dia:")
print(df_hora.to_string(index=False))

# =============================================================
# 4. VISUALIZAÇÕES (Matplotlib — sem mudanças na API)
# =============================================================
AZUL    = '#1565C0'
LARANJA = '#E65100'
VERDE   = '#2E7D32'

fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle(
    'MoveData | AlphaTransit Intelligence – Cidade Alpha\n'
    'Análise de Atraso e Congestionamento das Viagens (Maio 2026)',
    fontsize=14, fontweight='bold', y=1.01
)

# Gráfico 1: Atraso médio por dia
ax1 = axes[0, 0]
ax1.plot(df_dia['DIA'], df_dia['ATRASO_MEDIO'], marker='o',
         color=LARANJA, linewidth=2.2, markersize=6, label='Atraso médio (min)')
media_geral = df['qt_atraso_min'].mean()
ax1.axhline(media_geral, color='red', linestyle='--', linewidth=1.2,
            label=f'Média geral: {media_geral:.1f} min')
ax1.fill_between(df_dia['DIA'], df_dia['ATRASO_MEDIO'], alpha=0.15, color=LARANJA)
ax1.set_title('Atraso Médio por Dia (maio/2026)', fontweight='bold')
ax1.set_xlabel('Dia do mês')
ax1.set_ylabel('Atraso médio (minutos)')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xticks(df_dia['DIA'])

# Gráfico 2: Scatter congestionamento x atraso com linha de tendência
ax2 = axes[0, 1]
scatter = ax2.scatter(
    df['qt_nivel_congestionamento_pct'],
    df['qt_atraso_min'],
    c=df['qt_velocidade_media_kmh'],
    cmap='RdYlGn_r', alpha=0.65, s=45, edgecolors='none'
)
cbar = plt.colorbar(scatter, ax=ax2)
cbar.set_label('Velocidade média (km/h)', fontsize=9)
z = np.polyfit(df['qt_nivel_congestionamento_pct'], df['qt_atraso_min'], 1)
xs = np.linspace(df['qt_nivel_congestionamento_pct'].min(),
                 df['qt_nivel_congestionamento_pct'].max(), 100)
ax2.plot(xs, np.poly1d(z)(xs), 'r--', linewidth=2, label='Tendência')
r_corr = float(np.corrcoef(df['qt_nivel_congestionamento_pct'], df['qt_atraso_min'])[0,1])
ax2.set_title('Congestionamento vs Atraso por Viagem', fontweight='bold')
ax2.set_xlabel('Congestionamento (%)')
ax2.set_ylabel('Atraso (minutos)')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.text(0.04, 0.93, f'r = {r_corr:.3f}', transform=ax2.transAxes,
         fontsize=10, color='darkred', fontweight='bold')

# Gráfico 3: Pizza de desempenho (RN04)
ax3 = axes[1, 0]
cores_pizza = [VERDE, '#F9A825', LARANJA]
wedges, texts, autotexts = ax3.pie(
    desemp_count.values,
    labels=desemp_count.index,
    autopct='%1.1f%%',
    colors=cores_pizza[:len(desemp_count)],
    startangle=90,
    textprops={'fontsize': 9}
)
for at in autotexts:
    at.set_fontweight('bold')
ax3.set_title('Classificação de Desempenho das Viagens (RN04)', fontweight='bold')

# Gráfico 4: Atraso médio por hora do dia
ax4 = axes[1, 1]
df_hora_valido = df_hora[df_hora['QTD'] >= 3]
bars = ax4.bar(df_hora_valido['HORA'], df_hora_valido['ATRASO_MEDIO'],
               color=[LARANJA if v > 0 else VERDE for v in df_hora_valido['ATRASO_MEDIO']],
               edgecolor='white', width=0.7)
ax4.axhline(0, color='black', linewidth=0.8)
ax4.set_title('Atraso Médio por Faixa de Horário', fontweight='bold')
ax4.set_xlabel('Hora do dia')
ax4.set_ylabel('Atraso médio (minutos)')
ax4.set_xticks(df_hora_valido['HORA'])
ax4.set_xticklabels([f'{h}h' for h in df_hora_valido['HORA']], fontsize=8)
ax4.grid(True, axis='y', alpha=0.3)
ax4.legend(handles=[
    mpatches.Patch(color=LARANJA, label='Atrasado'),
    mpatches.Patch(color=VERDE,   label='Adiantado / No horário')
], fontsize=8)

plt.tight_layout()
plt.savefig('MoveData_grafico_atraso_congestionamento.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[11] Gráfico salvo: MoveData_grafico_atraso_congestionamento.png")

# =============================================================
# 5. PREPARAR JSON PARA NOSQL (Redis key-value)
# =============================================================
resultado_json = []

for _, row in df_dia.iterrows():
    resultado_json.append({
        "tipo":                      "atraso_por_dia",
        "dia":                       int(row['DIA']),
        "mes_ano":                   "2026-05",
        "qtd_viagens":               int(row['QTD_VIAGENS']),
        "atraso_medio_min":          float(row['ATRASO_MEDIO']),
        "congestionamento_medio_pct": float(row['CONGESTIONAMENTO_MEDIO']),
        "velocidade_media_kmh":      float(row['VELOCIDADE_MEDIA']),
        "pct_viagens_atrasadas":     float(row['PCT_ATRASADAS']),
    })

for _, row in df_linha.head(5).iterrows():
    resultado_json.append({
        "tipo":                      "ranking_linha_atraso",
        "nm_linha":                  str(row['nm_linha']),
        "qtd_viagens":               int(row['QTD']),
        "atraso_medio_min":          round(float(row['ATRASO_MEDIO']), 2),
        "congestionamento_medio_pct": round(float(row['CONGESTIONAMENTO_MEDIO']), 2),
    })

with open('MoveData_resultado_atraso.json', 'w', encoding='utf-8') as f:
    json.dump(resultado_json, f, ensure_ascii=False, indent=2)

print("[12] JSON salvo: MoveData_resultado_atraso.json")

# =============================================================
# 6. INSIGHTS FINAIS
# =============================================================
pct_atrasadas = (df['qt_atraso_min'] > 0).mean() * 100
pior_dia      = df_dia.loc[df_dia['ATRASO_MEDIO'].idxmax()]
pior_linha    = df_linha.iloc[0]

print("\n" + "=" * 65)
print("INSIGHTS — MoveData | AlphaTransit Intelligence")
print("=" * 65)
print(f"\n  → {pct_atrasadas:.1f}% das viagens concluídas chegaram atrasadas.")
print(f"  → Atraso médio geral: {media_geral:.1f} minutos por viagem.")
print(f"  → Correlação atraso × congestionamento: {r_corr:.3f}")
print(f"  → Dia mais crítico: dia {int(pior_dia['DIA'])} "
      f"— atraso médio {pior_dia['ATRASO_MEDIO']:.1f} min "
      f"| cong. {pior_dia['CONGESTIONAMENTO_MEDIO']:.1f}%.")
print(f"  → Linha mais atrasada: {pior_linha['nm_linha']} "
      f"({pior_linha['ATRASO_MEDIO']:.1f} min de atraso médio).")
print("\n  RECOMENDAÇÕES PARA A GESTÃO PÚBLICA (Cidade Alpha):")
print("  1. Reforçar frota nas linhas com maior atraso recorrente.")
print("  2. Investigar trechos com congestionamento >60% e criar")
print("     corredores exclusivos de ônibus.")
print("  3. Priorizar alertas para a Persona Ana em horários de pico.")
print("  4. Alimentar camada Gold do Databricks com esses indicadores")
print("     para monitoramento contínuo via dashboard.")
