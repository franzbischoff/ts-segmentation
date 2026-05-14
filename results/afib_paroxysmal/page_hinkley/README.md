# Resultados do Detector Page-Hinkley

**Status**: ✅ COMPLETO (Novembro 2025)

Esta pasta contém os resultados da avaliação do detector **Page-Hinkley** no dataset afib_paroxysmal.

## Detector: Page-Hinkley

**Algoritmo**: Page-Hinkley Test
**Biblioteca**: scikit-multiflow
**Princípio**: Teste sequencial para detectar mudança de média acumulativa

**Parâmetros principais**:
- `lambda_`: Threshold de detecção (magnitude de mudança)
- `delta`: Permissividade (tolerância a flutuações)
- `alpha`: Forgetting factor (peso de observações antigas)

## Como Executar

### 1. Gerar Predições
```bash
python -m src.generate_predictions \
    --data data/afib_paroxysmal_full.csv \
    --detector page_hinkley \
    --output results/afib_paroxysmal/page_hinkley/predictions_intermediate.csv \
    --lambda 1 10 30 50 80 \
    --ph-delta 0.001 0.005 0.01 0.02 0.04 \
    --alpha 0.9999 0.99 \
    --ma-window 10 50 200 \
    --min-gap 500 1000 2000 4000
```

### 2. Avaliar Métricas
```bash
python -m src.evaluate_predictions \
    --predictions results/afib_paroxysmal/page_hinkley/predictions_intermediate.csv \
    --metrics-output results/afib_paroxysmal/page_hinkley/metrics_comprehensive_with_nab.csv \
    --report-output results/afib_paroxysmal/page_hinkley/final_report_with_nab.json
```

### 3. Gerar Visualizações
```bash
python -m src.visualize_results \
    --metrics results/afib_paroxysmal/page_hinkley/metrics_comprehensive_with_nab.csv \
    --output-dir results/afib_paroxysmal/page_hinkley/visualizations
```

## Grid Search Executado

```python
LAMBDA_VALUES = [1, 10, 30, 50, 80]            # Magnitude de mudança
DELTA_VALUES = [0.001, 0.005, 0.01, 0.02, 0.04] # Tolerância
ALPHA_VALUES = [0.9999, 0.99]                  # Forgetting factor
MA_WINDOW_VALUES = [10, 50, 200]
MIN_GAP_VALUES = [500, 1000, 2000, 4000]
```

**Total**: 5 × 5 × 2 × 3 × 4 = 600 combinações

> Nota: O valor `MIN_GAP_VALUES` corresponde ao parâmetro `min_gap_samples`, que é
> aplicado como filtro de pós-processamento pela pipeline (`src/streaming_detector.py`)
> e não faz parte do detector Page-Hinkley. Use estes valores para a avaliação onde
> as detecções brutas são suprimidas se estiverem demasiado próximas.

## Características Esperadas

### Vantagens do Page-Hinkley
- ✅ Rápido (baixa complexidade computacional)
- ✅ Memória constante
- ✅ Bom para mudanças abruptas de média
- ✅ Parâmetros intuitivos

### Desvantagens
- ❌ Sensível a scaling do sinal
- ❌ Pode não detectar mudanças graduais
- ❌ Requer normalização adequada
- ❌ Focado apenas em mudanças de média (não variância)

## Comparação com ADWIN

| Aspecto | ADWIN | Page-Hinkley |
|---------|-------|--------------|
| Janela | Adaptativa | Acumulativa |
| Memória | O(W) | O(1) |
| Velocidade | Moderada | Rápida |
| Tipo mudança | Média/Variância | Média |
| Parâmetros | 1 (delta) | 3 (lambda, delta, alpha) |

## Estado de Execução

- ✅ Grid search executado e integrado na pipeline
- ✅ Métricas e visualizações geradas em `results/afib_paroxysmal/page_hinkley/`
- ✅ Comparações por dataset disponíveis em `comparisons/afib_paroxysmal/`

---

**Criado**: 2025-11-13
**Última atualização**: 2026-05-12
**Status**: Análise completa integrada na pipeline
