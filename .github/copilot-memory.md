# Projeto: Streaming ECG Regime Change Detection (Sessão de Trabalho - Memória Persistent- **Predições geradas**: `results/adwin/predi2. **Avaliar Métricas**: `python -m src.evaluate_predictions --predictions results/<detector>/predictions_intermediate.csv`
3. **Visualizar**: `python -m src.visualize_results --metrics results/<detector>/metrics_comprehensive_with_nab.csv`

#### Comparação entre Detectores
- **Script criado**: `src/compare_detectors.py`
- **Outputs**: Relatório markdown + CSV de rankings
**Uso**: `python -m src.compare_detectors --detectors adwin page_hinkley kswin hddm_a hddm_w`

#### Grid Search Incremental
- **`src/generate_predictions.py`**: Modo incremental implementado
  - Parâmetro `--append`: carrega predições existentes e gera apenas novas combinações
  - Parâmetros customizados para todos os detectores
  - Merge automático de resultados antigos + novos
  - Backup automático antes de modificar

## 3. Componentes Implementados

### Core Detection System (7 Detectores)ediate.csv` (126 MB)
- **Métricas calculadas**: `results/adwin/metrics_comprehensive_with_nab.csv` (33 MB)
- **Relatório final**: `results/adwin/final_report_with_nab.json` (12 KB)
- **Visualizações**: 9 gráficos PNG em `results/adwin/visualizations/` (4.3 MB)

**Melhores Configurações ADWIN**:
- **F3-weighted**: delta=0.005, ma_window=300, min_gap=1000 → Score: 0.3994, Recall@10s: 97.77%, FP/min: 10.00
- **NAB Standard**: delta=0.050, ma_window=10, min_gap=2000 → Score: -4.2820, Recall@10s: 74.01%
- **NAB Low FN**: delta=0.080, ma_window=100, min_gap=2000 → Score: -3.3841, Recall@10s: 91.19%
- **NAB Low FP**: delta=0.005, ma_window=10, min_gap=5000 → Score: -7.0183, Recall@10s: 34.98%

### 🔄 EM PROGRESSO: Extensão Grid ADWIN
- **Motivação**: Gráfico `parameter_sensitivity.png` mostra potencial de melhora em min_gap < 1000
- **Status**: Rodando em background (tmux)
- **Novas combinações**: 594 (11 deltas × 9 ma_windows × 6 min_gaps: 100, 200, 300, 400, 500, 750)
- **Tempo estimado**: ~53 min
- **Após completar**: Re-avaliar métricas + re-gerar visualizações

### ⏳ PRÓXIMOS PASSOS: Grid Searches de Produção

#### Ordem Recomendada (2 Fases)
**Fase 1 - Rápida (~29 min)**:
- `./scripts/generate_page_hinkley.sh` - 384 combos, ~29 min

**Fase 2 - Média-Lenta (~240 min)**:
- `./scripts/generate_kswin.sh` - 1,280 combos, ~90 min
- `./scripts/generate_hddm_a.sh` - 640 combos, ~60 min
- `./scripts/generate_hddm_w.sh` - 2,560 combos, ~180 min

Após cada grid search, executar pipeline completo:
1. Avaliar: `python -m src.evaluate_predictions --predictions results/<detector>/predictions_intermediate.csv`
2. Visualizar: `python -m src.visualize_results --metrics results/<detector>/metrics_comprehensive_with_nab.csv`
- `deprecated/grid_search.py` - Substituído por pipeline de 3 passos
- `deprecated/exhaustive_grid_search.py` - Substituído por generate_predictions.py
- `scripts/test_page_hinkley.sh` - Removido (obsoleto)

### 📊 IMPLEMENTADO: Sistema Completo de Avaliação

#### Pipeline de 3 Passos
1. **Gerar Predições**: `python -m src.generate_predictions --detector <NAME> --output results/<NAME>/predictions_intermediate.csv`tualização**: 2025-11-13 (Sessão 3 - Multi-Detector Framework)
**Status**: 7 detectores implementados e validados, grid searches otimizados, scripts de automação completos

Este documento resume tudo o que foi feito até agora para permitir continuidade futura mesmo sem o histórico da conversa.


### ✅ COMPLETO: Framework Multi-Detector (5 Detectores)

#### Implementação e Validação
   - Validação (5 ficheiros): F3=0.3687, Recall@10s=70.63%, FP/min=6.71
   - Extensão rodando: 594 combinações para min_gap < 1000 (tmux)
   - Script: `scripts/extended_min_gap_grid.sh`

2. **Page-Hinkley** (Cumulative Sum Test)
   - Grid: 384 combinações (4 lambdas × 4 deltas × 2 alphas × 3 ma_windows × 4 min_gaps)
   - Grid otimizado: Reduzido de 9,408 para 384 (redução de 96%)
   - Validação (5 ficheiros): F3=0.1629, Recall@10s=32.76%, FP/min=3.08 (melhor!)
   - Script: `scripts/generate_page_hinkley.sh` (~29 min)

3. **KSWIN** (Kolmogorov-Smirnov Windowing) ⭐ 100% RECALL
   - Grid: 1,280 combinações (4 alphas × 4 window_sizes × 4 stat_sizes × 4 ma_windows × 5 min_gaps)
   - Validação (5 ficheiros): F3=0.5035, Recall@10s=100% ⭐, FP/min=10.65
   - Valores contínuos (sem conversão binária)
   - Script: `scripts/generate_kswin.sh` (~90 min)

4. **HDDM_A** (Hoeffding Drift Detection Method - Average)
   - Grid: 640 combinações (4 drift_confs × 4 warning_confs × 2 two_sides × 4 ma_windows × 5 min_gaps)
   - Validação (5 ficheiros): F3=0.2967, Recall@10s=48.57%, FP/min=3.75
   - Script: `scripts/generate_hddm_a.sh` (~60 min)

5. **HDDM_W** (Hoeffding Drift Detection Method - Weighted) ⭐ MELHOR F3
   - Grid: 2,560 combinações (4 drift_confs × 4 warning_confs × 4 lambdas × 2 two_sides × 4 ma_windows × 5 min_gaps)
   - Validação (5 ficheiros): **F3=0.5342**, Recall@10s=74.29%, **EDD=1.73s**, FP/min=3.84
   - Script: `scripts/generate_hddm_w.sh` (~180 min)

**Nota**: DDM e EDDM foram removidos do framework por serem inadequados para análise de séries temporais. Estes detectores foram projetados para classificação binária (concept drift em streams de labels), não para detecção de mudanças em valores contínuos.

**Total de Combinações**: 5,359 (5 detectores apropriados para time series)
**Tempo Estimado Total**: ~412 min (~6.9 horas)

**Detectores removidos**: DDM e EDDM foram excluídos por serem inadequados para análise de séries temporais (projetados para concept drift em classificação binária).

#### Scripts de Automação
Documentação completa em `scripts/README.md` (atualizado):
- 5 scripts de produção (todos executáveis)
- Ordem de execução recomendada em 2 fases (rápido → médio-lento)
- Workflow padronizado: gerar → avaliar → visualizar → comparar
- Detalhes técnicos e troubleshooting

**Nota**: DDM e EDDM removidos (inadequados para time series).

### ✅ COMPLETO: Detector ADWIN (Dataset Completo)
- **Dataset**: 229 ficheiros afib_paroxysmal
- **Grid search**: 495 combinações de parâmetros
- **Avaliações**: 113,355 (495 × 229 ficheiros)
### Executar Grid Search com Scripts
```bash
# Fase 1 - Rápida (~30 min)
cd scripts && ./generate_ddm.sh && ./generate_eddm.sh

# Fase 2 - Média (~119 min)
./generate_page_hinkley.sh && ./generate_kswin.sh

# Fase 3 - Lenta (~240 min)
./generate_hddm_a.sh && ./generate_hddm_w.sh
```

- **Métricas calculadas**: `results/adwin/metrics_comprehensive_with_nab.csv` (33 MB)
- **Relatório final**: `results/adwin/final_report_with_nab.json` (12 KB)
**Última Atualização**: 2025-11-13 (Sessão 3 - Multi-Detector Framework)

## 10. Resumo da Sessão 3 (2025-11-13)

### Trabalho Realizado
1. ✅ **Implementados 5 detectores apropriados para time series**: Page-Hinkley, KSWIN, HDDM_A, HDDM_W, ADWIN
2. ✅ **Validação completa**: Cada detector testado com 5 ficheiros
3. ✅ **Grid search otimizado**: Page-Hinkley reduzido 96% (9,408 → 384 combos)
4. ✅ **Scripts de automação**: 5 scripts prontos (total ~412 min, ~6.9h)
5. ✅ **Documentação completa**: scripts/README.md atualizado
6. ✅ **Memória do projeto atualizada**: Estado completo documentado

**Nota (2025-11-17)**: DDM e EDDM foram posteriormente removidos por serem inadequados para análise de séries temporais.

### Detectores Validados (Ranking por F3)
1. **HDDM_W**: F3=0.5342 🏆 (melhor), Recall@10s=74.29%, EDD=1.73s
2. **KSWIN**: F3=0.5035, Recall@10s=100% 🏆, FP/min=10.65
3. **ADWIN**: F3=0.3687, Recall@10s=70.63% (dataset completo: F3=0.3994)
4. **HDDM_A**: F3=0.2967, Recall@10s=48.57%
5. **Page-Hinkley**: F3=0.1629, FP/min=3.08 🏆 (melhor)

### Próximos Passos Recomendados

**Curto Prazo** (próxima sessão):
1. ⏳ Monitorar conclusão ADWIN extensão (min_gap < 1000, ~53 min restante)
2. ⏳ Executar grid searches de produção (ordem recomendada em scripts/README.md):
   - Fase 1 (~29 min): Page-Hinkley
   - Fase 2 (~240 min): KSWIN + HDDM_A + HDDM_W
3. ⏳ Gerar visualizações para cada detector concluído
4. ⏳ Atualizar READMEs individuais com resultados

**Médio Prazo**:
1. Comparações multi-detector:
   - HDDM_W vs KSWIN (top 2 por F3 e Recall)
   - Análise de performance vs complexidade
2. Análise de trade-offs:
   - F3 vs FP/min vs EDD
   - Recall vs Precision
   - Performance vs Tempo de Execução
3. Documentação final:
   - Relatório comparativo completo
   - Recomendações de uso por cenário
   - Matriz de decisão (qual detector usar quando)

### Data Processing
- **Geração sintética**: `src/data_loader.py` - sinal sintético + ground-truth
- **Download Zenodo**: `src/zenodo_download.py` - dataset record 6879233
- **Preprocessamento genérico**: `src/prepare_dataset.py`
- **ECG preprocessing**: `src/ecg_preprocess.py` (port de scripts R)
  - Descoberta de ficheiros `.hea` com filtro por classe
  - Leitura de cabeçalho + CSV comprimido + anotações
  - Extração de eventos de regime (label_store ∈ {28,32,33})
  - Resample opcional (ex.: 200 → 250 Hz)
  - Limpeza de eventos duplicados e bordas

### Evaluation & Metrics
- **Sistema de métricas**: `src/evaluation.py`
  - Métricas clássicas (F1/F3 classic)
  - Métricas ponderadas por latência (F1*/F3* weighted)
  - Métricas temporais (Recall@4s/10s, Precision@4s/10s, EDD, FP/min)
  - **NAB Scores** (Standard, Low FP, Low FN) - Implementado 2025-11-13

- **Avaliação em lote**: `src/evaluate_predictions.py`
  - Processa CSV de predições intermediárias
  - Calcula todas as métricas por ficheiro
  - Agrega por combinação de parâmetros
  - Gera relatório JSON com melhores configurações
  - Suporta todos os 7 detectores dinamicamente

### Grid Search & Predictions
- **Geração de predições**: `src/generate_predictions.py`
  - Suporta todos os 7 detectores
  - Grid search parametrizado por detector
  - Modo incremental (--append) para extensões de grid
  - Paralelização com joblib (--n-jobs -1)
  - Grids configurados:
    - ADWIN: 495 combinações
    - Page-Hinkley: 384 combinações (otimizado de 9,408)
   - DDM: (removido do pipeline)
   - EDDM: (removido do pipeline)
    - KSWIN: 1,280 combinações
    - HDDM_A: 640 combinações
    - HDDM_W: 2,560 combinações
  - Output: `predictions_intermediate.csv` com detecções brutas
  - Suporta múltiplos detectores

### Visualization
   **Sistema de visualizações**: `src/visualize_results.py` (Implementado 2025-11-13)
  - **Precision-Recall scatter plots** (4s e 10s windows)
  - **Pareto front** (soluções não-dominadas)
  - **Parameter heatmaps** (4 métricas: F3, NAB, Recall, FP/min)
  - **Score distributions** (box plots comparativos)
  - **3D trade-off surface** (Recall × FP × EDD)
  - **Parameter sensitivity** (análise de sensibilidade)
  - Output: 9 gráficos PNG de alta qualidade
   - Documentação: `docs/visualizations_guide.md`

### Comparison & Analysis
   **Comparação entre detectores**: `src/compare_detectors.py` (Implementado 2025-11-13)
  - Tabela de melhores configurações por métrica
  - Rankings de detectores
  - Comparação estatística (mean ± std)
  - Relatório markdown completo
  - Recomendações de uso

### Automation Scripts
- **Scripts de produção**: `scripts/` (7 scripts executáveis)
   - `extended_min_gap_grid.sh` - ADWIN extensão (594 combos, ~53 min)
   - `generate_page_hinkley.sh` - Page-Hinkley (384 combos, ~29 min)
   - `generate_ddm.sh` - (removido do pipeline)
   - `generate_eddm.sh` - (removido do pipeline)
   - `generate_kswin.sh` - KSWIN (1,280 combos, ~90 min)
   - `generate_hddm_a.sh` - HDDM_A (640 combos, ~60 min)
   - `generate_hddm_w.sh` - HDDM_W (2,560 combos, ~180 min)
- **Documentação**: `scripts/README.md` (8.3KB)
   - Descrição detalhada de cada script
   - Tabela de comparação (combos, tempo, F3)
   - Ordem de execução recomendada (3 fases)
   - Workflow completo (gerar → avaliar → visualizar)
   - Troubleshooting

## 4. Estrutura de Resultados Organizada (2025-11-13)

### Diretórios por Detector
```
results/
├── adwin/                          # ✅ COMPLETO
│   ├── predictions_intermediate.csv (126 MB)
│   ├── metrics_comprehensive_with_nab.csv (33 MB)
│   ├── final_report_with_nab.json (12 KB)
│   ├── visualizations/ (9 gráficos PNG, 4.3 MB)
│   └── README.md
│
├── page_hinkley/                   # ⏳ PRONTO PARA PRODUÇÃO
│   └── README.md (template para preencher após grid search)
│
├── kswin/                          # ⏳ PRONTO PARA PRODUÇÃO
│   └── (a criar após grid search)
│
├── hddm_a/                         # ⏳ PRONTO PARA PRODUÇÃO
│   └── (a criar após grid search)
│
├── hddm_w/                         # ⏳ PRONTO PARA PRODUÇÃO
│   └── (a criar após grid search)
│
├── comparisons/                    # ⏳ AGUARDA MÚTIPLOS DETECTORES
│   └── (a criar após executar grid searches)
│
└── README.md
```

**Nota**: Diretórios `ddm/` e `eddm/` foram removidos (detectores inadequados para time series).
```
results/
├── adwin/                          # ✅ COMPLETO
│   ├── predictions_intermediate.csv (126 MB)
│   ├── metrics_comprehensive_with_nab.csv (33 MB)
│   ├── final_report_with_nab.json (12 KB)
│   ├── visualizations/ (9 gráficos PNG, 4.3 MB)
│   └── README.md
│
├── page_hinkley/                   # ⏳ PRONTO PARA PRODUÇÃO
│   └── README.md (template para preencher após grid search)
│
├── ddm/                            # ⏳ PRONTO PARA PRODUÇÃO
│   └── README.md (template para preencher após grid search)
│
├── eddm/                           # ⏳ PRONTO PARA PRODUÇÃO
│   └── (a criar após grid search)
│
├── kswin/                          # ⏳ PRONTO PARA PRODUÇÃO
│   └── (a criar após grid search)
│
├── hddm_a/                         # ⏳ PRONTO PARA PRODUÇÃO
│   └── (a criar após grid search)
│
├── hddm_w/                         # ⏳ PRONTO PARA PRODUÇÃO
│   └── (a criar após grid search)
│
├── comparisons/                    # ⏳ AGUARDA MÚLTIPLOS DETECTORES
│   └── (a criar após executar grid searches)
│
└── README.md
```

### Documentação Completa
- **results/README.md** - Organização de resultados por detector, workflow padronizado
- **results/adwin/README.md** - Resultados completos do ADWIN, melhores configurações
- **results/page_hinkley/README.md** - Template para Page-Hinkley (a implementar)
- **scripts/README.md** - Documentação completa de automação (5 detectores)
- **docs/evaluation_metrics_v1.md** - Documentação detalhada das métricas
- **docs/visualizations_guide.md** - Guia completo de interpretação de gráficos

**Nota**: Referências a DDM/EDDM foram removidas (detectores inadequados).

## 5. Métricas de Avaliação (Sistema Completo)

### 5.1. Métricas Clássicas (F1/F3 Classic)
- F1-classic: Média harmônica de precision e recall
- F3-classic: Versão que enfatiza recall (β=3)
- Uso: Baseline para comparação com literatura

### 4.2. Métricas Ponderadas por Latência (F1*/F3* Weighted)
**Função de Peso Temporal**:
```
w(δ) = {
    1.0,                se δ ≤ 4s    (detecção ideal)
    1 - (δ-4)/(10-4),  se 4s < δ ≤ 10s (decaimento linear)
    0.0,                se δ > 10s   (detecção tardia demais)
}
```

**Métricas Auxiliares**:
- Recall@4s, Recall@10s: % eventos detectados dentro da janela
- Precision@4s, Precision@10s: Precisão temporal
- EDD (Expected Detection Delay): Atraso mediano
- FP/min: Taxa de falsos positivos

**Uso**: **F3-weighted é a métrica primária** para otimização

### 4.3. NAB Score (Numenta Anomaly Benchmark)
**Implementado**: 2025-11-13

**Função Sigmoid**:
```python
S(r) = 2 × sigmoid(-5r) - 1
# r = posição relativa na janela
# r = -1.0 → score ≈ +0.987 (início)
# r = 0.0  → score = 0.0 (fim)
# r > 0.0  → score negativo (FP)
```

**Profiles de Custo**:
1. **NAB Standard** (balanceado): tp=1.0, fp=0.11, fn=1.0
2. **NAB Low FP** (penalizar FP 2×): tp=1.0, fp=0.22, fn=1.0
3. **NAB Low FN** (penalizar FN 2×): tp=1.0, fp=0.055, fn=2.0

**Características**:
- Período probatório (15% inicial ignorado)
- Recompensa detecção antecipada
- Penalidade crescente para FPs
- Scores podem ser negativos (comum em dados ruidosos)

**Implementação**:
- `src/evaluation.py`: Funções `sigmoid()`, `nab_scaled_sigmoid()`, `NABCostMatrix`, `calculate_nab_score()`
- Integrado em `calculate_comprehensive_metrics()`
- Testado com suite completa (`test_nab_metric.py` - 8/8 tests passed)

### 4.4. Comparação entre Métricas
| Métrica | Temporal? | Melhor Para | Range |
|---------|-----------|-------------|-------|
| F1-classic | ❌ | Baseline | [0, 1] |
| F3-classic | ❌ | Recall sem tempo | [0, 1] |
| F1-weighted | ✅ | Balance precision/recall | [0, 1] |
| **F3-weighted** | ✅ | **Otimização primária** | [0, 1] |
| NAB Standard | ✅ | Comparação com literatura | ℝ |
| NAB Low FP | ✅ | Minimizar alarmes | ℝ |
| NAB Low FN | ✅ | Aplicações críticas | ℝ |

## 5. Visualizações (Implementado 2025-11-13)

### Script: `src/visualize_results.py`
Sistema completo de análise visual dos resultados de grid search.

### Gráficos Gerados (9 total)

1. **pr_scatter_plots.png** - Precision-Recall scatter
   - Painel 4s e 10s
   - Cor = F3-weighted score
   - Estrela vermelha = melhor configuração

2. **pareto_front.png** - Fronteira de soluções não-dominadas
   - Eixos: Recall@10s vs FP/min
   - Identifica trade-offs ótimos
   - Mostra nº de soluções Pareto-ótimas

3. **heatmap_f3-weighted.png** - Sensibilidade de parâmetros
4. **heatmap_nab-score-standard.png** - Efeito em NAB Standard
5. **heatmap_recall-10s.png** - Efeito em Recall@10s
6. **heatmap_fp-per-min.png** - Efeito em taxa de FP
   - Layout: delta × ma_window, painéis por min_gap
   - Cores quentes = melhores valores

7. **score_distributions.png** - Box plots comparativos
   - 4 painéis: F-scores, NAB, Recall@4s/10s, FP/min e EDD

8. **3d_tradeoff.png** - Superfície 3D
   - Eixos: Recall@10s × FP/min × EDD
   - Cor = F3-weighted

9. **parameter_sensitivity.png** - Sensibilidade paramétrica
   - Linhas: F3-weighted e Recall@10s
   - Colunas: delta, ma_window, min_gap
   - Área sombreada = ± 1 std

### Workflow de Análise Recomendado
1. `pr_scatter_plots.png` → Entender trade-offs gerais
2. `pareto_front.png` → Identificar soluções ótimas
3. `heatmap_*.png` → Refinar valores de parâmetros
4. `score_distributions.png` → Verificar variabilidade
5. `3d_tradeoff.png` → Trade-offs multi-objetivo
6. `parameter_sensitivity.png` → Entender impacto de parâmetros

## 6. Próximos Passos Prioritários

### Alta Prioridade
1. **Implementar Page-Hinkley**
   - Gerar predições com grid search sugerido
   - Avaliar métricas completas
   - Criar visualizações
   - Documentar resultados em `results/page_hinkley/README.md`

2. **Implementar DDM**
   - Adaptar para sinais contínuos (usar derivada ou z-score)
   - Seguir pipeline padronizado
   - Comparar com ADWIN

3. **Comparação Multi-Detector**
   - Executar `src/compare_detectors.py` após ter ≥2 detectores
   - Gerar relatório comparativo
   - Identificar detector superior por métrica

### Média Prioridade
4. **Análise de Ensemble**
   - Voting (maioria entre 2-3 detectores)
   - Weighted voting (ponderar por F3-score)
   - Cascata (detector rápido → detector preciso)

5. **Validação Cruzada**
   - Testar em outras classes (persistent_afib, non_afib)
   - Split por paciente
   - Análise de variabilidade inter-paciente

### Baixa Prioridade
6. **Outros Detectores**
   - EDDM (Early DDM)
   - HDDM (Hoeffding's Bound)
   - KSWIN (Kolmogorov-Smirnov)

7. **Otimizações**
   - Paralelização de generate_predictions
   - Cache de resultados intermediários
   - Streaming incremental real

## 7. Lições Aprendidas & Boas Práticas

### Métricas
- ✅ F3-weighted é melhor métrica primária para otimização
- ✅ NAB scores úteis para comparação com literatura, mas valores negativos são normais
- ✅ Reportar sempre múltiplas métricas (F3, NAB, Recall@10s, FP/min)
- ⚠️ Evitar otimizar apenas para recall (gera muitos FPs)

### Parâmetros
- **delta**: Menor = mais sensível (↑ recall, ↑ FP)
- **ma_window**: Suavização reduz ruído mas pode atrasar detecção
- **min_gap**: Crucial para reduzir FPs em clustering

### Workflow
- ✅ Pipeline de 3 passos (Predict → Evaluate → Visualize) funciona bem
- ✅ Separação clara entre predições brutas e métricas facilita debug
- ✅ Organização por detector permite comparações limpas
- ✅ Visualizações são essenciais para entender trade-offs

### Performance
- ADWIN: ~50 min para 229 ficheiros × 495 combinações
- Avaliação: ~84 segundos para 113k avaliações
- Visualizações: ~30 segundos para 9 gráficos

## 8. Bugs Conhecidos & Limitações

### Resolvidos ✅
- NAB scores ausentes do terminal → Corrigido (2025-11-13)
- Quebras de linha `\n` literais no terminal → Corrigido (2025-11-13)
- NAB scores sem valores no relatório comparativo → Corrigido (2025-11-13)

### Limitações Atuais
- ⚠️ Média móvel não estritamente causal (usa convolução 'same')
- ⚠️ Processamento sequencial de ficheiros (pode paralelizar)
- ⚠️ Apenas canal único por vez (multi-lead futuro)
- ⚠️ NAB scores negativos podem confundir (normal para dados ruidosos)

### A Resolver
- [ ] Implementar média móvel estritamente causal (buffer FIFO)
- [ ] Adicionar suporte multi-lead
- [ ] Paralelizar generate_predictions por ficheiro
- [ ] Adicionar testes unitários completos

## 9. Comandos Rápidos (Cheat Sheet)

### Preprocessar Dataset
```bash
python -m src.ecg_preprocess \
    --root data/zenodo_6879233/extracted/afib_regimes \
    --classes paroxysmal_afib \
    --limit-per-class 10 \
    --output data/afib_paroxysmal_tidy.csv
```

### Pipeline Completo para Novo Detector
```bash
# 1. Gerar predições
python -m src.generate_predictions \
    --detector <NAME> \
    --output results/<NAME>/predictions_intermediate.csv \
    --delta 0.005 0.01 0.015 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 \
    --ma-window 10 30 50 100 200 300 500 \
    --min-gap 500 1000 1500 2000 2500 3000 4000 5000 7500 10000

# 2. Avaliar métricas
python -m src.evaluate_predictions \
    --predictions results/<NAME>/predictions_intermediate.csv \
    --metrics-output results/<NAME>/metrics_comprehensive_with_nab.csv \
    --report-output results/<NAME>/final_report_with_nab.json

# 3. Visualizar
python -m src.visualize_results \
    --metrics results/<NAME>/metrics_comprehensive_with_nab.csv \
    --output-dir results/<NAME>/visualizations
```

### Comparar Detectores
```bash
python -m src.compare_detectors \
   --detectors adwin page_hinkley kswin hddm_a hddm_w \
    --output results/comparisons/comparative_report.md \
    --csv-output results/comparisons/detector_rankings.csv
```

### Ver Resultados ADWIN
```bash
# Relatório terminal
python -m src.evaluate_predictions \
    --predictions results/adwin/predictions_intermediate.csv \
    --metrics-output results/adwin/metrics_comprehensive_with_nab.csv \
    --report-output results/adwin/final_report_with_nab.json \
    --skip-evaluation

# Abrir visualizações
xdg-open results/adwin/visualizations/pareto_front.png
```

---

**Fim da Memória Persistente**
**Última Atualização**: 2025-11-13 (Reorganização completa, NAB implementado, visualizações criadas)
**Próxima Sessão**: Implementar Page-Hinkley e DDM, gerar comparações
- **Resultados per-patient**:
  - data_101_7.par: F1=0.400 (delta=0.005, ma_window=125, min_gap=3000)
  - data_101_6.par: F1=0.250 (delta=0.080, ma_window=175, min_gap=3000)
  - data_101_5.par: F1=0.174 (delta=0.050, ma_window=50, min_gap=1000)

#### **Melhor Combinação Global (baseline universal)**:
```
delta = 0.08
ma_window = 175
min_gap_samples = 3000
```
- **Performance**: F1 médio=0.217±0.202, testado em 3 pacientes
- **Trade-off**: Funciona bem em 2/3 pacientes, falha no mais difícil

### Insights Validados
1. **Variabilidade inter-paciente significativa**: Cada paciente tem parâmetros ótimos diferentes.
2. **Não existe configuração universal**: Trade-off entre robustez global vs performance individual.
3. **Abordagem exhaustiva é efetiva**: Encontra configurações ótimas per-patient e global.
4. **Baseline está pronto**: Configuração universal identificada para comparação com detector R.

## 5. Validação Rápida Realizada (2025-09-27)
Comando usado (classe única paroxysmal_afib, 10 ficheiros):
```bash
python -m src.ecg_preprocess \
  --root data/zenodo_6879233/extracted/afib_regimes \
  --classes paroxysmal_afib \
  --limit-per-class 10 \
  --lead II \
  --resample-to 250 \
  --output data/afib_paroxysmal_tidy.csv
```
Resultado:
- Linhas totais: 586,554
- Registos (ids): 10
- Eventos de regime (soma): 46
- Eventos por registo (descr.): min=1, mediana=4, máx=10
- Exemplo primeiro id: ~145,971 samples, 1 evento em posição ~70,599.

Execução do detector ADWIN:
```bash
python -m src.streaming_detector \
  --data data/afib_paroxysmal_tidy.csv \
  --detector adwin --ma-window 25 \
  --min-gap-samples 3000 --param delta=0.01 \
  --tolerance 500 --sample-rate 250
```
Métricas obtidas (pipeline concatenando todos os ids):
- Detecções: 41 | Ground-truth: 46
- TP=2, FP=39, FN=44
- Precision ≈ 0.049 | Recall ≈ 0.043 | Delay médio ≈ 106 samples (~0.424 s)

Interpretação inicial:
- Muitos FP: provável influência de mudanças de baseline entre registos + delta não ajustado + ausência de features derivadas dentro do fluxo.

## 6. Estrutura Atual dos Principais Arquivos
- `src/streaming_detector.py`: loop streaming + opções de pré-processamento (média móvel, derivada) + min-gap + JSON logging.
- `src/ecg_preprocess.py`: conversão batch dos múltiplos registos WFDB → tidy CSV multi-id.
- `src/grid_search.py`: grid simples (atualmente orientado a dataset único); precisa adaptação multi-id.
- **`src/exhaustive_grid_search.py`**: grid exhaustivo per-file com paralelização, similar à abordagem R.
- `R/`: scripts originais de referência (muito extensos) — não usados diretamente em runtime Python.

## 7. Decisões & Diretrizes Consolidadas
- Sem lookahead: processar amostra a amostra (condição mantida).
- Reprodutibilidade: dependências pinadas em `requirements.txt`.
- Não versionar dados grandes: pasta `data/` ignorada no `.gitignore`.
- Incrementos pequenos validados por execuções rápidas antes de expandir escopo.
- Documentar cada novo parâmetro no README (feito para ecg_preprocess principal; pendente para exhaustive_grid_search).

## 8. Backlog / Próximos Passos Recomendados

### **Curto prazo** (próxima sessão):
1. **Comparar baseline Python vs detector R** usando os mesmos dados e parâmetros encontrados.
2. **Executar grid search no dataset completo** (todos os 10 ficheiros) para validação final.
3. **Documentar parâmetros ótimos** no README com tabela de configurações.
4. **Análise de robustez**: Avaliar se parâmetros globais são suficientemente estáveis.

### **Médio prazo**:
5. Adicionar coluna `time_seconds` ao CSV tidy (sample_index / fs) – para inspeção temporal.
6. Tornar códigos de anotação configuráveis via CLI (`--label-codes 28 32 33`).
7. Permitir manter registos sem eventos (`--keep-nochange`), útil para FP analysis.
8. Opcional: aplicar derivada + normalização incremental (online z-score) antes de detectar.
9. Implementar outros detectores (EDDM, HDDM_A, HDDM_W) se suportados pela versão do scikit-multiflow.
10. Métrica de distribuição de atrasos (histograma + percentis) além do delay médio.

### **Longo prazo**:
11. Adicionar testes unitários mínimos (clean_truth, resample, matching de eventos, build_tidy sem eventos).
12. Exportar métricas agregadas em JSON para ingestão posterior (ex.: dashboard).
13. Extender grid search para multi-run por semente / média dos resultados.
14. Pipeline de CI (lint + testes básicos) e badge no README.
15. Suporte multi-lead (wide vs long) e seleção automática de lead com maior SNR.
16. Detecção adaptativa híbrida (ex.: ADWIN sobre derivada + PageHinkley sobre média filtrada).
17. Compressão/segmentação incremental para reduzir custo em sinais muito longos (chunk streaming real).
18. Persistir regime indices crus (pré-limpeza) em JSON para auditoria.

## 9. Pendências Técnicas / Riscos
- Grid search exhaustivo validado apenas em 3 pacientes; precisa validação em dataset completo.
- Concatenar múltiplos ids pode inflar FP (resolvido com per-file evaluation).
- Limpeza de eventos pode excluir mudanças muito cedo/tarde que façam sentido clinicamente (validar com domínio).
- Resample linear pode introduzir suavização leve; se houver QRS acurado envolvido em sinais curtos, talvez considerar métodos band-limited ou polyphase.

## 10. Comandos Úteis (Resumo)

### Geração subset (paroxysmal_afib, 10 ficheiros):
```bash
python -m src.ecg_preprocess --root data/zenodo_6879233/extracted/afib_regimes \
  --classes paroxysmal_afib --limit-per-class 10 \
  --lead II --resample-to 250 \
  --output data/afib_paroxysmal_tidy.csv
```

### Detecção ADWIN (baseline):
```bash
python -m src.streaming_detector --data data/afib_paroxysmal_tidy.csv \
  --detector adwin --ma-window 25 --min-gap-samples 3000 \
  --param delta=0.01 --tolerance 500 --sample-rate 250
```

### **Grid Search Exhaustivo (NOVO)**:
```bash
# Teste rápido (3 ficheiros)
python -m src.exhaustive_grid_search \
  --data data/multi_test.csv \
  --output results/exhaustive_grid_multi.csv \
  --n-jobs -1

# Dataset completo
python -m src.exhaustive_grid_search \
  --data data/afib_paroxysmal_tidy.csv \
  --output results/exhaustive_grid_full.csv \
  --n-jobs -1
```

### **Parâmetros Ótimos Encontrados**:
```bash
# Melhor configuração global (baseline universal)
python -m src.streaming_detector \
  --data data/afib_paroxysmal_tidy.csv \
  --detector adwin \
  --ma-window 175 \
  --min-gap-samples 3000 \
  --param delta=0.08 \
  --tolerance 500 --sample-rate 250
```

## 11. Estado Final da Sessão (2025-09-28)
- **Grid search exhaustivo implementado e validado** com 385 combinações de parâmetros.
- **Per-file evaluation funcionando** com paralelização eficiente.
- **Parâmetros ótimos identificados**: delta=0.08, ma_window=175, min_gap=3000 (baseline universal).
- **Variabilidade inter-paciente quantificada**: F1 varia de 0.0 a 0.4 entre pacientes.
- **Baseline Python está completo e pronto para comparação** com detector R.
- **Próximo passo recomendado**: Comparação direta Python vs R nos mesmos dados.

---
(Atualizado em: 2025-09-28)
