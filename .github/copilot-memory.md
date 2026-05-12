# Projeto: Streaming ECG Regime Change Detection (Sessão de Trabalho - Memória Persistente)

## RESUMO EXECUTIVO DA SESSÃO 14 — 2026-05-12 (Limpeza Final de Documentação)

### ✅ Trabalho de Hoje

**Objetivo**: Remover inconsistências finais na documentação e alinhar a memória do projecto com o estado actual do repositório

#### 1. Limpeza de Artefactos Redundantes
- Removidos os `*.jsonl` que tinham `*.csv` equivalente em `results/`
- Mantidos os `*.json` de relatórios, sumários e execuções two-fold, por não serem duplicados directos

#### 2. Correções de Documentação
- `results/README.md`: corrigido o padrão de entrada de `data/<dataset>_*.csv` e normalizados os nomes reais dos ficheiros de análise cross-dataset
- `docs/visualizations_guide.md`: actualizado para 9 PNGs na Camada 1 e para os nomes reais das saídas da Camada 2
- `results/afib_paroxysmal/adwin/README.md`: corrigido `afib_regimes` para `afib_paroxysmal`
- `.github/copilot-instructions.md`: corrigido o caminho de `docs/evaluation_metrics.md`

### 📌 Estado Actual
- `results/` ficou sem `*.jsonl` redundantes com `*.csv`
- A documentação principal já não refere caminhos/nomes desactualizados para os artefactos activos
- O projecto permanece pronto para revisão final antes da publicação

**Última Atualização**: 2026-05-12 (Sessão 14 - documentação e memória alinhadas)

---

## RESUMO EXECUTIVO DA SESSÃO 13 — 2025-12-23 (Auditoria e Limpeza de Documentação) ✅

### ✅ Trabalho de Hoje

**Objetivo**: Auditar toda documentação do projeto para verificar consistência, informação desatualizada e contradições antes da publicação

#### 1. Auditoria Completa Realizada
- Leu todos os ficheiros em `docs/`, `results/`, `comparisons/`
- Verificou 35+ ficheiros em `tmp/` (marcados como obsoletos)
- Identificou **5 ficheiros com problemas** (crítico a moderado)

#### 2. Problemas Identificados e Corrigidos

**`docs/visualizations_guide.md`** (CRÍTICO)
- ❌ Mencionava script removido (`visualize_comparison.py`)
- ❌ Fases confusas (Fase 1/2/3 vs Camadas 1/2/3)
- ❌ Sem menção a análise SHAP (Sessão 12)
- ✅ **Corrigido**: Reescreveu contexto como "3 camadas" (per-detector, cross-dataset, SHAP), adicionou scripts novos

**`docs/evaluation_metrics.md`** (MODERADO)
- ❌ Não mencionava agregação macro/micro cross-dataset
- ❌ Sem contexto das Opções 1, 2, 3
- ✅ **Corrigido**: Adicionada seção 6 com as 3 opções (ceiling, portability, robustness) com interpretações completas

**`results/README.md`** (MODERADO)
- ❌ Invertia realidade: dizia `results/comparisons/` era ativo quando é legado
- ❌ Faltava documentação de `models_aggregated.csv` (novo em Sessão 12)
- ❌ Faltava menção a `--append` mode
- ✅ **Corrigido**:
  - Clarificado `comparisons/<dataset>/` é ativo, `results/comparisons/` é histórico
  - Adicionado "Cross-Dataset Analysis" (Op1, Op2, Op3)
  - Adicionado "Agregação de Métricas" (models_aggregated.csv)
  - Adicionado "Modo 2: Append Mode" no fluxo
  - Expandido para 4 modos completos

**`comparisons/afib_paroxysmal/comparative_report.md`** (MENOR)
- ❌ Data desatualizada (2025-11-13, 10 dias desatualizada)
- ✅ **Corrigido**: Atualizado para 2025-12-22

**`docs/predictions_csv_format_specification.md`** (MENOR)
- ⚠️ Não tinha documentação sobre `models_aggregated.csv` (novo)
- ✅ **Corrigido**: Adicionada seção "Formato Agregado: models_aggregated.csv" com:
  - Estrutura completa (model_id, parâmetros, n_records, 20 métricas)
  - Exemplo de saída
  - Diferenças vs predictions_intermediate.csv
  - Notas sobre NaN

#### 3. Ficheiros **NÃO** Corrigidos (Conforme Pedido)
- ✅ **`tmp/`**: Mantido como está (35+ ficheiros obsoletos preservados para histórico)

### 📊 Sumário de Correções

| Ficheiro | Severidade | Problema | Status |
|----------|-----------|----------|--------|
| docs/visualizations_guide.md | 🔴 CRÍTICO | Script removido, fases confusas, SHAP omitido | ✅ Corrigido |
| docs/evaluation_metrics.md | 🟡 MODERADO | Sem contexto macro/agregação | ✅ Corrigido |
| results/README.md | 🟡 MODERADO | Inverteu histórico, faltam artefatos | ✅ Corrigido |
| comparisons/afib_paroxysmal/comparative_report.md | 🟡 MODERADO | Data desatualizada | ✅ Corrigido |
| docs/predictions_csv_format_specification.md | 🟢 MENOR | Falta formato agregado | ✅ Corrigido |

### 🎯 Documentação Agora

- ✅ Todas as instruções operacionais atualizadas
- ✅ Arquitetura de análise clara (3 camadas)
- ✅ Todas as opções documentadas (Opções 1, 2, 3)
- ✅ Novos artefatos `models_aggregated.csv` documentados
- ✅ Pipeline completo incluindo `--append` mode
- ✅ Sem contradições entre ficheiros

### 🔄 Pronto para Publicação

Documentação está **congruente, rigorosa e sem contradições**. Pronta para:
- Publicação académica
- Reprodução por terceiros
- Apresentação aos stakeholders

---

## RESUMO EXECUTIVO DA SESSÃO 12 — 2025-12-22 (Preparação para Análise SHAP)

### ✅ Trabalho de Hoje

**Objetivo**: Discutir métodos de análise de importância de parâmetros e criar ficheiros agregados para análise SHAP em R

#### 1. Discussão: Análise de Importância de Parâmetros

**Contexto**: Visualização `parameter_sensitivity.png` usa método descritivo simples
- **Método atual**: Análise univariada (agrupa por parâmetro, calcula média ± desvio padrão)
- **Limitações identificadas**:
  - Não captura interações entre parâmetros
  - Não distingue importância global vs local
  - Não quantifica contribuição relativa (apenas correlação univariada)

**Métodos avançados não utilizados** (discussão teórica):
- ❌ **SHAP** (Shapley Additive exPlanations) - contribuição marginal
- ❌ **FIRM** (Feature Importance Ranking Measure)
- ❌ **ICE** (Individual Conditional Expectation) - efeitos heterogéneos
- ❌ **Permutation Importance** - impacto de permutar parâmetros

**Decisão**: Manter método atual na pipeline Python; análise SHAP será feita externamente em R

#### 2. Interpretação de Gráficos SHAP Dependence

**Exemplo analisado**: `regime_threshold` vs SHAP value (cor: `window_size`)

**Diferenças chave entre gráficos**:

| Aspeto | `parameter_sensitivity.png` | SHAP dependence (R) |
|--------|----------------------------|---------------------|
| **Eixo Y** | Métrica absoluta (0-1) | Contribuição relativa (pode ser negativa) |
| **Baseline** | Não tem referência | Centrado em 0 (predição média) |
| **Cor** | Uniforme | Codifica outro parâmetro (interações) |
| **Tipo** | Univariado descritivo | Multivariado explicativo |

**Interpretação do exemplo SHAP**:
- `regime_threshold < 0.3`: SHAP positivo (+10 a +50) → **melhora** métrica
- `regime_threshold ≥ 0.3`: SHAP negativo (−5 a −20) → **piora** métrica
- Cor (window_size): Modera o efeito negativo (laranja = mais resistente, roxo = mais sensível)

**Conclusão**: SHAP complementa (não substitui) o gráfico atual. Atual mostra "qual configuração é melhor"; SHAP mostra "por que é melhor e como interage"

#### 3. Script Criado: `src/simplify_metrics_for_analysis.py`

**Propósito**: Agregar CSV de métricas por combinação única de parâmetros (modelo)

**Funcionalidades**:
- Auto-detecção de colunas de parâmetros e métricas
- Agregação por combinação única (mean ou median)
- Formato de saída: `model_id` + parâmetros + `n_records` + métricas agregadas
- Suporte para estatísticas adicionais (std, min, max) com `--add-stats`
- Preserva NaN em métricas (`edd_median_s`, `edd_p95_s` ficam NaN quando não há detecções)

**Comando típico**:
```bash
python -m src.simplify_metrics_for_analysis \
  --input results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv \
  --output results/<dataset>/<detector>/models_aggregated.csv \
  --aggregation mean
```

#### 4. Ficheiros Gerados: `models_aggregated.csv` (18 ficheiros)

**Criados para todos os detectores × datasets**:

| Detector | afib_paroxysmal | malignantventricular | vtachyarrhythmias |
|----------|----------------|---------------------|-------------------|
| **adwin** | 594 modelos (229 rec/modelo) | 495 modelos (22 rec) | 495 modelos (34 rec) |
| **page_hinkley** | 600 modelos (229 rec) | 384 modelos (22 rec) | 384 modelos (34 rec) |
| **kswin** | 1,280 modelos (229 rec) | 1,280 modelos (22 rec) | 1,280 modelos (34 rec) |
| **hddm_a** | 320 modelos (229 rec) | 320 modelos (22 rec) | 320 modelos (34 rec) |
| **hddm_w** | 1,280 modelos (229 rec) | 1,280 modelos (22 rec) | 1,280 modelos (34 rec) |
| **floss** | 25,920 modelos (229 rec) | 25,920 modelos (22 rec) | 25,920 modelos (34 rec) |

**Estrutura dos CSV**:
- Coluna 1: `model_id` (model_1, model_2, ...)
- Colunas 2-5: Parâmetros do modelo (ex: window_size, regime_threshold, regime_landmark, min_gap_samples)
- Coluna 6: `n_records` (quantos ficheiros foram agregados)
- Colunas 7-26: Métricas agregadas (20 métricas: f3_weighted, recall_10s, nab_score_standard, etc.)

**Valores NaN preservados**:
- `edd_median_s`: 3,000 modelos (FLOSS malignantventricular) têm NaN → modelos que não detectaram a tempo
- `edd_p95_s`: Mesma quantidade de NaN
- **Decisão**: Manter NaN (indica falha de detecção, informação valiosa para SHAP)

#### 5. Git: Adição Forçada ao Repositório

**Problema**: `results/**/*.csv` está no `.gitignore`
**Solução**: Adição forçada com `git add -f`

**Ficheiros staged (18)**:
```bash
A  results/afib_paroxysmal/adwin/models_aggregated.csv
A  results/afib_paroxysmal/floss/models_aggregated.csv
A  results/afib_paroxysmal/hddm_a/models_aggregated.csv
A  results/afib_paroxysmal/hddm_w/models_aggregated.csv
A  results/afib_paroxysmal/kswin/models_aggregated.csv
A  results/afib_paroxysmal/page_hinkley/models_aggregated.csv
A  results/malignantventricular/adwin/models_aggregated.csv
A  results/malignantventricular/floss/models_aggregated.csv
A  results/malignantventricular/hddm_a/models_aggregated.csv
A  results/malignantventricular/hddm_w/models_aggregated.csv
A  results/malignantventricular/kswin/models_aggregated.csv
A  results/malignantventricular/page_hinkley/models_aggregated.csv
A  results/vtachyarrhythmias/adwin/models_aggregated.csv
A  results/vtachyarrhythmias/floss/models_aggregated.csv
A  results/vtachyarrhythmias/hddm_a/models_aggregated.csv
A  results/vtachyarrhythmias/hddm_w/models_aggregated.csv
A  results/vtachyarrhythmias/kswin/models_aggregated.csv
A  results/vtachyarrhythmias/page_hinkley/models_aggregated.csv
```

**Mensagem de commit sugerida**:
```
Add aggregated model metrics for SHAP analysis

- Add models_aggregated.csv for all 6 detectors × 3 datasets
- Each file aggregates metrics by unique parameter combinations
- Generated using src/simplify_metrics_for_analysis.py
- Format: model_id + parameters + aggregated metrics (mean across files)
- Ready for external analysis (SHAP/FIRM) in R environment
```

### 📊 Impacto

**Antes**: Apenas CSV detalhados (570K linhas para FLOSS malignantventricular)
**Depois**: CSV agregados por modelo (25,920 linhas para FLOSS) + script reutilizável

**Casos de uso**:
1. **Análise SHAP em R**: Usar `models_aggregated.csv` como input para `shapviz::sv_dependence()`
2. **Random Forest/XGBoost**: Treinar modelo preditivo com parâmetros → métricas
3. **Permutation Importance**: Avaliar impacto de permutar parâmetros
4. **Portability para outros projetos**: Script genérico (`simplify_metrics_for_analysis.py`)

### 🎯 Estado Atual

**Scripts Python ativos**:
- ✅ `src/simplify_metrics_for_analysis.py` (196 linhas) - Agregação para SHAP/ML

**Ficheiros prontos para análise externa**:
- ✅ 18 × `models_aggregated.csv` (6 detectores × 3 datasets)
- ✅ Staged no git para commit

**Próxima ação pendente**: Commit dos ficheiros `models_aggregated.csv`

### 🔜 Próximos Passos Sugeridos

#### Análise SHAP em R (Projeto `false.alarm`)
1. **Carregar dados**: `read.csv("models_aggregated.csv")`
2. **Treinar modelo preditivo**: Random Forest com parâmetros → `f3_weighted`
3. **Calcular SHAP values**: `shapviz::shapviz()` + `sv_dependence()`
4. **Gerar gráficos**: Dependence plots, importance ranking, interaction plots

#### Documentação Futura
5. **Criar guia**: `docs/shap_analysis_guide.md` com workflow completo R ↔ Python
6. **Atualizar README**: Mencionar `models_aggregated.csv` como output alternativo

---

## RESUMO EXECUTIVO DA SESSÃO 11 — 2025-12-15 (Fase 2: Visualizações Comparativas COMPLETA ✅)

### ✅ Trabalho de Hoje

**Objetivo**: Criar scripts de visualização comparativa e gerar 16 PNGs para análise multi-detector

#### 1. Scripts Python Criados (3)
- **`src/visualize_comparison_by_dataset.py`** (474 linhas)
  - Gera 4 PNG por dataset: radar, scatter, heatmap, 3D
  - Radar chart: 4 métricas (F3, Recall, Precision, Fast Detection)
  - Métricas 0-1: valores reais (não normalizadas)
  - EDD: escala fixa 0-10s (invertida)
  - Cores consistentes por detector (DETECTOR_COLORS)

- **`src/visualize_cross_dataset_summary.py`** (329 linhas)
  - Gera 4 PNG cross-dataset
  - Option1: Ceiling analysis (bar chart + error bars)
  - Option2: Portability heatmap (transferability %)
  - Option3: Unified score ranking (bar chart)
  - Production decision matrix (bubble chart + quadrantes)

- **`src/generate_comparison_reports.py`** (257 linhas)
  - Wrapper para executar Scripts 1 & 2
  - Atualiza READMEs com timestamps
  - Execution summary com success/failure tracking

#### 2. Visualizações Geradas (16 PNGs)
- **By-Dataset** (12 ficheiros, 4 por dataset):
  - `afib_paroxysmal/`: radar (782KB), scatter (315KB), heatmap (200KB), 3D (699KB)
  - `malignantventricular/`: radar (835KB), scatter (298KB), heatmap (199KB), 3D (677KB)
  - `vtachyarrhythmias/`: radar (733KB), scatter (297KB), heatmap (198KB), 3D (710KB)
- **Cross-Dataset** (4 ficheiros):
  - Option1 ceiling (166KB), Option2 portability (102KB)
  - Option3 unified (161KB), Decision matrix (364KB)

#### 3. Correções de Normalização Implementadas
- **Problema inicial**: FLOSS mostrava zeros no radar (Recall, NAB, EDD)
- **Causa**: Normalização min-max entre detectores (mínimo = 0.0, máximo = 1.0)
- **Solução aplicada**:
  1. **NAB Standard**: Removida inversão (valores maiores = melhor, mesmo negativos)
  2. **F3/Recall/Precision**: Mantidos valores reais 0-100% (não normalizados)
  3. **EDD**: Escala fixa 0-10s com inversão (menor tempo = melhor)
  4. **FP/min e NAB**: Removidos do radar (escalas confusas)
- **Resultado**: Radar com 4 métricas interpretáveis, FLOSS mostra Recall=65% (não 0%)

#### 4. Limpeza de Código
- Removido `src/visualize_comparison.py` (246 linhas, obsoleto)
- Script antigo só comparava 2 detectores
- Substituído por `visualize_comparison_by_dataset.py` (6 detectores)

#### 5. Métricas de Execução
- **Tempo total**: ~13 segundos (3 datasets + cross-dataset)
- **Taxa de sucesso**: 100% (4/4 tasks, 16/16 PNGs)
- **Total de código**: 1,060 linhas Python (3 scripts)
- **Total de PNGs**: 7.8 MB (16 ficheiros)
- **READMEs atualizados**: 7 ficheiros com timestamps

#### 6. Documentação Atualizada
- **`PHASE2_COMPLETION_SUMMARY.md`** (novo) - Sumário executivo completo
- **`PHASE2_ROADMAP.md`** - Marcado como ✅ COMPLETADO (16:24:43)
- READMEs by-dataset atualizados com `Last Updated: 2025-12-15 16:56:XX`
- README cross-dataset atualizado

### 📊 Impacto

**Antes**: Estrutura preparada mas sem visualizações (Fase 1)
**Depois**: 16 PNG visualizações geradas + 3 scripts Python funcionais + documentação completa

**Qualidade**: Radars com métricas interpretáveis (não mais zeros confusos)

### 🎯 Estado Final do Projeto

#### Scripts Ativos (src/)
- `visualize_comparison_by_dataset.py` (474 linhas) - Comparações por dataset
- `visualize_cross_dataset_summary.py` (329 linhas) - Análises cross-dataset
- `generate_comparison_reports.py` (257 linhas) - Wrapper automático
- Outros 13 scripts de pipeline (detectors, evaluation, etc.)

#### Visualizações Completas
- **By-Dataset**: 3 datasets × 4 PNG = 12 ficheiros
- **Cross-Dataset**: 4 PNG (ceiling, portability, unified, decision matrix)
- **Legacy**: 3 PNG antigos preservados

#### Decisões Técnicas Importantes
1. **Normalização**: Métricas 0-1 mantidas em valores reais
2. **EDD Scale**: Escala fixa 0-10s (interpretável)
3. **Radar Simplificado**: 4 métricas core (F3, Recall, Precision, Fast Detection)
4. **Cores Consistentes**: Palette fixa por detector em todos os gráficos

### 🔜 Próximos Passos Sugeridos

#### Curto Prazo (Próxima Sessão)
1. **Análise de Resultados**: Revisar radars e identificar padrões
2. **Decisão de Produção**: Escolher detector(es) baseado em visualizações
3. **Validação Clínica**: Consultar especialistas sobre trade-offs

#### Médio Prazo
4. **Ensemble Methods**: Combinar FLOSS (precision) + ADWIN (recall)?
5. **Confidence Intervals**: Adicionar intervalos de confiança aos gráficos
6. **Interactive Dashboard**: Converter PNGs estáticos para Plotly/Dash

#### Longo Prazo
7. **Automated Testing**: CI/CD para regenerar visualizações em updates
8. **Real-Time Monitoring**: Dashboard streaming para produção
9. **A/B Testing**: Comparar detectores em ambiente clínico real

---

## PLANO PARA PRÓXIMA SESSÃO (2025-12-16)

### Objetivo Principal
**Análise e Interpretação dos Resultados Visuais**

### Tarefas Propostas

#### 1. Revisão de Radars (30-45 min)
- Comparar os 3 radars (afib, malignant, vtachy)
- Identificar padrões consistentes vs específicos por dataset
- Documentar insights em cada README by-dataset

#### 2. Análise Cross-Dataset (30 min)
- Interpretar production decision matrix
- Validar recomendações por quadrante
- Atualizar matriz de decisão se necessário

#### 3. Decisão de Detector(es) para Produção (45 min)
- Definir cenário de uso primário (Recall? Precision? Balanced?)
- Escolher top 3 detectores candidatos
- Propor estratégia de validação clínica

#### 4. Próximos Experimentos (30 min)
- Definir se testa ensemble methods
- Planejar grid search refinado para top detector
- Considerar datasets adicionais (se disponíveis)

### Perguntas a Responder

1. **FLOSS** tem melhor F3 mas recall 65% - aceitável clinicamente?
2. **ADWIN** tem recall 98% mas 10 FP/min - demasiados alarmes?
3. **KSWIN** é o melhor compromisso? Ou precisamos de ensemble?
4. As diferenças entre datasets indicam overfitting ou variabilidade real?
5. EDD ~3s é aceitável para todos os eventos ou precisamos <2s para alguns?

### Recursos Necessários
- Acesso a radars gerados (`results/comparisons/by_dataset/*/visualizations/`)
- Decision matrix (`results/comparisons/cross_dataset/production_decision_matrix.png`)
- Contexto clínico (se disponível): severidade dos eventos, tolerância a FPs

---

## RESUMO EXECUTIVO DA SESSÃO 10 (continuação) — 2025-12-14 (Opção 3 + Visualização única)

### ✅ Entregas novas desta sessão
- **Opção 3 concluída (Unified Robustness Score)**
   - Script: `src/unified_robustness_score.py`
   - Artefatos: `results/cross_dataset_analysis/unified_robustness_option3.{csv,md}`
   - Fórmula: `score = 0.6×(1 - avg_2fold_gap) + 0.4×(1 - transfer_variance)`
   - Ranking final: FLOSS 0.9763, ADWIN 0.9713, KSWIN 0.9690, HDDM_A 0.9509, HDDM_W 0.9426, Page-Hinkley 0.9049
- **Visualização única (Opções 1, 2, 3)**
   - Script: `src/visualize_option123.py`
   - Saída: `results/cross_dataset_analysis/option123_summary.png`
   - Eixos: X = ceiling F3 (Opção 1), Y = transferability média (Opção 2), cor/tamanho = score unificado (Opção 3)
- **README consolidado (3 opções)**
   - `results/cross_dataset_analysis/README.md` agora descreve Opções 1, 2 e 3, inclui comando da visualização e decisão por cenário

### 🔑 Insights atualizados
- FLOSS continua líder em ceiling e também lidera no score unificado, mas perde ~24% ao transferir; precisa de validação/tuning em produção.
- ADWIN mantém a maior portabilidade (94.9%, CV 9.5%) e fica em 2º no score unificado; melhor escolha para produção imediata.
- KSWIN permanece o melhor equilíbrio (2º em ceiling, 2º em portabilidade, 3º no score unificado), indicado para produção com validação rápida.
- Page-Hinkley e HDDM_W apresentam alta instabilidade de parâmetros (CV ~73%); evitar em produção sem testes extensivos.

### 📁 Artefatos principais da sessão
- `results/cross_dataset_analysis/unified_robustness_option3.csv`
- `results/cross_dataset_analysis/unified_robustness_option3.md`
- `results/cross_dataset_analysis/option123_summary.png`
- `results/cross_dataset_analysis/README.md` (atualizado para as 3 opções)

---

## RESUMO EXECUTIVO DA SESSÃO 10 (2025-12-14)

### ✅ Trabalho de Hoje

#### 1. Agregação Two-Fold Cross-Validation
   - `src/aggregate_twofold_analysis.py` (590 linhas) criado para processar todos os 18 relatórios two-fold (6 detectores × 3 datasets)
   - Implementada seleção robusta: para cada detector×dataset, escolhe o fold com **melhor cross-fold F3** (generalização), com tiebreaker por **menor gap**
   - Análise em 3 níveis: Robustness Ranking global, Per-Dataset Comparison, Generalization Gap Analysis

#### 2. Opção 1: Performance Ceiling com Tuning Local (Cross-Dataset Generalization)
   - Adicionada função `generate_cross_dataset_generalization_report()` ao script de agregação
   - **Pergunta respondida**: "Qual detector atinge melhor performance quando otimizado POR dataset?"
   - Usa **cross-fold F3 scores** (mais realistas que intra-fold)
   - **Resultado**: FLOSS domina com F3=0.4285 (±0.13, CV=31%), mas requer tuning por dataset
   - Artefatos: `cross_dataset_generalization_option1.{md,csv}`

#### 3. Opção 2: Leave-One-Dataset-Out Validation (Parameter Portability)
   - `src/test_parameter_portability.py` (380 linhas) criado para testar transferibilidade de hiperparâmetros
   - **Pergunta respondida**: "Posso usar params de um dataset NOUTRO sem re-tuning?"
   - Para cada detector, transfere melhores params de fonte→alvo, mede F3, compara com local best
   - **36 transfers testados** (6 detectores × 3 sources × 2 targets cada)
   - Usa `metrics_comprehensive_with_nab.csv` (filtragem por params exatos)
   - **Resultado SURPRESA**: ADWIN tem 94.90% transferability (melhor que FLOSS com 75.85%)!
   - Artefatos: `parameter_portability_option2.{md,csv}`

### 📊 Insights-Chave

#### Trade-off Fundamental: Ceiling vs Portabilidade
```
Opção 1 (Ceiling):        Opção 2 (Transfer):
1. FLOSS   → 0.4285       1. ADWIN  → 94.90%
2. KSWIN   → 0.3176       2. KSWIN  → 87.84%
3. Page-H  → 0.3132       3. FLOSS  → 75.85% ← PERDE 24%!
4. HDDM_A  → 0.2997       4. HDDM_A → 65.17%
5. ADWIN   → 0.2879       5. Page-H → 54.31%
6. HDDM_W  → 0.1527       6. HDDM_W → 45.64%
```

**Revelação**: Melhor ceiling (FLOSS) ≠ Melhor portabilidade (ADWIN)

#### KSWIN = Sweet Spot
- Performance: 2º lugar (F3=0.3176)
- Portabilidade: 2º lugar (88%)
- **Melhor compromisso** entre potencial e robustez

#### FLOSS Requer Tuning Obrigatório
- Tunado: EXCELENTE (F3=0.4285)
- Transferido: MEDÍOCRE (F3≈0.32, -24% performance)
- **Não usar em produção sem validação/tuning**

#### ADWIN para Quick-Deploy
- Params de qualquer dataset funcionam noutros (95% retention)
- Performance absoluta menor (F3=0.29), mas previsível
- **Ideal quando labels para re-tuning não existem**

### 📁 Artefatos Gerados (Sessão 10)

```
results/cross_dataset_analysis/
├── twofold_analysis_summary.md                  (2.5 KB, resumo executivo)
├── twofold_robustness_{afib,malign,vtachy}.csv (3 CSVs, métricas por dataset)
├── TWOFOLD_ROBUSTNESS_README.md                 (7 KB, documentação completa)
├── cross_dataset_generalization_option1.md      (Opção 1: ceiling analysis)
├── cross_dataset_generalization_option1.csv     (rankings + stats)
├── parameter_portability_option2.md             (Opção 2: 36 transfer tests)
└── parameter_portability_option2.csv            (transferability ratios)
```

### 🎯 Recomendações Para Produção

**Cenário 1: Novo dataset COM LABELS** (pode tunar)
- Usar: FLOSS + grid search
- Performance esperada: F3 ≈ 0.42
- Tempo: ~horas

**Cenário 2: Novo dataset SEM LABELS** (produção imediata)
- Usar: ADWIN com params de afib_paroxysmal
- Performance esperada: F3 ≈ 0.27 (95% do teto)
- Tempo: ~minutos

**Cenário 3: Equilíbrio performance/portabilidade**
- Usar: KSWIN com params de afib_paroxysmal
- Performance esperada: F3 ≈ 0.28 (88% do teto)
- Tempo: ~minutos + validação

### 📌 Estado
- Opções 1 e 2 completas e documentadas
- 34 transfers testados com sucesso (2 falharam por params não presentes no grid)
- Trade-off ceiling vs portabilidade quantificado
- Guias de produção por cenário estabelecidos

### 🔄 Próximos Passos (Backlog Atualizado)

#### **Opção 3: Unified Robustness Score** 📈 (Opcional, estatístico)
- Combinar ambas dimensões numa métrica unificada:
  ```
  Robustness_Score = w1 × (1 - avg_2fold_gap) + w2 × (1 - cross_dataset_variance)
  ```
  onde w1 + w2 = 1 (e.g., w1=0.6, w2=0.4)
- Detecta detectores que generalizam bem DENTRO de datasets E são consistentes ACROSS datasets
- **Pergunta que responde**: "Qual detector é universalmente robusto em ambas as dimensões?"
- **Esforço**: Médio (análise estatística + escolha de pesos)

#### **Outras Tarefas Pendentes**
- Expandir comparações visuais FLOSS vs outros detectores (ponto 2 do backlog Sessão 6)
- Criar matriz de decisão visual (qual detector usar em qual cenário)

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
6. **FLOSS** - Fast Lowcost Online Semantic Segmentation ✅
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
