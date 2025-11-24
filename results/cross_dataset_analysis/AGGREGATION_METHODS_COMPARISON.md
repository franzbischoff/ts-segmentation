# Cross-Dataset Analysis: Comparison of Aggregation Methods

**Date**: 2025-11-24
**Methods Compared**: File-Weighted (micro-average) vs True Macro-Average

---

## 📊 Key Difference

### File-Weighted (Micro-Average)
- **Concatenates all files** from all datasets
- **Más peso** ao dataset maior (afib_paroxysmal = 229/285 = 80% do peso)
- **Fórmula**: `mean(all_files_concat)`

### True Macro-Average
- **Calcula média por dataset** primeiro
- **Peso igual** para cada dataset (afib = malignant = vtachy = 1/3 cada)
- **Fórmula**: `mean(dataset_means)`

---

## 🏆 Rankings Comparativos

### TRUE MACRO-AVERAGE (cada dataset pesa 1/3)

| Rank | Detector | Score | Std | Robustez |
|------|----------|-------|-----|----------|
| **1** 🥇 | **FLOSS** | **0.3958** | 0.0972 | ⭐⭐⭐⭐ Excelente |
| **2** 🥈 | **KSWIN** | **0.2976** | 0.1015 | ⭐⭐⭐⭐ Excelente |
| **3** 🥉 | **HDDM_A** | **0.2584** | 0.0593 | ⭐⭐⭐⭐⭐ Muito robusto |
| 4 | HDDM_W | 0.1252 | 0.1552 | ⭐⭐ Menos robusto |

**Nota**: ADWIN e Page-Hinkley não aparecem porque suas top configs estão presentes apenas em 1 dataset (não generalizaram).

### FILE-WEIGHTED (favorece dataset maior - 80% afib_paroxysmal)

| Rank | Detector | Score | Std | Observação |
|------|----------|-------|-----|------------|
| **1** 🥇 | **FLOSS** | **0.4491** | 0.2244 | Beneficia de afib_paroxysmal |
| **2** 🥈 | **Page-Hinkley** | **0.3885** | 0.2117 | Top config presente em 1 dataset |
| **3** 🥉 | **KSWIN** | **0.3773** | 0.2114 | - |
| 4 | ADWIN | 0.3629 | 0.2145 | Top config presente em 1 dataset |
| 5 | HDDM_A | 0.3273 | 0.1944 | - |
| 6 | HDDM_W | 0.2843 | 0.2567 | - |

---

## 🔍 Análise Comparativa

### FLOSS
- **File-weighted**: 0.4491 (melhor por far)
- **True macro**: 0.3958 (-11.9%)
- **Conclusão**: FLOSS beneficia do dataset maior mas AINDA É #1 no true macro! 🏆

### KSWIN
- **File-weighted**: 0.3773
- **True macro**: 0.2976 (-21.1%)
- **Conclusão**: Perde bastante quando datasets pequenos pesam igual

### HDDM_A
- **File-weighted**: 0.3273
- **True macro**: 0.2584 (-21.1%)
- **Conclusão**: Similar ao KSWIN, perde com peso igual

### HDDM_W
- **File-weighted**: 0.2843
- **True macro**: 0.1252 (-56.0%!)
- **Conclusão**: COLAPSA no true macro! Muito pior nos datasets pequenos

### Page-Hinkley & ADWIN
- **File-weighted**: Presente no ranking
- **True macro**: NÃO aparecem (top configs só no afib_paroxysmal)
- **Conclusão**: **NÃO generalizam** - overfitting ao dataset maior!

---

## 💡 Insights Principais

1. **FLOSS domina em AMBOS** os métodos 🏆
   - File-weighted: 0.4491 (#1)
   - True macro: 0.3958 (#1)
   - Único detector consistentemente superior

2. **Page-Hinkley e ADWIN NÃO generalizam**
   - Top configs aparecem apenas em afib_paroxysmal
   - **Overfitting** ao dataset maior
   - Não confiáveis cross-dataset

3. **HDDM_W é pior em tudo**
   - Último em file-weighted (0.2843)
   - Pior ainda em true macro (0.1252, -56%!)
   - Evitar completamente

4. **HDDM_A ganha robustez** no true macro
   - Std = 0.0593 (melhor robustez!)
   - Mas performance cai 21%

5. **KSWIN estável**
   - #3 no file-weighted
   - #2 no true macro
   - Boa robustez (std=0.10)

---

## 🎯 Recomendações Finais

### Para Produção (Máxima Performance)
✅ **Use FLOSS** (ambos métodos confirmam: #1 consistente)
- File-weighted: 0.4491
- True macro: 0.3958
- **Conclusão**: Melhor em QUALQUER método de agregação

### Para Máxima Generalização (Peso Igual aos Datasets)
✅ **Use FLOSS ou KSWIN**
- FLOSS: 0.3958 (±0.097) - Melhor performance
- KSWIN: 0.2976 (±0.102) - Segunda opção

### Para Robustez Máxima
✅ **Use HDDM_A**
- True macro: 0.2584 (±0.059)
- Menor std entre todos!
- Trade-off: performance moderada

### ⚠️ Evitar
❌ **HDDM_W**: Pior em tudo (colapsa -56% no true macro)
❌ **Page-Hinkley**: Não generaliza (só presente em 1 dataset)
❌ **ADWIN**: Não generaliza (só presente em 1 dataset)

---

## 📁 Ficheiros Gerados

Cada detector tem agora:

```
results/cross_dataset_analysis/<detector>/
├── file_weighted_rankings.csv       # Micro-average (80% afib)
├── file_weighted_report.json
├── true_macro_average_rankings.csv  # Macro-average (cada dataset 1/3)
├── true_macro_report.json
└── cross_dataset_report.json        # Old (renomear manualmente se necessário)
```

---

## 🔬 Conclusão Técnica

**True Macro-Average revela configurações que NÃO generalizam**:
- Page-Hinkley e ADWIN pareciam bons (file-weighted: #2 e #4)
- Mas **overfittam ao afib_paroxysmal** (80% do peso)
- True macro expõe esta falha (top configs ausentes em outros datasets)

**FLOSS é o único detector robusto**:
- Lidera em AMBOS os métodos de agregação
- Performa bem em TODOS os 3 datasets
- Recomendação: **FLOSS para produção** 🎯

**Próximos passos**:
- Atualizar documentação com descobertas
- Regenerar READMEs com verdadeiros resultados macro
- Considerar remover HDDM_W, Page-Hinkley e ADWIN de benchmarks futuros
