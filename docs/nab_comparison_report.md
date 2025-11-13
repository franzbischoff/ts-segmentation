# Resultados do Grid Search com Métricas NAB
**Data**: 13 de Novembro de 2025
**Dataset**: afib_paroxysmal_full.csv (229 ficheiros)
**Total de Avaliações**: 113,355

---

## Sumário de Avaliação

- **Total de ficheiros**: 229
- **Combinações de parâmetros**: 495
- **Total de avaliações**: 113,355
- **Eventos ground truth**: 643,995
- **Total de detecções**: 6,752,494

---

## Comparação de Melhores Parâmetros por Métrica

### Tabela Comparativa

| Métrica | delta | ma_window | min_gap | Score Médio | Recall@10s | Precision@10s | FP/min | EDD (s) |
|---------|-------|-----------|---------|-------------|------------|---------------|--------|---------|
| **F3-weighted** ⭐ | 0.005 | 300 | 1000 | **0.3994** | 97.77% | 10.20% | 10.00 | 2.64 |
| F1-weighted | 0.005 | 10 | 1000 | 0.1682 | 80.55% | 13.88% | 6.22 | 3.52 |
| F1-classic | 0.015 | 300 | 2000 | 0.2239 | 91.31% | 14.36% | 5.69 | 4.64 |
| F3-classic | 0.100 | 300 | 2000 | 0.2215 | 92.67% | 14.10% | 5.87 | 4.69 |
| **NAB Standard** | 0.050 | 10 | 2000 | **-4.282** | 74.01% | 15.69% | 4.33 | 4.65 |
| **NAB Low FP** | 0.005 | 10 | 5000 | **-3.894** | 34.98% | 24.72% | 1.53 | 6.99 |
| **NAB Low FN** | 0.080 | 100 | 2000 | **-3.384** | 91.19% | 13.93% | 5.78 | 4.66 |

⭐ *Métrica primária de otimização*

---

## Análise Detalhada por Métrica

### 1. F3-Weighted (Métrica Primária)
**Parâmetros Ótimos**: delta=0.005, ma_window=300, min_gap=1000

**Performance**:
- F3-weighted: 0.3994 ± 0.2159
- Recall@10s: **97.77%** (quase todos os eventos detectados)
- Recall@4s: 78.63% (detecção rápida)
- Precision@10s: 10.20%
- EDD mediano: **2.64s** (muito rápido)
- FP/min: 10.00

**Características**:
- ✅ **Máximo recall**: Detecta virtualmente todos os eventos
- ✅ **Latência mínima**: Detecção extremamente rápida (2.64s)
- ✅ **Suavização forte**: ma_window=300 (1.2s @ 250Hz)
- ⚠️ **Alta taxa de FP**: 10 FP/minuto (esperado em streaming)
- ✅ **Min gap baixo**: Permite detecções rápidas consecutivas

**Interpretação**: Esta configuração maximiza a detecção precoce de mudanças, ideal para aplicações onde não perder eventos é crítico.

---

### 2. NAB Standard (Balanced)
**Parâmetros Ótimos**: delta=0.050, ma_window=10, min_gap=2000

**Performance**:
- NAB Score: -4.282 ± 8.540
- F3-weighted: 0.3172 ± 0.1831
- Recall@10s: 74.01%
- Precision@10s: 15.69%
- EDD mediano: 4.65s
- FP/min: **4.33** (mais baixo que F3)

**Características**:
- ✅ **Menor taxa de FP**: 4.33 FP/min vs 10.00 do F3
- ✅ **Melhor precision**: 15.69% vs 10.20%
- ⚠️ **Recall moderado**: 74% vs 97.77% do F3
- ✅ **Suavização mínima**: ma_window=10 preserva detalhes
- ✅ **Min gap alto**: 2000 (8s) filtra redundâncias

**Interpretação**: NAB favorece configurações com menos falsos positivos, mesmo à custa de recall. Score negativo indica que ainda há trabalho de otimização, mas é consistente com a natureza do NAB scoring.

---

### 3. NAB Low FP (Minimize False Positives)
**Parâmetros Ótimos**: delta=0.005, ma_window=10, min_gap=5000

**Performance**:
- NAB Score: -3.894 ± 6.990
- F3-weighted: 0.1815 ± 0.1770
- Recall@10s: **34.98%** (muito baixo!)
- Precision@10s: **24.72%** (muito alto!)
- EDD mediano: 6.99s
- FP/min: **1.53** (extremamente baixo)

**Características**:
- ✅ **Mínimo FP**: Apenas 1.53 FP/minuto
- ✅ **Alta precision**: 24.72% (2.4× melhor que F3)
- ❌ **Recall muito baixo**: Detecta apenas 35% dos eventos
- ✅ **Min gap máximo**: 5000 (20s) evita redundâncias
- ⚠️ **Trade-off extremo**: Sacrifica recall por precision

**Interpretação**: Esta configuração é **adequada apenas para cenários onde alarmes falsos são extremamente custosos** e perder alguns eventos é aceitável. Exemplo: sistemas com operadores humanos que sofrem de fadiga de alarme.

---

### 4. NAB Low FN (Minimize False Negatives)
**Parâmetros Ótimos**: delta=0.080, ma_window=100, min_gap=2000

**Performance**:
- NAB Score: -3.384 ± 8.485 (**melhor NAB score**)
- F3-weighted: 0.3622 ± 0.1744
- Recall@10s: **91.19%**
- Precision@10s: 13.93%
- EDD mediano: 4.66s
- FP/min: 5.78

**Características**:
- ✅ **Alto recall**: 91.19% dos eventos detectados
- ✅ **Balanceado**: Meio-termo entre F3 e NAB Standard
- ✅ **Suavização moderada**: ma_window=100 (0.4s)
- ✅ **Melhor NAB score**: -3.384 é o menos negativo
- ✅ **FP controlado**: 5.78 FP/min é razoável

**Interpretação**: **Melhor compromisso geral** entre recall alto e FP moderado. Adequado para aplicações clínicas onde não perder eventos é importante mas também se quer controlar alarmes.

---

## Top 10 Configurações

### Top 10 por F3-Weighted

| Rank | delta | ma_window | min_gap | F3-weighted |
|------|-------|-----------|---------|-------------|
| 1 | 0.005 | 300 | 1000 | **0.3994** |
| 2 | 0.010 | 300 | 1000 | 0.3993 |
| 3 | 0.015 | 250 | 1000 | 0.3993 |
| 4 | 0.040 | 100 | 1000 | 0.3990 |
| 5 | 0.005 | 75 | 1000 | 0.3983 |
| 6 | 0.050 | 150 | 1000 | 0.3980 |
| 7 | 0.015 | 150 | 1000 | 0.3977 |
| 8 | 0.025 | 200 | 1000 | 0.3977 |
| 9 | 0.025 | 300 | 1000 | 0.3976 |
| 10 | 0.015 | 200 | 1000 | 0.3975 |

**Padrão**: 100% usam min_gap=1000, ma_window alto (75-300)

### Top 10 por NAB Standard

| Rank | delta | ma_window | min_gap | NAB Score |
|------|-------|-----------|---------|-----------|
| 1 | 0.050 | 10 | 2000 | **-4.282** |
| 2 | 0.025 | 10 | 2000 | -4.285 |
| 3 | 0.040 | 10 | 2000 | -4.298 |
| 4 | 0.005 | 10 | 2000 | -4.322 |
| 5 | 0.080 | 25 | 2000 | -4.327 |
| 6 | 0.010 | 25 | 2000 | -4.334 |
| 7 | 0.100 | 25 | 2000 | -4.342 |
| 8 | 0.005 | 25 | 2000 | -4.347 |
| 9 | 0.080 | 10 | 2000 | -4.350 |
| 10 | 0.020 | 10 | 2000 | -4.357 |

**Padrão**: 100% usam min_gap=2000, ma_window baixo (10-25)

---

## Insights e Padrões Observados

### 1. **Trade-off Fundamental: Recall vs Precision**

```
F3-weighted:    Recall↑↑ (97.77%)  Precision↓ (10.20%)  FP↑↑ (10.00/min)
NAB Standard:   Recall↓  (74.01%)  Precision↑ (15.69%)  FP↓  (4.33/min)
NAB Low FP:     Recall↓↓ (34.98%)  Precision↑↑ (24.72%) FP↓↓ (1.53/min)
NAB Low FN:     Recall↑  (91.19%)  Precision~ (13.93%)  FP~  (5.78/min)
```

### 2. **Efeito dos Parâmetros**

#### min_gap_samples:
- **1000 (4s)**: Favorecido por F3-weighted → Máximo recall
- **2000 (8s)**: Favorecido por NAB → Balanceamento
- **5000 (20s)**: Favorecido por NAB Low FP → Mínimo FP

#### ma_window:
- **10-25**: Favorecido por NAB → Preserva detalhes, mais FPs detectados como distintos
- **75-300**: Favorecido por F3 → Suavização forte, reduz FP por fusão

#### delta:
- **0.005-0.015**: Sensibilidade alta → Mais detecções
- **0.025-0.050**: Sensibilidade moderada → Balanceamento NAB
- **0.080-0.100**: Sensibilidade baixa → Menos FP

### 3. **Interpretação dos Scores NAB Negativos**

Os scores NAB negativos (-3 a -9) indicam que:
- O detector ainda gera mais penalidades (FP + FN) do que recompensas (TP precoces)
- Isto é **normal** para detecção streaming em dados ruidosos
- O foco deve ser na **comparação relativa** entre configurações
- Scores NAB são mais úteis para ranking do que valor absoluto

### 4. **Convergência nas Configurações**

**F3-weighted** converge para:
- min_gap = 1000 (unanimidade no top 10)
- ma_window alto (suavização forte)
- delta variável (menos crítico)

**NAB** converge para:
- min_gap = 2000 (unanimidade no top 10)
- ma_window baixo (menos suavização)
- delta moderado

Isto sugere que **F3 e NAB otimizam objetivos diferentes**:
- **F3**: Maximizar recall com latência baixa
- **NAB**: Balancear TP precoces com penalidade de FP

---

## Recomendações de Uso

### Quando usar F3-weighted (delta=0.005, ma=300, gap=1000)?
✅ **Aplicações clínicas críticas**
- Não pode perder nenhuma mudança de regime
- Recall de 97.77% é essencial
- Operadores podem lidar com 10 FP/minuto
- Exemplos: UCI, monitorização contínua de alto risco

### Quando usar NAB Standard (delta=0.050, ma=10, gap=2000)?
✅ **Comparação com literatura**
- Publicar resultados comparáveis com NAB benchmark
- Avaliação balanceada padrão
- FP moderado (4.33/min) é aceitável

### Quando usar NAB Low FP (delta=0.005, ma=10, gap=5000)?
✅ **Ambientes com fadiga de alarme**
- Apenas 1.53 FP/minuto
- Precision de 24.72%
- ⚠️ **Atenção**: Recall baixo (35%) - aceitável apenas se perder eventos é tolerável
- Exemplos: Enfermaria com poucos enfermeiros, alarmes que requerem ação física

### Quando usar NAB Low FN (delta=0.080, ma=100, gap=2000)?
✅ **Melhor compromisso geral** ⭐
- Recall alto (91.19%)
- FP controlado (5.78/min)
- **Recomendado** para maioria das aplicações clínicas
- Equilíbrio entre não perder eventos e não sobrecarregar operadores

---

## Conclusões

1. **F3-weighted permanece como métrica primária** para otimização quando recall é prioritário

2. **NAB Low FN oferece melhor equilíbrio** para aplicações práticas (score -3.384, recall 91%)

3. **NAB Standard é útil** para comparação com literatura (-4.282, FP controlado)

4. **NAB Low FP é muito conservador** (recall 35%) - usar apenas em cenários específicos

5. **Padrões convergentes**:
   - F3 → min_gap baixo + ma alto
   - NAB → min_gap alto + ma baixo

6. **Trade-off inevitável**: Streaming sempre terá FP elevados; escolha depende da aplicação

---

## Próximos Passos

1. ✅ Analisar distribuição de scores por paciente
2. ✅ Identificar casos extremos (F3 muito baixo/alto)
3. ✅ Gerar visualizações (curvas ROC, PR)
4. ✅ Validação em dataset holdout
5. ✅ Comparação com baseline clínico

---

**Gerado em**: 13 de Novembro de 2025
**Pipeline**: generate_predictions.py → evaluate_predictions.py
**Métricas**: F1/F3 Classic + F1*/F3* Weighted + NAB (Standard, Low FP, Low FN)
