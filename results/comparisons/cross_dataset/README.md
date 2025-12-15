# Cross-Dataset Analysis: 3 Opções de Avaliação

**Last Updated:** 2025-12-15 16:56:17 (✅ SUCCESS)


**Última Atualização**: 2025-12-15 (Fase 1 - Estrutura + Documentação)
**Próxima Fase**: Fase 2 - Geração de Visualizações

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
1. FLOSS       F3 = 0.4285 ± 0.13 (CV=31%)
2. KSWIN       F3 = 0.3176 ± 0.10 (CV=31%)
3. Page-Hinkley F3 = 0.3132 ± 0.07 (CV=22%)
4. HDDM_A      F3 = 0.2997 ± 0.15 (CV=50%)
5. ADWIN       F3 = 0.2879 ± 0.09 (CV=31%)
6. HDDM_W      F3 = 0.1527 ± 0.13 (CV=85%)
```

**Interpretação**:
- FLOSS é 48% melhor que ADWIN quando tunado
- Mas requer tuning específico por dataset
- Não é portável (vê Opção 2)

**Use Case**: Research, quando tem labels para tuning

**Ficheiros**:
- `option1_ceiling_analysis.png` (em preparação)
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
- 36 transfers testadas (6 detectores × 3 sources × 2 targets)

**Ranking**:
```
1. ADWIN       Transferability = 94.90% (melhor generalização)
2. KSWIN       Transferability = 87.84%
3. FLOSS       Transferability = 75.85% ← PERDE 24% ao transferir!
4. HDDM_A      Transferability = 65.17%
5. Page-Hinkley Transferability = 54.31%
6. HDDM_W      Transferability = 45.64%
```

**Interpretação**:
- ADWIN é a melhor escolha para **produção sem labels**
- FLOSS é excelente quando tunado, mas não se generaliza bem
- KSWIN é o sweet spot (88% portabilidade)

**Use Case**: Produção com novo dataset SEM labels

**Ficheiros**:
- `option2_portability_heatmap.png` (em preparação)
- Dados: [`../../cross_dataset_analysis/parameter_portability_option2.csv`](../../cross_dataset_analysis/parameter_portability_option2.csv)
- Report: [`../../cross_dataset_analysis/parameter_portability_option2.md`](../../cross_dataset_analysis/parameter_portability_option2.md)

---

### ⚖️ **Opção 3: Unified Robustness Score (Combinação)**

**Pergunta**: "Qual detector é universalmente robusto (ceiling + portabilidade)?"

**Fórmula**:
```
Score = 0.6×(1 - avg_ceiling_gap) + 0.4×(1 - transfer_variance)
         └─ Performance ─┘              └─ Portabilidade ─┘
```
- Pesa 60% ceiling (performance máxima)
- Pesa 40% portabilidade (generalização)

**Ranking**:
```
1. FLOSS       Score = 0.9763 (melhor globalmente)
2. ADWIN       Score = 0.9713 (segundo lugar)
3. KSWIN       Score = 0.9690 (sweet spot)
4. HDDM_A      Score = 0.9509
5. HDDM_W      Score = 0.9426
6. Page-Hinkley Score = 0.9049
```

**Interpretação**:
- FLOSS lidera mesmo com penalidade de transferabilidade
- ADWIN é muito perto (bom compromisso)
- KSWIN é o sweet spot (performance + portabilidade balanceados)

**Use Case**: Escolha holística para maioria dos cenários

**Ficheiros**:
- `option3_unified_score_ranking.png` (em preparação)
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
│     └─ F3 esperado: 0.42-0.43 (máximo)
│     └─ Esforço: Grid search (~horas)
│
└─ SEM LABELS (produção imediata)?
   │
   ├─ Precisa máximo recall? (clínica)
   │  └─ KSWIN + ma=50, min_gap=1000
   │     └─ Recall=99%, mas FP/min=9.4
   │
   ├─ Precisa mínimos alarmes? (alertas)
   │  └─ ADWIN + params default
   │     └─ Recall=60%, FP/min=3.1, portabilidade=95%
   │
   └─ Balanced (melhor aposta geral)?
      └─ KSWIN + ma=50, min_gap=1000
         └─ Recall=99%, F3=0.24, portabilidade=88%
```

### Tabela Comparativa

| Cenário | Detector | Razão | Performance | Transferability |
|---------|----------|-------|---|---|
| **Max Performance** | FLOSS | F3=0.43 | 🥇 0.4285 | 75.85% |
| **No Tuning** | ADWIN | 95% portabilidade | 0.2879 | 🥇 94.90% |
| **Balanced** | KSWIN | Sweet spot | 0.3176 | 87.84% |
| **Max Recall** | KSWIN | 99.44% detecção | 0.2435 | 87.84% |
| **Min FP** | FLOSS | 2.32 FP/min | 0.3397 | 75.85% |
| **Holistic** | FLOSS | Score=0.9763 | 0.4285 | 75.85% |

---

## 📁 Ficheiros Disponíveis

### Visualizações (Fase 2 - em preparação)
- `option123_summary.png` - Visão conjunta (3 opções em 1 gráfico)
  - Eixo X: Ceiling F3 (Opção 1)
  - Eixo Y: Transferability (Opção 2)
  - Cor/Tamanho: Unified Score (Opção 3)

- `option1_ceiling_analysis.png` - Bar chart com CV
- `option2_portability_heatmap.png` - Heatmap 3 datasets × 6 detectores
- `option3_unified_score_ranking.png` - Bar chart ranqueado
- `production_decision_matrix.png` - Matriz visual de decisão

### Dados (CSVs + Markdown)
- Opção 1: [`../../cross_dataset_analysis/cross_dataset_generalization_option1.*`](../../cross_dataset_analysis/)
- Opção 2: [`../../cross_dataset_analysis/parameter_portability_option2.*`](../../cross_dataset_analysis/)
- Opção 3: [`../../cross_dataset_analysis/unified_robustness_option3.*`](../../cross_dataset_analysis/)

---

## 🔍 Como Navegar

### Se quer: Resumo rápido
→ Ver `option123_summary.png` (quando disponível na Fase 2)

### Se quer: Detalhes de um aspeto
- Performance máxima? → Opção 1 + `option1_ceiling_analysis.png`
- Portabilidade? → Opção 2 + `option2_portability_heatmap.png`
- Score holístico? → Opção 3 + `option3_unified_score_ranking.png`

### Se quer: Decisão prática
→ Ver `production_decision_matrix.png` + tabela acima

### Se quer: Dados numéricos
→ Ver CSVs em `../../cross_dataset_analysis/`

---

## 📊 Visualizações (Fase 2 Roadmap)

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
└── option123_summary.png (NOVO!)
    └── Script: visualize_option123.py (mantém para compatibilidade)
    └── Plot: 3D scatter (X=ceiling, Y=transferability, cor/tamanho=score unificado)
```

---

## 🎓 Referências Relacionadas

- **Relatórios Detalhados**: [`../../cross_dataset_analysis/`](../../cross_dataset_analysis/)
- **Por Dataset**: [`../by_dataset/`](../by_dataset/)
- **Documentação de Métricas**: [`../../../docs/evaluation_metrics_v1.md`](../../../docs/evaluation_metrics_v1.md)
- **Guia Principal**: [`../README.md`](../README.md)

---

## 📝 Notas

1. **As 3 opções não são excludentes** - complementam-se para visão holística
2. **Opção 2 (ADWIN 95%) é superior para produção sem tuning**
3. **Opção 1 (FLOSS 0.43) representa máximo potencial se tiver labels**
4. **Opção 3 (FLOSS score=0.97) é "sabedoria convencional" se não souber qual escolher**
5. **Visualizações atualizadas serão geradas em Fase 2** com dados de 2025-12-14

---

**Última Atualização**: 2025-12-15 (Fase 1 - Estrutura)
**Status**: ✅ Documentação completa; 🔜 Visualizações em Fase 2
