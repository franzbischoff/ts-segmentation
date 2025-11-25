# Análise Cross-Dataset: HDDM_A (2025-11-25)

**Datasets**: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`  
**Critério**: True Macro-Average com `n_datasets = 3` garantido.

---

## 🛡️ Melhor Configuração (generalista mais estável)

```yaml
drift_confidence:    0.005
warning_confidence:  0.050   # (0.005/0.001 dão o mesmo resultado)
two_side_option:     True
ma_window:           1
min_gap_samples:     2000
F3-weighted macro-average: 0.2584 ± 0.0593
```

- **Mudança vs 24/11**: o `min_gap_samples` precisou ser aumentado para 2000 para manter a consistência nos datasets ventriculares; o score macro agora reflete exclusivamente combinações presentes em todos os cenários.
- **Destaque**: continua sendo o detector **mais robusto** (std < 0.06), mesmo após a filtragem.

### Top 5 (True Macro)

| Rank | drift | warning | two_side | ma | gap | Score | Std |
|------|-------|---------|----------|----|-----|-------|-----|
| 1 | 0.005 | 0.050 | True | 1 | 2000 | **0.2584** | 0.0593 |
| 2 | 0.005 | 0.005 | True | 1 | 2000 | 0.2584 | 0.0593 |
| 3 | 0.005 | 0.001 | True | 1 | 2000 | 0.2584 | 0.0593 |
| 4 | 0.005 | 0.010 | True | 1 | 2000 | 0.2584 | 0.0593 |
| 5 | 0.005 | 0.005 | False | 1 | 2000 | 0.2573 | 0.0530 |

**Conclusão**: o parâmetro `warning_confidence` permanece praticamente irrelevante enquanto `drift_confidence=0.005`. O fator decisivo foi ampliar `min_gap_samples`.

---

## 📉 File-Weighted (Micro) – Contexto

- Melhor combinação micro (sem filtro): `drift=0.005`, `warning=0.01`, `two_side=True`, `ma=1`, `gap=1000` → **0.3273 ± 0.1944**
- Diferença macro × micro: -21% (0.2584 vs 0.3273) — reflexo direto do peso enorme de `afib_paroxysmal`.

---

## 🔧 Insights

1. **Cobertura**: todas as 640 combinações originais passam na filtragem (`n_datasets=3`), mas apenas as com `gap=2000` mantêm o topo macro.
2. **Robustez**: std ≤ 0.06 nas melhores configs (long shot melhor que qualquer outro detector).
3. **Smoothing**: `ma_window=1` continua suficiente; adicionar média móvel degrada recall nos datasets menores.
4. **Dois lados**: `two_side=True` traz pequeno ganho (+0.001) e segue recomendado.

---

## ✅ Recomendações

- **Quando usar**: pipelines que priorizam **consistência extrema** mesmo sacrificando recall/pontuação absoluta.
- **Quando evitar**: aplicações que exigem máxima sensibilidade (FLOSS/KSWIN/Page-Hinkley têm scores bem maiores).
- **Arquivos úteis**:
  - `results/cross_dataset_analysis/hddm_a/true_macro_average_rankings.csv`
  - `results/cross_dataset_analysis/hddm_a/true_macro_report.json`
  - `results/cross_dataset_analysis/hddm_a/file_weighted_report.json`

---

**Próximos passos**:
1. Avaliar variantes com `min_gap_samples=2500` para cenários ainda mais barulhentos.  
2. Usar HDDM_A como “detector de fallback” em ensembles (ativo apenas quando detectores agressivos discordam).  
3. Documentar o comportamento “warning sem efeito” em `docs/evaluation_metrics_v1.md` para futuros operadores.
