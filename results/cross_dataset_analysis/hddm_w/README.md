# Análise Cross-Dataset: HDDM_W (2025-11-25)

**Datasets**: `afib_paroxysmal`, `malignantventricular`, `vtachyarrhythmias`  
**Critério**: True Macro-Average (igual peso por dataset) filtrando apenas combinações presentes nos três cenários.

---

## 🔻 Resultado Geral

```yaml
drift_confidence:    0.005
warning_confidence:  0.001  # (variações não mudam o score)
lambda_option:       0.01
two_side_option:     False   # (True e False empatam)
ma_window:           1
min_gap_samples:     1000
F3-weighted macro-average: 0.1252 ± 0.1552
```

- **Posição**: último lugar entre os 6 detectores testados.
- **Impacto do filtro**: nenhuma combinação foi removida (todas as 2.560 já apareciam nos 3 datasets), mas os valores macro evidenciam a fragilidade do método.

### Top 5 (True Macro)

Todos os cinco primeiros empataram exatamente no score e no desvio padrão; variam apenas em `warning_confidence`, `two_side_option` e `lambda_option` (entre 0.01 e 0.2).

| Rank | drift | warn | λ | two_side | ma | gap | Score | Std |
|------|-------|------|----|-----------|----|-----|-------|-----|
| 1 | 0.005 | 0.001 | 0.01 | False | 1 | 1000 | **0.1252** | 0.1552 |
| 2 | 0.005 | 0.005 | 0.01 | True | 1 | 1000 | 0.1252 | 0.1552 |
| 3 | 0.005 | 0.001 | 0.01 | True | 1 | 1000 | 0.1252 | 0.1552 |
| 4 | 0.005 | 0.050 | 0.01 | True | 1 | 1000 | 0.1252 | 0.1552 |
| 5 | 0.005 | 0.010 | 0.01 | False | 1 | 1000 | 0.1252 | 0.1552 |

**Conclusão**: assim como no HDDM_A, `warning_confidence` e `two_side_option` têm impacto mínimo. Porém, aqui nem `lambda` diferente melhora o cenário.

---

## 📉 File-Weighted (Micro) — Apenas histórico

- Melhor combinação micro (sem mudança): `drift=0.005`, `warning=0.001`, `lambda=0.2`, `two_side=True`, `ma=1`, `gap=1000` → **0.2843 ± 0.2567**
- Diferença macro × micro: -56% (0.1252 vs 0.2843). O score file-weighted era inflado por afib_paroxysmal e mascarava o baixo desempenho nos datasets ventriculares.

---

## 🔧 Insights e Recomendações

1. **Performance baixa**: 0.1252 é menos da metade do score do HDDM_A (0.2584) e 3× inferior ao FLOSS (0.3958).
2. **Alta variância**: std ≈ 0.155 — o maior entre todos os detectores; imprevisível em dados novos.
3. **Parâmetros com pouco efeito**: `warning_confidence`, `two_side_option` e até `lambda` mostraram empate numérico no topo.
4. **Recomendação prática**: **substituir HDDM_W por HDDM_A** em qualquer pipeline cross-dataset. O irmão “Average” é 2× melhor em score e ainda mais robusto.

---

### Quando (não) usar

- ❌ **Produção generalista**: evitar. HDDM_A, ADWIN ou KSWIN são alternativas superiores em todos os aspectos.
- ❌ **Cenários específicos**: mesmo focando em `afib_paroxysmal`, o ganho não justifica a variabilidade extrema.
- ✅ **Uso acadêmico**: apenas se o objetivo for comparar variantes de HDDM ou avaliar o impacto do termo `lambda`.

---

**Arquivos para referência**:
- `results/cross_dataset_analysis/hddm_w/true_macro_average_rankings.csv`
- `results/cross_dataset_analysis/hddm_w/true_macro_report.json`
- `results/cross_dataset_analysis/hddm_w/file_weighted_report.json`

**Próximos passos sugeridos**:
1. Remover HDDM_W das comparações principais para simplificar relatórios.
2. Caso mantenha, documentar explicitamente que os resultados são apenas para fins de contraste histórico.
