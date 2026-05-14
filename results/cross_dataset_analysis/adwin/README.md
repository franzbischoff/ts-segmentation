# Análise Cross-Dataset: ADWIN (atualizado 2026-05-14)

> Nota de escopo: esta é uma análise macro/micro por detector. Para rankings finais de publicação e comparação robusta entre detectores, usar os artefatos Option 1/2/3 em `results/cross_dataset_analysis/`.

**Datasets considerados**: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`  
**Modo principal**: True Macro-Average (cada dataset = 1/3 do peso) com requisito de cobertura em todos os 3 datasets.

---

## 🏆 Configuração Mais Robusta (True Macro)

```yaml
delta:           0.05
ma_window:       200
min_gap_samples: 2000
F3-weighted macro-average: 0.2863 ± 0.0761
```

- **Mudança chave**: a filtragem por cobertura removeu as “especialistas”. Só ficaram combinações que funcionam nos 3 datasets.
- **Tendências**: valores de `delta` médios-altos (0.05–0.10) + `ma_window` largo (200–250) e `min_gap_samples=2000` reduziram falsos positivos sem colapsar o recall dos datasets menores.

### Top 5 (True Macro)

| Rank | delta | ma_window | gap | Score | Std |
|------|-------|-----------|-----|-------|-----|
| 1 | 0.05 | 200 | 2000 | **0.2863** | 0.0761 |
| 2 | 0.10 | 150 | 2000 | 0.2862 | 0.0681 |
| 3 | 0.06 | 200 | 2000 | 0.2861 | 0.0743 |
| 4 | 0.025 | 250 | 2000 | 0.2847 | 0.0639 |
| 5 | 0.020 | 250 | 2000 | 0.2841 | 0.0695 |

**Insight**: todos os vencedores usam `min_gap_samples=2000` (≈8 s @ 250 Hz), confirmando que ADWIN precisa de supressão mais longa para manter estabilidade fora do afib.

---

## 📉 File-Weighted (Micro) para Referência

O ranking ponderado por número de ficheiros continua dominado por `afib_paroxysmal`, portanto permanece útil apenas como “baseline histórico”.

- **Melhor combinação micro**: `delta=0.015`, `ma_window=250`, `gap=1000` → **0.3629 ± 0.2145**
- **Gap macro vs micro**: -21% (0.2863 vs 0.3629). O ganho artificial vinha da dependência do dataset maior.

---

## 🔍 Resumo Técnico

1. **Cobertura total**: 495 configurações atendem `n_datasets=3` (antes 594 sem filtro).  
2. **Distribuição**: média = 0.2249, mediana = 0.2244, min std = 0.0117 (configurações mais estáveis).
3. **Perfil paramétrico**:
   - `delta` entre 0.02 e 0.10 oferece o melhor compromisso recall × FP.
   - `ma_window ≥ 200` suaviza ruído entre classes.
   - `min_gap_samples=2000` torna-se padrão para uso cross-dataset.

---

## ✅ Recomendações

- **Produção multi-dataset**: usar a configuração macro (#1) → menos sensível, porém consistente.
- **Afinar para um dataset específico**: consulte `file_weighted_rankings.csv`, mas valide manualmente fora do afib.
- **Relatórios úteis**:
  - `results/cross_dataset_analysis/adwin/true_macro_average_rankings.csv`
  - `results/cross_dataset_analysis/adwin/true_macro_report.json`
  - `results/cross_dataset_analysis/adwin/file_weighted_report.json`

---

**Próximos passos sugeridos**:
1. Validar ADWIN macro vs FLOSS/KSWIN no `src.compare_detectors` (modo `--dataset` por classe).  
2. Explorar `min_gap_samples` > 2000 para cenários onde os datasets pequenos continuam ruidosos.  
3. Adicionar visualizações cruzadas (heatmaps macro) destacando a região `delta∈[0.05,0.10]`.
