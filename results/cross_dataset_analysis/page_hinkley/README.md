# Análise Cross-Dataset: Page-Hinkley (atualizado 2026-05-14)

> Nota de escopo: esta é uma análise macro/micro por detector. Para rankings finais de publicação e comparação robusta entre detectores, usar os artefatos Option 1/2/3 em `results/cross_dataset_analysis/`.

**Datasets**: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`  
**Critério**: True Macro-Average com cobertura mínima em todos os datasets (n=3).

---

## 🏅 Configuração Generalista

```yaml
lambda_:         10.0
delta:           0.005
alpha:           0.9999
ma_window:       10
min_gap_samples: 1000
F3-weighted macro-average: 0.2637 ± 0.0977
```

- **Mudança vs 24/11**: para generalizar, o algoritmo precisou aumentar o ganho (`lambda_=10`) e reduzir `ma_window` para reagir rápido nos datasets menores.
- **Impacto**: a pontuação macro fica ~21% abaixo do ranking file-weighted (0.3345), mas agora reflete desempenho consistente entre datasets.

### Top 5 (True Macro)

| Rank | λ | δ | α | ma | gap | Score | Std |
|------|---|----|------|----|-----|-------|-----|
| 1 | 10.0 | 0.005 | 0.9999 | 10 | 1000 | **0.2637** | 0.0977 |
| 2 | 10.0 | 0.010 | 0.9999 | 10 | 1000 | 0.2620 | 0.0950 |
| 3 | 10.0 | 0.005 | 0.9999 | 10 | 2000 | 0.2605 | 0.0529 |
| 4 | 10.0 | 0.010 | 0.9999 | 10 | 2000 | 0.2588 | 0.0493 |
| 5 | 10.0 | 0.005 | 0.9999 | 50 | 1000 | 0.2556 | 0.0795 |

**Observações**:
- `lambda_ = 10` em todas as posições: sensibilidade máxima necessária para detectar regimes nos datasets ventriculares.
- `min_gap_samples=1000` ou `2000` aparecem como filtros obrigatórios para domar falsos positivos.

---

## 📉 File-Weighted (Micro) — Apenas Referência

- Melhor combinação micro: `lambda_=10`, `delta=0.005`, `alpha=0.9999`, `ma=10`, `gap=1000` → **0.3345 ± 0.2018**
- Gap macro vs micro: -21% (0.2637 vs 0.3345). A diferença reforça o quanto o dataset `afib_paroxysmal` inflava os resultados.

---

## 🔧 Insights Técnicos

1. **Cobertura**: 384 configurações mantêm `n_datasets=3` (antes 600 sem filtro).  
2. **Tendência paramétrica**:
   - `alpha=0.9999` permanece indispensável (memória longa).
   - `delta ≤ 0.01` oferece melhor equilíbrio; valores maiores degradam vtachyarrhythmias.
   - `ma_window=10` aparece em 4/5 das melhores combinações macro (menos smoothing para captar surtos rápidos).
3. **Robustez**: std máximo nos vencedores fica em 0.098 (antes >0.21), indicando maior consistência entre datasets.

---

## ✅ Recomendações

- **Uso geral**: aplicar a configuração macro (Rank #1) sempre que o pipeline precisar cobrir os três cenários.
- **Afinar para afib_paroxysmal**: consultar o ranking file-weighted ou os artefatos canônicos em `comparisons/afib_paroxysmal/` se o objetivo for maximizar recall nesse dataset específico.
- **Outputs relevantes**:
  - `results/cross_dataset_analysis/page_hinkley/true_macro_average_rankings.csv`
  - `results/cross_dataset_analysis/page_hinkley/true_macro_report.json`
  - `results/cross_dataset_analysis/page_hinkley/file_weighted_report.json`

---

**Próximos passos**:
1. Incluir estas combinações generalistas nas comparações (`src.compare_detectors --dataset <nome>`).  
2. Testar `lambda_` intermediário (2–5) em passos futuros para encontrar equilíbrio custo × sensibilidade.  
3. Documentar limitações do Page-Hinkley para regimes com morfologia muito variável (ex.: vtachyarrhythmias curtas).
