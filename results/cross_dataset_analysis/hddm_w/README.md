# Análise Cross-Dataset: HDDM_W - Resultados

**Data**: 2025-11-24
**Método**: Macro-Average (média simples entre datasets)
**Datasets**: afib_paroxysmal, malignantventricular, vtachyarrhythmias

---

## Melhor Configuração Cross-Dataset

Parâmetros que **generalizam melhor** através dos 3 datasets:

```yaml
drift_confidence:    0.005
warning_confidence:  0.001
lambda_option:       0.2
two_side_option:     True
ma_window:           1
min_gap_samples:     1000

F3-weighted macro-average = 0.2843 (±0.2567)
```

**Ranking Geral**: **6º lugar** (último) entre 6 detectores (-21.7% vs ADWIN, -36.7% vs FLOSS)
**Robustez**: **#6 pior** (maior std entre todos os detectores)

---

## ⚠️ Análise: Por Que HDDM_W Fica em Último?

### Comparação com HDDM_A (irmão)

| Métrica | HDDM_W | HDDM_A | Delta |
|---------|--------|--------|-------|
| **Score** | 0.2843 | 0.3273 | -13.1% ❌ |
| **Std** | 0.2567 | 0.1944 | +32.0% ❌ |
| **Configs** | 2,560 | 640 | +300% |
| **Lambda** | 0.2 (weighted) | N/A (average) | - |

**Veredito**: HDDM_W (weighted) é **pior em tudo** comparado ao HDDM_A (average):
- ❌ Performa -13% pior
- ❌ 32% MENOS robusto (std=0.26 vs 0.19)
- ❌ Testou 4× mais configs mas não melhorou

---

## 📈 Top 5 Configurações Rankeadas

### Macro-Average Rankings

1-5. **drift=0.005, warn=varied, λ=0.2, two_side=True/False, ma=1, gap=1000** → 0.2843 (±0.2567)

**Observação**: As top-5 configs têm **EXATAMENTE o mesmo score e std**!

Isto indica que com `drift=0.005` e `λ=0.2`:
- `warning_confidence` tem impacto ZERO
- `two_side_option` tem impacto ZERO

### Insights

- **drift_confidence=0.005** fixo no top-10
- **lambda=0.2** consistente (peso recente médio)
- **warning_confidence IRRELEVANTE** (igual ao HDDM_A)
- **two_side IRRELEVANTE** (surpreendente!)
- **ma_window=1** universal (sem smoothing)
- **gap=1000** universal

---

## 🎯 Características do HDDM_W

### Algoritmo
Hoeffding's Drift Detection Method - Weighted:
- Variante do HDDM_A com pesos exponenciais
- Lambda (λ) controla decay: valores recentes têm mais peso
- Teoricamente mais sensível a mudanças recentes

### Parâmetros Ótimos (?)

| Parâmetro | Valor | Significado |
|-----------|-------|-------------|
| **drift_confidence** | 0.005 | Threshold de confiança para drift |
| **warning_confidence** | 0.001 | ⚠️ SEM EFEITO |
| **lambda_option** | 0.2 | Peso exponencial (menor = mais peso no passado) |
| **two_side_option** | True | ⚠️ SEM EFEITO |
| **ma_window** | 1 | Sem smoothing |
| **min_gap** | 1000 | 4s mínimo entre detecções |

### Problemas Identificados
❌ **Performance inferior**: 6º/6 em score (0.2843)
❌ **Pior robustez**: 6º/6 em std (0.2567 - maior variação)
❌ **Weighted não ajuda**: λ=0.2 pior que HDDM_A average
❌ **Parâmetros inúteis**: warning_confidence E two_side_option sem impacto
❌ **Espaço de busca desperdiçado**: 2,560 configs vs 640 do HDDM_A, zero ganho

---

## 💡 Recomendações de Uso

### Quando Usar HDDM_W Cross-Dataset

❌ **NUNCA** - Use HDDM_A em seu lugar (sempre superior)

### Por Que NÃO Usar

❌ **HDDM_A é melhor**: +13% performance, +32% robustez
❌ **Todos outros são melhores**: Até o 5º (HDDM_A) supera facilmente
❌ **Weighted backfires**: Pesos exponenciais pioram performance
❌ **Complexidade desnecessária**: Mais parâmetros, pior resultado

### Alternativas Superiores

1. **HDDM_A** - Irmão superior (+13% score, std=0.19)
2. **ADWIN** - +27.6% score, robustez similar
3. **KSWIN** - +32.7% score, robustez equivalente
4. **Page-Hinkley** - +36.7% score
5. **FLOSS** - +58.0% score (quase 2× melhor!)

---

## 🔬 Análise Técnica: O Que Deu Errado?

### Hipóteses

**1. Weighted decay inadequado para ECG**:
- λ=0.2 pode ignorar padrões de longo prazo necessários
- Mudanças de regime cardíaco têm assinaturas complexas
- HDDM_A (average sem decay) captura melhor

**2. Overfitting ao ruído recente**:
- Pesos exponenciais amplificam ruído local
- ECG tem alta variabilidade beat-to-beat
- Average suaviza melhor

**3. Parâmetros mal calibrados**:
- λ=0.2 pode ser subótimo
- Mas grid search testou 2,560 configs e nenhum foi bom!

### Comparação λ values (hipotética)

Grid testou λ ∈ {0.05, 0.1, 0.2, 0.5}, mas **TODOS** convergiram para λ=0.2 no top-10. Isso sugere que **weighted HDDM é fundamentalmente inadequado** para este problema.

---

## 📊 Performance Detalhada

### vs Outros Detectores (Cross-Dataset)

```
FLOSS:         0.4491 ██████████████████████ (+58.0% vs HDDM_W)
Page-Hinkley:  0.3885 ████████████████ (+36.7%)
KSWIN:         0.3773 ███████████████ (+32.7%)
ADWIN:         0.3629 ██████████████ (+27.6%)
HDDM_A:        0.3273 ████████████ (+15.1%)
HDDM_W:        0.2843 ██████████ (baseline - ÚLTIMO)
```

**HDDM_W é 15-58% PIOR** que todos os outros detectores!

### Robustez (std) vs Outros

```
HDDM_A:        0.1944 ████████████████ (MELHOR - baseline)
KSWIN:         0.2114 █████████████████ (+8.7%)
Page-Hinkley:  0.2117 █████████████████ (+8.9%)
ADWIN:         0.2145 ██████████████████ (+10.3%)
FLOSS:         0.2244 ██████████████████ (+15.4%)
HDDM_W:        0.2567 ████████████████████ (+32.1% - PIOR)
```

**HDDM_W tem a MAIOR variabilidade** (menos robusto) entre todos!

---

## 📁 Outputs Gerados

- `macro_average_rankings.csv` - 2,560 configs rankeadas (179 KB - maior!)
- `cross_dataset_report.json` - Top 10 + estatísticas (4.1 KB)
- `README.md` - Este ficheiro (post-mortem analysis)

### Estatísticas Gerais

- **Total de configurações**: 2,560 únicas (4× mais que HDDM_A!)
- **Datasets analisados**: 3
- **Total de linhas processadas**: 729,600 (maior volume)
- **Resultado**: PIOR detector mesmo com mais busca 😞

---

## 🎓 Lições Aprendidas

1. **Mais parâmetros ≠ melhor**: HDDM_W testou 4× mais configs, ficou em último
2. **Weighted pode backfire**: Pesos exponenciais nem sempre melhoram
3. **Average vence weighted**: HDDM_A simpler is better
4. **Domain matters**: Weighted pode funcionar em outros domínios, mas não em ECG
5. **Occam's Razor**: Simplicidade (HDDM_A) supera complexidade (HDDM_W)

---

## 📈 Próximos Passos (Não Recomendados)

1. ❌ ~~Testar outras configs HDDM_W~~ - Use HDDM_A em vez
2. ❌ ~~Refinar λ~~ - Fundamentalmente inadequado
3. ❌ ~~Grid search mais fino~~ - Já testamos 2,560 configs
4. ✅ **RECOMENDAÇÃO**: Remove HDDM_W dos pipelines futuros, mantenha HDDM_A

---

## 🚫 Conclusão: EVITE HDDM_W

HDDM_W é o **PIOR detector** cross-dataset com score 0.2843 (último lugar) e std=0.2567 (pior robustez). O esquema de pesos exponenciais (λ=0.2) **PIORA** a performance comparado ao HDDM_A (average simples).

### Recomendação Final

**NUNCA use HDDM_W**. Em todas as situações, HDDM_A (irmão simpler) é superior:
- +15% score
- +32% robustez
- Menos parâmetros
- Mais rápido

Se precisa de performance superior, use FLOSS, Page-Hinkley ou KSWIN.
Se precisa de robustez máxima, use HDDM_A.
**HDDM_W não tem caso de uso válido neste projeto.**

---

**Status**: ⛔ **DEPRECATED** - Considere remover de futuros benchmarks para economizar tempo computacional.
