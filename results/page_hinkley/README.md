# Resultados do Detector Page-Hinkley

**Status**: 🔄 A implementar

Esta pasta conterá os resultados da avaliação do detector **Page-Hinkley** no dataset afib_regimes.

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
    --data data/afib_paroxysmal_tidy.csv \
    --detector page_hinkley \
    --output results/page_hinkley/predictions_intermediate.csv \
    --param lambda_=10 lambda_=20 lambda_=30 lambda_=40 lambda_=50 \
    --param delta=0.005 delta=0.01 delta=0.02 delta=0.03 \
    --param alpha=0.9999 alpha=0.999 alpha=0.99 \
    --ma-window 10 30 50 100 200 300 500 \
    --min-gap 500 1000 1500 2000 2500 3000 4000 5000 7500 10000
```

### 2. Avaliar Métricas
```bash
python -m src.evaluate_predictions \
    --predictions results/page_hinkley/predictions_intermediate.csv \
    --metrics-output results/page_hinkley/metrics_comprehensive_with_nab.csv \
    --report-output results/page_hinkley/final_report_with_nab.json
```

### 3. Gerar Visualizações
```bash
python -m src.visualize_results \
    --metrics results/page_hinkley/metrics_comprehensive_with_nab.csv \
    --output-dir results/page_hinkley/visualizations
```

## Grid Search Sugerido

```python
LAMBDA_VALUES = [10, 20, 30, 40, 50]           # Magnitude de mudança
DELTA_VALUES = [0.005, 0.01, 0.02, 0.03]       # Tolerância
ALPHA_VALUES = [0.9999, 0.999, 0.99]           # Forgetting factor
MA_WINDOW_VALUES = [10, 30, 50, 100, 200, 300, 500]
MIN_GAP_VALUES = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 7500, 10000]
```

**Total**: 5 × 4 × 3 × 7 × 10 = 4,200 combinações

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

## Próximos Passos

- [ ] Implementar grid search completo
- [ ] Analisar sensibilidade aos parâmetros
- [ ] Comparar com resultados ADWIN
- [ ] Testar em diferentes classes (paroxysmal/persistent/non-afib)

---

**Criado**: 2025-11-13
**Status**: Pendente implementação
