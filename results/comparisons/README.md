# 📊 Detector Comparisons & Analysis — HISTÓRICO VISUAL

> ⚠️ **IMPORTANTE**: Esta pasta contém **visualizações históricas** geradas em Dezembro 2025.
>
> **Para números finais e rankings de publicação**, consultar: [`comparisons/<dataset>/`](../../comparisons/)
>
> **Para replicar estas visualizações**, ver: [Geração de Relatórios](#-geração-de-relatórios)

**Última Atualização**: 2026-05-14
**Status**: Arquivo visual de apoio (não canônico; use `comparisons/<dataset>/` para métricas/rankings)

---

## 📁 Estrutura de Navegação

### 🎯 **1. Comparações por Dataset** → `by_dataset/`

Visualizações multi-detector por dataset específico. Cada pasta contém:
- **Gráficos comparativos** gerados localmente em `visualizations/`:
  - `radar_6detectors.png` - Visão holística (6 detectores × 6 métricas)
  - `f3_vs_fp_scatter.png` - Trade-off performance vs alarmes
  - `heatmap_metrics_comparison.png` - Comparação de sensibilidade de detectores
  - `parameter_tradeoffs.png` - Trade-offs multi-objetivo

⚠️ **Nota**: Os ficheiros `comparative_report.md`, `detector_rankings.csv`, etc. estão no local canônico: [`comparisons/<dataset>/`](../../comparisons/)

**Datasets com Visualizações:**
- [**afib_paroxysmal**](by_dataset/afib_paroxysmal/) - 229 ficheiros, 1,301 eventos → [resultados canônicos](../../comparisons/afib_paroxysmal/)
- [**malignantventricular**](by_dataset/malignantventricular/) - 22 ficheiros, 592 eventos → [resultados canônicos](../../comparisons/malignantventricular/)
- [**vtachyarrhythmias**](by_dataset/vtachyarrhythmias/) - 34 ficheiros, 97 eventos → [resultados canônicos](../../comparisons/vtachyarrhythmias/)

---

### 🌍 **2. Análises Cross-Dataset** → `cross_dataset/`

Análises robustez e portabilidade de detectores **através de múltiplos datasets**. Incluem as **3 opções de avaliação**:

#### **Opção 1: Performance Ceiling** 🎯
- Pergunta: "Qual é a melhor performance que cada detector consegue atingir (quando tunado)?
- Métrica: F3-weighted máximo por dataset (macro-average)
- Ficheiro: `option1_ceiling_analysis.png`
- Ranking: FLOSS (0.4306) > KSWIN (0.3203) > Page-Hinkley (0.3152)

#### **Opção 2: Parameter Portability** 🚀
- Pergunta: "Consigo usar hiperparâmetros de um dataset noutro sem re-tuning?"
- Métrica: Transferability ratio (params origem → alvo)
- Ficheiro: `option2_portability_heatmap.png`
- Ranking: ADWIN (95.07%) > KSWIN (87.75%) > FLOSS (75.83%)

#### **Opção 3: Unified Robustness Score** ⚖️
- Pergunta: "Qual detector é globalmente robusto (combinando ceiling + portabilidade)?"
- Fórmula: `0.6×(1 - 2-fold gap) + 0.4×(1 - transfer_variance)`
- Ficheiro: `option3_unified_score_ranking.png`
- Ranking: FLOSS (0.9761) > ADWIN (0.9710) > KSWIN (0.9690)

#### **Production Decision Matrix** 🎓
- Ficheiro: `production_decision_matrix.png`
- Matriz de decisão: Qual detector escolher (por cenário)
  - Novo dataset COM labels? → FLOSS + grid search
  - Novo dataset SEM labels? → ADWIN (95% portabilidade)
  - Balanced? → KSWIN (sweet spot)

---

## 📊 Comparação Rápida: 3 Opções

| Perspetiva | Foco | Top Detector | Score | Use Case |
|-----------|------|---|---|---|
| **Opção 1** | 🎯 Máxima performance | FLOSS | F3=0.4306 | Research, max performance |
| **Opção 2** | 🚀 Portabilidade | ADWIN | 95.07% | Production ready, sem labels |
| **Opção 3** | ⚖️ Robustez unificada | FLOSS | 0.9761 | Escolha holística |

---

## 🔍 Como Usar Esta Estrutura

### Cenário 1: "Qual detector é melhor para dataset X?"
1. Ler `comparisons/<dataset>/comparative_report.md`
2. Consultar `comparisons/<dataset>/detector_rankings.csv` e `detector_summary.csv`
3. Usar `results/comparisons/by_dataset/<dataset>/visualizations/` apenas como apoio visual histórico

### Cenário 2: "Qual detector escolho para produção?"
1. Ir a `cross_dataset/`
2. Ler `production_decision_matrix.png`
3. Se tiver labels → usar Opção 1 (FLOSS)
4. Se SEM labels → usar Opção 2 (ADWIN)
5. Se quiser balanced → considerar KSWIN como sweet spot e validar contra Opção 3

### Cenário 3: "Como transferir hiperparâmetros entre datasets?"
1. Ir a `cross_dataset/`
2. Ver `option2_portability_heatmap.png`
3. ADWIN: ~95% chance de retenção média (melhor choice)
4. FLOSS: ~76% de retenção média (precisa validação)

---

## 📝 Estrutura de Ficheiros (Histórica)

```
results/comparisons/  (HISTÓRICO VISUAL APENAS)
├── README.md (este ficheiro)
│
├── by_dataset/  (visualizações PNG)
│   ├── afib_paroxysmal/visualizations/
│   │   ├── radar_6detectors.png
│   │   ├── f3_vs_fp_scatter.png
│   │   ├── heatmap_metrics_comparison.png
│   │   └── parameter_tradeoffs.png
│   ├── malignantventricular/visualizations/ (mesma estrutura)
│   └── vtachyarrhythmias/visualizations/ (mesma estrutura)
│
└── cross_dataset/  (visualizações PNG cross-dataset)
    ├── option1_ceiling_analysis.png
    ├── option2_portability_heatmap.png
    ├── option3_unified_score_ranking.png
    └── production_decision_matrix.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

comparisons/  (LOCAL CANÔNICO PARA PUBLICAÇÃO)
├── afib_paroxysmal/
│   ├── comparative_report.md
│   ├── detector_rankings.csv
│   ├── detector_summary.csv
│   ├── constraint_tradeoffs.csv
│   └── robustness.csv
├── malignantventricular/ (mesma estrutura)
└── vtachyarrhythmias/ (mesma estrutura)
```

---

## 🔄 Estado de Geração

- Visualizações by-dataset: concluídas em `results/comparisons/by_dataset/*/visualizations/`.
- Visualizações cross-dataset: concluídas em `results/comparisons/cross_dataset/`.
- Relatórios canônicos para decisão/publicação: `comparisons/<dataset>/`.

---

## 🛠️ Geração de Relatórios

Para atualizar todas as comparações de uma vez:

```bash
# Atualiza visualizações históricas em results/comparisons/
python -m src.generate_comparison_reports \
    --datasets afib_paroxysmal malignantventricular vtachyarrhythmias \
    --output-base results/comparisons
```

Para comparação por dataset específico:

```bash
# Gera comparações + visualizações para um dataset
python -m src.visualize_comparison_by_dataset \
    --dataset afib_paroxysmal \
    --output-dir results/comparisons/by_dataset/afib_paroxysmal/visualizations
```

Para análise cross-dataset:

```bash
# Gera análises de robustez (opções 1, 2, 3) + decision matrix
python -m src.visualize_cross_dataset_summary \
    --output-dir results/comparisons/cross_dataset
```

---

## 📚 Referências Relacionadas

- **Análises Detalhadas por Detector**: [`results/cross_dataset_analysis/`](../cross_dataset_analysis/)
- **Resultados por Dataset**: [`results/<dataset>/<detector>/`](../)
- **Documentação de Métricas**: [`docs/evaluation_metrics.md`](../../docs/evaluation_metrics.md)
- **Guia de Visualizações**: [`docs/visualizations_guide.md`](../../docs/visualizations_guide.md)

---

## 📌 Notas Importantes

1. `results/comparisons/` é histórico e visual.
  - Para rankings e números finais de publicação, usar `comparisons/<dataset>/`.

2. Os artefatos legados FLOSS vs KSWIN foram movidos para `tmp/results_comparisons_legacy/`.
  - Ficam fora do versionamento por serem somente histórico local.

3. **Opções 1, 2, 3** são complementares, não excludentes
   - Opção 1: foco em performance máxima
   - Opção 2: foco em portabilidade
   - Opção 3: foco em robustez global
   - Juntas: perspetiva holística

4. O arquivo `option123_summary.png` é mantido em `results/cross_dataset_analysis/`.
