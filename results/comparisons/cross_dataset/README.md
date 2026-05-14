# Cross-Dataset Analysis: 3 Opções de Avaliação

**Last Updated:** 2026-05-14


**Última Atualização**: 2026-05-14
**Status**: Visualizações concluídas; usar `comparisons/<dataset>/` para rankings canônicos.

---

## 🎯 Objetivo

Avaliar **robustez** de detectores através de múltiplos datasets, respondendo 3 perguntas:

1. **Opção 1**: Qual detector atinge melhor performance (quando otimizado)?
2. **Opção 2**: Qual detector generaliza melhor entre datasets (portabilidade)?
3. **Opção 3**: Qual detector é globalmente robusto (combinação das duas)?

---

## 📊 As 3 Opções (Perspetivas)

### 🎯 **Opção 1: Performance Ceiling (Cross-Dataset Generalization)**

**Pergunta**: "Qual é a melhor performance que cada detector consegue atingir (tunado por dataset)?"

**Métrica**: F3-weighted máximo (cross-fold)
- Macro-average de melhores configs por dataset
- Representa o "ceiling" - máximo potencial

**Ranking**:
```
1. FLOSS        F3 = 0.4306 ± 0.13 (CV=30.7%)
2. KSWIN        F3 = 0.3203 ± 0.11 (CV=33.8%)
3. Page-Hinkley F3 = 0.3152 ± 0.08 (CV=26.5%)
4. HDDM_A       F3 = 0.3022 ± 0.07 (CV=24.4%)
5. ADWIN        F3 = 0.2890 ± 0.12 (CV=41.0%)
6. HDDM_W       F3 = 0.1534 ± 0.20 (CV=128.1%)
```

**Interpretação**:
- FLOSS é ~49.0% melhor que ADWIN quando tunado
- Mas requer tuning específico por dataset
- Não é portável (vê Opção 2)

**Use Case**: Research, quando tem labels para tuning

**Ficheiros**:
- `option1_ceiling_analysis.png`
- Dados: [`../../cross_dataset_analysis/cross_dataset_generalization_option1.csv`](../../cross_dataset_analysis/cross_dataset_generalization_option1.csv)
- Report: [`../../cross_dataset_analysis/cross_dataset_generalization_option1.md`](../../cross_dataset_analysis/cross_dataset_generalization_option1.md)

---

### 🚀 **Opção 2: Parameter Portability (Leave-One-Dataset-Out)**

**Pergunta**: "Consigo usar hiperparâmetros de um dataset noutro sem re-tuning?"

**Métrica**: Transferability ratio
```
ratio = (F3_transferred / F3_local_best) × 100%
```
- Testa: melhores params de dataset A → dataset B
- 34 transfers testadas (5 detectores × 6 transfers + Page-Hinkley com 4 transfers disponíveis)

**Ranking**:
```
1. ADWIN        Transferability = 95.07% (melhor generalização)
2. KSWIN        Transferability = 87.75%
3. FLOSS        Transferability = 75.83% ← perde ~24.17% ao transferir
4. HDDM_A       Transferability = 64.99%
5. Page-Hinkley Transferability = 54.32%
6. HDDM_W       Transferability = 45.76%
```

**Interpretação**:
- ADWIN é a melhor escolha para **produção sem labels**
- FLOSS é excelente quando tunado, mas não se generaliza bem
- KSWIN é o sweet spot (88% portabilidade)

**Use Case**: Produção com novo dataset SEM labels

**Ficheiros**:
- `option2_portability_heatmap.png`
- Dados: [`../../cross_dataset_analysis/parameter_portability_option2.csv`](../../cross_dataset_analysis/parameter_portability_option2.csv)
- Report: [`../../cross_dataset_analysis/parameter_portability_option2.md`](../../cross_dataset_analysis/parameter_portability_option2.md)

---

### ⚖️ **Opção 3: Unified Robustness Score (Combinação)**

**Pergunta**: "Qual detector é universalmente robusto (ceiling + portabilidade)?"

**Fórmula**:
```
Score = 0.6×(1 - 2-fold gap) + 0.4×(1 - transfer_variance)
         └─ Performance ─┘              └─ Portabilidade ─┘
```
- Pesa 60% consistência intra-dataset medida pelo gap two-fold
- Pesa 40% estabilidade da portabilidade entre datasets

**Ranking**:
```
1. FLOSS       Score = 0.9761 (melhor globalmente)
2. ADWIN       Score = 0.9710 (segundo lugar)
3. KSWIN       Score = 0.9690 (sweet spot)
4. HDDM_A      Score = 0.9507
5. HDDM_W      Score = 0.9425
6. Page-Hinkley Score = 0.9047
```

**Interpretação**:
- FLOSS lidera mesmo com penalidade de transferabilidade
- ADWIN é muito perto (bom compromisso)
- KSWIN é o sweet spot (performance + portabilidade balanceados)

**Use Case**: Escolha holística para maioria dos cenários

**Ficheiros**:
- `option3_unified_score_ranking.png`
- Dados: [`../../cross_dataset_analysis/unified_robustness_option3.csv`](../../cross_dataset_analysis/unified_robustness_option3.csv)
- Report: [`../../cross_dataset_analysis/unified_robustness_option3.md`](../../cross_dataset_analysis/unified_robustness_option3.md)

---

## 📋 Matriz de Decisão: Qual Detector Usar?

### Árvore de Decisão

```
NOVO DATASET?
│
├─ COM LABELS para tuning?
│  │
│  └─ SIM: Usar FLOSS
│     └─ F3 esperado: 0.43 (ceiling atual)
│     └─ Esforço: Grid search (~horas)
│
└─ SEM LABELS (produção imediata)?
   │
   ├─ Precisa máxima portabilidade?
   │  └─ ADWIN
   │     └─ Transferability média: 95.07%
   │
   └─ Balanced (melhor aposta geral)?
      └─ KSWIN
         └─ Ceiling=0.3203, transferability=87.75%
```

### Tabela Comparativa

| Cenário | Detector | Razão | Performance | Transferability |
|---------|----------|-------|---|---|
| **Max Performance** | FLOSS | Maior ceiling atual | 🥇 0.4306 | 75.83% |
| **No Tuning** | ADWIN | Maior portabilidade média | 0.2890 | 🥇 95.07% |
| **Balanced** | KSWIN | Sweet spot | 0.3203 | 87.75% |
| **Holistic** | FLOSS | Score unificado mais alto | 0.4306 | 75.83% |

---

## 📁 Ficheiros Disponíveis

### Visualizações disponíveis
- `option1_ceiling_analysis.png` - Bar chart com CV
- `option2_portability_heatmap.png` - Heatmap 3 datasets × 6 detectores
- `option3_unified_score_ranking.png` - Bar chart ranqueado
- `production_decision_matrix.png` - Matriz visual de decisão

Observação: `option123_summary.png` está em `results/cross_dataset_analysis/option123_summary.png`.

### Dados (CSVs + Markdown)
- Opção 1: [`../../cross_dataset_analysis/cross_dataset_generalization_option1.*`](../../cross_dataset_analysis/)
- Opção 2: [`../../cross_dataset_analysis/parameter_portability_option2.*`](../../cross_dataset_analysis/)
- Opção 3: [`../../cross_dataset_analysis/unified_robustness_option3.*`](../../cross_dataset_analysis/)

---

## 🔍 Como Navegar

### Se quer: Resumo rápido
→ Ver `results/cross_dataset_analysis/option123_summary.png`

### Se quer: Detalhes de um aspeto
- Performance máxima? → Opção 1 + `option1_ceiling_analysis.png`
- Portabilidade? → Opção 2 + `option2_portability_heatmap.png`
- Score holístico? → Opção 3 + `option3_unified_score_ranking.png`

### Se quer: Decisão prática
→ Ver `production_decision_matrix.png` + tabela acima

### Se quer: Dados numéricos
→ Ver CSVs em `../../cross_dataset_analysis/`

---

## 📊 Visualizações (Referência de geração)

```
FASE 2: Geração de Visualizações
├── option1_ceiling_analysis.png
│   └── Script: visualize_cross_dataset_summary.py
│   └── Plot: Bar chart (6 detectores, com CV error bars)
│
├── option2_portability_heatmap.png
│   └── Script: visualize_cross_dataset_summary.py
│   └── Plot: Heatmap 3×6 (datasets × detectores, cores = transferability %)
│
├── option3_unified_score_ranking.png
│   └── Script: visualize_cross_dataset_summary.py
│   └── Plot: Bar chart (6 detectores, com score unificado)
│
├── production_decision_matrix.png
│   └── Script: visualize_cross_dataset_summary.py
│   └── Plot: Bubble chart ou decision tree visual
│
Nota: o resumo conjunto (`option123_summary.png`) não é salvo nesta pasta.
```

---

## 🎓 Referências Relacionadas

- **Relatórios Detalhados**: [`../../cross_dataset_analysis/`](../../cross_dataset_analysis/)
- **Por Dataset**: [`../by_dataset/`](../by_dataset/)
- **Documentação de Métricas**: [`../../../docs/evaluation_metrics.md`](../../../docs/evaluation_metrics.md)
- **Guia Principal**: [`../README.md`](../README.md)

---

## 📝 Notas

1. **As 3 opções não são excludentes** - complementam-se para visão holística
2. **Opção 2 (ADWIN 95.07%) é superior para produção sem tuning**
3. **Opção 1 (FLOSS 0.4306) representa máximo potencial se tiver labels**
4. **Opção 3 (FLOSS score=0.97) é "sabedoria convencional" se não souber qual escolher**
5. Este diretório contém os PNGs históricos gerados para suporte visual.

---

**Última Atualização**: 2026-05-14
**Status**: ✅ Visualizações presentes; ✅ documentação ajustada para consistência
