# Análise Cross-Dataset: FLOSS (atualizado 2026-05-14)

> Nota de escopo: esta é uma análise macro/micro por detector. Para rankings finais de publicação e comparação robusta entre detectores, usar os artefatos Option 1/2/3 em `results/cross_dataset_analysis/`.

**Datasets**: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`
**Critério padrão**: True Macro-Average com cobertura em todos os datasets.

---

## 🥇 Campeão Geral (True Macro)

```yaml
window_size:         125
regime_threshold:    0.55
regime_landmark:     5.0
min_gap_samples:     1000
F3-weighted macro-average: 0.3982 ± 0.0981
```

- **Status**: continua líder isolado, agora com configurações que comprovadamente funcionam nos três datasets.
- **Mudança vs 24/11**: o grid expandido revelou que janelas maiores (125) e thresholds médios entregam equilíbrio melhor que a combinação antiga (window=75, threshold=0.7) quando exigimos cobertura total.

### Top 5 (True Macro)

| Rank | window | thresh | landmark | gap | Score | Std |
|------|--------|--------|----------|-----|-------|-----|
| 1 | 125 | 0.55 | 5.0 | 1000 | **0.3982** | 0.0981 |
| 2 | 125 | 0.60 | 5.0 | 1000 | 0.3961 | 0.0948 |
| 3 | 125 | 0.55 | 5.0 | 500 | 0.3959 | 0.0921 |
| 4 | 125 | 0.50 | 4.5 | 1000 | 0.3949 | 0.1136 |
| 5 | 125 | 0.55 | 4.5 | 1000 | 0.3930 | 0.0987 |

**Insights**:
- `window_size=125` domina o top-5 (≈0.5 s @ 250 Hz).
- `regime_threshold` entre 0.50–0.60 garante recall alto sem explosão de FP.
- `regime_landmark` 4.5–5.0 é o “sweet spot” para segmentar regimes sem antecipar demais.

---

## 📉 File-Weighted (Micro) — Referência histórica

- Melhor combinação micro permanece `window=75`, `threshold=0.7`, `landmark=4.0`, `gap=1000` → **0.4491 ± 0.2244**
- Diferença macro × micro: -11%. O file-weighted ainda mostra o teto máximo quando o dataset `afib_paroxysmal` domina (80% dos ficheiros).

---

## 🔧 Resumo Técnico

1. **Cobertura total**: 25.920 combinações aparecem nos 3 datasets (nenhuma filtrada).
2. **Estabilidade**: std médio das top configs fica em ≈0.10 — muito melhor do que 0.228 observado quando olhamos apenas para o melhor F3* em afib.
3. **Min gap**: 1000 continua ótimo; aumentar para 2000 não trouxe ganhos relevantes no macro ranking.
4. **Window maior**: janelas ≥125 oferecem resiliência aos artefatos ventriculares mantendo recall alto em afib.

---

## ✅ Recomendações

- **Produção multi-dataset**: usar a configuração macro (#1) como padrão.
- **Afinar para um dataset específico**: recorrer ao ranking file-weighted apenas como ponto de partida e validar manualmente.
- **Documentos úteis**:
  - `results/cross_dataset_analysis/floss/true_macro_average_rankings.csv`
  - `results/cross_dataset_analysis/floss/true_macro_report.json`
  - `results/cross_dataset_analysis/floss/file_weighted_report.json`

---

**Próximos passos**:
1. Testar ensembles “FLOSS + detector clássico” para reduzir FP mantendo o recall superior.
2. Geração de gráficos comparando o novo espaço (window 125) vs combinações antigas (window 75).
3. Atualizar `comparisons/<dataset>/*` usando as configurações macro generalistas para evitar o antigo viés do dataset principal.
