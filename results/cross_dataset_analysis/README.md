# Cross-Dataset Analysis Overview (2025-11-25)

**Objetivo**: encontrar configurações de detectores de mudança que generalizem entre `afib_paroxysmal`, `malignantventricular` e `vtachyarrhythmias`.  
**Ferramenta**: `src.cross_dataset_analysis.py` com o novo parâmetro `--min-datasets` (default = nº de datasets listados).

---

## 🆕 O que mudou nesta atualização?

1. **Cobertura obrigatória** (`n_datasets >= 3`) em todos os rankings CSV/JSON.
2. **Novas recomendações macro** para cada detector, refletidas nas pastas `results/cross_dataset_analysis/<detector>/`.
3. **Documentação atualizada** (`README.md` por detector + arquivos de síntese) para remover o “specialist loophole”.

---

## 📊 Resultados Principais (True Macro)

| Detector | Melhor Configuração (resumo) | Score | Std |
|----------|------------------------------|-------|-----|
| **FLOSS** | window=125, thr=0.55, landmark=5.0, gap=1000 | **0.3958** | 0.0972 |
| **KSWIN** | α=0.01, win=500, stat=20, ma=100, gap=1000 | 0.2976 | 0.1015 |
| ADWIN | delta=0.05, ma=200, gap=2000 | 0.2835 | **0.0745** |
| Page-Hinkley | λ=10, δ=0.005, α=0.9999, ma=10, gap=1000 | 0.2625 | 0.0966 |
| HDDM_A | drift=0.005, warn=0.05, two_side=True, ma=1, gap=2000 | 0.2584 | **0.0593** |
| HDDM_W | drift=0.005, warn=0.001, λ=0.01, two_side=False, ma=1, gap=1000 | 0.1252 | 0.1552 |

---

## 📁 Estrutura Atualizada

```
results/cross_dataset_analysis/
├── README.md                      # este ficheiro
├── CROSS_DATASET_ANALYSIS_SUMMARY.md
├── AGGREGATION_METHODS_COMPARISON.md
├── <detector>/
│   ├── README.md                  # análise específica (macro vs micro)
│   ├── true_macro_average_rankings.csv
│   ├── true_macro_report.json
│   ├── file_weighted_rankings.csv
│   └── file_weighted_report.json
```

Cada `README.md` individual descreve:
- Configuração “macro” recomendada (com cobertura total).
- Configuração “file-weighted” apenas para referência.
- Principais insights paramétricos e próximos passos.

---

## 🔧 Como reproduzir

```bash
# Macro-average com cobertura total
python -m src.cross_dataset_analysis \
    --detector adwin \
    --mode true_macro \
    --min-datasets 3 \
    --output results/cross_dataset_analysis/adwin

# File-weighted para comparação histórica
python -m src.cross_dataset_analysis \
    --detector adwin \
    --mode file_weighted \
    --min-datasets 3 \
    --output results/cross_dataset_analysis/adwin
```

---

## ✅ Próximos Passos

1. Rodar `src.compare_detectors` utilizando as novas configurações “macro” como baseline.
2. Levar o parâmetro `--min-datasets` à documentação principal, para que outros membros também garantam cobertura mínima.
3. Criar visualizações específicas destacando a região paramétrica macro-ótima de cada detector.
