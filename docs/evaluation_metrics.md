# Métricas de Avaliação

Documentação técnica das métricas utilizadas para avaliar detectores de mudança de regime em sinais ECG streaming (250 Hz).

## Introdução

Este documento descreve **com rigor** as métricas realmente implementadas na pipeline e como são calculadas. A avaliação considera três dimensões:

- **Acurácia de detecção**: TP, FP, FN
- **Rapidez da detecção**: Latência (segundos)
- **Robustez operacional**: Penalidades de custo (NAB)

## Fontes de Verdade no Código

As implementações canônicas estão em:

- **`src/evaluation.py`**
  - `calculate_comprehensive_metrics()` — Cálculo de métricas por registo
  - `latency_weighted_f1()` — F1/F3 ponderados por latência
  - `calculate_nab_score()` — NAB (Numenta Anomaly Benchmark)

- **`src/evaluate_predictions.py`**
  - Aplica `calculate_comprehensive_metrics()` para cada registo
  - Agrega resultados por combinação de parâmetros
  - Gera CSVs e relatórios finais

---

## 1. Definições de Matching (TP, FP, FN, TN)

O matching é baseado em **eventos em streaming**: cada mudança real (ground truth) pode ser associada a no máximo uma detecção válida dentro da janela temporal de aceitação.

### True Positive (TP)

Uma detecção é TP quando **simultaneamente**:

1. Ocorre **após o início** do evento real
2. Ocorre **dentro da janela de aceitação** $\tau$ (típicamente 10 segundos)
3. O evento real **ainda não foi associado** a uma detecção anterior

**Nota**: Cada evento real pode ter no máximo um TP.

### False Positive (FP)

Uma detecção é FP quando:

- Não encontra evento real elegível para matching na janela; **OU**
- É uma detecção extra que não é aproveitada pelo matching (regra: máximo 1 TP por evento)

### False Negative (FN)

Um evento real é FN quando:

- Não recebe nenhuma detecção válida dentro da janela de aceitação

### True Negative (TN)

**Não é utilizado como métrica central neste problema.**

- Em problemas de detecção de eventos em streaming, TN não tem significado bem definido (quantos "não-eventos" há?)
- A função NAB internamente fixa $TN = 0$ e não o inclui no cálculo final
- Todas as comparações e rankings usam apenas TP, FP, FN

---

## 2. Métricas Clássicas (sem ponderação temporal)

### Precisão Clássica

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

**Interpretação**: Fração de detecções que correspondem a eventos reais.

**Alcance**: [0, 1]
- 1.0 = nenhum falso positivo
- 0.0 = todas as detecções são falsas

### Recall Clássico

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

**Interpretação**: Fração de eventos reais que foram detectados.

**Alcance**: [0, 1]
- 1.0 = todos os eventos foram detectados
- 0.0 = nenhum evento foi detectado

### F1-Score Clássico

$$
F1 = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
$$

**Interpretação**: Média harmônica de precision e recall. Equilibra ambas as métricas igualmente.

**Alcance**: [0, 1]

### F3-Score Clássico (β = 3)

$$
F_\beta = \frac{(1 + \beta^2) \times \text{Precision} \times \text{Recall}}{\beta^2 \times \text{Precision} + \text{Recall}}
$$

Para $\beta = 3$:

$$
F3 = \frac{10 \times \text{Precision} \times \text{Recall}}{9 \times \text{Precision} + \text{Recall}}
$$

**Interpretação**: Dá **3 vezes mais peso** ao Recall que à Precision.

**Justificativa**: Em detecção de regime, não perder um evento (recall alto) é mais crítico que minimizar falsos positivos.

**Alcance**: [0, 1]

---

## 3. Métricas Ponderadas por Latência

A detecção precoce é mais valiosa que a tardia. Aplicamos ponderação temporal $w(\delta)$ onde $\delta$ é a latência de detecção.

### Função de Peso Temporal

$$
w(\delta) = \begin{cases}
1.0 & \text{se } \delta \leq \text{plateau} \\
1 - \frac{\delta - \text{plateau}}{\tau - \text{plateau}} & \text{se } \text{plateau} < \delta \leq \tau \\
0.0 & \text{se } \delta > \tau \text{ ou } \delta < 0
\end{cases}
$$

**Parâmetros típicos**:
- **Plateau**: 4 segundos (detecção rápida = peso máximo)
- **τ (tau)**: 10 segundos (limite de aceitação)

**Interpretação**:
- $\delta \in [0, 4s]$: peso = 1.0 (perfeito)
- $\delta \in (4, 10]$: peso decai linearmente de 1.0 a 0.0
- $\delta > 10s$: peso = 0.0 (rejeitado)

### Precision Ponderada ($\text{Precision}^*$)

$$
\text{Precision}^* = \frac{\sum_{TP} w(\delta_{TP})}{\sum_{TP} w(\delta_{TP}) + FP}
$$

**Interpretação**: TP com latência alta contam menos; todos os FP contam como 1.

### Recall Ponderado ($\text{Recall}^*$)

$$
\text{Recall}^* = \frac{\sum_{TP} w(\delta_{TP})}{TP + FN}
$$

**Interpretação**: TP com latência alta contam menos; FN sempre conta como 1.

### F1-Weighted ($F1^*$)

$$
F1^* = 2 \cdot \frac{\text{Precision}^* \times \text{Recall}^*}{\text{Precision}^* + \text{Recall}^*}
$$

### F3-Weighted ($F3^*$) — **Métrica Primária**

$$
F3^* = \frac{10 \times \text{Precision}^* \times \text{Recall}^*}{9 \times \text{Precision}^* + \text{Recall}^*}
$$

**Importância**:
- Esta é a **métrica primária de otimização** do projeto
- Enfatiza recall (não perder eventos) com sensibilidade temporal
- Recompensa detecções rápidas implicitamente via ponderação

---

## 4. Métricas Temporais Derivadas

Calculadas em `src/evaluation.py` como derivações simples de recall/precision.

### Recall@τs e Precision@τs

Recálculos de Recall e Precision com janelas de aceitação específicas:

- **recall_4s**, **precision_4s**: $\tau = 4$ segundos
- **recall_10s**, **precision_10s**: $\tau = 10$ segundos

**Interpretação**: Mostra robustez em diferentes tolerâncias de latência.

### Expected Detection Delay (EDD)

Apenas para **True Positives**:

$$
\text{EDD}_{\text{median}} = \text{mediana}(\delta_{TP})
$$

$$
\text{EDD}_{p95} = \text{percentil 95}(\delta_{TP})
$$

**Interpretação**:
- $\text{EDD}_{\text{median}}$: latência típica de detecção
- $\text{EDD}_{p95}$: latência no pior caso (5% das detecções são mais lentas)

**Unidade**: Segundos

### False Positives per Minute

$$
\text{FP/min} = FP \times \frac{60}{\text{duration\_seconds}}
$$

**Interpretação**: Taxa operacional de alarmes falsos.

**Unidade**: Falsos positivos por minuto de sinal

---

## 5. NAB (Numenta Anomaly Benchmark)

Sistema de scoring que simula **custos operacionais reais** de detecção.

### Princípios

- Cada TP, FP, FN tem um **custo definido** pelo perfil
- A **posição temporal** de uma detecção dentro da janela afeta o score
  - Detecção rápida (logo após evento): prêmio maior
  - Detecção tardia (perto do limite): prêmio menor
- Resultado final é a **soma ponderada** de ganhos (TP) e perdas (FP, FN)

### Três Perfis NAB

#### 1. NAB Standard (Balanceado)

| Componente | Custo |
|-----------|-------|
| TP | +1.0 (ganho) |
| FP | −0.11 (penalidade) |
| FN | −1.0 (penalidade) |

**Interpretação**: Equilibra custo de FP e FN. Típico para cenários genéricos.

#### 2. NAB Low FP (Minimizar Alarmes Falsos)

| Componente | Custo |
|-----------|-------|
| TP | +1.0 (ganho) |
| FP | −1.0 (penalidade ALTA) |
| FN | −0.22 (penalidade) |

**Interpretação**: Para cenários com **operadores humanos** que sofrem fadiga de alarme. Falsos positivos são custosos.

#### 3. NAB Low FN (Minimizar Eventos Perdidos)

| Componente | Custo |
|-----------|-------|
| TP | +1.0 (ganho) |
| FP | −0.22 (penalidade) |
| FN | −1.0 (penalidade ALTA) |

**Interpretação**: Para cenários **críticos** onde não perder um evento é essencial. Falsos negativos são custosos.

### Cálculo Detalhado

Para cada TP, o score final é multiplicado por uma **função sigmoide** que depende da **posição relativa** da detecção na janela:

$$
s_{\text{TP}} = \text{sigmoid}\left(\frac{\delta - \tau/2}{\tau/4}\right)
$$

- Detecção no meio da janela: $s = 0.5$ (prêmio reduzido a 50%)
- Detecção rápida: $s \to 1.0$ (prêmio máximo)
- Detecção tardia: $s \to 0.0$ (prêmio mínimo)

**Score Final**:

$$
\text{NAB} = \sum_{\text{TP}} s_{\text{TP}} - (\#\text{FP} \times c_{\text{FP}}) - (\#\text{FN} \times c_{\text{FN}})
$$

### Interpretação Prática

- **Quanto maior, melhor**
- Pode ser **negativo** quando penalidades superam ganhos (comum em dados ruidosos)
- Em comparações, **usar ranking relativo**, não valor absoluto
- Exemplo: -4.0 vs -3.0 → o segundo é melhor (menos negativo)

---

## 6. Análise Macro: Robustez Cross-Dataset

Além das métricas por-sinal, a pipeline avalia **robustez global** combinando múltiplos datasets e detectores.

### Opção 1: Performance Ceiling (Melhor Performance Local)

**Pergunta**: "Qual é o melhor performance possível de cada detector quando otimizado por dataset?"

**Método**:
- Para cada detector×dataset, seleciona a melhor configuração (cross-fold F3)
- Agrega usando macro-average (média simples entre datasets)
- Calcula estatísticas de dispersão (CV, min, max)

**Artefatos**: `cross_dataset_generalization_option1.{csv,md}`

**Interpretação**:
- **Alto F3 (~0.40)**: Detector tem grande potencial com tuning adequado (ex: FLOSS)
- **Baixo F3 (~0.15)**: Detector tem limitações fundamentais
- **CV alto (>50%)**: Performance varia muito entre datasets (menos portável)
- **CV baixo (<30%)**: Detector generaliza bem

### Opção 2: Parameter Portability (Transferibilidade)

**Pergunta**: "Posso usar os parâmetros ótimos de um dataset noutro sem re-tuning?"

**Método**:
- Para cada detector, testa Leave-One-Dataset-Out:
  - Toma melhor config de dataset A
  - Aplica em dataset B (sem retuning)
  - Compara F3 transferido vs F3 local ótimo
  - Calcula razão: (F3_transferido / F3_local) × 100%

**Artefatos**: `parameter_portability_option2.{csv,md}`

**Interpretação**:
- **>95% retention**: Parâmetros completamente portáveis (ex: ADWIN 94.90%)
- **85-95% retention**: Razoável (pequeno re-tuning recomendado)
- **75-85% retention**: Significativo drop (tuning obrigatório)
- **<75% retention**: Não usar sem re-tuning (ex: FLOSS -24%)

### Opção 3: Unified Robustness Score (Combinado)

**Pergunta**: "Qual detector é universalmente robusto em ambas dimensões?"

**Fórmula**:
$$\text{Score} = 0.6 \times (1 - \text{intra_dataset_gap}) + 0.4 \times (1 - \text{inter_dataset_variance})$$

- **Intra-dataset gap**: Diferença entre intra-fold e cross-fold F3 (overfitting)
- **Inter-dataset variance**: CV de portability entre datasets

**Artefatos**: `unified_robustness_option3.{csv,md}`

**Interpretação**: Detectors com score >0.97 são robustos em ambas dimensões (ex: FLOSS, ADWIN, KSWIN)

---

## 7. Comparação de Métricas

### Resumo Visual

| Métrica | Foco | Ponderação | Primária? |
|---------|------|-----------|----------|
| **F1 Classic** | Equilibro | Não | ❌ |
| **F3 Classic** | Recall | Não | ❌ |
| **F1 Weighted** | Equilibro + Latência | Sim | ❌ |
| **F3 Weighted** | Recall + Latência | Sim | ✅ **SIM** |
| **NAB Standard** | Custo operacional | Sigmoide | Complementar |
| **NAB Low FP** | Custo operacional (FP alto) | Sigmoide | Complementar |
| **NAB Low FN** | Custo operacional (FN alto) | Sigmoide | Complementar |

### Quando Usar Cada Uma

**F3-Weighted** (primária):
- Avaliação global e ranking final de detectores
- Otimização de hiperparâmetros
- Publicações e comparações
- Métrica de agregação nas análises cross-dataset (Opções 1-3)

**NAB Standard**:
- Validação do F3-weighted
- Quando se quer penalizar FP significativamente

**NAB Low FP**:
- Cenários com operadores humanos (fadiga de alarme)
- Contextos onde alarmes falsos são muito custosos

**NAB Low FN**:
- Cenários críticos (exemplo: emergências)
- Máxima segurança (não perder eventos)

**Recall@10s**:
- KPI simples: "que fração de eventos foram detectados?"
- Fácil comunicação com stakeholders

**EDD (Mediano)**:
- Speediness: "qual é a latência típica?"
- Requisitos de tempo real

---

## 8. Cálculo Passo a Passo (Exemplo)

Suponha um sinal com 1 evento real em t=100s:

**Cenário 1: Detecção Rápida**
- Evento real: t = 100s
- Detecção: t = 102s (latência = 2s)
- Resultado:
  - TP = 1, FP = 0, FN = 0
  - $w(2s) = 1.0$ (no plateau)
  - $\text{Recall} = 1/1 = 1.0$, $\text{Precision} = 1/1 = 1.0$
  - $F3 = 1.0$ ✅
  - $\text{EDD} = 2s$ ✅

**Cenário 2: Detecção Tardia**
- Evento real: t = 100s
- Detecção: t = 108s (latência = 8s)
- Resultado:
  - TP = 1, FP = 0, FN = 0
  - $w(8s) = 1 - (8-4)/(10-4) = 0.333$
  - $\text{Recall}^* = 0.333/1 = 0.333$, $\text{Precision}^* = 0.333/1 = 0.333$
  - $F3^* = 0.333$ ⚠️ (penalizado)
  - $\text{EDD} = 8s$

**Cenário 3: Falso Positivo**
- Evento real: nenhum
- Detecção: t = 50s
- Resultado:
  - TP = 0, FP = 1, FN = 0
  - $\text{Recall} = 0$, $\text{Precision} = 0$ (0/1)
  - $F3 = 0$ (não detectou nada)
  - $\text{FP/min}$ = contribuição a 1 alarme falso

---

## 9. Localização dos Artefatos

### Por Detector e Dataset

Métricas calculadas para **cada combinação de parâmetros**:

```
results/<dataset>/<detector>/
├── metrics_comprehensive_with_nab.csv      # Todos os valores calculados
└── final_report_with_nab.json              # Resumo e configuração ótima
```

**Colunas do CSV**:
- Colunas de parâmetro (ex: delta, ma_window, min_gap_samples)
- f1_classic, f1_weighted, f3_classic, **f3_weighted**
- recall_4s, recall_10s, precision_4s, precision_10s
- edd_median_s, edd_p95_s, fp_per_min
- nab_score_standard, nab_score_low_fp, nab_score_low_fn

### Comparação Entre Detectores

Por dataset:

```
comparisons/<dataset>/
├── comparative_report.md             # Análise textual comparativa
├── detector_rankings.csv             # Ranking por F3-weighted
├── detector_summary.csv             # Sumário agregado de métricas
├── constraint_tradeoffs.csv         # Análise de trade-offs (Recall vs FP/min)
└── robustness.csv                   # Robustez entre configurações
```

### Cross-Dataset (Macro-Averages)

Agregações entre datasets:

```
results/cross_dataset_analysis/
├── cross_dataset_generalization_option1.{csv,md}  # Opção 1: performance ceiling
├── parameter_portability_option2.{csv,md}         # Opção 2: transferibilidade
├── unified_robustness_option3.{csv,md}            # Opção 3: score unificado
├── option123_summary.png                          # Visualização das 3 opções
├── README.md                                      # Resumo das análises
└── <detector>/
    └── README.md                                  # Resumo por detector
```

---

## 10. Notas Importantes

### Tratamento de Casos Especiais

1. **Divisão por zero** em Precision/Recall
   - Se TP = FP = 0: Precision = indefinido → considerado 1.0
   - Se TP = FN = 0: Recall = indefinido → considerado 1.0

2. **NaN em métricas NAB**
   - Alguns modelos podem gerar NaN em EDD se não houver TPs
   - Estes modelos são mantidos nos CSVs como NaN (indicam falha de detecção)

3. **Agregação de métricas**
   - Média ou mediana sobre registos? **Média** é o padrão
   - Desvio padrão é mantido para análise de variabilidade

### Evitar Confusão com Terminologia

- **"Métrica primária"** = F3-weighted (usada para ranking)
- **"Complementar"** = NAB (validação de F3)
- **"KPI"** = Recall@10s, FP/min (comunicação com stakeholders)

### Por Que Não Usar DDM/EDDM?

Excluídos porque:
- São inadequados para **séries temporais contínuas em streaming** de ECG neste contexto
- Não se adaptam bem à **detecção de mudanças de regime** com avaliação temporal/latência
- A pipeline atual prioriza detectores validados neste domínio (adwin, page_hinkley, kswin, hddm_a, hddm_w, floss)

---

## Referências Código

Para implementação completa, consulte:
- [src/evaluation.py](../src/evaluation.py)
- [src/evaluate_predictions.py](../src/evaluate_predictions.py)
