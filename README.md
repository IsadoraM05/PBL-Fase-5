# MoveData — PBL Fase 5 (Inteligência Analítica, Estatística e Tomada de Decisão)

Análise de dados das viagens de ônibus autônomos da **cidade Alfa** (dataset fictício,
criado para o exercício), desenvolvida para o desafio **"Monitor Inteligente de Transporte
Público"**.

O projeto percorre o caminho completo de um trabalho de Data Intelligence: preparação e
verificação da qualidade dos dados, análise estatística com teste de 6 hipóteses de negócio
e, por fim, um dashboard interativo em Streamlit com recomendações para a gestão pública.

A base tem duas tabelas: **2.000 viagens** (28 colunas) e **27.413 eventos de parada**
(12 colunas), cobrindo o período de janeiro a agosto de 2026.

## Grupo

**MoveData**

- Gabriel Soares
- Isadora Maciel
- João Boone
- Juliana Larissa Napoli
- Quéren Matos

## Estrutura do projeto

```
.
├── dados/
│   └── Dados PBL fase 5.xlsx        # base de viagens, eventos de parada e dicionário de dados
├── notebooks/
│   ├── fase_4/                      # entregas da fase anterior (análise em Python e Redis/NoSQL)
│   └── fase_5/
│       ├── Preparacao_Qualidade_Dados.py
│       ├── Analise_Estatistica_H1.py ... H6.py
│       └── Dashboard.py             # dashboard Streamlit
├── relatorio/
│   ├── resumo_hipoteses.md          # resultado de cada hipótese, com teste e conclusão
│   ├── analise_qualidade.md         # revisão de qualidade e completude do projeto
│   └── graficos/                    # gráficos das 6 hipóteses em PNG
├── MoveData_PBL_Fase_5.ipynb        # notebook com todo o código e as saídas
└── requirements.txt
```

## Hipóteses testadas

| # | Hipótese | Teste | Resultado |
|---|---|---|---|
| H1 | Maior congestionamento está associado a maior atraso | Spearman (ρ = 0,5506; p < 0,001) | ✅ **Confirmada** |
| H2 | Viagens em horário de pico têm maior atraso médio | Kruskal-Wallis (H = 319,5291; p < 0,001) + post-hoc de Dunn | ✅ **Confirmada** |
| H3 | A chuva está associada a maior congestionamento | Pearson / Spearman (ρ = −0,0382; p = 0,0874) | ❌ **Não confirmada** |
| H4 | A chuva está associada a maior ocupação dos ônibus | Pearson / Spearman (ρ = −0,0146; p = 0,5151) | ❌ **Não confirmada** |
| H5 | Maior ocupação está associada a maior consumo energético por km | Pearson / Spearman / Regressão (r = 0,5975; R² = 0,3570) | ✅ **Confirmada** |
| H6 | Maior movimentação de passageiros aumenta o tempo de parada | Pearson / Spearman (r = 0,3680; p < 0,001) | ✅ **Confirmada** |

Nível de significância adotado: α = 0,05. Os detalhes de cada teste — estatísticas
descritivas, verificação de normalidade, p-valores e conclusões — estão em
[`relatorio/resumo_hipoteses.md`](relatorio/resumo_hipoteses.md).

Vale destacar H3 e H4: nem toda hipótese levantada pelo negócio se confirma nos dados. A
chuva **não** apresentou associação significativa nem com o congestionamento nem com a
ocupação, e isso é um resultado legítimo da investigação.

## Como rodar

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Análise estatística

Rodar os scripts individualmente, a partir da raiz do projeto:

```bash
python notebooks/fase_5/Preparacao_Qualidade_Dados.py
python notebooks/fase_5/Analise_Estatistica_H1.py
python notebooks/fase_5/Analise_Estatistica_H2.py
python notebooks/fase_5/Analise_Estatistica_H3.py
python notebooks/fase_5/Analise_estatistica_H4.py
python notebooks/fase_5/Analise_Estatistica_H5.py
python notebooks/fase_5/Analise_Estatistica_H6.py
```

Os scripts localizam a base sozinhos, então também funcionam se o terminal estiver dentro
de `notebooks/fase_5/`. Cada um salva seu gráfico em `relatorio/graficos/`.

Como alternativa, abra o notebook **`MoveData_PBL_Fase_5.ipynb`**, que reúne todo o código
em sequência e já vem com as saídas e os gráficos salvos.

### 3. Dashboard (Streamlit)

Use um dos comandos abaixo, dependendo de onde está o terminal:

- Da raiz do projeto: `streamlit run notebooks/fase_5/Dashboard.py`
- De dentro de `notebooks/fase_5/`: `streamlit run Dashboard.py`

O dashboard abre no navegador em `http://localhost:8501` e traz os indicadores principais,
os gráficos das relações analisadas, um filtro por período do dia e as recomendações para a
gestão pública.

---

Projeto acadêmico — FIAP, Fase 5 do PBL. Os dados são fictícios e foram gerados apenas para
fins didáticos.
