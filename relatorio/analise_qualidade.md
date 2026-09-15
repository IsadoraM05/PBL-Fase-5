# MoveData — PBL Fase 5

## Análise de qualidade e completude do projeto

**Data:** 15/09/2026 · **Escopo:** diagnóstico, sem alteração de código
**Base comparativa:** `Exercício_Guiado_PBL_Fase_5_Entregáveis.pdf`, `FIAP ON FASE 5 … CAPÍTULO 1 PBL EXERCÍCIO GUIADO 1TSCO 2026 v1.docx`, `Template_Entregas_Fase_5_v1.docx`, `Hipoteses.docx` e `_MoveData_ENTREGA_PBL_FASE_5_.docx`

> **Onde estavam os documentos:** não existe pasta `docs/` no projeto. O enunciado, o template e o `Hipoteses.docx` estão em `C:\Users\soare\Downloads` (`PBL - Cap 01.zip`, `Docs-20260915T220554Z-1-001.zip`, `Hipoteses.docx`). Foram lidos a partir de uma cópia temporária; nada foi copiado para dentro do projeto.

---

## 1. O que foi verificado

| Frente | Como foi verificado |
|---|---|
| Enunciado x entrega | Leitura integral dos 3 documentos da disciplina + `Hipoteses.docx` + documento de entrega do grupo |
| Código | Leitura dos 8 arquivos de `notebooks/fase_5/` e das 18 células do notebook + análise estática (imports/variáveis) |
| Execução | Scripts rodados a partir de dois diretórios diferentes; dashboard executado via `streamlit.testing` com e sem filtro |
| Dados | ~40 verificações no Excel além das já feitas pelo `Preparacao_Qualidade_Dados.py` |
| Estatística | Recálculo das 6 hipóteses + IC, post-hoc, correlação parcial, tamanho de efeito e análise de poder |

---

## 2. Comparação com o enunciado

O enunciado pede 4 entregas. Situação atual:

| Entrega | Exigência | Situação |
|---|---|---|
| 1ª — Mapa da missão | Grupo, componentes, RMs, desafio | ✅ Completa (no `.docx`: MoveData, 5 componentes com RM) |
| 2ª — Preparação e qualidade | Excel com dados **e dicionário de dados** + código `.py`/`.ipynb` | ⚠️ Presente, mas o dicionário tem nomes de coluna errados (M15) e a checagem de qualidade tem lacunas (M17–M20) |
| 3ª — Análise estatística | Código com estatística descritiva, **amostragem**, testes de hipóteses, correlação | ⚠️ Descritiva, testes e correlação ✅ · **amostragem ausente** (M21) |
| 4ª — Dashboard + recomendações | Streamlit/Looker para os níveis operacional, tático e estratégico | ⚠️ Existe e roda, mas com problemas de interpretação e usabilidade (M6–M14) |

**Ponto a favor:** o enunciado enfatiza que "nem todas as hipóteses levantadas são necessariamente confirmadas pelos dados" — o projeto tem 2 hipóteses não confirmadas (H3 e H4) tratadas corretamente no código. Isso está alinhado ao espírito da atividade e deve ser **destacado** no PDF, não escondido.

**Técnicas listadas no enunciado e não utilizadas:** amostragem, limites/derivadas, integrais. As duas últimas não fazem sentido para estes dados — não recomendo forçar. Amostragem faz sentido e é barata de incluir (ver seção 6).

---

## 3. Problemas CRÍTICOS

### C1 — Caminho relativo fixo quebra a execução fora da raiz do projeto
**Arquivos:** `notebooks/fase_5/Analise_Estatistica_H1.py:13`, `H2:13`, `H3:13`, `H4:13`, `H5:13`, `H6:13`, `Dashboard.py:143` · células 2, 5, 7, 9, 11, 13, 15 do notebook

Todos usam `caminho = "dados/Dados PBL fase 5.xlsx"`, que só funciona se o processo for iniciado **na raiz** do projeto. Reproduzido:

```
$ cd notebooks/fase_5 && py Analise_Estatistica_H1.py
FileNotFoundError: [Errno 2] No such file or directory: 'dados/Dados PBL fase 5.xlsx'
```

Isso importa porque o enunciado orienta o avaliador a abrir a pasta dos arquivos no PyCharm e rodar de lá (`cd C:\comandos_python\` → `streamlit run …`). Agravantes:

- `Preparacao_Qualidade_Dados.py:6` **já usa o padrão correto** (`Path(__file__).resolve().parents[2] / "dados" / …`), mas a célula 2 do notebook usa a versão relativa — script e notebook divergem.
- A instrução da célula 16 do notebook (`streamlit run Dashboard.py` "a partir da pasta do projeto") não funciona em lugar nenhum: da raiz o arquivo não é encontrado (está em `notebooks/fase_5/`), e de dentro de `notebooks/fase_5/` o Excel não é encontrado.

**Sugestão:** replicar em todos os arquivos o padrão já usado no `Preparacao_Qualidade_Dados.py` e corrigir a instrução da célula 16 para `streamlit run notebooks/fase_5/Dashboard.py` (comando validado).

### C2 — O notebook entregue não tem nenhuma saída salva
**Arquivo:** `MoveData_PBL_Fase_5.ipynb` (células 2, 5, 7, 9, 11, 13, 15, 17)

Todas as células de código estão com `execution_count: None` e `outputs: []`, e o notebook não tem `kernelspec`/`language_info` no metadata. Quem abrir o arquivo vê **apenas código** — nenhum número, nenhum p-valor, nenhum gráfico. Como o notebook é o entregável das 2ª e 3ª entregas, o avaliador não consegue ver os resultados sem instalar tudo e reexecutar.

**Sugestão:** rodar tudo e salvar o notebook com as saídas (ou exportar também em HTML/PDF para anexar). Os PNGs em `relatorio/graficos/` ajudam, mas não substituem as saídas numéricas dentro do notebook.

### C3 — Não existe arquivo de dependências, e `scipy` não está na lista do exercício guiado
**Arquivos:** raiz do projeto (ausente) · comparar com `bibliotecaspython.txt` do exercício guiado

O exercício guiado entrega um `bibliotecaspython.txt` e manda o aluno rodar `pip install -r bibliotecaspython.txt`. O conteúdo dele é apenas:

```
streamlit
pandas
matplotlib
openpyxl
```

O projeto **não tem** arquivo equivalente, e as 6 hipóteses dependem de `scipy`, que não está nessa lista. Um avaliador que siga o roteiro do guiado instala as 4 bibliotecas e recebe `ModuleNotFoundError: No module named 'scipy'` já na primeira célula de hipótese.

**Sugestão:** criar `requirements.txt` (ou `bibliotecaspython.txt`, para espelhar o enunciado) com `pandas`, `numpy`, `scipy`, `matplotlib`, `streamlit`, `openpyxl`, e citá-lo no PDF de entrega.

---

## 4. Problemas MODERADOS

### 4.1 Estatística

**M1 — H4 imprime o título de H3** · `Analise_estatistica_H4.py:30` e célula 11
`print("\n=== H3 - CHUVA X OCUPAÇÃO ===")` — deveria ser H4. Aparece na saída que vai para o PDF.

**M2 — H2 não tem teste post-hoc** · `Analise_Estatistica_H2.py:103` e conclusão na linha 130
Kruskal-Wallis é um teste *omnibus*: diz que **pelo menos dois** períodos diferem, não **quais**. A conclusão escrita afirma que os picos têm atraso maior que entrepico e noturno, mas isso foi lido das médias, não testado. Verifiquei — a afirmação **se sustenta**, e o post-hoc deixaria isso formal:

| Par | p ajustado (Bonferroni) | Conclusão |
|---|---|---|
| Entrepico x Noturno | 1,3 × 10⁻⁵ | difere |
| Entrepico x Pico_Manha | 1,6 × 10⁻³² | difere |
| Entrepico x Pico_Tarde | 6,3 × 10⁻²⁶ | difere |
| Noturno x Pico_Manha | 9,5 × 10⁻⁴⁵ | difere |
| Noturno x Pico_Tarde | 1,0 × 10⁻³⁷ | difere |
| Pico_Manha x Pico_Tarde | 1,000 | **não difere** |

Tamanho de efeito ε² = 0,159 (efeito médio). **Sugestão:** acrescentar Mann-Whitney par a par com correção de Bonferroni (≈10 linhas, sem mexer no teste principal) e o ε².

**M3 — "atraso médio" x o que o Kruskal-Wallis mede** · `Analise_Estatistica_H2.py:130-142`
O texto fala em média; Kruskal-Wallis compara distribuições (postos/medianas). Não invalida nada, mas um avaliador atento pode cobrar. **Sugestão:** escrever "diferença na distribuição do atraso" e apresentar média e mediana juntas (já estão calculadas na linha 35).

**M4 — H5 é a única hipótese sem bloco de conclusão** · `Analise_Estatistica_H5.py` (termina na linha 148, após o gráfico)
H3, H4 e H6 imprimem "rejeitamos/não rejeitamos H0"; H1 imprime a decisão; H5 termina no gráfico da regressão, sem declarar a decisão sobre H0. Quebra o padrão do notebook. **Sugestão:** fechar com o mesmo bloco das outras.

**M5 — H5 tem confundimento não discutido** · `Analise_Estatistica_H5.py:97-120`
Ocupação e congestionamento estão correlacionados (r = 0,454), e **congestionamento também explica o consumo** (r = 0,588 — quase o mesmo que ocupação, 0,597). Controlando congestionamento, a correlação de H5 cai de **0,5975 para 0,4585**. A relação continua existindo, mas atribuir todo o consumo à ocupação superestima o efeito.
**Sugestão:** acrescentar um parágrafo de limitação (ou uma correlação parcial de 3 linhas). Vale a mesma observação em H1: controlando "é pico", r cai de 0,5633 para 0,4416.

**M6 — Preparação afirma que não há inconsistências** · `Preparacao_Qualidade_Dados.py:252`
"Não foram identificadas inconsistências que exigissem exclusão ou correção de registros." As verificações feitas de fato passaram, mas há inconsistências reais não testadas (M8, M9, M10). A frase, como está, é forte demais. **Sugestão:** delimitar ("dentro das verificações aplicadas…") ou ampliar as checagens.

**M7 — Verificações de qualidade ausentes** · `Preparacao_Qualidade_Dados.py`
Não há: checagem de valores negativos na base de **eventos** (só viagens, linhas 74-96); checagem de duplicidade de **chave** (`id_viagem`, `id_evento` — só `duplicated()` de linha inteira, linhas 57 e 60); nenhuma análise de outliers; nenhum `describe()` geral. Verifiquei os dois primeiros: não há duplicidade de chave nem negativo indevido nos eventos — mas a evidência não está no código entregue.

### 4.2 Qualidade dos dados (achados novos)

**M8 — As duas abas não se reconciliam** (nenhuma dessas checagens existe hoje)

| Coluna da aba `viagens` | Confronto com a aba `eventos` | Divergências |
|---|---|---|
| `qt_paradas` | nº de eventos da viagem | **0 / 2000** ✅ (é a única já verificada) |
| `tempo_medio_parada_min` | média de `tempo_parada_min` | **1429 / 2000** (viés sistemático de −0,10 min) |
| `ocupacao_media_pct` | média de `ocupacao_pct` | **1539 / 2000** (viés de −2,24 p.p.) |
| `ocupacao_maxima_pct` | máximo de `ocupacao_pct` | **1892 / 2000** (até ±21 p.p.) |
| `atraso_min` (viagem) | atraso do último evento | **1417 / 2000** (até ±5 min) |
| `qt_passageiros_embarcados` | soma de `embarques` | 20 / 2000 (até −13) |

Indica que as duas abas foram geradas de forma independente. **Não invalida H1–H6** (cada hipótese usa uma única aba), mas é exatamente o tipo de achado que valoriza a entrega de "qualidade de dados". **Sugestão:** incluir essas checagens no script e registrar como limitação conhecida da base.

**M9 — `velocidade_media_kmh` tem teto artificial em 55,0 km/h** · aba `viagens`
9 viagens têm exatamente 55,0 km/h, mas `distancia_km / (tempo_real_min/60)` daria de 55,7 a 76,8 km/h. Nenhum registro passa de 55. É um *clipping* na geração dos dados. Não afeta H1–H6 (a coluna não é usada), mas quebra se alguém a utilizar.

**M10 — 4,1% dos eventos têm horário que anda para trás** · aba `eventos`
1120 eventos (em 792 viagens) têm `hora_real` **anterior** à da parada anterior da mesma viagem — mediana de −1 min. Exemplo real (viagem 1, paradas 5 e 6): chega às 16:49 na parada 5 e às 16:48 na parada 6. Fisicamente impossível. Só 1 caso é cruzamento de meia-noite legítimo (viagem 1407, único evento com `data_evento ≠ data_viagem` — esse está correto).

**M11 — Dicionário de dados não bate com as colunas reais** · aba `dicionario_dados`

| No dicionário | Na base (real) |
|---|---|
| `qnt_passageiros_embarcados` | `qt_passageiros_embarcados` |
| `ocupacao_max_pct` | `ocupacao_maxima_pct` |
| `consumo_evergia_kwh` | `consumo_energia_kwh` |
| `data_evento `, `embarques `, `id_parada `, `qt_incidentes ` | (mesmo nome, com espaço sobrando no dicionário) |

Há ainda "ônibos" e "Pencentual" (2x) nas descrições. O dicionário é item explícito da 2ª entrega e aparece como print no documento do grupo.

### 4.3 Dashboard

**M12 — `eficiencia_kwh_km` é chamada de "Eficiência", mas é consumo** · `Dashboard.py:370` e `383`
O dicionário define a coluna como "quantidade de energia consumida por quilômetro" — quanto **maior**, **pior**. O gráfico "Ocupação x Eficiência energética" sobe da esquerda para a direita, o que um gestor lê como "mais ocupação = mais eficiência", exatamente o oposto. Os scripts de H5 usam o rótulo correto ("Consumo energético por km"); só o dashboard diverge. **Sugestão:** renomear para "Consumo (kWh/km)" no dashboard.

**M13 — Insight com número fixo, do teste errado, que não acompanha o filtro** · `Dashboard.py:511`
O card cita `r = 0,5633`, que é o **Pearson** calculado sobre a base inteira. Dois problemas: (a) H1 concluiu pelo **Spearman** (ρ = 0,5506), porque Shapiro-Wilk rejeitou normalidade — o dashboard exibe justamente a estatística que a análise descartou; (b) ao filtrar por "Noturno" os gráficos mudam, mas o número continua 0,5633.
**Sugestão:** ou calcular a correlação dinamicamente sobre o recorte filtrado, ou deixar explícito "base completa, Spearman ρ = 0,5506".

**M14 — H3 e H4 são exibidas sem dizer que não deram significativas** · `Dashboard.py:300-365`
Os gráficos "Chuva x Congestionamento" e "Chuva x Ocupação" aparecem sob o título "📈 Relações entre os indicadores", e nenhum dos 3 cards de insight menciona chuva. O dashboard **não afirma** textualmente algo falso — mas o enquadramento sugere relação onde não há (p = 0,79 e p = 0,31). Confirmei que a conclusão do grupo é robusta: mesmo restringindo às 594 viagens com chuva > 0, nada se torna significativo (p = 0,08 e p = 0,39), e comparando dias com/sem chuva também não (p = 0,05 e p = 0,63).
**Sugestão:** adicionar um 4º card "🌧️ Chuva: sem efeito detectado" com os números. Isso *valoriza* a entrega — o enunciado destaca hipóteses não confirmadas como resultado legítimo.

**M15 — Recomendação sem sustentação nos dados** · `Dashboard.py:563`
"Monitorar trechos com maior congestionamento, priorizando **regiões** onde o aumento do trânsito esteja associado a maiores atrasos" — não existe variável de trecho ou região na base, e nenhuma análise por localidade foi feita. Testei o que mais se aproxima (`id_linha`, 40 linhas): **não há diferença de atraso entre linhas** (Kruskal-Wallis H = 34,5; p = 0,68).
**Sugestão:** reescrever para algo que os dados sustentam, como "priorizar as viagens em faixas de congestionamento acima de 60%", ou assumir explicitamente que é uma recomendação de próximo passo, dependente de dado geográfico que a base ainda não tem.

**M16 — Apenas 3 dos 6 resultados viram insight** · `Dashboard.py:502-547`
Há cards para H1, H2 e H6. Faltam H5 (relação forte, r = 0,5975) e H3/H4 (ver M14).

**M17 — Sem cache: o Excel é relido a cada interação** · `Dashboard.py:146` e `151`
Medido com `streamlit.testing`: **4,3 s** na carga inicial e **3,0 s** a cada mudança de filtro, relendo 2.000 + 27.413 linhas. **Sugestão:** `@st.cache_data` numa função de carga — muda de ~3 s para instantâneo.

**M18 — Nenhum tratamento de erro** · `Dashboard.py:143-155` e os 6 scripts
Se o Excel não existir, estiver aberto no Excel (bloqueio de arquivo) ou faltar uma coluna, o usuário recebe um traceback cru de pandas. **Sugestão:** um `try/except` com `st.error("Base não encontrada em …")` no dashboard e uma verificação das colunas esperadas.

**M19 — Um único filtro** · `Dashboard.py:176`
Só "Período". A base oferece dimensões úteis e já prontas: `dia_semana`, `id_linha` (40), `data_viagem` (01/01 a 31/08/2026), `status_viagem`, faixa de chuva. Para atender "operacional, tático e estratégico" como pede o enunciado, 2 ou 3 filtros extras ajudam bastante. Ressalva honesta: nos dados atuais `dia_semana` (3,02 a 3,99 min) e `id_linha` (p = 0,68) quase não variam — os filtros servem para exploração, não vão revelar padrão novo.

**M20 — Cinco blocos de gráfico praticamente idênticos** · `Dashboard.py:266-444`
O mesmo bloco de ~28 linhas (figura, scatter, labels, grid, spines, `tight_layout`, `st.pyplot`, `close`) repetido 5 vezes, mudando só as colunas e os rótulos. **Sugestão:** extrair `grafico_dispersao(x, y, rotulo_x, rotulo_y)` — o arquivo cai de 578 para ~420 linhas.

**M21 — Gráfico que ignora o filtro, sem avisar** · `Dashboard.py:459`
"Atraso médio por período" usa `df_viagens_base` (base completa) de propósito — o que é correto, senão o gráfico vira uma barra só. Mas o usuário filtra "Noturno", vê os KPIs mudarem e esse gráfico não. **Sugestão:** uma legenda "(todos os períodos, para comparação)".

### 4.4 Estrutura e reprodutibilidade

**M22 — Cada célula relê o Excel do zero** · células 2, 5, 7, 9, 11, 13 e 15 (12 chamadas de `read_excel`)
O enunciado descreve a 3ª entrega como "a partir dos dados refinados no 1º desafio", e o exercício guiado gera um arquivo ajustado (`cidade_alfa_consumo_agua_ajustado.xlsx`) que alimenta o dashboard. No projeto não há base ajustada: cada hipótese recarrega o arquivo bruto. É defensável (os dados já estavam limpos), mas convém dizer isso explicitamente no PDF.

**M23 — `tick_labels` exige matplotlib ≥ 3.9** · `Analise_Estatistica_H2.py:79`
`plt.boxplot(dados_boxplot, tick_labels=…)` — o parâmetro se chamava `labels` até a 3.8. Em ambiente com matplotlib mais antigo (comum no PyCharm de quem não atualizou), a célula de H2 quebra.

**M24 — Notebook sem os enunciados formais de H0/H1 e sem conclusão final**
As células markdown 4, 8, 10, 12 e 14 têm só o título da hipótese. O `Hipoteses.docx` tem H0/H1 formalizados para as 6 — esse conteúdo não está no notebook, e a 3ª entrega é justamente "testes de hipóteses". Também não há seção de conclusões/recomendações ao final (o notebook termina na célula do dashboard).

**M25 — Documento de entrega com texto do modelo não removido** · `_MoveData_ENTREGA_PBL_FASE_5_.docx`, 4ª entrega
Ficaram no documento: "Para essa entrega, também temos como exemplo o arquivo analisecorrelacao.py…" e "Figura 6: Código fonte utilizado para gerar o dashboard de correlação entre a temperatura e o consumo de **água** na cidade Alfa" — texto do exercício guiado de água, que não tem relação com o projeto de mobilidade. Há também um "F" solto logo após a seção de estatísticas. Como o PDF sai desse arquivo, isso vai para o avaliador.

---

## 5. Problemas MENORES

| # | Problema | Onde |
|---|---|---|
| m1 | `import numpy as np` sem uso | H1:3, H2:3, H3:3, H4:3 |
| m2 | `chi2_contingency` importado e nunca usado (resíduo da versão antiga de H2) | H3:4 |
| m3 | `from pathlib import Path` sem uso | H5:2, H6:2 |
| m4 | `linregress` importado e não usado | H6:5 |
| m5 | `df_eventos` é carregado (27.413 linhas) só para imprimir `.shape` | H1:21, H3:21, H4:21, H5:21 |
| m6 | `eventos_por_viagem` calculado duas vezes, idêntico | `Preparacao_Qualidade_Dados.py:206` e `213` |
| m7 | "Cidade **Alpha**" / "ALPHA TRANSIT" no dashboard x "Cidade **Alfa**" no notebook, no enunciado e nos dados | `Dashboard.py:126` e `132` |
| m8 | Nome do desafio divergente: "A cidade Alfa e a mobilidade" (docx) x "Monitor Inteligente de Transporte Público" (notebook, célula 0) | docx x notebook |
| m9 | Arquivo fora do padrão de nome: `Analise_estatistica_H4.py` (minúsculo) entre `Analise_Estatistica_H*.py` | `notebooks/fase_5/` |
| m10 | `use_container_width` foi depreciado no Streamlit (pedir `width='stretch'`) — 5 ocorrências, ainda funciona | `Dashboard.py:297, 330, 365, 398, 444, 491` |
| m11 | CSS com cores claras fixas (`background: white`, texto `#123B4A`) — títulos de seção ficam com contraste ruim se o avaliador usar o tema escuro do Streamlit | `Dashboard.py:13-116` |
| m12 | `Hipoteses.docx` H4 cita a variável `ocupação_pct` (nome que existe na aba de **eventos**); o código usa `ocupacao_media_pct` (viagens) — a escolha do código está certa, o documento é que precisa alinhar | docx x H4 |
| m13 | `Hipoteses.docx` H6 enuncia "maior **ocupação** está relacionada a maior tempo de parada", mas as variáveis declaradas e o código usam embarques + desembarques (movimentação) | docx x H6 |
| m14 | Scripts imprimem "P-valor: < 0.001" e escondem o valor exato (H5: 7,6 × 10⁻¹⁹⁴; H2: 5,9 × 10⁻⁶⁹) | H2:107, H3:57, H4:59, H5:74, H6:76 |
| m15 | H1 calcula e imprime Pearson (linha 63) **antes** de testar normalidade (linha 78), que é o teste que justifica usar Spearman — ordem didaticamente invertida | `Analise_Estatistica_H1.py:63-95` |
| m16 | Shapiro-Wilk com n = 2000 rejeita normalidade por desvios mínimos; a decisão por Spearman está certa, mas convém justificar pelo formato da distribuição, não só pelo p-valor | H1:78-79, H2:55 |
| m17 | A categoria "Noturno" inclui viagens das 05h (além de 20h–22h) — coerente, mas merece nota no dicionário | aba `viagens` |
| m18 | `satisfacao_media` e `qt_incidentes` nunca são usadas em nenhuma análise | base de dados |

---

## 6. Técnicas estatísticas que agregariam valor

Só listo o que usa os dados que já existem e responde às hipóteses que o grupo já levantou — sem hipótese nova artificial. Todos os números abaixo foram calculados sobre a base real.

### 6.1 Amostragem — a única técnica do enunciado que está faltando (recomendo incluir)
É citada duas vezes no enunciado ("Criar amostras de dados", "Amostragem") e não aparece em lugar nenhum do projeto. Com 2.000 viagens dá para demonstrar em ~15 linhas: amostra aleatória simples de n = 300 e amostra estratificada por `periodo`, comparando média/desvio da amostra com os da população. É a melhoria de **melhor custo-benefício** para a nota.

### 6.2 Intervalos de confiança (complementam, não substituem, os testes)
Já calculados, prontos para usar:

| Hipótese | Estimativa | IC 95% |
|---|---|---|
| H1 (Spearman) | ρ = 0,5506 | [0,5193 · 0,5805] |
| H3 (Spearman) | ρ = −0,0382 | [−0,0819 · 0,0056] → **contém zero** |
| H4 (Spearman) | ρ = −0,0146 | [−0,0584 · 0,0293] → **contém zero** |
| H5 (Pearson) | r = 0,5975 | [0,5686 · 0,6250] |

Atraso médio por período (IC 95% pela t): Pico_Tarde [5,41 · 6,40] · Pico_Manha [5,40 · 6,22] · Entrepico [2,03 · 2,68] · Noturno [0,61 · 1,44]. Os intervalos dos dois picos se sobrepõem e os demais não — é a leitura visual do post-hoc do M2.

### 6.3 Análise de poder — transforma "não deu significativo" em conclusão forte
Com n = 2.000 e poder de 80%, o estudo detectaria qualquer correlação a partir de **|r| ≈ 0,063**. Como H3 e H4 ficaram em −0,038 e −0,015, dá para afirmar com segurança: *não é falta de amostra; se existe efeito da chuva, ele é menor que 0,06 e irrelevante na prática*. Isso responde à crítica óbvia de "sua amostra era pequena".

### 6.4 Teste de outliers
O enunciado cita `describe()` como forma de identificar valores extremos, e hoje não há nenhuma análise de outliers. Pela regra do IQR (1,5×):

| Coluna | Outliers | Observação |
|---|---|---|
| `chuva_mm` | 307 | **falso positivo** — 70,3% dos valores são zero, o que colapsa o IQR; a regra não se aplica a variável com excesso de zeros |
| `atraso_pct` | 113 (15 extremos) | derivada, consistente com atrasos grandes em viagens curtas |
| `velocidade_media_kmh` | 48 | ver M9 (teto em 55) |
| `qt_passageiros_embarcados` | 39 | plausível |
| `distancia_km`, `congestionamento_pct`, `ocupacao_media_pct`, `consumo_energia_kwh` | 0 | limpos |

Vale mais pela **discussão** (mostrar que o grupo sabe quando a regra do IQR não vale) do que por remover registros — não recomendo remover nada.

### 6.5 Duas análises que os dados sustentam e o grupo não explorou

**(a) Chuva x Atraso — o desdobramento natural de H3.** O próprio `Hipoteses.docx` diz que H3 é "relacionada à hipótese 1". A chuva não mexe no congestionamento (H3, p = 0,79), mas tem associação **significativa com o atraso**:

- Pearson r = 0,1475 · p = 3,4 × 10⁻¹¹
- Atraso médio sem chuva: 3,12 min · com chuva: 4,28 min (Mann-Whitney p = 1,6 × 10⁻⁵)

Ou seja: chove → o ônibus atrasa ~1,2 min a mais, mas **não** por congestionamento (provavelmente embarque mais lento). É um resultado bom, fecha o raciocínio de H3 e não exige hipótese nova.

**(b) Satisfação x Atraso.** `satisfacao_media` está na base e nunca foi usada: r = −0,358 (p = 1,6 × 10⁻⁶¹) com o atraso. Conecta a análise técnica ao impacto no cidadão — material forte para a seção de recomendações à gestão pública.

### 6.6 Tamanho de efeito
Nenhum teste reporta tamanho de efeito. Acrescentar ε² no Kruskal-Wallis (= 0,159) e o R² já existente em H5 (0,357) é barato e demonstra rigor.

---

## 7. Prioridade sugerida para o grupo

| Ordem | Item | Esforço | Por quê |
|---|---|---|---|
| 1 | **C2** — salvar o notebook com as saídas | 5 min | O avaliador não vê resultado nenhum hoje |
| 2 | **C3** — criar `requirements.txt` com scipy | 5 min | Sem isso o projeto não roda seguindo o roteiro do enunciado |
| 3 | **C1** — corrigir os caminhos (copiar o padrão do `Preparacao`) | 20 min | Quebra ao rodar de outra pasta |
| 4 | **M25** — limpar o texto do modelo no docx de entrega | 10 min | Texto de "consumo de água" no PDF final |
| 5 | **M1** — título "H3" dentro de H4 | 1 min | Erro visível na saída |
| 6 | **M12 / M13 / M14** — "Eficiência"→"Consumo", insight de H1 e card de chuva | 30 min | São afirmações que os dados não sustentam como estão |
| 7 | **6.1** — amostragem | 30 min | Única técnica do enunciado ainda ausente |
| 8 | **M2 / 6.2 / 6.3** — post-hoc, IC e poder | 1 h | Transformam H2, H3 e H4 em conclusões defensáveis |
| 9 | **M11** — corrigir o dicionário de dados | 15 min | Item explícito da 2ª entrega |
| 10 | **M8 / M9 / M10** — registrar as inconsistências de dados | 45 min | Vira ponto forte da entrega de qualidade |
| 11 | **M15 / M19 / M17 / M20** — dashboard: recomendação, filtros, cache, refatoração | 2 h | Usabilidade e código |
| 12 | Menores (m1–m18) | 30 min | Cosmético |

**Nada precisa ser refeito.** As 6 hipóteses estão com o teste correto para o tipo de variável, e as duas conclusões negativas (H3 e H4) resistiram a todas as verificações alternativas que apliquei. O que falta é blindagem: reprodutibilidade (C1–C3), coerência entre o que o dashboard diz e o que os testes mostraram (M12–M15), e duas ou três técnicas a mais para cobrir o que o enunciado pede.
