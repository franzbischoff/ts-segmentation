# Cross-Dataset Analysis (Atualização 2025-11-25)

**Script**: `python -m src.cross_dataset_analysis`
**Datasets**: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`
**Mudança chave**: Todas as métricas passaram a exigir **cobertura em todos os datasets** (`n_datasets=3`). Isso elimina o antigo “specialist loophole”, onde combinações inexistentes nos datasets menores inflavam o score macro.

---

## 🏆 Ranking True Macro (peso igual por dataset)

| Rank | Detector | Melhor Configuração (resumo) | Score | Std |
|------|----------|------------------------------|-------|-----|
| **1** | **FLOSS** | `window=125`, `thr=0.55`, `landmark=5.0`, `gap=1000` | **0.3958** | 0.0972 |
| **2** | **KSWIN** | `alpha=0.01`, `window=500`, `stat=20`, `ma=100`, `gap=1000` | **0.2976** | 0.1015 |
| 3 | ADWIN | `delta=0.05`, `ma=200`, `gap=2000` | 0.2835 | **0.0745** |
| 4 | Page-Hinkley | `λ=10`, `δ=0.005`, `α=0.9999`, `ma=10`, `gap=1000` | 0.2625 | 0.0966 |
| 5 | HDDM_A | `drift=0.005`, `warn=0.05`, `two_side=True`, `ma=1`, `gap=2000` | 0.2584 | **0.0593** |
| 6 | HDDM_W | `drift=0.005`, `warn=0.001`, `λ=0.01`, `two_side=False`, `ma=1`, `gap=1000` | 0.1252 | 0.1552 |

**Observações rápidas**:
- FLOSS mantém folga de ~10 p.p. sobre o segundo colocado.
- ADWIN e Page-Hinkley continuam competitivos, porém agora com `min_gap` maior/`lambda` agressivo para suportar os datasets ventriculares.
- HDDM_A continua imbatível em robustez (std < 0.06), mas com score apenas moderado.

---

## 📉 Ranking File-Weighted (micro, 80% peso em afib)

| Rank | Detector | Melhor Configuração | Score | Std |
|------|----------|---------------------|-------|-----|
| **1** | **FLOSS** | `window=75`, `thr=0.7`, `landmark=4.0`, `gap=1000` | **0.4491** | 0.2244 |
| 2 | KSWIN | `alpha=0.005`, `window=500`, `stat=50`, `ma=50`, `gap=1000` | 0.3773 | 0.2114 |
| 3 | ADWIN | `delta=0.015`, `ma=250`, `gap=1000` | 0.3629 | 0.2145 |
| 4 | Page-Hinkley | `λ=10`, `δ=0.005`, `ma=10`, `gap=1000` | 0.3345 | 0.2018 |
| 5 | HDDM_A | `drift=0.005`, `warn=0.01`, `ma=1`, `gap=1000` | 0.3273 | 0.1944 |
| 6 | HDDM_W | `drift=0.005`, `warn=0.001`, `λ=0.2`, `ma=1`, `gap=1000` | 0.2843 | 0.2567 |

*Use estes valores apenas como baseline histórico; o file-weighted continua enviesado para `afib_paroxysmal`.*

---

## 🔑 Principais Insights Após a Atualização

1. **Cobertura obrigatória mudou os vencedores**: ADWIN e Page-Hinkley passaram a recomendar `min_gap_samples=2000` ou `λ=10/ma=10`, reduzindo muito a discrepância entre datasets.
2. **Min gap ideal varia por detector**:
   - `1000` continua ótimo para FLOSS, KSWIN e HDDM_W.
   - `2000` é o novo padrão para ADWIN e HDDM_A.
3. **Std como sinal de robustez**:
   - HDDM_A (0.059) e ADWIN (0.074) são os mais previsíveis.
   - FLOSS e KSWIN ficam em torno de 0.10 (ainda muito bons).
   - HDDM_W permanece instável (0.155).
4. **FLOSS segue líder absoluto** mesmo após remover o viés — o método de matrix profile generaliza melhor que os detectores clássicos de drift.

---

## 📁 Onde Encontro os Artefatos?

```
results/cross_dataset_analysis/
├── <detector>/
│   ├── file_weighted_rankings.csv
│   ├── file_weighted_report.json
│   ├── true_macro_average_rankings.csv
│   ├── true_macro_report.json
│   └── README.md   # resumo específico por detector
├── AGGREGATION_METHODS_COMPARISON.md
└── CROSS_DATASET_ANALYSIS_SUMMARY.md  (este ficheiro)
```

---

## ✅ Próximos Passos Sugeridos

1. **Comparações atualizadas**: rodar `src.compare_detectors` usando as novas combinações macro para alimentar `comparisons/<dataset>/`.
2. **Documentação**: Referenciar explicitamente o parâmetro `--min-datasets` no README principal do projeto.
3. **Novos gráficos**: Gerar heatmaps com a métrica macro para comunicar as regiões “generalistas” por detector.
4. **Ensembles**: investigar “FLOSS + detector clássico” para reduzir FP mantendo o alto recall evidenciado no file-weighted.
