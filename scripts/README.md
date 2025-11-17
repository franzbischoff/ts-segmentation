# Scripts de Grid Search - Detectores de Drift

Este diretório contém scripts automatizados para executar grid search completo em todos os detectores de drift implementados.

## 📋 Scripts Disponíveis

### 1. **generate_page_hinkley.sh** 📊 MÉDIO
**Detector**: Page-Hinkley (Cumulative Sum Test)
**Combinações**: 384 (grid moderado)
**Tempo estimado**: ~29 minutos (229 ficheiros)
**Prioridade**: ⭐ Média

```bash
./generate_page_hinkley.sh
```

**Configuração** (grid moderado - reduzido de 9,408):
- `lambda_`: [10, 30, 50, 80] (4 valores)
- `delta`: [0.005, 0.01, 0.02, 0.04] (4 valores)
- `alpha`: [0.9999, 0.99] (2 valores)
- `ma_window`: [10, 50, 200] (3 valores)
- `min_gap_samples`: [500, 1000, 2000, 4000] (4 valores)

**Características**:
- Teste de soma cumulativa
- Menos falsos positivos (3.08/min na validação)
- Recall moderado (32.76%)

---

### 2. **generate_kswin.sh** 📊 MÉDIO-LENTO
**Detector**: KSWIN (Kolmogorov-Smirnov Windowing)
**Combinações**: 1,280
**Tempo estimado**: ~90 minutos / 1.5 horas (229 ficheiros)
**Prioridade**: ⭐ Média - 100% Recall@10s

```bash
./generate_kswin.sh
```

**Configuração**:
- `alpha`: [0.001, 0.005, 0.01, 0.05] (4 valores) - nível de significância
- `window_size`: [50, 100, 200, 500] (4 valores) - janela de referência
- `stat_size`: [20, 30, 50, 100] (4 valores) - janela estatística
- `ma_window`: [1, 10, 50, 100] (4 valores)
- `min_gap_samples`: [500, 1000, 2000, 3000, 5000] (5 valores)

**Características**:
- Teste estatístico K-S rigoroso
- Trabalha com valores contínuos
- 100% Recall@10s mas mais FP (10.65/min)

---

### 3. **generate_hddm_a.sh** 📊 MÉDIO
**Detector**: HDDM_A (Hoeffding Drift Detection - Average)
**Combinações**: 640
**Tempo estimado**: ~60 minutos / 1 hora (229 ficheiros)
**Prioridade**: 📊 Baixa - Performance moderada

```bash
./generate_hddm_a.sh
```

**Configuração**:
- `drift_confidence`: [0.0001, 0.0005, 0.001, 0.005] (4 valores)
- `warning_confidence`: [0.001, 0.005, 0.01, 0.05] (4 valores)
- `two_side_option`: [True, False] (2 valores)
- `ma_window`: [1, 10, 50, 100] (4 valores)
- `min_gap_samples`: [500, 1000, 2000, 3000, 5000] (5 valores)

**Características**:
- Bounds de Hoeffding baseados em média
- F3: 0.2967 na validação
- Recall@10s: 48.57%

---

### 4. **generate_hddm_w.sh** 🐌 LENTO
**Detector**: HDDM_W (Hoeffding Drift Detection - Weighted)
**Combinações**: 2,560
**Tempo estimado**: ~180 minutos / 3 horas (229 ficheiros)
**Prioridade**: 🔥 Alta - Segundo melhor F3 (0.5342)

```bash
./generate_hddm_w.sh
```

**Configuração**:
- `drift_confidence`: [0.0001, 0.0005, 0.001, 0.005] (4 valores)
- `warning_confidence`: [0.001, 0.005, 0.01, 0.05] (4 valores)
- `lambda_option`: [0.01, 0.05, 0.1, 0.2] (4 valores) - fator de ponderação
- `two_side_option`: [True, False] (2 valores)
- `ma_window`: [1, 10, 50, 100] (4 valores)
- `min_gap_samples`: [500, 1000, 2000, 3000, 5000] (5 valores)

**Características**:
- Média móvel ponderada
- Melhor para streams não-estacionários
- F3: 0.5342, Recall@10s: 74.29%
- EDD rápido: 1.73s

---

### 5. **extend_min_gap_grid.sh** 🔧 ESPECÍFICO ADWIN
**Detector**: ADWIN (extensão)
**Combinações**: 594 (novas)
**Tempo estimado**: ~53 minutos (229 ficheiros)
**Prioridade**: ⏳ Em execução (tmux)

```bash
./extend_min_gap_grid.sh
```

**Funcionalidade**:
- **Modo APPEND**: Adiciona novas combinações sem recalcular existentes
- Testa `min_gap_samples`: [100, 200, 300, 400, 500, 750]
- Baseado em análise de sensibilidade (`parameter_sensitivity.png`)
- Cria backup automático antes de modificar

---

## 📊 Resumo Comparativo

| Script | Detector | Combinações | Tempo | F3 (validação) | Recall@10s | Prioridade |
|--------|----------|-------------|-------|----------------|------------|------------|
| `generate_hddm_w.sh` | HDDM_W | 2,560 | ~180 min | 0.5342 🏆 | 74.29% | 🔥 Alta |
| `generate_kswin.sh` | KSWIN | 1,280 | ~90 min | 0.5035 | **100%** 🏆 | 🔥 Alta |
| `generate_page_hinkley.sh` | Page-Hinkley | 384 | ~29 min | 0.1629 | 32.76% | ⭐ Média |
| `generate_hddm_a.sh` | HDDM_A | 640 | ~60 min | 0.2967 | 48.57% | 📊 Baixa |
| `extend_min_gap_grid.sh` | ADWIN | 594 | ~53 min | - | - | ⏳ Rodando |

**Tempo Total**: ~412 minutos (~6.9 horas)

**Nota**: DDM e EDDM foram removidos por serem inadequados para análise de séries temporais (projetados para classificação binária).

---

## 🚀 Ordem Recomendada de Execução

### Fase 1: Rápido (~29 min)
```bash
./generate_page_hinkley.sh  # 29 min - Grid moderado, menos FP
```

### Fase 2: Médios (~150 min)
```bash
./generate_kswin.sh         # 90 min - 100% Recall
./generate_hddm_a.sh        # 60 min - Performance moderada
```

### Fase 3: Lento (~180 min)
```bash
./generate_hddm_w.sh   # 180 min - Melhor F3 (0.5342)
```

### Fase 4: ADWIN (aguardar término)
```bash
# ADWIN extension já rodando em tmux
# Aguardar conclusão para re-avaliar
```

---

## 📝 Workflow Padrão

Para cada detector, após executar o script de geração:

### 1. Avaliar Predições
```bash
python -m src.evaluate_predictions \
    --predictions results/<detector>/predictions_intermediate.csv \
    --metrics-output results/<detector>/metrics_comprehensive_with_nab.csv \
    --report-output results/<detector>/final_report_with_nab.json
```

### 2. Gerar Visualizações
```bash
python -m src.visualize_results \
    --metrics results/<detector>/metrics_comprehensive_with_nab.csv \
    --output-dir results/<detector>/visualizations
```

### 3. Comparar Detectores
```bash
python -m src.compare_detectors \
    --detectors <detector1> <detector2> <detector3> \
    --output results/comparisons/<nome_comparacao>.md
```

---

## ⚙️ Configuração Comum

Todos os scripts usam:
- **Dataset**: `data/afib_paroxysmal_full.csv` (229 ficheiros)
- **Paralelização**: `--n-jobs 20` (todos os cores disponíveis)
- **Output**: `results/<detector>/predictions_intermediate.csv`
- **Confirmação**: Prompt interativo antes de iniciar
- **Instruções**: Next steps após conclusão

---

## 🔍 Detalhes Técnicos

### Observação: DDM/EDDM removidos
DDM e EDDM foram removidos do fluxo de trabalho por serem apropriados para concept drift em streams de labels (classificação binária) e não para análise de valores contínuos em séries temporais. Caso alguém entenda a sua utilidade no futuro, manter a conversão binária em um branch separado é uma opção.

### Parâmetros Comuns
- **ma_window**: Suavização do sinal (média móvel)
- **min_gap_samples**: Gap mínimo entre detecções consecutivas
-- **use_derivative**: Usar primeira derivada do sinal (apenas para detectores que precisem explicitamente, atualmente não usado por DDM/EDDM no pipeline principal)

### Resultados da Validação (5 ficheiros)
**Nota**: Os resultados de DDM/EDDM figuram no histórico do projeto, mas tais detectores foram removidos do fluxo ativo por serem inadequados para time series contínuas. Os detectores atualmente em uso são: ADWIN, Page-Hinkley, KSWIN, HDDM_A e HDDM_W.
- **HDDM_W**: F3=0.5342, EDD=1.73s, FP/min=3.84
- **KSWIN**: Recall@10s=100%, mas FP/min=10.65
- **Page-Hinkley**: FP/min=3.08 (melhor), mas Recall@10s=32.76%
- **HDDM_A**: Performance moderada em todas as métricas

---

## 📚 Referências

- **Pipeline Completo**: Consultar `README.md` na raiz do projeto
- **Métricas**: Ver `docs/evaluation_metrics_v1.md`
- **Visualizações**: Ver `docs/visualizations_guide.md`
- **Código**: `src/generate_predictions.py`, `src/evaluate_predictions.py`

---

## 🆘 Troubleshooting

### Erro: "Data file not found"
```bash
# Verificar se dataset existe
ls -lh data/afib_paroxysmal_full.csv
```

### Erro: "ModuleNotFoundError"
```bash
# Ativar ambiente virtual
source .venv/bin/activate
```

### Processo interrompido
Todos os scripts salvam resultados incrementalmente. Se interrompido, o arquivo parcial estará disponível em `results/<detector>/predictions_intermediate.csv`.

### Monitorar progresso
```bash
# Verificar tamanho do arquivo de output
watch -n 10 "wc -l results/<detector>/predictions_intermediate.csv"

# Verificar últimas linhas do log (se usando tee)
tail -f results/<detector>/grid_execution.log
```

---

**Última atualização**: 2025-11-13
**Framework**: Multi-detector drift detection (7 detectores implementados)
**Status**: Todos os scripts prontos para produção ✅
