# Cross-Dataset Analysis: Three Options (Session 10 - 2025-12-14)

**Objetivo**: Avaliar robustez de detectores combinando múltiplas dimensões:
1. **Opção 1** - Ceiling performance (máximo atingível com tuning local)
2. **Opção 2** - Parameter portability (capacidade de transferência entre datasets)
3. **Opção 3** - Unified robustness score (combinação de ambas dimensões)

---

## 📊 Resumo Executivo: Três Perspectivas

| Opção | Foco | Melhor Detector | Métrica | Use Case |
|-------|------|------------------|---------|----------|
| **Opção 1** | 🎯 Performance máxima (ceiling) | **FLOSS** | F3=0.4285 | Research, max performance |
| **Opção 2** | 🚀 Portabilidade (transfer) | **ADWIN** | 94.90% retention | Production ready |
| **Opção 3** | ⚖️ Robustez unificada | **FLOSS** | Score=0.9763 | Holistic selection |

### Trade-off Principal

```
FLOSS:    0.4285 ceiling ←──────────┐
                                    │ vs
ADWIN:    0.2879 ceiling ────→ 94.90% transfer

"FLOSS Paradox": melhor performance quando retuned, mas pior portabilidade
```

---

## 📁 Ficheiros Gerados

### Visualização Única (Opções 1, 2 e 3)
- [results/cross_dataset_analysis/option123_summary.png](results/cross_dataset_analysis/option123_summary.png)
- Como gerar: `python -m src.visualize_option123`
- Eixo X: ceiling F3 (Opção 1); Eixo Y: transferability média (Opção 2); cor/tamanho: score unificado (Opção 3)

### Opção 1: Cross-Dataset Generalization
- **CSV**: `cross_dataset_generalization_option1.csv`
  - Columns: detector, mean_cross_fold_f3, median, std_dev, min, max, cv%, avg_gap
  - Agregação: Macro-average de F3 cross-fold de todos os datasets
- **Markdown**: `cross_dataset_generalization_option1.md`
  - Tabela de ranking (6 detectores)
  - Analysis por detector com F3 ceiling e intra-dataset consistency
  - Production guidance

### Opção 2: Parameter Portability
- **CSV**: `parameter_portability_option2.csv`
  - Columns: detector, source_dataset, target_dataset, source_cross_f3, target_transferred_f3, target_local_best_f3, transferability_ratio, performance_drop, performance_drop_pct, interpretation
  - **34 transferências efetivas testadas** (6 detectores × 3 origins × 2 targets = 36 esperadas; page_hinkley falhou em 2 combinações)
- **Markdown**: `parameter_portability_option2.md`
  - Trade-off table (Option 1 vs Option 2)
  - Critical insights (FLOSS paradox, KSWIN sweet spot, ADWIN robustness)
  - 4 production scenarios com F3 esperado e tempo de setup
  - Decision matrix por use case

### Opção 3: Unified Robustness Score
- **CSV**: `unified_robustness_option3.csv`
  - Columns: rank, detector, unified_score, intra_consistency, inter_generalization, ceiling_f3, avg_transferability, cv_transferability
  - Fórmula: `0.6 × (1 - 2fold_gap) + 0.4 × (1 - transfer_variance)`
- **Markdown**: `unified_robustness_option3.md`
  - Final ranking com scores (0 to 1 scale)
  - Top 3 recommendations com breakdown
  - Interpretation guide (o que cada componente mede)
  - Production guidance by score range
  - Comparison of all 3 options

---

## 🎯 Final Ranking por Opção

### Opção 1: Ceiling Performance (com tuning)
```
1. FLOSS       F3 = 0.4285  (50% better than average)
2. KSWIN       F3 = 0.3176
3. Page-Hinkley F3 = 0.3132
4. HDDM_A      F3 = 0.2997
5. ADWIN       F3 = 0.2879
6. HDDM_W      F3 = 0.1527
```

### Opção 2: Parameter Portability (transfer retention)
```
1. ADWIN        94.90% (excellent, zero poor transfers)
2. KSWIN        87.84% (stable, balanced)
3. FLOSS        75.85% (-24% loss vs ceiling!)
4. HDDM_A       65.17%
5. Page-Hinkley 54.31%
6. HDDM_W       45.64%
```

### Opção 3: Unified Robustness Score
```
1. FLOSS        0.9763  (best intra + good inter)
2. ADWIN        0.9713  (excellent inter, poor intra)
3. KSWIN        0.9690  (balanced both)
4. HDDM_A       0.9509
5. HDDM_W       0.9426
6. Page-Hinkley 0.9049
```

---

## 🎯 Recomendações por Cenário

### Cenário 1: Research / Benchmarking
- **Detector**: FLOSS
- **Setup**: Grid search com Parameters otimizados localmente
- **Performance**: F3 ≈ 0.42 (ceiling)
- **Tempo**: Horas (tuning obrigatório)
- **Referência**: Opção 1

### Cenário 2: Production Immediato (sem labels)
- **Detector**: ADWIN
- **Setup**: Use parâmetros pré-tuned (afib_paroxysmal)
- **Performance**: F3 ≈ 0.27 (95% de retention)
- **Tempo**: Minutos (sem tuning)
- **Referência**: Opção 2

### Cenário 3: Production com Validação
- **Detector**: KSWIN
- **Setup**: Parâmetros de afib_paroxysmal + quick validation
- **Performance**: F3 ≈ 0.28 (88% de retention)
- **Tempo**: Minutos + validação rápida
- **Referência**: Opção 3 (melhor trade-off)

### Cenário 4: Dados Heterogêneos
- **Detector**: Ensemble (ADWIN + KSWIN)
- **Setup**: Voting/weighted ensemble
- **Performance**: F3 ≈ 0.30+ (compensate individual weaknesses)
- **Tempo**: Setup ensemble + tuning
- **Referência**: Opções 2 + 3

---

## 🔍 Como Interpretar Cada Métrica

### Opção 1: Mean Cross-Fold F3
- **O que mede**: Melhor performance possível após tuning local
- **Alto (>0.35)**: Detector pode ser muito bom se bem tuned
- **Baixo (<0.25)**: Detector tem limitações fundamentais
- **Uso**: Research, max performance goals

### Opção 2: Transferability Ratio
- **O que mede**: % de performance retained ao transferir params
- **Excellent (>0.95)**: Params completamente portáveis
- **Good (0.85-0.95)**: Alguns ajustes, mas baseline sólido
- **Moderate (0.75-0.84)**: Tuning recomendado
- **Poor (<0.60)**: Avoid sem re-tuning
- **Uso**: Production, quick deployment

### Opção 3: Unified Robustness Score
- **O que mede**: Combinação balanceada de consistência + portabilidade
- **Formula**: 60% intra-dataset + 40% inter-dataset
- **Excellent (0.85-1.0)**: Production-ready
- **Good (0.75-0.84)**: Production-viable com validation
- **Acceptable (0.60-0.74)**: Possível com monitoring
- **Poor (<0.60)**: Research only
- **Uso**: Holistic detector selection

---

## 📚 Scripts Executáveis

### Regenerar Opção 1
```bash
python -m src.aggregate_twofold_analysis
```
Output: `cross_dataset_generalization_option1.{csv,md}`

### Regenerar Opção 2
```bash
python -m src.test_parameter_portability
```
Output: `parameter_portability_option2.{csv,md}`

### Regenerar Opção 3
```bash
python -m src.unified_robustness_score
```
Output: `unified_robustness_option3.{csv,md}`

---

## 🧠 Key Insights

### Insight 1: FLOSS Paradox
- **Ceiling** (Opção 1): F3=0.4285 (🥇 melhor)
- **Portability** (Opção 2): 75.85% (-24% loss vs ceiling)
- **Implicação**: FLOSS nunca deve ser usado em production sem re-tuning
- **Recomendação**: Research-only, ou produção com validation custosa

### Insight 2: KSWIN = Sweet Spot
- **Ceiling**: F3=0.3176 (🥈 2º melhor)
- **Portability**: 87.84% (🥈 2º melhor)
- **CV**: 34% (stable across datasets)
- **Implicação**: Best balance para ambas dimensões
- **Recomendação**: Primeira escolha para production com constraints

### Insight 3: ADWIN Robustness
- **Ceiling**: F3=0.2879 (5º pior)
- **Portability**: 94.90% (🥇 melhor!)
- **Distribution**: 2 Excellent + 3 Good + 1 Acceptable (ZERO poor!)
- **Implicação**: Mais previsível que KSWIN, apesar de menor ceiling
- **Recomendação**: Preferência quando re-tuning impossível

### Insight 4: Parameter Instability
- **Page-Hinkley**: CV=73.7% (muito instável)
- **HDDM_W**: CV=73.2% (idem)
- **ADWIN**: CV=9.5% (excelente estabilidade)
- **Implicação**: Alguns detectores variam muito entre datasets
- **Recomendação**: Avoid production sem extended testing

---

## 🔗 Referência Rápida

| Pergunta | Resposta | Documento |
|----------|----------|-----------|
| Qual é o melhor desempenho teórico? | FLOSS (F3=0.4285) | Option 1 |
| Qual posso usar hoje sem tuning? | ADWIN (94.90% retention) | Option 2 |
| Qual é o melhor equilíbrio? | KSWIN (0.9690 score) | Option 3 |
| Para dados heterogêneos? | ADWIN + KSWIN ensemble | Opção 2+3 |
| Quantos datasets testaram? | 3 (afib, malign, vtachy) | Todas |
| Qual é a métrica principal? | F3-weighted (recall≥4s) | Evaluation metrics |

---

## 📝 Estrutura de Ficheiros (Completa)

```
results/cross_dataset_analysis/
├── README.md (este ficheiro)
│
├── OPTION 1 (Ceiling Performance)
│   ├── cross_dataset_generalization_option1.csv
│   └── cross_dataset_generalization_option1.md
│
├── OPTION 2 (Parameter Portability)
│   ├── parameter_portability_option2.csv
│   └── parameter_portability_option2.md
│
├── OPTION 3 (Unified Robustness)
│   ├── unified_robustness_option3.csv
│   └── unified_robustness_option3.md
│
├── 2-FOLD DATA (Supporting)
│   ├── cross_dataset_generalization_option1.csv (source for Option 1)
│   └── twofold_robustness_*.csv (3 files)
│
├── SUPPORTING (Current)
│   ├── CROSS_DATASET_ANALYSIS_SUMMARY.md
│
├── LEGACY/ARCHIVE
│   ├── ANALYSIS_RANKING_DISCREPANCIES.md
│   ├── AGGREGATION_METHODS_COMPARISON.md
│   └── <detector>/ (6 dirs with per-detector analysis)
```

---

## 🚀 Próximos Passos (Sugerido)

1. **Validar achados**: Compare com cardiologist/ECG domain expert
2. **Escolher detector**: Baseado no cenário (research vs production)
3. **Implementar pipeline**: Use detector selecionado em produção
4. **Monitor performance**: Track F3 real vs expected
5. **Iterate**: Re-tune se performance divergir significativamente

---

**Gerado**: Session 10, 2025-12-14
**Tools**: `aggregate_twofold_analysis.py`, `test_parameter_portability.py`, `unified_robustness_score.py`
