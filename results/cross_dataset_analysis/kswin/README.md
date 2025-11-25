# Análise Cross-Dataset: KSWIN (2025-11-25)

**Datasets**: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`  
**Requisito**: Configurações válidas em todos os 3 datasets (n_datasets=3).

---

## 🥈 Melhor Configuração (True Macro)

```yaml
alpha:           0.01
window_size:     500
stat_size:       20
ma_window:       100
min_gap_samples: 1000
F3-weighted macro-average: 0.2976 ± 0.1015
```

KSWIN continua a ser o **segundo melhor generalista** (atrás apenas do FLOSS). A filtragem por cobertura preservou praticamente todo o desempenho — a pontuação macro caiu apenas 0.002 pontos, demonstrando quão estável o detector já era.

### Top 5 (True Macro)

| Rank | α | win | stat | ma | gap | Score | Std |
|------|----|-----|------|----|-----|-------|-----|
| 1 | 0.01 | 500 | 20 | 100 | 1000 | **0.2976** | 0.1015 |
| 2 | 0.005 | 500 | 20 | 100 | 1000 | 0.2966 | 0.1019 |
| 3 | 0.05 | 500 | 30 | 100 | 1000 | 0.2962 | 0.1014 |
| 4 | 0.05 | 500 | 30 | 50 | 1000 | 0.2961 | 0.1010 |
| 5 | 0.05 | 500 | 20 | 10 | 1000 | 0.2961 | 0.1027 |

**Padrões constantes**:
- `window_size=500` domina 100% das combinações vencedoras.
- `min_gap_samples=1000` continua suficiente — não foi necessário ampliar como no ADWIN.
- `alpha` varia entre 0.005 e 0.05, mostrando que o teste KS tolera níveis de confiança diferentes sem comprometer muito a média.

---

## 📉 File-Weighted (Micro) — Contexto

- Melhor combinação micro: `alpha=0.005`, `window=500`, `stat=50`, `ma=50`, `gap=1000` → **0.3773 ± 0.2114**
- Diferença macro × micro: -21% (efeito natural de dar menos peso ao dataset `afib_paroxysmal`).

---

## 🔧 Insights Técnicos

1. **Cobertura**: todas as 1.280 configurações originais já atendiam `n_datasets=3` — nenhuma foi descartada.
2. **Robustez**: o desvio padrão dos vencedores (≈0.10) é o segundo menor entre os detectores de alta performance.
3. **Sensibilidade vs smoothing**:
   - `stat_size` pequeno (20–30) captura alterações rápidas; `window_size=500` garante contexto.
   - `ma_window` mais longo (50–100) suaviza jitter após a decisão do KS.

---

## ✅ Recomendações

- **Produção streaming**: aplicar a configuração macro (#1) para máximo equilíbrio recall × FP em múltiplos cenários.
- **Analises focadas em afib**: valer-se do ranking file-weighted apenas como baseline histórico, validando sempre nos datasets ventriculares antes de produção.
- **Outputs úteis**:
  - `results/cross_dataset_analysis/kswin/true_macro_average_rankings.csv`
  - `results/cross_dataset_analysis/kswin/true_macro_report.json`
  - `results/cross_dataset_analysis/kswin/file_weighted_report.json`

---

**Próximos passos**:
1. Comparar diretamente vs FLOSS na ferramenta `src.compare_detectors --dataset vtachyarrhythmias`.  
2. Investigar combinações com `min_gap_samples=1500/2000` para casos com ruído ventricular extremo.  
3. Incorporar os resultados em ensembles híbridos (ex.: KSWIN + FLOSS) para reduzir FP mantendo alto recall.
