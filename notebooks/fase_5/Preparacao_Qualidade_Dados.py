
import pandas as pd
from pathlib import Path

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