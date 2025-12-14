# Projeto: Streaming ECG Regime Change Detection (Sessão de Trabalho - Memória Persistente)

## RESUMO EXECUTIVO DA SESSÃO 10 (2025-12-14)

### ✅ Trabalho de Hoje
1. **Agregação two-fold cross-validation**
   - `src/aggregate_twofold_analysis.py` (382 linhas) criado para processar todos os 18 relatórios two-fold (6 detectores × 3 datasets)
   - Implementada seleção robusta: para cada detector×dataset, escolhe o fold com **melhor cross-fold F3** (generalização), com tiebreaker por **menor gap**
   - Análise em 3 níveis: Robustness Ranking global, Per-Dataset Comparison, Generalization Gap Analysis

2. **Artefatos Gerados**
   - 📊 **twofold_analysis_summary.md** (2.5 KB): Resumo executivo com tabelas de robustez
   - 📁 **3 CSVs de robustez** (um por dataset): Métricas por detector para análise posterior
   - 📘 **TWOFOLD_ROBUSTNESS_README.md** (7 KB): Documentação completa com:
     - Metodologia e seleção de configurações
     - Rankings globais de robustez (FLOSS: 1º com 0.0211 avg gap)
     - Per-dataset insights (FLOSS domina em afib_paroxysmal e vtachyarrhythmias)
     - Perfis por detector (strengths/challenges/recommendations)
     - Guia de produção (qual usar quando?)

3. **Insights-Chave**
   - ✅ **FLOSS**: Melhor robustez geral (gap 0.0211 = 2.1% drop ao generalizar)
   - ✅ **ADWIN**: Excelente em datasets pequenos (malignantventricular: 0.0046 gap)
   - ✅ **KSWIN**: Bom equilíbrio performance/robustez
   - ⚠️  **Page-Hinkley**: Maior sensibilidade paramétrica (0.0516 avg gap)

### 📌 Estado
- Two-fold analysis completa e documentada. Scores de generalização calculados e rankings estabelecidos.
- Recomendações para produção: usar FLOSS para novos dados (máxima portabilidade de hiperparâmetros).

### 🔄 Próximos Passos
- Opcionalmente: expandir comparações FLOSS vs outros detectores (ponto 2 do backlog Sessão 6)
- Opcionalmente: criar matriz de decisão visual (qual detector usar em qual cenário)

## RESUMO EXECUTIVO DA SESSÃO 9 (2025-11-28)

### ✅ Trabalho de Hoje
1. **Relatórios 2-fold mais visíveis**
   - `src/evaluate_predictions.py` agora imprime um resumo dos folds no terminal e cria um snapshot Markdown com sufixo/timestamp sempre que `--two-fold-analysis` é usado.
   - Scripts `scripts/evaluate_*.sh` (ADWIN, FLOSS, KSWIN, HDDM_A, HDDM_W, Page-Hinkley) passam automaticamente os parâmetros `--two-fold-*`.
2. **Correções adicionais**
   - Conversão dos `record_id` (int64) ao salvar `fold_assignments_seed*.json`, evitando `TypeError`.
   - Orientação documentada sobre interpretação dos resultados two-fold (média intra-fold vs cross-fold, gap de generalização) e sobre o atraso inerente dos detectores streaming (landmark/evidência).

### 📌 Estado
- Todos os datasets/detectores já possuem relatórios two-fold JSON + Markdown (com seed 42) e fold assignments persistidos; execução dos scripts agora sempre produz também os snapshots.
- Usuário alinhado sobre como relatar os valores A→B/B→A e justificar atrasos de detecção.

### 🔄 Próximos Passos
- Agregar e comparar as métricas two-fold (usar os scores “fold oposto”) por detector/dataset conforme a metodologia discutida, preparando tabelas/resumos macro.

## RESUMO EXECUTIVO DA SESSÃO 8 (2025-11-27)

### ✅ Trabalho de Hoje
1. **Robustez 2-fold reutilizando predições existentes**
   - `src/evaluate_predictions.py` agora aceita `--two-fold-analysis` (+seed, metric e sufixo). O script divide os `record_id` em duas metades determinísticas (persistidas em `results/<dataset>/fold_assignments_seed<seed>.json`), encontra o melhor conjunto de parâmetros em cada metade e mede o desempenho cruzado usando apenas `predictions_intermediate.csv`/`metrics_comprehensive_with_nab.csv`.
   - Relatório adicional salvo em `results/<dataset>/<detector>/final_report_with_nab_twofold_seed<seed>.json` com métricas intra-fold, cross-fold e sugestões (maior média no fold oposto / menor gap).

2. **Documentação atualizada**
   - `results/README.md` descreve o novo modo 2-fold, parâmetros de CLI e artefatos extra.

3. **Execução recomendada**
   - Para rodar no dataset `vtachyarrhythmias`, ativar `.venv` e usar:
     `python -m src.evaluate_predictions --predictions results/vtachyarrhythmias/<detector>/predictions_intermediate.csv --metrics-output .../metrics_comprehensive_with_nab.csv --report-output .../final_report_with_nab.json --two-fold-analysis --two-fold-seed 42 --two-fold-primary-metric f3_weighted`

### 📌 Status
- Nenhuma nova geração de predições; apenas reutilização dos CSVs existentes.
- Repositório permanece organizado por dataset/detector com outputs estáveis.

### 🔄 Próximos Passos
- Executar o novo modo 2-fold para cada detector/dataset (começar por `vtachyarrhythmias` para validar).
- Assim que estivermos satisfeitos com os relatórios por dataset, incorporar a lógica em `compare_detectors` para comparação cross-dataset com os scores “fold-oposto”.

## RESUMO EXECUTIVO DA SESSÃO 7 (2025-11-26)

### ✅ Trabalho de Hoje
1. **Sincronização das instruções operacionais**
   - `.github/copilot-instructions.md` reescrito para refletir o estado atual (6 detectores completos × 3 datasets, comparações em `comparisons/<dataset>/`, análises macro/micro em `results/cross_dataset_analysis/`).
   - Pipeline padronizado e comandos críticos atualizados (uso obrigatório de `--dataset` no `compare_detectors`, notas sobre `min_gap_samples` como pós-processamento, proibição de novos MD sem aval).

2. **Verificação estrutural**
   - Confirmada a estrutura por dataset: `results/{afib_paroxysmal,malignantventricular,vtachyarrhythmias}/<detector>/` com CSVs, JSON/JSONL, summaries e 9 visualizações por detector.
   - Validados diretórios de comparação (`comparisons/<dataset>/...`) contendo `comparative_report.md`, `detector_rankings.csv`, `detector_summary.csv`, `constraint_tradeoffs.csv`, `robustness.csv`.

### 📌 Estado Atual (inalterado desde Sessão 6)
- 6 detectores (ADWIN, Page-Hinkley, KSWIN, HDDM_A, HDDM_W, FLOSS) concluídos em 3 datasets, totalizando 18 avaliações completas com métricas/visualizações/relatórios.
- Cross-dataset analysis por detector em `results/cross_dataset_analysis/<detector>/` (macro & micro averages + READMEs).
- Scripts `generate/evaluate/visualize` suportam `--max-files/--max-samples` e repassam argumentos extras.

### 🔄 Próximos Passos Relevantes
- Executar novas comparações multi-detector quando necessário via `python -m src.compare_detectors --dataset <dataset> ...` para manter `comparisons/<dataset>/` atualizados.
- Expandir comparações FLOSS vs outros detectores e análises cross-dataset, conforme backlog da Sessão 6.

### 📝 Observações
- Sem alterações no código-fonte além da atualização de `.github/copilot-instructions.md`.
- Nenhum novo dataset ou resultado pesado versionado.

**Última Atualização**: 2025-11-26 (Sessão 7 - Instruções sincronizadas, estado verificado)
**Status**: ✅ TODAS AS AVALIAÇÕES COMPLETAS - 6 detectores (ADWIN, Page-Hinkley, KSWIN, HDDM_A, HDDM_W, FLOSS) × 3 datasets (afib_paroxysmal, malignantventricular, vtachyarrhythmias) = 18 avaliações completas com métricas, visualizações e relatórios

Este documento resume tudo o que foi feito até agora para permitir continuidade futura mesmo sem o histórico da conversa.

---

## RESUMO EXECUTIVO DA SESSÃO 6 (2025-11-24)

### ✅ Trabalho Completado (Todas as Avaliações)

#### **STATUS FINAL: PIPELINE COMPLETO** 🎉

Todas as avaliações de **6 detectores** em **3 datasets** foram concluídas com sucesso:

| Dataset | Ficheiros | Eventos | Samples | Detectores Completos |
|---------|-----------|---------|---------|----------------------|
| **afib_paroxysmal** | 229 | 1,301 | 41.3M | ✅ 6/6 (ADWIN, Page-Hinkley, KSWIN, HDDM_A, HDDM_W, FLOSS) |
| **malignantventricular** | 22 | 592 | 11.6M | ✅ 6/6 (ADWIN, Page-Hinkley, KSWIN, HDDM_A, HDDM_W, FLOSS) |
| **vtachyarrhythmias** | 34 | 97 | 4.3M | ✅ 6/6 (ADWIN, Page-Hinkley, KSWIN, HDDM_A, HDDM_W, FLOSS) |
| **TOTAL** | **285** | **1,990** | **57.2M** | **18 avaliações completas** |

#### 1. Estrutura de Resultados Organizada por Dataset

A estrutura foi reorganizada por dataset para facilitar comparações:

```
results/
├── afib_paroxysmal/          # 229 ficheiros, 1,301 eventos
│   ├── adwin/                ✅ Completo (594 configs, 136K avaliações, 195MB predictions)
│   ├── page_hinkley/         ✅ Completo (600 configs, 137K avaliações, 126MB predictions)
│   ├── kswin/                ✅ Completo (1,280 configs, 293K avaliações, 543MB predictions)
│   ├── hddm_a/               ✅ Completo (640 configs, 147K avaliações, 155MB predictions)
│   ├── hddm_w/               ✅ Completo (2,560 configs, 586K avaliações, 498MB predictions)
│   └── floss/                ✅ Completo (25,920 configs, 5.9M avaliações, 1.1GB predictions)
│
├── malignantventricular/     # 22 ficheiros, 592 eventos
│   ├── adwin/                ✅ Completo (39MB predictions, 3.4MB metrics)
│   ├── page_hinkley/         ✅ Completo (58MB predictions, 2.8MB metrics)
│   ├── kswin/                ✅ Completo (153MB predictions, 7.7MB metrics)
│   ├── hddm_a/               ✅ Completo (97MB predictions, 4.5MB metrics)
│   ├── hddm_w/               ✅ Completo (32MB predictions, 7.9MB metrics)
│   └── floss/                ✅ Completo (315MB predictions, 143MB metrics)
│
├── vtachyarrhythmias/        # 34 ficheiros, 97 eventos
│   ├── adwin/                ✅ Completo (15MB predictions, 4.4MB metrics)
│   ├── page_hinkley/         ✅ Completo (23MB predictions, 3.9MB metrics)
│   ├── kswin/                ✅ Completo (54MB predictions, 11MB metrics)
│   ├── hddm_a/               ✅ Completo (35MB predictions, 6.3MB metrics)
│   ├── hddm_w/               ✅ Completo (16MB predictions, 12MB metrics)
│   └── floss/                ✅ Completo (125MB predictions, 199MB metrics)
│
└── comparisons/              # Comparações multi-detector
    └── floss_vs_kswin.*      ✅ Radar, bars, distributions (dataset afib_paroxysmal)
```

#### 2. Estatísticas de Avaliação por Detector

**Dataset: afib_paroxysmal (229 ficheiros)**

| Detector | Configs | Avaliações | Tamanho Predictions | Tamanho Metrics | Visualizações |
|----------|---------|------------|---------------------|-----------------|---------------|
| ADWIN | 594 | 136,026 | 195 MB | 39 MB | ✅ 9 gráficos |
| Page-Hinkley | 600 | 137,400 | 126 MB | 34 MB | ✅ 9 gráficos |
| KSWIN | 1,280 | 293,120 | 543 MB | 77 MB | ✅ 9 gráficos |
| HDDM_A | 640 | 146,560 | 155 MB | 39 MB | ✅ 9 gráficos |
| HDDM_W | 2,560 | 586,240 | 498 MB | 146 MB | ✅ 9 gráficos |
| FLOSS | 25,920 | 5,935,680 | 1.1 GB | 1.3 GB | ✅ 9 gráficos |
| **TOTAL** | **31,594** | **7,235,026** | **2.6 GB** | **1.6 GB** | **54 gráficos** |

**Todos os datasets têm**:
- ✅ `predictions_intermediate.csv` (predições brutas)
- ✅ `metrics_comprehensive_with_nab.csv` (métricas completas)
- ✅ `final_report_with_nab.json` (relatório com melhores configurações)
- ✅ `visualizations/` (9 gráficos PNG por detector)

#### 3. Melhores Configurações por Detector (afib_paroxysmal)

Com base em **F3-weighted** (métrica primária de otimização):

1. **FLOSS** (F3* = 0.3397)
   - window_size: 75, regime_threshold: 0.7, regime_landmark: 4.0, min_gap: 1000

2. **KSWIN** (F3* = 0.167)
   - alpha: 0.005, window_size: 500, stat_size: 50, ma_window: 50, min_gap: 1000

3. **ADWIN** (F3* = 0.1603)
   - delta: 0.005, ma_window: 300, min_gap: 1000

4. **Page-Hinkley** (F3* = 0.1551)
   - lambda: 1.0, delta: 0.04, alpha: 0.9999, ma_window: 50, min_gap: 1000

5. **HDDM_A** (F3* = 0.1547)
   - drift_confidence: 0.005, warning_confidence: 0.001, two_side: true, ma_window: 1, min_gap: 1000

6. **HDDM_W** (F3* = 0.1489)
   - drift_confidence: 0.005, warning_confidence: 0.001, lambda: 0.2, two_side: false, ma_window: 1, min_gap: 1000

**Nota**: FLOSS demonstra performance significativamente superior (2× melhor que segundo colocado)

### 📊 Estado Atual do Projeto

#### Detectores Completos (6/6) ✅
1. **ADWIN** - 3 datasets completos ✅
2. **Page-Hinkley** - 3 datasets completos ✅
3. **KSWIN** - 3 datasets completos ✅
4. **HDDM_A** - 3 datasets completos ✅
5. **HDDM_W** - 3 datasets completos ✅
6. **FLOSS** - 3 datasets completos ✅ (integração R→Python)

#### Comparações Multi-Detector
- **FLOSS vs KSWIN** - Completo ✅ (dataset afib_paroxysmal)
  - Visualizações: radar chart, bar charts, violin plots
  - Relatório executivo em `results/comparisons/floss_vs_kswin.md`

#### Próximos Passos Sugeridos

**Alta Prioridade**:
1. 🔄 **Comparações adicionais entre detectores**
   - FLOSS vs ADWIN, FLOSS vs Page-Hinkley
   - Análise de robustez cross-dataset
   - Comparação de performance vs complexidade computacional

2. 🔄 **Análise cross-dataset**
   - Como os detectores performam em datasets diferentes?
   - Generalização de hiperparâmetros
   - Transferência de configurações entre datasets

3. 🔄 **Documentação final**
   - Atualizar README principal com resultados finais
   - Criar guia de seleção de detector por cenário
   - Matriz de decisão (qual detector usar quando)

**Média Prioridade**:
4. **Ensemble methods**
   - Voting entre top-3 detectores
   - Weighted voting por F3-score
   - Análise de complementaridade

5. **Otimização de hiperparâmetros**
   - Bayesian optimization para top detectores
   - Análise de sensibilidade paramétrica
   - Transfer learning de hiperparâmetros

---

## RESUMO EXECUTIVO DA SESSÃO 5 (2025-11-18)

### ✅ Trabalho Realizado

#### 1. Scripts de Automação para FLOSS
- ✅ **`scripts/evaluate_floss.sh`**: Script completo de avaliação de métricas
  - Verifica existência do `predictions_intermediate.csv`
  - Executa `evaluate_predictions.py` com todos os parâmetros
  - Gera outputs (CSV, JSONL, JSON report e summary)
  - Mensagens coloridas e informativas
- ✅ **`scripts/visualize_floss.sh`**: Script completo de geração de visualizações
  - Verifica existência do `metrics_comprehensive_with_nab.csv`
  - Executa `visualize_results.py` para gerar 9 gráficos
  - Lista ficheiros PNG gerados com tamanhos
  - Sugere comandos para visualização
- ✅ **Ambos scripts tornados executáveis** (`chmod +x`)

#### 2. Documentação Completa sobre `min_gap_samples`
- ✅ **Clarificação técnica**: `min_gap_samples` é um **filtro de pós-processamento** aplicado pela pipeline, **não é um parâmetro dos detectores** do scikit-multiflow
- ✅ **Documentos centrais atualizados**:
  - `src/streaming_detector.py`: Docstring e help text do CLI explicam que é pós-processamento
  - `docs/evaluation_metrics_v1.md`: Nota explícita sobre aplicação pós-detecção
  - `scripts/README.md`: Observação clara dissociando de parâmetros de detector
  - `results/README.md`: Esclarece que `predictions_intermediate.csv` contém detecções brutas
  - `README.md` (raiz): Pipeline menciona passo de pós-processamento

- ✅ **Documentação por detector atualizada**:
  - `results/adwin/README.md`: Nota sobre min_gap sendo pipeline post-processing
  - `results/floss/README.md`: Nota sobre filtro aplicado após detecções brutas
  - `results/page_hinkley/README.md`: Nota no bloco de grid explicando pós-processamento

- ✅ **Código fonte documentado**:
  - `src/generate_predictions.py`: Docstring do módulo + comentários em todas as funções `create_param_grid_*`
  - Comentários explicam que `min_gap_samples` testa filtro de supressão temporal

#### 3. Análise Técnica Detalhada
- ✅ **Explicação completa do funcionamento**: Quando detector emite detecção, pipeline verifica se passaram `min_gap_samples` desde última detecção aceite
- ✅ **Exemplo prático**: min_gap=1000 (4s @ 250Hz) → após aceitar detecção, próximas dentro de 1000 samples são ignoradas
- ✅ **Propósito documentado**:
  - Evitar detecções espúrias (detector dispara múltiplas vezes na mesma mudança)
  - Reduzir falsos positivos (detector instável)
  - Respeitar constraints do domínio (mudanças de regime não acontecem em milissegundos)

### 📊 Estado Atual do Projeto

#### Detectores Completos
1. **ADWIN** - 113,355 avaliações (495 configs × 229 ficheiros) ✅
2. **FLOSS** - 989,280 avaliações (4,320 configs × 229 ficheiros) ✅
3. **Page-Hinkley** - Scripts prontos, aguarda execução 🔄
4. **KSWIN** - Scripts prontos, aguarda execução 🔄
5. **HDDM_A** - Scripts prontos, aguarda execução 🔄
6. **HDDM_W** - Scripts prontos, aguarda execução 🔄

#### Comparações Multi-Detector
- **FLOSS vs KSWIN** - Completo ✅
  - Radar chart, bar charts, violin plots
  - Relatório executivo em `results/comparisons/`
  - KSWIN superior em recall (99.44% vs 59.21%)
  - FLOSS superior em precision (20.98% vs 10.74%)

#### Scripts de Automação
**Geração de predições** (6 scripts):
- `generate_adwin.sh`, `generate_page_hinkley.sh`, `generate_kswin.sh`
- `generate_hddm_a.sh`, `generate_hddm_w.sh`, `extend_min_gap_grid.sh`

**Avaliação de métricas** (6 scripts):
- `evaluate_adwin.sh`, `evaluate_page_hinkley.sh`, `evaluate_kswin.sh`
- `evaluate_hddm_a.sh`, `evaluate_hddm_w.sh`, `evaluate_floss.sh` ✨ NOVO

**Visualização** (6 scripts):
- `visualize_adwin.sh`, `visualize_page_hinkley.sh`, `visualize_kswin.sh`
- `visualize_hddm_a.sh`, `visualize_hddm_w.sh`, `visualize_floss.sh` ✨ NOVO

### 📁 Ficheiros Criados/Modificados (Sessão 5)

**Criados**:
- `scripts/evaluate_floss.sh` (75 linhas) - Pipeline de avaliação FLOSS
- `scripts/visualize_floss.sh` (90 linhas) - Pipeline de visualização FLOSS

**Modificados (Documentação min_gap_samples)**:
- `src/streaming_detector.py` - Docstring + help text CLI
- `src/generate_predictions.py` - Docstring módulo + 5 comentários em grids
- `docs/evaluation_metrics_v1.md` - Nota técnica sobre pós-processamento
- `scripts/README.md` - Observação explícita
- `results/README.md` - Esclarece detecções brutas
- `results/adwin/README.md` - Nota sobre filtro pipeline
- `results/floss/README.md` - Nota sobre pós-processamento
- `results/page_hinkley/README.md` - Nota em bloco de grid
- `.github/copilot-memory.md` - Esta atualização

### 🔧 Melhorias de Usabilidade

1. **Scripts FLOSS padronizados**:
   - Mesma estrutura que outros detectores
   - Mensagens coloridas (verde/azul/amarelo)
   - Verificações de pré-requisitos
   - Output informativo com tamanhos de ficheiros
   - Sugestões de próximos passos

2. **Documentação técnica clara**:
   - 9 ficheiros atualizados para explicar min_gap_samples
   - Código fonte comentado para futuros desenvolvedores
   - Exemplos práticos de uso
   - Dissociação clara entre parâmetros de detector vs pipeline

3. **Consistência**:
   - Todos os detectores agora têm 3 scripts (generate/evaluate/visualize)
   - Documentação uniforme em todos os `results/*/README.md`
   - Mensagens de erro/sucesso padronizadas

---

## RESUMO EXECUTIVO DA SESSÃO 4 (2025-11-17)

### ✅ Trabalho Realizado

#### 1. Integração R-Python (FLOSS Detector)
- ✅ **Correção do `evaluate_predictions.py`**: Agora aceita CSVs com formato mínimo (apenas colunas obrigatórias)
  - Colunas opcionais (`gt_indices`, `det_indices`, `duration_samples`) tornadas realmente opcionais
  - Código robusto para lidar com diferentes formatos de CSV
- ✅ **Avaliação completa do FLOSS**: 989,280 avaliações (229 ficheiros × 4,320 configurações)
- ✅ **Documentação completa**: `results/floss/README.md` refletindo dados corretos
- ✅ **Especificação CSV**: `docs/predictions_csv_format_specification.md` completamente validada

#### 2. Sistema de Visualizações Melhorado
- ✅ **Correção de heatmaps**: Detecta automaticamente parâmetros com variação suficiente
- ✅ **Suporte a novos parâmetros**: `regime_threshold`, `regime_landmark` (FLOSS)
- ✅ **Filtros automáticos**: Remove parâmetros constantes (ex: `min_gap_samples=200`)
- ✅ **9 visualizações geradas** para FLOSS com sucesso

#### 3. Comparação Multi-Detector
- ✅ **Script de comparação visual**: `src/visualize_comparison.py` criado
- ✅ **Gráficos comparativos gerados**:
  - Radar chart (6 dimensões de performance)
  - Bar charts (7 métricas chave)
  - Violin plots (distribuições de métricas)
- ✅ **Relatório comparativo**: `results/comparisons/floss_vs_kswin.md` com análise executiva
- ✅ **Correção de bugs**: JSON structure handling para `best_parameters['f3_weighted']`

### 📊 Resultados Principais

#### FLOSS Performance (Dataset Completo: 229 ficheiros)
**Melhor Configuração (F3 Weighted)**:
```
window_size: 25
regime_threshold: 0.85
regime_landmark: 3.0
min_gap_samples: 200
```

**Métricas**:
- F3* = 0.3582 (± 0.2276)
- Recall@10s = 59.21%
- Precision@10s = 20.98%
- FP/min = 2.32
- EDD median = 2.66s
- NAB Standard = -3.11 (± 6.11)

#### Comparação FLOSS vs KSWIN

| Métrica | FLOSS | KSWIN | Vencedor |
|---------|-------|-------|----------|
| **F3*** | 0.3582 | **0.4135** | KSWIN (+15.4%) |
| **Recall@10s** | 59.21% | **99.44%** | KSWIN (+67.9%) |
| **Precision@10s** | **20.98%** | 10.74% | FLOSS (+95.4%) |
| **FP/min** | **2.32** | 9.43 | FLOSS (4.1× menos) |
| **NAB Standard** | **-3.11** | -5.26 | FLOSS (+41.6%) |
| **EDD median** | **2.66s** | 2.89s | FLOSS (8% mais rápido) |

**Recomendações**:
- **KSWIN**: Aplicações clínicas (não pode perder eventos)
- **FLOSS**: Sistemas de alerta (minimizar falsos alarmes)

### 🐛 Bugs Corrigidos

1. **`evaluate_predictions.py`** (Linhas 47-49, 89-93, 113-117):
   - Problema: Esperava colunas opcionais (`gt_indices`, `det_indices`, `duration_samples`)
   - Solução: Verificação `if col in predictions_df.columns` antes de processar

2. **`visualize_results.py`** (Linhas 46-48, 268-285):
   - Problema: Não reconhecia parâmetros do FLOSS, não filtrava parâmetros constantes
   - Solução: Adicionados `regime_threshold`, `regime_landmark` à lista; filtro `df[col].nunique() > 1`

3. **`visualize_comparison.py`** (Linhas 54-56, 224-226):
   - Problema: Tentava acessar `best_parameters` diretamente (é um dict de dicts)
   - Solução: Extrai especificamente `best_parameters['f3_weighted']`

### 📁 Ficheiros Criados/Modificados

**Criados**:
- `src/visualize_comparison.py` (246 linhas) - Comparação visual entre detectores
- `results/floss/README.md` (refazer completo com dados corretos)
- `results/comparisons/floss_vs_kswin.md` - Relatório executivo
- `results/comparisons/floss_vs_kswin_radar.png` - Gráfico radar
- `results/comparisons/floss_vs_kswin_bars.png` - Barras comparativas
- `results/comparisons/floss_vs_kswin_distributions.png` - Distribuições

**Modificados**:
- `src/evaluate_predictions.py` - Colunas opcionais tornadas realmente opcionais
- `src/visualize_results.py` - Suporte a FLOSS + filtro de parâmetros constantes
- `docs/predictions_csv_format_specification.md` - Validação completa

### 🔧 Melhorias Técnicas

1. **Robustez da integração R→Python**:
   - CSV mínimo (11 colunas) validado
   - Compatibilidade com múltiplos formatos
   - Documentação clara de colunas obrigatórias vs opcionais

2. **Visualizações adaptativas**:
   - Detecção automática de parâmetros variáveis
   - Heatmaps funcionam com qualquer número de parâmetros
   - Mensagens informativas quando há poucos parâmetros

3. **Sistema de comparação**:
   - Radar chart com 6 dimensões normalizadas
   - Métricas invertidas corretamente (NAB, EDD, FP/min)
   - Código reutilizável para qualquer par de detectores

---

## 1. Visão Geral do Projeto

### Objetivo
Detectar mudanças de regime (concept drift / change points) em sinais de ECG em fluxo (250 Hz) com processamento estritamente streaming (sem lookahead).

### Datasets Processados (3 datasets completos)

Todos os datasets foram extraídos do **Zenodo 6879233** (afib_regimes) e processados via `src/ecg_preprocess.py`:

| Dataset | Ficheiros | Eventos | Samples | Taxa | Derivação |
|---------|-----------|---------|---------|------|-----------|
| **afib_paroxysmal** | 229 | 1,301 | 41.3M | 250 Hz | Lead II |
| **malignantventricular** | 22 | 592 | 11.6M | 250 Hz | Lead II |
| **vtachyarrhythmias** | 34 | 97 | 4.3M | 250 Hz | Lead II |
| **TOTAL** | **285** | **1,990** | **57.2M** | - | - |

**Configuração de Preprocessamento**:
- Lead/Derivação: Lead II (padrão para análise de ritmo cardíaco)
- Taxa de amostragem: 250 Hz (resample aplicado quando necessário)
- Processamento: `src/ecg_preprocess.py` com `--lead II --resample-to 250`
- Ground truth: Eventos de mudança de regime extraídos de anotações (label_store ∈ {28,32,33})
- Limpeza: Remoção de eventos duplicados e bordas


### Detectores Implementados

#### Python (5 detectores via scikit-multiflow)
1. **ADWIN** - Adaptive Windowing ✅
2. **Page-Hinkley** - Cumulative Sum Test ✅
3. **KSWIN** - Kolmogorov-Smirnov Windowing ✅
4. **HDDM_A** - Hoeffding Drift Detection (Average) ✅
5. **HDDM_W** - Hoeffding Drift Detection (Weighted) ✅

**Nota**: DDM e EDDM foram removidos (inadequados para séries temporais contínuas).

#### R (1 detector integrado)
6. **FLOSS** - Fast Low-rank Online Subspace Tracking ✅
   - Implementado em R (pacote `false.alarm`)
   - Integração R→Python validada
   - 989,280 avaliações completas

### Organização dos Resultados
Cada detector tem estrutura padronizada:
```
results/<detector>/
├── predictions_intermediate.csv
├── metrics_comprehensive_with_nab.csv
├── final_report_with_nab.json
├── visualizations/ (9 gráficos PNG)
└── README.md
```

## 2. Pipeline de Avaliação (3 Passos)- **Predições geradas**: `results/adwin/predi2. **Avaliar Métricas**: `python -m src.evaluate_predictions --predictions results/<detector>/predictions_intermediate.csv`
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

## RESUMO EXECUTIVO DA SESSÃO 6 (2025-11-20)

### ✅ Trabalho Realizado

- ✅ Corrigido IndentationError em `src/streaming_detector.py` que impedia a geração de predições.
- ✅ Atualizados os scripts `scripts/generate_*.sh`, `scripts/evaluate_*.sh` e `scripts/visualize_*.sh` para:
   - aceitar `--max-files` e outros argumentos pass-through para testes rápidos
   - preferir `results/<dataset>` sem sufixos `_full`/_`tidy` (com fallback para compatibilidade)
- ✅ Melhorias em `visualize_results.py` para lidar com NaN em EDD e incluir `regime_threshold`/`regime_landmark` em `parameter_sensitivity.png`.
- ✅ Melhoria do `src/compare_detectors.py`:
   - `--dataset` argumento (default: `afib_paroxysmal`), saída organizada em `comparisons/<dataset>/`
   - Exporta `detector_summary.csv`, `robustness.csv`, e `constraint_tradeoffs.csv`
   - Suporta `--robust-top-n` e `--robust-top-percent` para análises de robustez
- ✅ Removidos flags não usados (`--stat-top-percent`) e simplificado o fluxo de estatísticas
- ✅ Adicionados testes unitários: `tests/test_compare_detectors.py` cobrindo `aggregate_metrics_by_params()` e `generate_robustness_analysis()`

### 🔧 Notas Técnicas / Próximos Passos

- Validar o `compare_detectors.py` em `comparisons/afib_paroxysmal/` e revisar `comparative_report.md` para garantir que a explicação sobre Top-N/Top-% está clara.
- Opcional: adicionar testes adicionais para `aggregate_metrics_by_params()` para cobrir booleans e single-parameter cases.
- Atualizar `results/README.md` com a sintaxe `--dataset` para garantir clareza na nova estrutura de pasta.

### ✅ Fecho do dia
- Status: PRONTO — todas tarefas do dia concluídas; ambiente `.venv` inicializado, testes rodaram e passaram.
