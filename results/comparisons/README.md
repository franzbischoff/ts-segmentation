# Detector Comparisons & Analysis

**Última Atualização**: 2025-12-15
**Estrutura Reorganizada**: Fase 1 (Limpeza + Documentação)

---

## 📁 Navegação Rápida

### 🎯 **1. Comparações por Dataset** → `by_dataset/`

Análises multi-detector por dataset específico. Cada pasta contém:
- **Relatório comparativo** (`comparative_report.md`)
- **Rankings & métricas** (`detector_rankings.csv`, `detector_summary.csv`)
- **Visualizações** (`visualizations/` com gráficos atualizados):
  - `radar_6detectors.png` - Visão holistada (6 detectores × 6 métricas)
  - `f3_vs_fp_scatter.png` - Trade-off performance vs alarmes
  - `heatmap_metrics_comparison.png` - Sensibilidade de detectores
  - `parameter_tradeoffs.png` - Trade-offs multi-objetivo

**Datasets Disponíveis:**
- [**afib_paroxysmal**](by_dataset/afib_paroxysmal/) - 229 ficheiros, 1,301 eventos
- [**malignantventricular**](by_dataset/malignantventricular/) - 22 ficheiros, 592 eventos
- [**vtachyarrhythmias**](by_dataset/vtachyarrhythmias/) - 34 ficheiros, 97 eventos

---

### 🌍 **2. Análises Cross-Dataset** → `cross_dataset/`

Análises robustez e portabilidade de detectores **através de múltiplos datasets**. Incluem as **3 opções de avaliação**:

#### **Opção 1: Performance Ceiling** 🎯
- Pergunta: "Qual é a melhor performance que cada detector consegue atingir (quando tunado)?
- Métrica: F3-weighted máximo por dataset (macro-average)
- Ficheiro: `option1_ceiling_analysis.png`
- Ranking: FLOSS (0.4285) > KSWIN (0.3176) > Page-Hinkley (0.3132)

#### **Opção 2: Parameter Portability** 🚀
- Pergunta: "Consigo usar hiperparâmetros de um dataset noutro sem re-tuning?"
- Métrica: Transferability ratio (params origem → alvo)
- Ficheiro: `option2_portability_heatmap.png`
- Ranking: ADWIN (94.90%) > KSWIN (87.84%) > FLOSS (75.85%)

#### **Opção 3: Unified Robustness Score** ⚖️
- Pergunta: "Qual detector é globalmente robusto (combinando ceiling + portabilidade)?"
- Fórmula: `0.6×(1-ceiling_gap) + 0.4×(1-transfer_variance)`
- Ficheiro: `option3_unified_score_ranking.png`
- Ranking: FLOSS (0.9763) > ADWIN (0.9713) > KSWIN (0.9690)

#### **Production Decision Matrix** 🎓
- Ficheiro: `production_decision_matrix.png`
- Matriz de decisão: Qual detector escolher (por cenário)
  - Novo dataset COM labels? → FLOSS + grid search
  - Novo dataset SEM labels? → ADWIN (95% portabilidade)
  - Balanced? → KSWIN (sweet spot)

---

## 📊 Comparação Rápida: 3 Opções

| Perspetiva | Foco | Top Detector | Score | Use Case |
|-----------|------|---|---|---|
| **Opção 1** | 🎯 Máxima performance | FLOSS | F3=0.4285 | Research, max performance |
| **Opção 2** | 🚀 Portabilidade | ADWIN | 94.90% | Production ready, sem labels |
| **Opção 3** | ⚖️ Robustez unificada | FLOSS | 0.9763 | Escolha holística |

---

## 🔍 Como Usar Esta Estrutura

### Cenário 1: "Qual detector é melhor para dataset X?"
1. Ir a `by_dataset/<dataset>/`
2. Ler `comparative_report.md`
3. Ver gráficos em `visualizations/` (especialmente `heatmap_metrics_comparison.png`)

### Cenário 2: "Qual detector escolho para produção?"
1. Ir a `cross_dataset/`
2. Ler `production_decision_matrix.png`
3. Se tiver labels → usar Opção 1 (FLOSS)
4. Se SEM labels → usar Opção 2 (ADWIN)
5. Se quiser balanced → usar Opção 3 (KSWIN)

### Cenário 3: "Como transferir hiperparâmetros entre datasets?"
1. Ir a `cross_dataset/`
2. Ver `option2_portability_heatmap.png`
3. ADWIN: 95% chance de sucesso (melhor choice)
4. FLOSS: 76% chance (precisa validação)

---

## 📝 Estrutura de Ficheiros

```
comparisons/
├── README.md (este ficheiro)
│
├── by_dataset/
│   ├── afib_paroxysmal/
│   │   ├── README.md
│   │   ├── comparative_report.md
│   │   ├── detector_rankings.csv
│   │   ├── detector_summary.csv
│   │   ├── constraint_tradeoffs.csv
│   │   ├── robustness.csv
│   │   └── visualizations/
│   │       ├── radar_6detectors.png
│   │       ├── f3_vs_fp_scatter.png
│   │       ├── heatmap_metrics_comparison.png
│   │       └── parameter_tradeoffs.png
│   ├── malignantventricular/
│   │   └── (mesma estrutura)
│   └── vtachyarrhythmias/
│       └── (mesma estrutura)
│
├── cross_dataset/
│   ├── README.md
│   ├── option123_summary.png (visão conjunta de 3 opções)
│   ├── option1_ceiling_analysis.png
│   ├── option2_portability_heatmap.png
│   ├── option3_unified_score_ranking.png
│   └── production_decision_matrix.png
│
└── legacy/
    ├── README.md
    ├── floss_vs_kswin.md (relatório antigo, v1)
    └── floss_vs_kswin_*.png (visualizações antigas)
```

---

## 🔄 Roadmap de Visualizações

### Fase 1 ✅ (Concluída - 2025-12-15)
- [x] Reorganizar estrutura de pastas
- [x] Criar layout hierárquico (by_dataset + cross_dataset)
- [x] Preservar ficheiros antigos em legacy/
- [x] Documentação de navegação

### Fase 2 🔜 (Próxima)
- [ ] Gerar visualizações `by_dataset/*/visualizations/`
  - [ ] Script: `src/visualize_comparison_by_dataset.py`
  - [ ] Gera: radar, scatter, heatmap, tradeoffs (6 detectores)

- [ ] Gerar visualizações `cross_dataset/`
  - [ ] Script: `src/visualize_cross_dataset_summary.py`
  - [ ] Gera: ceiling ranking, portability matrix, unified score, decision matrix

- [ ] Criar `generate_comparison_reports.py` (wrapper)
  - [ ] Chama ambos scripts
  - [ ] Organiza saídas automaticamente
  - [ ] Atualiza READMEs

### Fase 3 🔜 (Validação)
- [ ] Executar scripts e validar saídas
- [ ] Verificar dimensões, cores, legibilidade dos gráficos
- [ ] Cleanup e versionamento Git

---

## 🛠️ Geração de Relatórios

Para atualizar todas as comparações de uma vez:

```bash
# Estrutura já existe; aguardando scripts Python da Fase 2
python -m src.generate_comparison_reports \
    --datasets afib_paroxysmal malignantventricular vtachyarrhythmias \
    --output-base results/comparisons
```

Para comparação por dataset específico:

```bash
# Gera comparações + visualizações para um dataset
python -m src.visualize_comparison_by_dataset \
    --dataset afib_paroxysmal \
    --output-dir results/comparisons/by_dataset/afib_paroxysmal/visualizations
```

Para análise cross-dataset:

```bash
# Gera análises de robustez (opções 1, 2, 3) + decision matrix
python -m src.visualize_cross_dataset_summary \
    --output-dir results/comparisons/cross_dataset
```

---

## 📚 Referências Relacionadas

- **Análises Detalhadas por Detector**: [`results/cross_dataset_analysis/`](../cross_dataset_analysis/)
- **Resultados por Dataset**: [`results/<detector>/`](../)
- **Documentação de Métricas**: [`docs/evaluation_metrics_v1.md`](../../docs/evaluation_metrics_v1.md)
- **Guia de Visualizações**: [`docs/visualizations_guide.md`](../../docs/visualizations_guide.md)

---

## 📌 Notas Importantes

1. **Ficheiros PNG em `by_dataset/*/visualizations/` ainda estão a ser gerados** (Fase 2)
   - Por enquanto, usar relatórios `.md` e CSVs para análise

2. **Legacy folder** contém comparações antigas (FLOSS vs KSWIN, v1)
   - Preservadas para histórico; não são atualizadas

3. **Opções 1, 2, 3** são complementares, não excludentes
   - Opção 1: foco em performance máxima
   - Opção 2: foco em portabilidade
   - Opção 3: foco em robustez global
   - Juntas: perspetiva holística

4. **READMEs por dataset** serão criados na Fase 1.3 com:
   - Resumo executivo (top detector por métrica)
   - Recomendações de uso
   - Links para visualizações
   - Detalhes de trade-offs

---

**Próximo Passo**: Fase 1.3 - Criar READMEs estruturais para `by_dataset/` e `cross_dataset/`
