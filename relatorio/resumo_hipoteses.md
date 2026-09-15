# MoveData — PBL Fase 5

## Resumo das hipóteses (H1 a H6)

Documento gerado a partir da **execução real** do notebook `MoveData_PBL_Fase_5.ipynb`
(todas as células, exceto a célula do Dashboard Streamlit).

- **Base de viagens** (`viagens_onibus_autonomos_cidade`): 2.000 registros × 28 colunas
- **Base de eventos de parada** (`eventos_parada_cidade_alfa`): 27.413 registros × 12 colunas
- **Nível de significância adotado:** α = 0,05
- **Gráficos:** `relatorio/graficos/`

---

## H1 — Congestionamento x Atraso

| Item | Valor |
|---|---|
| Variáveis | `congestionamento_pct` (numérica) x `atraso_min` (numérica) |
| Teste de normalidade | Shapiro-Wilk: congestionamento p = 0,000000 / atraso p = 0,000000 → **nenhuma das duas é normal** |
| Teste principal | Correlação de **Spearman** (não paramétrico) |
| Resultado | ρ = **0,5506** · p-valor = **0,000000** (< 0,001) |
| Correlação de Pearson (referência) | r = 0,5633 |
| Decisão | **Rejeitamos H0** |
| Gráfico | `H1_congestionamento_atraso.png` |

Descritivas: congestionamento médio 43,42% (dp 22,98; min 0; máx 95);
atraso médio 3,47 min (dp 4,95; min −8; máx 22).

**Conclusão em linguagem simples:** existe uma associação positiva e estatisticamente
significativa, de força moderada, entre congestionamento e atraso. Quanto mais congestionada
a via, maior tende a ser o atraso da viagem. O congestionamento explica parte importante do
atraso, mas não tudo — há outros fatores envolvidos.

---

## H2 — Período do dia x Atraso médio

| Item | Valor |
|---|---|
| Variáveis | `periodo` (categórica, 4 grupos) x `atraso_min` (numérica) |
| Teste de normalidade | Shapiro-Wilk por grupo: Entrepico p = 0,000235 · Pico_Tarde p = 0,057456 · Pico_Manha p = 0,053039 · Noturno p = 0,001328 → **ao menos um grupo não é normal** |
| Teste principal | **Kruskal-Wallis** (não paramétrico, alternativa à ANOVA) |
| Resultado | H = **319,5291** · p-valor **< 0,001** |
| Decisão | **Rejeitamos H0** |
| Gráfico | `H2_periodo_atraso.png` (boxplot) |

Atraso médio por período (min):

| Período | Média | Mediana | Desvio-padrão | N |
|---|---|---|---|---|
| Pico_Tarde | 5,90 | 6,0 | 4,53 | 323 |
| Pico_Manha | 5,81 | 6,0 | 4,56 | 472 |
| Entrepico | 2,35 | 2,0 | 4,61 | 790 |
| Noturno | 1,02 | 1,0 | 4,33 | 415 |

### Teste post-hoc (Dunn com correção de Bonferroni)

O Kruskal-Wallis é um teste *omnibus*: indica que pelo menos dois períodos diferem, mas não
diz quais. O post-hoc de Dunn compara todos os pares, com os p-valores ajustados por
Bonferroni para as 6 comparações. Matriz de p-valores ajustados, como saiu na execução:

```
            Entrepico   Noturno  Pico_Manha  Pico_Tarde
Entrepico    1.000000  0.000036         0.0         0.0
Noturno      0.000036  1.000000         0.0         0.0
Pico_Manha   0.000000  0.000000         1.0         1.0
Pico_Tarde   0.000000  0.000000         1.0         1.0
```

| Par | p ajustado | Resultado |
|---|---|---|
| Entrepico x Noturno | 0,000036 | diferença significativa |
| Entrepico x Pico_Manha | 0,000000 | diferença significativa |
| Entrepico x Pico_Tarde | 0,000000 | diferença significativa |
| Noturno x Pico_Manha | 0,000000 | diferença significativa |
| Noturno x Pico_Tarde | 0,000000 | diferença significativa |
| Pico_Manha x Pico_Tarde | 1,000000 | **sem** diferença significativa |

**5 dos 6 pares apresentam diferença estatisticamente significativa**, com exceção de
Pico_Manha x Pico_Tarde (p = 1,000000).

**Conclusão em linguagem simples:** o atraso muda de forma significativa conforme o período
do dia. Os horários de pico (manhã e tarde) concentram os maiores atrasos — cerca de 5,8 a
5,9 minutos em média — contra 2,4 minutos no entrepico e apenas 1,0 minuto no período
noturno. O post-hoc de Dunn confirma que manhã e tarde formam um único grupo de pico, com
atraso equivalente entre si, mas ambos diferem de entrepico e de noturno. Ou seja: não se
trata de um horário crítico isolado, e sim de duas janelas de pico com o mesmo patamar de
atraso. Isso sustenta a recomendação de reforço operacional nos horários de pico.

---

## H3 — Chuva x Congestionamento

| Item | Valor |
|---|---|
| Variáveis | `chuva_mm` (numérica) x `congestionamento_pct` (numérica) |
| Testes aplicados | Correlação de **Pearson** e de **Spearman** |
| Resultado (Pearson) | r = **−0,0059** · p-valor = **0,7905** |
| Resultado (Spearman) | ρ = **−0,0382** · p-valor = **0,0874** |
| Decisão | **Não rejeitamos H0** |
| Gráfico | `H3_chuva_congestionamento.png` |

Descritivas: chuva média 2,01 mm (mediana 0; máx 34,3 — a maioria das viagens ocorreu sem
chuva); congestionamento médio 43,42%.

**Conclusão em linguagem simples:** nesta base, a chuva **não** apresentou relação
estatisticamente significativa com o nível de congestionamento. As correlações ficaram
praticamente em zero (e até levemente negativas), e os p-valores acima de 0,05 indicam que
não há evidência para afirmar que chover aumenta o congestionamento. Vale registrar que mais
de metade das viagens teve chuva zero, o que limita o poder do teste.

---

## H4 — Chuva x Ocupação média

| Item | Valor |
|---|---|
| Variáveis | `chuva_mm` (numérica) x `ocupacao_media_pct` (numérica) |
| Testes aplicados | Correlação de **Pearson** e de **Spearman** |
| Resultado (Pearson) | r = **−0,0226** · p-valor = **0,3129** |
| Resultado (Spearman) | ρ = **−0,0146** · p-valor = **0,5151** |
| Decisão | **Não rejeitamos H0** |
| Gráfico | `H4_chuva_ocupacao.png` |

Descritivas: chuva média 2,01 mm; ocupação média 51,09% (dp 17,21; min 8; máx 98).

**Conclusão em linguagem simples:** não há evidência de que dias de chuva levem mais
passageiros para os ônibus. A correlação é praticamente nula e o p-valor bem acima de 0,05.
A hipótese de que a chuva empurra a demanda para o transporte público não se confirmou nesta
base.

---

## H5 — Ocupação média x Consumo energético por km

| Item | Valor |
|---|---|
| Variáveis | `ocupacao_media_pct` (numérica) x `eficiencia_kwh_km` (numérica) |
| Testes aplicados | Correlação de **Pearson**, de **Spearman** e **regressão linear simples** |
| Resultado (Pearson) | r = **0,5975** · p-valor **< 0,001** |
| Resultado (Spearman) | ρ = **0,5745** · p-valor **< 0,001** |
| Regressão linear | intercepto = **1,1886** · coeficiente angular = **0,0058** · R² = **0,3570** · p-valor **< 0,001** |
| Decisão | **Rejeitamos H0** |
| Gráficos | `H5_ocupacao_consumo.png` (dispersão) e `H5_ocupacao_consumo_regressao.png` (com reta de regressão) |

Descritivas: ocupação média 51,09%; consumo médio 1,4862 kWh/km (dp 0,1678; min 0,95;
máx 2,05).

**Conclusão em linguagem simples:** quanto mais cheio o ônibus, maior o consumo de energia
por quilômetro — associação positiva, moderada e estatisticamente significativa. Pela
regressão, cada ponto percentual a mais de ocupação está associado a cerca de 0,0058 kWh/km
a mais de consumo (≈ 0,58 kWh/km a cada 100 pontos percentuais). A ocupação sozinha explica
aproximadamente 35,7% da variação do consumo (R² = 0,357), então há outros fatores relevantes
além do peso de passageiros.

### Conclusão (bloco impresso pelo script)

> Resultado: rejeitamos H0.
> Há evidências de associação positiva estatisticamente significativa entre a ocupação média
> e o consumo energético por km.
>
> A regressão linear indica que a ocupação sozinha explica 35.7% da variação do consumo
> energético por km (R² = 0.3570).
>
> Observação (limitação): a ocupação também é correlacionada com o congestionamento, que por
> sua vez também se associa ao consumo. Parte da relação observada pode, portanto, ser
> influenciada por esse terceiro fator.

**Limitação — possível confundimento:** a ocupação média não é independente do
congestionamento (r ≈ 0,45 nesta base), e o congestionamento também está associado ao
consumo energético. Isso significa que parte do efeito atribuído aqui à ocupação pode, na
verdade, vir do trânsito enfrentado na viagem. A associação continua existindo e é
significativa, mas seu tamanho deve ser lido com cautela: separar as duas contribuições
exigiria uma regressão múltipla ou uma correlação parcial, que não foram aplicadas neste
trabalho.

---

## H6 — Movimentação de passageiros x Tempo de parada

| Item | Valor |
|---|---|
| Variáveis | `movimentacao_passageiros` (= `embarques` + `desembarques`) x `tempo_parada_min` |
| Base | eventos de parada (27.413 registros) |
| Testes aplicados | Correlação de **Pearson** e de **Spearman** |
| Resultado (Pearson) | r = **0,3680** · p-valor **< 0,001** |
| Resultado (Spearman) | ρ = **0,3276** · p-valor **< 0,001** |
| Decisão | **Rejeitamos H0** |
| Gráfico | `H6_movimentacao_tempo_parada.png` |

Descritivas: movimentação média 10,34 passageiros por parada (mediana 7; máx 181);
tempo de parada médio 1,34 min (dp 0,41; min 0,35; máx 3,54).

**Conclusão em linguagem simples:** paradas com mais embarques e desembarques tendem a durar
mais — associação positiva, de força fraca a moderada, mas altamente significativa graças ao
grande volume de registros. A movimentação de passageiros explica parte do tempo de parada;
o restante vem de outros fatores (abertura de portas, acessibilidade, tráfego na parada etc.).

---

## Quadro-resumo

| Hipótese | Teste usado | Estatística | p-valor | Decisão (α = 0,05) |
|---|---|---|---|---|
| H1 — Congestionamento x Atraso | Spearman | ρ = 0,5506 | 0,000000 | Rejeita H0 — associação positiva |
| H2 — Período x Atraso médio | Kruskal-Wallis | H = 319,5291 | < 0,001 | Rejeita H0 — atraso maior nos picos |
| H3 — Chuva x Congestionamento | Pearson / Spearman | r = −0,0059 / ρ = −0,0382 | 0,7905 / 0,0874 | Não rejeita H0 — sem associação |
| H4 — Chuva x Ocupação | Pearson / Spearman | r = −0,0226 / ρ = −0,0146 | 0,3129 / 0,5151 | Não rejeita H0 — sem associação |
| H5 — Ocupação x Consumo/km | Pearson / Spearman / Regressão | r = 0,5975 / ρ = 0,5745 / R² = 0,3570 | < 0,001 | Rejeita H0 — associação positiva |
| H6 — Movimentação x Tempo de parada | Pearson / Spearman | r = 0,3680 / ρ = 0,3276 | < 0,001 | Rejeita H0 — associação positiva |

> **Notas da tabela:**
>
> - **H2** — além do Kruskal-Wallis, foi aplicado um **teste post-hoc de Dunn (Bonferroni)**,
>   que identifica quais pares de períodos diferem. Ver a subseção "Teste post-hoc" na
>   seção da H2.
> - **H5** — o resultado tem uma **limitação documentada** (possível confundimento com o
>   congestionamento). Ver a subseção "Limitação" na seção da H5.

### Observações sobre os p-valores

Os p-valores acima reproduzem exatamente o que o notebook imprimiu. Nos casos marcados
como `< 0,001`, os próprios scripts optam por exibir esse limite em vez do valor exato
(condição `if p < 0.001: print("P-valor: < 0.001")`), por isso o valor numérico completo
não consta aqui.
