# Resultados do Detector DDM

**Status**: 🔄 A implementar

Esta pasta conterá os resultados da avaliação do detector **DDM (Drift Detection Method)** no dataset afib_regimes.

## Detector: DDM

**Algoritmo**: DDM (Drift Detection Method)
**Biblioteca**: scikit-multiflow
**Princípio**: Monitora mudanças na taxa de erro usando conceitos de controle estatístico

**Adaptação para ECG**:
- Usar derivada ou valor absoluto como "erro"
- Threshold baseado em desvio do valor médio

**Parâmetros principais**:
- `out_control_level`: Nível para declarar drift (padrão: 3.0)
- `warning_level`: Nível de alerta (padrão: 2.0)

## Como Executar

### 1. Gerar Predições
```bash
python -m src.generate_predictions \
    --data data/afib_paroxysmal_tidy.csv \
    --detector ddm \
    --output results/ddm/predictions_intermediate.csv \
    --param out_control_level=2.0 out_control_level=2.5 out_control_level=3.0 out_control_level=3.5 \
    --param warning_level=1.5 warning_level=2.0 warning_level=2.5 \
    --ma-window 10 30 50 100 200 300 500 \
    --min-gap 500 1000 1500 2000 2500 3000 4000 5000 7500 10000
```

### 2. Avaliar Métricas
```bash
python -m src.evaluate_predictions \
    --predictions results/ddm/predictions_intermediate.csv \
    --metrics-output results/ddm/metrics_comprehensive_with_nab.csv \
    --report-output results/ddm/final_report_with_nab.json
```

### 3. Gerar Visualizações
```bash
python -m src.visualize_results \
    --metrics results/ddm/metrics_comprehensive_with_nab.csv \
    --output-dir results/ddm/visualizations
```

## Grid Search Sugerido

```python
OUT_CONTROL_LEVELS = [2.0, 2.5, 3.0, 3.5]      # Drift threshold
WARNING_LEVELS = [1.5, 2.0, 2.5]                # Warning threshold
MA_WINDOW_VALUES = [10, 30, 50, 100, 200, 300, 500]
MIN_GAP_VALUES = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 7500, 10000]
```

**Total**: 4 × 3 × 7 × 10 = 840 combinações

## Características Esperadas

### Vantagens do DDM
- ✅ Baseado em conceitos bem estabelecidos (controle estatístico)
- ✅ Warning level permite preparação antecipada
- ✅ Robusto a ruído de curto prazo
- ✅ Bom para mudanças persistentes

### Desvantagens
- ❌ Originalmente para classificação (adaptação necessária)
- ❌ Pode ser lento para detectar mudanças graduais
- ❌ Requer período de warm-up
- ❌ Menos sensível que ADWIN

## Adaptação para Sinais Contínuos

DDM foi projetado para monitorar taxa de erro em classificação. Para ECG:

**Opção 1**: Usar derivada como proxy de "erro"
```python
derivative = np.diff(signal)
feed_to_ddm(abs(derivative))
```

**Opção 2**: Usar diferença da média móvel
```python
error_proxy = abs(signal - moving_average(signal))
feed_to_ddm(error_proxy)
```

**Opção 3**: Z-score em janela deslizante
```python
z_score = (signal - local_mean) / local_std
feed_to_ddm(abs(z_score))
```

## Comparação com ADWIN e Page-Hinkley

| Aspecto | ADWIN | Page-Hinkley | DDM |
|---------|-------|--------------|-----|
| Base teórica | Janelas adaptativas | Teste sequencial | Controle estatístico |
| Warning | ❌ | ❌ | ✅ |
| Memória | O(W) | O(1) | O(1) |
| Velocidade | Moderada | Rápida | Rápida |
| Tipo mudança | Média/Variância | Média | "Erro"/Desvio |
| Originalmente para | Streaming geral | Mudança de processo | Classificação online |

## Próximos Passos

- [ ] Implementar adaptação para sinal contínuo
- [ ] Testar diferentes proxies de "erro"
- [ ] Analisar utilidade do warning level
- [ ] Comparar com ADWIN e Page-Hinkley
- [ ] Avaliar sensibilidade aos parâmetros

## Referência

```
Gama J, Medas P, Castillo G, Rodrigues P.
Learning with drift detection.
Advances in Artificial Intelligence–SBIA 2004.
```

---

**Criado**: 2025-11-13
**Status**: Pendente implementação
