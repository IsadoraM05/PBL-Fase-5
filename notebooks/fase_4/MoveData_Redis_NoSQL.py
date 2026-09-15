"""
=============================================================
MoveData | AlphaTransit Intelligence | Cidade Alpha
FASE 4 – ENTREGÁVEL 3: Armazenamento em SGBD NoSQL (Redis)

Versão: redis-py 8.0.1 | Redis Server 8.4+

NOTAS DE COMPATIBILIDADE (redis-py 8.0 - mai/2026):
  - Protocolo RESP3 ativo por padrão (mantemos compatibilidade)
  - socket_timeout e socket_connect_timeout agora default = 5s
  - TCP keepalive ativado por padrão
  - max_connections=100 nos pools (novo padrão)
  - HMSET removido definitivamente — usar HSET com mapping={}

Alinhamento com fases anteriores:
  - Fase 2 (4ª entrega NoSQL): banco key-value para GPS e sessão
  - Fase 3 (arquitetura): dados chegam Bronze → Silver → Gold;
    Redis persiste os indicadores Gold para acesso em tempo real

Estrutura de chaves:
  movedata:atraso:dia:{dia}          → indicadores por dia (SET)
  movedata:linha:ranking_atraso      → ranking das linhas (LIST)
  movedata:resumo:geral              → KPIs resumidos (HASH)
=============================================================
"""

import json
import redis  # pip install "redis>=8.0"

print(f"redis-py versão: {redis.__version__}")

# =============================================================
# CONEXÃO COM O REDIS (redis-py 8.0)
# - RESP3 ativo por padrão (protocol=3 internamente)
# - socket_timeout=5s por padrão (novo comportamento 8.0)
# - decode_responses=True para receber str em vez de bytes
# =============================================================
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True,
    # socket_timeout e socket_connect_timeout agora default 5s no 8.0
    # TCP keepalive ativado por padrão no 8.0
)

# =============================================================
# CARREGAR JSON DA ETAPA DE ANÁLISE EXPLORATÓRIA
# =============================================================
with open('MoveData_resultado_atraso.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print("=" * 65)
print("MoveData | PERSISTÊNCIA REDIS 8.x – FASE GOLD DO DATABRICKS")
print("=" * 65)

# =============================================================
# 1. PERSISTIR: indicadores por dia (key-value com SET)
# =============================================================
dias = [d for d in dados if d['tipo'] == 'atraso_por_dia']
for item in dias:
    chave = f"movedata:atraso:dia:{item['dia']:02d}_2026_05"
    r.set(chave, json.dumps(item, ensure_ascii=False))
    print(f"  SET {chave}")

# =============================================================
# 2. PERSISTIR: ranking das linhas mais atrasadas (LIST)
# =============================================================
r.delete("movedata:linha:ranking_atraso")
linhas = [d for d in dados if d['tipo'] == 'ranking_linha_atraso']
for item in linhas:
    r.rpush("movedata:linha:ranking_atraso", json.dumps(item, ensure_ascii=False))
print(f"\n  RPUSH movedata:linha:ranking_atraso ({len(linhas)} linhas)")

# =============================================================
# 3. PERSISTIR: KPIs gerais — HSET com mapping= (redis-py 8.0)
#    ATENÇÃO: HMSET foi removido no redis-py 4.0+
#    Sintaxe correta: r.hset(name, mapping={...})
# =============================================================
atraso_medios = [d['atraso_medio_min'] for d in dias]
pcts          = [d['pct_viagens_atrasadas'] for d in dias]

kpis = {
    "periodo":                  "Maio 2026",
    "total_viagens_analisadas": str(sum(d['qtd_viagens'] for d in dias)),
    "atraso_medio_geral_min":   str(round(sum(atraso_medios) / len(atraso_medios), 2)),
    "pct_viagens_atrasadas":    str(round(sum(pcts) / len(pcts), 1)),
    "pior_dia":                 str(max(dias, key=lambda x: x['atraso_medio_min'])['dia']),
    "melhor_dia":               str(min(dias, key=lambda x: x['atraso_medio_min'])['dia']),
    "linha_mais_atrasada":      linhas[0]['nm_linha'] if linhas else "N/D",
    "fonte":                    "AlphaTransit Intelligence – camada Gold Databricks",
}

# redis-py 8.0: HSET com mapping= é a forma correta
# (HMSET foi descontinuado desde redis-py 4.0, removido no 5.0+)
r.hset("movedata:resumo:geral", mapping=kpis)
print("\n  HSET movedata:resumo:geral (mapping={})")

# =============================================================
# VERIFICAÇÃO DOS DADOS PERSISTIDOS
# =============================================================
print("\n" + "=" * 65)
print("VERIFICAÇÃO – DADOS PERSISTIDOS NO REDIS 8.x")
print("=" * 65)

print("\n  [1] Resumo geral (HGETALL):")
resumo = r.hgetall("movedata:resumo:geral")
for k, v in resumo.items():
    print(f"      {k}: {v}")

print("\n  [2] Indicador do dia 06 (GET):")
val = r.get("movedata:atraso:dia:06_2026_05")
if val:
    d = json.loads(val)
    print(f"      Atraso médio:          {d['atraso_medio_min']} min")
    print(f"      Congestionamento:      {d['congestionamento_medio_pct']}%")
    print(f"      % Viagens atrasadas:   {d['pct_viagens_atrasadas']}%")

print("\n  [3] Linha mais atrasada (LINDEX ranking 0):")
first = r.lindex("movedata:linha:ranking_atraso", 0)
if first:
    linha = json.loads(first)
    print(f"      Linha:         {linha['nm_linha']}")
    print(f"      Atraso médio:  {linha['atraso_medio_min']} min")
    print(f"      Congestionamento: {linha['congestionamento_medio_pct']}%")

print("\n  [OK] Todos os dados persistidos com sucesso no Redis 8.x!")
print("       Prontos para consumo em tempo real pelo AlphaTransit.")
